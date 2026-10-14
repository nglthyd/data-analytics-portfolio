"""Independent SQLite verification for the merchant-operations analysis."""
from __future__ import annotations

import argparse
import math
import sqlite3
from pathlib import Path

import pandas as pd

from analysis import DEALS_FILE, ITEMS_FILE, MQL_FILE, ORDERS_FILE, SELLERS_FILE
from merchant_analysis import STATES, build_merchant_table, summarize_merchants


def _ratio(numerator, denominator):
    return round(float(numerator) / denominator * 100, 4) if denominator else None


def _quantile(values, q):
    if not values:
        return None
    ordered = sorted(float(value) for value in values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _sql_summary(connection):
    row = connection.execute(
        """
        SELECT
            COUNT(*) AS total_closed,
            COALESCE(SUM(observed_seller), 0) AS observable_closed,
            COALESCE(SUM(CASE WHEN observed_seller = 0 THEN 1 ELSE 0 END), 0) AS unknown_coverage_closed,
            COALESCE(SUM(CASE WHEN complete_90d = 0 THEN 1 ELSE 0 END), 0) AS incomplete_closed,
            COALESCE(SUM(chronology_error), 0) AS chronology_error_closed,
            COALESCE(SUM(eligible), 0) AS eligible_closed,
            COALESCE(SUM(CASE WHEN eligible = 1 AND orders_90d > 0 THEN 1 ELSE 0 END), 0) AS activated,
            COALESCE(SUM(CASE WHEN eligible = 1 AND orders_90d = 0 THEN 1 ELSE 0 END), 0) AS observable_no_activation,
            COALESCE(SUM(CASE WHEN eligible = 1 THEN orders_90d ELSE 0 END), 0) AS orders_90d,
            COALESCE(SUM(CASE WHEN eligible = 1 THEN gmv_90d ELSE 0 END), 0.0) AS gmv_90d
        FROM merchant_sql
        """
    ).fetchone()
    total_orders = int(row[8])
    total_gmv = float(row[9])
    summary = {
        "total_closed": int(row[0]),
        "observable_closed": int(row[1]),
        "unknown_coverage_closed": int(row[2]),
        "incomplete_closed": int(row[3]),
        "chronology_error_closed": int(row[4]),
        "eligible_closed": int(row[5]),
        "activated": int(row[6]),
        "observable_no_activation": int(row[7]),
        "activation_pct_of_eligible": _ratio(int(row[6]), int(row[5])),
        "orders_90d": total_orders,
        "gmv_90d": round(total_gmv, 2),
        "gmv_per_seller_order": round(total_gmv / total_orders, 4) if total_orders else None,
    }

    state_counts = dict(connection.execute(
        "SELECT status, COUNT(*) FROM merchant_sql GROUP BY status"
    ).fetchall())
    states = [{"status": state, "count": int(state_counts.get(state, 0))} for state in STATES]

    cohorts = []
    for cohort in connection.execute(
        """
        SELECT
            substr(contact_date, 1, 7) AS contact_month,
            COUNT(*) AS total_closed,
            COALESCE(SUM(observed_seller), 0) AS observable_closed,
            COALESCE(SUM(eligible), 0) AS eligible_closed,
            COALESCE(SUM(CASE WHEN eligible = 1 AND orders_90d > 0 THEN 1 ELSE 0 END), 0) AS activated,
            COALESCE(SUM(CASE WHEN eligible = 1 THEN gmv_90d ELSE 0 END), 0.0) AS gmv_90d
        FROM merchant_sql
        GROUP BY substr(contact_date, 1, 7)
        ORDER BY contact_month
        """
    ):
        cohorts.append({
            "contact_month": str(cohort[0]),
            "total_closed": int(cohort[1]),
            "observable_closed": int(cohort[2]),
            "eligible_closed": int(cohort[3]),
            "activated": int(cohort[4]),
            "activation_pct_of_eligible": _ratio(int(cohort[4]), int(cohort[3])),
            "gmv_90d": round(float(cohort[5]), 2),
            "low_sample": int(cohort[3]) < 30,
        })

    positive_rows = connection.execute(
        """
        SELECT seller_id, gmv_90d
        FROM merchant_sql
        WHERE eligible = 1 AND gmv_90d > 0
        ORDER BY gmv_90d DESC, seller_id ASC
        """
    ).fetchall()
    positive_values = [float(row[1]) for row in positive_rows]
    positive_total = sum(positive_values)
    n = len(positive_rows)
    top10_count = math.ceil(n * 0.1)
    top20_count = math.ceil(n * 0.2)
    concentration = {
        "n": n,
        "top10_count": top10_count,
        "top20_count": top20_count,
        "top10_gmv_pct": _ratio(sum(positive_values[:top10_count]), positive_total),
        "top20_gmv_pct": _ratio(sum(positive_values[:top20_count]), positive_total),
        "curve": [],
    }
    cumulative = 0.0
    for rank, value in enumerate(positive_values, 1):
        cumulative += value
        concentration["curve"].append({
            "rank": rank,
            "merchants_pct": _ratio(rank, n),
            "gmv_pct": _ratio(cumulative, positive_total),
        })

    threshold = _quantile(positive_values, 0.75)
    segment_names = (
        "high_contribution", "other_activated", "observable_no_activation",
        "unknown_coverage", "incomplete_window", "chronology_error",
    )
    segments = []
    for name in segment_names:
        if name == "high_contribution":
            where, params = "eligible = 1 AND gmv_90d >= ?", (threshold,)
        elif name == "other_activated":
            if threshold is None:
                where, params = "status = 'activated'", ()
            else:
                where, params = "status = 'activated' AND gmv_90d < ?", (threshold,)
        else:
            where, params = "status = ?", (name,)
        count, value = connection.execute(
            f"SELECT COUNT(*), SUM(gmv_90d) FROM merchant_sql WHERE {where}", params
        ).fetchone()
        known_value = name in {"high_contribution", "other_activated", "observable_no_activation"}
        segments.append({
            "segment": name,
            "count": int(count),
            "gmv_90d": round(float(value or 0.0), 2) if known_value else None,
            "threshold": round(threshold, 4) if name == "high_contribution" and threshold is not None else None,
        })

    sensitivity = []
    for q in (0.70, 0.75, 0.80):
        cut = _quantile(positive_values, q)
        if cut is None:
            high_count, high_value = 0, 0.0
        else:
            high_count, high_value = connection.execute(
                "SELECT COUNT(*), COALESCE(SUM(gmv_90d), 0.0) FROM merchant_sql WHERE eligible = 1 AND gmv_90d >= ?",
                (cut,),
            ).fetchone()
        sensitivity.append({
            "quantile": q,
            "threshold": round(cut, 4) if cut is not None else None,
            "high_count": int(high_count),
            "high_gmv_pct": _ratio(float(high_value), positive_total),
        })
    return {
        "summary": summary,
        "states": states,
        "cohorts": cohorts,
        "concentration": concentration,
        "segments": segments,
        "sensitivity": sensitivity,
    }


def _assert_close(actual, expected, path="root"):
    if isinstance(expected, dict):
        if set(actual) != set(expected):
            raise AssertionError(f"{path} keys differ: {set(actual) ^ set(expected)}")
        for key in expected:
            _assert_close(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        if len(actual) != len(expected):
            raise AssertionError(f"{path} length differs: {len(actual)} != {len(expected)}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            _assert_close(left, right, f"{path}[{index}]")
        return
    if isinstance(expected, float) and actual is not None:
        if not math.isclose(float(actual), expected, rel_tol=1e-9, abs_tol=1e-6):
            raise AssertionError(f"{path} differs: {actual} != {expected}")
        return
    if actual != expected:
        raise AssertionError(f"{path} differs: {actual!r} != {expected!r}")


def _assert_rows(sql_rows, python_rows):
    sql_rows = sql_rows.set_index("mql_id").sort_index()
    python_rows = python_rows.set_index("mql_id").sort_index()
    if list(sql_rows.index) != list(python_rows.index):
        raise AssertionError("merchant mql_id sets differ")
    text_columns = ("seller_id", "origin_group", "status")
    flag_columns = ("observed_seller", "complete_90d", "chronology_error", "eligible")
    for mql_id in python_rows.index:
        for column in text_columns:
            if str(sql_rows.loc[mql_id, column]) != str(python_rows.loc[mql_id, column]):
                raise AssertionError(f"{mql_id}.{column} differs")
        for column in ("contact_date", "won_date"):
            if pd.Timestamp(sql_rows.loc[mql_id, column]) != pd.Timestamp(python_rows.loc[mql_id, column]):
                raise AssertionError(f"{mql_id}.{column} differs")
        for column in flag_columns:
            if bool(sql_rows.loc[mql_id, column]) != bool(python_rows.loc[mql_id, column]):
                raise AssertionError(f"{mql_id}.{column} differs")
        for column in ("orders_90d", "gmv_90d"):
            left, right = sql_rows.loc[mql_id, column], python_rows.loc[mql_id, column]
            if pd.isna(left) and pd.isna(right):
                continue
            if pd.isna(left) or pd.isna(right):
                raise AssertionError(f"{mql_id}.{column} null semantics differ")
            if not math.isclose(float(left), float(right), rel_tol=1e-9, abs_tol=1e-6):
                raise AssertionError(f"{mql_id}.{column} differs: {left} != {right}")


def verify_frames(mql, deals, sellers, orders, items, *, observation_end=None):
    python_table = build_merchant_table(
        mql, deals, sellers, orders, items, observation_end=observation_end
    )
    resolved_end = observation_end
    if resolved_end is None:
        resolved_end = pd.to_datetime(
            orders["order_purchase_timestamp"], format="mixed", errors="raise"
        ).max()
    resolved_end = pd.Timestamp(resolved_end)

    connection = sqlite3.connect(":memory:")
    try:
        for name, frame in (
            ("mql", mql), ("closed_deals", deals), ("sellers", sellers),
            ("orders", orders), ("order_items", items),
        ):
            frame.to_sql(name, connection, index=False, if_exists="replace")
        query = Path(__file__).with_name("merchant_queries.sql").read_text(encoding="utf-8").strip().rstrip(";")
        connection.execute(
            "CREATE TEMP TABLE merchant_sql AS " + query,
            {"observation_end": resolved_end.isoformat(sep=" ")},
        )
        sql_table = pd.read_sql_query("SELECT * FROM merchant_sql ORDER BY mql_id", connection)
        _assert_rows(sql_table, python_table)
        python_summary = summarize_merchants(python_table)
        sql_summary = _sql_summary(connection)
        _assert_close(sql_summary, python_summary)
    finally:
        connection.close()
    return {"verified_sellers": len(python_table), "summary": python_summary}


def main():
    parser = argparse.ArgumentParser(description="Verify merchant metrics with independent SQLite SQL")
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--ecommerce-dir", required=True, type=Path)
    args = parser.parse_args()
    frames = (
        pd.read_csv(args.data_dir / MQL_FILE),
        pd.read_csv(args.data_dir / DEALS_FILE),
        pd.read_csv(args.ecommerce_dir / SELLERS_FILE),
        pd.read_csv(args.ecommerce_dir / ORDERS_FILE),
        pd.read_csv(args.ecommerce_dir / ITEMS_FILE),
    )
    result = verify_frames(*frames)
    summary = result["summary"]["summary"]
    print(
        "MERCHANT_SQL_VERIFIED: "
        f"sellers={result['verified_sellers']} eligible={summary['eligible_closed']} "
        f"activated={summary['activated']} orders_90d={summary['orders_90d']} "
        f"gmv_90d={summary['gmv_90d']:.2f}"
    )


if __name__ == "__main__":
    main()
