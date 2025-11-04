import requests
from .constants.main import APIBotConstants
from constants.main import Constants
import pandas as pd
from typing import List, Dict
import os
import re


class GoogleBooksFetcher():
    def __init__(self, search_string: str, amount: int):
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
        clean_string = clean_string.replace(' or ', ' OR ').replace(' and ', ' AND ')
        return clean_string
        
    def run(self):
        url = Constants.ROUTE
        all_items: List[Dict[str, str]] = []

        if self.amount <= 0:
            return all_items

        start_index = 0
        MAX_REQUEST = 40

        while len(all_items) < self.amount:
            params = {
                'q': self.__search_string,
                'maxResults': min(MAX_REQUEST, self.amount - len(all_items)),
                'startIndex': start_index,
                'printType': 'books',
            }

            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(response.status_code)
                break

            books = response.json()
            temp_list = []
            for book in books.get('items', []):
                info = book.get('volumeInfo', {})
                temp_list.append({
                    'title': info.get('title'),
                    'link': info.get('infoLink'),
                    'description': info.get('description'),
                    'author': info.get('authors')
                })

            if not temp_list:
                break

            all_items.extend(temp_list)
            start_index += len(temp_list)

        GoogleBooksFetcher.save_to_csv(all_items)
