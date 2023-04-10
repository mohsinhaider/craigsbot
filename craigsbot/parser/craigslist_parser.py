import math

from bs4 import BeautifulSoup

from craigsbot.exceptions import MissingGeographicDataException


class CraigslistSearchResultsParser(BeautifulSoup):
    def __init__(self, markup):
        BeautifulSoup.__init__(self, markup, 'html.parser')

    def get_next_search_results_url(self) -> str:
        head_tag = self.find("head")
        next_link_tag = head_tag.find("link", {"rel": "next"})
        if not next_link_tag:
            return

        return next_link_tag.get("href")

    def get_postings_metadata(self) -> list:
        ids_and_links = []
        li_tags = self.find_all(class_="cl-search-result cl-search-view-mode-thumb")
        for li_tag in li_tags:
            div_tag = li_tag.findChild("div", {"class": "result-node"})
            a_tag = div_tag.findChild("a", {"class": "result-thumb"})
            ids_and_links.append({
                "data-id": li_tag["data-pid"],
                "href": a_tag["href"]
            })
        return ids_and_links

    def get_page_count(self):
        page_number = self.find(class_="cl-page-number").text
        page_number_tokens = page_number.split(" ")
        results_per_page = page_number_tokens[2]
        total_results = page_number_tokens[4]
        if "," in total_results:
            total_results = total_results.replace(",", "")
        return math.ceil(int(total_results) / int(results_per_page))


class CraigslistPostingParser(BeautifulSoup):
    def __init__(self, markup):
        BeautifulSoup.__init__(self, markup, 'html.parser')

    def get_lat_long(self) -> list:
        head_tag = self.find("head")
        meta_geo_tag = head_tag.find("meta", {"name": "geo.position"})
        if not meta_geo_tag:
            url = self._get_url()
            raise MissingGeographicDataException(f"Missing meta geo tag for posting {url}")

        return meta_geo_tag.get("content").split(";")

    def _get_url(self) -> str:
        head_tag = self.find("head")
        meta_url_tag = head_tag.find("meta", {"property": "og:url"})
        return meta_url_tag["content"]
