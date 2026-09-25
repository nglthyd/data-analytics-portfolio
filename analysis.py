"""Reproduce the Olist funnel portfolio numbers from the two original CSV files.

Usage (PowerShell):
python analysis.py --data-dir "E:/data_analysis/olist-marketing/source" `
  --ecommerce-dir "E:/data_analysis/olist-marketing/ecommerce-source"
The public repository intentionally does not redistribute the source CSV files.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


MQL_FILE = "olist_marketing_qualified_leads_dataset.csv"
DEALS_FILE = "olist_closed_deals_dataset.csv"
SELLERS_FILE = "olist_sellers_dataset.csv"
ORDERS_FILE = "olist_orders_dataset.csv"
ITEMS_FILE = "olist_order_items_dataset.csv"
FOCUS_START = "2018-01-01"
FOCUS_END_EXCLUSIVE = "2018-05-01"


def _require_columns(frame: pd.DataFrame, name: str, required: set[str]) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"{name} missing required columns: {missing}")


def _parse_date(frame: pd.DataFrame, column: str) -> pd.Series:
    try:
        return pd.to_datetime(frame[column], format="mixed", errors="raise")
    except (TypeError, ValueError) as error:
        raise ValueError(f"invalid {column}: {error}") from error


def build_lead_value_table(
    mql: pd.DataFrame,
    deals: pd.DataFrame,
    sellers: pd.DataFrame,
    orders: pd.DataFrame,
    items: pd.DataFrame,
    *,
    observation_end: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Return one row per MQL with observed 90-day order value.

    The comparison window starts at first contact. Orders must also occur on or
    after the deal's won date. Incomplete 90-day observations remain missing;
    complete observations without a conversion or order are explicit zeroes.
    """

    _require_columns(mql, "mql", {"mql_id", "first_contact_date", "origin"})
    _require_columns(deals, "closed deals", {"mql_id", "seller_id", "won_date"})
    _require_columns(sellers, "sellers", {"seller_id"})
    _require_columns(orders, "orders", {"order_id", "order_status", "order_purchase_timestamp"})
    _require_columns(items, "order items", {"order_id", "order_item_id", "seller_id", "price"})

    if mql["mql_id"].isna().any() or not mql["mql_id"].is_unique:
        raise ValueError("mql_id must be unique and non-null in MQL data")
    if deals["mql_id"].isna().any() or not deals["mql_id"].is_unique:
        raise ValueError("mql_id must be unique and non-null in closed deals")
    if not deals["mql_id"].isin(mql["mql_id"]).all():
        raise ValueError("Every closed deal must match an MQL")
    nonnull_deal_sellers = deals["seller_id"].dropna()
    if nonnull_deal_sellers.duplicated().any():
        raise ValueError("seller_id must be unique in closed deals")
    if sellers["seller_id"].isna().any() or not sellers["seller_id"].is_unique:
        raise ValueError("seller_id must be unique and non-null in sellers data")
    if orders["order_id"].isna().any() or not orders["order_id"].is_unique:
        raise ValueError("order_id must be unique and non-null in orders data")
    if items[["order_id", "order_item_id"]].isna().any().any() or items.duplicated(
        ["order_id", "order_item_id"]
    ).any():
        raise ValueError("order_id + order_item_id must be unique and non-null in order items")
    if not items["order_id"].isin(orders["order_id"]).all():
        raise ValueError("Every order item must match an order")
    if not items["seller_id"].isin(sellers["seller_id"]).all():
        raise ValueError("Every order item seller_id must match sellers data")

    leads = mql.copy()
    leads["contact_date"] = _parse_date(leads, "first_contact_date")
    deal_map = deals[["mql_id", "seller_id", "won_date"]].copy()
    deal_map["won_date"] = _parse_date(deal_map, "won_date")
    order_map = orders[["order_id", "order_status", "order_purchase_timestamp"]].copy()
    order_map["order_purchase_timestamp"] = _parse_date(order_map, "order_purchase_timestamp")

    if observation_end is None:
        observation_end = order_map["order_purchase_timestamp"].max()
    observation_end = pd.Timestamp(observation_end)

    leads = leads.merge(deal_map, on="mql_id", how="left", validate="one_to_one")
    leads["origin_group"] = leads["origin"].fillna("(missing)")
    leads["won"] = leads["won_date"].notna()
    leads["observed_seller"] = leads["seller_id"].isin(sellers["seller_id"])
    leads["complete_90d"] = leads["contact_date"] + pd.Timedelta(days=90) <= observation_end
    leads["close_days"] = (leads["won_date"] - leads["contact_date"]).dt.days

    deal_leads = leads.loc[
        leads["seller_id"].notna(),
        ["mql_id", "seller_id", "contact_date", "won_date", "complete_90d"],
    ]
    item_orders = items[["order_id", "order_item_id", "seller_id", "price"]].merge(
        order_map,
        on="order_id",
        how="left",
        validate="many_to_one",
    )
    linked = deal_leads.merge(item_orders, on="seller_id", how="inner", validate="one_to_many")
    valid = linked.loc[
        linked["complete_90d"]
        & linked["order_status"].eq("delivered")
        & linked["order_purchase_timestamp"].ge(linked["won_date"])
        & linked["order_purchase_timestamp"].ge(linked["contact_date"])
        & linked["order_purchase_timestamp"].lt(
            linked["contact_date"] + pd.Timedelta(days=90)
        )
    ]
    value = (
        valid.groupby("mql_id")
        .agg(orders_90d=("order_id", "nunique"), gmv_90d=("price", "sum"))
        .reset_index()
    )
    leads = leads.merge(value, on="mql_id", how="left", validate="one_to_one")
    complete = leads["complete_90d"]
    leads.loc[complete, "orders_90d"] = leads.loc[complete, "orders_90d"].fillna(0)
    leads.loc[complete, "gmv_90d"] = leads.loc[complete, "gmv_90d"].fillna(0.0)
    leads["orders_90d"] = leads["orders_90d"].astype("Int64")
    leads["activated_seller_90d"] = leads["orders_90d"].gt(0).astype("boolean")
    return leads


