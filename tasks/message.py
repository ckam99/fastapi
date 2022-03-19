from core.kafka import Kafka
from schemas.message import Message
import asyncio


async def message_created(topic: str, msg: Message):
    await Kafka.produce(topic, msg.dict())
