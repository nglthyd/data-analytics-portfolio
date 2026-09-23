(() => {
  "use strict";
  const data = window.OLIST_METRICS;
  if (!data) {
    document.getElementById("channel-chart").textContent = "指标文件未加载，请刷新页面。";
    return;
  }

  const formatCount = (number) => Number(number).toLocaleString("zh-CN");
  const formatPct = (number) => `${Number(number).toFixed(2)}%`;
  const put = (id, value) => { document.getElementById(id).textContent = value; };
  const byOrigin = new Map(data.focus.channel.map((row) => [row.origin, row]));
  const name = {
    organic_search: "自然搜索",
    paid_search: "付费搜索",
    direct_traffic: "直接访问",
    social: "社交",
    email: "邮件",
    referral: "推荐",
  };

  put("all-leads", formatCount(data.overall.leads));
  put("all-wins", formatCount(data.overall.wins));
  put("all-conversion", formatPct(data.overall.conversion_pct));
  put("focus-conversion", formatPct(data.focus.conversion_pct));
  for (const [id, origin] of Object.entries({
    "paid-rate": "paid_search", "organic-rate": "organic_search",
    "social-rate": "social", "email-rate": "email", "unknown-rate": "unknown",
  })) put(id, formatPct(byOrigin.get(origin).conversion_pct));

  const chart = document.getElementById("channel-chart");
  for (const origin of ["paid_search", "organic_search", "direct_traffic", "referral", "social", "email"]) {
    const row = byOrigin.get(origin);
    const item = document.createElement("div");
    item.className = `channel-row${row.conversion_pct < 10 ? " low" : ""}`;
    item.setAttribute("role", "listitem");
    item.setAttribute("aria-label", `${name[origin]}：${row.leads} 条线索，${row.wins} 条成交，成交率 ${formatPct(row.conversion_pct)}`);

    const label = document.createElement("span");
    label.className = "channel-name";
    label.textContent = name[origin];
    const track = document.createElement("div");
    track.className = "channel-bar-track";
    track.setAttribute("aria-hidden", "true");
    const bar = document.createElement("div");
    bar.className = "channel-bar";
    bar.style.width = `${Math.max(0, Math.min(100, row.conversion_pct / 20 * 100))}%`;
    track.appendChild(bar);
    const value = document.createElement("span");
    value.className = "channel-value";
    value.textContent = formatPct(row.conversion_pct);
    const count = document.createElement("small");
    count.className = "channel-count";
    count.textContent = `n=${formatCount(row.leads)}`;
    value.appendChild(count);
    item.append(label, track, value);
    chart.appendChild(item);
  }

  const table = document.getElementById("channel-table");
  for (const row of data.focus.channel) {
    const tr = document.createElement("tr");
    const classification = row.origin === "unknown" || row.origin === "(missing)"
      ? "未归因，暂不作投放依据" : row.leads < 150 ? "样本较少" : "可比较";
    for (const value of [row.origin, formatCount(row.leads), formatCount(row.wins), formatPct(row.conversion_pct), classification]) {
      const td = document.createElement("td");
      td.textContent = value;
      if (value === classification && classification !== "可比较") td.className = "warning-tag";
      tr.appendChild(td);
    }
    table.appendChild(tr);
  }
})();
