class SeleniumConstant:
    URL: str = 'https://www.amazon.com.br/'
    BOOKS_LIST: str = "//*[@role='listitem']"
    BOOK_TITLE: str = 'productTitle'
    BOOK_RATING: str = 'acrPopover'
    BOOK_DESCRIPTION: str = 'bookDescription_feature_div'
    BOOK_AUTHOR: str = 'bylineInfo'
    BOOK_CONTRIBUTIONS: str = "contribution"
    PAGE_AMOUNT_BOOK: str = '//*[@id="search"]/span/div/h1/div/div[1]/div/div/div[2]/h2/span[1]'
