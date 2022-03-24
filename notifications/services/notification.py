

from core.database import get_database
from tortoise.transactions import in_transaction
from models.notification import Notification
import json
from core.mailer import send_email_async


async def confirme_user_account(payload: str):

    payload: dict = json.loads(payload)
    data: dict = payload.get('data')

    db = await get_database()
    async with in_transaction('default') as connection:
        body = {
            'email': data.get('email'),
            'code': payload.get('code'),
        }
        notify = Notification(
            title='Registration',
            source=payload.get('source'),
            body=body,
            user_id=data.get('id')
        )
        await send_email_async(f"Welcome {data.get('firstname')}", body=body, to=[data.get('email')], template_name='mail/confirm_email.html')
        await notify.save(using_db=connection)
        print("email successfully sent!")
    await db.close()
