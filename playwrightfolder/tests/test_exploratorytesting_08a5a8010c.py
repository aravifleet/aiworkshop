import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from pages.exploratorytesting_08a5a8010c_page import ScenarioPage

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
USECASE_FILE = WORKSPACE_ROOT / "playwrightfolder" / "data" / "exploratorytesting_08a5a8010c_usecases.json"

async def main():
    usecases = json.loads(USECASE_FILE.read_text(encoding="utf-8"))
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        pom = ScenarioPage(page)
        for usecase in usecases:
            await pom.open(usecase.get("page_url") or pom.default_url)
            screenshot_name = f"{usecase['title']}_{usecase['type']}".replace(" ", "_").lower()
            await pom.screenshot(WORKSPACE_ROOT / "screenshots" / f"{screenshot_name}_qa.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
