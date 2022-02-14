from tortoise.contrib.pydantic import pydantic_model_creator
from models import Post
from schemas import Post as PostSchema
from typing import List


class PostAPIView():
    serializer = pydantic_model_creator(Post)

    async def all(self):
        return await self.serializer.from_queryset(Post.all())

    async def create(self, credentials: PostSchema):
        user = await Post.create(**credentials.dict(exclude_unset=True))
        return self.serializer.from_orm(user)

    async def find(self, user_id: int):
        post = await Post.get(id=user_id)
        return post

    async def remove(self, user_id: int):
        post = await Post.get(id=user_id)
        await post.delete()
        return post

