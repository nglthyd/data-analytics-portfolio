"""Behavioral tests; fixtures never write source CSV files."""
from __future__ import annotations

import importlib.util
import json
import unittest

import pandas as pd

from analysis import build_lead_value_table
from test_analysis import synthetic_frames

# Before implementation, exercise the real baseline so RED is a behavioral
# assertion (unknown coverage is zero), rather than an import/collection error.
if importlib.util.find_spec("merchant_analysis"):
    from merchant_analysis import build_merchant_table, summarize_merchants
else:
    build_merchant_table = build_lead_value_table
    summarize_merchants = None

END = pd.Timestamp("2018-04-01")


class MerchantTests(unittest.TestCase):
    def build(self, frames=None, end=END):
        return build_merchant_table(*(frames or synthetic_frames()), observation_end=end)

    def summarize(self, table):
        self.assertTrue(callable(summarize_merchants), "merchant summary API is missing")
        return summarize_merchants(table)

    def verify(self, frames=None, end=END):
        self.assertIsNotNone(importlib.util.find_spec("verify_merchant"), "independent verifier is missing")
        from verify_merchant import verify_frames
        return verify_frames(*(frames or synthetic_frames()), observation_end=end)

    def test_unknown_coverage_is_null_instead_of_baseline_zero(self):
        table = self.build().set_index("mql_id")
        self.assertTrue(pd.isna(table.loc["social_unobserved", "gmv_90d"]),
                        "unknown coverage must not be reported as real zero")
        self.assertTrue(pd.isna(table.loc["social_unobserved", "orders_90d"]))
        self.assertEqual(table.loc["social_unobserved", "status"], "unknown_coverage")
        self.assertEqual(len(table), 4)

    def test_boundary_multi_item_multi_seller_and_incomplete(self):
        table = self.build().set_index("seller_id")
        self.assertEqual(table.loc["seller_1", "orders_90d"], 3)
        self.assertEqual(table.loc["seller_1", "gmv_90d"], 200.0)
        self.assertEqual(table.loc["seller_2", "orders_90d"], 2)
        self.assertEqual(table.loc["seller_2", "gmv_90d"], 240.0)
        self.assertTrue(pd.isna(table.loc["seller_4", "gmv_90d"]))
        self.assertEqual(table.loc["seller_4", "status"], "incomplete_window")
        self.assertEqual(table.loc["seller_1", "landing_page_id"], "landing")

    def test_observable_no_order_preserves_zero(self):
        frames = list(synthetic_frames())
        frames[4] = frames[4].loc[~frames[4].seller_id.eq("seller_2")].copy()
        table = self.build(frames).set_index("seller_id")
        self.assertEqual(table.loc["seller_2", "orders_90d"], 0)
        self.assertEqual(table.loc["seller_2", "gmv_90d"], 0.0)
        self.assertEqual(table.loc["seller_2", "status"], "observable_no_activation")

    def test_status_precedence_retains_overlapping_flags(self):
        frames = list(synthetic_frames())
        frames[1].loc[2, "won_date"] = "2017-12-31"
        frames[1].loc[3, "won_date"] = "2018-03-01"
        table = self.build(frames).set_index("seller_id")
        self.assertEqual(table.loc["seller_3", "status"], "chronology_error")
        self.assertEqual(table.loc["seller_4", "status"], "chronology_error")
        self.assertFalse(table.loc["seller_3", "observed_seller"])
        self.assertFalse(table.loc["seller_4", "complete_90d"])
        result = self.summarize(table.reset_index())["summary"]
        self.assertEqual(result["chronology_error_closed"], 2)
        self.assertEqual(result["unknown_coverage_closed"], 1)
        self.assertEqual(result["incomplete_closed"], 1)
        self.assertEqual(result["eligible_closed"], 2)

    def test_chronology_excludes_precontact_deal_value(self):
        frames = list(synthetic_frames())
        frames[1].loc[0, "won_date"] = "2017-12-31"
        table = self.build(frames).set_index("seller_id")
        self.assertTrue(pd.isna(table.loc["seller_1", "gmv_90d"]))
        result = self.summarize(table.reset_index())
        self.assertEqual(result["summary"]["gmv_90d"], 240.0)
        self.assertEqual(result["summary"]["orders_90d"], 2)

    def test_rejects_all_duplicate_primary_keys(self):
        for index in range(5):
            with self.subTest(frame=index):
                frames = list(synthetic_frames())
                frames[index] = pd.concat([frames[index], frames[index].iloc[[0]]], ignore_index=True)
                with self.assertRaises(ValueError):
                    self.build(frames)
        frames = list(synthetic_frames())
        frames[1].loc[1, "seller_id"] = "seller_1"
        with self.assertRaisesRegex(ValueError, "seller_id"):
            self.build(frames)

    def test_rejects_null_keys_and_unmatched_foreign_keys(self):
        for index, column in ((0, "mql_id"), (1, "seller_id"), (2, "seller_id"),
                              (3, "order_id"), (4, "order_item_id")):
            with self.subTest(index=index, column=column):
                frames = list(synthetic_frames())
                frames[index].loc[0, column] = None
                with self.assertRaises(ValueError):
                    self.build(frames)
        for index, column in ((1, "mql_id"), (4, "order_id"), (4, "seller_id")):
            with self.subTest(index=index, foreign=column):
                frames = list(synthetic_frames())
                frames[index].loc[0, column] = "absent"
                with self.assertRaises(ValueError):
                    self.build(frames)

    def test_rejects_invalid_and_null_dates(self):
        for index, column in ((0, "first_contact_date"), (1, "won_date"),
                              (3, "order_purchase_timestamp")):
            for bad in (None, "not-a-date", "2018-02-30", ""):
                with self.subTest(index=index, bad=bad):
                    frames = list(synthetic_frames())
                    frames[index].loc[0, column] = bad
                    with self.assertRaisesRegex(ValueError, column):
                        self.build(frames)
        with self.assertRaisesRegex(ValueError, "observation_end"):
            self.build(end=pd.NaT)

    def test_prices_cast_numeric_and_reject_bad_even_on_excluded_orders(self):
        frames = list(synthetic_frames())
        frames[4]["price"] = frames[4].price.astype(str)
        self.assertEqual(self.build(frames).set_index("seller_id").loc["seller_1", "gmv_90d"], 200.0)
        for bad in (None, "bad", float("inf"), float("nan"), -0.01):
            with self.subTest(bad=bad):
                frames = list(synthetic_frames())
                frames[4]["price"] = frames[4].price.astype(object)
                frames[4].loc[4, "price"] = bad  # canceled order must still be validated
                with self.assertRaisesRegex(ValueError, "price"):
                    self.build(frames)

    def test_timestamp_window_uses_exact_time_not_date_truncation(self):
        frames = list(synthetic_frames())
        frames[0].loc[0, "first_contact_date"] = "2018-01-01 12:30:00"
        frames[3].loc[2, "order_purchase_timestamp"] = "2018-04-01 12:29:59"
        table = self.build(frames, pd.Timestamp("2018-04-01 12:30:00")).set_index("seller_id")
        self.assertEqual(table.loc["seller_1", "gmv_90d"], 1199.0)
        self.verify(frames, pd.Timestamp("2018-04-01 12:30:00"))

    def test_empty_shapes_and_empty_orders_require_observation_end(self):
        frames = list(synthetic_frames())
        for index in (0, 1, 3, 4):
            frames[index] = frames[index].iloc[:0].copy()
        table = self.build(frames)
        self.assertEqual(len(table), 0)
        result = self.summarize(table)
        self.assertIsNone(result["summary"]["activation_pct_of_eligible"])
        self.assertIsNone(result["summary"]["gmv_per_seller_order"])
        self.assertEqual(result["concentration"]["curve"], [])
        json.dumps(result, allow_nan=False)
        self.verify(frames)
        frames = list(synthetic_frames())
        frames[3], frames[4] = frames[3].iloc[:0].copy(), frames[4].iloc[:0].copy()
        with self.assertRaisesRegex(ValueError, "observation_end"):
            self.build(frames, None)
        self.assertFalse(self.build(frames, pd.Timestamp("2018-01-01")).complete_90d.any())

    def test_summary_schema_cohorts_and_privacy(self):
        result = self.summarize(self.build())
        self.assertEqual(set(result), {"summary", "states", "cohorts", "concentration", "segments", "sensitivity"})
        s = result["summary"]
        for key, value in {"total_closed": 4, "observable_closed": 3, "unknown_coverage_closed": 1,
                           "incomplete_closed": 1, "chronology_error_closed": 0, "eligible_closed": 2,
                           "activated": 2, "observable_no_activation": 0, "orders_90d": 5,
                           "gmv_90d": 440.0, "activation_pct_of_eligible": 100.0,
                           "gmv_per_seller_order": 88.0}.items():
            self.assertEqual(s[key], value, key)
        self.assertEqual(sum(row["count"] for row in result["states"]), 4)
        self.assertEqual(sum(row["total_closed"] for row in result["cohorts"]), 4)
        self.assertEqual(sum(row["count"] for row in result["segments"]), 4)
        self.assertEqual(sum(row["gmv_90d"] for row in result["segments"] if row["gmv_90d"] is not None), 440.0)
        encoded = json.dumps(result, allow_nan=False)
        for raw_id in ("seller_1", "paid_win", "mql_id", "seller_id"):
            self.assertNotIn(raw_id, encoded)

    def test_concentration_ceil_and_quantile_ties(self):
        frames = list(synthetic_frames())
        base = self.build(frames).loc[lambda x: x.seller_id.eq("seller_1")]
        self.assertIn("eligible", base.columns, "eligibility field missing")
        table = pd.concat([base.assign(seller_id=f"tie_{i}", mql_id=f"lead_{i}",
                                      gmv_90d=100.0 if i < 4 else 0.0,
                                      orders_90d=1 if i < 4 else 0,
                                      status="activated" if i < 4 else "observable_no_activation")
                           for i in range(11)], ignore_index=True)
        result = self.summarize(table)
        c = result["concentration"]
        # Approved denominator: positive-GMV eligible sellers, not all sellers.
        self.assertEqual(c["n"], 4)
        self.assertEqual(c["top10_count"], 1)
        self.assertEqual(c["top20_count"], 1)
        self.assertEqual(c["top10_gmv_pct"], 25.0)
        self.assertEqual(c["top20_gmv_pct"], 25.0)
        self.assertEqual(c["curve"][-1]["gmv_pct"], 100.0)
        high = next(row for row in result["segments"] if row["segment"] == "high_contribution")
        self.assertEqual(high["count"], 4)  # >= threshold allows ties beyond top quartile
        for row in result["sensitivity"]:
            self.assertEqual(row["threshold"], 100.0)
            self.assertEqual(row["high_count"], 4)
            self.assertEqual(row["high_gmv_pct"], 100.0)
        shuffled = self.summarize(table.sample(frac=1, random_state=2))
        self.assertEqual(result, shuffled)

    def test_zero_gmv_delivered_orders_are_activated_and_ratios_safe(self):
        frames = list(synthetic_frames())
        frames[4]["price"] = 0.0
        result = self.summarize(self.build(frames))
        self.assertEqual(result["summary"]["activated"], 2)
        self.assertEqual(result["summary"]["gmv_per_seller_order"], 0.0)
        self.assertIsNone(result["concentration"]["top10_gmv_pct"])
        self.assertTrue(all(row["threshold"] is None for row in result["sensitivity"]))
        json.dumps(result, allow_nan=False)
        self.verify(frames)

    def test_independent_sql_verifies_synthetic_rows_and_summary(self):
        result = self.verify()
        self.assertEqual(result["verified_sellers"], 4)
        self.assertEqual(result["summary"]["summary"]["gmv_90d"], 440.0)
        frames = list(synthetic_frames())
        frames[1].loc[0, "won_date"] = "2017-12-31"
        result = self.verify(frames)
        self.assertEqual(result["summary"]["summary"]["gmv_90d"], 240.0)


if __name__ == "__main__":
    unittest.main()
