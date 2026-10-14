"""Small deterministic SVG charts, with accessible labels and explicit captions."""
from html import escape
from pathlib import Path

STATE_LABELS = {
    "unknown_coverage": "样本中不可观测",
    "incomplete_window": "观察窗不完整",
    "chronology_error": "成交日期异常",
    "observable_no_activation": "可观测但未激活",
    "activated": "窗口内已激活",
    "high_contribution": "高贡献已激活",
    "other_activated": "其他已激活",
}


def _shell(title, caption, height, body):
    lines = [caption[i:i+38] for i in range(0, len(caption), 38)] or [""]
    footer = "".join(f'<text x="28" y="{height + 27 + i*21}" class="note">{escape(line)}</text>'
                     for i, line in enumerate(lines))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {height+48+len(lines)*21}" '
            'role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(caption)}</desc>'
            '<style>text{font-family:"Microsoft YaHei",Arial,sans-serif;fill:#173046;font-size:15px}'
            '.heading{font-size:22px;font-weight:700}.note{fill:#5B6E79;font-size:13px}'
            '.grid{stroke:#DEE6E8;stroke-width:1}</style>'
            f'<rect width="760" height="100%" fill="#fff"/><text x="28" y="36" class="heading">{escape(title)}</text>'
            f'{body}{footer}</svg>')


def bar_chart(title, rows, unit, caption):
    maximum = max([float(value) for _, value in rows] + [1.0])
    body = []
    for index, (label, value) in enumerate(rows):
        y = 76 + index*48
        length = max(0, float(value))/maximum*395
        body.append(f'<text x="28" y="{y+18}">{escape(str(label))}</text>'
                    f'<rect x="225" y="{y}" width="{length:.3f}" height="26" rx="3" fill="#006D68"/>'
                    f'<text x="{232+length:.3f}" y="{y+19}">{float(value):,.2f}{escape(unit)}</text>')
    if not rows:
        body.append('<text x="28" y="90">没有符合条件的样本</text>')
    return _shell(title, caption, max(115, 83+len(rows)*48), "".join(body))


def concentration_chart(curve):
    body = []
    for tick in (0, 25, 50, 75, 100):
        x, y = 72+tick*6.1, 365-tick*2.8
        body += [f'<line class="grid" x1="{x}" y1="85" x2="{x}" y2="365"/>',
                 f'<line class="grid" x1="72" y1="{y}" x2="682" y2="{y}"/>',
                 f'<text x="{x}" y="388" text-anchor="middle">{tick}%</text>',
                 f'<text x="61" y="{y+5}" text-anchor="end">{tick}%</text>']
    points = [(0, 0)] + [(float(r["merchants_pct"]), float(r["gmv_pct"])) for r in curve]
    body.append('<polyline fill="none" stroke="#006D68" stroke-width="3" points="'+
                " ".join(f"{72+x*6.1:.2f},{365-y*2.8:.2f}" for x,y in points)+'"/>')
    body.append('<text x="72" y="65" class="note">累计商品GMV占比</text>'
                '<text x="360" y="420" text-anchor="middle">正GMV已激活商家累计占比</text>')
    return _shell("商家贡献集中度", "按90天商品GMV降序排列；只包含合格且正GMV商家，不代表平台整体或利润。", 435, "".join(body))


def generate_charts(ops, legacy_metrics, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = ops["summary"]
    total = summary["total_closed"]
    states = [(STATE_LABELS.get(r["status"], r["status"]), r["count"]) for r in ops["states"]]
    cohorts = [(r["contact_month"], r["activation_pct_of_eligible"])
               for r in ops["cohorts"] if r["activation_pct_of_eligible"] is not None]
    segments = [(STATE_LABELS.get(r.get("segment", r.get("status", "")), r.get("segment", r.get("status", ""))),
                 r.get("gmv_90d", 0) or 0) for r in ops["segments"] if r.get("gmv_90d") is not None]
    coverage = [(r["origin"], r["observed_pct_of_wins"])
                for r in legacy_metrics["downstream"]["channel"]
                if r["wins"] >= 10 and r["observed_pct_of_wins"] is not None]
    charts = {
        "ops-states.svg": bar_chart("成交商家观察状态", states, "家", f"分母为{total}个成交商家；未知覆盖不是流失。异常与不完整窗口单独标记。"),
        "ops-cohorts.svg": bar_chart("首次接触月份与90天激活", cohorts, "%", "每月分母为可观测、日期合格且拥有完整90天窗口的成交商家；样本数见明细，不做因果比较。"),
        "ops-concentration.svg": concentration_chart(ops["concentration"].get("curve", [])),
        "ops-segments.svg": bar_chart("运营分组的90天商品GMV", segments, "R$", "仅合格可观测商家计金额；高贡献采用正GMV商家q75阈值，是描述性分组，非行业标准。"),
        "ops-coverage.svg": bar_chart("渠道成交商家的可观测覆盖", coverage, "%", "固定2018年1至4月线索期；分母为渠道成交商家，至少10家成交才展示。不能当作运营流失率。"),
    }
    for filename, svg in charts.items():
        (output_dir / filename).write_text(svg, encoding="utf-8")
    return list(charts)
