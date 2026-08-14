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
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)

    os.environ.setdefault("AGENTIC_QA_WORKSPACE_ROOT", str(workspace_root.resolve()))

    from main.agentic_qa import main_sync

    main_sync()


if __name__ == "__main__":
    main()
