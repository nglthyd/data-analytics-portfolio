# 真实数据验证报告

验证时间：2026-09-25 19:44（Asia/Hong_Kong）  
运行环境：Python 3.12.14，pandas 3.0.1，SQLite（Python 标准库）

## 输入文件指纹

| 文件 | 行数 | SHA256 |
|---|---:|---|
| `olist_marketing_qualified_leads_dataset.csv` | 8,000 | `5537753B7549CE4068E52E2402C29F2773C5375FC0575520AE8F3F301F666573` |
| `olist_closed_deals_dataset.csv` | 842 | `1433F402D8FFF00CA167579DE641D9525F6E846368958C166F699EF1B0C31F3D` |
| `olist_sellers_dataset.csv` | 3,095 | `1F643D2B950373B85735E7794B20986F528D7A000432E7C6F9BCBB44D0846A0E` |
| `olist_orders_dataset.csv` | 99,441 | `8DF58EF3D2D7E9944010F7BEECD9B75367F5588EC6E3C91CEC19AE3345EF9ECF` |
| `olist_order_items_dataset.csv` | 112,650 | `0BC4D068C4FE38CBB01BD90E8746E3C613FE7B4BAEF75FAB7B0E329701C3E279` |

完整电商 ZIP 的 SHA256 为 `967E41E04FC306FE604E2A693F488995A8B41E5047418F8A5C8E4ABD6DECA784`。仓库不包含这些原始文件。

## 运行命令

```powershell
python -W error .\analysis.py `
  --data-dir '营销CSV目录' `
  --ecommerce-dir '电商CSV目录' `
  --output '.\data\metrics.js'

python -W error .\verify.py `
  --data-dir '营销CSV目录' `
  --ecommerce-dir '电商CSV目录'

python -W error -m unittest -v test_analysis.py test_repository.py
```

## 数据契约结果

- MQL、成交、商家、订单主键均唯一且非空。
- `order_id + order_item_id` 复合键唯一且非空。
- 842 条成交全部匹配 MQL；所有订单商品行都匹配订单和商家。
- 60 条 MQL 缺失来源；1 条成交日期早于首次接触日期。
- 842 个成交商家中，380 个进入公开电商样本，462 个未进入。
- 公开样本含 1,278 个多商家订单；有效价值计算按商家商品行归属。
- 匹配商家的已交付订单中，成交日前订单为 0。

## 关键对账结果

```text
PASS: 3 funnel SQL queries match Python; source-quality checks pass
PASS: 3 full-funnel SQL queries match Python; 90-day value totals and channels close
```

Python 与 SQLite 对齐的全量 90 天结果：

| 阶段 | 数量 |
|---|---:|
| 完整观察 MQL | 8,000 |
| 成交 | 842 |
| 可观测成交商家 | 380 |
| 90 天激活商家 | 245 |
| 90 天去重订单 | 1,693 |
| 90 天商品 GMV | 261,665.04 |

固定线索期 2018-01 至 2018-04：4,695 条 MQL、651 个成交、315 个可观测商家、199 个 90 天激活商家、1,400 个订单、商品 GMV 229,124.91。渠道 MQL 合计与该分母相等，渠道 GMV 合计与该金额相等。

## 尚未消除的限制

验证能证明计算在既定口径下一致，不能证明样本无选择偏差。跨数据集只有 45.13% 的成交商家可继续观察；缺失成本、退款净额、利润和实验分组。页面因此使用“可观测 GMV”并把 `unknown` 标为不可执行，不输出 ROI 或预算结论。

