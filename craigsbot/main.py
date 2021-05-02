import logging

from dotenv import load_dotenv
load_dotenv()

from mongoengine import DoesNotExist

from craigsbot.boundary import (
    create_boundary,
    is_coordinate_in_boundary,
)
from craigsbot.clients import CraigslistClient
from craigsbot.config import Configuration
from craigsbot.db import initialize_database
from craigsbot.exceptions import SMSSendFailureException
from craigsbot.models import Posting
from craigsbot.sms import (
    create_sms_client,
    send_sms_message,
)


logger = logging.getLogger(__name__)


def start_application() -> None:
    initialize_database()
    process_postings()


def process_postings() -> None:
    search_results_urls = CraigslistClient.get_all_search_results_page_urls(Configuration.SEARCH_RESULTS_URL)
    boundary = create_boundary()
    counter = 0

    for search_results_url in search_results_urls:
        postings_metadata = CraigslistClient.get_postings_metadata(search_results_url)
        for posting_metadata in postings_metadata:
            counter += 1
            posting_data_id = posting_metadata["data-id"].strip()
            try:
                Posting.objects.get(data_id=posting_data_id)
                continue
            except DoesNotExist:
                posting_url = posting_metadata["href"]
                logger.info(f"Encountered candidate new posting: {posting_url}")

            lat, long = map(lambda c: float(c), CraigslistClient.get_posting_lat_long(posting_url))
            if is_coordinate_in_boundary(lat, long, boundary):
                sms_message = f"Craigsbot found a new apartment: {posting_url}"
                try:
                    sms_client = create_sms_client()
                    send_sms_message(
                        number=Configuration.TWILIO_TO_PHONE_NUMBER,
                        message=sms_message,
                        client=sms_client,
                    )
                except Exception as e:
                    logger.error("Failed to send message")
                    raise SMSSendFailureException from e
                else:
                    Posting(
                        data_id=posting_data_id,
                        url=posting_url,
                        latitude=lat,
                        longitude=long,
                    ).save()
            else:
                logger.info(f"Encountered posting outside of boundary: {posting_url}")

    logger.info(f"Found {counter} posts during this run")


start_application()
