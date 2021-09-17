
from tortoise.contrib.pydantic import pydantic_model_creator
import schemas
from models import Post, User


class UserAPIView():
    serializer = pydantic_model_creator(User)

    async def all(self):
        return await self.serializer.from_queryset(User.all())

    async def create(self, payload: schemas.UserInSchema):
        user = await User.create(**payload.dict(exclude_unset=True))
        return self.serializer.from_orm(user)

    async def find(self, user_id: int):
        return await self.serializer.from_queryset_single(User.get(id=user_id))


class PostAPIView():

    serializer = pydantic_model_creator(Post)

    async def all(self):
        posts = await Post.all().prefetch_related('user')
        return posts

    async def create(self, payload: schemas.PostInSchema):
        post_obj = await Post.create(**payload.dict(exclude_unset=True))
        return post_obj

    async def find(self, post_id: int):
        post = await Post.get(id=post_id).select_related('user')
        return post
