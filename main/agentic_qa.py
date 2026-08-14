import argparse
import asyncio
import csv
import hashlib
import importlib
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, urlunparse

from playwright.async_api import Error, Page, async_playwright

PyPDF2 = None
Document = None

CODE_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = Path(os.environ.get("AGENTIC_QA_WORKSPACE_ROOT", str(CODE_ROOT))).resolve()
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))
from dom import dom as dom_helper

DOCS_DIR = WORKSPACE_ROOT / "docsnew"
DOM_DIR = WORKSPACE_ROOT / "dom" / "dom_elements"
PLAYWRIGHT_DIR = WORKSPACE_ROOT / "playwright-script"
PLAYWRIGHT_POM_DIR = WORKSPACE_ROOT / "playwrightfolder"
PLAYWRIGHT_PAGES_DIR = PLAYWRIGHT_POM_DIR / "pages"
PLAYWRIGHT_TESTS_DIR = PLAYWRIGHT_POM_DIR / "tests"
PLAYWRIGHT_DATA_DIR = PLAYWRIGHT_POM_DIR / "data"
SCREENSHOT_DIR = WORKSPACE_ROOT / "screenshots"
FAILURE_SCREENSHOT_DIR = WORKSPACE_ROOT / "failusecases"
USECASES_DIR = WORKSPACE_ROOT / "usecases"
REPORTS_DIR = WORKSPACE_ROOT / "reports"
RESULTS_DIR = WORKSPACE_ROOT / "results"
CONFIG_DIR = WORKSPACE_ROOT / "configuration"
CONFIG_FILE = CONFIG_DIR / "playwright_config.json"

RESULTS_CSV = RESULTS_DIR / "results.csv"
RESULTS_TXT = RESULTS_DIR / "results.txt"
RESULTS_MD = RESULTS_DIR / "results.md"
RESULTS_JSON = RESULTS_DIR / "results.json"
URL_REGEX = re.compile(r"https?://[\w\-\.\/:?&=#%]+")
SUPPORTED_DOC_SUFFIXES = [".md", ".txt", ".pdf", ".docx", ".csv"]
DATA_ITEM_REGEX = re.compile(r"^(username|password|email)\s*(?::|-|=)\s*(?:\*\*([^*]+)\*\*|(.+))", re.IGNORECASE)
DEFAULT_CLICK_TIMEOUT_SECONDS = 20
DEFAULT_PAGE_DISCOVERY_LIMIT = 25
DEFAULT_SELECT_OPTION_DISCOVERY_LIMIT = 30
DEFAULT_USECASE_TOTAL = 50
MAX_MANUAL_PATTERN_EVENTS = 250
MAX_USECASE_RETRIES = 1
EXPLORATION_TIME_LIMIT_SECONDS = 390
AUTH_EXPLORATION_BUDGET_SECONDS = 120
EXPLORATION_WORKER_COUNT = 3
MAX_DISCOVERY_DOM_SNAPSHOTS = 4
TEACH_STORAGE_KEY = "agenticQaTeachEvents"
SCENARIO_STORE_FILE = USECASES_DIR / "scenario_registry.json"
ACTION_MEMORY_FILE = CONFIG_DIR / "action_memory.json"
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
DEFAULT_OPENAI_MODEL = "gpt-5"
SINGLE_TAB_GUARD_SCRIPT = """(() => {
    if (window.__agenticQaSingleTabGuardInstalled) {
        return;
    }
    window.__agenticQaSingleTabGuardInstalled = true;

    const normalizeTargets = () => {
        for (const anchor of Array.from(document.querySelectorAll('a[target="_blank"]'))) {
            anchor.setAttribute('target', '_self');
            anchor.removeAttribute('rel');
        }
        for (const form of Array.from(document.querySelectorAll('form[target="_blank"]'))) {
            form.setAttribute('target', '_self');
        }
    };

    const nativeOpen = window.open ? window.open.bind(window) : null;
    window.open = function(url, target, features) {
        if (typeof url === 'string' && url.trim()) {
            try {
                window.location.assign(url);
                return window;
            } catch (error) {
                // Fall through to native behavior only if same-tab navigation fails.
            }
        }
        if (nativeOpen) {
            return nativeOpen(url, '_self', features);
        }
        return window;
    };

    normalizeTargets();
    const observer = new MutationObserver(() => normalizeTargets());
    observer.observe(document.documentElement || document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['target', 'rel'] });

    document.addEventListener('click', (event) => {
        const anchor = event.target && event.target.closest ? event.target.closest('a[target="_blank"]') : null;
        if (anchor) {
            anchor.setAttribute('target', '_self');
            anchor.removeAttribute('rel');
        }
    }, true);

    window.addEventListener('beforeunload', () => observer.disconnect(), { once: true });
})();"""
AUTH_LOGIN_KEYWORDS = ("login", "log in", "sign in", "signin", "authentication", "auth")
AUTH_LOGOUT_KEYWORDS = ("logout", "log out", "sign out", "signout")
AUTH_SUBMIT_KEYWORDS = ("login", "log in", "sign in", "signin", "submit", "continue", "auth")
AUTH_SUCCESS_KEYWORDS = ("dashboard", "welcome", "logged in", "my account", "profile", "secure area", "successfully logged")
AUTH_ERROR_KEYWORDS = ("invalid", "incorrect", "required", "error", "failed", "warning", "try again", "mismatch")
AUTH_FIELD_KEYWORDS = ("user", "username", "email", "password", "login", "signin", "sign in")
DISCOVERY_EXPAND_KEYWORDS = ("menu", "more", "show", "browse", "expand", "open", "category", "filter", "navigation", "departments")
EXPLORATORY_KEYWORDS = ("exploratory", "explore", "all available", "all links", "all options", "all possible actions")
FRESH_DOM_KEYWORDS = (
    "capture the dom freshly",
    "capture dom freshly",
    "fresh dom",
    "delete old dom",
    "delete the old dom",
    "delete any previously stored dom",
    "do not rely on previously captured dom",
    "do not reuse an older dom snapshot",
    "cached structure",
    "freshly each time",
)
DISCOVERY_SKIP_CLICK_KEYWORDS = (
    "submit",
    "sign in",
    "log in",
    "login",
    "logout",
    "log out",
    "sign out",
    "delete",
    "remove",
    "checkout",
    "pay",
    "place order",
    "buy",
    "add to cart",
    "purchase",
)
LOW_VALUE_ACTION_TEXT = (
    "skip to main content",
    "manage consents",
    "main menu",
    "sub-navigation",
    "accept",
    "decline",
    "privacy policy",
    "terms and conditions",
    "cookie",
    "consent",
)
LOW_VALUE_ACTION_HREF_PARTS = ("#main-content", "/privacy-policy", "/terms-and-conditions")
SECTION_HEADER_PREFIXES = (
    "scenario",
    "changes required",
    "from the current flow",
    "rules",
    "notes",
    "outputs",
    "purpose",
    "how it works",
)


def load_workspace_env() -> None:
    env_path = WORKSPACE_ROOT / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            os.environ[key] = value


load_workspace_env()

