from playwright.sync_api import sync_playwright
from bots.playwright.main import BookDataExtractor
import subprocess

with sync_playwright() as playwright:
    data_extractor = BookDataExtractor(playwright,
                                       'cura quantica and energia and chakras and reiki and lei da atracao and cura natural',
                                       page_amount=1)
    data_extractor.run()

    