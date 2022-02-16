from worker import Kafka
import asyncio

# loop = asyncio.get_event_loop()

# loop.run_until_complete(Kafka.consume())

asyncio.run(Kafka.consume())
