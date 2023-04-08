from typing import Any

from mongoengine import connect

from craigsbot.config import Configuration


def initialize_database():
    connect(
        host=f"mongodb+srv://{Configuration.DATABASE_USERNAME}:{Configuration.DATABASE_PASSWORD}@{Configuration.DATABASE_HOST}/{Configuration.DATABASE_NAME}?retryWrites=true&w=majority"
    )
