"""Reproduce the Olist funnel portfolio numbers from the two original CSV files.

Usage (PowerShell): python analysis.py --data-dir "E:/data_analysis/olist-marketing/source"
The public repository intentionally does not redistribute the source CSV files.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


MQL_FILE = "olist_marketing_qualified_leads_dataset.csv"
DEALS_FILE = "olist_closed_deals_dataset.csv"
FOCUS_START = "2018-01-01"
FOCUS_END_EXCLUSIVE = "2018-05-01"


def build_metrics(data_dir: Path) -> dict:
    mql = pd.read_csv(data_dir / MQL_FILE)
    deals = pd.read_csv(data_dir / DEALS_FILE)

    assert set(mql.columns) == {"mql_id", "first_contact_date", "landing_page_id", "origin"}
    assert "mql_id" in deals and "won_date" in deals
    assert mql.mql_id.is_unique and deals.mql_id.is_unique, "mql_id must be unique in both tables"
    assert not mql.mql_id.isna().any() and not deals.mql_id.isna().any()
    assert deals.mql_id.isin(mql.mql_id).all(), "Every closed deal must have a lead"

    leads = mql.copy()
    leads["contact_date"] = pd.to_datetime(leads.first_contact_date, errors="raise")
    deals_small = deals[["mql_id", "won_date"]].copy()
    deals_small["won_date"] = pd.to_datetime(deals_small.won_date, errors="raise")
    leads = leads.merge(deals_small, on="mql_id", how="left", validate="one_to_one")
    leads["won"] = leads.won_date.notna()
    leads["origin_group"] = leads.origin.fillna("(missing)")
    leads["close_days"] = (leads.won_date - leads.contact_date).dt.days

    focus = leads[
        (leads.contact_date >= FOCUS_START)
        & (leads.contact_date < FOCUS_END_EXCLUSIVE)
    ].copy()
    channel = (
        focus.groupby("origin_group", dropna=False)
        .agg(leads=("mql_id", "size"), wins=("won", "sum"))
        .reset_index()
        .rename(columns={"origin_group": "origin"})
        .sort_values(["leads", "origin"], ascending=[False, True])
    )
    channel["conversion_pct"] = channel.wins / channel.leads * 100
    assert int(channel.leads.sum()) == len(focus)
    assert int(channel.wins.sum()) == int(focus.won.sum())

    monthly = (
        leads.assign(month=leads.contact_date.dt.strftime("%Y-%m"))
        .groupby("month")
        .agg(leads=("mql_id", "size"), wins=("won", "sum"))
        .reset_index()
    )
    monthly["conversion_pct"] = monthly.wins / monthly.leads * 100

    nonnegative_lag = leads.close_days.dropna().loc[lambda s: s >= 0]
    negative_lag_count = int((leads.close_days < 0).sum())
    metrics = {
        "source": "Olist Marketing Funnel by Olist (Kaggle)",
        "period": {
            "first_contact_min": leads.contact_date.min().strftime("%Y-%m-%d"),
            "first_contact_max": leads.contact_date.max().strftime("%Y-%m-%d"),
            "last_won_date": deals_small.won_date.max().strftime("%Y-%m-%d"),
            "focus_start": FOCUS_START,
            "focus_end_inclusive": "2018-04-30",
        },
        "audit": {
            "mql_rows": int(len(mql)),
            "deal_rows": int(len(deals)),
            "duplicate_mql_ids": int(mql.mql_id.duplicated().sum()),
            "duplicate_deal_ids": int(deals.mql_id.duplicated().sum()),
            "unmatched_deals": int((~deals.mql_id.isin(mql.mql_id)).sum()),
            "missing_origin": int(mql.origin.isna().sum()),
            "negative_close_days": negative_lag_count,
        },
        "overall": {
            "leads": int(len(leads)),
            "wins": int(leads.won.sum()),
            "conversion_pct": round(float(leads.won.mean() * 100), 2),
        },
        "focus": {
            "leads": int(len(focus)),
            "wins": int(focus.won.sum()),
            "conversion_pct": round(float(focus.won.mean() * 100), 2),
            "channel": [
                {
                    "origin": str(row.origin),
                    "leads": int(row.leads),
                    "wins": int(row.wins),
                    "conversion_pct": round(float(row.conversion_pct), 2),
                }
                for row in channel.itertuples(index=False)
            ],
        },
        "median_nonnegative_close_days": round(float(nonnegative_lag.median()), 1),
        "monthly": [
            {
                "month": str(row.month),
                "leads": int(row.leads),
                "wins": int(row.wins),
                "conversion_pct": round(float(row.conversion_pct), 2),
            }
            for row in monthly.itertuples(index=False)
        ],
    }
    assert metrics["overall"]["wins"] == metrics["audit"]["deal_rows"]
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).parent / "data" / "metrics.js"
    )
    args = parser.parse_args()
    metrics = build_metrics(args.data_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "window.OLIST_METRICS = " + json.dumps(metrics, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
