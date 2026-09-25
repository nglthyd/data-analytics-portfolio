"""Local browser smoke test for desktop and mobile layouts."""

from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).parent
URL = (ROOT / "index.html").as_uri()
SCREENSHOTS = ROOT / "screenshots"


def run() -> None:
    SCREENSHOTS.mkdir(exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for label, width, height in (("desktop", 1440, 900), ("mobile", 390, 844)):
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto(URL, wait_until="networkidle")
            assert page.title() == "刘涛｜数据分析作品集"
            assert page.locator("#all-leads").inner_text() == "8,000"
            assert page.locator("#all-wins").inner_text() == "842"
            assert page.locator("#focus-conversion").inner_text() == "13.87%"
            assert page.locator("#observable-sellers").inner_text() == "380"
            assert page.locator("#activated-sellers").inner_text() == "245"
            for chart_id in ("channel-chart", "funnel-chart", "value-matrix", "gmv-chart"):
                chart = page.locator(f"#{chart_id}")
                assert chart.count() == 1, f"missing #{chart_id}"
                assert chart.get_attribute("aria-label"), f"missing label on #{chart_id}"
                assert chart.locator("[data-mark]").count() > 0, f"no generated marks in #{chart_id}"
                if chart.locator("svg").count():
                    assert chart.locator("svg title").count() == 1
                    assert chart.locator("svg desc").count() == 1
            page.locator(".detail-table summary").first.click()
            assert page.locator("#channel-table tr").count() == 11
            assert page.locator("#value-table tr").count() == 11
            assert page.locator("#channel-table").get_by_text("未知来源").count() == 1
            assert page.locator(".preview img").evaluate("img => img.complete && img.naturalWidth > 0")
            assert not errors, errors
            overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            assert overflow <= 1, f"horizontal overflow {overflow}px at {width}px"
            page.screenshot(path=str(SCREENSHOTS / f"{label}.png"), full_page=True)
            if label == "desktop":
                for element_id in ("channel-chart", "funnel-chart", "value-matrix", "gmv-chart"):
                    page.locator(f"#{element_id}").screenshot(
                        path=str(SCREENSHOTS / f"{element_id}.png")
                    )
            print(f"PASS {label}: metrics, chart, detail table, image, console, overflow")
            page.close()
        browser.close()


if __name__ == "__main__":
    run()
