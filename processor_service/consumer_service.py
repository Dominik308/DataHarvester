import json
import subprocess
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer


def get_ip_of_broker(name: str) -> str:
    """Gets IP via ping command in linux shell"""
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


def clean_data(data):
    """Function to clean data"""
    # Implement your data cleaning logic here
    cleaned_data = data  # Placeholder line
    return cleaned_data


# Wait for ending creation of broker
time.sleep(10)

# Create a Kafka consumer
ip_of_broker = get_ip_of_broker("broker")
consumer = KafkaConsumer(
    *['stonks_max', 'stonks_1y', 'stonks_6mo', 'stonks_1mo', 'stonks_1wk', 'stonks_1d'],  # List of topics
    bootstrap_servers=f'{ip_of_broker}:19092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserializer function
)

# Create an Elasticsearch client
ip_of_data_preparer = get_ip_of_broker("data-preparer")
es = Elasticsearch(
    hosts=[{"host": "host.docker.internal", "port": 9200}]
    # [f'http://{ip_of_data_preparer}:9200'],
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
                    'limit': '2000'  # Increase the limit as needed
                }
            }
        }
    }
)

# Consume messages from the topics
for message in consumer:
    # Get the raw data
    raw_data = message.value

    # Save the raw data
    with open('raw_data.json', 'a') as f:
        json.dump(raw_data, f)
        f.write('\n')

    # Clean the data
    cleaned_data = clean_data(raw_data)

    # Save the cleaned data
    with open('cleaned_data.json', 'a') as f:
        json.dump(cleaned_data, f)
        f.write('\n')

    # Send the cleaned data to Elasticsearch
    es.index(index='stock_data', body=cleaned_data)
