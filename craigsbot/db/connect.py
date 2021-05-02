from typing import Any

import mongoengine

from craigsbot.config import Configuration


def initialize_database() -> Any:
    return mongoengine.connect(db=Configuration.DATABASE_NAME, host=Configuration.DATABASE_HOST,
                               port=Configuration.DATABASE_PORT)
