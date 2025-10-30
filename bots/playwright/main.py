from playwright.sync_api import Playwright, ElementHandle, BrowserContext
from ..constants.main import PlaywrightConstants, Constants
from typing import List, Dict
import pandas as pd
from .utils.PlaywrightHandler import PlaywrightHandler
from .utils.SearchStringToUrl import SearchStringToUrl
import os
from time import sleep

class BookDataExtractorPw:
    def __init__(self, playwright: Playwright, search_string: str, page_amount: int=30):
        self.__search_string = search_string #NOSONAR
        self.__page_amount = page_amount
        self.__playwright_handler = PlaywrightHandler(playwright)
        self.__search_string_to_url = SearchStringToUrl(search_string)

    @staticmethod
    def save_to_csv(data: List[Dict[str, str]]) -> None:
        if not os.path.exists('./bots/playwright/data'):
            os.mkdir('./bots/playwright/data')
        df = pd.DataFrame(data)
        df.to_csv('./bots/playwright/data/books_data.csv', index=False, encoding='utf-8')

    def __get_books_data(self, context: BrowserContext, book_list: List[ElementHandle]):
        books: List[Dict[str, str]] = []
        for book in book_list:
            try:
                href = book.query_selector('a').get_attribute('href')
                if not href:
                    print('Link da página não encontrada')
                    continue

                book_page = context.new_page()
                book_page.goto(Constants.URL + href)

                try:
                    book_title: str = book_page.locator(PlaywrightConstants.BOOK_TITLE).inner_text(timeout=2000)
                except Exception:
                    book_title = None

                try:
                    book_rating: str = (
                                        book_page.locator(
                                        PlaywrightConstants.BOOK_RATING)
                                        .inner_text(timeout=2000)
                                        .split('\n')[0]
                                        .strip()
                                        )
                except Exception:
                    book_rating = None

                try:
                    book_description: str = (
                                            book_page.locator(PlaywrightConstants.BOOK_DESCRIPTION)
                                            .inner_text(timeout=2000) 
                                            .replace('\n', '')[:200]
                                            ) 
                except Exception:
                    book_description = None

                try:
                    contributions: str = book_page.query_selector_all(PlaywrightConstants.BOOK_CONTRIBUTIONS)
                    len_contributions = len(contributions)
                    list_authors = (
                                    [book_page.locator(f'//*[@id="bylineInfo"]/span[{i}]/a').inner_text(timeout=2000)
                                    for i in range(1, len_contributions + 1)] 
                                    if len_contributions > 1 
                                    else [book_page.locator('//*[@id="bylineInfo"]/span/a').inner_text(timeout=2000)]
                                    )
                except Exception:
                    list_authors = []

                books.append({
                    'title': book_title,
                    'rating': book_rating,
                    'description': book_description,
                    'author': list_authors
                })

            except Exception as e:
                print(f'{e}')
            
            finally:
                book_page.close()

        return books

    def run(self) -> None:
        sleep(0.5)
        items: List[Dict[str, str]] = []
        site_page: int = 1

        while site_page <= self.__page_amount:
            self.__playwright_handler.page.goto(self.__search_string_to_url.get_url(f'&i=stripbooks&page={site_page}'))
                                    
            elements = self.__playwright_handler.page.query_selector_all(PlaywrightConstants.BOOKS_LIST)
            if not elements:
                break

            books_data = self.__get_books_data(context=self.__playwright_handler.context, book_list=elements)
            items.extend(books_data)

            total_books = self.__playwright_handler.page.locator(PlaywrightConstants.PAGE_AMOUNT_BOOK).inner_text().split(' ')[2]
            if len(books_data) >= int(total_books):
                print('Todos os livros da busca obtidos!')
                break

            site_page += 1

        BookDataExtractorPw.save_to_csv(items)

        self.__playwright_handler.context.close()
        self.__playwright_handler.browser.close()
