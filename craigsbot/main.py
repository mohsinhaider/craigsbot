import os
import sys

craig_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(craig_path)

import logging

from dotenv import load_dotenv
load_dotenv()

from mongoengine import DoesNotExist

from craigsbot.boundary import (
    create_boundaries,
    is_coordinate_in_boundary,
)
from craigsbot.clients import CraigslistClient
from craigsbot.config import Configuration
from craigsbot.db import initialize_database
# from craigsbot.exceptions import SMSSendFailureException
from craigsbot.models import Posting
# from craigsbot.sms import (
#     create_sms_client,
#     send_sms_message,
# )
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)


# TODO:  Compare results between these two
# (No hood filters): https://sfbay.craigslist.org/search/sfc/apa?max_bedrooms=4&max_price=6000&min_bedrooms=2&min_price=3500#search=1~thumb~0~0
# hood filters: https://sfbay.craigslist.org/search/sfc/apa?max_bedrooms=4&max_price=6000&min_bedrooms=2&min_price=3500&nh=12&nh=17&nh=18#search=1~thumb~0~0

def start_application() -> None:
    initialize_database()
    driver = setup_selenium()
    process_postings(driver)


def setup_selenium():
    driver_path = Configuration.CHROMEDRIVER_PATH
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Create a new Chrome driver
    driver = webdriver.Chrome(
        executable_path=driver_path,
        chrome_options=chrome_options
    )

    return driver


def process_postings(driver) -> None:
    boundaries = create_boundaries()
    counter = 0
    search_results_url = Configuration.SEARCH_RESULTS_URL

    number_of_pages = CraigslistClient.get_page_count(driver, search_results_url)
    for i in range(number_of_pages):
        if i != 0:
            search_results_url = search_results_url.replace(f"thumb~{i-1}", f"thumb~{i}")

        postings_metadata = CraigslistClient.get_postings_metadata(driver, search_results_url)

        for posting_metadata in postings_metadata:
            posting_data_id = posting_metadata["data-id"].strip()
            try:
                Posting.objects.get(data_id=posting_data_id)
                continue
            except DoesNotExist:
                posting_url = posting_metadata["href"]
                logger.info(f"Encountered candidate new posting: {posting_url}")

            counter += 1
            lat, long = map(lambda c: float(c), CraigslistClient.get_posting_lat_long(driver, posting_url))
            for boundary in boundaries:
                if is_coordinate_in_boundary(lat, long, boundary):
                    sms_message = f"Craigsbot found a new apartment: {posting_url}"
                    print(f"Encountered posting inside of boundary {posting_url}")
                    try:
                        print("Sending sms")
                    except Exception as e:
                        print("Error sending sms")
                        # logger.error("Failed to send message")
                        # raise SMSSendFailureException from e
                    else:
                        Posting(
                            data_id=posting_data_id,
                            url=posting_url,
                            latitude=lat,
                            longitude=long,
                        ).save()
                else:
                    print(f"Encountered posting outside of boundary: {posting_url}")
                    Posting(
                        data_id=posting_data_id,
                        url=posting_url,
                        latitude=lat,
                        longitude=long,
                    ).save()

    driver.quit()
    logger.info(f"Found {counter} posts during this run")


if __name__ == "__main__":
    print("in here")
    start_application()
