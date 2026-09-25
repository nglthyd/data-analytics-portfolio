# Olist Full-Funnel Portfolio Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the portfolio into a reproducible MQL-to-90-day-GMV analysis, publish the verified site, then synchronize the one-page resume, interview guide, and job-fair preparation plan.

**Architecture:** Raw Olist CSV files stay outside Git. `analysis.py` produces one metrics object consumed by the static site; `queries.sql` and `verify.py` independently recompute critical aggregates in SQLite. Synthetic unit tests lock down attribution, time-window, granularity, and zero-preservation behavior before production implementation.

**Tech Stack:** Python 3.12, pandas, SQLite, unittest, vanilla HTML/CSS/JavaScript/SVG, Playwright, ReportLab/pypdf, python-docx.

---

## File map

- Modify `E:\projects\data-analytics-portfolio\analysis.py`: source validation, lead-level 90-day value model, exported metrics.
- Modify `E:\projects\data-analytics-portfolio\queries.sql`: independent full-funnel SQL checks.
- Modify `E:\projects\data-analytics-portfolio\verify.py`: SQL/Python comparisons and audit assertions.
- Create `E:\projects\data-analytics-portfolio\test_analysis.py`: synthetic behavior and edge-case tests.
- Create `E:\projects\data-analytics-portfolio\requirements.txt`: minimum reproducible dependencies.
- Modify `E:\projects\data-analytics-portfolio\data\metrics.js`: generated site data.
- Modify `E:\projects\data-analytics-portfolio\index.html`, `app.js`, `styles.css`: charts, narrative, references, responsive behavior.
- Modify `E:\projects\data-analytics-portfolio\verify_page.py`: chart and content smoke tests.
- Create `E:\projects\data-analytics-portfolio\docs\data_dictionary.md`, `methodology.md`, `validation_report.md`, `references.md`.
- Modify `E:\projects\data-analytics-portfolio\README.md`: recruiter-facing overview and reproduction.
- Modify `C:\Users\25629\Documents\Codex\2026-09-20\zhe\tmp\resume_edit\rebuild_resume5.py`: verified Olist resume bullets.
- Replace `C:\Users\25629\Desktop\刘涛简历5.pdf` only after a one-page visual check.
- Modify `C:\Users\25629\Desktop\数据分析作品集_完整流程与面试重点.docx`: updated process and interview guide.
- Modify `E:\projects\job-practice-packet\job_fair_20261024_resume5_plan.md`: revised project-question rotation.

### Task 1: Acquire and inventory the official e-commerce source

**Files:**
- Create locally: `E:\data_analysis\olist-marketing\brazilian-ecommerce.zip`
- Extract locally: `E:\data_analysis\olist-marketing\ecommerce-source\*.csv`
- Modify: `E:\projects\data-analytics-portfolio\findings.md`
- Modify: `E:\projects\data-analytics-portfolio\progress.md`

- [x] **Step 1: Download from the official Kaggle dataset endpoint**

Run in PowerShell:

```powershell
Invoke-WebRequest -Uri 'https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce' -OutFile 'E:\data_analysis\olist-marketing\brazilian-ecommerce.zip'
```

Expected: a non-empty ZIP; do not continue if the response is HTML or an error page.

- [x] **Step 2: Inspect ZIP names before extraction**

Expected: nine Olist CSV files including orders, order_items, sellers, customers, products, payments, reviews, geolocation, and category translation.

- [x] **Step 3: Extract to the explicit data directory**

Expected: original CSVs remain outside the repository.

- [x] **Step 4: Run a shape/key/missing-value inventory**

Required checks: rows, columns, duplicate candidate keys, missing `seller_id`, timestamp min/max, order-status counts, and item-row uniqueness.

- [x] **Step 5: Record source URL, SHA256 hashes, shapes, and audit findings**

Use `apply_patch`; never write raw data or personal paths into the public README.

### Task 2: Lock behavior with failing synthetic tests

**Files:**
- Create: `E:\projects\data-analytics-portfolio\test_analysis.py`
- Modify later: `E:\projects\data-analytics-portfolio\analysis.py`

- [x] **Step 1: Write failing tests for the desired API**

Tests must import these not-yet-present functions:

```python
from analysis import build_lead_value_table, summarize_value_by_channel
```

The synthetic fixture must include: one unconverted lead, one deal with missing `seller_id`, one seller with no order, a delivered order on day 89, an order on day 90, a cancelled order, two item rows in one order, a multi-seller order, and an order before `won_date`.

Required assertions:

```python
assert lead.loc["unconverted", "gmv_90d"] == 0
assert lead.loc["day89", "gmv_90d"] > 0
assert lead.loc["day90", "gmv_90d"] == 0
assert lead.loc["pre_win", "gmv_90d"] == 0
assert summary.loc["paid_search", "mqls"] == 2
assert summary.loc["paid_search", "gmv_per_mql_90d"] == expected
```

