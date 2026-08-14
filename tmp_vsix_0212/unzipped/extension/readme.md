# Agentic-QA VS Code Extension

This VSIX package bundles the Agentic-QA Python runner with the VS Code extension and is designed for fresh installation on Windows, macOS, and Linux.

## What The Bundle Supports

- VS Code on Windows, macOS, and Linux
- Scenario input through `Upload file` or `Paste scenario`
- Bundled Python runner shipped inside the VSIX
- The platform-default Python command:
  - `python` on Windows
  - `python3` on macOS and Linux
- A custom Python executable through the `agenticQA.pythonPath` setting when needed

## Fresh Installation

1. Install Python 3.9 or newer.
2. Install the required Python dependencies on the target machine.

### Windows

```powershell
python -m pip install playwright PyPDF2 python-docx
python -m playwright install
```

### macOS or Linux

```bash
python3 -m pip install playwright PyPDF2 python-docx
python3 -m playwright install
```

3. In VS Code, open the Extensions view.
4. Run `Extensions: Install from VSIX...`.
5. Select the `agentic-qa-*.vsix` or `agentic-qa-runner-*.vsix` bundle from the `vscode-extension/` folder.
6. Open the target workspace folder in VS Code.

## First-Time Configuration

- If VS Code cannot find Python automatically, set `agenticQA.pythonPath`.
- Recommended values:
  - Windows: `python`
  - macOS/Linux: `python3`
- If your environment uses a virtual environment or a custom executable, point the setting directly to that interpreter.

## Usage

1. Open the workspace in VS Code.
2. Run `Agentic-QA: Run automation` from the Command Palette.
3. Choose one of:
   - `Upload file` for `.md`, `.txt`, `.pdf`, or `.docx`
   - `Paste scenario` to save into `docsnew/pasted_scenario.md`
4. Watch the terminal launched by the extension.
5. Review the generated use cases under `/usecases`.
6. Approve with `Y` in the terminal to continue the browser run.

## Runtime Behavior

- Each run clears old generated use cases, results, reports, screenshots, DOM snapshots, and generated Playwright assets before writing fresh outputs.
- If the scenario document explicitly says something like `draft 50 use cases`, the runner respects that total.
- The runner now discovers site pages and stores a site-understanding summary before asking for use-case approval.
- Authentication scenarios are sharper now, with explicit positive login and login-plus-logout coverage when auth is detected.
- Every executed use case stores a screenshot under `/screenshots`.
- Reports clearly show `PASS` or `FAIL` across the generated output files.

## Packaging Notes

- This extension bundle is JavaScript plus a small Python launcher, so it is not tied to a single operating system.
- Browser execution still depends on the local Playwright browser installation completed by the user machine.
- The extension now ships its Python sources inside the VSIX, so users do not need a cloned copy of this repository just to run the command.
- Generated folders such as `usecases`, `results`, `reports`, `screenshots`, `dom`, and `playwrightfolder` are written into the currently opened VS Code workspace.
