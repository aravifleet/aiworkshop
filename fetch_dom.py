import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright

class InteractiveDOMCrawler:
    """
    Manages a live Playwright browser session to crawl across multiple pages/actions 
    and fetch DOMs sequentially.
    """
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.step_counter = 0

    async def start(self):
        """Starts the browser session."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        print("🌐 Browser session started.")

    def clean_dom_for_ai(self, html_content: str) -> str:
        """Strips non-essential tags (scripts, styles, SVGs) for cleaner AI input."""
        cleaned = re.sub(r'<script\b[^<]*(?:(?!</script>)<[^<]*)*</script>', '', html_content, flags=re.IGNORECASE)
        cleaned = re.sub(r'<style\b[^<]*(?:(?!</style>)<[^<]*)*</style>', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'<svg\b[^<]*(?:(?!</svg>)<[^<]*)*</svg>', '<svg>[SVG HIDDEN]</svg>', cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    async def navigate_to(self, url: str) -> str:
        """Navigates to a new URL and captures the DOM."""
        self.step_counter += 1
        print(f"\n[Step {self.step_counter}] Navigating to: {url}")
        
        await self.page.goto(url, wait_until="networkidle", timeout=30000)
        return await self._save_and_return_dom()

    async def click_and_fetch(self, selector_or_text: str) -> str:
        """
        Clicks an element (via CSS selector or text) and fetches the DOM after navigation/rendering.
        """
        self.step_counter += 1
        print(f"\n[Step {self.step_counter}] Clicking element: '{selector_or_text}'...")

        # Playwright auto-waits for element to be actionable
        if selector_or_text.startswith("/") or selector_or_text.startswith("//"):
            # XPath
            await self.page.click(f"xpath={selector_or_text}")
        elif selector_or_text.startswith("text=") or " " in selector_or_text:
            # Text matching
            await self.page.click(f"text={selector_or_text.replace('text=', '')}")
        else:
            # CSS Selector
            await self.page.click(selector_or_text)

        # Wait for dynamic updates / network requests to finish after click
        await self.page.wait_for_load_state("networkidle")
        
        return await self._save_and_return_dom()

    async def _save_and_return_dom(self) -> str:
        """Internal helper to capture, log, and save DOM."""
        dom_content = await self.page.content()
        filename = Path(f"step_{self.step_counter}_dom.html")
        filename.write_text(dom_content, encoding="utf-8")
        
        cleaned = self.clean_dom_for_ai(dom_content)
        print(f"✅ DOM Fetched for Step {self.step_counter}!")
        print(f"   Saved to: {filename.resolve()}")
        print(f"   Raw Length: {len(dom_content)} chars | Cleaned AI Length: {len(cleaned)} chars")
        
        return dom_content

    async def close(self):
        """Closes the browser session."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("\n🔒 Browser session closed.")

# --- Example Usage Workflow ---
async def main():
    crawler = InteractiveDOMCrawler(headless=True)
    await crawler.start()

    try:
        # Step 1: Open initial page
        dom1 = await crawler.navigate_to("https://example.com")

        # Step 2: Click a link (e.g., 'More information...' link on example.com)
        # You can pass link text, CSS selectors (like 'a.next-btn'), or XPaths
        dom2 = await crawler.click_and_fetch("More information...")

        print("\n--- Final Summary ---")
        print("Captured sequential DOMs for all steps in the flow!")

    finally:
        await crawler.close()

if __name__ == "__main__":
    asyncio.run(main())