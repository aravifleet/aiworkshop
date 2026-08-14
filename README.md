# prototype2

This workspace contains an Agentic-QA framework for developer instruction-driven browser automation.

It reads `.md`, `.txt`, `.pdf`, `.docx`, and `.csv` scenario documents, extracts the target URL plus supported metadata, drafts use cases for developer approval, captures fresh DOM inventories, runs Playwright automation, stores screenshots for every executed use case, and writes reports under the workspace output folders.

LLM-backed use case refinement now supports both Gemini and Groq. If a Gemini key is present, Gemini is used by default. You can override the provider with `AGENTIC_QA_LLM_PROVIDER=gemini` or `AGENTIC_QA_LLM_PROVIDER=groq`.

## What Changed

- If a scenario document explicitly asks for a number of use cases such as `draft 50 use cases`, the generated output now respects that total instead of stopping at only three seed cases.
- Happy path, negative, and edge coverage remain part of the generated set, and the rest of the requested total is filled with additional exploratory cases.
- The runner now discovers the available site pages and stores a site-understanding summary before asking for approval, so the approval step happens with real DOM knowledge instead of only document guesses.
- Authentication coverage is sharper now. When login behavior is detected, the generated high-level cases explicitly include positive login, positive login plus logout, invalid credentials, and missing-data validation.
- Every new run starts clean. Old `/usecases`, `/results`, `/reports`, `/screenshots`, `/failusecases`, `/dom/dom_elements`, `/playwright-script`, and generated `/playwrightfolder` assets are removed before fresh outputs are written.
- Every executed use case now writes a screenshot into `/screenshots`. Failed runs are also copied into `/failusecases`.
- Test result outputs now show a clear `PASS` or `FAIL` label in `.csv`, `.txt`, `.md`, `.json`, and HTML reports.
- Document parsing has been tightened to ignore more section headers and non-actionable lines so the runner follows the scenario more literally, reads `.docx` table content too, and avoids inventing steps from formatting noise.

## CLI Usage

1. Install the package locally:

```powershell
cd C:\Users\Fleet Studio-75\OneDrive\Desktop\prototype2
python -m pip install -e .
python -m playwright install
```

Optional LLM provider environment variables:

```powershell
$env:GEMINI_API_KEY="your-gemini-key"
$env:AGENTIC_QA_LLM_PROVIDER="gemini"
```

Or, for Groq:

```powershell
$env:GROQ_API_KEY="your-groq-key"
$env:AGENTIC_QA_LLM_PROVIDER="groq"
```

2. Add a scenario file under `/docsnew`, or run with direct input:

```powershell
python -m main.cli --scenario "https://example.com/login\nUsername: user\nPassword: pass\nDraft 50 use cases based on this scenario.\nVerify login works."
```

3. Run the framework:

```powershell
agentic-qa
```

Or:

```powershell
python -m main.cli --file docsnew\example.md
```

To teach the framework from your own manual exploration first:

```powershell
python -m main.cli --file docsnew\example.md --teach
```

This opens a visible browser, lets you manually click/type/select through the site, captures DOM blueprints for the pages you visit, and saves both the learned interaction patterns and taught page inventory into `configuration/action_memory.json`. A snapshot copy of the taught page inventory is also written to `dom/dom_elements/teach_dom_inventory.json`.

4. Review the generated use cases written under `/usecases`, then approve in the terminal with `Y` to continue.

## Scenario Authoring Notes

- Put the target URL in the document.
- If you want an exact total, say it explicitly, for example `Draft 50 use cases based on the scenario`.
- Supported metadata lines include `Username:`, `Password:`, and `Email:`.
- CSV requirement sheets are supported too. Header-based CSVs such as `URL, Email, Password, Instructions` are converted into the same instruction format internally.
- Keep instructions literal and specific. The parser follows actionable lines and ignores headings, notes, and section labels when possible.
- If the target flow requires login and the document does not include credentials, the run now stops early and asks you to add them to the document before rerunning.

## Fresh-Run Behavior

- Every run clears old generated use cases, test results, reports, screenshots, failure screenshots, DOM snapshots, and generated Playwright assets.
- The framework always writes a fresh output set for the current run so old artifacts do not accumulate in the workspace.

## Outputs

- `/usecases` stores the current run's `.json`, `.csv`, `.md`, and `.txt` use case files.
- `/usecases` also stores `*_site_understanding.json|md|txt` with the discovered page map, auth hints, and coverage suggestions for the current run.
- `/dom/dom_elements` stores fresh DOM snapshots and `dom_inventory.json` for the current run.
- `/results` stores `results.csv`, `results.txt`, `results.md`, and `results.json` with explicit `PASS` or `FAIL` labels.
- `/reports` stores a JSON report and an Extent-style HTML report for the current run.
- `/screenshots` stores screenshots for every executed use case.
- `/failusecases` stores copies of failed-use-case screenshots.
- `/playwright-script` stores a generated runnable script for the current run.
- `/playwrightfolder` stores the generated POM-style Playwright assets for the current run.

## VS Code Extension

The repository includes a VS Code extension under `vscode-extension/`.

Run this command in VS Code:

```text
Agentic-QA: Run automation
```

Or use:

```text
Agentic-QA: Teach from manual exploration
```

Then choose:

- `Upload file` for `.md`, `.txt`, `.pdf`, or `.docx`
- `Paste scenario` to save and run `docsnew/pasted_scenario.md`

The teach command opens a visible browser session, records your manual exploration patterns, and stores them in `configuration/action_memory.json` so later automation can reuse them. The extension launches the shared Python runner in a terminal and asks for approval there before execution continues. Installation details for fresh VS Code users on Windows, macOS, and Linux are in [vscode-extension/README.md](C:\Users\Fleet Studio-75\OneDrive\Desktop\prototype2\vscode-extension\README.md:1).
