# prototype2 Agentic-QA Framework User Manual

## Purpose

This workspace implements an Agentic-QA framework that reads developer instruction files from `/docsnew`, drafts use cases for approval, captures DOM across discovered pages, runs Playwright automation, and writes reports plus QA-ready Playwright assets.

## Folder Structure

- `/docsnew` - developer instruction `.md`, `.txt`, `.pdf`, or `.docx` files
- `/playwright-script` - generated flat Playwright runner scripts for the current run
- `/playwrightfolder` - generated POM-style Playwright assets for the current run
- `/dom/dom_elements` - DOM snapshots and `dom_inventory.json` for the current run
- `/screenshots` - screenshots for every executed use case
- `/failusecases` - copies of failed-use-case screenshots
- `/usecases` - generated use case `.json`, `.md`, `.txt`, `.csv` files for the current run
- `/results` - `results.csv`, `results.txt`, `results.md`, `results.json`
- `/reports` - JSON report and Extent-style HTML report
- `/configuration` - config such as `playwright_config.json`
- `/main` - core execution and helper code

## Prerequisites

1. Install Python 3.9 or newer.
2. Install the project and Playwright browsers:

```powershell
cd C:\Users\Fleet Studio-75\OneDrive\Desktop\prototype2
python -m pip install -e .
python -m playwright install
```

## How To Run

1. Put an instruction file in `/docsnew` or use the VS Code paste flow.
2. Make sure the document contains the target URL.
3. Optional metadata such as `Username:`, `Password:`, and `Email:` can be included.
4. If you need a specific total, say it directly in the document, for example `Draft 50 use cases based on this scenario`.
5. Run the CLI:

```powershell
agentic-qa
```

Or:

```powershell
python -m main.cli --file docsnew\example.md
```

6. Review the generated use cases in `/usecases`.
7. Approve in the terminal with `Y`.
8. After the run completes, review:

- `/usecases`
- `/results`
- `/reports`
- `/screenshots`
- `/failusecases`
- `/playwright-script`
- `/playwrightfolder`
- `/dom/dom_elements`

## Clean Output Behavior

- Every new run removes old generated use cases, test results, reports, screenshots, failure screenshots, DOM snapshots, and generated Playwright assets before writing fresh files.
- The workspace keeps only the current run's generated outputs, which prevents old artifacts from piling up between runs.

## How It Works

1. The runner reads a selected `.md`, `.txt`, `.pdf`, or `.docx` instruction file.
2. It extracts the target URL, metadata, and actionable instruction lines.
3. It writes generated use cases and asks for approval.
4. After approval, it captures fresh DOM snapshots and discovers same-site pages.
5. It expands the final use case set, respecting an explicit requested count when the document provides one.
6. It runs the use cases with Playwright.
7. It writes results, screenshots, and reports with clear `PASS` or `FAIL` labels.

## Expected Output

- `results/results.csv`
- `results/results.txt`
- `results/results.md`
- `results/results.json`
- `reports/report_YYYYMMDD_HHMMSS.json`
- `reports/extent_report_YYYYMMDD_HHMMSS.html`
- `playwright-script/*.py`
- `playwrightfolder/pages/*.py`
- `playwrightfolder/tests/*.py`
- `playwrightfolder/data/*.json`
- `dom/dom_elements/*.html`
- `dom/dom_elements/dom_inventory.json`
- `screenshots/*.png`
- `failusecases/*.png`

## Notes

- Explicit counts like `draft 50 use cases` are respected as the total generated count.
- Happy path, negative, and edge coverage remain part of the generated output.
- Screenshots are captured for every executed use case.
- Parsing is intentionally conservative so headings and formatting noise are less likely to turn into invented steps.
