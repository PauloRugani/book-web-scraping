from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class SeleniumHandler:
    def __init__(self, driver_url: str):
        self.driver_url = driver_url
        self.driver: webdriver.Chrome = self.__init_selenium()

    def __init_selenium(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_service = Service(self.driver_url)  # usa o chromedriver do PATH
        
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        return driver