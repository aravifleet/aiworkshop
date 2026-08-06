import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
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
      "capture DOM after login"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/"
  },
  {
    "title": "Negative path: invalid or missing input",
    "description": "Validate expected failures when input is incorrect or required steps are skipped.",
    "type": "negative",
    "instructions": [
      "fill username with invalid_user",
      "fill password with invalid_pass",
      "click login",
      "verify error message appears"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/"
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
    "page_url": "https://practicetestautomation.com/practice-test-login/"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 1",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 2",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 3",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link HOME"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 4",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 5",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link COURSES"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 6",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 7",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link BLOG"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 8",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link CONTACT"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 9",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 10",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 11",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 12",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action open menu"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 13",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action Submit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Submit",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action Submit"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 14",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field username.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill username with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "fill field username"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 15",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field password.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill password with happy_path_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "fill field password"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 16",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 17",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 18",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link HOME"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 19",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 20",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link COURSES"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 21",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 22",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link BLOG"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 23",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link CONTACT"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 24",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 25",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 26",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 27",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action open menu"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 28",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action Submit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Submit",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action Submit"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 29",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field username.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill username with invalid_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "fill field username"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 30",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field password.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill password with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "fill field password"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 31",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 32",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 33",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link HOME"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 34",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 35",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link COURSES"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 36",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 37",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link BLOG"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 38",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link CONTACT"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 39",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 40",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 41",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 42",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action open menu"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 43",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action Submit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Submit",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click action Submit"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 44",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field username.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill username with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "fill field username"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 45",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field password.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill password with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "fill field password"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 46",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 47",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 48",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link HOME"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 49",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 50",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/",
    "category": "click link COURSES"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 1",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 2",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 3",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link HOME"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 4",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link PRACTICE"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 5",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link COURSES"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 6",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 7",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link BLOG"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 8",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link CONTACT"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 9",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 10",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 11",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 12",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action open menu"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 13",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action Submit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Submit",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action Submit"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 14",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field username.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill username with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "fill field username"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 15",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field password.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill password with happy_path_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "fill field password"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 16",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 17",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 18",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link HOME"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 19",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link PRACTICE"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 20",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link COURSES"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 21",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 22",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link BLOG"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 23",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link CONTACT"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 24",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 25",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 26",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 27",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action open menu"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 28",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action Submit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Submit",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action Submit"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 29",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field username.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill username with invalid_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "fill field username"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 30",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field password.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill password with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "fill field password"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 31",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 32",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 33",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link HOME"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 34",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link PRACTICE"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 35",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link COURSES"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 36",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 37",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link BLOG"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 38",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link CONTACT"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 39",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 40",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 41",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 42",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action open menu"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 43",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click action Submit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Submit",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click action Submit"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 44",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field username.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill username with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "fill field username"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 45",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to fill field password.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill password with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "fill field password"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 46",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 47",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 48",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link HOME"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 49",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link PRACTICE"
  },
  {
    "title": "Test Login | Practice Test Automation: exploratory case 50",
    "description": "Auto-generated exploratory case for Test Login | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice-test-login/#main-container",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 1",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 2",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 3",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link HOME"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 4",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 5",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 6",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 7",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link BLOG"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 8",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link CONTACT"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 9",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link nine courses with over 100,000.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link nine courses with over 100,000"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 10",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BestSeller XPath course.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://www.udemy.com/course/xpath-locators-for-selenium/?referralCode=ACB28329B5AC2333DDCC",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link BestSeller XPath course"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 11",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link HighestRated Selenium course.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://www.udemy.com/course/selenium-for-beginners/?referralCode=A21BE51035C15406EFA4",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link HighestRated Selenium course"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 12",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link diverse selection of articles,.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link diverse selection of articles,"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 13",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link practical platform.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link practical platform"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 14",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link BLOG"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 15",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 16",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Built with Kit"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 17",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 18",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 19",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Built with Kit"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 20",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 21",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click action open menu"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 22",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action Get the cheat sheet.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Get the cheat sheet",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click action Get the cheat sheet"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 23",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action Subscribe.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Subscribe",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click action Subscribe"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 24",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action Close.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Close",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click action Close"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 25",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "fill field email_address"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 26",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with invalid_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "fill field email_address"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 27",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "fill field tags[]"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 28",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "fill field tags[]"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 29",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "fill field tags[]"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 30",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/#main-container",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 31",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 32",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link HOME"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 33",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 34",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 35",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 36",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link BLOG"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 37",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link CONTACT"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 38",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link nine courses with over 100,000.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link nine courses with over 100,000"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 39",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BestSeller XPath course.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://www.udemy.com/course/xpath-locators-for-selenium/?referralCode=ACB28329B5AC2333DDCC",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link BestSeller XPath course"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 40",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link HighestRated Selenium course.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://www.udemy.com/course/selenium-for-beginners/?referralCode=A21BE51035C15406EFA4",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link HighestRated Selenium course"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 41",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link diverse selection of articles,.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link diverse selection of articles,"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 42",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link practical platform.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link practical platform"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 43",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link BLOG"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 44",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 45",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Built with Kit"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 46",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 47",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 48",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click link Built with Kit"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 49",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 50",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/",
    "category": "click action open menu"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 1",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 2",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 3",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link HOME"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 4",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 5",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link COURSES"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 6",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 7",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link BLOG"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 8",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link CONTACT"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 9",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Login Page.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Login Page"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 10",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Exceptions.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-exceptions/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Exceptions"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 11",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Table.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-table/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Table"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 12",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 13",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 14",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 15",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click action open menu"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 16",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 17",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 18",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link HOME"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 19",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 20",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link COURSES"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 21",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 22",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link BLOG"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 23",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link CONTACT"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 24",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Login Page.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Login Page"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 25",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Exceptions.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-exceptions/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Exceptions"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 26",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Table.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-table/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Table"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 27",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 28",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 29",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 30",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click action open menu"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 31",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 32",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 33",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link HOME"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 34",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 35",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link COURSES"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 36",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 37",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link BLOG"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 38",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link CONTACT"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 39",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Login Page.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-login/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Login Page"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 40",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Exceptions.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-exceptions/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Exceptions"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 41",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Test Table.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice-test-table/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Test Table"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 42",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 43",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 44",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 45",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click action open menu"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 46",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 47",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 48",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link HOME"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 49",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Practice | Practice Test Automation: exploratory case 50",
    "description": "Auto-generated exploratory case for Practice | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/practice/",
    "category": "click link COURSES"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 1",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 2",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 3",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link HOME"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 4",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 5",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link COURSES"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 6",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 7",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link BLOG"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 8",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link CONTACT"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 9",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Selenium WebDriver with Java: .",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/beginners-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Selenium WebDriver with Java: "
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 10",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/beginners-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 11",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Selenium WebDriver: Selenium A.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-python-udemy",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Selenium WebDriver: Selenium A"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 12",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-python-udemy",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 13",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Java for Testers.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/java-for-testers-udemy",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Java for Testers"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 14",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/java-for-testers-udemy",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 15",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Python: The Complete Guide for.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/python-for-testers",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Python: The Complete Guide for"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 16",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/python-for-testers",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 17",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Advanced Selenium WebDriver wi.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/advanced-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Advanced Selenium WebDriver wi"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 18",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/advanced-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 19",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link XPath and CSS Locators for Tes.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/xpath-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link XPath and CSS Locators for Tes"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 20",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/xpath-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 21",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 22",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click action open menu"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 23",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/#main-container",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 24",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 25",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link HOME"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 26",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 27",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link COURSES"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 28",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 29",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link BLOG"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 30",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link CONTACT"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 31",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Selenium WebDriver with Java: .",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/beginners-course-coupon",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Selenium WebDriver with Java: "
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 32",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/beginners-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 33",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Selenium WebDriver: Selenium A.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-python-udemy",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Selenium WebDriver: Selenium A"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 34",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-python-udemy",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 35",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Java for Testers.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/java-for-testers-udemy",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Java for Testers"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 36",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/java-for-testers-udemy",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 37",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Python: The Complete Guide for.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/python-for-testers",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Python: The Complete Guide for"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 38",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/python-for-testers",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 39",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Advanced Selenium WebDriver wi.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/advanced-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Advanced Selenium WebDriver wi"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 40",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/advanced-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 41",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link XPath and CSS Locators for Tes.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/xpath-course-coupon",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link XPath and CSS Locators for Tes"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 42",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Enroll in this course on Udemy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/xpath-course-coupon",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Enroll in this course on Udemy"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 43",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 44",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click action open menu"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 45",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/#main-container",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 46",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 47",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link HOME"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 48",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 49",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link COURSES"
  },
  {
    "title": "Courses | Practice Test Automation: exploratory case 50",
    "description": "Auto-generated exploratory case for Courses | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/courses/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 1",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 2",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 3",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field email_address"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 4",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 5",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 6",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 7",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 8",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 9",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field email_address"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 10",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 11",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 12",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 13",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 14",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 15",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field email_address"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 16",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 17",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 18",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 19",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 20",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 21",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field email_address"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 22",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 23",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 24",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 25",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 26",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 27",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field email_address"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 28",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 29",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 30",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 31",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 32",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 33",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field email_address"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 34",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 35",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 36",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 37",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 38",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 39",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field email_address"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 40",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 41",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 42",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 43",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 44",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 45",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field email_address"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 46",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 47",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 48",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "fill field tags[]"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 49",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click link Powered By Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click link Powered By Kit"
  },
  {
    "title": "AI-powered test automation \u2014 a live workshop: exploratory case 50",
    "description": "Auto-generated exploratory case for AI-powered test automation \u2014 a live workshop to click action Join the waitlist.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Join the waitlist",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://dmytro-shyshkin.kit.com/ai-workshop",
    "category": "click action Join the waitlist"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 1",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 2",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 3",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link HOME"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 4",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 5",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link COURSES"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 6",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 7",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link BLOG"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 8",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link CONTACT"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 9",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Teach AI to Diagnose Failing T.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/ai-diagnose-failing-tests/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Teach AI to Diagnose Failing T"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 10",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Teach AI to Diagnose Failing T.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/ai-diagnose-failing-tests/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Teach AI to Diagnose Failing T"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 11",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Read More Teach AI to Diagnose.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/ai-diagnose-failing-tests/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Read More Teach AI to Diagnose"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 12",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link The Assertion Is the Hard Part.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/assertion-is-the-hard-part/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link The Assertion Is the Hard Part"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 13",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link The Assertion Is the Hard Part.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/assertion-is-the-hard-part/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link The Assertion Is the Hard Part"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 14",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Read More The Assertion Is the.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/assertion-is-the-hard-part/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Read More The Assertion Is the"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 15",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link The Framework Was Never the Ha.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/framework-debate-distraction-ai-test-automation/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link The Framework Was Never the Ha"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 16",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link The Framework Was Never the Ha.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/framework-debate-distraction-ai-test-automation/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link The Framework Was Never the Ha"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 17",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Read More The Framework Was Ne.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/framework-debate-distraction-ai-test-automation/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Read More The Framework Was Ne"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 18",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Unlock Your Future: Selenium W.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-webdriver-career-launcher-part-6-engaging-with-the-selenium-community/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Unlock Your Future: Selenium W"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 19",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link \u201cSelenium WebDriver Career Lau.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-webdriver-career-launcher-part-1-elevating-your-career/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link \u201cSelenium WebDriver Career Lau"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 20",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Read More Unlock Your Future: .",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-webdriver-career-launcher-part-6-engaging-with-the-selenium-community/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Read More Unlock Your Future: "
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 21",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 22",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click action open menu"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 23",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/#main-container",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 24",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 25",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link HOME"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 26",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 27",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link COURSES"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 28",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 29",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link BLOG"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 30",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link CONTACT"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 31",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Teach AI to Diagnose Failing T.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/ai-diagnose-failing-tests/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Teach AI to Diagnose Failing T"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 32",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Teach AI to Diagnose Failing T.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/ai-diagnose-failing-tests/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Teach AI to Diagnose Failing T"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 33",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Read More Teach AI to Diagnose.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/ai-diagnose-failing-tests/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Read More Teach AI to Diagnose"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 34",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link The Assertion Is the Hard Part.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/assertion-is-the-hard-part/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link The Assertion Is the Hard Part"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 35",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link The Assertion Is the Hard Part.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/assertion-is-the-hard-part/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link The Assertion Is the Hard Part"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 36",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Read More The Assertion Is the.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/assertion-is-the-hard-part/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Read More The Assertion Is the"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 37",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link The Framework Was Never the Ha.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/framework-debate-distraction-ai-test-automation/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link The Framework Was Never the Ha"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 38",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link The Framework Was Never the Ha.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/framework-debate-distraction-ai-test-automation/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link The Framework Was Never the Ha"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 39",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Read More The Framework Was Ne.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/framework-debate-distraction-ai-test-automation/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Read More The Framework Was Ne"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 40",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Unlock Your Future: Selenium W.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-webdriver-career-launcher-part-6-engaging-with-the-selenium-community/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Unlock Your Future: Selenium W"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 41",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link \u201cSelenium WebDriver Career Lau.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-webdriver-career-launcher-part-1-elevating-your-career/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link \u201cSelenium WebDriver Career Lau"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 42",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Read More Unlock Your Future: .",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/selenium-webdriver-career-launcher-part-6-engaging-with-the-selenium-community/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Read More Unlock Your Future: "
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 43",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 44",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click action open menu"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 45",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/#main-container",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 46",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 47",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link HOME"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 48",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 49",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link COURSES"
  },
  {
    "title": "Blog | Practice Test Automation: exploratory case 50",
    "description": "Auto-generated exploratory case for Blog | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/blog/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 1",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 2",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 3",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link HOME"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 4",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 5",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link COURSES"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 6",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 7",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link BLOG"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 8",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link CONTACT"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 9",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 10",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 11",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link Built with Kit"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 12",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 13",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action open menu"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 14",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action Submit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Submit",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action Submit"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 15",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action Subscribe.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Subscribe",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action Subscribe"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 16",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action Close.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Close",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action Close"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 17",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[fields][0][first].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[fields][0][first] with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[fields][0][first]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 18",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[fields][0][last].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[fields][0][last] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[fields][0][last]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 19",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[fields][1].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[fields][1] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[fields][1]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 20",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[fields][2].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[fields][2] with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[fields][2]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 21",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[hp].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "fill wpforms[hp] with happy_path_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[hp]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 22",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field g-recaptcha-response.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill g-recaptcha-response with edge_case_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field g-recaptcha-response"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 23",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field g-recaptcha-hidden.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill g-recaptcha-hidden with invalid_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field g-recaptcha-hidden"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 24",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[id].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[id] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[id]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 25",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field page_title.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill page_title with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field page_title"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 26",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field page_url.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill page_url with invalid_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field page_url"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 27",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field url_referer.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill url_referer with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field url_referer"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 28",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field page_id.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill page_id with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field page_id"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 29",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[post_id].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[post_id] with invalid_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[post_id]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 30",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field email_address"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 31",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field tags[]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 32",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/#main-container",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 33",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 34",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link HOME"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 35",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 36",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link COURSES"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 37",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 38",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link BLOG"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 39",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link CONTACT"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 40",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 41",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 42",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click link Built with Kit"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 43",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 44",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action open menu"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 45",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action Submit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Submit",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action Submit"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 46",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action Subscribe.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Subscribe",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action Subscribe"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 47",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to click action Close.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Close",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "click action Close"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 48",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[fields][0][first].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[fields][0][first] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[fields][0][first]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 49",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[fields][0][last].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[fields][0][last] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[fields][0][last]"
  },
  {
    "title": "Contact | Practice Test Automation | Selenium WebDriver: exploratory case 50",
    "description": "Auto-generated exploratory case for Contact | Practice Test Automation | Selenium WebDriver to fill field wpforms[fields][1].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill wpforms[fields][1] with invalid_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/contact/",
    "category": "fill field wpforms[fields][1]"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 1",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 2",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 3",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link HOME"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 4",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 5",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link COURSES"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 6",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 7",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link BLOG"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 8",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link CONTACT"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 9",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 10",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 11",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 12",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 13",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 14",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click action open menu"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 15",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/#main-container",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 16",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 17",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link HOME"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 18",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 19",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link COURSES"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 20",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 21",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link BLOG"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 22",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link CONTACT"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 23",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 24",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 25",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 26",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 27",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 28",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click action open menu"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 29",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/#main-container",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 30",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 31",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link HOME"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 32",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 33",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link COURSES"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 34",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 35",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link BLOG"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 36",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link CONTACT"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 37",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 38",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 39",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 40",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 41",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 42",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click action open menu"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 43",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/#main-container",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 44",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 45",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link HOME"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 46",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link PRACTICE"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 47",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link COURSES"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 48",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 49",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link BLOG"
  },
  {
    "title": "Privacy Policy | Practice Test Automation: exploratory case 50",
    "description": "Auto-generated exploratory case for Privacy Policy | Practice Test Automation to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/privacy-policy/",
    "category": "click link CONTACT"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 1",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/#main-container",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 2",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 3",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link HOME"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 4",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link PRACTICE"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 5",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 6",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 7",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link BLOG"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 8",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link CONTACT"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 9",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link nine courses with over 100,000.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link nine courses with over 100,000"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 10",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BestSeller XPath course.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://www.udemy.com/course/xpath-locators-for-selenium/?referralCode=ACB28329B5AC2333DDCC",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link BestSeller XPath course"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 11",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link HighestRated Selenium course.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://www.udemy.com/course/selenium-for-beginners/?referralCode=A21BE51035C15406EFA4",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link HighestRated Selenium course"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 12",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link diverse selection of articles,.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link diverse selection of articles,"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 13",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link practical platform.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link practical platform"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 14",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link BLOG"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 15",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 16",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Built with Kit"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 17",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 18",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 19",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Built with Kit"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 20",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 21",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click action open menu"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 22",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action Get the cheat sheet.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Get the cheat sheet",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click action Get the cheat sheet"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 23",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action Subscribe.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Subscribe",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click action Subscribe"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 24",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action Close.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click Close",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click action Close"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 25",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "fill field email_address"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 26",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field email_address.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill email_address with invalid_input",
      "capture DOM after input",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "fill field email_address"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 27",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with happy_path_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "fill field tags[]"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 28",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with edge_case_input",
      "capture DOM after input"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "fill field tags[]"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 29",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to fill field tags[].",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "fill tags[] with invalid_input",
      "capture DOM after input",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "fill field tags[]"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 30",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Press \"Enter\" to skip to conte.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/#main-container",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Press \"Enter\" to skip to conte"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 31",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link https://practicetestautomation.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link https://practicetestautomation"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 32",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link HOME.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link HOME"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 33",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link PRACTICE.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link PRACTICE"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 34",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 35",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link AI WORKSHOP.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/workshop",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link AI WORKSHOP"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 36",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link BLOG"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 37",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link CONTACT.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/contact/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link CONTACT"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 38",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link nine courses with over 100,000.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link nine courses with over 100,000"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 39",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BestSeller XPath course.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://www.udemy.com/course/xpath-locators-for-selenium/?referralCode=ACB28329B5AC2333DDCC",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link BestSeller XPath course"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 40",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link HighestRated Selenium course.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://www.udemy.com/course/selenium-for-beginners/?referralCode=A21BE51035C15406EFA4",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link HighestRated Selenium course"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 41",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link diverse selection of articles,.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "fill username with student",
      "fill password with Password123",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link diverse selection of articles,"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 42",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link practical platform.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/practice/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link practical platform"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 43",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link BLOG.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/blog/",
      "verify page loads",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link BLOG"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 44",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link COURSES.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/courses/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link COURSES"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 45",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Built with Kit"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 46",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Practice Test Automation..",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/",
      "verify page loads",
      "capture DOM after click",
      "verify links are visible"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Practice Test Automation."
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 47",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Privacy Policy.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://practicetestautomation.com/privacy-policy/",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Privacy Policy"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 48",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click link Built with Kit.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click https://kit.com/features/forms?utm_campaign=poweredby&utm_content=form&utm_medium=referral&utm_source=dynamic",
      "verify page loads",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click link Built with Kit"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 49",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action button:nth-of-type(1).",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click button:nth-of-type(1)",
      "capture DOM after click"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click action button:nth-of-type(1)"
  },
  {
    "title": "Practice Test Automation | Learn Selenium WebDriver: exploratory case 50",
    "description": "Auto-generated exploratory case for Practice Test Automation | Learn Selenium WebDriver to click action open menu.",
    "type": "exploratory",
    "instructions": [
      "verify page loads",
      "capture DOM before actions",
      "click open menu",
      "capture DOM after click",
      "submit required inputs incorrectly"
    ],
    "page_url": "https://practicetestautomation.com/#main-container",
    "category": "click action open menu"
  }
]
URL = 'https://practicetestautomation.com/practice-test-login/'

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
