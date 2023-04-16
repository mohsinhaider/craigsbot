import datetime
import os
import pytz
import sys
import time

craig_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(craig_path)

import logging
import random
import time

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
timezone = pytz.timezone('US/Pacific')


def start_application() -> None:
    initialize_database()
    driver = setup_selenium()
    process_postings(driver)


def setup_selenium():
    driver_path = Configuration.CHROMEDRIVER_PATH
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Comment out below on server
    # chrome_options.add_argument("--no-sandbox")

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
    counter = 0
    number_of_pages = CraigslistClient.get_page_count(driver, search_results_url)

    # Get date data for results file name so that it doesn't keep changing
    now = datetime.datetime.now(timezone)
    regular_time = now.strftime("%I:%M%p")
    date = now.date()
    count_new_postings = 0

    for i in range(number_of_pages):
        if i != 0:
            if count_new_postings > 10:
                r = random.uniform(100, 120)
            else:
                r = random.uniform(5, 6)
            count_new_postings = 0
            time.sleep(r)
            search_results_url = search_results_url.replace(f"thumb~{i-1}", f"thumb~{i}")

        postings_metadata = CraigslistClient.get_postings_metadata(driver, search_results_url)
        if len(postings_metadata) == 0:
            # Craigslist isn't returning results to sleep for 3 minutes and then try again
            time.sleep(180)
            postings_metadata = CraigslistClient.get_postings_metadata(driver, search_results_url)

        for posting_metadata in postings_metadata:
            print(counter)
            counter += 1
            posting_data_id = posting_metadata["data-id"].strip()
            file1 = open(f"{Configuration.RESULTS_FILE_PATH}/{regular_time}-{date}.txt", "a")
            try:
                Posting.objects.get(data_id=posting_data_id)
                file1.write(f"{counter} Already seen\n")
                continue
            except DoesNotExist:
                posting_url = posting_metadata["href"]
                logger.info(f"Encountered candidate new posting: {posting_url}")
                count_new_postings += 1

            random_num = random.uniform(0.6, 0.9)
            time.sleep(random_num)
            lat, long = map(lambda c: float(c), CraigslistClient.get_posting_lat_long(driver, posting_url))
            found_in_boundary = False
            for boundary in boundaries:
                if is_coordinate_in_boundary(lat, long, boundary):
                    found_in_boundary = True
                    sms_message = f"Craigsbot found a new apartment: {posting_url}"
                    print(f"Encountered posting inside of boundary {posting_url}")
                    try:
                        print("Sending sms")
                        file1.write(f"{counter} {posting_url}\n")
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
                            is_in_boundary=True,
                        ).save()
                        break

            if not found_in_boundary:
                file1.write(f"{counter} Out of boundary\n")
                logger.info(f"Encountered posting outside of boundary: {posting_url}")
                Posting(
                    data_id=posting_data_id,
                    url=posting_url,
                    latitude=lat,
                    longitude=long,
                    is_in_boundary=False,
                ).save()
            file1.close()

    driver.quit()
    logger.info(f"Found {counter} posts during this run")


if __name__ == "__main__":
    start_application()
