# prototype2 Agentic-QA Framework User Manual

## Purpose

This workspace implements an Agentic-QA framework that reads developer instruction files from `/docsnew`, generates reusable use cases, asks for approval, captures DOM across discovered pages, runs Playwright automation, and writes reports plus QA-ready Playwright assets.

## Folder Structure

- `/docsnew` - developer instruction `.md`, `.txt`, `.pdf`, or `.docx` files
- `/playwright-script` - generated flat Playwright runner scripts
- `/playwrightfolder` - reusable POM-style Playwright assets for QA
- `/dom/dom_elements` - DOM snapshots and `dom_inventory.json`
- `/screenshots` - passed scenario full-page screenshots
- `/failusecases` - failed scenario screenshots
- `/usecases` - generated use case `.json`, `.md`, `.txt`, `.csv` files
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
3. Optional metadata such as `Username:` and `Password:` can be included.
4. Run the CLI:

```powershell
agentic-qa
```

Or:

```powershell
python -m main.cli --file docsnew\example.md
```

5. Review the seed use cases created in `/usecases`.
6. Approve in the terminal with `Y`.
7. After the run completes, review:

- `/usecases`
- `/results`
- `/reports`
- `/screenshots`
- `/failusecases`
- `/playwright-script`
- `/playwrightfolder`
- `/dom/dom_elements`

## How It Works

1. The runner reads a selected `.md`, `.txt`, `.pdf`, or `.docx` instruction file.
2. It extracts the target URL and metadata.
3. It writes seed use cases and asks for approval.
4. After approval, it captures fresh DOM snapshots and discovers same-site pages.
5. It expands the final use cases, stores them for reuse, and writes Playwright assets.
6. It runs the use cases with Playwright.
7. It writes results and reports.

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

- Approved use cases are reused on later runs of the same scenario unless you run with `--regenerate`.
- DOM snapshots are refreshed on every execution run.
- The framework enforces a 20-second click timeout by default through `configuration/playwright_config.json`.
