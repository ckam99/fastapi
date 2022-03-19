
from tortoise.exceptions import ConfigurationError
from core.exceptions import DbConnectionError
from database.base import get_database
from database.helpers import generate_verify_code
from core.mails import send_email_async
from pydantic import EmailStr


async def send_confirm_mail(email: EmailStr):
    try:
        db = await get_database()
        code = await generate_verify_code(email=email)
        body = {
            'email': email,
            'code': code
        }
        await db.close()
        await send_email_async('Confirmation', body=body, to=[
            email], template_name='mail/confirm_email.html')
    except ConfigurationError:
        raise DbConnectionError(
            "Database connection: No DB associated to model")
