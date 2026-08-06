from pathlib import Path
from playwright.async_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def open(self, url: str):
        await self.page.goto(url, wait_until="networkidle")

    async def capture_screenshot(self, path: Path):
        await self.page.screenshot(path=str(path))

    async def get_dom(self) -> str:
        return await self.page.content()
