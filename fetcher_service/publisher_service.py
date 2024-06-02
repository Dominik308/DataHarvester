import time

from kafka import KafkaProducer
from kafka.errors import KafkaError


producer = KafkaProducer(bootstrap_servers='kafka-server:9092')

# Asynchronous by default
future = producer.send('my-topic', b'raw_bytes')

# Block for 'synchronous' sends
while True:
    try:
        record_metadata = future.get(timeout=5)
        producer.flush()
        print(record_metadata)
    except KafkaError as ex:
        # Decide what to do if produce request failed...
        print(ex)
        # exit()
    finally:
        time.sleep(3)
