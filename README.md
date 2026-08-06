# prototype2

This workspace contains an Agentic-QA framework for developer instruction-driven automation.

The framework supports `upload` and `paste` flows, reads `.md`, `.txt`, `.pdf`, and `.docx` instructions, generates reusable use cases, asks for developer approval before execution, captures fresh DOM inventories on every run, executes Playwright automation, and stores outputs under `/results`, `/reports`, `/screenshots`, `/dom/dom_elements`, `/usecases`, `/playwright-script`, and `/playwrightfolder`.

## CLI Usage

1. Install the package locally:

```powershell
cd C:\Users\Fleet Studio-75\OneDrive\Desktop\prototype2
python -m pip install -e .
python -m playwright install
```

2. Add a scenario file under `/docsnew`, or run with direct input:

```powershell
python -m main.cli --scenario "https://example.com/login\nUsername: user\nPassword: pass\nVerify login works."
```

3. Run the framework:

```powershell
agentic-qa
```

Or:

```powershell
python -m main.cli --file docsnew\example.md
```

4. Review the seed use cases written under `/usecases`, then approve in the terminal with `Y` to continue.

### Reuse Behavior

- The first run generates and stores the scenario use cases.
- Later runs of the same scenario reuse the approved use cases instead of regenerating them.
- Use `--regenerate` if you want to refresh the saved use cases.
- Use `--approve` if you want to skip the interactive approval prompt.

## Outputs

- `/usecases` stores `.json`, `.csv`, `.md`, and `.txt` use case files.
- `/dom/dom_elements` stores fresh DOM snapshots and `dom_inventory.json` on every run.
- `/results` stores `results.csv`, `results.txt`, `results.md`, and `results.json`.
- `/reports` stores a JSON report and an Extent-style HTML report.
- `/playwright-script` stores a generated runnable script.
- `/playwrightfolder` stores reusable POM assets under `pages`, `tests`, and `data`.

## VS Code Extension

The repository includes a VS Code extension under `vscode-extension/`.

Run this command in VS Code:

```text
Agentic-QA: Run automation
```

Then choose:

- `Upload file` for `.md`, `.txt`, `.pdf`, or `.docx`
- `Paste scenario` to save and run `docsnew/pasted_scenario.md`

The extension launches the shared Python runner in a terminal and asks for approval there before execution continues.
