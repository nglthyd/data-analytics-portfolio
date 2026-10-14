(() => {
  "use strict";
  const ops = window.OLIST_METRICS?.merchant_ops;
  const put = (id, text) => { const node = document.getElementById(id); if (node) node.textContent = text; };
  if (!ops) { put("ops-scope", "商家分析数据未加载，请先运行 build_portfolio.py。"); return; }
  const number = value => value == null ? "不适用" : Number(value).toLocaleString("zh-CN");
  const pct = value => value == null ? "不适用" : `${Number(value).toFixed(2)}%`;
  const s = ops.summary;
  put("ops-eligible", number(s.eligible_closed));
  put("ops-no-activation", number(s.observable_no_activation));
  put("ops-activation", pct(s.activation_pct_of_eligible));
  put("ops-anomalies", number(s.chronology_error_closed));
  put("ops-scope", `组内激活率的分母为${number(s.eligible_closed)}家合格可观测成交商家，不是8,000条MQL。${number(s.unknown_coverage_closed)}家成交商家的真实经营表现未知。各类审计标记可能重叠，状态图按明确优先级分组。`);
  const tbody = document.getElementById("ops-cohort-table");
  for (const row of ops.cohorts) {
    const tr = document.createElement("tr");
    for (const value of [row.contact_month, number(row.total_closed), number(row.eligible_closed),
                          number(row.activated), pct(row.activation_pct_of_eligible),
                          Number(row.gmv_90d).toLocaleString("zh-CN", {minimumFractionDigits: 2, maximumFractionDigits: 2})]) {
      const td = document.createElement("td"); td.textContent = value; tr.appendChild(td);
    }
    tbody.appendChild(tr);
  }
})();