for path in [
    RESULTS_DIR,
    DOM_DIR,
    PLAYWRIGHT_DIR,
    PLAYWRIGHT_POM_DIR,
    PLAYWRIGHT_PAGES_DIR,
    PLAYWRIGHT_TESTS_DIR,
    PLAYWRIGHT_DATA_DIR,
    SCREENSHOT_DIR,
    FAILURE_SCREENSHOT_DIR,
    USECASES_DIR,
    REPORTS_DIR,
    CONFIG_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return cleaned.strip("_") or "scenario"


def load_action_memory() -> dict:
    if not ACTION_MEMORY_FILE.exists():
        return {}
    try:
        return json.loads(ACTION_MEMORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_action_memory(memory: dict) -> None:
    ACTION_MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    ACTION_MEMORY_FILE.write_text(json.dumps(memory, indent=2), encoding="utf-8")


def memory_key_for_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower() or slugify(url)


def merge_manual_patterns(existing_patterns: List[dict], new_patterns: List[dict]) -> List[dict]:
    merged: List[dict] = []
    seen: Set[Tuple[str, str, str, str, str]] = set()
    for pattern in (new_patterns or []) + (existing_patterns or []):
        if not isinstance(pattern, dict):
            continue
        dedupe_key = (
            str(pattern.get("action", "")).strip().lower(),
            str(pattern.get("url", "")).strip().lower(),
            str(pattern.get("selector", "")).strip().lower(),
            str(pattern.get("label", "")).strip().lower(),
            str(pattern.get("value", "")).strip().lower(),
        )
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        merged.append(pattern)
        if len(merged) >= MAX_MANUAL_PATTERN_EVENTS:
            break
    return merged


def merge_string_list(existing: List[str], incoming: List[str], limit: Optional[int] = None) -> List[str]:
    merged: List[str] = []
    seen: Set[str] = set()
    for item in (existing or []) + (incoming or []):
        value = str(item).strip()
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append(value)
        if limit is not None and len(merged) >= limit:
            break
    return merged


def merge_record_list(existing: List[dict], incoming: List[dict], key_fields: Tuple[str, ...]) -> List[dict]:
    merged: List[dict] = []
    index_by_key: Dict[Tuple[str, ...], int] = {}
    for item in (existing or []) + (incoming or []):
        if not isinstance(item, dict):
            continue
        key = tuple(str(item.get(field, "")).strip().lower() for field in key_fields)
        if not any(key):
            continue
        if key in index_by_key:
            merged[index_by_key[key]].update({k: v for k, v in item.items() if v not in (None, "", [], {})})
            continue
        index_by_key[key] = len(merged)
        merged.append(dict(item))
    return merged


def merge_input_records(existing: List[dict], incoming: List[dict]) -> List[dict]:
    merged: List[dict] = []
    index_by_key: Dict[Tuple[str, str, str, str, str], int] = {}
    for item in (existing or []) + (incoming or []):
        if not isinstance(item, dict):
            continue
        key = (
            str(item.get("name", "")).strip().lower(),
            str(item.get("id", "")).strip().lower(),
            str(item.get("placeholder", "")).strip().lower(),
            str(item.get("type", "")).strip().lower(),
            str(item.get("selector", "")).strip().lower(),
        )
        if not any(key):
            continue
        normalized = dict(item)
        normalized["options"] = merge_record_list([], list(item.get("options", [])), ("label", "value"))
        if key in index_by_key:
            existing_item = merged[index_by_key[key]]
            existing_item.update({k: v for k, v in normalized.items() if v not in (None, "", [], {})})
            existing_item["options"] = merge_record_list(
                list(existing_item.get("options", [])),
                list(normalized.get("options", [])),
                ("label", "value"),
            )
            continue
        index_by_key[key] = len(merged)
        merged.append(normalized)
    return merged


def merge_page_records(existing: dict, incoming: dict) -> dict:
    merged = dict(existing)
    merged["url"] = merged.get("url") or incoming.get("url") or ""
    merged["title"] = merged.get("title") or incoming.get("title") or ""
    merged["links"] = merge_record_list(list(existing.get("links", [])), list(incoming.get("links", [])), ("text", "href", "selector"))
    merged["buttons"] = merge_record_list(list(existing.get("buttons", [])), list(incoming.get("buttons", [])), ("text", "selector"))
    merged["inputs"] = merge_input_records(list(existing.get("inputs", [])), list(incoming.get("inputs", [])))
    merged["headings"] = merge_string_list(list(existing.get("headings", [])), list(incoming.get("headings", [])), limit=12)
    existing_preview = str(existing.get("text_preview", "")).strip()
    incoming_preview = str(incoming.get("text_preview", "")).strip()
    merged["text_preview"] = incoming_preview if len(incoming_preview) > len(existing_preview) else existing_preview
    merged["select_explorations"] = merge_record_list(
        list(existing.get("select_explorations", [])),
        list(incoming.get("select_explorations", [])),
        ("selector", "value", "selected_url"),
    )
    merged["explored_select_option_count"] = max(
        int(existing.get("explored_select_option_count", 0) or 0),
        int(incoming.get("explored_select_option_count", 0) or 0),
    )
    merged["inventory_source"] = merged.get("inventory_source") or incoming.get("inventory_source") or ""
    merged["discovery_state"] = merged.get("discovery_state") or incoming.get("discovery_state") or ""
    merged["discovered_at"] = merged.get("discovered_at") or incoming.get("discovered_at") or datetime.now().isoformat()
    merged["error"] = merged.get("error") or incoming.get("error") or ""
    return merged


def load_taught_pages_for_url(url: str) -> List[dict]:
    memory_entry = load_action_memory().get(memory_key_for_url(url), {})
    taught_pages = memory_entry.get("taught_pages", [])
    if not isinstance(taught_pages, list):
        return []
    return [page for page in taught_pages if isinstance(page, dict)]


def load_manual_patterns_for_url(url: str) -> List[dict]:
    memory_entry = load_action_memory().get(memory_key_for_url(url), {})
    manual_patterns = memory_entry.get("manual_patterns", [])
    if not isinstance(manual_patterns, list):
        return []
    return [pattern for pattern in manual_patterns if isinstance(pattern, dict)]


def append_existing_usecase(usecases: List[dict], usecase: dict) -> None:
    title = str(usecase.get("title", "")).strip()
    page_url = str(usecase.get("page_url", "")).strip()
    if not title:
        return
    if any(existing.get("title") == title and str(existing.get("page_url", "")).strip() == page_url for existing in usecases):
        return
    usecases.append(usecase)


def taught_page_priority_score(page: dict) -> int:
    inputs = list(page.get("inputs", []))
    selectable_controls = sum(1 for item in inputs if str(item.get("type", "")).lower() in {"select", "radio", "checkbox"})
    fillable_controls = sum(1 for item in inputs if str(item.get("type", "")).lower() not in {"hidden", "submit", "button"})
    return (selectable_controls * 6) + (fillable_controls * 3) + len(page.get("buttons", [])[:10]) + len(page.get("links", [])[:10])


def build_taught_usecases(
    url: str,
    metadata: dict,
    taught_pages: List[dict],
    manual_patterns: List[dict],
) -> List[dict]:
    if not taught_pages and not manual_patterns:
        return []

    usecases: List[dict] = []
    ordered_page_urls: List[str] = []
    for pattern in manual_patterns:
        page_url = str(pattern.get("url", "")).strip()
        if page_url and page_url not in ordered_page_urls:
            ordered_page_urls.append(page_url)

    taught_page_map = {
        str(page.get("url", "")).strip(): page
        for page in taught_pages
        if str(page.get("url", "")).strip()
    }

    journey_steps = ["verify page loads", "capture DOM before actions"]
    for pattern in manual_patterns[:30]:
        action = str(pattern.get("action", "")).strip().lower()
        selector = str(pattern.get("selector", "")).strip()
        label = str(pattern.get("label", "")).strip()
        href = str(pattern.get("href", "")).strip()
        value = str(pattern.get("value", "")).strip()
        target = href or selector or label
        if action == "click" and target:
            journey_steps.append(f"click {target}")
            journey_steps.append("capture DOM after click")
        elif action == "fill" and value and (selector or label):
            journey_steps.append(f"fill {selector or label} with {value}")
            journey_steps.append("capture DOM after input")
        elif action == "change" and value and (selector or label):
            journey_steps.append(f"select {selector or label} option {value}")
            journey_steps.append("capture DOM after input")

    if len(journey_steps) > 2:
        append_usecase(
            usecases,
            url,
            "Taught path: replay learned exploration journey",
            "Replay the manually taught website journey before exploring alternate options.",
            "happy",
            journey_steps,
            ordered_page_urls[0] if ordered_page_urls else url,
            "taught-flow",
        )

    priority_pages: List[dict] = []
    for page_url in ordered_page_urls:
        page = taught_page_map.get(page_url)
        if page:
            priority_pages.append(page)
    for page in taught_pages:
        if page not in priority_pages:
            priority_pages.append(page)

    scored_priority_pages = sorted(priority_pages, key=taught_page_priority_score, reverse=True)
    for page in scored_priority_pages[:3]:
        exploratory_variants = build_exploratory_cases(page, 1, metadata, ["taught blueprint"])
        if not exploratory_variants:
            continue
        candidate = dict(exploratory_variants[0])
        page_title = page.get("title") or page.get("url") or "Page"
        candidate["title"] = f"{testcase_prefix_for_url(url)}-Taught blueprint alternate: {page_title}"
        candidate["description"] = f"Use the manually taught DOM blueprint for {page_title} and try an alternate meaningful action from the same page."
        candidate["category"] = "taught-blueprint"
        append_existing_usecase(usecases, candidate)

    if is_login_intent(["login"], metadata) and has_login_credentials(metadata):
        login_url = ordered_page_urls[0] if ordered_page_urls else url
        append_usecase(
            usecases,
            url,
            "Taught path: authenticated entry using learned site flow",
            "Validate the learned site path while using the supplied credentials where authentication is required.",
            "happy",
            [
                f"fill {login_identifier_key(metadata)} with {login_identifier_value(metadata)}",
                f"fill password with {metadata.get('password', '')}",
                "click login",
                "verify authenticated state",
                "capture DOM after login",
            ],
            login_url,
            "taught-authentication",
        )

    return usecases


def testcase_prefix_for_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower() or url.lower()
    host = host.replace("www.", "")
    host = re.sub(r"[^a-z0-9]+", "-", host).strip("-")
    return f"TC-{host or 'site'}"


def read_pdf_file(path: Path) -> str:
    pypdf2_module = load_pypdf2_module()
    reader = pypdf2_module.PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def read_docx_file(path: Path) -> str:
    document_class = load_docx_document()
    document = document_class(str(path))
    parts: List[str] = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            parts.append(text)

    for table in document.tables:
        for row in table.rows:
            cells = [re.sub(r"\s+", " ", cell.text).strip() for cell in row.cells]
            if any(cells):
                parts.append(" | ".join(cell for cell in cells if cell))

    return "\n".join(parts)


def read_csv_file(path: Path) -> str:
    rows: List[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as csvfile:
        sample = csvfile.read(4096)
        csvfile.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample or ",")
        except csv.Error:
            dialect = csv.excel
        reader = csv.reader(csvfile, dialect)
        all_rows = [[cell.strip() for cell in row] for row in reader if any(cell.strip() for cell in row)]

    if not all_rows:
        return ""

    header = all_rows[0]
    header_keys = [re.sub(r"[^a-z0-9]+", "_", cell.lower()).strip("_") for cell in header]
    structured_header = any(key in {"url", "website", "site", "username", "email", "password", "instruction", "instructions", "requirement", "requirements", "scenario"} for key in header_keys)

    if structured_header and len(all_rows) > 1:
        for row in all_rows[1:]:
            parts = []
            for index, value in enumerate(row):
                if not value:
                    continue
                key = header[index] if index < len(header) and header[index] else f"Column {index + 1}"
                parts.append(f"{key}: {value}")
            if parts:
                rows.append("\n".join(parts))
    else:
        for row in all_rows:
            rows.append("\n".join(value for value in row if value))

    return "\n\n".join(rows)


def load_pypdf2_module():
    global PyPDF2
    if PyPDF2 is None:
        try:
            PyPDF2 = importlib.import_module("PyPDF2")
        except ImportError as exc:
            raise RuntimeError(
                "PDF support requires PyPDF2. Rebuild the VSIX with bundled dependencies or install PyPDF2 in the selected Python environment."
            ) from exc
    return PyPDF2


def load_docx_document():
    global Document
    if Document is None:
        try:
            Document = importlib.import_module("docx").Document
        except ImportError as exc:
            raise RuntimeError(
                "DOCX support requires python-docx. Rebuild the VSIX with bundled dependencies or install python-docx in the selected Python environment."
            ) from exc
    return Document


def read_doc_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return normalize_document_text(read_pdf_file(path))
    if suffix == ".docx":
        return normalize_document_text(read_docx_file(path))
    if suffix == ".csv":
        return normalize_document_text(read_csv_file(path))
    return normalize_document_text(path.read_text(encoding="utf-8"))


def read_first_doc_file() -> Optional[Path]:
    docs: List[Path] = []
    for suffix in SUPPORTED_DOC_SUFFIXES:
        docs.extend(sorted(DOCS_DIR.glob(f"*{suffix}")))
    return docs[0] if docs else None


def save_scenario_text(text: str, file_name: str = "pasted_scenario.md") -> Path:
    if not text.strip():
        raise ValueError("Scenario text is empty.")
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    scenario_path = DOCS_DIR / file_name
    scenario_path.write_text(text.strip() + "\n", encoding="utf-8")
    return scenario_path


def prompt_user_for_scenario_text() -> str:
    print("Enter the scenario text for testing.")
    print("Start with the target URL on the first line.")
    print("Finish by typing a single line containing only EOF.")
    lines: List[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "EOF":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def prompt_user_for_file_path() -> str:
    return input("Enter the path to the .pdf, .md, .txt, .docx or .csv instruction file: ").strip()


def resolve_doc_path(doc_path: Optional[str], scenario_text: Optional[str]) -> Optional[Path]:
    if scenario_text:
        if "\\n" in scenario_text:
            scenario_text = scenario_text.replace("\\n", "\n")
        return save_scenario_text(scenario_text)

    if doc_path:
        provided_path = Path(doc_path)
        if not provided_path.is_absolute():
            provided_path = WORKSPACE_ROOT / provided_path
        if not provided_path.exists():
            raise FileNotFoundError(f"Instruction file not found: {provided_path}")
        if provided_path.suffix.lower() not in SUPPORTED_DOC_SUFFIXES:
            raise ValueError(f"Instruction file must be one of: {', '.join(SUPPORTED_DOC_SUFFIXES)}")
        return provided_path

    existing = read_first_doc_file()
    if existing:
        use_existing = input(f"Found existing instruction file '{existing.name}'. Use it? [Y/n]: ").strip().lower()
        if use_existing in ["", "y", "yes"]:
            return existing

    choice = input("No instruction file selected. Type 'file' to provide a path or 'paste' to enter scenario text: ").strip().lower()
    if choice == "file":
        file_path = prompt_user_for_file_path()
        return resolve_doc_path(file_path, None)
    if choice == "paste":
        return save_scenario_text(prompt_user_for_scenario_text())

    print("No valid input selected.")
    return None


def extract_url(text: str) -> Optional[str]:
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    if URL_REGEX.match(first_line):
        return first_line.strip()
    found = URL_REGEX.search(text)
    return found.group(0) if found else None


def normalize_document_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.replace("\u00a0", " ").replace("\ufeff", "").replace("\u200b", "")
    return normalized.strip() + ("\n" if normalized.strip() else "")


def clean_instruction_line(line: str) -> str:
    cleaned = re.sub(r"^[\-\*\u2022]+\s*", "", line.strip())
    cleaned = re.sub(r"^\d+\s*[\.\)]\s*", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" -")


def get_groq_api_key() -> str:
    return (
        os.environ.get("GROQ_API_KEY", "").strip()
        or os.environ.get("GROQ_KEY", "").strip()
        or os.environ.get("groq_key", "").strip()
    )


def get_gemini_api_key() -> str:
    return (
        os.environ.get("GEMINI_API_KEY", "").strip()
        or os.environ.get("GOOGLE_API_KEY", "").strip()
        or os.environ.get("GEMINI_KEY", "").strip()
        or os.environ.get("gemini_key", "").strip()
    )


def get_openai_api_key() -> str:
    return (
        os.environ.get("OPENAI_API_KEY", "").strip()
        or os.environ.get("OPENAI_KEY", "").strip()
        or os.environ.get("openai_key", "").strip()
    )


def get_llm_provider() -> str:
    configured = os.environ.get("AGENTIC_QA_LLM_PROVIDER", "").strip().lower()
    if configured:
        return configured
    if get_openai_api_key():
        return "openai"
    if get_gemini_api_key():
        return "gemini"
    if get_groq_api_key():
        return "groq"
    return ""


def is_instruction_noise(line: str) -> bool:
    lowered = line.lower().strip()
    if not lowered:
        return True
    if lowered.startswith("#"):
        return True
    if lowered.startswith("note:"):
        return True
    if lowered.endswith(":") and not URL_REGEX.search(lowered):
        return True
    if lowered in SECTION_HEADER_PREFIXES:
        return True
    if re.fullmatch(r"[\W_]+", lowered):
        return True
    return False


def is_usecase_generation_directive(line: str) -> bool:
    return bool(
        re.search(
            r"(?:draft|generate|create|prepare|write|build)\s+\d+\s+(?:(?:high\s*level|low\s*level|positive|negative|happy\s*path|edge|exploratory|\w+)\s+){0,5}(?:test\s*)?(?:use\s*cases|cases|test\s*cases)",
            line,
            re.IGNORECASE,
        )
    )


def is_usecase_count_directive(line: str) -> bool:
    return bool(
        re.search(
            r"(?:must\s+not\s+exceed|should\s+not\s+exceed|do\s+not\s+exceed|not\s+exceed(?:ing)?|no\s+more\s+than|up\s+to|maximum\s+of|max(?:imum)?)\s*(?:more\s+than\s*)?\d+\b",
            line,
            re.IGNORECASE,
        )
    )


def parse_instructions(text: str) -> List[str]:
    lines = [clean_instruction_line(line) for line in text.splitlines() if line.strip()]
    instructions = []
    for line in lines:
        if not line:
            continue
        if URL_REGEX.match(line):
            continue
        if DATA_ITEM_REGEX.match(line):
            continue
        if is_instruction_noise(line):
            continue
        if is_usecase_generation_directive(line):
            continue
        if is_usecase_count_directive(line):
            continue
        instructions.append(line)
    return instructions


def extract_metadata(text: str) -> dict:
    metadata = {}
    for line in text.splitlines():
        match = DATA_ITEM_REGEX.match(line.strip())
        if match:
            key = match.group(1).lower()
            metadata[key] = (match.group(2) or match.group(3) or "").strip()
    return normalize_credentials_metadata(metadata)


def normalize_credentials_metadata(metadata: dict) -> dict:
    normalized = dict(metadata)
    email_value = str(normalized.get("email", "")).strip()
    username_value = str(normalized.get("username", "")).strip()
    if email_value and "@" not in email_value and not username_value:
        normalized["username"] = email_value
    return normalized


def merge_runtime_metadata(metadata: dict, incoming: dict) -> dict:
    merged = dict(metadata)
    for key in ["username", "email", "password"]:
        value = str(incoming.get(key, "")).strip()
        if value:
            merged[key] = value
    return merged


def build_requirement_understanding(
    text: str,
    url: str,
    instructions: List[str],
    metadata: dict,
    requested_count: Optional[int],
) -> dict:
    lower_text = " ".join(instructions).lower()
    action_keywords = []
    if "responsive" in lower_text:
        action_keywords.append("responsive coverage")
    if "link" in lower_text or "header" in lower_text or "menu" in lower_text:
        action_keywords.append("navigation and link coverage")
    if "checkout" in lower_text or "cart" in lower_text or "ecommerce" in lower_text:
        action_keywords.append("commerce and checkout flow")
    if "form" in lower_text or is_form_intent(instructions):
        action_keywords.append("form interactions and validation")
    if is_login_intent(instructions, metadata):
        action_keywords.append("authentication-aware flow")
    if requires_fresh_dom_run(instructions):
        action_keywords.append("fresh DOM capture without reuse")
    if not action_keywords:
        action_keywords.append("general website exploration")

    return {
        "primary_url": url,
        "instruction_count": len(instructions),
        "requested_usecase_count": requested_count or DEFAULT_USECASE_TOTAL,
        "credentials_provided": has_login_credentials(metadata),
        "credential_mode": "email" if metadata.get("email") else ("username" if metadata.get("username") else "missing"),
        "fresh_dom_required": requires_fresh_dom_run(instructions),
        "exploratory_request": is_exploratory_request(instructions),
        "focus_areas": infer_document_focus_areas(instructions, metadata),
        "action_keywords": action_keywords,
        "key_requirements": instructions[:10],
        "source_excerpt": text.splitlines()[:12],
    }


def print_requirement_understanding(understanding: dict) -> None:
    print("Document understanding:")
    print(f"- Target URL: {understanding['primary_url']}")
    print(f"- Parsed instructions: {understanding['instruction_count']}")
    print(f"- Requested use cases: {understanding['requested_usecase_count']}")
    print(f"- Credentials provided: {'Yes' if understanding['credentials_provided'] else 'No'}")
    print(f"- Fresh DOM required: {'Yes' if understanding['fresh_dom_required'] else 'No'}")
    print(f"- Focus areas: {', '.join(understanding['focus_areas'])}")
    print(f"- Execution intent: {', '.join(understanding['action_keywords'])}")
    print("Key requirements I extracted:")
    for requirement in understanding.get("key_requirements", []):
        print(f"- {requirement}")


def capture_confirmed_requirement(
    instruction_path: Path,
    initial_text: str,
) -> Tuple[Path, str, str, List[str], dict, Optional[int], dict]:
    text = normalize_document_text(initial_text)
    current_path = instruction_path

    while True:
        url = extract_url(text)
        if not url:
            print("The requirement does not contain a valid URL yet.")
            text = normalize_document_text(prompt_user_for_scenario_text())
            if not text:
                continue
            current_path = save_scenario_text(text, file_name=f"{slugify(current_path.stem)}_confirmed.md")
            continue

        instructions = parse_instructions(text)
        metadata = extract_metadata(text)
        requested_count = requested_usecase_count(text)
        understanding = build_requirement_understanding(text, url, instructions, metadata, requested_count)
        print_requirement_understanding(understanding)

        confirmation = input("Is this what you want to do? [Y/N/E]: ").strip().lower()
        if confirmation in {"y", "yes"}:
            return current_path, text, url, instructions, metadata, requested_count, understanding
        if confirmation in {"e", "edit"}:
            print("Enter only the minor change or extra instruction and finish with EOF.")
            minor_edit = prompt_user_for_scenario_text()
            if not minor_edit.strip():
                print("No minor edit was provided. Keeping the current requirement for confirmation.")
                continue
            text = apply_minor_requirement_edit(text, minor_edit)
            current_path = save_scenario_text(text, file_name=f"{slugify(current_path.stem)}_edited.md")
            continue

        print("Type the requirement again and finish with EOF.")
        replacement = normalize_document_text(prompt_user_for_scenario_text())
        if not replacement:
            print("No replacement requirement was provided. Keeping the current requirement for confirmation.")
            continue
        text = replacement
        current_path = save_scenario_text(text, file_name=f"{slugify(current_path.stem)}_confirmed.md")


def prompt_for_missing_credentials(login_page_url: str) -> dict:
    print("Authentication appears to be required, but usable credentials were not found.")
    print(f"Detected login page: {login_page_url}")
    identifier = input("Enter email or username for this site (leave blank to cancel): ").strip()
    password = input("Enter password (leave blank to cancel): ").strip()
    if not identifier or not password:
        return {}
    if "@" in identifier:
        return {"email": identifier, "password": password}
    return {"username": identifier, "password": password}


def apply_minor_requirement_edit(current_text: str, edit_text: str) -> str:
    addition = normalize_document_text(edit_text)
    if not addition.strip():
        return current_text
    base = current_text.rstrip()
    return (base + "\n" + addition.strip() + "\n").strip() + "\n"


def requested_usecase_count(text: str) -> Optional[int]:
    normalized_text = " ".join(text.split())
    for pattern in [
        r"(?:limit|restrict|cap)\s+(?:the\s+)?(?:test\s*)?(?:use\s*cases|cases|test\s*cases)\s+(?:to|at)\s*(\d+)",
        r"(?:use\s*cases|usecases|test\s*cases|cases)\s+(?:needed|required|requested)\s+(?:only\s*)?(\d+)",
        r"(?:only\s*)?(\d+)\s+(?:use\s*cases|usecases|test\s*cases|cases)\s+(?:needed|required|requested)?",
        r"(?:draft|generate|create|prepare|write|build)\s*(\d+)\s+(?:(?:high\s*level|low\s*level|positive|negative|happy\s*path|edge|exploratory|\w+)\s+){0,5}(?:test\s*)?(?:use\s*cases|cases|test\s*cases)",
        r"(?:must\s+not\s+exceed|should\s+not\s+exceed|do\s+not\s+exceed|not\s+exceed(?:ing)?|no\s+more\s+than|up\s+to|maximum\s+of|max(?:imum)?)\s*(?:more\s+than\s*)?(\d+)\s*(?:test\s*)?(?:use\s*cases|cases|test\s*cases)?",
        r"more than\s*(\d+)\s*(?:use\s*cases|cases)",
        r"at least\s*(\d+)\s*(?:use\s*cases|cases)",
        r"(?:exactly|only|just)\s*(\d+)\s*(?:test\s*)?(?:use\s*cases|cases|test\s*cases)",
        r"(?:need|want|run|execute)\s*(\d+)\s*(?:test\s*)?(?:use\s*cases|cases|test\s*cases)",
        r"(?:use\s*cases|cases|test\s*cases)\s*(?:to|at)\s*(\d+)",
        r"(\d+)\s*[:\-]\s*(\d+)\s*(?:use\s*cases|cases)",
        r"(\d+)\s*(?:test\s*)?(?:use\s*cases|cases|test\s*cases)\s*(?:per\s*page)?",
    ]:
        match = re.search(pattern, normalized_text, re.IGNORECASE)
        if not match:
            continue
        numbers = [int(group) for group in match.groups() if group]
        if len(numbers) == 2:
            return max(max(numbers), 3)
        if numbers:
            return max(numbers[0], 3)
    return None


def has_login_credentials(credentials: dict) -> bool:
    return bool(credentials.get("password") and (credentials.get("username") or credentials.get("email")))


def login_identifier_key(credentials: dict) -> str:
    return "username" if credentials.get("username") else "email"


def login_identifier_value(credentials: dict) -> str:
    return credentials.get("username") or credentials.get("email") or ""


def is_login_intent(instructions: List[str], metadata: dict) -> bool:
    lower_text = " ".join(instructions).lower()
    return has_login_credentials(metadata) or any(
        term in lower_text for term in ["login", "sign in", "signin", "credentials", "password", "username", "email"]
    )


def is_form_intent(instructions: List[str]) -> bool:
    lower_text = " ".join(instructions).lower()
    return any(term in lower_text for term in ["fill", "enter", "select", "submit", "search", "input"])


def contains_any_keyword(value: str, keywords: Tuple[str, ...]) -> bool:
    lowered = value.lower()
    return any(keyword in lowered for keyword in keywords)


def normalize_instruction(instruction: str) -> str:
    return instruction.lower().strip()


def scenario_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_registry() -> dict:
    if not SCENARIO_STORE_FILE.exists():
        return {}
    try:
        return json.loads(SCENARIO_STORE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_registry(registry: dict) -> None:
    SCENARIO_STORE_FILE.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def build_scenario_id(doc_path: Path, text: str) -> str:
    return f"{slugify(doc_path.stem)}_{scenario_hash(text)[:10]}"


def usecase_bundle_paths(scenario_id: str) -> Dict[str, Path]:
    return {
        "json": USECASES_DIR / f"{scenario_id}_usecases.json",
        "md": USECASES_DIR / f"{scenario_id}_usecases.md",
        "txt": USECASES_DIR / f"{scenario_id}_usecases.txt",
        "csv": USECASES_DIR / f"{scenario_id}_usecases.csv",
    }


def site_understanding_paths(scenario_id: str) -> Dict[str, Path]:
    return {
        "json": USECASES_DIR / f"{scenario_id}_site_understanding.json",
        "md": USECASES_DIR / f"{scenario_id}_site_understanding.md",
        "txt": USECASES_DIR / f"{scenario_id}_site_understanding.txt",
    }


def infer_page_purpose(page_data: dict) -> str:
    title = page_data.get("title", "")
    url = page_data.get("url", "")
    headings = " ".join(page_data.get("headings", []))
    link_text = " ".join((link.get("text") or "") for link in page_data.get("links", []))
    button_text = " ".join((button.get("text") or "") for button in page_data.get("buttons", []))
    source = " ".join([title, url, headings, link_text, button_text]).lower()

    if page_has_auth_form_signal(page_data):
        return "authentication"
    if "contact" in source or "support" in source:
        return "contact"
    if "search" in source:
        return "search"
    if page_data.get("inputs"):
        return "form"
    if "blog" in source or "article" in source:
        return "content"
    if "course" in source or "pricing" in source or "shop" in source:
        return "catalog"
    return "navigation"


def page_has_login_signal(page_data: dict) -> bool:
    title = page_data.get("title", "")
    url = page_data.get("url", "")
    headings = " ".join(page_data.get("headings", []))
    text_preview = page_data.get("text_preview", "")
    inputs = page_data.get("inputs", [])
    buttons = page_data.get("buttons", [])
    source = " ".join([title, url, headings, text_preview]).lower()
    if contains_any_keyword(source, AUTH_LOGIN_KEYWORDS):
        return True
    if any((item.get("type") or "").lower() == "password" for item in inputs):
        return True
    for item in inputs:
        candidate = " ".join([
            item.get("name", ""),
            item.get("id", ""),
            item.get("placeholder", ""),
            item.get("type", ""),
        ]).lower()
        if contains_any_keyword(candidate, AUTH_FIELD_KEYWORDS):
            return True
    for button in buttons:
        if contains_any_keyword(button.get("text", ""), AUTH_LOGIN_KEYWORDS):
            return True
    return False


def page_has_auth_form_signal(page_data: dict) -> bool:
    inputs = page_data.get("inputs", [])
    title = page_data.get("title", "")
    url = page_data.get("url", "")
    headings = " ".join(page_data.get("headings", []))
    text_preview = page_data.get("text_preview", "")
    buttons = page_data.get("buttons", [])

    has_password = any((item.get("type") or "").lower() == "password" for item in inputs)
    has_identifier = False
    for item in inputs:
        candidate = " ".join([
            item.get("name", ""),
            item.get("id", ""),
            item.get("placeholder", ""),
            item.get("type", ""),
        ]).lower()
        if contains_any_keyword(candidate, ("user", "username", "email", "login", "signin", "sign in")):
            has_identifier = True
            break

    if has_password and has_identifier:
        return True

    source = " ".join([title, url, headings, text_preview]).lower()
    has_auth_copy = contains_any_keyword(source, AUTH_LOGIN_KEYWORDS)
    has_auth_button = any(contains_any_keyword(button.get("text", ""), AUTH_LOGIN_KEYWORDS) for button in buttons)
    return has_password and (has_auth_copy or has_auth_button)


def page_has_logout_signal(page_data: dict) -> bool:
    title = page_data.get("title", "")
    url = page_data.get("url", "")
    text_preview = page_data.get("text_preview", "")
    source = " ".join([title, url, text_preview]).lower()
    if contains_any_keyword(source, AUTH_LOGOUT_KEYWORDS):
        return True
    for item in page_data.get("links", []) + page_data.get("buttons", []):
        text = item.get("text") or item.get("href") or ""
        if contains_any_keyword(text, AUTH_LOGOUT_KEYWORDS):
            return True
    return False


def find_logout_target(page_data: dict) -> Optional[str]:
    for item in page_data.get("links", []) + page_data.get("buttons", []):
        text = (item.get("text") or "").strip()
        href = (item.get("href") or "").strip()
        if text and contains_any_keyword(text, AUTH_LOGOUT_KEYWORDS):
            return text
        if href and contains_any_keyword(href, AUTH_LOGOUT_KEYWORDS):
            return href
    return None


def infer_document_focus_areas(instructions: List[str], metadata: dict) -> List[str]:
    focus_areas: List[str] = []
    lower_text = " ".join(instructions).lower()
    if is_login_intent(instructions, metadata):
        focus_areas.append("authentication")
    if is_form_intent(instructions):
        focus_areas.append("form validation")
    if "search" in lower_text:
        focus_areas.append("search")
    if "link" in lower_text or "navigate" in lower_text or "menu" in lower_text:
        focus_areas.append("navigation")
    if "logout" in lower_text or "sign out" in lower_text:
        focus_areas.append("logout")
    return focus_areas or ["general navigation"]


def is_exploratory_request(instructions: List[str]) -> bool:
    lower_text = " ".join(instructions).lower()
    return any(keyword in lower_text for keyword in EXPLORATORY_KEYWORDS)


def requires_fresh_dom_run(instructions: List[str]) -> bool:
    lower_text = " ".join(instructions).lower()
    return any(keyword in lower_text for keyword in FRESH_DOM_KEYWORDS)


def clear_persisted_site_memory(url: str) -> None:
    memory = load_action_memory()
    key = memory_key_for_url(url)
    if key not in memory:
        return
    memory.pop(key, None)
    save_action_memory(memory)


def load_site_memory_for_url(url: str) -> dict:
    return load_action_memory().get(memory_key_for_url(url), {})


def build_site_understanding(
    url: str,
    instructions: List[str],
    metadata: dict,
    discovered_pages: List[dict],
    requested_count: Optional[int],
) -> dict:
    pages = discovered_pages or [{"url": url, "title": "Primary page", "links": [], "buttons": [], "inputs": []}]
    auth_pages = [page for page in pages if page_has_auth_form_signal(page)]
    logout_pages = [page for page in pages if page_has_logout_signal(page)]
    primary_auth_page = auth_pages[0] if auth_pages else pages[0]
    memory = load_action_memory().get(memory_key_for_url(url), {})
    logout_target = None
    for page in auth_pages + logout_pages + pages:
        logout_target = find_logout_target(page)
        if logout_target:
            break
    if not logout_target:
        logout_target = memory.get("logout_target")

    page_summaries = []
    for page in pages:
        purpose = infer_page_purpose(page)
        page_summaries.append({
            "title": page.get("title") or page.get("url") or "Untitled page",
            "url": page.get("url") or url,
            "purpose": purpose,
            "link_count": len(page.get("links", [])),
            "button_count": len(page.get("buttons", [])),
            "input_count": len(page.get("inputs", [])),
            "headings": page.get("headings", [])[:5],
            "auth_related": page_has_auth_form_signal(page) or page_has_logout_signal(page),
            "text_preview": page.get("text_preview", ""),
        })

    auth_detected = bool(auth_pages) or is_login_intent(instructions, metadata)
    coverage_hints: List[str] = []
    if auth_detected:
        coverage_hints.append("Include positive login coverage with valid credentials.")
        coverage_hints.append("Include logout coverage as part of the high-level auth flow.")
        coverage_hints.append("Include invalid and incomplete credential checks.")
    if any(page.get("input_count", 0) > 0 for page in page_summaries):
        coverage_hints.append("Validate visible form behavior and error feedback.")
    if any(page.get("link_count", 0) > 0 for page in page_summaries):
        coverage_hints.append("Cover major navigation paths across discovered pages.")

    summary = {
        "primary_url": url,
        "requested_usecase_count": requested_count or DEFAULT_USECASE_TOTAL,
        "page_count": len(pages),
        "auth_detected": auth_detected,
        "login_page_url": primary_auth_page.get("url") or url,
        "login_page_title": primary_auth_page.get("title") or "Primary page",
        "logout_target": logout_target or "logout",
        "document_focus_areas": infer_document_focus_areas(instructions, metadata),
        "coverage_hints": coverage_hints,
        "pages": page_summaries,
        "summary_text": (
            f"Discovered {len(pages)} page(s). "
            f"Primary auth page: {(primary_auth_page.get('title') or primary_auth_page.get('url') or url)}. "
            f"Focus areas: {', '.join(infer_document_focus_areas(instructions, metadata))}."
        ),
    }
    return summary


def site_requires_login_credentials(
    url: str,
    instructions: List[str],
    metadata: dict,
    discovered_pages: List[dict],
) -> bool:
    if has_login_credentials(metadata):
        return False

    if is_login_intent(instructions, metadata):
        return True

    if not discovered_pages:
        return False

    normalized_url = normalize_crawl_url(url).rstrip("/")
    start_page = None
    for page in discovered_pages:
        page_url = normalize_crawl_url(str(page.get("url", "")).strip()).rstrip("/")
        if page_url == normalized_url:
            start_page = page
            break
    if start_page is None:
        start_page = discovered_pages[0]

    auth_pages = [page for page in discovered_pages if page_has_auth_form_signal(page)]
    meaningful_non_auth_pages = [
        page for page in discovered_pages
        if not page_has_auth_form_signal(page) and not str(page.get("error", "")).strip()
    ]

    if start_page and page_has_auth_form_signal(start_page):
        return True
    if auth_pages and not meaningful_non_auth_pages:
        return True
    return False


def write_site_understanding_files(scenario_id: str, site_understanding: dict) -> Dict[str, Path]:
    paths = site_understanding_paths(scenario_id)
    lines = [
        "# Site Understanding",
        f"Primary URL: {site_understanding['primary_url']}",
        f"Requested Use Cases: {site_understanding['requested_usecase_count']}",
        f"Discovered Pages: {site_understanding['page_count']}",
        f"Authentication Detected: {'Yes' if site_understanding['auth_detected'] else 'No'}",
        f"Primary Auth Page: {site_understanding['login_page_title']} ({site_understanding['login_page_url']})",
        f"Logout Target Hint: {site_understanding['logout_target']}",
        "",
        f"Summary: {site_understanding['summary_text']}",
        "",
        "Focus Areas:",
    ]
    for area in site_understanding.get("document_focus_areas", []):
        lines.append(f"- {area}")
    lines.append("")
    lines.append("Coverage Hints:")
    for hint in site_understanding.get("coverage_hints", []):
        lines.append(f"- {hint}")
    lines.append("")
    lines.append("Discovered Pages:")
    for page in site_understanding.get("pages", []):
        lines.append(
            f"- {page['title']} | {page['purpose']} | {page['url']} | "
            f"links={page['link_count']} buttons={page['button_count']} inputs={page['input_count']}"
        )
        if page.get("headings"):
            lines.append(f"  headings: {', '.join(page['headings'])}")

    content = "\n".join(lines)
    paths["json"].write_text(json.dumps(site_understanding, indent=2), encoding="utf-8")
    paths["md"].write_text(content, encoding="utf-8")
    paths["txt"].write_text(content, encoding="utf-8")
    return paths


def append_usecase(
    usecases: List[dict],
    site_url: str,
    title: str,
    description: str,
    case_type: str,
    instructions: List[str],
    page_url: str,
    category: Optional[str] = None,
) -> None:
    prefixed_title = f"{testcase_prefix_for_url(site_url)}-{title}"
    if any(existing["title"] == prefixed_title and existing.get("page_url", "") == page_url for existing in usecases):
        return
    payload = {
        "title": prefixed_title,
        "description": description,
        "type": case_type,
        "instructions": instructions,
        "page_url": page_url,
    }
    if category:
        payload["category"] = category
    usecases.append(payload)


def assign_case_ids(usecases: List[dict]) -> List[dict]:
    assigned: List[dict] = []
    for index, usecase in enumerate(usecases, start=1):
        case_id = f"TC{index:03d}"
        updated = dict(usecase)
        updated["case_id"] = case_id
        title = str(updated.get("title", "")).strip()
        if title and not title.startswith(f"{case_id} -"):
            updated["title"] = f"{case_id} - {title}"
        assigned.append(updated)
    return assigned


def build_baseline_usecases(
    url: str,
    instructions: List[str],
    metadata: dict,
    site_understanding: Optional[dict] = None,
) -> List[dict]:
    metadata = normalize_credentials_metadata(metadata)
    lower_text = " ".join(instructions).lower()
    usecases: List[dict] = []
    auth_detected = (site_understanding or {}).get("auth_detected", False) or is_login_intent(instructions, metadata)
    auth_page_url = (site_understanding or {}).get("login_page_url", url)
    logout_target = (site_understanding or {}).get("logout_target", "logout")

    if auth_detected:
        has_valid_credentials = has_login_credentials(metadata)
        valid_identifier_key = login_identifier_key(metadata) if has_valid_credentials else "username"
        valid_identifier_value = login_identifier_value(metadata) if has_valid_credentials else ""
        invalid_identifier_value = "invalid_email@example.com" if valid_identifier_key == "email" else "invalid_user"
        login_steps: List[str] = []
        logout_steps: List[str] = []
        if has_valid_credentials:
            login_steps.extend([
                f"fill {valid_identifier_key} with {valid_identifier_value}",
                f"fill password with {metadata.get('password', '')}",
            ])
            logout_steps.extend(login_steps)
        else:
            login_steps.append("verify auth form is visible")
            logout_steps.append("verify auth form is visible")
        login_steps.extend([
            "submit auth form",
            "verify authenticated state",
            "capture DOM after login",
        ])
        logout_steps.extend([
            "submit auth form",
            "verify authenticated state",
            "capture DOM after login",
            f"click {logout_target}",
            "verify logout succeeds",
            "capture DOM after logout",
        ])

        append_usecase(
            usecases,
            url,
            "Happy path: positive login",
            "Validate that valid credentials allow the user to log in successfully.",
            "happy",
            login_steps,
            auth_page_url,
            "authentication",
        )
        append_usecase(
            usecases,
            url,
            "Happy path: positive login and logout",
            "Validate the complete authentication round trip from login through logout.",
            "happy",
            logout_steps,
            auth_page_url,
            "authentication",
        )
        append_usecase(
            usecases,
            url,
            "Negative path: invalid login is rejected",
            "Validate expected error handling when invalid credentials are submitted.",
            "negative",
            [
                f"fill {valid_identifier_key} with {invalid_identifier_value}",
                "fill password with invalid_pass",
                "submit auth form",
                "verify error message appears",
                "capture DOM after invalid login",
            ],
            auth_page_url,
            "authentication",
        )
        append_usecase(
            usecases,
            url,
            "Negative path: missing login data is validated",
            "Validate required-field behavior for the authentication form.",
            "negative",
            [
                "submit required inputs incorrectly",
                "verify validation or error feedback",
                "capture DOM after invalid input",
            ],
            auth_page_url,
            "authentication",
        )
        append_usecase(
            usecases,
            url,
            "Edge case: authentication controls remain visible",
            "Check that the login page exposes the expected controls before interaction.",
            "edge",
            [
                "verify page loads",
                "verify auth form is visible",
                "verify links are visible",
                "capture DOM after auth form inspection",
            ],
            auth_page_url,
            "authentication",
        )
        return usecases

    if is_form_intent(instructions):
        happy_steps = [
            instr for instr in instructions
            if normalize_instruction(instr).startswith(("fill", "enter", "click", "select", "submit", "search"))
        ] or ["verify page loads", "capture DOM"]
        negative_steps = [
            "submit required inputs incorrectly",
            "verify validation or error feedback",
            "capture DOM after invalid input",
        ]
    else:
        happy_steps = ["verify page loads", "capture DOM"]
        negative_steps = ["verify page loads", "capture DOM"]

    edge_steps = ["verify navigation is stable", "capture DOM after each major step"]
    if "link" in lower_text or "responsive" in lower_text:
        edge_steps.append("verify links are visible")
    if "search" in lower_text:
        edge_steps.append("enter search query with test")

    append_usecase(
        usecases,
        url,
        "Happy path: basic flow",
        f"Validate the happy path on {url} using the provided instructions.",
        "happy",
        happy_steps,
        url,
    )
    append_usecase(
        usecases,
        url,
        "Negative path: invalid or missing input",
        "Validate expected failures when input is incorrect or required steps are skipped.",
        "negative",
        negative_steps,
        url,
    )
    append_usecase(
        usecases,
        url,
        "Edge case: alternate navigation or UI behavior",
        "Verify edge cases and alternate navigation from the same starting point.",
        "edge",
        edge_steps,
        url,
    )
    return usecases


def build_seed_usecases(
    url: str,
    instructions: List[str],
    metadata: dict,
    requested_count: Optional[int] = None,
    site_understanding: Optional[dict] = None,
    expand_to_requested_count: bool = False,
) -> List[dict]:
    usecases = build_baseline_usecases(url, instructions, metadata, site_understanding)

    target_count = requested_count if requested_count is not None else len(usecases)
    if expand_to_requested_count and target_count > len(usecases):
        usecases.extend(
            build_exploratory_cases(
                {"url": url, "title": "Primary page", "links": [], "buttons": [], "inputs": [], "headings": [], "text_preview": ""},
                target_count - len(usecases),
                metadata,
                instructions,
            )
        )
    return usecases[:target_count] if requested_count is not None else usecases


def infer_action_candidates(
    page_data: dict,
    primary_url: str,
    include_all_controls: bool = False,
    allow_persisted_memory: bool = True,
) -> List[Tuple[str, str]]:
    learned = learned_actions_for_page(page_data, primary_url) if allow_persisted_memory else []
    link_actions: List[Tuple[str, str]] = []
    button_actions: List[Tuple[str, str]] = []
    select_actions: List[Tuple[str, str]] = []
    fill_actions: List[Tuple[str, str]] = []
    links = page_data.get("links", [])
    buttons = page_data.get("buttons", [])
    inputs = page_data.get("inputs", [])
    area_rank = {"header": 0, "navigation": 1, "main": 2, "body": 3, "footer": 4}
    primary_host = urlparse(primary_url).netloc.lower()

    sorted_links = sorted(
        links[:200 if include_all_controls else 80],
        key=lambda link: (
            area_rank.get(str(link.get("area") or "").lower(), 5),
            len(str(link.get("text") or "")),
            str(link.get("text") or link.get("href") or "").lower(),
        ),
    )

    for link in sorted_links:
        label = link.get("text") or link.get("href") or "link"
        href = link.get("href") or primary_url
        resolved_href = urljoin(primary_url, href)
        parsed_href = urlparse(resolved_href)
        if parsed_href.scheme not in {"http", "https"}:
            continue
        if primary_host and parsed_href.netloc.lower() != primary_host:
            continue
        if is_noise_link_target(href, primary_url):
            continue
        if not include_all_controls and is_low_value_link_action(label, href, primary_url):
            continue
        if include_all_controls and href and href.rstrip("/") == primary_url.rstrip("/"):
            continue
        link_actions.append(("click", f"{label}||{resolved_href}"))

    sorted_buttons = sorted(
        buttons[:80 if include_all_controls else 40],
        key=lambda button: (
            area_rank.get(str(button.get("area") or "").lower(), 5),
            len(str(button.get("text") or "")),
            str(button.get("text") or button.get("selector") or "").lower(),
        ),
    )

    for button in sorted_buttons:
        label = button.get("text") or button.get("selector") or "button"
        if not include_all_controls and is_low_value_button_action(button):
            continue
        button_actions.append(("button", label))

    for input_item in inputs[:80 if include_all_controls else 25]:
        label = (
            input_item.get("label")
            or input_item.get("name")
            or input_item.get("placeholder")
            or input_item.get("id")
            or input_item.get("value")
            or input_item.get("type")
            or "field"
        )
        if is_low_value_input_action(input_item, include_headers=include_all_controls) or (
            not include_all_controls and is_low_value_control_action(label)
        ):
            continue
        input_type = str(input_item.get("type") or "").lower()
        if input_type in {"radio", "checkbox"}:
            choice_target = input_item.get("label") or input_item.get("value") or input_item.get("selector") or label
            if choice_target:
                button_actions.append(("button", str(choice_target)))
            continue
        if input_type == "select":
            options = [option for option in input_item.get("options", []) if option.get("value") or option.get("label")]
            for option in options[:25]:
                option_value = option.get("value") or option.get("label") or ""
                if option_value:
                    select_actions.append(("select", f"{label}||{option_value}"))
            continue
        fill_actions.append(("fill", label))

    actions: List[Tuple[str, str]] = []
    actions.extend(link_actions)
    actions.extend(button_actions)
    actions.extend(fill_actions)
    actions.extend(select_actions)

    prioritized_actions: List[Tuple[str, str]] = []
    seen_actions: Set[Tuple[str, str]] = set()
    for action in learned + actions:
        if is_noise_action_candidate(action, primary_url):
            continue
        if action in seen_actions:
            continue
        seen_actions.add(action)
        prioritized_actions.append(action)

    return prioritized_actions or [("observe", primary_url)]


async def snapshot_teach_mode_page_inventory(page: Page, captured_pages: List[dict]) -> None:
    if page.is_closed():
        return
    page_url = str(page.url or "").strip()
    if not page_url.startswith(("http://", "https://")):
        return

    try:
        await page.wait_for_load_state("domcontentloaded", timeout=5000)
    except Exception:
        pass

    try:
        content = await page.content()
        dom_helper.save_dom_snapshot(slugify(page_url), content)
    except Exception:
        pass

    try:
        inventory = await collect_page_inventory(page)
    except Exception:
        return

    inventory["inventory_source"] = "teach_mode"
    inventory["discovery_state"] = "taught_by_user"
    inventory["discovered_at"] = datetime.now().isoformat()
    captured_pages.append(inventory)


async def attach_teach_mode_page_capture(context, captured_pages: List[dict]) -> None:
    def install_handlers(page: Page) -> None:
        page.on("domcontentloaded", lambda *_: asyncio.create_task(snapshot_teach_mode_page_inventory(page, captured_pages)))
        page.on("load", lambda *_: asyncio.create_task(snapshot_teach_mode_page_inventory(page, captured_pages)))

    for existing_page in context.pages:
        install_handlers(existing_page)

    def handle_new_page(page: Page) -> None:
        install_handlers(page)
        asyncio.create_task(snapshot_teach_mode_page_inventory(page, captured_pages))

    context.on("page", handle_new_page)


def infer_form_fill_steps(page_data: dict, case_index: int) -> List[str]:
    inputs = [item for item in page_data.get("inputs", []) if not is_low_value_input_action(item)][:4]
    steps: List[str] = []
    if not inputs:
        return steps

    variant = case_index % 3
    for input_item in inputs:
        label = input_item.get("name") or input_item.get("placeholder") or input_item.get("id") or input_item.get("type") or "field"
        normalized = str(label).lower()
        if "password" in normalized:
            value = "edge_case_input" if variant == 0 else ("invalid_input" if variant == 1 else "happy_path_input")
        elif "email" in normalized:
            value = "invalid_input" if variant == 1 else "happy_path_input"
        else:
            value = "happy_path_input" if variant == 2 else ("edge_case_input" if variant == 0 else "invalid_input")
        steps.append(f"fill {label} with {value}")

    return steps


def learned_actions_for_page(page_data: dict, primary_url: str) -> List[Tuple[str, str]]:
    memory_entry = load_action_memory().get(memory_key_for_url(primary_url), {})
    manual_patterns = memory_entry.get("manual_patterns", [])
    if not manual_patterns:
        return []

    page_url = str(page_data.get("url") or primary_url).strip().lower()
    learned_actions: List[Tuple[str, str]] = []
    seen: Set[Tuple[str, str]] = set()
    for pattern in manual_patterns:
        target_url = str(pattern.get("url", "")).strip().lower()
        if target_url and target_url != page_url:
            continue
        action = str(pattern.get("action", "")).strip().lower()
        selector = str(pattern.get("selector", "")).strip()
        label = str(pattern.get("label", "")).strip()
        value = str(pattern.get("value", "")).strip()
        href = str(pattern.get("href", "")).strip()

        candidate: Optional[Tuple[str, str]] = None
        if action == "click":
            click_target = href or selector or label
            if click_target:
                candidate = ("click", click_target)
        elif action == "change":
            if value and (selector or label):
                candidate = ("select", f"{selector or label}||{value}")
        elif action == "fill":
            fill_target = selector or label
            if fill_target:
                candidate = ("fill", fill_target)

        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        learned_actions.append(candidate)

    return learned_actions


def is_low_value_link_action(label: str, href: str, page_url: str) -> bool:
    normalized_label = (label or "").strip().lower()
    normalized_href = (href or "").strip().lower()
    normalized_page_url = (page_url or "").strip().lower()
    if contains_any_keyword(normalized_label, LOW_VALUE_ACTION_TEXT):
        return True
    if any(part in normalized_href for part in LOW_VALUE_ACTION_HREF_PARTS):
        return True
    if normalized_href and normalized_page_url and normalized_href.rstrip("/") == normalized_page_url.rstrip("/"):
        return True
    return False


def is_noise_link_target(href: str, page_url: str) -> bool:
    normalized_href = (href or "").strip().lower()
    normalized_page_url = (page_url or "").strip().lower()
    if not normalized_href:
        return True
    if normalized_href.startswith(("#", "javascript:", "mailto:", "tel:")):
        return True
    if "#" in normalized_href and normalized_href.split("#", 1)[0].rstrip("/") == normalized_page_url.rstrip("/"):
        return True
    return False


def is_low_value_control_action(label: str) -> bool:
    normalized_label = (label or "").strip().lower()
    return not normalized_label or contains_any_keyword(normalized_label, LOW_VALUE_ACTION_TEXT)


def is_low_value_input_action(input_item: dict, include_headers: bool = False) -> bool:
    input_type = str(input_item.get("type") or "").lower()
    identifier = " ".join([
        str(input_item.get("name") or ""),
        str(input_item.get("id") or ""),
        str(input_item.get("placeholder") or ""),
        str(input_item.get("selector") or ""),
    ]).lower()
    if input_type in {"hidden", "submit", "button"}:
        return True
    if not include_headers and (identifier.startswith("header-") or "#header-" in identifier):
        return True
    if "search pane" in identifier or "search-pane" in identifier:
        return True
    if "product-lists-" in identifier:
        return True
    if not include_headers and identifier.strip() in {"type", "search"}:
        return True
    return contains_any_keyword(identifier, LOW_VALUE_ACTION_TEXT)


def is_low_value_button_action(button_item: dict) -> bool:
    label = str(button_item.get("text") or button_item.get("selector") or "")
    selector = str(button_item.get("selector") or "").lower()
    normalized_label = label.strip().lower()
    if is_low_value_control_action(label):
        return True
    if normalized_label.startswith("button:nth-of-type("):
        return True
    if normalized_label == "search" and ("header" in selector or "search" in selector):
        return True
    return False


def is_noise_action_candidate(action: Tuple[str, str], page_url: str) -> bool:
    action_type, action_target = action
    normalized_target = (action_target or "").strip().lower()
    if not normalized_target:
        return True
    if action_type == "click" and "||" in action_target:
        _, href = action_target.split("||", 1)
        return is_noise_link_target(href, page_url)
    if action_type in {"click", "button"} and normalized_target.startswith(("button:nth-of-type(", "a:nth-of-type(")):
        return True
    return False


def build_exploratory_cases(page_data: dict, target_count: int, metadata: dict, instructions: List[str]) -> List[dict]:
    page_title = page_data.get("title") or page_data.get("url") or "Page"
    page_url = page_data.get("url") or ""
    exploratory_request = is_exploratory_request(instructions)
    fresh_dom_run = requires_fresh_dom_run(instructions)
    actions = infer_action_candidates(
        page_data,
        page_url,
        include_all_controls=exploratory_request,
        allow_persisted_memory=not fresh_dom_run,
    )
    exploratory_cases: List[dict] = []
    login_hint = page_has_auth_form_signal(page_data)
    has_form_inputs = any(
        str(item.get("type") or "").lower() not in {"hidden", "submit", "button", "select"}
        and not is_low_value_input_action(item, include_headers=exploratory_request)
        for item in page_data.get("inputs", [])
    )

    for index in range(target_count):
        action = actions[index] if index < len(actions) else (actions[index % len(actions)] if actions else ("observe", "page"))
        steps = ["verify page loads", "capture DOM before actions"]
        action_type, action_target = action
        title_suffix = ""

        if action_type == "click":
            if "||" in action_target:
                label, href = action_target.split("||", 1)
            else:
                label, href = action_target, action_target
            steps.append(f"click {href}")
            steps.append("verify page loads")
            steps.append("capture DOM after click")
            if exploratory_request:
                steps.append("return to previous page")
                steps.append("verify page loads")
                steps.append("capture DOM after going back")
            title_suffix = f"click link {label[:30]}"
        elif action_type == "button":
            steps.append(f"click {action_target}")
            steps.append("capture DOM after click")
            if exploratory_request:
                steps.append("return to previous page")
                steps.append("verify page loads")
                steps.append("capture DOM after going back")
            title_suffix = f"click action {action_target[:30]}"
        elif action_type == "fill":
            if has_form_inputs and not login_hint and index % 2 == 0:
                form_steps = infer_form_fill_steps(page_data, index)
                steps.extend(form_steps)
                steps.append("submit required inputs incorrectly" if index % 3 == 1 else "click submit")
                steps.append("capture DOM after input")
                title_suffix = f"explore form {page_title[:24]}"
            else:
                value = "edge_case_input" if index % 3 == 0 else ("invalid_input" if index % 3 == 1 else "happy_path_input")
                steps.append(f"fill {action_target} with {value}")
                steps.append("capture DOM after input")
                title_suffix = f"fill field {action_target[:30]}"
        elif action_type == "select":
            if "||" in action_target:
                label, value = action_target.split("||", 1)
            else:
                label, value = action_target, ""
            steps.append(f"select {label} option {value}")
            steps.append("verify navigation is stable")
            steps.append("capture DOM after input")
            title_suffix = f"select option {value[:24]}"
        else:
            steps.append("verify navigation is stable")
            steps.append("capture DOM after each major step")
            title_suffix = "observe page"

        if login_hint and index % 4 == 0:
            steps.append("verify auth form is visible")

        if index % 5 == 0:
            steps.append("verify links are visible")
        if has_form_inputs and not login_hint and index % 7 == 0:
            steps.append("submit required inputs incorrectly")

        exploratory_cases.append({
            "title": f"{page_title}: exploratory case {index + 1}",
            "description": f"Auto-generated exploratory case for {page_title} to {title_suffix}.",
            "type": "exploratory",
            "instructions": steps,
            "page_url": page_url,
            "category": title_suffix,
        })

    return exploratory_cases


def build_exploratory_sweep_usecases(
    pages: List[dict],
    target_count: int,
    metadata: dict,
    instructions: List[str],
) -> List[dict]:
    usecases: List[dict] = []
    remaining = max(target_count, 0)
    exploratory_request = is_exploratory_request(instructions)

    for page in pages:
        if remaining <= 0:
            break
        page_url = str(page.get("url") or "").strip()
        action_candidates = infer_action_candidates(
            page,
            page_url or str(page.get("title") or "page"),
            include_all_controls=exploratory_request,
            allow_persisted_memory=not requires_fresh_dom_run(instructions),
        )
        if not action_candidates:
            continue
        page_target = min(len(action_candidates), remaining)
        usecases.extend(build_exploratory_cases(page, page_target, metadata, instructions))
        remaining = target_count - len(usecases)

    if remaining > 0 and pages:
        for page in pages:
            if remaining <= 0:
                break
            top_up_cases = build_exploratory_cases(page, remaining, metadata, instructions)
            for usecase in top_up_cases:
                append_existing_usecase(usecases, usecase)
                if len(usecases) >= target_count:
                    break
            remaining = target_count - len(usecases)

    return usecases[:target_count]


def sanitize_llm_usecases(raw_usecases: Any, fallback_url: str, target_count: int) -> List[dict]:
    if not isinstance(raw_usecases, list):
        return []

    cleaned: List[dict] = []
    seen: Set[Tuple[str, str]] = set()
    for index, item in enumerate(raw_usecases):
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip() or f"Exploratory case {index + 1}"
        page_url = str(item.get("page_url", "")).strip() or fallback_url
        description = str(item.get("description", "")).strip() or f"Generated use case for {title}."
        case_type = str(item.get("type", "exploratory")).strip().lower() or "exploratory"
        if case_type not in {"happy", "negative", "edge", "exploratory"}:
            case_type = "exploratory"
        instructions = [str(step).strip() for step in item.get("instructions", []) if str(step).strip()]
        if not instructions:
            continue

        dedupe_key = (title.lower(), page_url.lower())
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        cleaned.append({
            "title": title,
            "description": description,
            "type": case_type,
            "instructions": instructions,
            "page_url": page_url,
            "category": str(item.get("category", case_type)).strip() or case_type,
        })
        if len(cleaned) >= target_count:
            break

    return cleaned


def build_llm_prompt_payload(
    document_text: str,
    url: str,
    instructions: List[str],
    metadata: dict,
    discovered_pages: List[dict],
    requested_count: int,
    site_understanding: Optional[dict],
    fallback_usecases: List[dict],
) -> dict:
    page_summaries = [
        {
            "title": page.get("title", ""),
            "url": page.get("url", ""),
            "purpose": page.get("purpose", ""),
            "headings": page.get("headings", [])[:4],
            "buttons": [(button.get("text") or button.get("selector") or "") for button in page.get("buttons", [])[:6]],
            "inputs": [item.get("name") or item.get("placeholder") or item.get("type") or "" for item in page.get("inputs", [])[:6]],
        }
        for page in (discovered_pages or [])[:8]
    ]
    baseline_preview = fallback_usecases[: min(len(fallback_usecases), 8)]

    prompt_payload = {
        "target_url": url,
        "requested_usecase_count": requested_count,
        "developer_requirement_document": document_text,
        "parsed_testing_instructions": instructions,
        "credentials_or_metadata": metadata,
        "site_understanding": site_understanding or {},
        "discovered_pages": page_summaries,
        "baseline_usecases": baseline_preview,
        "allowed_instruction_patterns": [
            "verify page loads",
            "verify auth form is visible",
            "fill <field> with <value>",
            "click <target>",
            "submit auth form",
            "verify authenticated state",
            "verify error message appears",
            "verify logout succeeds",
            "verify validation or error feedback",
            "verify links are visible",
            "verify navigation is stable",
            "submit required inputs incorrectly",
            "capture DOM after <action>",
            "capture DOM before actions",
        ],
        "requirements": [
            "The uploaded or pasted developer requirement document is mandatory and is the source of truth.",
            "Do not invent flows, pages, or assertions that are not grounded in the requirement document or the discovered site context.",
            "When the document asks for specific coverage such as header links, checkout, login, logout, forms, responsive behavior, or fresh DOM handling, reflect those priorities directly.",
            "Think like a QA engineer: infer meaningful happy, negative, edge, and exploratory coverage from the requirement and discovered site context.",
            "Do not require the developer to spoon-feed testing ideas if the requirement already implies them.",
            "Return only runnable JSON. No markdown, no commentary.",
            "Use only the allowed instruction patterns so the existing automation executor can run them.",
            "Stay within the requested use case count.",
            "Prioritize the real login page for authentication scenarios when credentials are provided.",
        ],
        "json_shape": [
            {
                "title": "string",
                "description": "string",
                "type": "happy|negative|edge|exploratory",
                "instructions": ["string"],
                "page_url": "string",
                "category": "string",
            }
        ],
    }

    return prompt_payload


def request_groq_usecases(
    prompt_payload: dict,
    url: str,
    requested_count: int,
) -> Optional[List[dict]]:
    api_key = get_groq_api_key()
    if not api_key:
        return None

    try:
        groq_module = importlib.import_module("groq")
    except ImportError:
        print("Groq API key detected, but the 'groq' package is not installed. Falling back to rule-based use case generation.")
        return None

    try:
        client_class = getattr(groq_module, "Groq")
    except AttributeError:
        print("Groq client could not be loaded from the installed package. Falling back to rule-based use case generation.")
        return None

    model_name = os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL

    try:
        client = client_class(api_key=api_key)
        completion = client.chat.completions.create(
            model=model_name,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior QA engineer. Generate practical website exploratory and functional test use cases from a developer requirement document "
                        "and discovered site context. Return only valid JSON."
                    ),
                },
                {"role": "user", "content": json.dumps(prompt_payload, ensure_ascii=True)},
            ],
        )
        content = completion.choices[0].message.content if completion and completion.choices else ""
        if not content:
            return None

        start = content.find("[")
        end = content.rfind("]")
        if start == -1 or end == -1 or end <= start:
            return None
        parsed = json.loads(content[start : end + 1])
        llm_usecases = sanitize_llm_usecases(parsed, url, requested_count)
        if llm_usecases:
            print(f"Groq-assisted use case refinement applied with model '{model_name}'.")
            return llm_usecases
    except Exception as exc:
        print(f"Groq-assisted generation could not be applied ({exc}). Falling back to rule-based use case generation.")

    return None


def request_gemini_usecases(
    prompt_payload: dict,
    url: str,
    requested_count: int,
) -> Optional[List[dict]]:
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    model_name = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash").strip() or "gemini-3.6-flash"
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    )
    request_body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are a senior QA engineer. Generate practical website exploratory and functional test use cases "
                            "from a developer requirement document and discovered site context. Return only valid JSON.\n\n"
                            + json.dumps(prompt_payload, ensure_ascii=True)
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
        },
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        candidates = payload.get("candidates", [])
        if not candidates:
            return None
        parts = (((candidates[0] or {}).get("content") or {}).get("parts") or [])
        content = "".join(str(part.get("text", "")) for part in parts if isinstance(part, dict))
        if not content:
            return None

        start = content.find("[")
        end = content.rfind("]")
        if start == -1 or end == -1 or end <= start:
            return None
        parsed = json.loads(content[start : end + 1])
        gemini_usecases = sanitize_llm_usecases(parsed, url, requested_count)
        if gemini_usecases:
            print(f"Gemini-assisted use case refinement applied with model '{model_name}'.")
            return gemini_usecases
    except urllib.error.HTTPError as exc:
        try:
            error_body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            error_body = str(exc)
        print(f"Gemini-assisted generation could not be applied ({error_body}). Falling back to rule-based use case generation.")
    except Exception as exc:
        print(f"Gemini-assisted generation could not be applied ({exc}). Falling back to rule-based use case generation.")

    return None


