import logging

from django.conf import settings
from twilio.rest import Client


logger = logging.getLogger(__name__)


def send_order_sms(phone_number, order_id):
    if not phone_number or not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_PHONE_NUMBER:
        return None

    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )

    try:
        message = client.messages.create(
            body=f"Your order #{order_id} has been placed successfully!",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=str(phone_number),
        )
        return message.sid
    except Exception:
        logger.exception("Failed to send order SMS for order %s", order_id)
        return None
