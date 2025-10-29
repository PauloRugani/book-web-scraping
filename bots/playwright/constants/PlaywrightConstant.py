class PlaywrightConstant:
    URL: str = 'https://www.amazon.com.br/'
    BOOKS_LIST: str = '[role="listitem"]'
    BOOK_TITLE: str = '[id="productTitle"]'
    BOOK_RATING: str = '//*[@id="averageCustomerReviews"]'
    BOOK_DESCRIPTION: str = '[id="bookDescription_feature_div"]'
    BOOK_AUTHOR: str = '//*[@id="bylineInfo"]'