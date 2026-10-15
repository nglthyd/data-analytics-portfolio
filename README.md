# 刘涛｜数据分析作品集

这是一个面向数据分析/数据驱动运营岗位的可复现作品集。主案例把 Olist 营销线索与电商订单接成一条可审计链路：**MQL → 成交 → 可观测商家 → 首次接触后 90 天已交付订单 → 商品 GMV → 商家运营验证方案**。第二案例展示陶瓷相关零售交易的清洗与 BI 看板。

**在线页面：** [nglthyd.github.io/data-analytics-portfolio](https://nglthyd.github.io/data-analytics-portfolio/)

2026-10-15 更新：加入商家观察状态、月份激活、贡献集中度、运营分组与渠道覆盖共5张图，以及尚未执行的商家激活试点方案。网页发布不代表运营试点已经实施。

## 主案例：Olist 获客质量与商家运营分析

### 业务问题

只看成交率会把“带来成交”误当成“带来后续价值”。本案例回答三个更接近业务的问题：

1. 各渠道带来的 MQL 有多少、成交率如何？
2. 成交商家中，有多少能在公开订单样本里继续观察并在 90 天内激活？
3. 在相同线索期和相同观察窗下，各渠道的可观测商品 GMV/MQL 有何差异？

### 关键结果

- 全量 8,000 条 MQL 中有 842 个成交；其中 380 个成交商家能映射到公开电商样本，245 个在首次接触后 90 天内产生已交付订单。
- 完整 90 天观察样本累计 1,693 个商家订单计数、可观测商品 GMV 261,665.04，平均每条 MQL 为 32.71；这里按签约商家分别去重订单后再累计，不等于全站唯一订单数。
- 固定线索期（2018-01-01 至 2018-04-30）内，付费搜索与自然搜索成交率接近（15.83% 与 15.30%），但付费搜索的 90 天激活率和可观测 GMV/MQL 更高（6.00%、59.41 对 4.31%、46.70）。这只是优先验证信号，不是因果结论。
- 社交渠道同期成交率 7.03%、90 天激活率 1.41%、可观测 GMV/MQL 7.87，三个阶段都偏弱，值得优先排查流量质量与承接流程。
- `unknown` 的可观测 GMV/MQL 虽高，但来源不可识别，不能当成可执行渠道；应先修复归因。
- 商家运营口径单独排除 1 条“成交早于首次接触”的日期异常，379 家进入合格观察组，其中 245 家激活、134 家未激活，组内激活率 64.64%。这与以全部 MQL 为分母的渠道激活率不是同一指标。
- 245 家正 GMV 商家中，前 25 家贡献 62.32% 的样本内 GMV。该集中度只用于识别经营关注点，不代表流失风险或投入后收益。

### 结论边界

这里的 GMV 只汇总 `order_items.price`，不含运费、成本、渠道费用、退款净额和利润，因此**不是 ROI、CAC、利润或完整 LTV**。842 个成交商家中有 462 个不在公开订单样本里，下游结果是可观测样本的下界，不等于全部成交商家的真实价值。渠道差异来自历史观察数据，不能直接解释为渠道的因果效果。

## 数据链路与实现

```text
MQL（每条线索一行）
  └─ mql_id → Closed deals（成交及 seller_id）
                  └─ seller_id → Sellers / Order items（商家商品行）
                                      └─ order_id → Orders（状态与购买时间）
```

- Python/pandas：数据契约、日期清洗、MQL 级 90 天价值表、渠道汇总和网页指标导出。
- SQLite：用独立 CTE 查询重新计算总量、渠道和 90 天价值，逐项与 Python 对账。
- HTML/CSS/JavaScript/SVG：不依赖外部图表 CDN，由 `data/metrics.js` 动态绘图。
- unittest + 页面烟雾测试：锁定时间边界、零值保留、重复键、多商家订单粒度和移动端布局。

详细说明：

- [数据字典与五表关系](docs/data_dictionary.md)
- [指标口径与分析方法](docs/methodology.md)
- [真实数据验证报告](docs/validation_report.md)
- [商家运营分析报告](docs/business_report.md)
- [运营行动与验证方案](docs/operations_plan.md)
- [项目理解说明](docs/understanding_guide.md)
- [一页简历候选表述](docs/resume_portfolio_candidate.md)
- [升级核验记录](docs/upgrade_validation.md)
- [数据来源、授权与参考](docs/references.md)

## 如何复现

需要 Python 3.10+。原始 CSV 不在仓库中重新分发；请从 Olist 的两个公开数据页下载并分别解压到营销目录和电商目录。

```powershell
python -m pip install -r .\requirements.txt
python .\analysis.py `
  --data-dir '你的营销CSV目录' `
  --ecommerce-dir '你的电商CSV目录'
python .\verify.py `
  --data-dir '你的营销CSV目录' `
  --ecommerce-dir '你的电商CSV目录'
python .\verify_merchant.py `
  --data-dir '你的营销CSV目录' `
  --ecommerce-dir '你的电商CSV目录'
python .\build_portfolio.py `
  --data-dir '你的营销CSV目录' `
  --ecommerce-dir '你的电商CSV目录'
python -m unittest -v
```

`build_portfolio.py` 同时生成 `data/metrics.js`、聚合运营指标、5 张 SVG 和业务报告；`verify.py` 独立复核旧版 6 组指标，`verify_merchant.py` 通过 [`merchant_queries.sql`](merchant_queries.sql) 从原始五表重算并逐商家对账。完整命令、文件哈希和核验结果见[升级核验记录](docs/upgrade_validation.md)。

## 第二案例：陶瓷相关零售交易

从公开英国零售数据中按陶瓷相关关键词形成审计子集：22,427 条原始匹配记录，保留 21,655 条历史有效交易，覆盖 78 个商品、2,585 个客户。进一步排除退款、零价和非正数量后，21,541 条严格销售记录对应有效销售额 GBP 450,066.19。该子集不代表中国陶瓷行业整体，也不包含另一个拍卖数据源；关键词命中不等于完美行业分类。

## 数据授权与 AI 协作

Olist 数据归原作者所有，来源和授权见[参考页](docs/references.md)。本仓库不重新分发原始 CSV。

本项目使用 Codex 协助检索资料、编写代码和搭建页面。我的责任是确定业务问题和口径、核对数据来源、审查 JOIN 与时间窗、运行 Python/SQL 双重验证并理解最终结论。**AI 协作不是把生成内容直接当答案**；关键数字必须能够从原始数据复算，限制必须明确披露。
