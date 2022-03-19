from tortoise.contrib.pydantic import pydantic_model_creator
from core.exceptions import ModelNotfoundError
from models.message import Message
from schemas import message as schema


class MessageRepository():

    serializer = pydantic_model_creator(Message)

    async def fetch_all(self):
        return await self.serializer.from_queryset(Message.all())

    async def create(self, credential: schema.MessageIn):
        message = await Message.create(**credential.dict(exclude_unset=True))
        return self.serializer.from_orm(message)

    async def fetch_one(self, message_id: int):
        message = await Message.get(id=message_id)
        if message:
            return message
        raise ModelNotfoundError(f"No message with id:{message_id} found")

    async def update(self, message_id: int, credential: schema.Message):
        message = await Message.get(id=message_id)
        message.update_from_dict()
        return message

    async def remove(self, message_id: int):
        message = await Message.get(id=message_id)
        await message.delete()
        return message
