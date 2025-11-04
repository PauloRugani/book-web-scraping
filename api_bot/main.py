import requests
from .constants.main import APIBotConstants
from constants.main import Constants
import pandas as pd
from typing import List, Dict
import os
import re


class GoogleBooksAPIScraper():
    def __init__(self, search_string: str, amount: str):
        self.search_string = search_string
        self.amount = amount
        self.__search_string = self.parse_search_string(search_string)


    @staticmethod
    def save_to_csv(data: List[Dict[str, str]]) -> None:
        if not os.path.exists(APIBotConstants.DB_PATH):
            os.mkdir(APIBotConstants.DB_PATH)
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(APIBotConstants.DB_PATH, 'books_data.csv'), index=False, encoding='utf-8')

    def parse_search_string(self, search_string: str) -> str:
        clean_string = search_string.lower()
        clean_string = re.sub(r"[^\w\s]", '', clean_string)
        clean_string = re.sub(r'\s+', ' ', clean_string).strip()
        clean_string = clean_string.replace(' or ', ' + ').replace(' and ', ' + ')
        return clean_string
        
    def run(self):
        url = Constants.ROUTE
        params = {
            'q': self.__search_string,
            'maxResults': self.amount,
            'printType': 'books',
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Err:", response.status_code)
            return []

        books = response.json()
        items = []
        for book in books.get('items', []):
            info = book.get('volumeInfo', {})
            items.append({
                'title': info.get('title'),
                'link': info.get('infoLink'),
                'description': info.get('description'),
                'author': info.get('authors')
            })

        GoogleBooksAPIScraper.save_to_csv(items)
