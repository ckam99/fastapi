
from core.exceptions import DbConnectionError
from celery import shared_task
import asyncio
from services.users import send_confirm_mail
import logging


logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_confirmation_email(self, email: str):
    try:
        asyncio.run(send_confirm_mail(email))
        return 'Confirmation email successfully sent!'
    except DbConnectionError as ex:
        return ex
    except Exception as ex:
        logger.error(ex)
        return f"Error Sending confirmation mail to {email}"