def extract_openai_response_text(payload: dict) -> str:
    output_items = payload.get("output", [])
    collected: List[str] = []
    for item in output_items:
        if not isinstance(item, dict):
            continue
        for content_item in item.get("content", []) or []:
            if not isinstance(content_item, dict):
                continue
            if content_item.get("type") == "output_text":
                text = str(content_item.get("text", "")).strip()
                if text:
                    collected.append(text)
    return "\n".join(collected).strip()


def request_openai_usecases(
    prompt_payload: dict,
    url: str,
    requested_count: int,
) -> Optional[List[dict]]:
    api_key = get_openai_api_key()
    if not api_key:
        return None

    model_name = os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL).strip() or DEFAULT_OPENAI_MODEL
    endpoint = "https://api.openai.com/v1/responses"
    request_body = {
        "model": model_name,
        "input": (
            "You are a senior QA engineer. Generate practical website exploratory and functional test use cases "
            "from a developer requirement document and discovered site context. Return only a JSON array.\n\n"
            + json.dumps(prompt_payload, ensure_ascii=True)
        ),
        "text": {
            "format": {
                "type": "json_schema",
                "name": "agentic_qa_usecases",
                "strict": True,
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "type": {"type": "string", "enum": ["happy", "negative", "edge", "exploratory"]},
                            "instructions": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "page_url": {"type": "string"},
                            "category": {"type": "string"},
                        },
                        "required": ["title", "description", "type", "instructions", "page_url", "category"],
                    },
                },
            }
        },
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        content = extract_openai_response_text(payload)
        if not content:
            return None

        parsed = json.loads(content)
        llm_usecases = sanitize_llm_usecases(parsed, url, requested_count)
        if llm_usecases:
            print(f"OpenAI-assisted use case refinement applied with model '{model_name}'.")
            return llm_usecases
    except urllib.error.HTTPError as exc:
        try:
            error_body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            error_body = str(exc)
        print(f"OpenAI-assisted generation could not be applied ({error_body}). Falling back to rule-based use case generation.")
    except Exception as exc:
        print(f"OpenAI-assisted generation could not be applied ({exc}). Falling back to rule-based use case generation.")

    return None


