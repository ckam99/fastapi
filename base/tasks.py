
from .models import User
from core.contrib.mails import send_email_async
from core.database.helpers import unique_code
from celery import shared_task


@shared_task(bind=True)
def send_confirmation_email(self, email: str):
    try:
        code = unique_code()
        print('code====', code)
        body = {
            'email': email,
            'code': code
        }
        send_email_async('Confirmation', body=body, to=[
            email], template_name='mail/confirm_email.html')
    except Exception as e:
        print("ASS :", e)


@shared_task(name="create_task")
def create_task(a, b, c):
    time.sleep(a)
    return b + c
