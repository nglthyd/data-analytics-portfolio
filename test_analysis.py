from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from analysis import build_lead_value_table, build_metrics, summarize_value_by_channel


def synthetic_frames() -> tuple[pd.DataFrame, ...]:
    mql = pd.DataFrame(
        [
            ("paid_win", "2018-01-01", "paid_search"),
            ("paid_no_win", "2018-01-01", "paid_search"),
            ("organic_win", "2018-01-01", "organic_search"),
            ("social_unobserved", "2018-01-01", "social"),
            ("incomplete", "2018-03-15", "referral"),
        ],
        columns=["mql_id", "first_contact_date", "origin"],
    )
    mql["landing_page_id"] = "landing"
    deals = pd.DataFrame(
        [
            ("paid_win", "seller_1", "2018-01-05"),
            ("organic_win", "seller_2", "2018-01-10"),
            ("social_unobserved", "seller_3", "2018-01-03"),
            ("incomplete", "seller_4", "2018-03-20"),
        ],
        columns=["mql_id", "seller_id", "won_date"],
    )
    sellers = pd.DataFrame(
        {
            "seller_id": ["seller_1", "seller_2", "seller_4", "other_seller"],
            "seller_zip_code_prefix": [1, 2, 4, 9],
            "seller_city": ["a", "b", "d", "z"],
            "seller_state": ["SP", "RJ", "BA", "MG"],
        }
    )
    orders = pd.DataFrame(
        [
            ("order_day5", "delivered", "2018-01-06"),
            ("order_day89", "delivered", "2018-03-31"),
            ("order_day90", "delivered", "2018-04-01"),
            ("order_cancelled", "canceled", "2018-01-20"),
            ("order_multi_seller", "delivered", "2018-01-20"),
            ("order_pre_win", "delivered", "2018-01-05"),
            ("order_organic", "delivered", "2018-01-15"),
            ("order_incomplete", "delivered", "2018-03-25"),
            ("order_observation_end", "delivered", "2018-04-01"),
        ],
        columns=["order_id", "order_status", "order_purchase_timestamp"],
    )
    orders["customer_id"] = [f"customer_{i}" for i in range(len(orders))]
    for column in (
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ):
        orders[column] = orders["order_purchase_timestamp"]
    items = pd.DataFrame(
        [
            ("order_day5", 1, "seller_1", 100.0),
            ("order_day89", 1, "seller_1", 50.0),
            ("order_day89", 2, "seller_1", 20.0),
            ("order_day90", 1, "seller_1", 999.0),
            ("order_cancelled", 1, "seller_1", 999.0),
            ("order_multi_seller", 1, "seller_1", 30.0),
            ("order_multi_seller", 2, "seller_2", 40.0),
            ("order_pre_win", 1, "seller_2", 500.0),
            ("order_organic", 1, "seller_2", 200.0),
            ("order_incomplete", 1, "seller_4", 300.0),
            ("order_observation_end", 1, "other_seller", 1.0),
        ],
        columns=["order_id", "order_item_id", "seller_id", "price"],
    )
    items["product_id"] = [f"product_{i}" for i in range(len(items))]
    items["shipping_limit_date"] = "2018-04-10"
    items["freight_value"] = 0.0
    return mql, deals, sellers, orders, items


