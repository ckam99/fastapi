from tortoise.contrib.pydantic import pydantic_model_creator
from core.exceptions import ModelNotfoundError
from models.user import User
from schemas import user as schema


class UserRepository():

    serializer = pydantic_model_creator(User)

    async def fetch_all(self):
        return await self.serializer.from_queryset(User.all())

    async def create(self, credential: schema.UserInSchema):
        user = await User.create(**credential.dict(exclude_unset=True))
        return self.serializer.from_orm(user)

    async def fetch_one(self, message_id: int) -> User:
        user = await User.get(id=message_id).prefetch_related('notifications')
        if user:
            return user
        raise ModelNotfoundError(f"No user with id:{message_id} found")

    async def update(self, message_id: int, credential: schema.UserInSchema):
        user = await User.get(id=message_id)
        user.update_from_dict()
        return user

    async def remove(self, message_id: int):
        user = await User.get(id=message_id)
        await user.delete()
        return user
