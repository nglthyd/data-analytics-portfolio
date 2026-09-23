"""Independent SQLite cross-checks for the published funnel numbers."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

from analysis import DEALS_FILE, MQL_FILE, build_metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    args = parser.parse_args()
    metrics = build_metrics(args.data_dir)

    connection = sqlite3.connect(":memory:")
    for file_name in (MQL_FILE, DEALS_FILE):
        pd.read_csv(args.data_dir / file_name).to_sql(
            file_name.removesuffix(".csv"), connection, index=False, if_exists="replace"
        )

    sql = (Path(__file__).parent / "queries.sql").read_text(encoding="utf-8")
    statements = [block.strip() for block in sql.split(";") if "SELECT" in block]
    assert len(statements) == 3
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

    # Adversarial checks: missing channels, source uniqueness, and invalid chronology.
    assert metrics["audit"]["missing_origin"] == 60
    assert metrics["audit"]["duplicate_mql_ids"] == 0
    assert metrics["audit"]["duplicate_deal_ids"] == 0
    assert metrics["audit"]["unmatched_deals"] == 0
    assert metrics["audit"]["negative_close_days"] == 1
    print("PASS: 3 SQL queries match Python; missing/duplicate/unmatched/negative-date checks pass")


if __name__ == "__main__":
    main()
