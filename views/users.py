
from tortoise.contrib.pydantic import pydantic_model_creator
from schemas.auth import RegisterSchema
from models.auth import User


class UserAPIView():
    serializer = pydantic_model_creator(User)

    async def all(self):
        return await self.serializer.from_queryset(User.all())

    async def create(self, credentials: RegisterSchema):
        user = await User.create(**credentials.dict(exclude_unset=True))
        return self.serializer.from_orm(user)

    async def find(self, user_id: int):
        user = await User.get(id=user_id).prefetch_related('posts')
        data = user.__dict__
        data['posts'] = await user.posts
        return data

    # async def get_posts(self, user_id: int):
    #     posts = await Post.filter(user_id=user_id).all()
    #     return posts
