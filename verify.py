"""Independent SQLite cross-checks for the published funnel numbers."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

from analysis import DEALS_FILE, ITEMS_FILE, MQL_FILE, ORDERS_FILE, SELLERS_FILE, build_metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--ecommerce-dir", type=Path, required=True)
    args = parser.parse_args()
    metrics = build_metrics(args.data_dir, ecommerce_dir=args.ecommerce_dir)

    connection = sqlite3.connect(":memory:")
    for file_name in (MQL_FILE, DEALS_FILE):
        pd.read_csv(args.data_dir / file_name).to_sql(
            file_name.removesuffix(".csv"), connection, index=False, if_exists="replace"
        )
    for file_name in (SELLERS_FILE, ORDERS_FILE, ITEMS_FILE):
        pd.read_csv(args.ecommerce_dir / file_name).to_sql(
            file_name.removesuffix(".csv"), connection, index=False, if_exists="replace"
        )

    sql = (Path(__file__).parent / "queries.sql").read_text(encoding="utf-8")
    statements = [block.strip() for block in sql.split(";") if "SELECT" in block]
    assert len(statements) == 6, f"Expected 6 SQL verification blocks, found {len(statements)}"
    overall = pd.read_sql_query(statements[0], connection).iloc[0]
    assert int(overall.leads) == metrics["overall"]["leads"]
    assert int(overall.wins) == metrics["overall"]["wins"]
    assert float(overall.conversion_pct) == metrics["overall"]["conversion_pct"]

    channel_sql = pd.read_sql_query(statements[1], connection)
    channel_python = pd.DataFrame(metrics["focus"]["channel"])
    merged = channel_sql.merge(channel_python, on="origin", validate="one_to_one", suffixes=("_sql", "_py"))
    assert len(merged) == len(channel_python) == len(channel_sql)
    for field in ("leads", "wins", "conversion_pct"):
        assert (merged[f"{field}_sql"] == merged[f"{field}_py"]).all(), field
    assert int(channel_sql.leads.sum()) == metrics["focus"]["leads"]
    assert int(channel_sql.wins.sum()) == metrics["focus"]["wins"]

    monthly_sql = pd.read_sql_query(statements[2], connection)
    monthly_python = pd.DataFrame(metrics["monthly"])
    assert monthly_sql.contact_month.tolist() == monthly_python.month.tolist()
    for field in ("leads", "wins", "conversion_pct"):
        assert monthly_sql[field].tolist() == monthly_python[field].tolist(), field

    mapping = pd.read_sql_query(statements[3], connection).iloc[0]
    for field in ("deal_sellers", "observable_deal_sellers", "unobserved_deal_sellers"):
        assert int(mapping[field]) == metrics["audit"][field], field

    downstream = pd.read_sql_query(statements[4], connection).iloc[0]
    for field in (
        "complete_mqls",
        "wins",
        "observed_sellers",
        "activated_sellers_90d",
        "orders_90d",
    ):
        assert int(downstream[field]) == metrics["downstream"][field], field
    assert float(downstream.gmv_90d) == metrics["downstream"]["gmv_90d"]

    channel_value_sql = pd.read_sql_query(statements[5], connection)
    channel_value_python = pd.DataFrame(metrics["downstream"]["channel"])
    channel_value = channel_value_sql.merge(
        channel_value_python,
        on="origin",
        validate="one_to_one",
        suffixes=("_sql", "_py"),
    )
    assert len(channel_value) == len(channel_value_sql) == len(channel_value_python)
    for field in (
        "mqls",
        "wins",
        "observed_sellers",
        "activated_sellers_90d",
        "orders_90d",
        "gmv_90d",
        "conversion_pct",
        "observed_pct_of_wins",
        "activation_pct_of_mql",
        "orders_per_mql_90d",
        "gmv_per_mql_90d",
    ):
        assert channel_value[f"{field}_sql"].tolist() == channel_value[
            f"{field}_py"
        ].tolist(), field
    assert int(channel_value_sql.mqls.sum()) == metrics["downstream"]["focus"][
        "complete_mqls"
    ]
    assert round(float(channel_value_sql.gmv_90d.sum()), 2) == metrics["downstream"][
        "focus"
    ]["gmv_90d"]

    # Adversarial checks: missing channels, source uniqueness, and invalid chronology.
    assert metrics["audit"]["missing_origin"] == 60
    assert metrics["audit"]["duplicate_mql_ids"] == 0
    assert metrics["audit"]["duplicate_deal_ids"] == 0
    assert metrics["audit"]["unmatched_deals"] == 0
    assert metrics["audit"]["negative_close_days"] == 1
    print("PASS: 3 funnel SQL queries match Python; source-quality checks pass")
    print("PASS: 3 full-funnel SQL queries match Python; 90-day value totals and channels close")


if __name__ == "__main__":
    main()
