
from tortoise.contrib.pydantic import pydantic_model_creator
from schemas.posts import PostInSchema
from schemas.users import UserInSchema
from models.base import Post, User


class UserAPIView():
    serializer = pydantic_model_creator(User)

    async def all(self):
        return await self.serializer.from_queryset(User.all())

    async def create(self, payload: UserInSchema):
        user = await User.create(**payload.dict(exclude_unset=True))
        return self.serializer.from_orm(user)

    async def find(self, user_id: int):
        user = await User.get(id=user_id).prefetch_related('posts')
        data = user.__dict__
        data['posts'] = await user.posts
        return data

    async def get_posts(self, user_id: int):
        posts = await Post.filter(user_id=user_id).all()
        return posts


class PostAPIView():
    async def all(self):
        posts = await Post.all().prefetch_related('user')
        return posts

    async def create(self, payload: PostInSchema):
        post_obj = await Post.create(**payload.dict(exclude_unset=True))
        return post_obj

    async def find(self, post_id: int):
        post = await Post.get(id=post_id).select_related('user')
        return post
