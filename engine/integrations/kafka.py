from confluent_kafka import Producer
import socket
import os

def init():
    kafka_host = os.getenv("KAFKA_ADDRESS", "localhost:9092")
    conf = {'bootstrap.servers': kafka_host,
            'client.id': socket.gethostname()}

    producer = Producer(conf)
    return producer

    producer.produce("topic", key="key", value="value")


    def acked(err, msg):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))

    producer.produce("topic", key="key", value="value", callback=acked)

    # Wait up to 1 second for events. Callbacks will be invoked during
    # this method call if the message is acknowledged.
    producer.poll(1)
