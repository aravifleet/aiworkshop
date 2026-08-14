# Agentic-QA VS Code Extension

This VSIX bundles the Agentic-QA extension code and Python source files, but it does not bundle Python itself or third-party Python libraries.

Agentic-QA supports both Gemini and Groq for LLM-assisted use case refinement. If a Gemini key is available, Gemini is used by default. Set `AGENTIC_QA_LLM_PROVIDER=groq` if you want to force the Groq path.

## What Users Need

Before running the command on a new machine, users need:

- Python 3.9 or newer
- Python packages:
  - `playwright`
  - `PyPDF2`
  - `python-docx`
  - `groq` only if you want to use the Groq provider
- Playwright browser install

### Windows

```powershell
python -m pip install playwright PyPDF2 python-docx groq
python -m playwright install
```

### macOS or Linux

```bash
python3 -m pip install playwright PyPDF2 python-docx groq
python3 -m playwright install
```

If Python is missing or the packages are not installed, the extension now prints these commands directly in the terminal it opens.

## Packaging

From the repository root:

```powershell
npm run vsix:package
```

That command packages the lighter VSIX without embedding a full Python runtime.

## Configuration

- `agenticQA.pythonPath` is optional.
- Leave it empty to use:
  - `python` on Windows
  - `python3` on macOS or Linux
- Set it when the user has Python in a custom location or virtual environment.

## Usage

1. Install the `.vsix` in VS Code.
2. Open the target workspace.
3. Run `Agentic-QA: Run automation` for the normal generate-and-execute flow, or `Agentic-QA: Teach from manual exploration` to record your own browser exploration first.
4. Choose `Upload file` or `Paste scenario`.
   Upload supports `.md`, `.txt`, `.pdf`, `.docx`, and `.csv`.
5. In teach mode, manually explore in the opened browser and then press Enter in the terminal to save learned patterns and taught page DOM blueprints to `configuration/action_memory.json`.
6. Watch the terminal for status and any install guidance.

If a target flow is login-gated and the instruction document does not include credentials, the runner will stop and ask you to add `Username:` or `Email:` plus `Password:` to the document before rerunning.
