import importlib
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent


class PortfolioOutputsTests(unittest.TestCase):
    def load_feature(self, name):
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError:
            self.fail(f"Missing planned feature: {name}")

    def test_bar_chart_is_accessible_parseable_svg(self):
        charts = self.load_feature("portfolio_charts")
        svg = charts.bar_chart("示例", [("未知", 2), ("已激活", 3)], "家", "分母为5家")
        root = ET.fromstring(svg)
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("分母为5家", svg)
        self.assertEqual(len(root.findall("{http://www.w3.org/2000/svg}title")), 1)
        self.assertEqual(len(root.findall("{http://www.w3.org/2000/svg}desc")), 1)

    def test_chart_empty_data_and_xml_escaping(self):
        charts = self.load_feature("portfolio_charts")
        ET.fromstring(charts.bar_chart("A & B", [], "%", "无样本"))
        ET.fromstring(charts.bar_chart("测试", [("<未知>", 0)], "家", "空值不当0"))

    def test_private_identifiers_rejected_at_export(self):
        build = self.load_feature("build_portfolio")
        for field in ("seller_id", "mql_id", "order_id", "first_contact_date"):
            with self.assertRaises(ValueError):
                build.validate_public_aggregates({"nested": [{field: "private"}]})

    def test_identifier_like_values_cannot_hide_under_public_labels(self):
        build = self.load_feature("build_portfolio")
        with self.assertRaisesRegex(ValueError, "identifier-like"):
            build.validate_public_aggregates({"label": "0123456789abcdef0123456789abcdef"})

    def test_nonfinite_public_values_rejected(self):
        build = self.load_feature("build_portfolio")
        with self.assertRaises(ValueError):
            build.validate_public_aggregates({"gmv": float("nan")})

    def test_generated_report_distinguishes_plan_from_experiment(self):
        build = self.load_feature("build_portfolio")
        ops = {"summary": {"total_closed": 5, "observable_closed": 3, "unknown_coverage_closed": 2,
                            "eligible_closed": 3, "activated": 2, "observable_no_activation": 1,
                            "orders_90d": 6, "gmv_90d": 440, "activation_pct_of_eligible": 66.67},
               "states": [], "cohorts": [], "concentration": {"top10_gmv_pct": 60, "top10_count": 1},
               "segments": [], "sensitivity": []}
        report = build.business_report(ops)
        self.assertIn("待验证假设", report)
        self.assertIn("未执行", report)
        self.assertIn("不是利润", report)
        self.assertNotIn("实际提升", report)
        self.assertNotIn("供给风险", report)

    def test_page_exposes_new_merchant_module_and_unexecuted_plan(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="merchant-ops"', html)
        self.assertIn('src="ops.js"', html)
        self.assertIn("验证方案尚未执行", html)
        for name in ("states", "cohorts", "concentration", "segments", "coverage"):
            self.assertIn(f"assets/ops-{name}.svg", html)


if __name__ == "__main__":
    unittest.main()
