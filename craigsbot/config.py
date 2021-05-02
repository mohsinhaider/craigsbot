import os


class Configuration:
    COORDINATES = os.environ.get("COORDINATES")

    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_PORT = int(os.environ.get("DATABASE_PORT"))

    SEARCH_RESULTS_URL = os.environ.get("SEARCH_RESULTS_URL")

    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_FROM_PHONE_NUMBER = os.environ.get("TWILIO_FROM_PHONE_NUMBER")
    TWILIO_TO_PHONE_NUMBER = os.environ.get("TWILIO_TO_PHONE_NUMBER")
