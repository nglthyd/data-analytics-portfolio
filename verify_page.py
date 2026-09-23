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
            assert page.locator(".channel-row").count() == 6
            page.locator(".detail-table summary").click()
            assert page.locator("#channel-table tr").count() == 11
            assert page.locator("#channel-table").get_by_text("unknown").count() == 1
            assert page.locator(".preview img").evaluate("img => img.complete && img.naturalWidth > 0")
            assert not errors, errors
            overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            assert overflow <= 1, f"horizontal overflow {overflow}px at {width}px"
            page.screenshot(path=str(SCREENSHOTS / f"{label}.png"), full_page=True)
            print(f"PASS {label}: metrics, chart, detail table, image, console, overflow")
            page.close()
        browser.close()


if __name__ == "__main__":
    run()
