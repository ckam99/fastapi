import pulsar
from settings import PULSAR_HOST
import json
import re

client = pulsar.Client(PULSAR_HOST)


POST_TOPICS = ['post_created', 'post_updated', 'post_removed']

# consumer = client.subscribe(topic=[*POST_TOPICS],
#                             subscription_name='my-sub')

consumer = client.subscribe(re.compile(
    'persistent://public/default/topic-*'), 'my-sub')


while True:
    msg = consumer.receive()
    try:
        print("Received message '{}' id='{}'".format(
            msg.data(), msg.message_id()))
        print("Received message: '%s'" % msg.data())
        print("topic: ", msg.topic_name())
        print("message value: '%s'" % msg.value())
        consumer.acknowledge(msg)
    except:
        consumer.negative_acknowledge(msg)

client.close()
