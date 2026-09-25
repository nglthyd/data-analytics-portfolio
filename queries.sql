-- Olist 营销漏斗：基于原始两表，不把成交额误称作利润/ROI。
-- 可用 SQLite 运行；first_contact_date 是 YYYY-MM-DD 文本。

-- 1) 全量核验：每个 mql_id 只计一次。
SELECT COUNT(*) AS leads,
       COUNT(d.mql_id) AS wins,
       ROUND(100.0 * COUNT(d.mql_id) / COUNT(*), 2) AS conversion_pct
FROM olist_marketing_qualified_leads_dataset AS m
LEFT JOIN olist_closed_deals_dataset AS d ON m.mql_id = d.mql_id;

-- 2) 对比 2018 年 1–4 月同一线索期的获客渠道；NULL 单列，不能混入 organic。
SELECT COALESCE(m.origin, '(missing)') AS origin,
       COUNT(*) AS leads,
       COUNT(d.mql_id) AS wins,
       ROUND(100.0 * COUNT(d.mql_id) / COUNT(*), 2) AS conversion_pct
FROM olist_marketing_qualified_leads_dataset AS m
LEFT JOIN olist_closed_deals_dataset AS d ON m.mql_id = d.mql_id
WHERE m.first_contact_date >= '2018-01-01'
  AND m.first_contact_date < '2018-05-01'
GROUP BY COALESCE(m.origin, '(missing)')
ORDER BY leads DESC, origin;

-- 3) 月度线索期诊断。不可把不同月的渠道占比变化当作渠道的因果作用。
SELECT SUBSTR(m.first_contact_date, 1, 7) AS contact_month,
       COUNT(*) AS leads,
       COUNT(d.mql_id) AS wins,
       ROUND(100.0 * COUNT(d.mql_id) / COUNT(*), 2) AS conversion_pct
FROM olist_marketing_qualified_leads_dataset AS m
LEFT JOIN olist_closed_deals_dataset AS d ON m.mql_id = d.mql_id
GROUP BY SUBSTR(m.first_contact_date, 1, 7)
ORDER BY contact_month;

-- 4) 成交商家映射覆盖。未进入公开订单样本的成交商家必须保留在覆盖率分母中。
SELECT COUNT(d.seller_id) AS deal_sellers,
       SUM(CASE WHEN s.seller_id IS NOT NULL THEN 1 ELSE 0 END) AS observable_deal_sellers,
       SUM(CASE WHEN s.seller_id IS NULL THEN 1 ELSE 0 END) AS unobserved_deal_sellers
FROM olist_closed_deals_dataset AS d
LEFT JOIN olist_sellers_dataset AS s ON d.seller_id = s.seller_id;

-- 5) 每条完整观察 MQL 保留一行，再汇总 90 天可观测价值。
WITH observation AS (
    SELECT MAX(order_purchase_timestamp) AS observation_end
    FROM olist_orders_dataset
),
eligible_mql AS (
    SELECT m.mql_id,
           m.first_contact_date,
           m.origin
    FROM olist_marketing_qualified_leads_dataset AS m
    CROSS JOIN observation AS x
    WHERE DATETIME(m.first_contact_date, '+90 days') <= x.observation_end
),
lead_map AS (
    SELECT e.mql_id,
           e.first_contact_date,
           e.origin,
           d.won_date,
           d.seller_id,
           CASE WHEN d.mql_id IS NOT NULL THEN 1 ELSE 0 END AS won,
           CASE WHEN s.seller_id IS NOT NULL THEN 1 ELSE 0 END AS observed_seller
    FROM eligible_mql AS e
    LEFT JOIN olist_closed_deals_dataset AS d ON e.mql_id = d.mql_id
    LEFT JOIN olist_sellers_dataset AS s ON d.seller_id = s.seller_id
),
valid_item_rows AS (
    SELECT lm.mql_id,
           oi.order_id,
           oi.price
    FROM lead_map AS lm
    JOIN olist_order_items_dataset AS oi ON lm.seller_id = oi.seller_id
    JOIN olist_orders_dataset AS o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_purchase_timestamp >= lm.won_date
      AND o.order_purchase_timestamp >= lm.first_contact_date
      AND o.order_purchase_timestamp < DATETIME(lm.first_contact_date, '+90 days')
),
lead_value AS (
    SELECT mql_id,
           COUNT(DISTINCT order_id) AS orders_90d,
           SUM(price) AS gmv_90d
    FROM valid_item_rows
    GROUP BY mql_id
)
SELECT COUNT(*) AS complete_mqls,
       SUM(lm.won) AS wins,
       SUM(lm.observed_seller) AS observed_sellers,
       SUM(CASE WHEN COALESCE(v.orders_90d, 0) > 0 THEN 1 ELSE 0 END) AS activated_sellers_90d,
       SUM(COALESCE(v.orders_90d, 0)) AS orders_90d,
       ROUND(SUM(COALESCE(v.gmv_90d, 0.0)), 2) AS gmv_90d
