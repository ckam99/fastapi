import pulsar
from settings import PULSAR_HOST
import json
import re
from database import get_database
from tortoise.transactions import in_transaction
from models import Post
import asyncio

client = pulsar.Client(PULSAR_HOST)


POST_TOPICS = ['post_created', 'post_updated', 'post_removed']
USER_TOPICS = ['user_created', 'user_updated', 'user_removed']

consumer = client.subscribe(topic=[*POST_TOPICS, *USER_TOPICS],
                            # consumer_type=pulsar.ConsumerType.Shared,
                            subscription_name='my-sub')


# consumer = client.subscribe(re.compile('persistent://public/default/.*'),
#                             consumer_type=pulsar.ConsumerType.Failover,
#                             subscription_name='my-sub')


while True:
    msg = consumer.receive()
    topic = str(msg.topic_name()).split('/')[-1]
    value: dict = json.loads(msg.value().decode())

    source: str = value.get('source', '')
    data: dict = value.get('data', {})

    print(data)

    if topic in POST_TOPICS:
        if topic == 'post_created':
            async def wrapper():
                db = await get_database()
                async with in_transaction() as conn:
                    post = Post(**data)
                    await post.save(using_db=conn)
                await db.close()
            asyncio.run(wrapper())

    if topic in USER_TOPICS:
        pass
    try:
        consumer.acknowledge(msg)
    except:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)

client.close()
