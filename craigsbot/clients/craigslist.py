from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from craigsbot.parser import (
    CraigslistPostingParser,
    CraigslistSearchResultsParser,
)


class CraigslistClient:
    @staticmethod
    def get_page_count(driver, url: str) -> int:
        source = CraigslistClient.get_search_results_source(driver, url)
        parser = CraigslistSearchResultsParser(source)
        return parser.get_page_count()

    @staticmethod
    def get_postings_metadata(driver, url: str) -> list:
        source = CraigslistClient.get_search_results_source(driver, url)
        parser = CraigslistSearchResultsParser(source)
        return parser.get_postings_metadata()

    @staticmethod
    def get_posting_lat_long(driver, url: str) -> list:
        source = CraigslistClient.get_posting_source(driver, url)
        parser = CraigslistPostingParser(source)
        return parser.get_lat_long()

    @staticmethod
    def get_search_results_source(driver, url: str):
        driver.get(url)
        wait1 = WebDriverWait(driver, 10)
        wait1.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cl-retrieving")))
        wait1 = WebDriverWait(driver, 10)
        wait1.until(EC.presence_of_element_located((By.CLASS_NAME, 'cl-search-result')))
        return driver.page_source

    @staticmethod
    def get_posting_source(driver, url: str):
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'postingtitle')))
        return driver.page_source
