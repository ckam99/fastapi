

from core.database import get_database
from tortoise.transactions import in_transaction
from models.event import Event
import json


async def save_event_from_source(payload: str, event_name: str):
    data: dict = json.loads(payload)
    db = await get_database()
    async with in_transaction('default') as connection:
        instance = Event(
            title=event_name,
            description=data.get('description', None),
            source=data.get('source'),
            payload=data.get('data')
        )
        await instance.save(using_db=connection)
    await db.close()
