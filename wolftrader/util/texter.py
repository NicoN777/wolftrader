from twilio.rest import Client
from application import twilio_sid, twilio_token, receivers, sender
from .logger import *

client = Client(twilio_sid, twilio_token)


class Texter:

    def __init__(self, body):
        self.body = body

    def __enter__(self):
        for recipient in receivers:
            self.message = client.messages.create(from_=sender, to=recipient, body=self.body)

        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        log_debug(self.message.sid)
