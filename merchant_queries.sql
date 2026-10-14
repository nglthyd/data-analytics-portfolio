WITH closed AS (
    SELECT
        m.mql_id,
        d.seller_id,
        COALESCE(m.origin, '(missing)') AS origin_group,
        m.first_contact_date AS contact_date,
        d.won_date,
        CASE WHEN s.seller_id IS NULL THEN 0 ELSE 1 END AS observed_seller,
        CASE
            WHEN datetime(m.first_contact_date, '+90 days') <= datetime(:observation_end)
            THEN 1 ELSE 0
        END AS complete_90d,
        CASE
            WHEN datetime(d.won_date) < datetime(m.first_contact_date)
            THEN 1 ELSE 0
        END AS chronology_error
    FROM closed_deals AS d
    JOIN mql AS m ON m.mql_id = d.mql_id
    LEFT JOIN sellers AS s ON s.seller_id = d.seller_id
),
seller_orders AS (
    SELECT
        i.seller_id,
        i.order_id,
        o.order_purchase_timestamp,
        SUM(CAST(i.price AS REAL)) AS order_gmv
    FROM order_items AS i
    JOIN orders AS o ON o.order_id = i.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY i.seller_id, i.order_id, o.order_purchase_timestamp
),
observed_value AS (
    SELECT
        c.mql_id,
        COUNT(so.order_id) AS orders_90d,
        COALESCE(SUM(so.order_gmv), 0.0) AS gmv_90d
    FROM closed AS c
    LEFT JOIN seller_orders AS so
      ON so.seller_id = c.seller_id
     AND datetime(so.order_purchase_timestamp) >= datetime(c.won_date)
     AND datetime(so.order_purchase_timestamp) >= datetime(c.contact_date)
     AND datetime(so.order_purchase_timestamp) < datetime(c.contact_date, '+90 days')
    WHERE c.observed_seller = 1
      AND c.complete_90d = 1
      AND c.chronology_error = 0
    GROUP BY c.mql_id
)
SELECT
    c.mql_id,
    c.seller_id,
    c.origin_group,
    c.contact_date,
    c.won_date,
    c.observed_seller,
    c.complete_90d,
    c.chronology_error,
    CASE
        WHEN c.observed_seller = 1
         AND c.complete_90d = 1
         AND c.chronology_error = 0
        THEN 1 ELSE 0
    END AS eligible,
    CASE
        WHEN c.chronology_error = 1 THEN 'chronology_error'
        WHEN c.complete_90d = 0 THEN 'incomplete_window'
        WHEN c.observed_seller = 0 THEN 'unknown_coverage'
        WHEN COALESCE(v.orders_90d, 0) = 0 THEN 'observable_no_activation'
        ELSE 'activated'
    END AS status,
    CASE
        WHEN c.observed_seller = 1
         AND c.complete_90d = 1
         AND c.chronology_error = 0
        THEN COALESCE(v.orders_90d, 0)
        ELSE NULL
    END AS orders_90d,
    CASE
        WHEN c.observed_seller = 1
         AND c.complete_90d = 1
         AND c.chronology_error = 0
        THEN COALESCE(v.gmv_90d, 0.0)
        ELSE NULL
    END AS gmv_90d
FROM closed AS c
LEFT JOIN observed_value AS v ON v.mql_id = c.mql_id
ORDER BY c.mql_id
