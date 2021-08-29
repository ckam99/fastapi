
from .models import User
from core.contrib.mails import send_email_async


async def send_confirmation_email(user: User):
    body = {
        'email': user.email
    }
    await send_email_async('Welcome', body=body, to=[user.email], template_name='mails/test.html')
