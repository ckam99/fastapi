from core.database import get_database
from tortoise.transactions import in_transaction
from models import Post
import json


class PostService:

    @staticmethod
    async def save_post(payload):
        data: dict = json.loads(payload)
        db = await get_database()
        async with in_transaction() as connection:
            post = Post(**data)
            await post.save(using_db=connection)
            # post = await connection.execute_query_dict('INSERT INTO post (id, title,body,image) VALUES (?, ?, ?, ?)', [
            #     data.get('id'),
            #     data.get('title'),
            #     data.get('body'),
            #     data.get('image')
            # ])
        await db.close()
