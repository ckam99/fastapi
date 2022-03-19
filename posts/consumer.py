import pulsar

from settings import PULSAR_HOST
import json
import re
from database import get_database


client = pulsar.Client(PULSAR_HOST)


POST_TOPICS = ['post_created', 'post_updated', 'post_removed']
USER_TOPICS = ['user_created', 'user_updated', 'user_removed']

# consumer = client.subscribe(topic=[*POST_TOPICS, *USER_TOPICS], consumer_type=ConsumerType.Shared,
#                             subscription_name='my-sub')

consumer = client.subscribe(re.compile('persistent://public/default/.*'),
                            consumer_type=pulsar.ConsumerType.Failover,
                            subscription_name='my-sub')

while True:
    msg = consumer.receive()
    if msg.topic_name() in POST_TOPICS:
        pass
    print("Received message: '%s'" % msg.data())
    print("topic: ", msg.topic_name())
    print("message value: '%s'" % msg.value())
    try:
        consumer.acknowledge(msg)
    except:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)

client.close()
