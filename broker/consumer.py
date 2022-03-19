import pulsar

client = pulsar.Client('pulsar://127.0.0.1:6650')
consumer = client.subscribe('my-topic',
                            subscription_name='my-sub-2')

while True:
    msg = consumer.receive()
    print("Received message: '%s'" % msg.data())
    consumer.acknowledge(msg)

client.close()
