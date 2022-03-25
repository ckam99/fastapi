from typing import Any, Dict, List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from core import settings
from pydantic import EmailStr
# from asgiref.sync import sync_to_async


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_TLS=settings.MAIL_USE_TLS,
    MAIL_SSL=settings.MAIL_USE_SSL,
    USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
    VALIDATE_CERTS=settings.MAIL_VALIDATE_CERTS,
    TEMPLATE_FOLDER='resources/templates'
)


async def send_email_async(subject: str, body: Dict[str, Any], to: List[EmailStr], template_name=str):
    message = MessageSchema(
        subject=subject,
        recipients=to,
        template_body=body,
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_name)


async def send_push_email(subject: str, body: Dict[str, Any], to: List[EmailStr], template_name=None):
    for receiver in to:
        await send_email_async(subject=subject, body=body, to=[receiver], template_name=template_name)
