import sys
from pathlib import Path


def main() -> None:
    workspace_root = Path.cwd()
    if str(workspace_root) not in sys.path:
        sys.path.insert(0, str(workspace_root))

    from main.agentic_qa import main_sync

    main_sync()


if __name__ == "__main__":
    main()
