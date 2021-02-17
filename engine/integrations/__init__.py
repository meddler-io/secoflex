from .kafka import init

enableKafka = False
kafka_producer = None

if enableKafka:
    print("Initializing Kafka Producer")
    kafka_producer = init()





def produce_data(topic, key, value):


    if not enableKafka:
        return False

    kafka_producer.produce(topic, key=key, value=value)
    kafka_producer.flush()


    return True
