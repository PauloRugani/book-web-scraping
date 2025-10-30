from playwright.sync_api import sync_playwright
from bots.playwright.main import BookDataExtractorPw
from bots.selenium.main import BookDataExtractorSel

bot = input('bot[selenium, playwright]: ')
match bot:
    case 'selenium':
        data_extractor = BookDataExtractorSel(r'C:\Users\phrug\OneDrive\Documentos\Repositórios\book-web-scraping\bots\selenium\driver\chromedriver.exe',
                                'cura quantica and energia and chakras and reiki and lei da atracao and cura natural',
                                page_amount=1)
        data_extractor.run()  

    case 'playwright':
        with sync_playwright() as playwright:
            data_extractor = BookDataExtractorPw(playwright,
                                            'cura quantica and energia and chakras and reiki and lei da atracao and cura natural',
                                            page_amount=1)
            data_extractor.run()

    case _:
        print('não dei essa opção, mano')

