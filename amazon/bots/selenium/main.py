import os
import pandas as pd
from typing import List, Dict
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .utils.SeleniumHandler import SeleniumHandler
from amazon import SeleniumConstants, SearchStringToUrl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

# print(SeleniumConstants.CHROME_DRIVER_PATH)
class AmazonBookExtractorSel:
    def __init__(self, search_string: str, page_amount: int=30):
        self.__page_amount = page_amount
        self.__selenium_handler = SeleniumHandler(SeleniumConstants.CHROME_DRIVER_PATH)
        self.__search_string_to_url = SearchStringToUrl(search_string)

    @staticmethod
    def save_to_csv(data: List[Dict[str, str]]) -> None:
        if not os.path.exists('./amazon/bots/selenium/data'):
            os.mkdir('./amazon/bots/selenium/data')
        df = pd.DataFrame(data)
        df.to_csv('./amazon/bots/selenium/data/books_data.csv', index=False, encoding='utf-8')

    def __get_books_data(self, book_list: List[WebElement]):
        books: List[Dict[str, str]] = []
        for book in book_list:
            try:
                href = WebDriverWait(book, 10).until(
                    EC.element_to_be_clickable((By.TAG_NAME, "a"))
                )

                ActionChains(self.__selenium_handler.driver) \
                    .key_down(Keys.CONTROL) \
                    .click(href) \
                    .key_up(Keys.CONTROL) \
                    .perform()

                self.__selenium_handler.driver.switch_to.window(self.__selenium_handler.driver.window_handles[-1])

                try:
                    book_title = WebDriverWait(self.__selenium_handler.driver, 10).until(
                        EC.presence_of_element_located((By.ID, SeleniumConstants.BOOK_TITLE))
                    ).text
                except Exception:
                    book_title = None

                try:
                    book_rating: str = (WebDriverWait(self.__selenium_handler.driver, 10).until(
                        EC.presence_of_element_located((By.ID, SeleniumConstants.BOOK_RATING))
                                        ).text
                                         .split('\n')[0]
                                         .strip()
                                         )
                except Exception:
                    book_rating = None

                try:
                    book_description: str = (WebDriverWait(self.__selenium_handler.driver, 10).until(
                        EC.presence_of_element_located((By.ID, SeleniumConstants.BOOK_DESCRIPTION))
                                        ).text
                                         .replace('\n', '')[:200]
                                         ) 
                except Exception:
                    book_description = None

                try:
                    contributions: str = self.__selenium_handler.driver.find_elements(By.CLASS_NAME, SeleniumConstants.BOOK_CONTRIBUTIONS)
                    len_contributions = len(contributions)
                    list_authors = (
                                    [self.__selenium_handler.driver.find_element(By.XPATH, f'//*[@id="bylineInfo"]/span[{i}]/a').text
                                    for i in range(1, len_contributions + 1)] 
                                    if len_contributions > 1 
                                    else [self.__selenium_handler.driver.find_element(By.XPATH, '//*[@id="bylineInfo"]/span/a').text]
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
                self.__selenium_handler.driver.close()
                self.__selenium_handler.driver.switch_to.window(self.__selenium_handler.driver.window_handles[0])

        return books

    def run(self):
        items: List[Dict[str, str]] = []
        site_page: int = 1

        while site_page <= self.__page_amount:
            self.__selenium_handler.driver.get(self.__search_string_to_url.get_url(f'&i=stripbooks&page={site_page}'))

            div = WebDriverWait(self.__selenium_handler.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )

            elements = div.find_elements(By.XPATH, SeleniumConstants.BOOKS_LIST)
            if not elements:
                break

            books_data = self.__get_books_data(book_list=elements)
            items.extend(books_data)

            total_books = self.__selenium_handler.driver.find_element(By.XPATH, SeleniumConstants.PAGE_AMOUNT_BOOK).text.split(' ')[2]
            if len(books_data) >= int(total_books):
                print('Todos os livros da busca obtidos!')
                break

            site_page += 1

        AmazonBookExtractorSel.save_to_csv(items)

        self.__selenium_handler.driver.close()