def request_llm_usecases(
    document_text: str,
    url: str,
    instructions: List[str],
    metadata: dict,
    discovered_pages: List[dict],
    requested_count: int,
    site_understanding: Optional[dict],
    fallback_usecases: List[dict],
) -> Optional[List[dict]]:
    provider = get_llm_provider()
    if not provider:
        return None

    prompt_payload = build_llm_prompt_payload(
        document_text=document_text,
        url=url,
        instructions=instructions,
        metadata=metadata,
        discovered_pages=discovered_pages,
        requested_count=requested_count,
        site_understanding=site_understanding,
        fallback_usecases=fallback_usecases,
    )

    if provider == "openai":
        return request_openai_usecases(prompt_payload, url, requested_count)
    if provider == "gemini":
        return request_gemini_usecases(prompt_payload, url, requested_count)
    if provider == "groq":
        return request_groq_usecases(prompt_payload, url, requested_count)

    print(
        f"Unknown LLM provider '{provider}'. Supported values for AGENTIC_QA_LLM_PROVIDER are 'openai', 'gemini' and 'groq'. "
        "Falling back to rule-based use case generation."
    )
    return None


def build_final_usecases(
    url: str,
    document_text: str,
    instructions: List[str],
    metadata: dict,
    discovered_pages: List[dict],
    requested_count: Optional[int],
    site_understanding: Optional[dict] = None,
) -> List[dict]:
    exploratory_request = is_exploratory_request(instructions)
    taught_pages = load_taught_pages_for_url(url)
    manual_patterns = load_manual_patterns_for_url(url)
    taught_usecases = build_taught_usecases(url, metadata, taught_pages, manual_patterns)
    seed_usecases = build_seed_usecases(
        url,
        instructions,
        metadata,
        requested_count=None,
        site_understanding=site_understanding,
        expand_to_requested_count=False,
    )
    final_usecases: List[dict] = []
    for usecase in taught_usecases + seed_usecases:
        append_existing_usecase(final_usecases, usecase)

    target_count = requested_count if requested_count is not None else DEFAULT_USECASE_TOTAL
    pages = discovered_pages or [{"url": url, "title": "Primary page", "links": [], "buttons": [], "inputs": [], "headings": [], "text_preview": ""}]
    remaining = target_count - len(final_usecases)
    if remaining <= 0:
        return final_usecases[:target_count]

    taught_page_urls = {str(page.get("url", "")).strip().lower() for page in taught_pages if str(page.get("url", "")).strip()}
    prioritized_pages = [page for page in pages if str(page.get("url", "")).strip().lower() in taught_page_urls]
    fallback_pages = [page for page in pages if str(page.get("url", "")).strip().lower() not in taught_page_urls]
    generation_pages = prioritized_pages or pages

    if exploratory_request:
        sweep_cases = build_exploratory_sweep_usecases(generation_pages + fallback_pages, remaining, metadata, instructions)
        for usecase in sweep_cases:
            append_existing_usecase(final_usecases, usecase)
            if len(final_usecases) >= target_count:
                break
        return final_usecases[:target_count]

    base_count = remaining // len(generation_pages)
    extra = remaining % len(generation_pages)
    for index, page in enumerate(generation_pages):
        page_target = base_count + (1 if index < extra else 0)
        if page_target <= 0:
            continue
        final_usecases.extend(build_exploratory_cases(page, page_target, metadata, instructions))

    if len(final_usecases) < target_count and fallback_pages:
        still_needed = target_count - len(final_usecases)
        base_count = still_needed // len(fallback_pages)
        extra = still_needed % len(fallback_pages)
        for index, page in enumerate(fallback_pages):
            page_target = base_count + (1 if index < extra else 0)
            if page_target <= 0:
                continue
            final_usecases.extend(build_exploratory_cases(page, page_target, metadata, instructions))

    if taught_pages or manual_patterns:
        return final_usecases[:target_count]

    llm_usecases = request_llm_usecases(
        document_text=document_text,
        url=url,
        instructions=instructions,
        metadata=metadata,
        discovered_pages=pages,
        requested_count=target_count,
        site_understanding=site_understanding,
        fallback_usecases=final_usecases,
    )
    if not llm_usecases:
        return final_usecases[:target_count]

    if len(llm_usecases) >= target_count:
        return llm_usecases[:target_count]

    seen = {(item["title"].lower(), item.get("page_url", "").lower()) for item in llm_usecases}
    for usecase in final_usecases:
        key = (usecase["title"].lower(), usecase.get("page_url", "").lower())
        if key in seen:
            continue
        llm_usecases.append(usecase)
        seen.add(key)
        if len(llm_usecases) >= target_count:
            break
    return llm_usecases[:target_count]


def write_usecases_files(scenario_id: str, source_name: str, url: str, usecases: List[dict]) -> Dict[str, Path]:
    paths = usecase_bundle_paths(scenario_id)
    lines = [f"# Use cases generated from {source_name}", f"URL: {url}", ""]
    for uc in usecases:
        lines.append(f"## {uc.get('case_id', '')} {uc['title']}".strip())
        lines.append(f"Type: {uc['type']}")
        lines.append(f"Description: {uc['description']}")
        if uc.get("page_url"):
            lines.append(f"Page URL: {uc['page_url']}")
        lines.append("Instructions:")
        for inst in uc["instructions"]:
            lines.append(f"- {inst}")
        lines.append("")

    paths["md"].write_text("\n".join(lines), encoding="utf-8")
    paths["txt"].write_text("\n".join(lines), encoding="utf-8")
    with paths["csv"].open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["case_id", "title", "type", "description", "page_url", "instructions"])
        for uc in usecases:
            writer.writerow([uc.get("case_id", ""), uc["title"], uc["type"], uc["description"], uc.get("page_url", ""), " | ".join(uc["instructions"])])

    paths["json"].write_text(json.dumps(usecases, indent=2), encoding="utf-8")
    return paths


def load_saved_usecases(scenario_id: str) -> Optional[List[dict]]:
    path = usecase_bundle_paths(scenario_id)["json"]
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def prompt_for_approval(usecases: List[dict], scenario_id: str, auto_approve: bool, site_understanding: Optional[dict] = None) -> bool:
    if auto_approve:
        print(f"Auto-approve enabled for scenario {scenario_id}.")
        return True

    if site_understanding:
        print("I have understood what this site is about and stored the discovered DOM inventory.")
        print(site_understanding.get("summary_text", ""))
        print(
            "Discovered pages: "
            + ", ".join(page["title"] for page in site_understanding.get("pages", [])[:5])
        )
    print(f"Generated {len(usecases)} use cases for scenario '{scenario_id}'.")
    print("Review the files under /usecases and approve before browser execution.")
    approval = input("Approve generated use cases and continue? [Y/N]: ").strip().lower()
    return approval in {"y", "yes"}


def update_registry_entry(scenario_id: str, doc_path: Path, text: str, approved: bool, usecase_count: int) -> None:
    registry = load_registry()
    registry[scenario_id] = {
        "scenario_id": scenario_id,
        "source_file": str(doc_path),
        "hash": scenario_hash(text),
        "approved": approved,
        "usecase_count": usecase_count,
        "updated_at": datetime.now().isoformat(),
    }
    save_registry(registry)


