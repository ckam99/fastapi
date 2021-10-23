import pika
import json
import settings
from typing import List

params = pika.URLParameters(settings.RABBITMQ_BROKER_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body, channels: List = []):
    properties = pika.BasicProperties(method)
    for ch in channels:
        channel.basic_publish(exchange='', routing_key=ch,
                              body=json.dumps(body), properties=properties)