class LeadValueTests(unittest.TestCase):
    def test_preserves_zeroes_and_applies_time_order_status_and_item_grain(self) -> None:
        frames = synthetic_frames()
        result = build_lead_value_table(*frames, observation_end=pd.Timestamp("2018-04-01"))
        lead = result.set_index("mql_id")

        self.assertEqual(lead.loc["paid_no_win", "gmv_90d"], 0.0)
        self.assertEqual(lead.loc["social_unobserved", "gmv_90d"], 0.0)
        self.assertEqual(lead.loc["paid_win", "gmv_90d"], 200.0)
        self.assertEqual(lead.loc["paid_win", "orders_90d"], 3)
        self.assertEqual(lead.loc["organic_win", "gmv_90d"], 240.0)
        self.assertEqual(lead.loc["organic_win", "orders_90d"], 2)
        self.assertTrue(pd.isna(lead.loc["incomplete", "gmv_90d"]))
        self.assertFalse(bool(lead.loc["incomplete", "complete_90d"]))

    def test_channel_summary_uses_all_complete_mqls_as_denominator(self) -> None:
        frames = synthetic_frames()
        lead = build_lead_value_table(*frames, observation_end=pd.Timestamp("2018-04-01"))
        summary = summarize_value_by_channel(lead).set_index("origin")

        self.assertEqual(summary.loc["paid_search", "mqls"], 2)
        self.assertEqual(summary.loc["paid_search", "wins"], 1)
        self.assertEqual(summary.loc["paid_search", "observed_sellers"], 1)
        self.assertEqual(summary.loc["paid_search", "activated_sellers_90d"], 1)
        self.assertEqual(summary.loc["paid_search", "gmv_per_mql_90d"], 100.0)
        self.assertEqual(summary.loc["organic_search", "gmv_per_mql_90d"], 240.0)
        self.assertNotIn("referral", summary.index)

    def test_build_metrics_adds_downstream_value_when_ecommerce_data_is_supplied(self) -> None:
        mql, deals, sellers, orders, items = synthetic_frames()
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            marketing_dir = root_path / "marketing"
            ecommerce_dir = root_path / "ecommerce"
            marketing_dir.mkdir()
            ecommerce_dir.mkdir()
            mql.to_csv(marketing_dir / "olist_marketing_qualified_leads_dataset.csv", index=False)
            deals.to_csv(marketing_dir / "olist_closed_deals_dataset.csv", index=False)
            sellers.to_csv(ecommerce_dir / "olist_sellers_dataset.csv", index=False)
            orders.to_csv(ecommerce_dir / "olist_orders_dataset.csv", index=False)
            items.to_csv(ecommerce_dir / "olist_order_items_dataset.csv", index=False)

            metrics = build_metrics(marketing_dir, ecommerce_dir=ecommerce_dir)

        self.assertEqual(metrics["downstream"]["complete_mqls"], 4)
        self.assertEqual(metrics["downstream"]["activated_sellers_90d"], 2)
        self.assertEqual(metrics["downstream"]["orders_90d"], 5)
        self.assertEqual(metrics["downstream"]["gmv_90d"], 440.0)
        paid = next(row for row in metrics["downstream"]["channel"] if row["origin"] == "paid_search")
        self.assertEqual(paid["mqls"], 2)
        self.assertEqual(paid["gmv_per_mql_90d"], 100.0)

    def test_rejects_duplicate_mql_id(self) -> None:
        mql, deals, sellers, orders, items = synthetic_frames()
        duplicate = pd.concat([mql, mql.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(ValueError, "mql_id must be unique"):
            build_lead_value_table(duplicate, deals, sellers, orders, items)

    def test_rejects_duplicate_order_item_key(self) -> None:
        mql, deals, sellers, orders, items = synthetic_frames()
        duplicate = pd.concat([items, items.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(ValueError, "order_id.*order_item_id"):
            build_lead_value_table(mql, deals, sellers, orders, duplicate)

    def test_rejects_closed_deal_without_mql(self) -> None:
        mql, deals, sellers, orders, items = synthetic_frames()
        bad = pd.concat(
            [deals, pd.DataFrame([{"mql_id": "absent", "seller_id": "x", "won_date": "2018-01-02"}])],
            ignore_index=True,
        )
        with self.assertRaisesRegex(ValueError, "closed deal.*MQL"):
            build_lead_value_table(mql, bad, sellers, orders, items)

    def test_rejects_invalid_dates(self) -> None:
        mql, deals, sellers, orders, items = synthetic_frames()
        mql.loc[0, "first_contact_date"] = "not-a-date"
        with self.assertRaisesRegex(ValueError, "first_contact_date"):
            build_lead_value_table(mql, deals, sellers, orders, items)


if __name__ == "__main__":
    unittest.main()
