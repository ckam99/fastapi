

from core.database import get_database
from tortoise.transactions import in_transaction
from models.message import Message
import json


async def save_message_from_dict(payload):
    data: dict = json.loads(payload)
    async with get_database() as db:
        async with in_transaction() as connection:
            post = Message(**data)
            await post.save(using_db=connection)
            # post = await connection.execute_query_dict('INSERT INTO post (id, title,body,image) VALUES (?, ?, ?, ?)', [
            #     data.get('id'),
            #     data.get('title'),
            #     data.get('body'),
            #     data.get('image')
            # ])
        await db.close()
