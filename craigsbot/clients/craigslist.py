import requests

from craigsbot.parser import (
    CraigslistPostingParser,
    CraigslistSearchResultsParser,
)


class CraigslistClient:
    @staticmethod
    def get_all_search_results_page_urls(base_url: str) -> str:
        search_results_url = base_url
        search_results_urls = [search_results_url]

        while True:
            content = CraigslistClient.get_content(search_results_url)
            parser = CraigslistSearchResultsParser(content)
            search_results_url = parser.get_next_search_results_url()
            if not search_results_url:
                break

            search_results_urls.append(search_results_url)

        return search_results_urls

    @staticmethod
    def get_postings_metadata(url: str) -> list:
        content = CraigslistClient.get_content(url)
        parser = CraigslistSearchResultsParser(content)
        return parser.get_postings_metadata()

    @staticmethod
    def get_posting_lat_long(url: str) -> list:
        content = CraigslistClient.get_content(url)
        parser = CraigslistPostingParser(content)
        return parser.get_lat_long()

    @staticmethod
    def get_content(url: str) -> str:
        response = requests.get(url)
        return response.content.decode("utf-8")
