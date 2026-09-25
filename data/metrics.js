window.OLIST_METRICS = {
  "source": "Olist Marketing Funnel and Brazilian E-Commerce by Olist (Kaggle)",
  "period": {
    "first_contact_min": "2017-06-14",
    "first_contact_max": "2018-05-31",
    "last_won_date": "2018-11-14",
    "focus_start": "2018-01-01",
    "focus_end_inclusive": "2018-04-30",
    "order_purchase_min": "2016-09-04 21:15:19",
    "order_purchase_max": "2018-10-17 17:30:18",
    "observation_end": "2018-10-17 17:30:18"
  },
  "audit": {
    "mql_rows": 8000,
    "deal_rows": 842,
    "duplicate_mql_ids": 0,
    "duplicate_deal_ids": 0,
    "unmatched_deals": 0,
    "missing_origin": 60,
    "negative_close_days": 1,
    "seller_rows": 3095,
    "order_rows": 99441,
    "order_item_rows": 112650,
    "deal_sellers": 842,
    "observable_deal_sellers": 380,
    "unobserved_deal_sellers": 462,
    "multi_seller_orders": 1278,
    "pre_won_delivered_orders": 0
  },
  "overall": {
    "leads": 8000,
    "wins": 842,
    "conversion_pct": 10.53
  },
  "focus": {
    "leads": 4695,
    "wins": 651,
    "conversion_pct": 13.87,
    "channel": [
      {
        "origin": "organic_search",
        "leads": 1392,
        "wins": 213,
        "conversion_pct": 15.3
      },
      {
        "origin": "paid_search",
        "leads": 916,
        "wins": 145,
        "conversion_pct": 15.83
      },
      {
        "origin": "social",
        "leads": 782,
        "wins": 55,
        "conversion_pct": 7.03
      },
      {
        "origin": "unknown",
        "leads": 659,
        "wins": 142,
        "conversion_pct": 21.55
      },
      {
        "origin": "direct_traffic",
        "leads": 302,
        "wins": 47,
        "conversion_pct": 15.56
      },
      {
        "origin": "email",
        "leads": 253,
        "wins": 12,
        "conversion_pct": 4.74
      },
      {
        "origin": "referral",
        "leads": 158,
        "wins": 16,
        "conversion_pct": 10.13
      },
      {
        "origin": "other",
        "leads": 103,
        "wins": 4,
        "conversion_pct": 3.88
      },
      {
        "origin": "display",
        "leads": 64,
        "wins": 4,
        "conversion_pct": 6.25
      },
      {
        "origin": "(missing)",
        "leads": 34,
        "wins": 10,
        "conversion_pct": 29.41
      },
      {
        "origin": "other_publicities",
        "leads": 32,
        "wins": 3,
        "conversion_pct": 9.38
      }
    ]
  },
  "median_nonnegative_close_days": 14.0,
  "monthly": [
    {
      "month": "2017-06",
      "leads": 4,
      "wins": 0,
      "conversion_pct": 0.0
    },
    {
      "month": "2017-07",
      "leads": 239,
      "wins": 2,
      "conversion_pct": 0.84
    },
    {
      "month": "2017-08",
      "leads": 386,
      "wins": 9,
      "conversion_pct": 2.33
    },
    {
      "month": "2017-09",
      "leads": 312,
      "wins": 7,
      "conversion_pct": 2.24
    },
    {
      "month": "2017-10",
      "leads": 416,
      "wins": 14,
      "conversion_pct": 3.37
    },
    {
      "month": "2017-11",
      "leads": 445,
      "wins": 18,
      "conversion_pct": 4.04
    },
    {
      "month": "2017-12",
      "leads": 200,
      "wins": 11,
      "conversion_pct": 5.5
    },
    {
      "month": "2018-01",
      "leads": 1141,
      "wins": 152,
      "conversion_pct": 13.32
    },
    {
      "month": "2018-02",
      "leads": 1028,
      "wins": 149,
      "conversion_pct": 14.49
    },
    {
      "month": "2018-03",
      "leads": 1174,
      "wins": 167,
      "conversion_pct": 14.22
    },
    {
      "month": "2018-04",
      "leads": 1352,
      "wins": 183,
      "conversion_pct": 13.54
    },
    {
      "month": "2018-05",
      "leads": 1303,
      "wins": 130,
      "conversion_pct": 9.98
    }
  ],
  "downstream": {
    "window_days": 90,
    "time_anchor": "first_contact_date",
    "valid_order_status": "delivered",
    "value_field": "order_items.price",
    "complete_mqls": 8000,
    "incomplete_mqls": 0,
    "wins": 842,
    "observed_sellers": 380,
    "activated_sellers_90d": 245,
    "orders_90d": 1693,
    "gmv_90d": 261665.04,
    "gmv_per_mql_90d": 32.71,
    "focus": {
      "start": "2018-01-01",
      "end_exclusive": "2018-05-01",
      "complete_mqls": 4695,
      "wins": 651,
      "observed_sellers": 315,
      "activated_sellers_90d": 199,
      "orders_90d": 1400,
      "gmv_90d": 229124.91
    },
    "channel": [
      {
        "origin": "organic_search",
        "mqls": 1392,
        "wins": 213,
        "observed_sellers": 98,
        "activated_sellers_90d": 60,
        "orders_90d": 352,
        "gmv_90d": 65004.71,
        "conversion_pct": 15.3,
        "observed_pct_of_wins": 46.01,
        "activation_pct_of_mql": 4.31,
        "orders_per_mql_90d": 0.2529,
        "gmv_per_mql_90d": 46.7,
        "actionable": true,
        "low_sample": false
      },
      {
        "origin": "paid_search",
        "mqls": 916,
        "wins": 145,
        "observed_sellers": 79,
        "activated_sellers_90d": 55,
        "orders_90d": 472,
        "gmv_90d": 54415.23,
        "conversion_pct": 15.83,
        "observed_pct_of_wins": 54.48,
        "activation_pct_of_mql": 6.0,
        "orders_per_mql_90d": 0.5153,
        "gmv_per_mql_90d": 59.41,
        "actionable": true,
        "low_sample": false
      },
      {
        "origin": "social",
        "mqls": 782,
        "wins": 55,
        "observed_sellers": 25,
        "activated_sellers_90d": 11,
        "orders_90d": 68,
        "gmv_90d": 6157.61,
        "conversion_pct": 7.03,
        "observed_pct_of_wins": 45.45,
        "activation_pct_of_mql": 1.41,
        "orders_per_mql_90d": 0.087,
        "gmv_per_mql_90d": 7.87,
        "actionable": true,
        "low_sample": false
      },
      {
        "origin": "unknown",
        "mqls": 659,
        "wins": 142,
        "observed_sellers": 67,
        "activated_sellers_90d": 44,
        "orders_90d": 382,
        "gmv_90d": 85308.65,
        "conversion_pct": 21.55,
        "observed_pct_of_wins": 47.18,
        "activation_pct_of_mql": 6.68,
        "orders_per_mql_90d": 0.5797,
        "gmv_per_mql_90d": 129.45,
        "actionable": false,
        "low_sample": false
      },
      {
        "origin": "direct_traffic",
        "mqls": 302,
        "wins": 47,
        "observed_sellers": 26,
        "activated_sellers_90d": 16,
        "orders_90d": 57,
        "gmv_90d": 5970.74,
        "conversion_pct": 15.56,
        "observed_pct_of_wins": 55.32,
        "activation_pct_of_mql": 5.3,
        "orders_per_mql_90d": 0.1887,
        "gmv_per_mql_90d": 19.77,
        "actionable": true,
        "low_sample": false
      },
      {
        "origin": "email",
        "mqls": 253,
        "wins": 12,
        "observed_sellers": 6,
        "activated_sellers_90d": 4,
        "orders_90d": 12,
        "gmv_90d": 5735.29,
        "conversion_pct": 4.74,
        "observed_pct_of_wins": 50.0,
        "activation_pct_of_mql": 1.58,
        "orders_per_mql_90d": 0.0474,
        "gmv_per_mql_90d": 22.67,
        "actionable": true,
        "low_sample": false
      },
      {
        "origin": "referral",
        "mqls": 158,
        "wins": 16,
        "observed_sellers": 7,
        "activated_sellers_90d": 5,
        "orders_90d": 15,
        "gmv_90d": 3542.69,
        "conversion_pct": 10.13,
        "observed_pct_of_wins": 43.75,
        "activation_pct_of_mql": 3.16,
        "orders_per_mql_90d": 0.0949,
        "gmv_per_mql_90d": 22.42,
        "actionable": true,
        "low_sample": false
      },
      {
        "origin": "other",
        "mqls": 103,
        "wins": 4,
        "observed_sellers": 2,
        "activated_sellers_90d": 1,
        "orders_90d": 38,
        "gmv_90d": 2539.69,
        "conversion_pct": 3.88,
        "observed_pct_of_wins": 50.0,
        "activation_pct_of_mql": 0.97,
        "orders_per_mql_90d": 0.3689,
        "gmv_per_mql_90d": 24.66,
        "actionable": true,
        "low_sample": true
      },
      {
        "origin": "display",
        "mqls": 64,
        "wins": 4,
        "observed_sellers": 2,
        "activated_sellers_90d": 1,
        "orders_90d": 1,
        "gmv_90d": 134.0,
        "conversion_pct": 6.25,
        "observed_pct_of_wins": 50.0,
        "activation_pct_of_mql": 1.56,
        "orders_per_mql_90d": 0.0156,
        "gmv_per_mql_90d": 2.09,
        "actionable": true,
        "low_sample": true
      },
      {
        "origin": "(missing)",
        "mqls": 34,
        "wins": 10,
        "observed_sellers": 3,
        "activated_sellers_90d": 2,
        "orders_90d": 3,
        "gmv_90d": 316.3,
        "conversion_pct": 29.41,
        "observed_pct_of_wins": 30.0,
        "activation_pct_of_mql": 5.88,
        "orders_per_mql_90d": 0.0882,
        "gmv_per_mql_90d": 9.3,
        "actionable": false,
        "low_sample": true
      },
      {
        "origin": "other_publicities",
        "mqls": 32,
        "wins": 3,
        "observed_sellers": 0,
        "activated_sellers_90d": 0,
        "orders_90d": 0,
        "gmv_90d": 0.0,
        "conversion_pct": 9.38,
        "observed_pct_of_wins": 0.0,
        "activation_pct_of_mql": 0.0,
        "orders_per_mql_90d": 0.0,
        "gmv_per_mql_90d": 0.0,
        "actionable": true,
        "low_sample": true
      }
    ]
  }
};
