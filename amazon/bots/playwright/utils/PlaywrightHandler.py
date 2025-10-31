from playwright.sync_api import Playwright, Page, BrowserContext, Browser
from typing import Tuple

class PlaywrightHandler:
    def __init__(self, playwright: Playwright):
        self.playwright = playwright
        self.browser, self.context, self.page = self.__init_plawright()

    def __init_plawright(self) -> Tuple[Browser, BrowserContext, Page]:
        browser = self.playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        return browser, context, page