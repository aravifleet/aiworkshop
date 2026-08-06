from pathlib import Path
from playwright.async_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def open(self, url: str, timeout_ms: int = 30000):
        await self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        await self.page.wait_for_load_state("networkidle", timeout=timeout_ms)

    async def screenshot(self, path: Path):
        await self.page.screenshot(path=path, full_page=True)