FROM lead_map AS lm
LEFT JOIN lead_value AS v ON lm.mql_id = v.mql_id;

-- 6) 同一线索期、同一 90 天观察窗下的渠道价值；unknown/缺失只做数据质量提示。
WITH observation AS (
    SELECT MAX(order_purchase_timestamp) AS observation_end
    FROM olist_orders_dataset
),
eligible_mql AS (
    SELECT m.mql_id,
           m.first_contact_date,
           COALESCE(m.origin, '(missing)') AS origin
    FROM olist_marketing_qualified_leads_dataset AS m
    CROSS JOIN observation AS x
    WHERE DATETIME(m.first_contact_date, '+90 days') <= x.observation_end
      AND m.first_contact_date >= '2018-01-01'
      AND m.first_contact_date < '2018-05-01'
),
lead_map AS (
    SELECT e.mql_id,
           e.first_contact_date,
           e.origin,
           d.won_date,
           d.seller_id,
           CASE WHEN d.mql_id IS NOT NULL THEN 1 ELSE 0 END AS won,
           CASE WHEN s.seller_id IS NOT NULL THEN 1 ELSE 0 END AS observed_seller
    FROM eligible_mql AS e
    LEFT JOIN olist_closed_deals_dataset AS d ON e.mql_id = d.mql_id
    LEFT JOIN olist_sellers_dataset AS s ON d.seller_id = s.seller_id
),
valid_item_rows AS (
    SELECT lm.mql_id,
           oi.order_id,
           oi.price
    FROM lead_map AS lm
    JOIN olist_order_items_dataset AS oi ON lm.seller_id = oi.seller_id
    JOIN olist_orders_dataset AS o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_purchase_timestamp >= lm.won_date
      AND o.order_purchase_timestamp >= lm.first_contact_date
      AND o.order_purchase_timestamp < DATETIME(lm.first_contact_date, '+90 days')
),
lead_value AS (
    SELECT mql_id,
           COUNT(DISTINCT order_id) AS orders_90d,
           SUM(price) AS gmv_90d
    FROM valid_item_rows
    GROUP BY mql_id
),
channel_value AS (
    SELECT lm.origin,
           COUNT(*) AS mqls,
           SUM(lm.won) AS wins,
           SUM(lm.observed_seller) AS observed_sellers,
           SUM(CASE WHEN COALESCE(v.orders_90d, 0) > 0 THEN 1 ELSE 0 END) AS activated_sellers_90d,
           SUM(COALESCE(v.orders_90d, 0)) AS orders_90d,
           SUM(COALESCE(v.gmv_90d, 0.0)) AS gmv_90d
    FROM lead_map AS lm
    LEFT JOIN lead_value AS v ON lm.mql_id = v.mql_id
    GROUP BY lm.origin
)
SELECT origin,
       mqls,
       wins,
       observed_sellers,
       activated_sellers_90d,
       orders_90d,
       ROUND(gmv_90d, 2) AS gmv_90d,
       ROUND(100.0 * wins / mqls, 2) AS conversion_pct,
       CASE WHEN wins = 0 THEN NULL ELSE ROUND(100.0 * observed_sellers / wins, 2) END AS observed_pct_of_wins,
       ROUND(100.0 * activated_sellers_90d / mqls, 2) AS activation_pct_of_mql,
       ROUND(1.0 * orders_90d / mqls, 4) AS orders_per_mql_90d,
       ROUND(1.0 * gmv_90d / mqls, 2) AS gmv_per_mql_90d
FROM channel_value
ORDER BY mqls DESC, origin;
