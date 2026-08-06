# prototype2 Agentic QA Framework User Manual

## Purpose

This workspace implements an agentic QA framework that reads developer instruction files from `/docsnew`, generates use cases, runs Playwright automation, captures DOM snapshots, and outputs results and reports.

## Folder structure

- `/docsnew` - place developer instruction `.md` or `.txt` files here.
- `/playwright-script` - generated Playwright script files in POM style.
- `/dom/dom_elements` - captured DOM snapshots for every major page.
- `/screenshots` - passed scenario screenshots.
- `/failusecases` - failed scenario screenshots.
- `/usecases` - generated use case `.md`, `.txt`, `.csv` files.
- `/results` - output summary files: `results.csv`, `results.txt`, `results.md`.
- `/reports` - JSON report files for each run.
- `/configuration` - config files such as `playwright_config.json`.
- `/main` - core execution and helper code.

## Prerequisites

1. Install Python 3.14 or newer.
2. Install Playwright and browser dependencies:
   ```powershell
   python -m pip install playwright
   python -m playwright install
   ```
3. (Optional) Install any other dependencies if added later.

## How to run

1. Put your instruction file in `/docsnew`.
   - The first line should contain the target URL or a URL should appear anywhere in the text.
   - Example:
     ```md
     https://practicetestautomation.com/practice-test-login/
     Username: student
     Password: Password123
     Verify login works and the form responds.
     ```
2. Run the main script:
   ```powershell
   cd "c:\Users\Fleet Studio-75\OneDrive\Desktop\prototype2"
   python .\main\agentic_qa.py
   ```
3. After the run completes, check:
   - `/usecases` for generated use case files
   - `/results/results.csv`, `/results/results.txt`, `/results/results.md`
   - `/reports` for the JSON run report
   - `/screenshots` for pass screenshots
   - `/failusecases` for failure screenshots
   - `/playwright-script` for the generated runnable Playwright script

## How it works

1. The script reads the first `.md` or `.txt` file from `/docsnew`.
2. It extracts the target URL and any provided metadata like `Username` and `Password`.
3. It generates three use case categories: happy path, negative path, and edge case.
4. It writes use cases to `/usecases` and also writes a generated Playwright script to `/playwright-script`.
5. It runs the use cases in Playwright.
6. It writes results to `/results` and `/reports`, captures DOM snapshots to `/dom/dom_elements`, and stores screenshots.

## Expected output

- `results/results.csv` — scenario summary table
- `results/results.txt` — simple text summary
- `results/results.md` — markdown summary
- `reports/report_YYYYMMDD_HHMMSS.json` — generated JSON report
- `playwright-script/*.py` — generated runnable script for the same scenario
- `dom/dom_elements/*.html` — DOM snapshots
- `screenshots/*.png` — pass screenshots
- `failusecases/*.png` — failure screenshots

## Troubleshooting

- If no file is found in `/docsnew`, add one and rerun.
- If the URL is missing, ensure the document contains a valid `https://...` link.
- If Playwright cannot launch, verify the browsers are installed with `python -m playwright install`.
- If a scenario fails, inspect `/failusecases/` and the JSON report in `/reports`.

## Notes

- The framework generates test actions from text based on phrases like `fill`, `click`, `verify`, and `capture DOM`.
- It is intentionally lightweight for developer self-testing and can be extended later with coverage feedback, PR gating, and richer script generation.
