from playwright.sync_api import sync_playwright

from api_fetcher.main import GoogleBooksFetcher


SEARCH_STRING = 'cura quantica OR energia OR chakras OR reiki OR lei da atracao OR cura natural'
PAGE_AMOUNT = 1

type = input('type[api, google books]')
                   
if type.lower() == 'api':
    book_scraper = GoogleBooksFetcher(SEARCH_STRING, 50)
    book_scraper.run()
else:
    print('Não dei essa opção de robô, mano')

                    
                    
