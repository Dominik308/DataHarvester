import json
import subprocess
import time
import os

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer


def get_ip_of_broker(name: str) -> str:
    """Gets IP via ping command in linux shell"""
    ip = subprocess.run(f'ping -c1 {name} | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


# Wait for ending creation of broker
time.sleep(30)

# Read stocks to send data to ElasticSearch from environment variable
stonks = os.environ["STONKS"].split(",")

# Create a Kafka consumer
ip_of_broker = get_ip_of_broker("broker")
port_of_broker = os.environ["KAFKA_BROKER_PORT"]
topics = [f'{stonk}_{time_span}'.lower() for time_span in ['2y', 'real_time'] for
          stonk in stonks]
consumer = KafkaConsumer(*topics, bootstrap_servers=f'{ip_of_broker}:{port_of_broker}', auto_offset_reset='earliest',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))  # Deserializer function
# consumer.subscribe(topics=topics)

# Create an Elasticsearch client
ip_of_data_preparer = get_ip_of_broker("data-preparer")
port_of_data_preparer = os.environ["ELASTICSEARCH_DATA_PREPARER_PORT"]
es = Elasticsearch(
    hosts=[{"host": "host.docker.internal", "port": int(port_of_data_preparer), "scheme": "http"}]
    # basic_auth=("elastic", "MagicWord")
)

for topic in topics:
    if not es.indices.exists(index=f'stock_data_{topic}'):  # Create index with mapping for ElasticSearch
        es.indices.create(index=f'stock_data_{topic}')

    es.indices.put_settings(
        index=f'stock_data_{topic}',
        headers={'Content-Type': 'application/json'},
        body={
            'index': {
                'mapping': {
                    'total_fields': {
                        'limit': '100000'  # Increase the limit as needed
                    }
                }
            }
        }
    )

# Consume messages from the topics
for message in consumer:
    data = message.value  # Get the data as dict

    # Send the data to Elasticsearch as json structure, e.g. dict is okay
    es.index(index=f'stock_data_{message.topic}', body=data)