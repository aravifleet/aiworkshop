import os
import sys
from pathlib import Path


def main() -> None:
    workspace_root = Path.cwd()
    extension_root = Path(__file__).resolve().parent
    bundle_root = extension_root / "python-src"

    if not (bundle_root / "main" / "agentic_qa.py").exists():
        raise RuntimeError(
            "Bundled Agentic-QA sources are missing from this extension package. "
            "Rebuild the VSIX after running the packaging step."
        )

    for path in [bundle_root, workspace_root]:
        if not path.exists():
            continue
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)

    os.environ.setdefault("AGENTIC_QA_WORKSPACE_ROOT", str(workspace_root.resolve()))

    try:
        from main.agentic_qa import main_sync
    except ModuleNotFoundError as exc:
        interpreter_name = Path(sys.executable).name or "python"
        print(f"Missing Python dependency: {exc.name}")
        print("Install the required packages with:")
        print(f"{interpreter_name} -m pip install groq playwright PyPDF2 python-docx")
        print(f"{interpreter_name} -m playwright install")
        return

    try:
        main_sync()
    except RuntimeError as exc:
        message = str(exc)
        if "requires PyPDF2" in message or "requires python-docx" in message:
            interpreter_name = Path(sys.executable).name or "python"
            print(message)
            print("Install the required packages with:")
            print(f"{interpreter_name} -m pip install groq playwright PyPDF2 python-docx")
            print(f"{interpreter_name} -m playwright install")
            return
        raise


if __name__ == "__main__":
    main()
