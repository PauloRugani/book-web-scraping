from playwright.sync_api import sync_playwright

from api_bot.main import GoogleBooksAPIScraper


SEARCH_STRING = 'cura quantica and energia and chakras and reiki and lei da atracao and cura natural'
PAGE_AMOUNT = 1

type = input('type[api, google books]')
                   
if type.lower() == 'api':
    book_scraper = GoogleBooksAPIScraper(SEARCH_STRING, 16)
    book_scraper.run()
else:
    print('Não dei essa opção de robô, mano')

                    
                    
