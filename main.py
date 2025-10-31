from playwright.sync_api import sync_playwright

from amazon.bots.playwright.main import AmazonBookExtractorPw
from amazon.bots.selenium.main import AmazonBookExtractorSel

SEARCH_STRING = 'cura quantica and energia and chakras and reiki and lei da atracao and cura natural'
PAGE_AMOUNT = 1

website = input('website[amazon, google]')
bot = input('bot[selenium, playwright]: ')

if website.lower() == 'amazon':
    if bot.lower() == 'selenium':
        book_scraper = AmazonBookExtractorSel(SEARCH_STRING, PAGE_AMOUNT)
        book_scraper.run()
    elif bot.lower() == 'playwright':
        with sync_playwright() as playwright:
            book_scraper = AmazonBookExtractorPw(playwright, SEARCH_STRING, PAGE_AMOUNT)
            book_scraper.run()
    else:
        print('Não dei essa opção de site, mano')
                   
elif website.lower() == 'google':
    if bot.lower() == 'selenium':
        book_scraper = AmazonBookExtractorSel(SEARCH_STRING, PAGE_AMOUNT)
        book_scraper.run()
    elif bot.lower() == 'playwright':
        with sync_playwright() as playwright:
            book_scraper = AmazonBookExtractorPw(playwright, SEARCH_STRING, PAGE_AMOUNT)
            book_scraper.run()
    else:
        print('Não dei essa opção de robô, mano')

else:
    print('Não dei essa opção de site, mano')
                    
                    
