from twilio.rest import Client
from application import twilio_sid, twilio_token, sms_recipients, sender
from .logger import *

client = Client(twilio_sid, twilio_token)


class Texter:

    def __init__(self, body):
        self.body = body

    def __enter__(self):
        for recipient in sms_recipients:
            self.message = client.messages.create(
                messaging_service_sid=sender,
                body=self.body,
                to=recipient
            )

        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        log_debug(self.message.sid)
