import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
USECASES = [
  {
    "title": "Happy path: basic flow",
    "description": "Validate the happy path on http://127.0.0.1:8765/fetched_page.html using the provided instructions.",
    "type": "happy",
    "instructions": [
      "verify page loads",
      "capture DOM"
    ],
    "page_url": "http://127.0.0.1:8765/fetched_page.html"
  },
  {
    "title": "Negative path: invalid or missing input",
    "description": "Validate expected failures when input is incorrect or required steps are skipped.",
    "type": "negative",
    "instructions": [
      "verify page loads",
      "capture DOM"
    ],
    "page_url": "http://127.0.0.1:8765/fetched_page.html"
  },
  {
    "title": "Edge case: alternate navigation or UI behavior",
    "description": "Verify edge cases and alternate navigation from the same starting point.",
    "type": "edge",
    "instructions": [
      "verify navigation is stable",
      "capture DOM after each major step",
      "verify links are visible"
    ],
    "page_url": "http://127.0.0.1:8765/fetched_page.html"
  },
  {
    "title": "Example Domain: exploratory case 1",
    "description": "Auto-generated exploratory case for Example Domain to click link Learn more.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://iana.org/domains/example",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "http://127.0.0.1:8765/fetched_page.html",
    "category": "click link Learn more"
  },
  {
    "title": "Example Domain: exploratory case 2",
    "description": "Auto-generated exploratory case for Example Domain to click link Learn more.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://iana.org/domains/example",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "http://127.0.0.1:8765/fetched_page.html",
    "category": "click link Learn more"
  },
  {
    "title": "Example Domain: exploratory case 3",
    "description": "Auto-generated exploratory case for Example Domain to click link Learn more.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://iana.org/domains/example",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "http://127.0.0.1:8765/fetched_page.html",
    "category": "click link Learn more"
  },
  {
    "title": "Example Domain: exploratory case 4",
    "description": "Auto-generated exploratory case for Example Domain to click link Learn more.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://iana.org/domains/example",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "http://127.0.0.1:8765/fetched_page.html",
    "category": "click link Learn more"
  },
  {
    "title": "Example Domain: exploratory case 5",
    "description": "Auto-generated exploratory case for Example Domain to click link Learn more.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://iana.org/domains/example",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "http://127.0.0.1:8765/fetched_page.html",
    "category": "click link Learn more"
  }
]
URL = 'http://127.0.0.1:8765/fetched_page.html'

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        for usecase in USECASES:
            await page.goto(usecase.get("page_url") or URL, wait_until="networkidle")
            await page.screenshot(path=str(WORKSPACE_ROOT / "screenshots" / f"{usecase['type']}_sample.png"), full_page=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
