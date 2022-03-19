from core.kafka import Kafka
import asyncio

asyncio.run(Kafka.consume())
