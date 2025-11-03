import re
from amazon import Constants

class SearchStringToUrl:
    def __init__(self, search_string: str) -> None:
        self.search_string = search_string

    def __parse_search_string(self) -> str:
        clean_string = self.search_string.lower()
        clean_string = re.sub(r"[^\w\s]", '', clean_string)
        clean_string = re.sub(r'\s+', ' ', clean_string).strip()
        clean_string = clean_string.replace(' or ', ' + ').replace(' and ', ' + ')
        return clean_string

    def __string_to_url(self, clean_string: str, filter: str) -> str:
        query = clean_string.replace("+", "%2B").replace(" ", "+")
        url_string = f'{Constants.URL}s?k={query}{filter}'
        return url_string

    def get_url(self, filter) -> str:
        clean_string = self.__parse_search_string()
        url = self.__string_to_url(clean_string, filter)
        return url