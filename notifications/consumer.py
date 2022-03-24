from core.kafka import Kafka
import asyncio


if __name__ == '__main__':
    asyncio.run(Kafka.consume())
