
from .models import User
from core.contrib.mails import send_email_async
from core.database.helpers import unique_code


async def send_confirmation_email(user: User):
    body = {
        'email': user.email,
        'code': await unique_code()
    }
    await send_email_async('Welcome', body=body, to=[user.email], template_name='mail/confirm_email.html')
