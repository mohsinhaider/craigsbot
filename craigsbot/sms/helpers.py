from typing import Any

from twilio.rest import Client

from craigsbot.config import Configuration


def create_sms_client() -> Client:
    return Client(Configuration.TWILIO_ACCOUNT_SID, Configuration.TWILIO_AUTH_TOKEN)


def send_sms_message(number: str, message: str, client: Client) -> Any:
    return client.messages.create(
        to=number,
        from_=Configuration.TWILIO_FROM_PHONE_NUMBER,
        body=message,
    )
