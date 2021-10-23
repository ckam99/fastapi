import pika
import json
import os
import django
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


params = pika.URLParameters(settings.RABBITMQ_BROKER_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='django')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f'Received', data)

    if properties.content_type == 'USER_CREATED':
        from blog import services
        services.create_user(data)

    if properties.content_type == 'POST_CREATED':
        print('Post CREATED')

    elif properties.content_type == 'POST_CREATED':
        print('Post UPDATED')

    elif properties.content_type == 'POST_DELETED':
        print('Post Deleted')


channel.basic_consume(
    queue='django', on_message_callback=callback, auto_ack=True)

print('Started MY Django Consuming')

channel.start_consuming()

channel.close()
