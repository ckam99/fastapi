from tortoise.contrib.pydantic import pydantic_model_creator
from core.exceptions import ModelNotfoundError
from models.notification import Notification
from schemas import notification as schema


class NotificationRepository():

    serializer = pydantic_model_creator(Notification)

    async def fetch_all(self):
        return await self.serializer.from_queryset(Notification.all().select_related('user'))

    async def create(self, credential: schema.NotificationInSchema):
        message = await Notification.create(**credential.dict(exclude_unset=True))
        return self.serializer.from_orm(message)

    async def fetch_one(self, message_id: int):
        message = await Notification.get(id=message_id).select_related('user')
        if message:
            return message
        raise ModelNotfoundError(f"No message with id:{message_id} found")

    async def update(self, message_id: int, credential: schema.NotificationSchema):
        message = await Notification.get(id=message_id)
        message.update_from_dict()
        return message

    async def remove(self, message_id: int):
        message = await Notification.get(id=message_id)
        await message.delete()
        return message
