import json
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent
LATEST_DOM_TXT = WORKSPACE_ROOT / "latest_dom.txt"
LATEST_DOM_PY = WORKSPACE_ROOT / "latest_dom.py"
DOM_HISTORY_DIR = WORKSPACE_ROOT / "dom_elements"
DOM_HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def _format_dom_py(dom_content: str) -> str:
    return "# Latest DOM snapshot captured by agentic QA\n" + "LATEST_DOM = " + json.dumps(dom_content, ensure_ascii=False, indent=2) + "\n"


def save_dom_snapshot(name: str, dom_content: str) -> None:
    LATEST_DOM_TXT.write_text(dom_content, encoding="utf-8")
    LATEST_DOM_PY.write_text(_format_dom_py(dom_content), encoding="utf-8")
    history_file = DOM_HISTORY_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{name}.html"
    history_file.write_text(dom_content, encoding="utf-8")