async def bind_runtime_listeners(page: Page, listener_state: dict) -> None:
    bound_pages = listener_state.setdefault("bound_pages", set())
    page_key = id(page)
    if page_key in bound_pages:
        return
    bound_pages.add(page_key)

    def active_bucket() -> Optional[dict]:
        return listener_state.get("bucket")

    def handle_console(msg) -> None:
        bucket = active_bucket()
        if bucket is not None and msg.type == "error":
            bucket["console"].append({"type": msg.type, "text": msg.text})

    def handle_page_error(exc) -> None:
        bucket = active_bucket()
        if bucket is not None:
            bucket["page_errors"].append(str(exc))

    page.on("console", handle_console)
    page.on("pageerror", handle_page_error)

    async def handle_response(response):
        bucket = active_bucket()
        if bucket is not None and response.status >= 400:
            bucket["network"].append({"url": response.url, "status": response.status})

    page.on("response", lambda response: asyncio.create_task(handle_response(response)))


async def adopt_new_runtime_page(
    current_page: Page,
    listener_state: Optional[dict],
    known_page_ids: Set[int],
    click_timeout_seconds: int,
) -> Page:
    popup_wait_seconds = min(max(click_timeout_seconds, 1), 2)
    deadline = asyncio.get_running_loop().time() + popup_wait_seconds
    while asyncio.get_running_loop().time() < deadline:
        for candidate in current_page.context.pages:
            if candidate.is_closed():
                continue
            if id(candidate) in known_page_ids:
                continue
            try:
                await candidate.wait_for_load_state("domcontentloaded", timeout=2000)
            except Exception:
                pass
            if listener_state is not None:
                await bind_runtime_listeners(candidate, listener_state)
            return candidate
        await asyncio.sleep(0.1)
    return current_page


async def click_with_page_adoption(
    page: Page,
    click_action,
    click_timeout_seconds: int,
    listener_state: Optional[dict] = None,
) -> Optional[Page]:
    await enforce_single_tab_on_page(page)
    known_page_ids = {id(item) for item in page.context.pages if not item.is_closed()}
    try:
        await asyncio.wait_for(click_action(), timeout=click_timeout_seconds)
    except Exception:
        return None
    return await adopt_new_runtime_page(page, listener_state, known_page_ids, click_timeout_seconds)


async def timed_click(
    page: Page,
    target: str,
    click_timeout_seconds: int,
    listener_state: Optional[dict] = None,
) -> Optional[Page]:
    if not target:
        return None
    normalized_target = target.lower().strip()

    if target.startswith("http://") or target.startswith("https://"):
        try:
            await page.goto(target, wait_until="domcontentloaded", timeout=click_timeout_seconds * 1000)
            return page
        except Exception:
            pass

    # For auth steps like "click login", prefer the actual submit control first.
    # This avoids getting stuck on non-clickable page text such as headings or instructions.
    if any(keyword in normalized_target for keyword in AUTH_SUBMIT_KEYWORDS):
        submitted_page = await click_auth_submit_control(page, click_timeout_seconds, listener_state)
        if submitted_page is not None:
            return submitted_page
    if any(keyword in normalized_target for keyword in AUTH_LOGOUT_KEYWORDS):
        logout_page = await click_logout_control(page, click_timeout_seconds, listener_state)
        if logout_page is not None:
            return logout_page

    selectors = []
    if target.startswith("xpath=") or target.startswith("//") or target.startswith("/"):
        selectors.append(target if target.startswith("xpath=") else f"xpath={target}")
    else:
        selectors.extend([
            f"button:has-text(\"{target}\")",
            f"[role='button']:has-text(\"{target}\")",
            f"a:has-text(\"{target}\")",
            f"[aria-label*='{target}']",
            f"input[value*='{target}']",
            f"text={target}",
            target,
        ])

    for selector in selectors:
        try:
            locator = page.locator(selector)
            if await locator.count() > 0:
                clicked_page = await click_with_page_adoption(
                    page,
                    locator.first.click,
                    click_timeout_seconds,
                    listener_state,
                )
                if clicked_page is not None:
                    return clicked_page
        except Exception:
            continue
        try:
            clicked_page = await click_with_page_adoption(
                page,
                lambda: page.click(selector),
                click_timeout_seconds,
                listener_state,
            )
            if clicked_page is not None:
                return clicked_page
        except Exception:
            continue

    return None


async def safe_fill(page: Page, target: str, value: str) -> bool:
    if not target:
        return False
    if target.startswith("xpath=") or target.startswith("//") or target.startswith("/"):
        selector = target if target.startswith("xpath=") else f"xpath={target}"
        try:
            await page.fill(selector, value)
            return True
        except Exception:
            return False

    selectors = []
    if target.startswith("#") or target.startswith(".") or target.startswith("css=") or "[" in target or "=" in target:
        selectors.append(target)
    selectors += [
        f"input[name*='{target}']",
        f"input[id*='{target}']",
        f"input[placeholder*='{target}']",
        f"input[aria-label*='{target}']",
        f"textarea[name*='{target}']",
        f"textarea[id*='{target}']",
        f"textarea[placeholder*='{target}']",
    ]
    normalized_target = target.lower().strip()
    if normalized_target in {"email", "username", "user", "login"} or any(
        keyword in normalized_target for keyword in ["email", "username", "user", "login"]
    ):
        selectors = [
            "input[name*=username]",
            "input[id*=username]",
            "input[name*=user]",
            "input[id*=user]",
            "input[name*=email]",
            "input[id*=email]",
            "input[placeholder*=user]",
            "input[placeholder*=email]",
            "input[type=email]",
            "input[type=text]",
        ] + selectors

    for selector in selectors:
        try:
            await page.fill(selector, value)
            return True
        except Exception:
            continue
    return False


async def safe_select(page: Page, target: str, value: str) -> bool:
    if not target:
        return False

    selectors = []
    if target.startswith("#") or target.startswith(".") or target.startswith("css=") or "[" in target or "=" in target:
        selectors.append(target)
    selectors += [
        f"select[name*='{target}']",
        f"select[id*='{target}']",
        f"select[aria-label*='{target}']",
    ]

    for selector in selectors:
        try:
            locator = page.locator(selector)
            if await locator.count() == 0:
                continue
            await locator.first.select_option(label=value)
            return True
        except Exception:
            try:
                locator = page.locator(selector)
                if await locator.count() == 0:
                    continue
                await locator.first.select_option(value=value)
                return True
            except Exception:
                continue

    try:
        selected = await page.evaluate(
            """({ target, value }) => {
                const normalizedTarget = (target || '').toLowerCase();
                const normalizedValue = (value || '').toLowerCase();
                const selects = Array.from(document.querySelectorAll('select'));
                const match = selects.find((element) => {
                    const descriptor = [
                        element.name || '',
                        element.id || '',
                        element.getAttribute('aria-label') || '',
                    ].join(' ').toLowerCase();
                    return descriptor.includes(normalizedTarget);
                });
                if (!match) {
                    return false;
                }
                const option = Array.from(match.options || []).find((item) => {
                    const label = (item.label || item.textContent || '').trim().toLowerCase();
                    const optionValue = (item.value || '').trim().toLowerCase();
                    return label === normalizedValue || optionValue === normalizedValue;
                });
                if (!option) {
                    return false;
                }
                match.value = option.value;
                match.dispatchEvent(new Event('input', { bubbles: true }));
                match.dispatchEvent(new Event('change', { bubbles: true }));
                return true;
            }""",
            {"target": target, "value": value},
        )
        if selected:
            return True
    except Exception:
        pass

    return False


async def explore_select_options_for_page(page: Page, page_url: str, timeout_ms: int, page_inventory: dict) -> List[dict]:
    explorations: List[dict] = []
    seen_selects: Set[str] = set()
    candidate_inputs = []
    option_timeout_ms = min(timeout_ms, 10000)

    for input_item in page_inventory.get("inputs", []):
        if str(input_item.get("type") or "").lower() != "select":
            continue
        if is_low_value_input_action(input_item):
            continue
        selector = str(input_item.get("selector") or "").strip()
        label = (
            input_item.get("name")
            or input_item.get("id")
            or input_item.get("placeholder")
            or selector
            or "select"
        )
        dedupe_key = selector or str(input_item.get("id") or input_item.get("name") or label)
        if dedupe_key in seen_selects:
            continue
        seen_selects.add(dedupe_key)
        options = [option for option in input_item.get("options", []) if option.get("value") or option.get("label")]
        if not options:
            continue
        candidate_inputs.append({"label": str(label), "selector": selector, "options": options[:DEFAULT_SELECT_OPTION_DISCOVERY_LIMIT]})

    if not candidate_inputs:
        return explorations

    for input_item in candidate_inputs:
        label = input_item["label"]
        selector = input_item["selector"]
        for index, option in enumerate(input_item["options"], start=1):
            option_value = str(option.get("value") or option.get("label") or "").strip()
            option_label = str(option.get("label") or option_value).strip()
            if not option_value and not option_label:
                continue
            try:
                await page.goto(page_url, wait_until="domcontentloaded", timeout=option_timeout_ms)
                await enforce_single_tab_on_page(page)
                await wait_for_runtime_page_ready(page, option_timeout_ms)
                selected = await safe_select(page, selector or label, option_value or option_label)
                await page.wait_for_timeout(1200)
                await wait_for_runtime_page_ready(page, option_timeout_ms)
                snapshot_path = ""
                last_error = ""
                for _ in range(3):
                    try:
                        snapshot_path = await capture_runtime_dom_snapshot(
                            page,
                            f"select_{label}_{option_label or option_value}_{index}",
                        )
                        last_error = ""
                        break
                    except Exception as exc:
                        last_error = str(exc)
                        await page.wait_for_timeout(800)
                explorations.append({
                    "field": label,
                    "selector": selector,
                    "option_label": option_label,
                    "option_value": option_value,
                    "selected": selected and bool(snapshot_path),
                    "snapshot": snapshot_path,
                    "result_url": page.url,
                    **({"error": last_error} if last_error else {}),
                })
            except Exception as exc:
                explorations.append({
                    "field": label,
                    "selector": selector,
                    "option_label": option_label,
                    "option_value": option_value,
                    "selected": False,
                    "snapshot": "",
                    "result_url": page.url,
                    "error": str(exc),
                })

    return explorations


async def fill_first_matching_field(page: Page, selectors: List[str], value: str) -> bool:
    for selector in selectors:
        try:
            locator = page.locator(selector)
            if await locator.count() > 0:
                await locator.first.fill(value)
                return True
        except Exception:
            continue
    return False


async def read_body_text(page: Page) -> str:
    try:
        return await page.locator("body").inner_text(timeout=5000)
    except Exception:
        return ""


async def is_auth_form_visible(page: Page) -> bool:
    try:
        password_count = await page.locator("input[type='password']").count()
        identifier_count = await page.locator(
            "input[type='text'], input[type='email'], input[name*='user'], input[id*='user'], input[name*='email'], input[id*='email']"
        ).count()
        return password_count > 0 and identifier_count > 0
    except Exception:
        return False


async def page_has_error_feedback(page: Page) -> bool:
    try:
        alert_count = await page.locator(
            "[role='alert'], .error, .alert, .validation-error, .message-error, .woocommerce-error"
        ).count()
        if alert_count > 0:
            return True
    except Exception:
        pass
    body_text = (await read_body_text(page)).lower()
    return contains_any_keyword(body_text, AUTH_ERROR_KEYWORDS)


async def page_looks_authenticated(page: Page) -> bool:
    body_text = (await read_body_text(page)).lower()
    current_url = page.url.lower()
    auth_form_visible = await is_auth_form_visible(page)
    if contains_any_keyword(body_text, AUTH_LOGOUT_KEYWORDS):
        return True
    if contains_any_keyword(body_text, AUTH_SUCCESS_KEYWORDS):
        return True
    if not auth_form_visible and not contains_any_keyword(current_url, AUTH_LOGIN_KEYWORDS):
        return True
    return False


async def page_looks_logged_out(page: Page) -> bool:
    body_text = (await read_body_text(page)).lower()
    if await is_auth_form_visible(page):
        return True
    if contains_any_keyword(body_text, AUTH_LOGIN_KEYWORDS):
        return True
    return False


async def attempt_form_submission(
    page: Page,
    click_timeout_seconds: int,
    listener_state: Optional[dict] = None,
) -> Page:
    submitted_page = await click_auth_submit_control(page, click_timeout_seconds, listener_state)
    if submitted_page is not None:
        try:
            await wait_for_runtime_page_ready(submitted_page, click_timeout_seconds * 1000)
        except Exception:
            pass
        return submitted_page
    for target in ["login", "sign in", "submit", "continue"]:
        clicked_page = await timed_click(page, target, click_timeout_seconds, listener_state)
        if clicked_page is not None:
            try:
                await wait_for_runtime_page_ready(clicked_page, click_timeout_seconds * 1000)
            except Exception:
                pass
            return clicked_page
    return page


async def click_logout_control(
    page: Page,
    click_timeout_seconds: int,
    listener_state: Optional[dict] = None,
) -> Optional[Page]:
    selectors = [
        "a:has-text('Log out')",
        "a:has-text('Logout')",
        "button:has-text('Log out')",
        "button:has-text('Logout')",
        "input[value*='Log out']",
        "input[value*='Logout']",
        "[aria-label*='Log out']",
        "[aria-label*='Logout']",
        "a[href*='logout']",
        "button[href*='logout']",
    ]
    for selector in selectors:
        try:
            locator = page.locator(selector)
            if await locator.count() > 0:
                clicked_page = await click_with_page_adoption(
                    page,
                    locator.first.click,
                    click_timeout_seconds,
                    listener_state,
                )
                if clicked_page is not None:
                    return clicked_page
        except Exception:
            continue

    try:
        clicked_page = await click_with_page_adoption(
            page,
            lambda: page.evaluate(
                """() => {
                const candidates = Array.from(document.querySelectorAll("a, button, input[type='submit'], input[type='button']"));
                const visible = candidates.find((element) => {
                    const text = ((element.innerText || element.value || element.getAttribute('aria-label') || '') + '').toLowerCase();
                    const href = (element.getAttribute('href') || '').toLowerCase();
                    return element.offsetParent !== null && (
                        text.includes('logout') ||
                        text.includes('log out') ||
                        text.includes('sign out') ||
                        href.includes('logout')
                    );
                });
                if (!visible) {
                    return false;
                }
                visible.click();
                return true;
            }"""
            ),
            click_timeout_seconds,
            listener_state,
        )
        if clicked_page is not None:
            return clicked_page
    except Exception:
        pass
    return None


async def click_auth_submit_control(
    page: Page,
    click_timeout_seconds: int,
    listener_state: Optional[dict] = None,
) -> Optional[Page]:
    selectors = [
        "#submit",
        "form button[type='submit']",
        "form input[type='submit']",
        "button[type='submit']",
        "input[type='submit']",
        "button:has-text('Submit')",
        "button:has-text('Enter')",
        "input[value*='Enter']",
        "button:has-text('Continue')",
        "input[value*='Continue']",
        "input[value*='Submit']",
        "button:has-text('Login')",
        "button:has-text('Log in')",
        "button:has-text('Sign in')",
        "input[value*='Login']",
        "input[value*='Log in']",
        "input[value*='Sign in']",
    ]
    for selector in selectors:
        try:
            locator = page.locator(selector)
            if await locator.count() > 0:
                clicked_page = await click_with_page_adoption(
                    page,
                    locator.first.click,
                    click_timeout_seconds,
                    listener_state,
                )
                if clicked_page is not None:
                    return clicked_page
        except Exception:
            continue

    try:
        clicked_page = await click_with_page_adoption(
            page,
            lambda: page.evaluate(
                """() => {
                const passwordField = document.querySelector("input[type='password']");
                if (!passwordField) {
                    return false;
                }
                const form = passwordField.closest("form");
                const scope = form || document;
                const candidates = Array.from(scope.querySelectorAll("button, input[type='submit'], input[type='button']"));
                const visible = candidates.find((element) => {
                    const text = ((element.innerText || element.value || element.getAttribute('aria-label') || '') + '').toLowerCase();
                    return element.offsetParent !== null && (
                        text.includes('submit') ||
                        text.includes('login') ||
                        text.includes('log in') ||
                        text.includes('sign in')
                    );
                });
                if (!visible) {
                    return false;
                }
                visible.click();
                return true;
            }"""
            ),
            click_timeout_seconds,
            listener_state,
        )
        if clicked_page is not None:
            return clicked_page
    except Exception:
        pass

    try:
        await page.locator("input[type='password']").first.press("Enter")
        await asyncio.sleep(0.8)
        return page
    except Exception:
        pass

    try:
        submitted = await page.evaluate(
            """() => {
                const passwordField = document.querySelector("input[type='password']");
                const form = passwordField ? passwordField.closest("form") : document.querySelector("form");
                if (!form) {
                    return false;
                }
                if (typeof form.requestSubmit === 'function') {
                    form.requestSubmit();
                    return true;
                }
                if (typeof form.submit === 'function') {
                    form.submit();
                    return true;
                }
                return false;
            }"""
        )
        if submitted:
            await asyncio.sleep(0.8)
            return page
    except Exception:
        pass
    return None


def extract_login_credentials_from_text(text: str) -> dict:
    credentials: dict = {}
    normalized = re.sub(r"[ \t]+", " ", text)
    lines = [re.sub(r"\s+", " ", line).strip() for line in normalized.splitlines() if line.strip()]
    candidate_text = "\n".join(
        line for line in lines
        if any(keyword in line.lower() for keyword in ["username", "email", "password", "credential", "login"])
    ) or normalized

    email_match = re.search(
        r"(?:email|e-mail)\s*(?::|is|=)?\s*([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})",
        candidate_text,
        re.IGNORECASE,
    )
    if email_match:
        credentials["email"] = email_match.group(1).strip()

    username_match = re.search(
        r"(?:username|user\s*name|user id|userid)\s*(?::|is|=)?\s*([A-Z0-9._-]+)",
        candidate_text,
        re.IGNORECASE,
    )
    if username_match:
        candidate = username_match.group(1).strip()
        if candidate.lower() not in {"username", "user", "email", "login"}:
            credentials["username"] = candidate

    password_match = re.search(
        r"(?:password|pass\s*word)\s*(?::|is|=)?\s*([^\s,;]+)",
        candidate_text,
        re.IGNORECASE,
    )
    if password_match:
        candidate = password_match.group(1).strip()
        if candidate.lower() not in {"password", "pass", "login"}:
            credentials["password"] = candidate

    return credentials


async def discover_site_login_credentials(page: Page) -> dict:
    try:
        body_text = await page.locator("body").inner_text(timeout=5000)
    except Exception:
        return {}
    return extract_login_credentials_from_text(body_text)


async def resolve_login_credentials(page: Page, metadata: dict, instructions: List[str]) -> dict:
    resolved = dict(metadata)
    if has_login_credentials(resolved):
        return resolved
    if not is_login_intent(instructions, metadata):
        return resolved

    discovered = await discover_site_login_credentials(page)
    for key in ["username", "email", "password"]:
        if discovered.get(key) and not resolved.get(key):
            resolved[key] = discovered[key]
    return resolved


async def ensure_authenticated_for_target(
    pom_page,
    target_url: str,
    metadata: dict,
    instructions: List[str],
    click_timeout_seconds: int,
    timeout_ms: int,
    listener_state: Optional[dict] = None,
) -> Tuple[dict, bool]:
    resolved_credentials = await resolve_login_credentials(pom_page.page, metadata, instructions)
    if not has_login_credentials(resolved_credentials):
        return resolved_credentials, False

    site_memory = load_site_memory_for_url(target_url)
    known_authenticated_urls = {
        normalize_crawl_url(str(item).strip()).rstrip("/")
        for item in site_memory.get("authenticated_page_urls", [])
        if str(item).strip()
    }
    normalized_target = normalize_crawl_url(target_url).rstrip("/")
    should_attempt_login = await is_auth_form_visible(pom_page.page) or normalized_target in known_authenticated_urls
    auth_intent_case = any(
        normalize_instruction(step).startswith(("fill username with", "fill email with", "fill password with", "submit auth form"))
        or normalize_instruction(step) in {"verify authenticated state", "verify auth form is visible"}
        for step in instructions
    )
    if auth_intent_case:
        return resolved_credentials, False
    if not should_attempt_login:
        return resolved_credentials, False

    if await is_auth_form_visible(pom_page.page):
        await fill_login_form(pom_page.page, resolved_credentials)
        pom_page.page = await attempt_form_submission(pom_page.page, click_timeout_seconds, listener_state)
        await wait_for_runtime_page_ready(pom_page.page, timeout_ms)

    if normalize_crawl_url(str(pom_page.page.url or "")).rstrip("/") != normalized_target:
        try:
            await pom_page.goto(target_url, timeout_ms)
        except Exception:
            pass
    return resolved_credentials, True


