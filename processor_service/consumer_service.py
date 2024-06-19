import json
import subprocess
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer


def get_ip_of_broker(name: str) -> str:
    """Gets IP via ping command in linux shell"""
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


# Wait for ending creation of broker
time.sleep(30)

# Create a Kafka consumer
ip_of_broker = get_ip_of_broker("broker")
topics = ['stonks_1y', 'stonks_1mo', 'stonks_5d', 'real_time']
consumer = KafkaConsumer(*topics, bootstrap_servers=f'{ip_of_broker}:19092', auto_offset_reset='earliest',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))  # Deserializer function
# consumer.subscribe(topics=topics)

# Create an Elasticsearch client
ip_of_data_preparer = get_ip_of_broker("data-preparer")
es = Elasticsearch(
    hosts=[{"host": "host.docker.internal", "port": 9200, "scheme": "http"}]
    # basic_auth=("elastic", "MagicWord")
)

if not es.indices.exists(index='stock_data'):
    es.indices.create(index='stock_data')

es.indices.put_settings(
    index='stock_data',
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

# es.options(
#     headers={'Content-Type': 'application/json'},
# )

# Consume messages from the topics
for message in consumer:
    data = message.value  # Get the data as dict
    # print("Data:", data, flush=True)

    # Send the data to Elasticsearch as json structure, e.g. dict is okay
    es.index(index='stock_data', body=data)
