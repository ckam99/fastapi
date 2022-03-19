from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from repositories.message import MessageRepository
from core.settings import KAFKA_HOST, KAFKA_TOPICS, KAFKA_GROUP_ID


class Kafka:

    @staticmethod
    async def produce(topic: str, data):
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_HOST)
        # Get cluster layout and initial topic/partition leadership information
        await producer.start()
        try:
            # Produce message
            await producer.send_and_wait(topic, json.dumps(data).encode('utf-8'))
        finally:
            # Wait for all pending messages to be delivered or expire.
            await producer.stop()

    @staticmethod
    async def consume():
        consumer = AIOKafkaConsumer(
            *KAFKA_TOPICS,
            bootstrap_servers=KAFKA_HOST,
            group_id=KAFKA_GROUP_ID)
        # Get cluster layout and join group `my-group`
        print('consumer started...')
        await consumer.start()
        try:
            # Consume messages
            async for msg in consumer:
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                      msg.key, msg.value, msg.timestamp)
                # if msg.topic == 'message-create':
                #     await MessageRepository.se(msg.value.decode())
                #     print("post created successully!")
        finally:
            await consumer.stop()