async def fill_login_form(page: Page, credentials: dict) -> bool:
    if not has_login_credentials(credentials):
        return False

    identifier_value = login_identifier_value(credentials)
    identifier_key = login_identifier_key(credentials)
    identifier_selectors = [
        "input[name*=username]",
        "input[id*=username]",
        "input[name*=user]",
        "input[id*=user]",
        "input[name*=email]",
        "input[id*=email]",
        "input[placeholder*=user]",
        "input[placeholder*=email]",
        "input[type=email]",
        "input[type=text]",
    ]
    password_selectors = [
        "input[type=password]",
        "input[name*=password]",
        "input[id*=password]",
        "input[placeholder*=password]",
    ]

    filled_identifier = await fill_first_matching_field(page, identifier_selectors, identifier_value)
    if not filled_identifier:
        filled_identifier = await safe_fill(page, identifier_key, identifier_value)
    if not filled_identifier and identifier_key != "username":
        filled_identifier = await safe_fill(page, "username", identifier_value)
    if not filled_identifier and identifier_key != "email":
        filled_identifier = await safe_fill(page, "email", identifier_value)

    filled_password = await fill_first_matching_field(page, password_selectors, credentials["password"])
    if not filled_password:
        filled_password = await safe_fill(page, "password", credentials["password"])

    return filled_identifier or filled_password


async def install_single_tab_guard(context) -> None:
    await context.add_init_script(SINGLE_TAB_GUARD_SCRIPT)


async def enforce_single_tab_on_page(page: Page) -> None:
    try:
        await page.evaluate(SINGLE_TAB_GUARD_SCRIPT)
    except Exception:
        pass


async def collapse_popup_into_opener(popup_page: Page) -> None:
    try:
        opener = await popup_page.opener()
    except Exception:
        opener = None
    if opener is None or opener.is_closed():
        return

    try:
        await popup_page.wait_for_load_state("domcontentloaded", timeout=4000)
    except Exception:
        pass

    popup_url = ""
    try:
        popup_url = str(popup_page.url or "").strip()
    except Exception:
        popup_url = ""

    if popup_url and popup_url not in {"about:blank", "chrome-error://chromewebdata/"}:
        try:
            await opener.goto(popup_url, wait_until="domcontentloaded", timeout=10000)
            await enforce_single_tab_on_page(opener)
            await wait_for_runtime_page_ready(opener, 10000)
        except Exception:
            pass

    try:
        if not popup_page.is_closed():
            await popup_page.close()
    except Exception:
        pass


async def install_popup_collapse_handler(context) -> None:
    def handle_page(page: Page) -> None:
        asyncio.create_task(collapse_popup_into_opener(page))

    context.on("page", handle_page)


class POMPage:
    def __init__(self, page: Page, dom_dir: Path):
        self.page = page
        self.dom_dir = dom_dir

    async def goto(self, url: str, timeout_ms: int) -> None:
        await self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        await enforce_single_tab_on_page(self.page)
        await wait_for_runtime_page_ready(self.page, timeout_ms)
        await self.capture_dom("home")

    async def capture_dom(self, name: str) -> str:
        return await capture_runtime_dom_snapshot(self.page, name)

    async def screenshot(self, name: str, failed: bool = False) -> str:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        FAILURE_SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        filename = SCREENSHOT_DIR / f"{datetime.now():%Y%m%d_%H%M%S_%f}_{slugify(name)}{'_FAIL' if failed else '_PASS'}.png"
        await self.page.screenshot(path=filename, full_page=True)
        if failed:
            failure_copy = FAILURE_SCREENSHOT_DIR / filename.name
            shutil.copyfile(filename, failure_copy)
        return str(filename.relative_to(WORKSPACE_ROOT))


async def capture_runtime_dom_snapshot(page: Page, name: str) -> str:
    content = await page.content()
    file_path = DOM_DIR / f"{datetime.now():%Y%m%d_%H%M%S_%f}_{slugify(name)}.html"
    file_path.write_text(content, encoding="utf-8")
    dom_helper.save_dom_snapshot(name, content)
    return str(file_path.relative_to(WORKSPACE_ROOT))


async def wait_for_runtime_page_ready(page: Page, timeout_ms: int) -> None:
    try:
        await page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
    except Exception:
        pass
    try:
        await page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 5000))
    except Exception:
        pass


def normalize_crawl_url(url: str) -> str:
    parsed = urlparse(url)
    normalized_path = parsed.path or "/"
    normalized = parsed._replace(fragment="", path=normalized_path)
    return urlunparse(normalized)


async def expand_discovery_surface(page: Page, timeout_ms: int) -> None:
    try:
        await page.evaluate(
            """({ expandKeywords, skipKeywords }) => {
                const isVisible = (element) => {
                    if (!element) return false;
                    const style = window.getComputedStyle(element);
                    if (style.visibility === 'hidden' || style.display === 'none') return false;
                    const rect = element.getBoundingClientRect();
                    return rect.width > 0 && rect.height > 0;
                };

                const shouldSkip = (element) => {
                    const text = ((element.innerText || element.textContent || element.getAttribute('aria-label') || '') + '')
                        .trim()
                        .toLowerCase();
                    return skipKeywords.some((keyword) => text.includes(keyword));
                };

                const candidates = Array.from(document.querySelectorAll(
                    "button, [role='button'], summary, [aria-expanded='false'], [aria-haspopup='true'], .menu-toggle, .navbar-toggler, .hamburger"
                ));
                let clicked = 0;

                for (const element of candidates) {
                    if (clicked >= 12) break;
                    if (!isVisible(element) || shouldSkip(element) || element.disabled) continue;
                    const text = ((element.innerText || element.textContent || element.getAttribute('aria-label') || '') + '')
                        .trim()
                        .toLowerCase();
                    const explicitlyExpandable =
                        element.tagName.toLowerCase() === 'summary' ||
                        element.getAttribute('aria-expanded') === 'false' ||
                        element.hasAttribute('aria-controls') ||
                        element.hasAttribute('aria-haspopup');
                    const keywordMatch = expandKeywords.some((keyword) => text.includes(keyword));
                    if (!explicitlyExpandable && !keywordMatch) continue;
                    try {
                        element.click();
                        clicked += 1;
                    } catch (error) {
                        // Best-effort expansion only.
                    }
                }
            }""",
            {"expandKeywords": list(DISCOVERY_EXPAND_KEYWORDS), "skipKeywords": list(DISCOVERY_SKIP_CLICK_KEYWORDS)},
        )
        await page.wait_for_timeout(800)
        try:
            await page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 5000))
        except Exception:
            pass
    except Exception:
        pass


async def collect_page_inventory(page: Page) -> dict:
    return await page.evaluate(
        """() => {
            const isVisible = (element) => {
                if (!element) return false;
                const style = window.getComputedStyle(element);
                if (style.visibility === 'hidden' || style.display === 'none') return false;
                const rect = element.getBoundingClientRect();
                return rect.width > 0 && rect.height > 0;
            };
            const areaFor = (element) => {
                if (!element || !element.closest) return 'body';
                if (element.closest('header, [role="banner"], .header, .site-header')) return 'header';
                if (element.closest('nav, [role="navigation"], .main-menu, .menu')) return 'navigation';
                if (element.closest('main, [role="main"]')) return 'main';
                if (element.closest('footer')) return 'footer';
                return 'body';
            };
            const labelFor = (element) => {
                if (!element) return '';
                const clean = (value) => (value || '').trim().replace(/\\s+/g, ' ').slice(0, 120);
                const ariaLabel = clean(element.getAttribute && element.getAttribute('aria-label'));
                if (ariaLabel) return ariaLabel;
                const placeholder = clean(element.getAttribute && element.getAttribute('placeholder'));
                if (placeholder) return placeholder;
                if (element.id) {
                    try {
                        const explicitLabel = document.querySelector(`label[for="${element.id.replace(/"/g, '\\"')}"]`);
                        const labelText = clean(explicitLabel && (explicitLabel.innerText || explicitLabel.textContent));
                        if (labelText) return labelText;
                    } catch (error) {
                        // Fall back to nearby text.
                    }
                }
                const parentLabel = element.closest && element.closest('label');
                const parentLabelText = clean(parentLabel && (parentLabel.innerText || parentLabel.textContent));
                if (parentLabelText) return parentLabelText;
                return clean(element.value || element.getAttribute('name') || element.id || element.type || element.tagName);
            };
            const links = Array.from(document.querySelectorAll('a'))
                .filter((link) => isVisible(link))
                .map((link, index) => ({
                    text: (link.innerText || link.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 120),
                    href: link.href || '',
                    selector: `a:nth-of-type(${index + 1})`,
                    area: areaFor(link)
                }))
                .filter(link => link.text || link.href);
            const buttons = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"]'))
                .filter((button) => isVisible(button))
                .map((button, index) => ({
                    text: (button.innerText || button.value || button.getAttribute('aria-label') || '').trim().replace(/\\s+/g, ' ').slice(0, 120),
                    selector: button.id ? `#${button.id}` : `${button.tagName.toLowerCase()}:nth-of-type(${index + 1})`,
                    area: areaFor(button)
                }))
                .filter(button => button.text || button.selector);
            const inputs = Array.from(document.querySelectorAll('input, textarea, select'))
                .filter((input) => isVisible(input))
                .map((input, index) => ({
                    name: input.getAttribute('name') || '',
                    id: input.getAttribute('id') || '',
                    label: labelFor(input),
                    placeholder: input.getAttribute('placeholder') || '',
                    type: input.getAttribute('type') || input.tagName.toLowerCase(),
                    value: (input.value || '').toString().trim().slice(0, 120),
                    selector: input.id ? `#${input.id}` : `${input.tagName.toLowerCase()}:nth-of-type(${index + 1})`,
                    area: areaFor(input),
                    options: input.tagName.toLowerCase() === 'select'
                        ? Array.from(input.options || [])
                            .map((option) => ({
                                label: (option.label || option.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 80),
                                value: (option.value || '').trim().slice(0, 80)
                            }))
                            .filter((option) => option.label || option.value)
                            .slice(0, 30)
                        : []
                }));
            const headings = Array.from(document.querySelectorAll('h1, h2, h3'))
                .map((heading) => (heading.innerText || heading.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 120))
                .filter(Boolean)
                .slice(0, 8);
            const textPreview = ((document.body && document.body.innerText) || '')
                .trim()
                .replace(/\\s+/g, ' ')
                .slice(0, 280);
            return {
                title: document.title || '',
                url: window.location.href,
                links,
                buttons,
                inputs,
                headings,
                text_preview: textPreview
            };
        }"""
    )


def should_capture_discovery_dom(url: str, captured_urls: Set[str], limit: int) -> bool:
    if len(captured_urls) >= limit:
        return False
    normalized = normalize_crawl_url(url)
    if normalized in captured_urls:
        return False
    captured_urls.add(normalized)
    return True


def extract_candidate_urls_from_inventory(
    inventory: dict,
    current_url: str,
    same_host: str,
    limit: int = 18,
) -> List[str]:
    ranked_links = sorted(
        list(inventory.get("links", [])),
        key=lambda link: (
            {"header": 0, "navigation": 1, "main": 2, "body": 3, "footer": 4}.get(str(link.get("area") or "").lower(), 5),
            str(link.get("text") or link.get("href") or "").lower(),
        ),
    )
    candidates: List[str] = []
    seen: Set[str] = set()
    for link in ranked_links:
        href = str(link.get("href") or "").strip()
        label = str(link.get("text") or href).strip()
        if not href or is_noise_link_target(href, current_url) or is_low_value_link_action(label, href, current_url):
            continue
        full_url = normalize_crawl_url(urljoin(current_url, href))
        parsed = urlparse(full_url)
        if parsed.scheme not in {"http", "https"} or parsed.netloc != same_host:
            continue
        if full_url in seen:
            continue
        seen.add(full_url)
        candidates.append(full_url)
        if len(candidates) >= limit:
            break
    return candidates


async def inspect_page_for_discovery(
    page: Page,
    target_url: str,
    timeout_ms: int,
    discovery_dom_urls: Set[str],
) -> dict:
    await page.goto(target_url, wait_until="domcontentloaded", timeout=timeout_ms)
    await wait_for_runtime_page_ready(page, timeout_ms)
    await expand_discovery_surface(page, timeout_ms)
    inventory = await collect_page_inventory(page)
    inventory["discovered_at"] = datetime.now().isoformat()
    if should_capture_discovery_dom(target_url, discovery_dom_urls, MAX_DISCOVERY_DOM_SNAPSHOTS):
        try:
            content = await page.content()
            dom_helper.save_dom_snapshot(slugify(target_url), content)
        except Exception:
            pass
    return inventory


