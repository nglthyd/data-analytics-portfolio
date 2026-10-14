"""Merchant-level operations on the observed Olist sample.

build_merchant_table returns one row per closed seller with original lead
fields, eligible, chronology_error and status. Status precedence: chronology
error, incomplete window, unknown coverage, then observed activation status.
Independent audit flags may overlap. summarize_merchants emits only aggregate
summary/states/cohorts/concentration/segments/sensitivity, never original IDs.
Concentration denominator is positive-GMV eligible sellers; unknown segment
GMV stays missing and is never a statement of real zero value.
"""
import math
import numpy as np
import pandas as pd
from analysis import build_lead_value_table, _require_columns

STATES = ("chronology_error", "incomplete_window", "unknown_coverage", "observable_no_activation", "activated")


def build_merchant_table(mql, deals, sellers, orders, items, *, observation_end=None):
    frames = [frame.copy() for frame in (mql,deals,sellers,orders,items)]
    for frame,column in ((frames[0],"first_contact_date"),(frames[1],"won_date"),(frames[3],"order_purchase_timestamp")):
        _require_columns(frame,column,{column})
        try:
            dates = pd.to_datetime(frame[column],format="mixed",errors="raise")
        except (ValueError,TypeError) as exc:
            raise ValueError(f"invalid {column}") from exc
        if dates.isna().any():
            raise ValueError(f"null {column}")
    _require_columns(frames[1],"deals",{"seller_id"})
    if frames[1].seller_id.isna().any():
        raise ValueError("null seller_id in closed deals")
    _require_columns(frames[4],"items",{"price"})
    try:
        price = pd.to_numeric(frames[4].price,errors="raise")
    except (ValueError,TypeError) as exc:
        raise ValueError("invalid price") from exc
    if not np.isfinite(price.to_numpy(dtype=float)).all() or price.lt(0).any():
        raise ValueError("price must be finite and nonnegative")
    frames[4]["price"] = price.astype(float)
    end = observation_end
    if end is None:
        end = pd.to_datetime(frames[3].order_purchase_timestamp,format="mixed").max()
    try:
        end = pd.Timestamp(end)
    except (ValueError,TypeError) as exc:
        raise ValueError("invalid observation_end") from exc
    if pd.isna(end):
        raise ValueError("observation_end required for empty orders")
    table = build_lead_value_table(*frames,observation_end=end)
    table = table.loc[table.won].copy().reset_index(drop=True)
    table["chronology_error"] = table.won_date.lt(table.contact_date)
    table["eligible"] = table.observed_seller & table.complete_90d & ~table.chronology_error
    table["status"] = "activated"
    table.loc[table.orders_90d.eq(0).fillna(False),"status"] = "observable_no_activation"
    table.loc[~table.observed_seller,"status"] = "unknown_coverage"
    table.loc[~table.complete_90d,"status"] = "incomplete_window"
    table.loc[table.chronology_error,"status"] = "chronology_error"
    table.loc[~table.eligible,["orders_90d","gmv_90d"]] = pd.NA
    table["activated_seller_90d"] = table.orders_90d.gt(0).astype("boolean")
    return table


def summarize_merchants(table):
    eligible = table.loc[table.eligible].copy()
    activated = eligible.orders_90d.gt(0)
    total_gmv = float(eligible.gmv_90d.sum())
    total_orders = int(eligible.orders_90d.sum())
    ratio = lambda n,d: round(float(n)/d*100,4) if d else None
    summary = {"total_closed":len(table),"observable_closed":int(table.observed_seller.sum()),
        "unknown_coverage_closed":int((~table.observed_seller).sum()),"incomplete_closed":int((~table.complete_90d).sum()),
        "chronology_error_closed":int(table.chronology_error.sum()),"eligible_closed":len(eligible),
        "activated":int(activated.sum()),"observable_no_activation":int(eligible.orders_90d.eq(0).sum()),
        "activation_pct_of_eligible":ratio(int(activated.sum()),len(eligible)),"orders_90d":total_orders,
        "gmv_90d":round(total_gmv,2),"gmv_per_seller_order":round(total_gmv/total_orders,4) if total_orders else None}
    states = [{"status":status,"count":int(table.status.eq(status).sum())} for status in STATES]
    months = table.contact_date.dt.strftime("%Y-%m")
    cohorts = []
    for month in sorted(months.unique()):
        group = table.loc[months.eq(month)]
        subset = group.loc[group.eligible]
        active = int(subset.orders_90d.gt(0).sum())
        cohorts.append({"contact_month":str(month),"total_closed":len(group),"observable_closed":int(group.observed_seller.sum()),
            "eligible_closed":len(subset),"activated":active,"activation_pct_of_eligible":ratio(active,len(subset)),
            "gmv_90d":round(float(subset.gmv_90d.sum()),2),"low_sample":len(subset)<30})
    positive = eligible.loc[eligible.gmv_90d.gt(0)].sort_values(["gmv_90d","seller_id"],ascending=[False,True])
    n = len(positive)
    positive_total = float(positive.gmv_90d.sum())
    concentration = {"n":n,"top10_count":math.ceil(n*.1),"top20_count":math.ceil(n*.2),
        "top10_gmv_pct":ratio(float(positive.gmv_90d.head(math.ceil(n*.1)).sum()),positive_total),
        "top20_gmv_pct":ratio(float(positive.gmv_90d.head(math.ceil(n*.2)).sum()),positive_total),"curve":[]}
    cumulative = 0.0
    for rank,value in enumerate(positive.gmv_90d,1):
        cumulative += float(value)
        concentration["curve"].append({"rank":rank,"merchants_pct":ratio(rank,n),"gmv_pct":ratio(cumulative,positive_total)})
    threshold = float(positive.gmv_90d.quantile(.75)) if n else None
    work = table.copy()
    work["segment"] = work.status
    work.loc[work.status.eq("activated"),"segment"] = "other_activated"
    if threshold is not None:
        work.loc[work.eligible & work.gmv_90d.ge(threshold),"segment"] = "high_contribution"
    segments = []
    for name in ("high_contribution","other_activated","observable_no_activation","unknown_coverage","incomplete_window","chronology_error"):
        group = work.loc[work.segment.eq(name)]
        known = group.loc[group.eligible]
        value = float(known.gmv_90d.sum()) if name in {"high_contribution","other_activated","observable_no_activation"} else None
        segments.append({"segment":name,"count":len(group),"gmv_90d":round(value,2) if value is not None else None,
            "threshold":round(threshold,4) if name=="high_contribution" and threshold is not None else None})
    sensitivity = []
    for q in (.70,.75,.80):
        cut = float(positive.gmv_90d.quantile(q)) if n else None
        high = positive.loc[positive.gmv_90d.ge(cut)] if cut is not None else positive
        sensitivity.append({"quantile":q,"threshold":round(cut,4) if cut is not None else None,
            "high_count":len(high),"high_gmv_pct":ratio(float(high.gmv_90d.sum()),positive_total)})
    return {"summary":summary,"states":states,"cohorts":cohorts,"concentration":concentration,"segments":segments,"sensitivity":sensitivity}
