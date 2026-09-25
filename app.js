(() => {
  "use strict";

  const data = window.OLIST_METRICS;
  const missingMessage = "指标文件未加载，请刷新页面或检查 data/metrics.js。";
  if (!data || !data.downstream) {
    const target = document.getElementById("channel-chart");
    if (target) target.textContent = missingMessage;
    return;
  }

  const formatCount = (number) => Number(number).toLocaleString("zh-CN");
  const formatPct = (number) => `${Number(number).toFixed(2)}%`;
  const formatMoney = (number) => `R$ ${Number(number).toLocaleString("zh-CN", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
  const put = (id, value) => {
    const target = document.getElementById(id);
    if (target) target.textContent = value;
  };
  const svgElement = (name, attributes = {}) => {
    const node = document.createElementNS("http://www.w3.org/2000/svg", name);
    for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
    return node;
  };

  const channelNames = {
    organic_search: "自然搜索",
    paid_search: "付费搜索",
    direct_traffic: "直接访问",
    social: "社交",
    email: "邮件",
    referral: "推荐",
    other: "其他",
    display: "展示广告",
    other_publicities: "其他广告",
    unknown: "未知来源",
    "(missing)": "来源缺失",
  };
  const frontByOrigin = new Map(data.focus.channel.map((row) => [row.origin, row]));
  const valueByOrigin = new Map(data.downstream.channel.map((row) => [row.origin, row]));
  const labelFor = (origin) => channelNames[origin] || origin;

  put("all-leads", formatCount(data.downstream.complete_mqls));
  put("all-wins", formatCount(data.downstream.wins));
  put("all-conversion", `${formatPct(data.overall.conversion_pct)} / 全量 MQL`);
  put("observable-sellers", formatCount(data.downstream.observed_sellers));
  put(
    "observable-rate",
    `${formatPct(data.downstream.observed_sellers / data.downstream.wins * 100)} / 成交`,
  );
  put("activated-sellers", formatCount(data.downstream.activated_sellers_90d));
  put(
    "activation-rate",
    `${formatPct(data.downstream.activated_sellers_90d / data.downstream.complete_mqls * 100)} / 全量 MQL`,
  );
  put("focus-conversion", formatPct(data.focus.conversion_pct));
  put("focus-gmv", formatMoney(data.downstream.focus.gmv_90d));

  const summaryIds = {
    paid_search: ["paid-rate", "paid-activation", "paid-value"],
    organic_search: ["organic-rate", "organic-activation", "organic-value"],
    social: ["social-rate", "social-activation", "social-value"],
  };
  for (const [origin, ids] of Object.entries(summaryIds)) {
    const row = valueByOrigin.get(origin);
    put(ids[0], formatPct(row.conversion_pct));
    put(ids[1], formatPct(row.activation_pct_of_mql));
    put(ids[2], formatMoney(row.gmv_per_mql_90d));
  }
  put("unknown-rate", formatPct(valueByOrigin.get("unknown").conversion_pct));
  put("unknown-value", formatMoney(valueByOrigin.get("unknown").gmv_per_mql_90d));

  const mainOrigins = [
    "paid_search",
    "organic_search",
    "direct_traffic",
    "referral",
    "social",
    "email",
  ];
  const channelChart = document.getElementById("channel-chart");
  for (const origin of mainOrigins) {
    const front = frontByOrigin.get(origin);
    const valueData = valueByOrigin.get(origin);
    const item = document.createElement("div");
    item.className = `channel-row${front.conversion_pct < 10 ? " low" : ""}`;
    item.setAttribute("role", "listitem");
    item.setAttribute("data-mark", origin);
    item.setAttribute(
      "aria-label",
      `${labelFor(origin)}：${front.leads} 条 MQL，成交率 ${formatPct(front.conversion_pct)}，90 天激活率 ${formatPct(valueData.activation_pct_of_mql)}`,
    );

    const label = document.createElement("span");
    label.className = "channel-name";
    label.textContent = labelFor(origin);
    const track = document.createElement("div");
    track.className = "channel-bar-track";
    track.setAttribute("aria-hidden", "true");
    const bar = document.createElement("div");
    bar.className = "channel-bar";
    bar.style.width = `${Math.max(0, Math.min(100, front.conversion_pct / 20 * 100))}%`;
    const activation = document.createElement("i");
    activation.className = "activation-marker";
    activation.style.left = `${Math.max(0, Math.min(100, valueData.activation_pct_of_mql / 20 * 100))}%`;
    track.append(bar, activation);
    const number = document.createElement("span");
    number.className = "channel-value";
    number.textContent = formatPct(front.conversion_pct);
    const count = document.createElement("small");
    count.className = "channel-count";
    count.textContent = `n=${formatCount(front.leads)} · 激活 ${formatPct(valueData.activation_pct_of_mql)}`;
    number.appendChild(count);
    item.append(label, track, number);
    channelChart.appendChild(item);
  }

  const funnelChart = document.getElementById("funnel-chart");
  const funnelStages = [
    { label: "完整观察 MQL", value: data.downstream.complete_mqls, note: "统一分母" },
    { label: "已成交", value: data.downstream.wins, note: "相对上一阶段" },
    { label: "可观测商家", value: data.downstream.observed_sellers, note: "跨公开样本覆盖" },
    { label: "90 天激活", value: data.downstream.activated_sellers_90d, note: "至少 1 个有效订单" },
  ];
  funnelStages.forEach((stage, index) => {
    const previous = index === 0 ? stage.value : funnelStages[index - 1].value;
    const rate = stage.value / previous * 100;
    const item = document.createElement("div");
    item.className = "funnel-stage";
    item.setAttribute("role", "listitem");
    item.setAttribute("data-mark", `${index + 1}`);
    item.setAttribute(
      "aria-label",
      `${stage.label} ${formatCount(stage.value)}，${index === 0 ? "全链路分母" : `相对上一阶段 ${formatPct(rate)}`}`,
    );
    const step = document.createElement("span");
    step.className = "funnel-index";
    step.textContent = String(index + 1).padStart(2, "0");
    const label = document.createElement("span");
    label.className = "funnel-label";
    label.textContent = stage.label;
    const number = document.createElement("strong");
    number.textContent = formatCount(stage.value);
    const detail = document.createElement("small");
    detail.textContent = index === 0 ? stage.note : `${formatPct(rate)} · ${stage.note}`;
    item.append(step, label, number, detail);
    funnelChart.appendChild(item);
  });

  const matrixTarget = document.getElementById("value-matrix");
  const matrixRows = data.downstream.channel.filter(
    (row) => row.mqls >= 150 || !row.actionable,
  );
  const width = 720;
  const height = 410;
  const margin = { top: 20, right: 34, bottom: 58, left: 68 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const xMax = 30;
  const yMax = 140;
  const xPosition = (value) => margin.left + value / xMax * plotWidth;
  const yPosition = (value) => margin.top + plotHeight - value / yMax * plotHeight;
  const svg = svgElement("svg", {
    viewBox: `0 0 ${width} ${height}`,
    role: "img",
    "aria-labelledby": "matrix-title matrix-desc",
  });
  const title = svgElement("title", { id: "matrix-title" });
  title.textContent = "渠道成交率与 90 天可观测 GMV 每 MQL 的气泡图";
  const description = svgElement("desc", { id: "matrix-desc" });
  description.textContent = "横轴为成交率，纵轴为商品 GMV 每 MQL，气泡大小表示 MQL 数，橙色表示未知或缺失来源。";
  svg.append(title, description);

  for (const tick of [0, 10, 20, 30]) {
    const x = xPosition(tick);
    svg.appendChild(svgElement("line", { x1: x, y1: margin.top, x2: x, y2: margin.top + plotHeight, class: "matrix-grid" }));
    const text = svgElement("text", { x, y: height - 30, class: "matrix-tick", "text-anchor": "middle" });
    text.textContent = `${tick}%`;
    svg.appendChild(text);
  }
  for (const tick of [0, 35, 70, 105, 140]) {
    const y = yPosition(tick);
    svg.appendChild(svgElement("line", { x1: margin.left, y1: y, x2: width - margin.right, y2: y, class: "matrix-grid" }));
    const text = svgElement("text", { x: margin.left - 10, y: y + 4, class: "matrix-tick", "text-anchor": "end" });
    text.textContent = String(tick);
    svg.appendChild(text);
  }
  const xLabel = svgElement("text", { x: margin.left + plotWidth / 2, y: height - 5, class: "matrix-axis", "text-anchor": "middle" });
  xLabel.textContent = "成交率";
  const yLabel = svgElement("text", { x: 15, y: margin.top + plotHeight / 2, class: "matrix-axis", transform: `rotate(-90 15 ${margin.top + plotHeight / 2})`, "text-anchor": "middle" });
  yLabel.textContent = "90 天可观测 GMV / MQL（R$）";
  svg.append(xLabel, yLabel);

  const labelOffsets = {
    paid_search: [12, -10],
    organic_search: [12, 18],
    direct_traffic: [10, -9],
    referral: [-10, -12],
    social: [10, -8],
    email: [-10, 20],
    unknown: [-12, -14],
    "(missing)": [-10, -10],
  };
  const maxMql = Math.max(...matrixRows.map((row) => row.mqls));
  for (const row of matrixRows) {
    const x = xPosition(row.conversion_pct);
    const y = yPosition(row.gmv_per_mql_90d);
    const radius = 7 + Math.sqrt(row.mqls / maxMql) * 15;
    const group = svgElement("g", {
      class: row.actionable ? "matrix-point" : "matrix-point warning",
      "data-mark": row.origin,
      role: "img",
      tabindex: "0",
      "aria-label": `${labelFor(row.origin)}，${row.mqls} 条 MQL，成交率 ${formatPct(row.conversion_pct)}，GMV 每 MQL ${formatMoney(row.gmv_per_mql_90d)}`,
    });
    group.appendChild(svgElement("circle", { cx: x, cy: y, r: radius }));
    const [dx, dy] = labelOffsets[row.origin] || [10, -10];
    const label = svgElement("text", {
      x: x + dx,
      y: y + dy,
      class: "matrix-label",
      "text-anchor": dx < 0 ? "end" : "start",
    });
    label.textContent = labelFor(row.origin);
    group.appendChild(label);
    svg.appendChild(group);
  }
  matrixTarget.appendChild(svg);

  const gmvChart = document.getElementById("gmv-chart");
  const gmvRows = data.downstream.channel
    .filter((row) => row.actionable && row.mqls >= 150)
    .sort((a, b) => b.gmv_per_mql_90d - a.gmv_per_mql_90d);
  const maxGmv = Math.max(...gmvRows.map((row) => row.gmv_per_mql_90d));
  for (const row of gmvRows) {
    const item = document.createElement("div");
    item.className = "gmv-row";
    item.setAttribute("role", "listitem");
    item.setAttribute("data-mark", row.origin);
    item.setAttribute(
      "aria-label",
      `${labelFor(row.origin)}，GMV 每 MQL ${formatMoney(row.gmv_per_mql_90d)}，成交商家可观测率 ${formatPct(row.observed_pct_of_wins)}`,
    );
    const label = document.createElement("span");
    label.className = "gmv-name";
    label.textContent = labelFor(row.origin);
    const track = document.createElement("div");
    track.className = "gmv-track";
    track.setAttribute("aria-hidden", "true");
    const bar = document.createElement("div");
    bar.className = "gmv-bar";
    bar.style.width = `${row.gmv_per_mql_90d / maxGmv * 100}%`;
    track.appendChild(bar);
    const number = document.createElement("span");
    number.className = "gmv-value";
    number.textContent = formatMoney(row.gmv_per_mql_90d);
    const detail = document.createElement("small");
    detail.textContent = `可观测 ${row.observed_sellers}/${row.wins} 个成交商家`;
    number.appendChild(detail);
    item.append(label, track, number);
    gmvChart.appendChild(item);
  }

  const channelTable = document.getElementById("channel-table");
  for (const row of data.focus.channel) {
    const tr = document.createElement("tr");
    const classification = row.origin === "unknown" || row.origin === "(missing)"
      ? "未归因，暂不作投放依据"
      : row.leads < 150 ? "样本较少" : "可比较";
    const values = [
      labelFor(row.origin),
      formatCount(row.leads),
      formatCount(row.wins),
      formatPct(row.conversion_pct),
      classification,
    ];
    values.forEach((value, index) => {
      const td = document.createElement("td");
      td.textContent = value;
      if (index === values.length - 1 && classification !== "可比较") td.className = "warning-tag";
      tr.appendChild(td);
    });
    channelTable.appendChild(tr);
  }

  const valueTable = document.getElementById("value-table");
  for (const row of data.downstream.channel) {
    const status = !row.actionable ? "不可执行归因" : row.low_sample ? "小样本" : "可比较";
    const tr = document.createElement("tr");
    const values = [
      labelFor(row.origin),
      formatCount(row.mqls),
      formatCount(row.observed_sellers),
      formatCount(row.activated_sellers_90d),
      formatPct(row.activation_pct_of_mql),
      formatMoney(row.gmv_90d),
      formatMoney(row.gmv_per_mql_90d),
      status,
    ];
    values.forEach((value, index) => {
      const td = document.createElement("td");
      td.textContent = value;
      if (index === values.length - 1 && status !== "可比较") td.className = "warning-tag";
      tr.appendChild(td);
    });
    valueTable.appendChild(tr);
  }
})();
