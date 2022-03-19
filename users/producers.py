import pulsar
from settings import PULSAR_HOST
import json


client = pulsar.Client(PULSAR_HOST)


def get_normalize_data(obj):
    if 'created_at' in obj:
        obj['created_at'] = obj['created_at'].isoformat()
    if 'updated_at' in obj:
        obj['updated_at'] = obj['updated_at'].isoformat()
    return obj


class Producer:

    def produce(self, topic: str, data) -> None:
        producer = client.create_producer(topic)
        producer.send(json.dumps(data).encode('utf-8'))
        # client.close()


class UserProducer(Producer):

    def __init__(self) -> None:
        self.data = {'source': 'users-service'}

    def user_created(self, data) -> None:
        self.data['data'] = get_normalize_data(data)
        self.produce('user_created', self.data)

    def user_updated(self, data) -> None:
        self.data['data'] = get_normalize_data(data)
        self.produce('user_updated', self.data)

    def user_removed(self, data) -> None:
        self.data['data'] = get_normalize_data(data)
        self.produce('user_removed', self.data)
