import os


class Configuration:
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_PORT = int(os.environ.get("DATABASE_PORT"))
    DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

    CHROMEDRIVER_PATH = os.environ["CHROMEDRIVER_PATH"]
    RESULTS_FILE_PATH = os.environ["RESULTS_FILE_PATH"]
    SEARCH_RESULTS_URL = os.environ["SEARCH_RESULTS_URL"]

    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_FROM_PHONE_NUMBER = os.environ.get("TWILIO_FROM_PHONE_NUMBER")
    TWILIO_TO_PHONE_NUMBER = os.environ.get("TWILIO_TO_PHONE_NUMBER")
