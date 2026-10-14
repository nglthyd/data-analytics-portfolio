import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const root = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:([A-Za-z]:))/, "$1"));
const nodeModules = process.env.CODEX_NODE_MODULES;
const edgePath = process.env.EDGE_PATH || "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const require = createRequire(import.meta.url);
const { chromium } = nodeModules
  ? require(path.join(nodeModules, "playwright"))
  : require("playwright");

function check(condition, message) {
  if (!condition) throw new Error(message);
}

const ops = JSON.parse(fs.readFileSync(path.join(root, "data", "merchant_ops.json"), "utf8"));
const screenshotDir = path.join(root, "qa", "screenshots");
fs.mkdirSync(screenshotDir, { recursive: true });
const browser = await chromium.launch({
  headless: true,
  executablePath: edgePath,
  args: ["--allow-file-access-from-files"],
});
const errors = [];

async function inspect(viewport, name) {
  const page = await browser.newPage({ viewport });
  page.on("pageerror", error => errors.push(`${name}: ${error.message}`));
  page.on("console", message => {
    if (message.type() === "error") errors.push(`${name}: console ${message.text()}`);
  });
  await page.goto(pathToFileURL(path.join(root, "index.html")).href, { waitUntil: "load" });
  await page.waitForFunction(() => document.querySelector("#ops-eligible")?.textContent !== "—");

  const visible = await page.locator("#merchant-ops").isVisible();
  check(visible, `${name}: merchant section is not visible`);
  check((await page.locator("#ops-eligible").textContent()).trim() === String(ops.summary.eligible_closed), `${name}: eligible metric differs`);
  check((await page.locator("#ops-no-activation").textContent()).trim() === String(ops.summary.observable_no_activation), `${name}: no-activation metric differs`);
  check((await page.locator("#ops-anomalies").textContent()).trim() === String(ops.summary.chronology_error_closed), `${name}: anomaly metric differs`);
  check((await page.locator("#ops-activation").textContent()).trim() === `${Number(ops.summary.activation_pct_of_eligible).toFixed(2)}%`, `${name}: activation rate differs`);
  check((await page.locator("#all-leads").textContent()).trim() !== "—", `${name}: legacy metrics did not render`);
  check(await page.locator("#channel-chart .channel-row").count() > 0, `${name}: legacy channel chart did not render`);
  check(await page.locator("#ops-cohort-table tr").count() === ops.cohorts.length, `${name}: cohort row count differs`);
  check(!(await page.locator("#merchant-ops").textContent()).includes("等待分析数据"), `${name}: placeholder remains`);

  const images = page.locator("#merchant-ops img");
  check(await images.count() === 5, `${name}: expected five evidence charts`);
  await images.evaluateAll(nodes => nodes.forEach(img => { img.loading = "eager"; }));
  for (let index = 0; index < 5; index += 1) {
    await images.nth(index).scrollIntoViewIfNeeded();
    await page.waitForFunction(img => img.complete, await images.nth(index).elementHandle());
    check(await images.nth(index).evaluate(img => img.complete && img.naturalWidth > 0), `${name}: chart ${index + 1} failed to load`);
  }
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  check(overflow <= 1, `${name}: horizontal overflow ${overflow}px`);
  await page.screenshot({ path: path.join(screenshotDir, `${name}.png`), fullPage: true });
  await page.locator("#merchant-ops").screenshot({ path: path.join(screenshotDir, `${name}-merchant.png`) });
  await page.close();
}

try {
  for (const file of [
    "assets/ops-states.svg", "assets/ops-cohorts.svg", "assets/ops-concentration.svg",
    "assets/ops-segments.svg", "assets/ops-coverage.svg",
  ]) {
    const svg = fs.readFileSync(path.join(root, file), "utf8");
    check(/<title(?:\s[^>]*)?>[^<]+<\/title>/.test(svg), `${file}: missing title`);
    check(/<desc(?:\s[^>]*)?>[^<]+<\/desc>/.test(svg), `${file}: missing description`);
  }
  for (const file of [
    "docs/business_report.md", "docs/operations_plan.md", "docs/understanding_guide.md",
    "docs/resume_portfolio_candidate.md", "docs/upgrade_validation.md",
  ]) {
    check(fs.existsSync(path.join(root, file)), `${file}: linked document is missing`);
  }
  await inspect({ width: 1440, height: 900 }, "desktop");
  await inspect({ width: 390, height: 844 }, "mobile");
  check(errors.length === 0, `browser errors: ${errors.join(" | ")}`);
  console.log(JSON.stringify({ status: "PAGE_QA_OK", screenshots: 4, errors: 0 }));
} finally {
  await browser.close();
}
