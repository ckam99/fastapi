from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from services import PostService
import os


class Kafka:

    KAFKA_HOST = '{}:{}'.format(os.environ.get(
        'KAFKA_HOST', 'localhost'), os.environ.get('KAFKA_PORT', '9092'))
    KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'fastapi')
    KAFKA_TOPICS = ['post_created', 'post_deleted', 'post_updated']

    @staticmethod
    async def produce(topic: str, data):
        producer = AIOKafkaProducer(bootstrap_servers=Kafka.KAFKA_HOST)
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
            *Kafka.KAFKA_TOPICS,
            bootstrap_servers=Kafka.KAFKA_HOST,
            group_id=Kafka.KAFKA_GROUP_ID)
        # Get cluster layout and join group `my-group`
        print('consumer started...')
        await consumer.start()
        try:
            # Consume messages
            async for msg in consumer:
                print("consumed: ", msg.topic, msg.partition, msg.offset,
                      msg.key, msg.value, msg.timestamp)
                if msg.topic == 'post_created':
                    await PostService.save_post(msg.value.decode())
                    print("post created successully!")
        finally:
            # Will leave consumer group; perform autocommit if enabled.
            await consumer.stop()