def summarize_value_by_channel(lead_values: pd.DataFrame) -> pd.DataFrame:
    """Summarize complete 90-day MQL observations by acquisition channel."""

    required = {
        "mql_id",
        "origin_group",
        "won",
        "observed_seller",
        "complete_90d",
        "activated_seller_90d",
        "orders_90d",
        "gmv_90d",
    }
    _require_columns(lead_values, "lead values", required)
    complete = lead_values.loc[lead_values["complete_90d"]].copy()
    summary = (
        complete.groupby("origin_group", dropna=False)
        .agg(
            mqls=("mql_id", "size"),
            wins=("won", "sum"),
            observed_sellers=("observed_seller", "sum"),
            activated_sellers_90d=("activated_seller_90d", "sum"),
            orders_90d=("orders_90d", "sum"),
            gmv_90d=("gmv_90d", "sum"),
        )
        .reset_index()
        .rename(columns={"origin_group": "origin"})
    )
    summary["conversion_pct"] = summary["wins"] / summary["mqls"] * 100
    summary["observed_pct_of_wins"] = (
        summary["observed_sellers"] / summary["wins"].where(summary["wins"].gt(0)) * 100
    )
    summary["activation_pct_of_mql"] = summary["activated_sellers_90d"] / summary["mqls"] * 100
    summary["orders_per_mql_90d"] = summary["orders_90d"] / summary["mqls"]
    summary["gmv_per_mql_90d"] = summary["gmv_90d"] / summary["mqls"]
    return summary.sort_values(["mqls", "origin"], ascending=[False, True]).reset_index(drop=True)


def _round_or_none(value: float, digits: int = 2) -> float | None:
    return None if pd.isna(value) else round(float(value), digits)


