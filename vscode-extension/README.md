# Agentic-QA VS Code Extension

This extension launches the shared Agentic-QA runner from VS Code.

## Installation

1. Install Python 3.9 or newer.
2. Make sure the workspace runner dependencies are installed:

```powershell
cd C:\Users\Fleet Studio-75\OneDrive\Desktop\prototype2
python -m pip install -e .
python -m playwright install
```

3. Install the `.vsix` package in VS Code with `Extensions: Install from VSIX...`.

## Usage

1. Open the workspace in VS Code.
2. Run `Agentic-QA: Run automation` from the Command Palette.
3. Choose one of:
- `Upload file` for `.md`, `.txt`, `.pdf`, or `.docx`
- `Paste scenario` to save into `docsnew/pasted_scenario.md`
4. Watch the terminal.
5. Review the generated use cases under `/usecases`.
6. Approve with `Y` in the terminal to continue the browser run.

## Notes

- The extension uses the same Python runner as the CLI, so upload and paste follow the same workflow.
- Re-running the same scenario reuses the approved use cases unless you regenerate them from the CLI.