- [x] **Step 2: Run the targeted test and verify RED**

```powershell
python -m unittest -v test_analysis.py
```

Expected: import failure for the new functions, proving the feature is absent.

- [x] **Step 3: Add tests for data-contract failures**

Duplicate `mql_id`, duplicate `order_id + order_item_id`, unmatched closed-deal MQL, and invalid dates must raise clear `ValueError` or `AssertionError` messages.

- [x] **Step 4: Run again and confirm failures are caused by missing behavior, not fixture errors**

### Task 3: Implement the lead-level 90-day value model

**Files:**
- Modify: `E:\projects\data-analytics-portfolio\analysis.py`
- Test: `E:\projects\data-analytics-portfolio\test_analysis.py`

- [x] **Step 1: Add source constants and schemas**

Required files: MQL, closed deals, sellers, orders, order items. Validate required columns before calculations.

- [x] **Step 2: Implement `build_lead_value_table` minimally**

Behavior:

```python
eligible = first_contact_date <= observation_end - pd.Timedelta(days=90)
valid_item = (
    order_status.eq("delivered")
    & order_purchase_timestamp.ge(won_date)
    & order_purchase_timestamp.ge(first_contact_date)
    & order_purchase_timestamp.lt(first_contact_date + pd.Timedelta(days=90))
)
```

Aggregate item `price` by `mql_id`; count distinct `order_id`; left join results back to every eligible MQL; fill missing order and GMV values with zero.

- [x] **Step 3: Implement `summarize_value_by_channel`**

Output columns: `origin`, `mqls`, `wins`, `mapped_sellers`, `activated_sellers_90d`, `conversion_pct`, `activation_pct`, `orders_90d`, `gmv_90d`, `orders_per_mql_90d`, `gmv_per_mql_90d`.

- [x] **Step 4: Run unit tests and verify GREEN**

Expected: all synthetic tests pass with no warnings.

- [x] **Step 5: Refactor loading, auditing, and metric construction into focused functions**

Keep existing public function `build_metrics(data_dir)` compatible; add optional `ecommerce_dir` for upgraded output.

- [x] **Step 6: Run the entire unit suite again**

### Task 4: Build independent SQLite verification

**Files:**
- Modify: `E:\projects\data-analytics-portfolio\queries.sql`
- Modify: `E:\projects\data-analytics-portfolio\verify.py`

- [x] **Step 1: Write a failing verifier expectation for new SQL blocks**

Expected blocks: existing overall/channel/monthly plus mapping audit, lead-level90d rollup, and channel 90-day value summary.

- [x] **Step 2: Run verifier and confirm it fails because new SQL is absent**

- [x] **Step 3: Add SQLite SQL using CTEs at explicit grains**

Use one CTE per grain: `eligible_mql`, `deal_map`, `valid_item_rows`, `lead_value`, `channel_value`. Count orders with `COUNT(DISTINCT order_id)` and sum only seller-specific item prices.

- [x] **Step 4: Compare every channel and overall total with Python**

Use exact equality for counts and two-decimal equality for rates/currency. Assert sum of channel MQLs equals eligible MQL count and sum of channel GMV equals lead-level GMV.

- [x] **Step 5: Run unit tests and real-data verifier**

Expected: all tests pass and verifier prints one explicit PASS line for old funnel checks and one for full-funnel checks.

### Task 5: Generate complete public documentation

**Files:**
- Create: `requirements.txt`, `docs/data_dictionary.md`, `docs/methodology.md`, `docs/validation_report.md`, `docs/references.md`
- Modify: `README.md`

- [x] **Step 1: Write documentation-link tests before documents**

The test must fail until README links to all four documents and all linked paths exist.

- [x] **Step 2: Write the data dictionary and relationship diagram**

For each table: grain, primary key, foreign key, used columns, excluded columns, and quality issues.

- [x] **Step 3: Write methodology and formulas**

Include numerator, denominator, time anchor, 90-day boundary, valid-order rule, zero preservation, mapping coverage, and why GMV is not ROI/LTV.

- [x] **Step 4: Generate the validation report from fresh real-data output**

Do not hand-copy unverifiable numbers. Include command, timestamp, hashes, PASS checks, audit counts, and remaining anomalies.

- [x] **Step 5: Write references and attribution**

Official Olist sources first; high-engagement public analyses only as labeled design references. State AI collaboration and Apache/CC license boundaries accurately.

- [x] **Step 6: Rewrite README for recruiters**

Order: business problem → headline findings → charts/site → data flow → reproducibility → validation → limitations → attribution.

- [x] **Step 7: Run documentation tests and link checks**

### Task 6: Add four meaningful charts to the site

**Files:**
- Modify: `data/metrics.js`, `index.html`, `app.js`, `styles.css`
- Test: `verify_page.py`

- [x] **Step 1: Write failing browser assertions**

