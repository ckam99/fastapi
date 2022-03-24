

from core.database import get_database
from tortoise.transactions import in_transaction
from models.notification import Notification
import json


async def create_notification_from_event(payload: str):
    data: dict = json.loads(payload)
    async with get_database() as db:
        async with in_transaction() as connection:
            instance = Notification(**data)
            await instance.save(using_db=connection)
        await db.close()


async def update_user_from_event(payload: str):

    payload: dict = json.loads(payload)
    user_data = payload['data']
    db = await get_database()
    async with in_transaction('default') as connection:
        user = User(**user_data)
        await user.save(using_db=connection)
    await db.close()
