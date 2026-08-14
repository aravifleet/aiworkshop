import os
import shutil
import sys
import json
from pathlib import Path


EXTENSION_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_SOURCE_ROOT = EXTENSION_ROOT / ".bundle-source"
RUNTIME_SOURCE_ROOT = BUNDLE_SOURCE_ROOT / "runtime"

PYTHON_PREFIX = Path(sys.base_prefix or sys.prefix).resolve()
LOCAL_APPDATA = Path(os.environ.get("LOCALAPPDATA", ""))
DEFAULT_PLAYWRIGHT_BROWSERS = LOCAL_APPDATA / "ms-playwright"
DEFAULT_BROWSER_TARGETS = ("chromium",)

TOP_LEVEL_EXCLUDES = {
    "__pycache__",
    "Doc",
    "docs",
    "ensurepip",
    "idlelib",
    "Lib\\test",
    "Lib\\tkinter",
    "Scripts",
    "Tools",
}

FILE_SUFFIX_EXCLUDES = {".pyc", ".pyo"}


def should_skip(relative_path: Path) -> bool:
    parts = relative_path.parts
    if any(part == "__pycache__" for part in parts):
        return True
    if relative_path.suffix.lower() in FILE_SUFFIX_EXCLUDES:
        return True
    normalized = str(relative_path).replace("/", "\\")
    for excluded in TOP_LEVEL_EXCLUDES:
        if normalized == excluded or normalized.startswith(f"{excluded}\\"):
            return True
    return False


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_python_runtime() -> None:
    if not PYTHON_PREFIX.exists():
        raise RuntimeError(f"Python installation was not found: {PYTHON_PREFIX}")

    for source_path in PYTHON_PREFIX.rglob("*"):
        relative_path = source_path.relative_to(PYTHON_PREFIX)
        if should_skip(relative_path):
            continue

        target_path = RUNTIME_SOURCE_ROOT / relative_path
        if source_path.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)


def verify_required_modules() -> None:
    required_modules = ("playwright", "PyPDF2", "docx")
    missing = []
    for module_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(module_name)

    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(
            f"Missing required Python packages in the build environment: {joined}. "
            "Install them on the packaging machine before building the VSIX."
        )


def copy_playwright_browsers() -> None:
    configured = os.environ.get("AGENTIC_QA_PLAYWRIGHT_BROWSERS_DIR", "").strip()
    source_root = Path(configured).expanduser() if configured else DEFAULT_PLAYWRIGHT_BROWSERS

    if not source_root.exists():
        raise RuntimeError(
            f"Playwright browser cache was not found at {source_root}. "
            "Run 'python -m playwright install' on the packaging machine before building the VSIX."
        )

    targets = os.environ.get("AGENTIC_QA_BUNDLED_BROWSERS", "").strip()
    requested = {item.strip().lower() for item in targets.split(",") if item.strip()} or set(DEFAULT_BROWSER_TARGETS)

    browsers_json_path = PYTHON_PREFIX / "Lib" / "site-packages" / "playwright" / "driver" / "package" / "browsers.json"
    if not browsers_json_path.exists():
        raise RuntimeError(f"Playwright browser manifest was not found: {browsers_json_path}")

    manifest = json.loads(browsers_json_path.read_text(encoding="utf-8"))
    selected_dirs = set()

    for browser in manifest.get("browsers", []):
        name = str(browser.get("name", "")).lower()
        revision = str(browser.get("revision", "")).strip()
        directory_name = f"{name.replace('-', '_')}-{revision}".replace("chromium_headless_shell", "chromium_headless_shell")
        if name in {"ffmpeg", "winldd"}:
            selected_dirs.add(f"{name}-{revision}")
            continue
        if name == "chromium" and "chromium" in requested:
            selected_dirs.add(f"chromium-{revision}")
            continue
        if name == "chromium-headless-shell" and "chromium" in requested:
            selected_dirs.add(f"chromium_headless_shell-{revision}")
            continue
        if name == "firefox" and "firefox" in requested:
            selected_dirs.add(f"firefox-{revision}")
            continue
        if name == "webkit" and "webkit" in requested:
            selected_dirs.add(f"webkit-{revision}")

    target_root = RUNTIME_SOURCE_ROOT / "ms-playwright"
    target_root.mkdir(parents=True, exist_ok=True)

    for entry in source_root.iterdir():
        if entry.name in {".links", ".settings"}:
            destination = target_root / entry.name
            if entry.is_dir():
                shutil.copytree(entry, destination, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
            else:
                shutil.copy2(entry, destination)
            continue

        if entry.name not in selected_dirs:
            continue

        destination = target_root / entry.name
        if entry.is_dir():
            shutil.copytree(entry, destination, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
        else:
            shutil.copy2(entry, destination)


def write_manifest() -> None:
    configured = os.environ.get("AGENTIC_QA_PLAYWRIGHT_BROWSERS_DIR", "").strip()
    browsers_root = Path(configured).expanduser() if configured else DEFAULT_PLAYWRIGHT_BROWSERS
    manifest_path = BUNDLE_SOURCE_ROOT / "runtime-manifest.txt"
    manifest_path.write_text(
        "\n".join(
            [
                f"python_executable={sys.executable}",
                f"python_prefix={PYTHON_PREFIX}",
                f"playwright_browsers={browsers_root}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    print(f"[agentic-qa] Building portable runtime from {PYTHON_PREFIX}")
    verify_required_modules()
    reset_dir(BUNDLE_SOURCE_ROOT)
    RUNTIME_SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    copy_python_runtime()
    copy_playwright_browsers()
    write_manifest()
    print(f"[agentic-qa] Portable runtime prepared at {RUNTIME_SOURCE_ROOT}")


if __name__ == "__main__":
    main()
