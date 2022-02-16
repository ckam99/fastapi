from worker import Kafka
from schemas import Post
import asyncio


def post_event(topic: str, post: Post):
    asyncio.run(Kafka.produce(topic, post))
