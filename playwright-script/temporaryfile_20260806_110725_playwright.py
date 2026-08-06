import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = WORKSPACE_ROOT / "screenshots"
FAILURE_SCREENSHOT_DIR = WORKSPACE_ROOT / "failusecases"
DOM_DIR = WORKSPACE_ROOT / "dom" / "dom_elements"

class POMPage:
    def __init__(self, page):
        self.page = page

    async def goto(self, url: str):
        await self.page.goto(url, wait_until="networkidle", timeout=30000)
        await self.capture_dom("home")

    async def capture_dom(self, name: str):
        content = await self.page.content()
        file_path = DOM_DIR / f"{name}.html"
        file_path.write_text(content, encoding="utf-8")

    async def click(self, target: str):
        if target.startswith("/") or target.startswith("//"):
            await self.page.click(f"xpath={target}")
        elif target.startswith("text=") or " " in target:
            await self.page.click(f"text={target.replace("text=", "")}")
        else:
            await self.page.click(target)
        await self.page.wait_for_load_state("networkidle")

    async def fill(self, selector: str, value: str):
        if selector.startswith("#") or selector.startswith(".") or selector.startswith("xpath="):
            await self.page.fill(selector, value)
        else:
            await self.page.fill(f"text={selector}", value)

    async def screenshot(self, name: str, failed: bool = False):
        target_dir = FAILURE_SCREENSHOT_DIR if failed else SCREENSHOT_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = target_dir / f"{name}_{'FAIL' if failed else 'PASS'}.png"
        await self.page.screenshot(path=str(filename))
        return str(filename)

    async def verify_page_loads(self):
        await self.page.wait_for_load_state("networkidle", timeout=30000)

    async def verify_links(self):
        await self.page.wait_for_load_state("networkidle", timeout=30000)
        return await self.page.locator("a").count()

async def safe_click(page, target: str):
    if target.startswith("/") or target.startswith("//"):
        await page.click(f"xpath={target}")
    elif target.startswith("text=") or " " in target:
        await page.click(f"text={target.replace("text=", "")}")
    else:
        await page.click(target)

async def run_test_case(page, url, usecase):
    result = {'title': usecase['title'], 'type': usecase['type'], 'status': 'passed', 'steps': []}
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        for instruction in usecase['instructions']:
            lower = instruction.lower()
            if "fill" in lower:
                parts = lower.split("with")
                if len(parts) == 2:
                    selector = parts[0].replace("fill", "").replace("enter", "").strip()
                    await page.fill(selector, parts[1].strip())
            elif "click" in lower:
                target = instruction.replace("click", "").strip()
                await safe_click(page, target)
            elif "verify links" in lower:
                await page.verify_links()
            elif "verify error" in lower:
                await page.capture_dom("verify_error")
            elif "verify page loads" in lower or "check page" in lower or "verify navigation" in lower:
                await page.verify_page_loads()
            elif "capture dom" in lower:
                await page.capture_dom("verify")
            result['steps'].append(instruction)
        await page.screenshot(usecase['type'], failed=False)
    except Exception as exc:
        result['status'] = 'failed'
        result['steps'].append(str(exc))
        await page.screenshot(usecase['type'], failed=True)
    return result

URL = 'https://practicetestautomation.com/practice-test-login/'
USECASES = [
    {
        "title": "Happy path: basic flow",
        "description": "Validate the happy path on https://practicetestautomation.com/practice-test-login/ using the provided instructions.",
        "type": "happy",
        "instructions": [
            "fill username with student",
            "fill password with Password123",
            "click login",
            "verify page loads",
            "capture DOM after login",
            "verify links are visible"
        ]
    },
    {
        "title": "Negative path: invalid input or missing action",
        "description": "Validate expected failures when inputs are missing or invalid.",
        "type": "negative",
        "instructions": [
            "fill username with invalid_user",
            "fill password with invalid_pass",
            "click login",
            "verify error message appears"
        ]
    },
    {
        "title": "Edge case: boundary or alternate navigation",
        "description": "Verify edge cases and alternate navigation from the same starting point.",
        "type": "edge",
        "instructions": [
            "verify navigation is stable",
            "capture DOM after each major step",
            "verify links are visible"
        ]
    }
]

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
    print("Run complete. Results:", results)

if __name__ == "__main__":
    asyncio.run(main())
