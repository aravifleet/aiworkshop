import asyncio
import csv
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from playwright.async_api import async_playwright, Page

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(WORKSPACE_ROOT))
from dom import dom as dom_helper

DOCS_DIR = WORKSPACE_ROOT / "docsnew"
DOM_DIR = WORKSPACE_ROOT / "dom" / "dom_elements"
PLAYWRIGHT_DIR = WORKSPACE_ROOT / "playwright-script"
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
PLAYWRIGHT_SCRIPT_DIR = PLAYWRIGHT_DIR

URL_REGEX = re.compile(r"https?://[\w\-\.\/:?&=#]+")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(DOM_DIR, exist_ok=True)
os.makedirs(PLAYWRIGHT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(FAILURE_SCREENSHOT_DIR, exist_ok=True)
os.makedirs(USECASES_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)


def read_first_doc_file() -> Optional[Path]:
    docs = sorted(DOCS_DIR.glob("*.md")) + sorted(DOCS_DIR.glob("*.txt"))
    return docs[0] if docs else None


def read_doc_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_url(text: str) -> Optional[str]:
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    if URL_REGEX.match(first_line):
        return first_line.strip()
    found = URL_REGEX.search(text)
    return found.group(0) if found else None


DATA_ITEM_REGEX = re.compile(r"^(username|password|email)\s*:\s*(?:\*\*([^*]+)\*\*|(.+))", re.IGNORECASE)

def parse_instructions(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    instructions = []
    for line in lines:
        if URL_REGEX.match(line):
            continue
        if line.startswith("#"):
            continue
        if line.lower().startswith("note:"):
            continue
        if DATA_ITEM_REGEX.match(line):
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
    return metadata


def generate_usecases(url: str, instructions: List[str], metadata: dict) -> List[dict]:
    lower_text = " ".join(instructions).lower()
    happy_steps: List[str] = ["verify page loads"]

    if metadata.get("username") and metadata.get("password"):
        happy_steps = [
            f"fill username with {metadata['username']}",
            f"fill password with {metadata['password']}",
            "click login",
            "verify page loads",
            "capture DOM after login",
        ]
    elif any(word in lower_text for word in ["login", "credentials", "password", "username"]):
        happy_steps = ["verify page loads", "capture DOM after login"]

    if "link" in lower_text or "responsive" in lower_text:
        happy_steps.append("verify links are visible")

    negative_steps = [
        "fill username with invalid_user",
        "fill password with invalid_pass",
        "click login",
        "verify error message appears",
    ]
    edge_steps = [
        "verify navigation is stable",
        "capture DOM after each major step",
        "verify links are visible" if ("link" in lower_text or "responsive" in lower_text) else "capture DOM",
    ]

    usecases = [
        {
            "title": "Happy path: basic flow",
            "description": f"Validate the happy path on {url} using the provided instructions.",
            "type": "happy",
            "instructions": happy_steps,
        },
        {
            "title": "Negative path: invalid input or missing action",
            "description": "Validate expected failures when inputs are missing or invalid.",
            "type": "negative",
            "instructions": negative_steps,
        },
        {
            "title": "Edge case: boundary or alternate navigation",
            "description": "Verify edge cases and alternate navigation from the same starting point.",
            "type": "edge",
            "instructions": edge_steps,
        },
    ]
    return usecases


def write_usecases_file(doc_path: Path, url: str, usecases: List[dict]) -> None:
    base_name = doc_path.stem
    target_md = USECASES_DIR / f"{base_name}_usecases.md"
    target_txt = USECASES_DIR / f"{base_name}_usecases.txt"
    target_csv = USECASES_DIR / f"{base_name}_usecases.csv"

    lines = [f"# Use cases generated from {doc_path.name}", f"URL: {url}", ""]
    for uc in usecases:
        lines.append(f"## {uc['title']}")
        lines.append(f"Type: {uc['type']}")
        lines.append(f"Description: {uc['description']}")
        lines.append("Instructions:")
        for inst in uc["instructions"]:
            lines.append(f"- {inst}")
        lines.append("")

    target_md.write_text("\n".join(lines), encoding="utf-8")
    target_txt.write_text("\n".join(lines), encoding="utf-8")
    with target_csv.open("w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "type", "description", "instructions"])
        for uc in usecases:
            writer.writerow([uc["title"], uc["type"], uc["description"], " | ".join(uc["instructions"])])


def write_playwright_script(doc_path: Path, url: str, usecases: List[dict]) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    script_path = PLAYWRIGHT_SCRIPT_DIR / f"{doc_path.stem}_{timestamp}_playwright.py"
    usecases_json = json.dumps(usecases, indent=4)

    script_template = f"""import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = WORKSPACE_ROOT / \"screenshots\"
FAILURE_SCREENSHOT_DIR = WORKSPACE_ROOT / \"failusecases\"
DOM_DIR = WORKSPACE_ROOT / \"dom\" / \"dom_elements\"

class POMPage:
    def __init__(self, page):
        self.page = page

    async def goto(self, url: str):
        await self.page.goto(url, wait_until=\"networkidle\", timeout=30000)
        await self.capture_dom(\"home\")

    async def capture_dom(self, name: str):
        content = await self.page.content()
        file_path = DOM_DIR / f\"{{name}}.html\"
        file_path.write_text(content, encoding=\"utf-8\")

    async def click(self, target: str):
        if target.startswith(\"/\") or target.startswith(\"//\"):
            await self.page.click(f\"xpath={{target}}\")
        elif target.startswith(\"text=\") or \" \" in target:
            await self.page.click(f\"text={{target.replace(\"text=\", \"\")}}\")
        else:
            await self.page.click(target)
        await self.page.wait_for_load_state(\"networkidle\")

    async def fill(self, selector: str, value: str):
        if selector.startswith(\"#\") or selector.startswith(\".\") or selector.startswith(\"xpath=\"):
            await self.page.fill(selector, value)
        else:
            await self.page.fill(f\"text={{selector}}\", value)

    async def screenshot(self, name: str, failed: bool = False):
        target_dir = FAILURE_SCREENSHOT_DIR if failed else SCREENSHOT_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = target_dir / f\"{{name}}_{{'FAIL' if failed else 'PASS'}}.png\"
        await self.page.screenshot(path=str(filename))
        return str(filename)

    async def verify_page_loads(self):
        await self.page.wait_for_load_state(\"networkidle\", timeout=30000)

    async def verify_links(self):
        await self.page.wait_for_load_state(\"networkidle\", timeout=30000)
        return await self.page.locator(\"a\").count()

async def safe_click(page, target: str):
    if target.startswith(\"/\") or target.startswith(\"//\"):
        await page.click(f\"xpath={{target}}\")
    elif target.startswith(\"text=\") or \" \" in target:
        await page.click(f\"text={{target.replace(\"text=\", \"\")}}\")
    else:
        await page.click(target)

async def run_test_case(page, url, usecase):
    result = {{'title': usecase['title'], 'type': usecase['type'], 'status': 'passed', 'steps': []}}
    try:
        await page.goto(url, wait_until=\"networkidle\", timeout=30000)
        for instruction in usecase['instructions']:
            lower = instruction.lower()
            if \"fill\" in lower:
                parts = lower.split(\"with\")
                if len(parts) == 2:
                    selector = parts[0].replace(\"fill\", \"\").replace(\"enter\", \"\").strip()
                    await page.fill(selector, parts[1].strip())
            elif \"click\" in lower:
                target = instruction.replace(\"click\", \"\").strip()
                await safe_click(page, target)
            elif \"verify links\" in lower:
                await page.verify_links()
            elif \"verify error\" in lower:
                await page.capture_dom(\"verify_error\")
            elif \"verify page loads\" in lower or \"check page\" in lower or \"verify navigation\" in lower:
                await page.verify_page_loads()
            elif \"capture dom\" in lower:
                await page.capture_dom(\"verify\")
            result['steps'].append(instruction)
        await page.screenshot(usecase['type'], failed=False)
    except Exception as exc:
        result['status'] = 'failed'
        result['steps'].append(str(exc))
        await page.screenshot(usecase['type'], failed=True)
    return result

URL = {url!r}
USECASES = {usecases_json}

async def main():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    pom_page = POMPage(page)
    results = []
    for uc in USECASES:
        results.append(await run_test_case(pom_page, URL, uc))
    await browser.close()
    await playwright.stop()
    print(\"Run complete. Results:\", results)

if __name__ == \"__main__\":
    asyncio.run(main())
"""

    script_path.write_text(script_template, encoding='utf-8')


def normalize_instruction(instruction: str) -> str:
    return instruction.lower().strip()


async def fill_first_matching_field(page: Page, selectors: List[str], value: str) -> bool:
    for selector in selectors:
        locator = page.locator(selector)
        if await locator.count() > 0:
            await locator.first.fill(value)
            return True
    return False


async def fill_login_form(page: Page, credentials: dict) -> bool:
    if not credentials.get("username") or not credentials.get("password"):
        return False

    username_selectors = [
        'input[name*=username]',
        'input[id*=username]',
        'input[name*=user]',
        'input[id*=user]',
        'input[placeholder*=user]',
        'input[placeholder*=email]',
        'input[type=text]',
    ]
    password_selectors = [
        'input[type=password]',
        'input[name*=password]',
        'input[id*=password]',
        'input[placeholder*=password]',
    ]

    filled_username = await fill_first_matching_field(page, username_selectors, credentials["username"])
    filled_password = await fill_first_matching_field(page, password_selectors, credentials["password"])
    return filled_username or filled_password


class POMPage:
    def __init__(self, page: Page, dom_dir: Path, report: dict):
        self.page = page
        self.dom_dir = dom_dir
        self.report = report

    async def goto(self, url: str):
        await self.page.goto(url, wait_until="networkidle", timeout=30000)
        await self.capture_dom("home")

    async def capture_dom(self, name: str):
        content = await self.page.content()
        file_path = self.dom_dir / f"{datetime.now():%Y%m%d_%H%M%S}_{name}.html"
        file_path.write_text(content, encoding="utf-8")
        dom_helper.save_dom_snapshot(name, content)
        self.report["dom_snapshots"].append(str(file_path.relative_to(WORKSPACE_ROOT)))

    async def click(self, target: str):
        if target.startswith("/") or target.startswith("//"):
            await self.page.click(f"xpath={target}")
        elif target.startswith("text="):
            await self.page.click(target)
        elif target.startswith("#") or target.startswith("."):
            await self.page.click(target)
        elif target:
            locator = self.page.locator(f"text={target}")
            if await locator.count() > 0:
                await locator.first.click()
            else:
                fallback = target.split()[0]
                await self.page.locator(f"text={fallback}").first.click()
        await self.page.wait_for_load_state("networkidle")

    async def fill(self, target: str, value: str):
        if target.startswith("#") or target.startswith(".") or target.startswith("xpath="):
            await self.page.fill(target, value)
        else:
            await self.page.fill(f"text={target}", value)

    async def screenshot(self, name: str, failed: bool = False):
        target_dir = FAILURE_SCREENSHOT_DIR if failed else SCREENSHOT_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = target_dir / f"{datetime.now():%Y%m%d_%H%M%S}_{name}{'_FAIL' if failed else '_PASS'}.png"
        await self.page.screenshot(path=filename)
        return str(filename.relative_to(WORKSPACE_ROOT))


async def run_test_case(page: POMPage, url: str, usecase: dict, metadata: dict) -> dict:
    result = {
        "title": usecase["title"],
        "type": usecase["type"],
        "status": "passed",
        "steps": [],
        "error": "",
    }
    try:
        await page.goto(url)
        if metadata.get("username") and metadata.get("password"):
            filled = await fill_login_form(page.page, metadata)
            if filled:
                result["steps"].append("Filled login credentials")
            else:
                result["steps"].append("Could not find login fields to fill credentials")

        for instruction in usecase["instructions"]:
            normalized = normalize_instruction(instruction)
            if "click" in normalized:
                target = normalized.replace("click", "").strip()
                await page.click(target)
                await page.capture_dom(target.replace(" ", "_").replace("/", "_"))
            elif "fill" in normalized or "enter" in normalized:
                match = re.match(r"(?:fill|enter)\s+(.+)\s+with\s+(.+)", normalized)
                if match:
                    selector, value = match.groups()
                    await page.fill(selector.strip(), value.strip())
                else:
                    result["status"] = "warning"
                    result["steps"].append(f"Skipped unclear fill instruction: {instruction}")
            elif "verify" in normalized or "check" in normalized:
                await page.capture_dom("verify")
            else:
                await page.capture_dom("unknown")
            result["steps"].append(instruction)
        result["screenshot"] = await page.screenshot(usecase["type"], failed=False)
    except Exception as exc:
        result["status"] = "failed"
        result["error"] = str(exc)
        result["screenshot"] = await page.screenshot(usecase["type"], failed=True)
    return result


def write_results(results: List[dict]) -> None:
    csv_lines = []
    txt_lines = ["Test results summary".upper(), ""]
    md_lines = ["# Test Results", "", f"Generated: {datetime.now().isoformat()}", ""]

    with RESULTS_CSV.open("w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "type", "status", "error", "screenshot"])
        for result in results:
            writer.writerow([result["title"], result["type"], result["status"], result["error"], result.get("screenshot", "")])
            txt_lines.append(f"{result['title']} | {result['type']} | {result['status']} | {result['error']}")
            md_lines.append(f"## {result['title']}")
            md_lines.append(f"- Type: {result['type']}")
            md_lines.append(f"- Status: {result['status']}")
            if result["error"]:
                md_lines.append(f"- Error: {result['error']}")
            md_lines.append(f"- Screenshot: {result.get('screenshot', '')}")
            md_lines.append("")

    RESULTS_TXT.write_text("\n".join(txt_lines), encoding="utf-8")
    RESULTS_MD.write_text("\n".join(md_lines), encoding="utf-8")


def write_report(results: List[dict]) -> None:
    report_path = REPORTS_DIR / f"report_{datetime.now():%Y%m%d_%H%M%S}.json"
    report_path.write_text(json.dumps({"generated": datetime.now().isoformat(), "results": results}, indent=2), encoding="utf-8")


def load_playwright_config() -> dict:
    default = {
        "browser": "chromium",
        "headless": False,
        "timeout": 30000,
        "slow_mo": 250,
    }
    if CONFIG_FILE.exists():
        try:
            loaded = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            default.update(loaded)
        except Exception:
            pass
    return default


def clear_old_data() -> None:
    for path in [USECASES_DIR, RESULTS_DIR, REPORTS_DIR, SCREENSHOT_DIR, FAILURE_SCREENSHOT_DIR, DOM_DIR]:
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


async def main():
    doc_path = read_first_doc_file()
    if not doc_path:
        print("No instruction file found in /docsnew. Add a .md or .txt file and rerun.")
        return

    text = read_doc_file(doc_path)
    url = extract_url(text)
    if not url:
        print("No URL found in the instruction document. Put the target URL on the first line.")
        return

    instructions = parse_instructions(text)
    metadata = extract_metadata(text)
    clear_old_data()
    usecases = generate_usecases(url, instructions, metadata)
    write_usecases_file(doc_path, url, usecases)
    write_playwright_script(doc_path, url, usecases)

    config = load_playwright_config()
    print(f"Launching browser headless={config.get('headless', False)} slow_mo={config.get('slow_mo', 250)}")
    results = []
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False, slow_mo=config.get("slow_mo", 250))
    context = await browser.new_context()
    page = await context.new_page()
    pom = POMPage(page, DOM_DIR, {"dom_snapshots": []})

    try:
        for usecase in usecases:
            result = await run_test_case(pom, url, usecase, metadata)
            results.append(result)
    finally:
        await browser.close()
        await playwright.stop()

    write_results(results)
    write_report(results)
    print("Execution complete. Results written to /results and /reports.")


if __name__ == "__main__":
    asyncio.run(main())
