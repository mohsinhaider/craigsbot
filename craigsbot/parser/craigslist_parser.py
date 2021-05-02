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
        metadata = []
        a_tags = self.find_all("a", {"class": "result-title hdrlnk"})
        for a_tag in a_tags:
            metadata.append({
                "data-id": a_tag["data-id"],
                "href": a_tag["href"]
            })

        return metadata


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
