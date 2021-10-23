import pika
import json
import settings

params = pika.URLParameters(settings.RABBITMQ_BROKER_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='fastapi')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f'Received', data)

    if properties.content_type == 'USER_CREATED':
        print('USER CREATED')

    if properties.content_type == 'POST_CREATED':
        print('Post CREATED')

    elif properties.content_type == 'POST_CREATED':
        print('Post UPDATED')

    elif properties.content_type == 'POST_DELETED':
        print('Post Deleted')


channel.basic_consume(
    queue='fastapi', on_message_callback=callback, auto_ack=True)

print('Started My fastAPI Consuming')

channel.start_consuming()

channel.close()
