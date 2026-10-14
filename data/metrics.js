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
  },
  "merchant_ops": {
    "summary": {
      "total_closed": 842,
      "observable_closed": 380,
      "unknown_coverage_closed": 462,
      "incomplete_closed": 0,
      "chronology_error_closed": 1,
      "eligible_closed": 379,
      "activated": 245,
      "observable_no_activation": 134,
      "activation_pct_of_eligible": 64.6438,
      "orders_90d": 1693,
      "gmv_90d": 261665.04,
      "gmv_per_seller_order": 154.557
    },
    "states": [
      {
        "status": "chronology_error",
        "count": 1
      },
      {
        "status": "incomplete_window",
        "count": 0
      },
      {
        "status": "unknown_coverage",
        "count": 462
      },
      {
        "status": "observable_no_activation",
        "count": 134
      },
      {
        "status": "activated",
        "count": 245
      }
    ],
    "cohorts": [
      {
        "contact_month": "2017-07",
        "total_closed": 2,
        "observable_closed": 1,
        "eligible_closed": 1,
        "activated": 0,
        "activation_pct_of_eligible": 0.0,
        "gmv_90d": 0.0,
        "low_sample": true
      },
      {
        "contact_month": "2017-08",
        "total_closed": 9,
        "observable_closed": 3,
        "eligible_closed": 3,
        "activated": 0,
        "activation_pct_of_eligible": 0.0,
        "gmv_90d": 0.0,
        "low_sample": true
      },
      {
        "contact_month": "2017-09",
        "total_closed": 7,
        "observable_closed": 0,
        "eligible_closed": 0,
        "activated": 0,
        "activation_pct_of_eligible": null,
        "gmv_90d": 0.0,
        "low_sample": true
      },
      {
        "contact_month": "2017-10",
        "total_closed": 14,
        "observable_closed": 4,
        "eligible_closed": 4,
        "activated": 0,
        "activation_pct_of_eligible": 0.0,
        "gmv_90d": 0.0,
        "low_sample": true
      },
      {
        "contact_month": "2017-11",
        "total_closed": 18,
        "observable_closed": 6,
        "eligible_closed": 6,
        "activated": 2,
        "activation_pct_of_eligible": 33.3333,
        "gmv_90d": 297.98,
        "low_sample": true
      },
      {
        "contact_month": "2017-12",
        "total_closed": 11,
        "observable_closed": 5,
        "eligible_closed": 5,
        "activated": 0,
        "activation_pct_of_eligible": 0.0,
        "gmv_90d": 0.0,
        "low_sample": true
      },
      {
        "contact_month": "2018-01",
        "total_closed": 152,
        "observable_closed": 76,
        "eligible_closed": 76,
        "activated": 38,
        "activation_pct_of_eligible": 50.0,
        "gmv_90d": 95982.57,
        "low_sample": false
      },
      {
        "contact_month": "2018-02",
        "total_closed": 149,
        "observable_closed": 74,
        "eligible_closed": 74,
        "activated": 45,
        "activation_pct_of_eligible": 60.8108,
        "gmv_90d": 25258.65,
        "low_sample": false
      },
      {
        "contact_month": "2018-03",
        "total_closed": 167,
        "observable_closed": 68,
        "eligible_closed": 67,
        "activated": 43,
        "activation_pct_of_eligible": 64.1791,
        "gmv_90d": 47702.64,
        "low_sample": false
      },
      {
        "contact_month": "2018-04",
        "total_closed": 183,
        "observable_closed": 97,
        "eligible_closed": 97,
        "activated": 73,
        "activation_pct_of_eligible": 75.2577,
        "gmv_90d": 60181.05,
        "low_sample": false
      },
      {
        "contact_month": "2018-05",
        "total_closed": 130,
        "observable_closed": 46,
        "eligible_closed": 46,
        "activated": 44,
        "activation_pct_of_eligible": 95.6522,
        "gmv_90d": 32242.15,
        "low_sample": false
      }
    ],
    "concentration": {
      "n": 245,
      "top10_count": 25,
      "top20_count": 49,
      "top10_gmv_pct": 62.3177,
      "top20_gmv_pct": 76.6898,
      "curve": [
        {
          "rank": 1,
          "merchants_pct": 0.4082,
          "gmv_pct": 18.587
        },
        {
          "rank": 2,
          "merchants_pct": 0.8163,
          "gmv_pct": 27.6792
        },
        {
          "rank": 3,
          "merchants_pct": 1.2245,
          "gmv_pct": 33.4792
        },
        {
          "rank": 4,
          "merchants_pct": 1.6327,
          "gmv_pct": 37.1651
        },
        {
          "rank": 5,
          "merchants_pct": 2.0408,
          "gmv_pct": 39.429
        },
        {
          "rank": 6,
          "merchants_pct": 2.449,
          "gmv_pct": 41.5348
        },
        {
          "rank": 7,
          "merchants_pct": 2.8571,
          "gmv_pct": 43.4968
        },
        {
          "rank": 8,
          "merchants_pct": 3.2653,
          "gmv_pct": 45.3684
        },
        {
          "rank": 9,
          "merchants_pct": 3.6735,
          "gmv_pct": 46.7119
        },
        {
          "rank": 10,
          "merchants_pct": 4.0816,
          "gmv_pct": 47.9922
        },
        {
          "rank": 11,
          "merchants_pct": 4.4898,
          "gmv_pct": 49.198
        },
        {
          "rank": 12,
          "merchants_pct": 4.898,
          "gmv_pct": 50.283
        },
        {
          "rank": 13,
          "merchants_pct": 5.3061,
          "gmv_pct": 51.3604
        },
        {
          "rank": 14,
          "merchants_pct": 5.7143,
          "gmv_pct": 52.3903
        },
        {
          "rank": 15,
          "merchants_pct": 6.1224,
          "gmv_pct": 53.401
        },
        {
          "rank": 16,
          "merchants_pct": 6.5306,
          "gmv_pct": 54.3716
        },
        {
          "rank": 17,
          "merchants_pct": 6.9388,
          "gmv_pct": 55.3371
        },
        {
          "rank": 18,
          "merchants_pct": 7.3469,
          "gmv_pct": 56.2875
        },
        {
          "rank": 19,
          "merchants_pct": 7.7551,
          "gmv_pct": 57.2335
        },
        {
          "rank": 20,
          "merchants_pct": 8.1633,
          "gmv_pct": 58.1691
        },
        {
          "rank": 21,
          "merchants_pct": 8.5714,
          "gmv_pct": 59.0504
        },
        {
          "rank": 22,
          "merchants_pct": 8.9796,
          "gmv_pct": 59.906
        },
        {
          "rank": 23,
          "merchants_pct": 9.3878,
          "gmv_pct": 60.7241
        },
        {
          "rank": 24,
          "merchants_pct": 9.7959,
          "gmv_pct": 61.5247
        },
        {
          "rank": 25,
          "merchants_pct": 10.2041,
          "gmv_pct": 62.3177
        },
        {
          "rank": 26,
          "merchants_pct": 10.6122,
          "gmv_pct": 63.0904
        },
        {
          "rank": 27,
          "merchants_pct": 11.0204,
          "gmv_pct": 63.8177
        },
        {
          "rank": 28,
          "merchants_pct": 11.4286,
          "gmv_pct": 64.541
        },
        {
          "rank": 29,
          "merchants_pct": 11.8367,
          "gmv_pct": 65.2584
        },
        {
          "rank": 30,
          "merchants_pct": 12.2449,
          "gmv_pct": 65.9734
        },
        {
          "rank": 31,
          "merchants_pct": 12.6531,
          "gmv_pct": 66.6878
        },
        {
          "rank": 32,
          "merchants_pct": 13.0612,
          "gmv_pct": 67.3986
        },
        {
          "rank": 33,
          "merchants_pct": 13.4694,
          "gmv_pct": 68.078
        },
        {
          "rank": 34,
          "merchants_pct": 13.8776,
          "gmv_pct": 68.741
        },
        {
          "rank": 35,
          "merchants_pct": 14.2857,
          "gmv_pct": 69.4032
        },
        {
          "rank": 36,
          "merchants_pct": 14.6939,
          "gmv_pct": 70.0425
        },
        {
          "rank": 37,
          "merchants_pct": 15.102,
          "gmv_pct": 70.6652
        },
        {
          "rank": 38,
          "merchants_pct": 15.5102,
          "gmv_pct": 71.2811
        },
        {
          "rank": 39,
          "merchants_pct": 15.9184,
          "gmv_pct": 71.8372
        },
        {
          "rank": 40,
          "merchants_pct": 16.3265,
          "gmv_pct": 72.384
        },
        {
          "rank": 41,
          "merchants_pct": 16.7347,
          "gmv_pct": 72.9005
        },
        {
          "rank": 42,
          "merchants_pct": 17.1429,
          "gmv_pct": 73.4008
        },
        {
          "rank": 43,
          "merchants_pct": 17.551,
          "gmv_pct": 73.8907
        },
        {
          "rank": 44,
          "merchants_pct": 17.9592,
          "gmv_pct": 74.3761
        },
        {
          "rank": 45,
          "merchants_pct": 18.3673,
          "gmv_pct": 74.8509
        },
        {
          "rank": 46,
          "merchants_pct": 18.7755,
          "gmv_pct": 75.3242
        },
        {
          "rank": 47,
          "merchants_pct": 19.1837,
          "gmv_pct": 75.793
        },
        {
          "rank": 48,
          "merchants_pct": 19.5918,
          "gmv_pct": 76.2508
        },
        {
          "rank": 49,
          "merchants_pct": 20.0,
          "gmv_pct": 76.6898
        },
        {
          "rank": 50,
          "merchants_pct": 20.4082,
          "gmv_pct": 77.1158
        },
        {
          "rank": 51,
          "merchants_pct": 20.8163,
          "gmv_pct": 77.5407
        },
        {
          "rank": 52,
          "merchants_pct": 21.2245,
          "gmv_pct": 77.9576
        },
        {
          "rank": 53,
          "merchants_pct": 21.6327,
          "gmv_pct": 78.368
        },
        {
          "rank": 54,
          "merchants_pct": 22.0408,
          "gmv_pct": 78.7692
        },
        {
          "rank": 55,
          "merchants_pct": 22.449,
          "gmv_pct": 79.1552
        },
        {
          "rank": 56,
          "merchants_pct": 22.8571,
          "gmv_pct": 79.5369
        },
        {
          "rank": 57,
          "merchants_pct": 23.2653,
          "gmv_pct": 79.9133
        },
        {
          "rank": 58,
          "merchants_pct": 23.6735,
          "gmv_pct": 80.278
        },
        {
          "rank": 59,
          "merchants_pct": 24.0816,
          "gmv_pct": 80.6364
        },
        {
          "rank": 60,
          "merchants_pct": 24.4898,
          "gmv_pct": 80.9938
        },
        {
          "rank": 61,
          "merchants_pct": 24.898,
          "gmv_pct": 81.3502
        },
        {
          "rank": 62,
          "merchants_pct": 25.3061,
          "gmv_pct": 81.7013
        },
        {
          "rank": 63,
          "merchants_pct": 25.7143,
          "gmv_pct": 82.0451
        },
        {
          "rank": 64,
          "merchants_pct": 26.1224,
          "gmv_pct": 82.3882
        },
        {
          "rank": 65,
          "merchants_pct": 26.5306,
          "gmv_pct": 82.7254
        },
        {
          "rank": 66,
          "merchants_pct": 26.9388,
          "gmv_pct": 83.0479
        },
        {
          "rank": 67,
          "merchants_pct": 27.3469,
          "gmv_pct": 83.3597
        },
        {
          "rank": 68,
          "merchants_pct": 27.7551,
          "gmv_pct": 83.6647
        },
        {
          "rank": 69,
          "merchants_pct": 28.1633,
          "gmv_pct": 83.9635
        },
        {
          "rank": 70,
          "merchants_pct": 28.5714,
          "gmv_pct": 84.261
        },
        {
          "rank": 71,
          "merchants_pct": 28.9796,
          "gmv_pct": 84.5518
        },
        {
          "rank": 72,
          "merchants_pct": 29.3878,
          "gmv_pct": 84.8375
        },
        {
          "rank": 73,
          "merchants_pct": 29.7959,
          "gmv_pct": 85.1166
        },
        {
          "rank": 74,
          "merchants_pct": 30.2041,
          "gmv_pct": 85.3851
        },
        {
          "rank": 75,
          "merchants_pct": 30.6122,
          "gmv_pct": 85.651
        },
        {
          "rank": 76,
          "merchants_pct": 31.0204,
          "gmv_pct": 85.9124
        },
        {
          "rank": 77,
          "merchants_pct": 31.4286,
          "gmv_pct": 86.1681
        },
        {
          "rank": 78,
          "merchants_pct": 31.8367,
          "gmv_pct": 86.4222
        },
        {
          "rank": 79,
          "merchants_pct": 32.2449,
          "gmv_pct": 86.6761
        },
        {
          "rank": 80,
          "merchants_pct": 32.6531,
          "gmv_pct": 86.9257
        },
        {
          "rank": 81,
          "merchants_pct": 33.0612,
          "gmv_pct": 87.1669
        },
        {
          "rank": 82,
          "merchants_pct": 33.4694,
          "gmv_pct": 87.4057
        },
        {
          "rank": 83,
          "merchants_pct": 33.8776,
          "gmv_pct": 87.6423
        },
        {
          "rank": 84,
          "merchants_pct": 34.2857,
          "gmv_pct": 87.8677
        },
        {
          "rank": 85,
          "merchants_pct": 34.6939,
          "gmv_pct": 88.0878
        },
        {
          "rank": 86,
          "merchants_pct": 35.102,
          "gmv_pct": 88.3068
        },
        {
          "rank": 87,
          "merchants_pct": 35.5102,
          "gmv_pct": 88.5245
        },
        {
          "rank": 88,
          "merchants_pct": 35.9184,
          "gmv_pct": 88.7419
        },
        {
          "rank": 89,
          "merchants_pct": 36.3265,
          "gmv_pct": 88.9571
        },
        {
          "rank": 90,
          "merchants_pct": 36.7347,
          "gmv_pct": 89.1711
        },
        {
          "rank": 91,
          "merchants_pct": 37.1429,
          "gmv_pct": 89.3805
        },
        {
          "rank": 92,
          "merchants_pct": 37.551,
          "gmv_pct": 89.5861
        },
        {
          "rank": 93,
          "merchants_pct": 37.9592,
          "gmv_pct": 89.7896
        },
        {
          "rank": 94,
          "merchants_pct": 38.3673,
          "gmv_pct": 89.9902
        },
        {
          "rank": 95,
          "merchants_pct": 38.7755,
          "gmv_pct": 90.1906
        },
        {
          "rank": 96,
          "merchants_pct": 39.1837,
          "gmv_pct": 90.3843
        },
        {
          "rank": 97,
          "merchants_pct": 39.5918,
          "gmv_pct": 90.5754
        },
        {
          "rank": 98,
          "merchants_pct": 40.0,
          "gmv_pct": 90.7623
        },
        {
          "rank": 99,
          "merchants_pct": 40.4082,
          "gmv_pct": 90.9415
        },
        {
          "rank": 100,
          "merchants_pct": 40.8163,
          "gmv_pct": 91.1153
        },
        {
          "rank": 101,
          "merchants_pct": 41.2245,
          "gmv_pct": 91.287
        },
        {
          "rank": 102,
          "merchants_pct": 41.6327,
          "gmv_pct": 91.4541
        },
        {
          "rank": 103,
          "merchants_pct": 42.0408,
          "gmv_pct": 91.6185
        },
        {
          "rank": 104,
          "merchants_pct": 42.449,
          "gmv_pct": 91.7809
        },
        {
          "rank": 105,
          "merchants_pct": 42.8571,
          "gmv_pct": 91.9345
        },
        {
          "rank": 106,
          "merchants_pct": 43.2653,
          "gmv_pct": 92.0858
        },
        {
          "rank": 107,
          "merchants_pct": 43.6735,
          "gmv_pct": 92.2349
        },
        {
          "rank": 108,
          "merchants_pct": 44.0816,
          "gmv_pct": 92.3835
        },
        {
          "rank": 109,
          "merchants_pct": 44.4898,
          "gmv_pct": 92.5284
        },
        {
          "rank": 110,
          "merchants_pct": 44.898,
          "gmv_pct": 92.6678
        },
        {
          "rank": 111,
          "merchants_pct": 45.3061,
          "gmv_pct": 92.8072
        },
        {
          "rank": 112,
          "merchants_pct": 45.7143,
          "gmv_pct": 92.9401
        },
        {
          "rank": 113,
          "merchants_pct": 46.1224,
          "gmv_pct": 93.0688
        },
        {
          "rank": 114,
          "merchants_pct": 46.5306,
          "gmv_pct": 93.1949
        },
        {
          "rank": 115,
          "merchants_pct": 46.9388,
          "gmv_pct": 93.321
        },
        {
          "rank": 116,
          "merchants_pct": 47.3469,
          "gmv_pct": 93.4467
        },
        {
          "rank": 117,
          "merchants_pct": 47.7551,
          "gmv_pct": 93.5719
        },
        {
          "rank": 118,
          "merchants_pct": 48.1633,
          "gmv_pct": 93.6956
        },
        {
          "rank": 119,
          "merchants_pct": 48.5714,
          "gmv_pct": 93.8179
        },
        {
          "rank": 120,
          "merchants_pct": 48.9796,
          "gmv_pct": 93.9399
        },
        {
          "rank": 121,
          "merchants_pct": 49.3878,
          "gmv_pct": 94.0614
        },
        {
          "rank": 122,
          "merchants_pct": 49.7959,
          "gmv_pct": 94.1786
        },
        {
          "rank": 123,
          "merchants_pct": 50.2041,
          "gmv_pct": 94.2933
        },
        {
          "rank": 124,
          "merchants_pct": 50.6122,
          "gmv_pct": 94.3998
        },
        {
          "rank": 125,
          "merchants_pct": 51.0204,
          "gmv_pct": 94.506
        },
        {
          "rank": 126,
          "merchants_pct": 51.4286,
          "gmv_pct": 94.6088
        },
        {
          "rank": 127,
          "merchants_pct": 51.8367,
          "gmv_pct": 94.7081
        },
        {
          "rank": 128,
          "merchants_pct": 52.2449,
          "gmv_pct": 94.8045
        },
        {
          "rank": 129,
          "merchants_pct": 52.6531,
          "gmv_pct": 94.8987
        },
        {
          "rank": 130,
          "merchants_pct": 53.0612,
          "gmv_pct": 94.9887
        },
        {
          "rank": 131,
          "merchants_pct": 53.4694,
          "gmv_pct": 95.0786
        },
        {
          "rank": 132,
          "merchants_pct": 53.8776,
          "gmv_pct": 95.1661
        },
        {
          "rank": 133,
          "merchants_pct": 54.2857,
          "gmv_pct": 95.2501
        },
        {
          "rank": 134,
          "merchants_pct": 54.6939,
          "gmv_pct": 95.3341
        },
        {
          "rank": 135,
          "merchants_pct": 55.102,
          "gmv_pct": 95.4178
        },
        {
          "rank": 136,
          "merchants_pct": 55.5102,
          "gmv_pct": 95.501
        },
        {
          "rank": 137,
          "merchants_pct": 55.9184,
          "gmv_pct": 95.5838
        },
        {
          "rank": 138,
          "merchants_pct": 56.3265,
          "gmv_pct": 95.6658
        },
        {
          "rank": 139,
          "merchants_pct": 56.7347,
          "gmv_pct": 95.7469
        },
        {
          "rank": 140,
          "merchants_pct": 57.1429,
          "gmv_pct": 95.8271
        },
        {
          "rank": 141,
          "merchants_pct": 57.551,
          "gmv_pct": 95.907
        },
        {
          "rank": 142,
          "merchants_pct": 57.9592,
          "gmv_pct": 95.9856
        },
        {
          "rank": 143,
          "merchants_pct": 58.3673,
          "gmv_pct": 96.0631
        },
        {
          "rank": 144,
          "merchants_pct": 58.7755,
          "gmv_pct": 96.1396
        },
        {
          "rank": 145,
          "merchants_pct": 59.1837,
          "gmv_pct": 96.216
        },
        {
          "rank": 146,
          "merchants_pct": 59.5918,
          "gmv_pct": 96.2924
        },
        {
          "rank": 147,
          "merchants_pct": 60.0,
          "gmv_pct": 96.3684
        },
        {
          "rank": 148,
          "merchants_pct": 60.4082,
          "gmv_pct": 96.444
        },
        {
          "rank": 149,
          "merchants_pct": 60.8163,
          "gmv_pct": 96.5178
        },
        {
          "rank": 150,
          "merchants_pct": 61.2245,
          "gmv_pct": 96.59
        },
        {
          "rank": 151,
          "merchants_pct": 61.6327,
          "gmv_pct": 96.6622
        },
        {
          "rank": 152,
          "merchants_pct": 62.0408,
          "gmv_pct": 96.7341
        },
        {
          "rank": 153,
          "merchants_pct": 62.449,
          "gmv_pct": 96.8058
        },
        {
          "rank": 154,
          "merchants_pct": 62.8571,
          "gmv_pct": 96.8769
        },
        {
          "rank": 155,
          "merchants_pct": 63.2653,
          "gmv_pct": 96.9464
        },
        {
          "rank": 156,
          "merchants_pct": 63.6735,
          "gmv_pct": 97.0151
        },
        {
          "rank": 157,
          "merchants_pct": 64.0816,
          "gmv_pct": 97.0838
        },
        {
          "rank": 158,
          "merchants_pct": 64.4898,
          "gmv_pct": 97.1522
        },
        {
          "rank": 159,
          "merchants_pct": 64.898,
          "gmv_pct": 97.2202
        },
        {
          "rank": 160,
          "merchants_pct": 65.3061,
          "gmv_pct": 97.2876
        },
        {
          "rank": 161,
          "merchants_pct": 65.7143,
          "gmv_pct": 97.354
        },
        {
          "rank": 162,
          "merchants_pct": 66.1224,
          "gmv_pct": 97.4205
        },
        {
          "rank": 163,
          "merchants_pct": 66.5306,
          "gmv_pct": 97.4854
        },
        {
          "rank": 164,
          "merchants_pct": 66.9388,
          "gmv_pct": 97.5496
        },
        {
          "rank": 165,
          "merchants_pct": 67.3469,
          "gmv_pct": 97.6118
        },
        {
          "rank": 166,
          "merchants_pct": 67.7551,
          "gmv_pct": 97.6733
        },
        {
          "rank": 167,
          "merchants_pct": 68.1633,
          "gmv_pct": 97.7348
        },
        {
          "rank": 168,
          "merchants_pct": 68.5714,
          "gmv_pct": 97.7959
        },
        {
          "rank": 169,
          "merchants_pct": 68.9796,
          "gmv_pct": 97.8559
        },
        {
          "rank": 170,
          "merchants_pct": 69.3878,
          "gmv_pct": 97.9132
        },
        {
          "rank": 171,
          "merchants_pct": 69.7959,
          "gmv_pct": 97.9705
        },
        {
          "rank": 172,
          "merchants_pct": 70.2041,
          "gmv_pct": 98.0275
        },
        {
          "rank": 173,
          "merchants_pct": 70.6122,
          "gmv_pct": 98.0844
        },
        {
          "rank": 174,
          "merchants_pct": 71.0204,
          "gmv_pct": 98.141
        },
        {
          "rank": 175,
          "merchants_pct": 71.4286,
          "gmv_pct": 98.1944
        },
        {
          "rank": 176,
          "merchants_pct": 71.8367,
          "gmv_pct": 98.2475
        },
        {
          "rank": 177,
          "merchants_pct": 72.2449,
          "gmv_pct": 98.3002
        },
        {
          "rank": 178,
          "merchants_pct": 72.6531,
          "gmv_pct": 98.3527
        },
        {
          "rank": 179,
          "merchants_pct": 73.0612,
          "gmv_pct": 98.4043
        },
        {
          "rank": 180,
          "merchants_pct": 73.4694,
          "gmv_pct": 98.4555
        },
        {
          "rank": 181,
          "merchants_pct": 73.8776,
          "gmv_pct": 98.504
        },
        {
          "rank": 182,
          "merchants_pct": 74.2857,
          "gmv_pct": 98.5519
        },
        {
          "rank": 183,
          "merchants_pct": 74.6939,
          "gmv_pct": 98.5989
        },
        {
          "rank": 184,
          "merchants_pct": 75.102,
          "gmv_pct": 98.6448
        },
        {
          "rank": 185,
          "merchants_pct": 75.5102,
          "gmv_pct": 98.6904
        },
        {
          "rank": 186,
          "merchants_pct": 75.9184,
          "gmv_pct": 98.7324
        },
        {
          "rank": 187,
          "merchants_pct": 76.3265,
          "gmv_pct": 98.7725
        },
        {
          "rank": 188,
          "merchants_pct": 76.7347,
          "gmv_pct": 98.812
        },
        {
          "rank": 189,
          "merchants_pct": 77.1429,
          "gmv_pct": 98.8506
        },
        {
          "rank": 190,
          "merchants_pct": 77.551,
          "gmv_pct": 98.889
        },
        {
          "rank": 191,
          "merchants_pct": 77.9592,
          "gmv_pct": 98.9271
        },
        {
          "rank": 192,
          "merchants_pct": 78.3673,
          "gmv_pct": 98.9653
        },
        {
          "rank": 193,
          "merchants_pct": 78.7755,
          "gmv_pct": 99.0026
        },
        {
          "rank": 194,
          "merchants_pct": 79.1837,
          "gmv_pct": 99.0393
        },
        {
          "rank": 195,
          "merchants_pct": 79.5918,
          "gmv_pct": 99.0756
        },
        {
          "rank": 196,
          "merchants_pct": 80.0,
          "gmv_pct": 99.108
        },
        {
          "rank": 197,
          "merchants_pct": 80.4082,
          "gmv_pct": 99.1397
        },
        {
          "rank": 198,
          "merchants_pct": 80.8163,
          "gmv_pct": 99.1707
        },
        {
          "rank": 199,
          "merchants_pct": 81.2245,
          "gmv_pct": 99.2014
        },
        {
          "rank": 200,
          "merchants_pct": 81.6327,
          "gmv_pct": 99.232
        },
        {
          "rank": 201,
          "merchants_pct": 82.0408,
          "gmv_pct": 99.2623
        },
        {
          "rank": 202,
          "merchants_pct": 82.449,
          "gmv_pct": 99.289
        },
        {
          "rank": 203,
          "merchants_pct": 82.8571,
          "gmv_pct": 99.3158
        },
        {
          "rank": 204,
          "merchants_pct": 83.2653,
          "gmv_pct": 99.3421
        },
        {
          "rank": 205,
          "merchants_pct": 83.6735,
          "gmv_pct": 99.3681
        },
        {
          "rank": 206,
          "merchants_pct": 84.0816,
          "gmv_pct": 99.3933
        },
        {
          "rank": 207,
          "merchants_pct": 84.4898,
          "gmv_pct": 99.4181
        },
        {
          "rank": 208,
          "merchants_pct": 84.898,
          "gmv_pct": 99.443
        },
        {
          "rank": 209,
          "merchants_pct": 85.3061,
          "gmv_pct": 99.4659
        },
        {
          "rank": 210,
          "merchants_pct": 85.7143,
          "gmv_pct": 99.4888
        },
        {
          "rank": 211,
          "merchants_pct": 86.1224,
          "gmv_pct": 99.5117
        },
        {
          "rank": 212,
          "merchants_pct": 86.5306,
          "gmv_pct": 99.5346
        },
        {
          "rank": 213,
          "merchants_pct": 86.9388,
          "gmv_pct": 99.5572
        },
        {
          "rank": 214,
          "merchants_pct": 87.3469,
          "gmv_pct": 99.5797
        },
        {
          "rank": 215,
          "merchants_pct": 87.7551,
          "gmv_pct": 99.6007
        },
        {
          "rank": 216,
          "merchants_pct": 88.1633,
          "gmv_pct": 99.6199
        },
        {
          "rank": 217,
          "merchants_pct": 88.5714,
          "gmv_pct": 99.639
        },
        {
          "rank": 218,
          "merchants_pct": 88.9796,
          "gmv_pct": 99.6577
        },
        {
          "rank": 219,
          "merchants_pct": 89.3878,
          "gmv_pct": 99.6764
        },
        {
          "rank": 220,
          "merchants_pct": 89.7959,
          "gmv_pct": 99.6948
        },
        {
          "rank": 221,
          "merchants_pct": 90.2041,
          "gmv_pct": 99.7129
        },
        {
          "rank": 222,
          "merchants_pct": 90.6122,
          "gmv_pct": 99.7304
        },
        {
          "rank": 223,
          "merchants_pct": 91.0204,
          "gmv_pct": 99.7476
        },
        {
          "rank": 224,
          "merchants_pct": 91.4286,
          "gmv_pct": 99.7644
        },
        {
          "rank": 225,
          "merchants_pct": 91.8367,
          "gmv_pct": 99.7808
        },
        {
          "rank": 226,
          "merchants_pct": 92.2449,
          "gmv_pct": 99.7961
        },
        {
          "rank": 227,
          "merchants_pct": 92.6531,
          "gmv_pct": 99.8114
        },
        {
          "rank": 228,
          "merchants_pct": 93.0612,
          "gmv_pct": 99.8255
        },
        {
          "rank": 229,
          "merchants_pct": 93.4694,
          "gmv_pct": 99.8389
        },
        {
          "rank": 230,
          "merchants_pct": 93.8776,
          "gmv_pct": 99.8522
        },
        {
          "rank": 231,
          "merchants_pct": 94.2857,
          "gmv_pct": 99.8654
        },
        {
          "rank": 232,
          "merchants_pct": 94.6939,
          "gmv_pct": 99.8775
        },
        {
          "rank": 233,
          "merchants_pct": 95.102,
          "gmv_pct": 99.8893
        },
        {
          "rank": 234,
          "merchants_pct": 95.5102,
          "gmv_pct": 99.9007
        },
        {
          "rank": 235,
          "merchants_pct": 95.9184,
          "gmv_pct": 99.9121
        },
        {
          "rank": 236,
          "merchants_pct": 96.3265,
          "gmv_pct": 99.9235
        },
        {
          "rank": 237,
          "merchants_pct": 96.7347,
          "gmv_pct": 99.9344
        },
        {
          "rank": 238,
          "merchants_pct": 97.1429,
          "gmv_pct": 99.9451
        },
        {
          "rank": 239,
          "merchants_pct": 97.551,
          "gmv_pct": 99.9558
        },
        {
          "rank": 240,
          "merchants_pct": 97.9592,
          "gmv_pct": 99.9659
        },
        {
          "rank": 241,
          "merchants_pct": 98.3673,
          "gmv_pct": 99.9759
        },
        {
          "rank": 242,
          "merchants_pct": 98.7755,
          "gmv_pct": 99.9836
        },
        {
          "rank": 243,
          "merchants_pct": 99.1837,
          "gmv_pct": 99.9908
        },
        {
          "rank": 244,
          "merchants_pct": 99.5918,
          "gmv_pct": 99.9962
        },
        {
          "rank": 245,
          "merchants_pct": 100.0,
          "gmv_pct": 100.0
        }
      ]
    },
    "segments": [
      {
        "segment": "high_contribution",
        "count": 62,
        "gmv_90d": 213783.87,
        "threshold": 918.9
      },
      {
        "segment": "other_activated",
        "count": 183,
        "gmv_90d": 47881.17,
        "threshold": null
      },
      {
        "segment": "observable_no_activation",
        "count": 134,
        "gmv_90d": 0.0,
        "threshold": null
      },
      {
        "segment": "unknown_coverage",
        "count": 462,
        "gmv_90d": null,
        "threshold": null
      },
      {
        "segment": "incomplete_window",
        "count": 0,
        "gmv_90d": null,
        "threshold": null
      },
      {
        "segment": "chronology_error",
        "count": 1,
        "gmv_90d": null,
        "threshold": null
      }
    ],
    "sensitivity": [
      {
        "quantile": 0.7,
        "threshold": 701.12,
        "high_count": 74,
        "high_gmv_pct": 85.3851
      },
      {
        "quantile": 0.75,
        "threshold": 918.9,
        "high_count": 62,
        "high_gmv_pct": 81.7013
      },
      {
        "quantile": 0.8,
        "threshold": 1121.476,
        "high_count": 49,
        "high_gmv_pct": 76.6898
      }
    ],
    "experiment_status": "design_only_not_executed",
    "source_fingerprints": [
      {
        "file": "olist_marketing_qualified_leads_dataset.csv",
        "rows": 8000,
        "sha256": "5537753b7549ce4068e52e2402c29f2773c5375fc0575520ae8f3f301f666573"
      },
      {
        "file": "olist_closed_deals_dataset.csv",
        "rows": 842,
        "sha256": "1433f402d8fff00ca167579de641d9525f6e846368958c166f699ef1b0c31f3d"
      },
      {
        "file": "olist_sellers_dataset.csv",
        "rows": 3095,
        "sha256": "1f643d2b950373b85735e7794b20986f528d7a000432e7c6f9bcbb44d0846a0e"
      },
      {
        "file": "olist_orders_dataset.csv",
        "rows": 99441,
        "sha256": "8df58ef3d2d7e9944010f7beecd9b75367f5588ec6e3c91cec19ae3345ef9ecf"
      },
      {
        "file": "olist_order_items_dataset.csv",
        "rows": 112650,
        "sha256": "0bc4d068c4fe38cbb01bd90e8746e3c613fe7b4baef75fab7b0e329701c3e279"
      }
    ]
  }
};
