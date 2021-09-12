
from .models import User
from core.contrib.mails import send_email_async
from core.database.helpers import unique_code
from celery import shared_task
import asyncio


@shared_task(bind=True)
def send_confirmation_email(self, email: str):
    code = asyncio.run(unique_code())
    body = {
        'email': email,
        'code': code
    }
    asyncio.run(send_email_async('Confirmation', body=body, to=[
        email], template_name='mail/confirm_email.html'))


@shared_task(name="create_task")
def create_task(a, b, c):
    time.sleep(a)
    return b + c


@shared_task(
    bind=True,
    soft_time_limit=42,  # raises celery.exceptions.SoftTimeLimitExceeded inside the coroutine
    time_limit=300,  # breaks coroutine execution
)
async def my_task(self, *args, **kwargs):
    await asyncio.sleep(5)
    print('Task 1 is done')


@shared_task
async def my_simple_task(*args, **kwargs):
    await asyncio.sleep(5)
    print('Task 2 is done')
