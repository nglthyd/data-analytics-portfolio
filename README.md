# 刘涛的数据分析作品集

本仓库是刘涛的公开数据分析作品集，包含两个案例：Olist 营销漏斗渠道分析与陶瓷相关零售交易分析。网页入口为仓库根目录的 `index.html`；页面个人信息仅展示姓名和本人授权的联系电话。

## 主案例：Olist 获客渠道

问题是“哪些渠道值得继续验证”，而不是在缺少成本数据时强行给渠道 ROI 排名。分析使用 [Olist 官方营销分析题](https://github.com/olist/work-at-olist-marketing)所指向的 [Marketing Funnel by Olist](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist) 两张匿名抽样表。该题是历史公开案例，**不是正在招聘的岗位**。

- 全量：8,000 条 MQL，842 条成交，成交率 10.53%。
- 固定线索期（2018-01-01 至 2018-04-30）：4,695 条 MQL，651 条成交，成交率 13.87%。
- 同期付费搜索：916 条线索、145 条成交，15.83%；自然搜索：1,392 条、213 条，15.30%；社交：782 条、55 条，7.03%。
- 两表 `mql_id` 均无重复，842 条成交都可匹配；60 条线索缺来源，1 条成交日期早于首次联系日期。

核心口径：分母是线索期内的全部 MQL；分子是这些 MQL 能关联到的成交记录。`unknown` 与空值独立展示，不被偷偷分配给其他渠道。渠道比较是观察性结果；没有成本和后续卖家价值，不能计算 CAC、ROI 或增量贡献，也不应凭成交率直接调整预算。

## 如何复算

需要 Python 3.10+ 与 `pandas`。从原始数据页下载并解压以下两张 CSV 至同一目录：

- `olist_marketing_qualified_leads_dataset.csv`
- `olist_closed_deals_dataset.csv`

在 PowerShell 中运行：

```powershell
python -m pip install pandas
python .\analysis.py --data-dir '你的原始CSV目录'
python .\verify.py --data-dir '你的原始CSV目录'
```

把示例路径换成你保存 CSV 的目录。`analysis.py` 生成网页使用的 `data/metrics.js`；`verify.py` 用内存 SQLite 独立执行 [`queries.sql`](queries.sql) 中三组 SQL，与 Python 的总量、渠道和月度结果逐项比对，并检查主键、缺失和异常日期。网页是静态 HTML/CSS/JS，可在本机打开预览。

## 第二案例：陶瓷相关零售交易

从公开英国零售数据中按陶瓷相关关键词形成审计子集：22,427 条原始匹配记录，保留 21,655 条历史有效交易；78 个商品、2,585 个客户。有效销售额 GBP 450,066.19 使用进一步排除退款、零价和非正数量后的 21,541 条严格销售记录。页面展示看板截图。该子集不代表中国陶瓷行业整体，也不包含另一个拍卖数据源；不把关键词命中视为完美的行业分类。

## 数据授权与 AI 协作

Olist 原始 CSV 不在本仓库重新分发。原数据页标注 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)；这里的分析是非商业求职展示，并明确归因 Olist。页面和分析脚本由 Codex 辅助制作，数值通过原始 CSV 与独立 SQL 核验。仓库中有代码并不等于本人已能脱离辅助独立复述全部细节；面试前需要按 README 和脚本逐项复盘。
