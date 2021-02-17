

# Consumer

from confluent_kafka import Consumer
conf = {'bootstrap.servers': "localhost:9092",
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)


running = True

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: 
                continue
            if msg.error():
                print(msg.error())
            else:
                print(msg.key(),  msg.value())
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

def shutdown():
    running = False


basic_consume_loop(consumer, ["test_topic"])