async def explore_site_inventory(
    context,
    seed_urls: List[str],
    timeout_ms: int,
    max_pages: int,
    time_budget_seconds: int,
    same_host: str,
    worker_count: int,
) -> List[dict]:
    queue: asyncio.Queue[str] = asyncio.Queue()
    enqueued: Set[str] = set()
    visited: Set[str] = set()
    discovery_dom_urls: Set[str] = set()
    pages: List[dict] = []
    state_lock = asyncio.Lock()

    async def enqueue_url(candidate_url: str) -> None:
        normalized = normalize_crawl_url(candidate_url)
        parsed = urlparse(normalized)
        if parsed.scheme not in {"http", "https"} or parsed.netloc != same_host:
            return
        async with state_lock:
            if normalized in enqueued or len(enqueued) >= max_pages * 3:
                return
            enqueued.add(normalized)
        await queue.put(normalized)

    for seed in seed_urls:
        if seed:
            await enqueue_url(seed)

    async def worker(worker_index: int) -> None:
        page = await context.new_page()
        try:
            while True:
                try:
                    current_url = await asyncio.wait_for(queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    if queue.empty():
                        return
                    continue

                try:
                    async with state_lock:
                        if current_url in visited or len(visited) >= max_pages:
                            continue
                        visited.add(current_url)

                    inventory = await inspect_page_for_discovery(page, current_url, timeout_ms, discovery_dom_urls)
                    inventory["inventory_source"] = "timed_parallel_discovery"
                    inventory["discovery_state"] = f"worker_{worker_index}"
                    async with state_lock:
                        pages.append(inventory)

                    for candidate in extract_candidate_urls_from_inventory(inventory, current_url, same_host):
                        await enqueue_url(candidate)
                except Exception as exc:
                    async with state_lock:
                        pages.append({
                            "url": current_url,
                            "title": "Discovery failed",
                            "links": [],
                            "buttons": [],
                            "inputs": [],
                            "headings": [],
                            "text_preview": "",
                            "error": str(exc),
                            "inventory_source": "timed_parallel_discovery",
                            "discovery_state": f"worker_{worker_index}_error",
                            "discovered_at": datetime.now().isoformat(),
                        })
                finally:
                    queue.task_done()
        finally:
            if not page.is_closed():
                await page.close()

    worker_count = max(1, min(worker_count, max_pages, len(seed_urls) or worker_count))
    workers = [asyncio.create_task(worker(index + 1)) for index in range(worker_count)]
    try:
        await asyncio.wait_for(queue.join(), timeout=max(1, time_budget_seconds))
    except asyncio.TimeoutError:
        print(f"Exploration reached the strict time box of {time_budget_seconds} seconds. Proceeding with discovered context.")
    finally:
        for task in workers:
            task.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

    return merge_discovered_pages(pages)


async def explore_authenticated_inventory(
    context,
    start_url: str,
    timeout_ms: int,
    max_pages: int,
    time_budget_seconds: int,
    metadata: dict,
    instructions: List[str],
    public_pages: List[dict],
    worker_count: int,
) -> List[dict]:
    auth_signals_present = is_login_intent(instructions, metadata) or any(page_has_auth_form_signal(page) for page in public_pages)
    if not auth_signals_present or not has_login_credentials(metadata):
        return []

    auth_page = await context.new_page()
    try:
        auth_page_url = start_url
        for public_page in public_pages:
            if page_has_auth_form_signal(public_page):
                auth_page_url = str(public_page.get("url") or start_url)
                break

        await auth_page.goto(auth_page_url, wait_until="domcontentloaded", timeout=timeout_ms)
        await wait_for_runtime_page_ready(auth_page, timeout_ms)
        auth_form_inventory = await collect_page_inventory(auth_page)
        auth_form_inventory["inventory_source"] = "authenticated_discovery"
        auth_form_inventory["discovery_state"] = "before_login"
        auth_form_inventory["discovered_at"] = datetime.now().isoformat()
        try:
            await capture_runtime_dom_snapshot(auth_page, "auth_form_before_login")
        except Exception:
            pass
        await fill_login_form(auth_page, metadata)
        submitted_page = await attempt_form_submission(auth_page, DEFAULT_CLICK_TIMEOUT_SECONDS)
        if submitted_page is not None:
            auth_page = submitted_page
        await wait_for_runtime_page_ready(auth_page, timeout_ms)
        if not await page_looks_authenticated(auth_page):
            return [{
                "url": auth_page_url,
                "title": "Authenticated discovery failed",
                "links": [],
                "buttons": [],
                "inputs": [],
                "headings": [],
                "text_preview": "",
                "error": "Authentication did not complete successfully.",
                "inventory_source": "authenticated_discovery",
                "discovery_state": "authentication_failed",
                "discovered_at": datetime.now().isoformat(),
            }]

        live_inventory = await collect_page_inventory(auth_page)
        live_inventory["inventory_source"] = "authenticated_discovery"
        live_inventory["discovery_state"] = "authenticated_seed"
        live_inventory["discovered_at"] = datetime.now().isoformat()
        authenticated_parent_url = str(auth_page.url or auth_page_url)
        try:
            await capture_runtime_dom_snapshot(auth_page, "authenticated_state_after_login")
        except Exception:
            pass
        child_seed_urls = extract_candidate_urls_from_inventory(
            live_inventory,
            authenticated_parent_url,
            urlparse(start_url).netloc,
            limit=10,
        )
        immediate_child_pages: List[dict] = []
        for child_url in child_seed_urls[:3]:
            try:
                await auth_page.goto(child_url, wait_until="domcontentloaded", timeout=timeout_ms)
                await wait_for_runtime_page_ready(auth_page, timeout_ms)
                child_inventory = await collect_page_inventory(auth_page)
                child_inventory["inventory_source"] = "authenticated_discovery"
                child_inventory["discovery_state"] = "post_login_child"
                child_inventory["discovered_at"] = datetime.now().isoformat()
                immediate_child_pages.append(child_inventory)
            except Exception:
                continue
        try:
            await auth_page.goto(authenticated_parent_url, wait_until="domcontentloaded", timeout=timeout_ms)
            await wait_for_runtime_page_ready(auth_page, timeout_ms)
        except Exception:
            pass
        seed_urls = [authenticated_parent_url] + child_seed_urls

        discovered_pages = await explore_site_inventory(
            context,
            seed_urls=seed_urls,
            timeout_ms=timeout_ms,
            max_pages=max(3, min(max_pages, 8)),
            time_budget_seconds=max(30, time_budget_seconds),
            same_host=urlparse(start_url).netloc,
            worker_count=worker_count,
        )

        logout_target = None
        for page_data in [live_inventory] + discovered_pages:
            logout_target = find_logout_target(page_data)
            if logout_target:
                break
        if logout_target:
            logout_page = await timed_click(auth_page, logout_target, DEFAULT_CLICK_TIMEOUT_SECONDS)
            if logout_page is not None:
                auth_page = logout_page
                await wait_for_runtime_page_ready(auth_page, timeout_ms)
                logout_inventory = await collect_page_inventory(auth_page)
                logout_inventory["inventory_source"] = "authenticated_discovery"
                logout_inventory["discovery_state"] = "after_logout"
                logout_inventory["discovered_at"] = datetime.now().isoformat()
                discovered_pages.append(logout_inventory)

        memory = load_action_memory()
        key = memory_key_for_url(start_url)
        memory_entry = memory.get(key, {})
        memory_entry["login_page_url"] = auth_page_url
        memory_entry["authenticated_page_urls"] = [page_data.get("url", "") for page_data in discovered_pages if page_data.get("url")]
        if logout_target:
            memory_entry["logout_target"] = logout_target
        memory[key] = memory_entry
        save_action_memory(memory)
        return merge_discovered_pages([auth_form_inventory, live_inventory], immediate_child_pages, discovered_pages)
    finally:
        if not auth_page.is_closed():
            await auth_page.close()


async def run_timed_exploration(
    context,
    url: str,
    timeout_ms: int,
    max_pages: int,
    metadata: dict,
    instructions: List[str],
    exploration_time_limit_seconds: int,
    worker_count: int,
) -> List[dict]:
    auth_budget = min(AUTH_EXPLORATION_BUDGET_SECONDS, max(30, exploration_time_limit_seconds // 3))
    public_budget = max(60, exploration_time_limit_seconds - auth_budget)
    public_pages = await explore_site_inventory(
        context,
        seed_urls=[url],
        timeout_ms=timeout_ms,
        max_pages=max_pages,
        time_budget_seconds=public_budget,
        same_host=urlparse(url).netloc,
        worker_count=worker_count,
    )
    authenticated_pages = await explore_authenticated_inventory(
        context,
        start_url=url,
        timeout_ms=timeout_ms,
        max_pages=max_pages,
        time_budget_seconds=auth_budget,
        metadata=metadata,
        instructions=instructions,
        public_pages=public_pages,
        worker_count=worker_count,
    )
    return merge_discovered_pages(public_pages, authenticated_pages)


def merge_discovered_pages(*page_groups: List[dict]) -> List[dict]:
    merged: List[dict] = []
    index_by_key: Dict[Tuple[str, str], int] = {}
    for group in page_groups:
        for page in group:
            if not isinstance(page, dict):
                continue
            key = (
                str(page.get("url", "")).strip().lower(),
                str(page.get("title", "")).strip().lower(),
            )
            if key in index_by_key:
                merged[index_by_key[key]] = merge_page_records(merged[index_by_key[key]], page)
                continue
            index_by_key[key] = len(merged)
            merged.append(dict(page))
    return merged


async def crawl_page_graph(page: Page, seed_urls: List[str], timeout_ms: int, max_pages: int, same_host: str) -> List[dict]:
    queue: List[str] = [normalize_crawl_url(url) for url in seed_urls if url]
    visited: Set[str] = set()
    pages: List[dict] = []

    while queue and len(visited) < max_pages:
        current = normalize_crawl_url(queue.pop(0))
        if current in visited:
            continue
        visited.add(current)
        try:
            await page.goto(current, wait_until="domcontentloaded", timeout=timeout_ms)
            await page.wait_for_load_state("networkidle", timeout=timeout_ms)
            await expand_discovery_surface(page, timeout_ms)
            content = await page.content()
            dom_helper.save_dom_snapshot(slugify(current), content)
            inventory = await collect_page_inventory(page)
            select_explorations = await explore_select_options_for_page(page, current, timeout_ms, inventory)
            if select_explorations:
                inventory["select_explorations"] = select_explorations
                inventory["explored_select_option_count"] = sum(1 for item in select_explorations if item.get("selected"))
            inventory["discovered_at"] = datetime.now().isoformat()
            pages.append(inventory)

            for link in inventory.get("links", []):
                href = link.get("href") or ""
                if not href:
                    continue
                full_url = normalize_crawl_url(urljoin(current, href))
                parsed = urlparse(full_url)
                if parsed.scheme not in {"http", "https"}:
                    continue
                if parsed.netloc != same_host:
                    continue
                if full_url not in visited and full_url not in queue and len(queue) + len(visited) < max_pages * 2:
                    queue.append(full_url)
        except Exception as exc:
            pages.append({
                "url": current,
                "title": "Discovery failed",
                "links": [],
                "buttons": [],
                "inputs": [],
                "error": str(exc),
                "discovered_at": datetime.now().isoformat(),
            })

    return pages


async def discover_pages_and_dom(page: Page, start_url: str, timeout_ms: int, max_pages: int) -> List[dict]:
    parsed_start = urlparse(start_url)
    same_host = parsed_start.netloc
    pages = await crawl_page_graph(page, [start_url], timeout_ms, max_pages, same_host)

    DOM_DIR.mkdir(parents=True, exist_ok=True)
    inventory_path = DOM_DIR / "dom_inventory.json"
    inventory_path.write_text(json.dumps(pages, indent=2), encoding="utf-8")
    return pages


async def discover_authenticated_pages(
    page: Page,
    start_url: str,
    timeout_ms: int,
    max_pages: int,
    metadata: dict,
    instructions: List[str],
    public_pages: List[dict],
) -> List[dict]:
    if not is_login_intent(instructions, metadata):
        return []

    credentials = await resolve_login_credentials(page, metadata, instructions)
    if not has_login_credentials(credentials):
        return []

    auth_page_url = start_url
    for public_page in public_pages:
        if page_has_auth_form_signal(public_page):
            auth_page_url = public_page.get("url") or start_url
            break

    try:
        await page.goto(auth_page_url, wait_until="domcontentloaded", timeout=timeout_ms)
        await page.wait_for_load_state("networkidle", timeout=timeout_ms)
        await fill_login_form(page, credentials)
        page = await attempt_form_submission(page, DEFAULT_CLICK_TIMEOUT_SECONDS)
        await page.wait_for_load_state("networkidle", timeout=timeout_ms)
        if not await page_looks_authenticated(page):
            return []

        authenticated_urls = [page.url]
        for link in (await collect_page_inventory(page)).get("links", []):
            href = link.get("href") or ""
            if href:
                authenticated_urls.append(urljoin(page.url, href))

        parsed_start = urlparse(start_url)
        authenticated_pages = await crawl_page_graph(page, authenticated_urls, timeout_ms, max_pages, parsed_start.netloc)

        logout_target = None
        for discovered_page in authenticated_pages:
            logout_target = find_logout_target(discovered_page)
            if logout_target:
                break

        logout_page = None
        if logout_target:
            logout_page = await timed_click(page, logout_target, DEFAULT_CLICK_TIMEOUT_SECONDS)
        if logout_page is not None:
            page = logout_page
            await page.wait_for_load_state("networkidle", timeout=timeout_ms)
            logout_inventory = await collect_page_inventory(page)
            logout_inventory["discovered_at"] = datetime.now().isoformat()
            logout_inventory["discovery_state"] = "after_logout"
            authenticated_pages.append(logout_inventory)

        memory = load_action_memory()
        key = memory_key_for_url(start_url)
        memory_entry = memory.get(key, {})
        memory_entry["login_page_url"] = auth_page_url
        memory_entry["authenticated_page_urls"] = [page_data.get("url", "") for page_data in authenticated_pages if page_data.get("url")]
        if logout_target:
            memory_entry["logout_target"] = logout_target
        memory[key] = memory_entry
        save_action_memory(memory)
        return authenticated_pages
    except Exception as exc:
        return [{
            "url": auth_page_url,
            "title": "Authenticated discovery failed",
            "links": [],
            "buttons": [],
            "inputs": [],
            "error": str(exc),
            "discovered_at": datetime.now().isoformat(),
        }]


def write_playwright_assets(scenario_id: str, url: str, usecases: List[dict]) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    flat_script_path = PLAYWRIGHT_DIR / f"{scenario_id}_{timestamp}_playwright.py"
    (PLAYWRIGHT_PAGES_DIR / "__init__.py").write_text("", encoding="utf-8")
    (PLAYWRIGHT_TESTS_DIR / "__init__.py").write_text("", encoding="utf-8")
    flat_script = f"""import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
USECASES = {json.dumps(usecases, indent=2)}
URL = {url!r}

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        for usecase in USECASES:
            await page.goto(usecase.get("page_url") or URL, wait_until="networkidle")
            screenshot_name = f"{{usecase['title']}}_{{usecase['type']}}".replace(" ", "_").lower()
            await page.screenshot(path=str(WORKSPACE_ROOT / "screenshots" / f"{{screenshot_name}}_sample.png"), full_page=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
"""
    flat_script_path.write_text(flat_script, encoding="utf-8")

    base_page_path = PLAYWRIGHT_PAGES_DIR / "base_page.py"
    if not base_page_path.exists():
        base_page_path.write_text(
            """from pathlib import Path
from playwright.async_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def open(self, url: str, timeout_ms: int = 30000):
        await self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        await self.page.wait_for_load_state("networkidle", timeout=timeout_ms)

    async def screenshot(self, path: Path):
        await self.page.screenshot(path=path, full_page=True)
""",
            encoding="utf-8",
        )

    site_page_path = PLAYWRIGHT_PAGES_DIR / f"{scenario_id}_page.py"
    site_page_path.write_text(
        f"""from .base_page import BasePage

class ScenarioPage(BasePage):
    scenario_id = {scenario_id!r}
    default_url = {url!r}
""",
        encoding="utf-8",
    )

    data_path = PLAYWRIGHT_DATA_DIR / f"{scenario_id}_usecases.json"
    data_path.write_text(json.dumps(usecases, indent=2), encoding="utf-8")

    test_path = PLAYWRIGHT_TESTS_DIR / f"test_{scenario_id}.py"
    test_path.write_text(
        f"""import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from pages.{scenario_id}_page import ScenarioPage

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
USECASE_FILE = WORKSPACE_ROOT / "playwrightfolder" / "data" / "{scenario_id}_usecases.json"

async def main():
    usecases = json.loads(USECASE_FILE.read_text(encoding="utf-8"))
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        pom = ScenarioPage(page)
        for usecase in usecases:
            await pom.open(usecase.get("page_url") or pom.default_url)
            screenshot_name = f"{{usecase['title']}}_{{usecase['type']}}".replace(" ", "_").lower()
            await pom.screenshot(WORKSPACE_ROOT / "screenshots" / f"{{screenshot_name}}_qa.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
""",
        encoding="utf-8",
    )


def build_runtime_report(
    scenario_id: str,
    source_file: Path,
    url: str,
    usecases: List[dict],
    discovered_pages: List[dict],
    results: List[dict],
    site_understanding: Optional[dict] = None,
) -> dict:
    return {
        "scenario_id": scenario_id,
        "source_file": str(source_file),
        "url": url,
        "generated_at": datetime.now().isoformat(),
        "usecase_count": len(usecases),
        "discovered_page_count": len(discovered_pages),
        "summary": summarize_results(results),
        "results": results,
        "discovered_pages": discovered_pages,
        "site_understanding": site_understanding or {},
    }


def write_results(results: List[dict]) -> None:
    summary = summarize_results(results)
    txt_lines = [
        "TEST RESULTS SUMMARY",
        f"PASS: {summary['passed']} | FAIL: {summary['failed']} | TOTAL: {summary['total']}",
        "",
    ]
    md_lines = [
        "# Test Results",
        "",
        f"Generated: {datetime.now().isoformat()}",
        f"PASS: {summary['passed']} | FAIL: {summary['failed']} | TOTAL: {summary['total']}",
        "",
    ]

    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["case_id", "title", "type", "result", "status_detail", "page_url", "error", "screenshot", "duration_seconds"])
        for result in results:
            writer.writerow([
                result.get("case_id", ""),
                result["title"],
                result["type"],
                result["result"],
                result["status_detail"],
                result.get("page_url", ""),
                result["error"],
                result.get("screenshot", ""),
                result.get("duration_seconds", ""),
            ])
            txt_lines.append(
                f"{result.get('case_id', '')} | {result['result']} | {result['title']} | {result['type']} | {result['status_detail']} | {result['error']}"
            )
            md_lines.append(f"## {result.get('case_id', '')} {result['title']}".strip())
            md_lines.append(f"- Type: {result['type']}")
            md_lines.append(f"- Result: {result['result']}")
            md_lines.append(f"- Status Detail: {result['status_detail']}")
            md_lines.append(f"- Page: {result.get('page_url', '')}")
            md_lines.append(f"- Duration Seconds: {result.get('duration_seconds', '')}")
            if result["error"]:
                md_lines.append(f"- Error: {result['error']}")
            md_lines.append(f"- Screenshot: {result.get('screenshot', '')}")
            if result.get("console_errors"):
                md_lines.append(f"- Console Errors: {len(result['console_errors'])}")
            if result.get("network_errors"):
                md_lines.append(f"- Network Errors: {len(result['network_errors'])}")
            md_lines.append("")

    RESULTS_TXT.write_text("\n".join(txt_lines), encoding="utf-8")
    RESULTS_MD.write_text("\n".join(md_lines), encoding="utf-8")
    RESULTS_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")


def write_reports(report_data: dict) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = REPORTS_DIR / f"report_{timestamp}.json"
    html_path = REPORTS_DIR / f"extent_report_{timestamp}.html"

    json_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")

    rows = []
    for result in report_data["results"]:
        result_class = "pass" if result["result"] == "PASS" else "fail"
        rows.append(
            "<tr>"
            f"<td>{result.get('case_id', '')}</td>"
            f"<td>{result['title']}</td>"
            f"<td>{result['type']}</td>"
            f"<td class='{result_class}'>{result['result']}</td>"
            f"<td>{result['status_detail']}</td>"
            f"<td>{result.get('page_url', '')}</td>"
            f"<td>{result.get('duration_seconds', '')}</td>"
            f"<td>{result.get('error', '')}</td>"
            "</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Agentic-QA Extent Report</title>
  <style>
    :root {{
      --bg: #f4efe6;
      --card: #fffaf2;
      --ink: #1e2430;
      --accent: #c65d2f;
      --pass: #2f855a;
      --warn: #b7791f;
      --fail: #c53030;
      --border: #e6d6bf;
    }}
    body {{ font-family: Georgia, 'Trebuchet MS', serif; background: linear-gradient(135deg, #f7f1e3, #efe4cf); color: var(--ink); margin: 0; padding: 24px; }}
    .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 24px; box-shadow: 0 18px 40px rgba(64, 52, 35, 0.08); }}
    h1, h2 {{ margin-top: 0; }}
    .meta {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 24px; }}
    .pill {{ padding: 12px 14px; border-radius: 14px; background: #fff; border: 1px solid var(--border); }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 16px; overflow: hidden; }}
    th, td {{ padding: 12px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }}
    th {{ background: #f8ebd6; }}
    .pass {{ color: var(--pass); font-weight: 700; }}
    .fail {{ color: var(--fail); font-weight: 700; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Agentic-QA Extent Report</h1>
    <div class="meta">
      <div class="pill"><strong>Scenario:</strong> {report_data['scenario_id']}</div>
      <div class="pill"><strong>Source:</strong> {report_data['source_file']}</div>
      <div class="pill"><strong>URL:</strong> {report_data['url']}</div>
      <div class="pill"><strong>Generated:</strong> {report_data['generated_at']}</div>
      <div class="pill"><strong>Use Cases:</strong> {report_data['usecase_count']}</div>
      <div class="pill"><strong>Discovered Pages:</strong> {report_data['discovered_page_count']}</div>
      <div class="pill"><strong>PASS:</strong> {report_data['summary']['passed']} | <strong>FAIL:</strong> {report_data['summary']['failed']} | <strong>TOTAL:</strong> {report_data['summary']['total']}</div>
    </div>
    <h2>Execution Summary</h2>
    <table>
      <thead>
        <tr>
          <th>Case ID</th>
          <th>Title</th>
          <th>Type</th>
          <th>Result</th>
          <th>Status Detail</th>
          <th>Page URL</th>
          <th>Duration Seconds</th>
          <th>Error</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
  </div>
</body>
</html>"""
    html_path.write_text(html, encoding="utf-8")


def load_playwright_config() -> dict:
    default = {
        "browser": "chromium",
        "headless": False,
        "timeout": 30000,
        "slow_mo": 250,
        "click_timeout_seconds": DEFAULT_CLICK_TIMEOUT_SECONDS,
        "max_discovery_pages": DEFAULT_PAGE_DISCOVERY_LIMIT,
        "exploration_time_limit_seconds": EXPLORATION_TIME_LIMIT_SECONDS,
        "exploration_workers": EXPLORATION_WORKER_COUNT,
    }
    if CONFIG_FILE.exists():
        try:
            loaded = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            default.update(loaded)
        except Exception:
            pass
    return default


def clear_run_artifacts() -> None:
    for path in [
        RESULTS_DIR,
        REPORTS_DIR,
        SCREENSHOT_DIR,
        FAILURE_SCREENSHOT_DIR,
        DOM_DIR,
        USECASES_DIR,
        PLAYWRIGHT_DIR,
        PLAYWRIGHT_DATA_DIR,
        PLAYWRIGHT_TESTS_DIR,
        PLAYWRIGHT_PAGES_DIR,
    ]:
        if path.exists():
            for item in path.glob("*"):
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        path.mkdir(parents=True, exist_ok=True)

    for old_file in [WORKSPACE_ROOT / "dom" / "latest_dom.txt", WORKSPACE_ROOT / "dom" / "latest_dom.py"]:
        if old_file.exists():
            old_file.unlink()

    if SCENARIO_STORE_FILE.exists():
        SCENARIO_STORE_FILE.unlink()


def parse_cli_args():
    parser = argparse.ArgumentParser(description="Run the agentic QA automation framework.")
    parser.add_argument("--file", "-f", dest="doc_path", help="Path to a .pdf, .md, .txt, .docx, or .csv scenario file.")
    parser.add_argument("--scenario", "-s", dest="scenario_text", help="Paste the scenario text directly.")
    parser.add_argument("--approve", action="store_true", help="Automatically approve generated use cases and continue execution.")
    parser.add_argument("--teach", action="store_true", help="Open a manual exploration session and learn interaction patterns from your clicks and form changes.")
    parser.add_argument("--regenerate", action="store_true", help="Retained for CLI compatibility. Fresh generated outputs are written on every run.")
    return parser.parse_args()


def parse_fill_instruction(instruction: str) -> Optional[Tuple[str, str]]:
    match = re.match(r"(?:fill|enter)\s+(.+?)\s+with\s+(.+)", instruction, re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip(), match.group(2).strip()


def parse_select_instruction(instruction: str) -> Optional[Tuple[str, str]]:
    match = re.match(r"select\s+(.+?)\s+option\s+(.+)", instruction, re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip(), match.group(2).strip()


async def attach_runtime_listeners(page: Page) -> dict:
    listener_state = {"bucket": None, "bound_pages": set()}
    await bind_runtime_listeners(page, listener_state)
    return listener_state


async def attach_teach_mode_recording(context, recorded_events: Optional[List[dict]] = None) -> None:
    script = """(() => {
            if (window.__agenticQaTeachInstalled) {
                return;
            }
            window.__agenticQaTeachInstalled = true;
            const storageKey = %s;

            const selectorFor = (element) => {
                if (!element || !element.tagName) return '';
                if (element.id) return `#${element.id}`;
                const name = element.getAttribute && element.getAttribute('name');
                if (name) return `${element.tagName.toLowerCase()}[name="${name}"]`;
                const role = element.getAttribute && element.getAttribute('role');
                if (role) return `${element.tagName.toLowerCase()}[role="${role}"]`;
                return element.tagName.toLowerCase();
            };

            const labelFor = (element) => {
                if (!element) return '';
                return (
                    element.innerText ||
                    element.textContent ||
                    element.value ||
                    element.getAttribute('aria-label') ||
                    element.getAttribute('placeholder') ||
                    element.getAttribute('name') ||
                    ''
                ).trim().replace(/\\s+/g, ' ').slice(0, 160);
            };

            const sendEvent = (payload) => {
                try {
                    const previous = JSON.parse(localStorage.getItem(storageKey) || '[]');
                    previous.push(payload);
                    localStorage.setItem(storageKey, JSON.stringify(previous.slice(-%d)));
                } catch (error) {
                    // Best-effort recording only.
                }
            };

            document.addEventListener('click', (event) => {
                const element = event.target && event.target.closest
                    ? event.target.closest('a, button, [role="button"], input[type="submit"], input[type="button"]')
                    : null;
                if (!element) return;
                sendEvent({
                    action: 'click',
                    url: window.location.href,
                    title: document.title || '',
                    selector: selectorFor(element),
                    label: labelFor(element),
                    href: element.href || element.getAttribute('href') || '',
                    value: ''
                });
            }, true);

            document.addEventListener('change', (event) => {
                const element = event.target;
                if (!element || !element.tagName) return;
                const tagName = element.tagName.toLowerCase();
                if (!['input', 'textarea', 'select'].includes(tagName)) return;
                const action = tagName === 'select' ? 'change' : 'fill';
                sendEvent({
                    action,
                    url: window.location.href,
                    title: document.title || '',
                    selector: selectorFor(element),
                    label: labelFor(element),
                    href: '',
                    value: (element.value || '').toString().slice(0, 200)
                });
            }, true);
        })();""" % (json.dumps(TEACH_STORAGE_KEY), MAX_MANUAL_PATTERN_EVENTS)
    await context.add_init_script(
        script
    )


def summarize_recorded_patterns(events: List[dict], limit: int = 12) -> List[str]:
    lines: List[str] = []
    for event in events[:limit]:
        action = str(event.get("action", "")).strip() or "event"
        label = str(event.get("label", "")).strip() or str(event.get("selector", "")).strip() or "unknown"
        url = str(event.get("url", "")).strip()
        value = str(event.get("value", "")).strip()
        if value:
            lines.append(f"{action}: {label} -> {value} ({url})")
        else:
            lines.append(f"{action}: {label} ({url})")
    return lines


async def harvest_teach_mode_events(context) -> List[dict]:
    harvested: List[dict] = []
    for page in context.pages:
        if page.is_closed():
            continue
        try:
            page_events = await page.evaluate(
                """(storageKey) => {
                    try {
                        return JSON.parse(localStorage.getItem(storageKey) || '[]');
                    } catch (error) {
                        return [];
                    }
                }""",
                TEACH_STORAGE_KEY,
            )
        except Exception:
            continue
        if isinstance(page_events, list):
            harvested.extend(page_events)
    return harvested


def format_result_label(status: str) -> str:
    return "PASS" if status == "passed" else "FAIL"


def summarize_results(results: List[dict]) -> dict:
    passed = sum(1 for result in results if result.get("result") == "PASS")
    failed = sum(1 for result in results if result.get("result") == "FAIL")
    return {"passed": passed, "failed": failed, "total": len(results)}


def decorate_result_record(result: dict) -> dict:
    result["result"] = format_result_label(result["status"])
    result["status_detail"] = result["status"].upper()
    return result


async def execute_instruction(
    pom_page: POMPage,
    instruction: str,
    metadata: dict,
    config: dict,
    result: dict,
    listener_state: Optional[dict] = None,
) -> None:
    normalized = normalize_instruction(instruction)
    click_timeout_seconds = int(config.get("click_timeout_seconds", DEFAULT_CLICK_TIMEOUT_SECONDS))

    if normalized.startswith("capture dom"):
        await pom_page.capture_dom(normalized.replace(" ", "_"))
        return

    if normalized == "verify auth form is visible":
        if not await is_auth_form_visible(pom_page.page):
            raise AssertionError("Authentication form is not visible.")
        await pom_page.capture_dom("auth_form_visible")
        return

    if normalized == "verify authenticated state":
        if not await page_looks_authenticated(pom_page.page):
            raise AssertionError("Authenticated state was not detected after login.")
        await pom_page.capture_dom("authenticated_state")
        return

    if normalized == "submit auth form":
        pom_page.page = await attempt_form_submission(pom_page.page, click_timeout_seconds, listener_state)
        await pom_page.capture_dom("after_auth_submit")
        return

    if normalized == "verify logout succeeds":
        if not await page_looks_logged_out(pom_page.page):
            raise AssertionError("Logout state was not detected.")
        await pom_page.capture_dom("after_logout_verification")
        return

    if normalized in {"verify error message appears", "verify validation or error feedback"}:
        if not await page_has_error_feedback(pom_page.page):
            raise AssertionError("Expected validation or error feedback was not found.")
        await pom_page.capture_dom("validation_feedback")
        return

    if normalized == "verify links are visible":
        result["link_count"] = await pom_page.page.locator("a").count()
        return

    if normalized in {"verify page loads", "verify navigation is stable"} or normalized.startswith("check "):
        await wait_for_runtime_page_ready(pom_page.page, config.get("timeout", 30000))
        await pom_page.capture_dom("verification")
        return

    if normalized == "return to previous page":
        await pom_page.page.wait_for_timeout(700)
        timeout_ms = config.get("timeout", 30000)
        try:
            prior_url = pom_page.page.url
            response = await pom_page.page.go_back(wait_until="domcontentloaded", timeout=timeout_ms)
            if response is None and pom_page.page.url == prior_url:
                await pom_page.goto(result.get("page_url") or prior_url, timeout_ms)
            else:
                await wait_for_runtime_page_ready(pom_page.page, timeout_ms)
        except Exception:
            await pom_page.goto(result.get("page_url") or pom_page.page.url, timeout_ms)
        await pom_page.capture_dom("after_return_to_previous_page")
        return

    if normalized == "submit required inputs incorrectly":
        pom_page.page = await attempt_form_submission(pom_page.page, click_timeout_seconds, listener_state)
        await pom_page.capture_dom("invalid_submission_state")
        return

    if normalized.startswith("click "):
        target = re.sub(r"(?i)^click\s+", "", instruction).strip()
        await pom_page.page.wait_for_timeout(700)
        started = asyncio.get_running_loop().time()
        clicked_page = await timed_click(pom_page.page, target, click_timeout_seconds, listener_state)
        elapsed = asyncio.get_running_loop().time() - started
        if elapsed > click_timeout_seconds:
            raise TimeoutError(f"Click action exceeded {click_timeout_seconds} seconds: {target}")
        if clicked_page is None:
            result["status"] = "warning"
            result["steps"].append(f"Could not click target: {target}")
        else:
            pom_page.page = clicked_page
            await wait_for_runtime_page_ready(pom_page.page, config.get("timeout", 30000))
            result["step_timings"].append({"instruction": instruction, "duration_seconds": round(elapsed, 2)})
            await pom_page.capture_dom(f"after_click_{target}")
        return

    if normalized.startswith("fill ") or normalized.startswith("enter "):
        parsed = parse_fill_instruction(instruction)
        if not parsed:
            result["status"] = "warning"
            result["steps"].append(f"Skipped unclear fill instruction: {instruction}")
            return
        selector, value = parsed
        if value.lower() == "invalid_input":
            value = "invalid_input_123"
        elif value.lower() == "edge_case_input":
            value = "!@# edge boundary 999"
        elif value.lower() == "happy_path_input":
            value = "happy_path_value"
        filled = await safe_fill(pom_page.page, selector, value)
        if not filled:
            result["status"] = "warning"
            result["steps"].append(f"Could not fill target: {selector}")
        else:
            await pom_page.capture_dom(f"after_fill_{selector}")
        return

    if normalized.startswith("select "):
        parsed = parse_select_instruction(instruction)
        if not parsed:
            result["status"] = "warning"
            result["steps"].append(f"Skipped unclear select instruction: {instruction}")
            return
        selector, value = parsed
        selected = await safe_select(pom_page.page, selector, value)
        if not selected:
            result["status"] = "warning"
            result["steps"].append(f"Could not select option '{value}' for target: {selector}")
        else:
            await pom_page.capture_dom(f"after_select_{selector}_{value}")
        return

    if is_login_intent([instruction], metadata) and has_login_credentials(metadata):
        await fill_login_form(pom_page.page, metadata)
        await pom_page.capture_dom("login_form")


async def run_test_case(page: Page, listener_state: dict, url: str, usecase: dict, metadata: dict, config: dict) -> dict:
    event_bucket = {"console": [], "network": [], "page_errors": []}
    listener_state["bucket"] = event_bucket
    pom_page = POMPage(page, DOM_DIR)

    result = {
        "case_id": usecase.get("case_id", ""),
        "title": usecase["title"],
        "type": usecase["type"],
        "status": "passed",
        "steps": [],
        "error": "",
        "page_url": usecase.get("page_url") or url,
        "console_errors": [],
        "network_errors": [],
        "page_errors": [],
        "step_timings": [],
        "duration_seconds": 0,
        "screenshot": "",
    }

    started = asyncio.get_running_loop().time()
    click_timeout_seconds = int(config.get("click_timeout_seconds", DEFAULT_CLICK_TIMEOUT_SECONDS))
    step_timeout_seconds = max(click_timeout_seconds * 2, 30)
    try:
        await pom_page.goto(result["page_url"], config.get("timeout", 30000))
        resolved_credentials, auto_authenticated = await ensure_authenticated_for_target(
            pom_page,
            result["page_url"],
            metadata,
            usecase["instructions"],
            click_timeout_seconds=click_timeout_seconds,
            timeout_ms=config.get("timeout", 30000),
            listener_state=listener_state,
        )
        if auto_authenticated:
            result["steps"].append("Auto-authenticated for protected page")
            await pom_page.capture_dom("auto_authenticated_target_page")
        if (not auto_authenticated) and has_login_credentials(resolved_credentials) and is_login_intent(usecase["instructions"], resolved_credentials):
            await fill_login_form(pom_page.page, resolved_credentials)
            if not has_login_credentials(metadata):
                result["steps"].append("Detected login credentials from the page")
            result["steps"].append("Filled login credentials")

        total_steps = len(usecase["instructions"])
        for step_index, instruction in enumerate(usecase["instructions"], start=1):
            print(f"  [{result.get('case_id', '')} step {step_index}/{total_steps}] {instruction}", flush=True)
            await asyncio.wait_for(
                execute_instruction(pom_page, instruction, resolved_credentials, config, result, listener_state),
                timeout=step_timeout_seconds,
            )
            result["steps"].append(instruction)

        result["screenshot"] = await pom_page.screenshot(f"{usecase['title']}_{usecase['type']}", failed=False)
    except TimeoutError as exc:
        result["status"] = "failed"
        result["error"] = str(exc)
        result["screenshot"] = await pom_page.screenshot(f"{usecase['title']}_{usecase['type']}", failed=True)
    except Error as exc:
        result["status"] = "failed"
        result["error"] = str(exc)
        result["screenshot"] = await pom_page.screenshot(f"{usecase['title']}_{usecase['type']}", failed=True)
    except Exception as exc:
        result["status"] = "failed"
        result["error"] = str(exc)
        try:
            result["screenshot"] = await pom_page.screenshot(f"{usecase['title']}_{usecase['type']}", failed=True)
        except Exception:
            result["screenshot"] = ""
    finally:
        result["duration_seconds"] = round(asyncio.get_running_loop().time() - started, 2)
        result["console_errors"] = event_bucket["console"]
        result["network_errors"] = event_bucket["network"]
        result["page_errors"] = event_bucket["page_errors"]
        decorate_result_record(result)
        listener_state["bucket"] = None
    return result


async def run_case_with_retry(page: Page, listener_state: dict, url: str, usecase: dict, metadata: dict, config: dict) -> dict:
    timeout_seconds = max(int(config.get("click_timeout_seconds", DEFAULT_CLICK_TIMEOUT_SECONDS)) * 2, 45)
    for attempt in range(1, MAX_USECASE_RETRIES + 2):
        try:
            result = await asyncio.wait_for(
                run_test_case(page, listener_state, url, usecase, metadata, config),
                timeout=timeout_seconds,
            )
            if attempt > 1 and result["status"] != "failed":
                result["steps"].append("Retry attempt succeeded")
            return result
        except asyncio.TimeoutError:
            print(f"Use case '{usecase['title']}' timed out, attempt {attempt}/{MAX_USECASE_RETRIES + 1}.")
            if attempt == MAX_USECASE_RETRIES + 1:
                return decorate_result_record({
                    "case_id": usecase.get("case_id", ""),
                    "title": usecase["title"],
                    "type": usecase["type"],
                    "status": "failed",
                    "steps": [f"Use case timed out after {timeout_seconds} seconds"],
                    "error": f"Timeout after {timeout_seconds} seconds",
                    "page_url": usecase.get("page_url") or url,
                    "console_errors": [],
                    "network_errors": [],
                    "page_errors": [],
                    "step_timings": [],
                    "duration_seconds": timeout_seconds,
                    "screenshot": "",
                })
            print("Retrying use case...")


async def main(
    doc_path: Optional[str] = None,
    scenario_text: Optional[str] = None,
    auto_approve: bool = False,
    regenerate: bool = False,
) -> None:
    try:
        instruction_path = resolve_doc_path(doc_path, scenario_text)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(str(exc))
        return

    if not instruction_path:
        print("No instruction file found in /docsnew. Add a .md, .txt, .pdf, .docx, or .csv file, provide a file path, or paste a scenario.")
        return

    initial_text = read_doc_file(instruction_path)
    instruction_path, text, url, instructions, metadata, requested_count, requirement_understanding = capture_confirmed_requirement(
        instruction_path,
        initial_text,
    )
    fresh_dom_run = requires_fresh_dom_run(instructions)
    if fresh_dom_run:
        clear_persisted_site_memory(url)
    clear_run_artifacts()

    config = load_playwright_config()
    scenario_id = build_scenario_id(instruction_path, text)
    usecases: List[dict] = []
    taught_pages = [] if fresh_dom_run else load_taught_pages_for_url(url)
    if taught_pages:
        print(f"Loaded {len(taught_pages)} taught page blueprint(s) from earlier teach mode.")
    if fresh_dom_run:
        print("Fresh DOM mode enabled. Previous site memory and stored DOM blueprints were cleared for this run.")

    print(f"Launching browser headless={config.get('headless', False)} slow_mo={config.get('slow_mo', 250)}")
    playwright = await async_playwright().start()
    browser_launcher = getattr(playwright, config.get("browser", "chromium"))
    browser = await browser_launcher.launch(headless=config.get("headless", False), slow_mo=config.get("slow_mo", 250))
    context = await browser.new_context()
    await install_single_tab_guard(context)
    await install_popup_collapse_handler(context)

    discovered_pages: List[dict] = []
    site_understanding: Optional[dict] = None
    results: List[dict] = []
    execution_page: Optional[Page] = None
    try:
        while True:
            discovered_pages = await run_timed_exploration(
                context,
                url=url,
                timeout_ms=config.get("timeout", 30000),
                max_pages=int(config.get("max_discovery_pages", DEFAULT_PAGE_DISCOVERY_LIMIT)),
                metadata=metadata,
                instructions=instructions,
                exploration_time_limit_seconds=int(config.get("exploration_time_limit_seconds", EXPLORATION_TIME_LIMIT_SECONDS)),
                worker_count=int(config.get("exploration_workers", EXPLORATION_WORKER_COUNT)),
            )
            discovered_pages = merge_discovered_pages(taught_pages, discovered_pages)
            (DOM_DIR / "dom_inventory.json").write_text(json.dumps(discovered_pages, indent=2), encoding="utf-8")

            site_understanding = build_site_understanding(url, instructions, metadata, discovered_pages, requested_count)
            site_understanding["requirement_understanding"] = requirement_understanding
            write_site_understanding_files(scenario_id, site_understanding)

            if not site_requires_login_credentials(url, instructions, metadata, discovered_pages):
                break

            supplied = prompt_for_missing_credentials(site_understanding.get("login_page_url", url))
            if not has_login_credentials(supplied):
                update_registry_entry(scenario_id, instruction_path, text, approved=False, usecase_count=len(usecases))
                print("Execution stopped because required credentials were not provided.")
                return
            metadata = merge_runtime_metadata(metadata, supplied)
            print("Credentials received. Rerunning the timed exploration now.")

        usecases = build_final_usecases(url, text, instructions, metadata, discovered_pages, requested_count, site_understanding)
        if requested_count is not None:
            usecases = usecases[:requested_count]
        usecases = assign_case_ids(usecases)
        write_usecases_files(scenario_id, instruction_path.name, url, usecases)
        if not prompt_for_approval(usecases, scenario_id, auto_approve, site_understanding):
            update_registry_entry(scenario_id, instruction_path, text, approved=False, usecase_count=len(usecases))
            print("Use case approval declined. Review the generated files under /usecases and rerun when ready.")
            return
        update_registry_entry(scenario_id, instruction_path, text, approved=True, usecase_count=len(usecases))

        write_playwright_assets(scenario_id, url, usecases)

        write_results(results)
        execution_page = await context.new_page()
        listener_state = await attach_runtime_listeners(execution_page)
        for index, usecase in enumerate(usecases, start=1):
            print(f"[{usecase.get('case_id', '')} {index}/{len(usecases)}] START - {usecase['title']}", flush=True)
            result = await run_case_with_retry(execution_page, listener_state, url, usecase, metadata, config)
            results.append(result)
            write_results(results)
            print(f"[{result.get('case_id', '')} {len(results)}/{len(usecases)}] {result['result']} - {result['title']}", flush=True)
    finally:
        if execution_page is not None and not execution_page.is_closed():
            await execution_page.close()
        await browser.close()
        await playwright.stop()

    write_results(results)
    report_data = build_runtime_report(scenario_id, instruction_path, url, usecases, discovered_pages, results, site_understanding)
    write_reports(report_data)


async def teach_mode(
    doc_path: Optional[str] = None,
    scenario_text: Optional[str] = None,
) -> None:
    try:
        instruction_path = resolve_doc_path(doc_path, scenario_text)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(str(exc))
        return

    if not instruction_path:
        print("No instruction file found in /docsnew. Add a .md, .txt, .pdf, .docx, or .csv file, provide a file path, or paste a scenario.")
        return

    text = read_doc_file(instruction_path)
    url = extract_url(text)
    if not url:
        print("No URL found in the instruction document. Put the target URL on the first line.")
        return

    metadata = extract_metadata(text)
    config = load_playwright_config()
    print("Teach mode will open a visible browser so you can explore manually.")
    print("Explore the site the way you want the AI to learn it, then return here and press Enter.")

    try:
        playwright = await async_playwright().start()
        browser_launcher = getattr(playwright, config.get("browser", "chromium"))
        browser = await browser_launcher.launch(headless=False, slow_mo=config.get("slow_mo", 250))
    except (PermissionError, OSError, Error) as exc:
        print("Teach mode could not launch the Playwright browser.")
        print(f"Browser startup error: {exc}")
        print("Run the command from your local terminal session where opening a visible browser window is allowed.")
        return

    context = await browser.new_context()
    await install_single_tab_guard(context)
    await install_popup_collapse_handler(context)
    taught_page_inventories: List[dict] = []
    await attach_teach_mode_recording(context)
    await attach_teach_mode_page_capture(context, taught_page_inventories)
    page = await context.new_page()

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=config.get("timeout", 30000))
        await wait_for_runtime_page_ready(page, config.get("timeout", 30000))
        if has_login_credentials(metadata):
            print("Credentials were found in the document. You can use them during manual exploration if needed.")
            print(f"Email/User: {metadata.get('email') or metadata.get('username')}")
        await asyncio.to_thread(input, "Press Enter here after you finish manual exploration...")
    finally:
        for open_page in context.pages:
            await snapshot_teach_mode_page_inventory(open_page, taught_page_inventories)
        recorded_events = await harvest_teach_mode_events(context)
        current_url = page.url if not page.is_closed() else url
        if not page.is_closed():
            await page.close()
        await browser.close()
        await playwright.stop()

    if not recorded_events and not taught_page_inventories:
        print("No manual exploration events were captured. Try interacting with visible links, buttons, inputs, or selects during teach mode.")
        return

    normalized_events: List[dict] = []
    for event in recorded_events:
        normalized_events.append({
            "action": str(event.get("action", "")).strip().lower(),
            "url": str(event.get("url", "")).strip() or current_url,
            "title": str(event.get("title", "")).strip(),
            "selector": str(event.get("selector", "")).strip(),
            "label": str(event.get("label", "")).strip(),
            "href": str(event.get("href", "")).strip(),
            "value": str(event.get("value", "")).strip(),
            "recorded_at": datetime.now().isoformat(),
        })

    memory = load_action_memory()
    key = memory_key_for_url(url)
    memory_entry = memory.get(key, {})
    existing_patterns = memory_entry.get("manual_patterns", [])
    memory_entry["manual_patterns"] = merge_manual_patterns(existing_patterns, normalized_events)
    existing_taught_pages = memory_entry.get("taught_pages", [])
    memory_entry["taught_pages"] = merge_discovered_pages(taught_page_inventories, existing_taught_pages)
    memory_entry["last_teach_session_at"] = datetime.now().isoformat()
    memory_entry["last_teach_source"] = str(instruction_path.name)
    memory_entry["taught_page_urls"] = sorted({
        str(item.get("url", "")).strip()
        for item in memory_entry["taught_pages"]
        if str(item.get("url", "")).strip()
    })
    memory[key] = memory_entry
    save_action_memory(memory)

    DOM_DIR.mkdir(parents=True, exist_ok=True)
    (DOM_DIR / "teach_dom_inventory.json").write_text(json.dumps(memory_entry["taught_pages"], indent=2), encoding="utf-8")

    print(f"Captured {len(normalized_events)} manual exploration event(s).")
    for line in summarize_recorded_patterns(memory_entry["manual_patterns"]):
        print(f"- {line}")
    print(f"Captured DOM blueprints for {len(memory_entry['taught_pages'])} taught page(s).")
    print(f"Learned patterns saved to {ACTION_MEMORY_FILE}.")
    print(f"Execution complete. Results written to {RESULTS_DIR}, reports to {REPORTS_DIR}, and Playwright assets to {PLAYWRIGHT_POM_DIR}.")


def main_sync() -> None:
    args = parse_cli_args()
    if args.teach:
        asyncio.run(teach_mode(args.doc_path, args.scenario_text))
        return
    asyncio.run(main(args.doc_path, args.scenario_text, args.approve, args.regenerate))


if __name__ == "__main__":
    main_sync()
