from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parent
PUBLIC_DOCS = (
    "docs/data_dictionary.md",
    "docs/methodology.md",
    "docs/validation_report.md",
    "docs/references.md",
)


class RepositoryDocumentationTests(unittest.TestCase):
    def test_page_declares_existing_project_relative_favicon(self) -> None:
        from html.parser import HTMLParser
        from xml.etree import ElementTree

        class Icons(HTMLParser):
            def __init__(self):
                super().__init__()
                self.hrefs = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "link" and attrs.get("rel") == "icon":
                    self.hrefs.append(attrs.get("href", ""))

        icons = Icons()
        icons.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(len(icons.hrefs), 1, "Explicit favicon avoids the missing host-root favicon.ico request")
        href = icons.hrefs[0]
        self.assertFalse(href.startswith(("/", "http:", "https:")))
        self.assertTrue((ROOT / href).is_file())
        self.assertEqual(ElementTree.parse(ROOT / href).getroot().tag, "{http://www.w3.org/2000/svg}svg")

    def test_readme_links_every_public_document(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for relative_path in PUBLIC_DOCS:
            with self.subTest(path=relative_path):
                self.assertIn(f"]({relative_path})", readme)
                self.assertTrue((ROOT / relative_path).is_file())

    def test_readme_discloses_value_and_attribution_boundaries(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for required_phrase in ("90 天", "GMV", "可观测", "不是 ROI", "AI 协作"):
            with self.subTest(phrase=required_phrase):
                self.assertIn(required_phrase, readme)


if __name__ == "__main__":
    unittest.main()
