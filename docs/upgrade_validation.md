# Olist作品集升级核验记录

## 范围与版本

- 候选工作目录：`data-analytics-portfolio-upgrade`
- 基线公开提交：`5e73c74d0e54fc6cdc5fd4ac9e166408d258c247`
- 本地分支：`codex/olist-ops-upgrade`
- 发布授权：2026-10-15用户要求将升级版同步到原GitHub Pages。旧工作目录和原始CSV不覆盖；网站版本标识为 `olist-ops-20261015`，发布提交以GitHub的main分支为准。

## 原始数据指纹

| 文件 | 行数 | SHA-256 |
| --- | ---: | --- |
| olist_marketing_qualified_leads_dataset.csv | 8,000 | `5537753b7549ce4068e52e2402c29f2773c5375fc0575520ae8f3f301f666573` |
| olist_closed_deals_dataset.csv | 842 | `1433f402d8fff00ca167579de641d9525f6e846368958c166f699ef1b0c31f3d` |
| olist_sellers_dataset.csv | 3,095 | `1f643d2b950373b85735e7794b20986f528d7a000432e7c6f9bcbb44d0846a0e` |
| olist_orders_dataset.csv | 99,441 | `8df58ef3d2d7e9944010f7beecd9b75367f5588ec6e3c91cec19ae3345ef9ecf` |
| olist_order_items_dataset.csv | 112,650 | `0bc4d068c4fe38cbb01bd90e8746e3c613fe7b4baef75fab7b0e329701c3e279` |

## 已验证结果

- 旧版9项单元测试和6组SQLite核验在升级前通过，旧指标保留。
- 新商家分析以原始五表为输入；Python与独立SQLite逐商家核对ID、状态、时间、空值、订单数和金额，并核对状态、月份、集中度和分群汇总。
- 真实数据核验结果：842个成交商家、379个运营合格商家、245个激活、134个未激活、1条日期异常、1,693个商家订单、R$261,665.04商品GMV。
- 5张SVG、聚合JSON与业务报告连续生成两次SHA-256一致；生成过程不导出商家、MQL、订单或客户原始ID。

## 最终验收

- `python -m unittest -v`：31项通过，0失败；包含公开聚合字段名拦截、32位原始标识形态拦截和非有限数值拦截。
- 旧版 `verify.py`：3组漏斗查询与3组五表价值查询均与Python结果一致。
- `verify_merchant.py`：842个成交商家的逐行状态、空值、订单和金额，以及状态、月份、集中度和分群汇总均与独立SQLite重算一致。
- `verify_page.mjs`：Microsoft Edge无头模式下完成1440px桌面与390px手机验收；旧版与新增指标均渲染，5张SVG加载成功，月份表行数一致，无脚本错误和横向溢出。
- Word理解手册经Microsoft Word只读导出为6页内部QA PDF并逐页检查；标题边框和空白尾页已修正，最终6页无截断、重叠或破表。可访问性审计为high=0、medium=0、low=0。
- 公开候选文件扫描未发现本机用户目录、D盘项目根或E盘路径；聚合输出未包含seller、MQL、order或customer原始ID。
- 发布门禁重跑：31项单元测试、原有6组SQL核验、新版842商家逐行SQL核验与本地双视口测试。`verify_page.mjs` 可通过 `PORTFOLIO_BASE_URL` 指向线上，用相同断言核对版本、数字、5张图和移动布局，避免仅确认代码已推送就宣布上线。

内置文档渲染脚本所需的LibreOffice不在当前工作区依赖中，因此Word视觉QA使用本机Microsoft Word只读导出完成；这不改变交付DOCX内容。

## 结论边界

本升级展示真实历史样本的分析和一份未执行的运营验证方案。没有真实上线、A/B结果、增量收益、利润、ROI、CAC或完整LTV。AI参与实现不等同于本人已独立掌握，理解情况需要另行口述和手写验证。
