from playwright.sync_api import Playwright, sync_playwright
from bots.playwright.main import run

with sync_playwright() as playwright:
    run(playwright)