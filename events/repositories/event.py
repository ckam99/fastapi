from tortoise.contrib.pydantic import pydantic_model_creator
from core.exceptions import ModelNotfoundError
from models.event import Event
from schemas import event as schema


class EventRepository():

    serializer = pydantic_model_creator(Event)

    async def fetch_all(self, limit: int = 100, offset: int = 0, *args, **kwargs):
        queryset = Event.filter(
            *args, **kwargs).limit(limit).offset(offset).all()
        return await self.serializer.from_queryset(queryset)

    async def create(self, credential: schema.EventInSchema):
        message = await Event.create(**credential.dict(exclude_unset=True))
        return self.serializer.from_orm(message)

    async def fetch_one(self, message_id: int):
        message = await Event.get(id=message_id)
        if message:
            return message
        raise ModelNotfoundError(f"No message with id:{message_id} found")

    async def update(self, message_id: int, credential: schema.EventSchema):
        message = await Event.get(id=message_id)
        message.update_from_dict(credential)
        return message

    async def remove(self, message_id: int):
        message = await Event.get(id=message_id)
        await message.delete()
        return message