def build_metrics(data_dir: Path, ecommerce_dir: Path | None = None) -> dict:
    mql = pd.read_csv(data_dir / MQL_FILE)
    deals = pd.read_csv(data_dir / DEALS_FILE)

    _require_columns(mql, "mql", {"mql_id", "first_contact_date", "origin"})
    _require_columns(deals, "closed deals", {"mql_id", "won_date"})
    if mql.mql_id.isna().any() or not mql.mql_id.is_unique:
        raise ValueError("mql_id must be unique and non-null in MQL data")
    if deals.mql_id.isna().any() or not deals.mql_id.is_unique:
        raise ValueError("mql_id must be unique and non-null in closed deals")
    if not deals.mql_id.isin(mql.mql_id).all():
        raise ValueError("Every closed deal must match an MQL")

    leads = mql.copy()
    leads["contact_date"] = _parse_date(leads, "first_contact_date")
    deals_small = deals[["mql_id", "won_date"]].copy()
    deals_small["won_date"] = _parse_date(deals_small, "won_date")
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
        "source": "Olist Marketing Funnel and Brazilian E-Commerce by Olist (Kaggle)",
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

    if ecommerce_dir is not None:
        _require_columns(deals, "closed deals", {"seller_id"})
        sellers = pd.read_csv(ecommerce_dir / SELLERS_FILE)
        orders = pd.read_csv(ecommerce_dir / ORDERS_FILE)
        items = pd.read_csv(ecommerce_dir / ITEMS_FILE)
        lead_values = build_lead_value_table(mql, deals, sellers, orders, items)
        observation_end = _parse_date(orders, "order_purchase_timestamp").max()
        complete = lead_values.loc[lead_values["complete_90d"]].copy()
        focus_values = lead_values.loc[
            lead_values["complete_90d"]
            & lead_values["contact_date"].ge(FOCUS_START)
            & lead_values["contact_date"].lt(FOCUS_END_EXCLUSIVE)
        ].copy()
        channel_value = summarize_value_by_channel(focus_values)

        deal_seller_ids = deals["seller_id"].dropna()
        observable_deals = deal_seller_ids.isin(sellers["seller_id"])
        seller_count_by_order = items.groupby("order_id")["seller_id"].nunique()

        deal_order_links = (
            deals[["seller_id", "won_date"]]
            .dropna(subset=["seller_id"])
            .assign(won_date=lambda frame: _parse_date(frame, "won_date"))
            .merge(
                items[["order_id", "seller_id"]].drop_duplicates(),
                on="seller_id",
                how="inner",
                validate="one_to_many",
            )
            .merge(
                orders[["order_id", "order_status", "order_purchase_timestamp"]].assign(
                    order_purchase_timestamp=lambda frame: _parse_date(
                        frame, "order_purchase_timestamp"
                    )
                ),
                on="order_id",
                how="left",
                validate="many_to_one",
            )
        )
        pre_won_delivered_orders = deal_order_links.loc[
            deal_order_links["order_status"].eq("delivered")
            & deal_order_links["order_purchase_timestamp"].lt(deal_order_links["won_date"]),
            "order_id",
        ].nunique()

        channel_rows = []
        for row in channel_value.itertuples(index=False):
            channel_rows.append(
                {
                    "origin": str(row.origin),
                    "mqls": int(row.mqls),
                    "wins": int(row.wins),
                    "observed_sellers": int(row.observed_sellers),
                    "activated_sellers_90d": int(row.activated_sellers_90d),
                    "orders_90d": int(row.orders_90d),
                    "gmv_90d": round(float(row.gmv_90d), 2),
                    "conversion_pct": _round_or_none(row.conversion_pct),
                    "observed_pct_of_wins": _round_or_none(row.observed_pct_of_wins),
                    "activation_pct_of_mql": _round_or_none(row.activation_pct_of_mql),
                    "orders_per_mql_90d": _round_or_none(row.orders_per_mql_90d, 4),
                    "gmv_per_mql_90d": _round_or_none(row.gmv_per_mql_90d),
                    "actionable": str(row.origin) not in {"unknown", "(missing)"},
                    "low_sample": int(row.mqls) < 150,
                }
            )

        metrics["period"].update(
            {
                "order_purchase_min": _parse_date(orders, "order_purchase_timestamp")
                .min()
                .strftime("%Y-%m-%d %H:%M:%S"),
                "order_purchase_max": observation_end.strftime("%Y-%m-%d %H:%M:%S"),
                "observation_end": observation_end.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        metrics["audit"].update(
            {
                "seller_rows": int(len(sellers)),
                "order_rows": int(len(orders)),
                "order_item_rows": int(len(items)),
                "deal_sellers": int(len(deal_seller_ids)),
                "observable_deal_sellers": int(observable_deals.sum()),
                "unobserved_deal_sellers": int((~observable_deals).sum()),
                "multi_seller_orders": int(seller_count_by_order.gt(1).sum()),
                "pre_won_delivered_orders": int(pre_won_delivered_orders),
            }
        )
        metrics["downstream"] = {
            "window_days": 90,
            "time_anchor": "first_contact_date",
            "valid_order_status": "delivered",
            "value_field": "order_items.price",
            "complete_mqls": int(len(complete)),
            "incomplete_mqls": int((~lead_values["complete_90d"]).sum()),
            "wins": int(complete["won"].sum()),
            "observed_sellers": int(complete["observed_seller"].sum()),
            "activated_sellers_90d": int(complete["activated_seller_90d"].sum()),
            "orders_90d": int(complete["orders_90d"].sum()),
            "gmv_90d": round(float(complete["gmv_90d"].sum()), 2),
            "gmv_per_mql_90d": round(float(complete["gmv_90d"].sum() / len(complete)), 2),
            "focus": {
                "start": FOCUS_START,
                "end_exclusive": FOCUS_END_EXCLUSIVE,
                "complete_mqls": int(len(focus_values)),
                "wins": int(focus_values["won"].sum()),
                "observed_sellers": int(focus_values["observed_seller"].sum()),
                "activated_sellers_90d": int(focus_values["activated_seller_90d"].sum()),
                "orders_90d": int(focus_values["orders_90d"].sum()),
                "gmv_90d": round(float(focus_values["gmv_90d"].sum()), 2),
            },
            "channel": channel_rows,
        }

        assert sum(row["mqls"] for row in channel_rows) == len(focus_values)
        assert round(sum(row["gmv_90d"] for row in channel_rows), 2) == round(
            float(focus_values["gmv_90d"].sum()), 2
        )
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--ecommerce-dir", type=Path)
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).parent / "data" / "metrics.js"
    )
    args = parser.parse_args()
    metrics = build_metrics(args.data_dir, ecommerce_dir=args.ecommerce_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "window.OLIST_METRICS = " + json.dumps(metrics, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
