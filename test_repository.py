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
