from fastapi_mailman.config import ConnectionConfig
from fastapi_mailman import Mail, EmailMessage, EmailStr
from core.settings import *


config = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_BACKEND=MAIL_BACKEND,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_PORT=MAIL_PORT,
    MAIL_DEFAULT_SENDER=MAIL_FROM
)
if MAIL_USE_TLS:
    config.MAIL_USE_TLS = MAIL_USE_TLS
if MAIL_USE_SSL:
    config.MAIL_USE_SSL = MAIL_USE_SSL

mail = Mail(config)


def mailer(subject: str, body: str, sender: EmailStr, to: list[EmailStr], as_html: bool = True, *args, **kwargs) -> EmailMessage:
    msg = EmailMessage(
        mailman=mail,
        subject=subject,
        body=body,
        from_email=sender,
        to=to,
        *args, **kwargs
    )
    if as_html:
        msg.content_subtype = "html"
    return msg


async def send_mail(subject, body, sender: EmailStr, to: list[EmailStr] = [], as_html: bool = True, *args, **kwargs):
    msg = mailer(subject, body, sender, to,  as_html, *args, **kwargs)
    return await msg.send()


async def push_mail(messages: list[EmailMessage]):
    async with mail.get_connection() as conn:
        for m in messages:
            m.connection = conn
        await conn.send_messages(messages)
