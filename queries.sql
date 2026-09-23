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
