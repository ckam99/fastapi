from core.kafka import Kafka
from schemas.message import Message
import asyncio


def message_created(topic: str, post: Message):
    asyncio.run(Kafka.produce(topic, Message))
