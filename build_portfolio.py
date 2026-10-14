"""Rebuild aggregate public metrics, SVG evidence and a measured business report."""
import argparse
import hashlib
import json
import math
import re
from pathlib import Path

import pandas as pd
from analysis import build_metrics, MQL_FILE, DEALS_FILE, SELLERS_FILE, ORDERS_FILE, ITEMS_FILE
from portfolio_charts import generate_charts

PRIVATE_FIELDS = {"seller_id", "mql_id", "order_id", "customer_id", "first_contact_date", "won_date"}
RAW_IDENTIFIER_PATTERN = re.compile(r"^[0-9a-fA-F]{32}$")


def validate_public_aggregates(value):
    if isinstance(value, dict):
        if PRIVATE_FIELDS.intersection(value):
            raise ValueError("Private row fields must not enter public aggregates")
        for child in value.values():
            validate_public_aggregates(child)
    elif isinstance(value, list):
        for child in value:
            validate_public_aggregates(child)
    elif isinstance(value, str) and RAW_IDENTIFIER_PATTERN.fullmatch(value):
        raise ValueError("Raw identifier-like value must not enter public aggregates")
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Non-finite number in public export")


def business_report(ops):
    s = ops["summary"]
    c = ops["concentration"]
    rate = s.get("activation_pct_of_eligible")
    rate_text = "不适用" if rate is None else f"{rate:.2f}%"
    lines = ["# Olist 商家运营分析报告", "",
             "## 结论与范围", "",
             "这是一份历史匿名公开样本的分析，不是受雇企业的真实运营业绩。",
             f"成交商家{s['total_closed']}家，其中公开样本可观测{s['observable_closed']}家、不可观测{s['unknown_coverage_closed']}家。",
             f"进入运营分析的合格商家{s['eligible_closed']}家；90天已激活{s['activated']}家、可观测未激活{s['observable_no_activation']}家，组内激活率{rate_text}。",
             f"合格样本记录{s['orders_90d']}个商家订单，商品GMV为R$ {s['gmv_90d']:,.2f}。这不是利润、ROI或完整LTV。", "",
             "## 为什么这些商家值得分析", "",
             "只比较成交率会忽略成交后的经营表现；反过来只看有订单的商家，也会丢掉未激活样本。",
             "可观测性是跨公开数据集的覆盖状态，并非入驻流程里的行为阶段。不可观测商家的经营情况未知，不记作真实零值。", "",
             "## 商家贡献与分组", "",
             f"正GMV合格商家中的前10%按向上取整选{c.get('top10_count', 0)}家，贡献占比为{c.get('top10_gmv_pct', 0) or 0:.2f}%。",
             "高贡献商家采用当前样本正GMV的75%分位阈值；并列值会使人数超过25%，不是VIP规则或最优运营策略。",
             "金额集中只说明样本内贡献依赖少数商家；是否形成经营依赖或存在供给问题，仍需结合库存、履约和服务记录验证。", "",
             "## 首次接触月份分析", "",
             "下表分母是各月可观测、成交日期正常、且完整观察90天的成交商家；不同月份商家构成可能不同。", "",
             "| 首次接触月 | 成交商家 | 合格可观测 | 已激活 | 激活率 | 商品GMV R$ |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in ops["cohorts"]:
        pct = "不适用" if r["activation_pct_of_eligible"] is None else f"{r['activation_pct_of_eligible']:.2f}%"
        lines.append(f"| {r['contact_month']} | {r['total_closed']} | {r['eligible_closed']} | {r['activated']} | {pct} | {r['gmv_90d']:,.2f} |")
    lines += ["", "## 运营下一步", "",
              "先核对日期异常与映射缺口；再对合格可观测未激活商家排查入驻承接、上架或供给问题；这些都是待验证假设。",
              "高贡献商家可作为经营支持试点对象，但应同时保留其他商家对照，避免只关注已经成功者。",
              "实验方案未执行，不能把拟定目标写成实际收益。详细方案见operations_plan.md。", "",
              "## 可以和不可以下的结论", "",
              "可以：在已明确的历史样本和观察窗内描述渠道差异、商家激活和贡献分布。",
              "不可以：把缺失覆盖叫流失；把相关性叫根因；把模拟或试点方案叫上线实验；把商品GMV叫利润。"]
    return "\n".join(lines) + "\n"


def build(data_dir, ecommerce_dir, root):
    from merchant_analysis import build_merchant_table, summarize_merchants
    legacy = build_metrics(data_dir, ecommerce_dir=ecommerce_dir)
    files = [data_dir/MQL_FILE, data_dir/DEALS_FILE, ecommerce_dir/SELLERS_FILE,
             ecommerce_dir/ORDERS_FILE, ecommerce_dir/ITEMS_FILE]
    frames = [pd.read_csv(path) for path in files]
    merchant_table = build_merchant_table(*frames)
    ops = summarize_merchants(merchant_table)
    ops["experiment_status"] = "design_only_not_executed"
    ops["source_fingerprints"] = [{"file": path.name, "rows": len(frame),
                                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                                  for path,frame in zip(files,frames)]
    validate_public_aggregates(ops)
    legacy["merchant_ops"] = ops
    root = Path(root)
    (root/"data").mkdir(exist_ok=True)
    (root/"docs").mkdir(exist_ok=True)
    text = json.dumps(legacy, ensure_ascii=False, indent=2, allow_nan=False)
    (root/"data"/"metrics.js").write_text("window.OLIST_METRICS = " + text + ";\n", encoding="utf-8")
    (root/"data"/"merchant_ops.json").write_text(json.dumps(ops, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    charts = generate_charts(ops, legacy, root/"assets")
    (root/"docs"/"business_report.md").write_text(business_report(ops), encoding="utf-8")
    return {"status":"PORTFOLIO_BUILD_OK", "charts":len(charts), "summary":ops["summary"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--ecommerce-dir", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    print(json.dumps(build(args.data_dir,args.ecommerce_dir,args.root),ensure_ascii=False,indent=2))
