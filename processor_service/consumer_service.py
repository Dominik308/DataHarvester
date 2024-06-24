import json
import subprocess
import time
import os

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer


def get_ip_of_broker(name: str) -> str:
    """Gets IP via ping command in linux shell"""
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


# Wait for ending creation of broker
time.sleep(30)

stonks = os.environ["STONKS"].split(",")

# Define expected data schema (replace with your actual data structure)
data_schema = {
    "properties": {
        "timestamp": {"type": "date"},  # Adjust data type as needed
        "symbol": {"type": "keyword"},
        "price": {"type": "float"},
        "volume": {"type": "long"},
        # Add more fields based on your data structure
    }
}

# Create a Kafka consumer
ip_of_broker = get_ip_of_broker("broker")
topics = [f'{stonk}_{time_span}'.lower() for time_span in ['stonks_1y', 'stonks_1mo', 'stonks_5d', 'real_time'] for stonk in stonks]
consumer = KafkaConsumer(*topics, bootstrap_servers=f'{ip_of_broker}:19092', auto_offset_reset='earliest',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))  # Deserializer function
# consumer.subscribe(topics=topics)

# Create an Elasticsearch client
ip_of_data_preparer = get_ip_of_broker("data-preparer")
es = Elasticsearch(
    hosts=[{"host": "host.docker.internal", "port": 9200, "scheme": "http"}]
    # basic_auth=("elastic", "MagicWord")
)

for topic in topics:
    if not es.indices.exists(index=f'stock_data_{topic}'):
        es.indices.create(index=f'stock_data_{topic}')

    # Create mappings for the index with the defined schema
    es.indices.put_mapping(index=f'stock_data_{topic}', body=data_schema)

# Consume messages from the topics
for message in consumer:
    data = message.value  # Get the data as dict

    # Send the data to Elasticsearch as json structure, e.g. dict is okay
    es.index(index=f'stock_data_{message.topic}', body=data)
