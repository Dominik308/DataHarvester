import json
import os

from kafka import KafkaProducer


try:
    port_of_broker = os.environ["KAFKA_BROKER_PORT"]
    producer = KafkaProducer(
        bootstrap_servers=f'localhost:{port_of_broker}',  # Kafka server address
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializer function
    )
    exit(0)
# except NoBrokersAvailable:
#     exit(1)
except Exception as ex:
    print(ex)
    exit(2)
