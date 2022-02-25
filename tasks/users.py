
# from core.mails import send_email_async
from database.helpers import unique_code
from celery import shared_task


@shared_task(bind=True)
def send_confirmation_email(self, email: str):
    try:
        code = unique_code()
        body = {
            'email': email,
            'code': code
        }
        # send_email_async('Confirmation', body=body, to=[
        #     email], template_name='mail/confirm_email.html')
        return 'Done!'
    except Exception:
        return 'Error sending confirmation email'