Required IDs: `channel-chart`, `funnel-chart`, `value-matrix`, `gmv-chart`. Assert non-empty generated marks, accessible labels, correct table rows, zero console errors, and no horizontal overflow at 1440×900 and 390×844.

- [x] **Step 2: Run browser test and verify RED**

Expected: missing new chart selectors.

- [x] **Step 3: Extend `metrics.js` from verified real-data output**

No manually invented numbers. Include audit coverage, funnel stages, channel value metrics, and annotation thresholds.

- [x] **Step 4: Add semantic HTML and table fallbacks**

Each chart gets a question title, one-sentence interpretation, sample size, metric definition, and limitations link.

- [x] **Step 5: Render native SVG/CSS charts**

Build: enhanced conversion bars, full-funnel steps, conversion×GMV bubble plot, and 90-day GMV/MQL bars. Use one signal color plus one warning color; flag unknown/missing/low sample channels.

- [x] **Step 6: Add responsive and accessible styles**

Keyboard focus, reduced motion, SVG title/description, readable mobile labels, and no CDN dependencies.

- [x] **Step 7: Run browser tests, inspect fresh desktop/mobile screenshots, and fix visual defects**

### Task 7: Publish only the verified repository state

**Files:**
- Public repository: `https://github.com/nglthyd/data-analytics-portfolio`

- [ ] **Step 1: Audit the upload set**

Exclude original CSVs, internal `task_plan.md`/`findings.md`/`progress.md`, local paths, credentials, and unapproved personal data.

- [ ] **Step 2: Re-run unit, SQL, documentation, and browser verification**

Stop on any failure.

- [ ] **Step 3: Update the existing public repository without rewriting history**

Use the authenticated GitHub UI if local Git remains unavailable. Do not force-push.

- [ ] **Step 4: Verify anonymously**

Repository, README, scripts, docs, metrics, CSS/JS, images, and Pages URL must return successfully. Confirm displayed metrics match local output.

### Task 8: Synchronize the one-page resume

**Files:**
- Modify: `C:\Users\25629\Documents\Codex\2026-09-20\zhe\tmp\resume_edit\rebuild_resume5.py`
- Replace after validation: `C:\Users\25629\Desktop\刘涛简历5.pdf`

- [ ] **Step 1: Draft only verified Olist wording**

Replace the old “no downstream value” line with concise full-funnel method/result/boundary language. Do not include the URL per user instruction.

- [ ] **Step 2: Generate to a temporary PDF**

Never overwrite the desktop PDF until the temporary output passes checks.

- [ ] **Step 3: Verify one page and required text**

Use pypdf for page count/text and render the page for visual inspection. Confirm photo size/location, no overlap, no clipping, and adequate bottom margin.

- [ ] **Step 4: Replace the desktop PDF and re-open/verify final file**

### Task 9: Rewrite the portfolio understanding guide

**Files:**
- Modify: `C:\Users\25629\Desktop\数据分析作品集_完整流程与面试重点.docx`

- [ ] **Step 1: Preserve a backup and inspect existing styles/page count**

- [ ] **Step 2: Rewrite around the upgraded end-to-end flow**

Must include: five-table model, 90-day anchor, denominator logic, JOIN-grain traps, Python/SQL verification, four charts, findings, limitations, AI boundary, 60-second explanation, and interviewer follow-ups. Emphasize must-understand content; mark implementation details as optional.

- [ ] **Step 3: Render and inspect every page**

No clipping, orphan headings, broken tables, or unreadably dense paragraphs.

### Task 10: Update the job-fair preparation plan

**Files:**
- Modify: `E:\projects\job-practice-packet\job_fair_20261024_resume5_plan.md`
- Modify: `E:\projects\job-practice-packet\progress.md`

- [ ] **Step 1: Replace old Olist questions with upgraded ones**

Cover first-contact 90-day window, seller/order joins, per-MQL denominator, GMV versus ROI/LTV, mapping coverage, right censoring, and multi-seller order grain.

- [ ] **Step 2: Preserve SQL51 next and the existing no-reminder preference**

- [ ] **Step 3: Add a staged mastery checkpoint**

Level 1: 60-second overview; Level 2: draw five-table model; Level 3: explain one metric and one edge case; Level 4: answer an unfamiliar business extension.

### Task 11: Final adversarial verification and knowledge sync

**Files:**
- Modify: project `progress.md` and `findings.md`
- Update personal knowledge base only with verified final paths/status.

- [ ] **Step 1: Run all fresh gates**

Commands must prove: tests green, SQL/Python parity, docs links valid, page smoke tests green, public URLs accessible, resume one page, DOCX rendered without layout defects.

- [ ] **Step 2: Attack three failure modes**

Check: JOIN multiplication inflates GMV; incomplete 90-day observations treated as zero; resume/README/site quote stale or inconsistent numbers.

- [ ] **Step 3: Back up, update, render, and verify the personal knowledge base**

- [ ] **Step 4: Report exact deliverables, verified commands, unresolved limitations, and public URLs**
