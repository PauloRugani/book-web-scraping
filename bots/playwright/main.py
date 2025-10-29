import re
from playwright.sync_api import Playwright, sync_playwright, ElementHandle, Page, BrowserContext
from time import sleep
from .constants.PlaywrightConstant import PlaywrightConstant
from typing import List, Dict, Any
import pandas as pd

def parse_search_string(search_string: str) -> str:
    search_string = search_string.lower()
    search_string = re.sub(r"[^\w\s]", '', search_string)
    search_string = re.sub(r'\s+', ' ', search_string).strip()
    search_string = search_string.replace(' or ', ' + ').replace(' and ', ' + ')
    return search_string

def string_to_url(base_url: str, parse_search_string: str, filter: str = '') -> str:
    url_string = base_url + f's?k={parse_search_string.replace("+", "%2B").replace(" ", "+")}' + filter
    return url_string

def save_to_csv(data: List[Dict[str, str]]) -> None:
    df = pd.DataFrame(data)
    df.to_csv(r'./books/books_data.csv', index=False, encoding='utf-8')

def get_book_data(context: BrowserContext, book_list: List[ElementHandle]):
    books: List[Dict[str, str]] = []
    for book in book_list:
        try:
            href = book.query_selector('a').get_attribute('href') # vai para a pagina do livro
            
            book_page = context.new_page()
            book_page.goto(PlaywrightConstant.URL + href)

            try:
                book_title: str = book_page.locator(PlaywrightConstant.BOOK_TITLE).inner_text(timeout=2000)
            except Exception:
                book_title = None

            try:
                book_rating: str = book_page.locator(PlaywrightConstant.BOOK_RATING).inner_text(timeout=2000).split('\n')[0].strip()
            except Exception:
                book_rating = None

            try:
                book_description: str = book_page.locator(PlaywrightConstant.BOOK_DESCRIPTION).inner_text(timeout=2000)
            except Exception:
                book_description = None

            try:
                book_author: str = book_page.locator(PlaywrightConstant.BOOK_AUTHOR).inner_text(timeout=2000)
            except Exception:
                book_author = None

            book_data: Dict[str, str] = {
                'title': book_title,
                'rating': book_rating,
                'description': book_description,
                'author': book_author
            }

            books.append(book_data)
        except Exception as e:
            print(f'pqp ta entrnado aqui {e}')
        
        finally:
            book_page.close()

    return books

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    items: List[Dict[str, str]] = []
    for i in range(1, 4):
        page.goto(string_to_url(PlaywrightConstant.URL, 
             parse_search_string('cura quantica and energia and chakras and reiki and lei da atracao and cura natural'), f'&i=stripbooks&page={i}'))
    
        elementos = page.query_selector_all(PlaywrightConstant.BOOKS_LIST) # por algum motivo so pega 16
        book_data = get_book_data(context=context, book_list=elementos)
        items = items + book_data

    save_to_csv(items)

    context.close()
    browser.close()
