import json
import subprocess
import time

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer


def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


time.sleep(10)  # Wait for ending creation of broker
ip_of_broker = get_ip_of_broker("broker")


# Create a Kafka consumer
consumer = KafkaConsumer(
    *['stonks_max', 'stonks_1y', 'stonks_6mo', 'stonks_1mo', 'stonks_1wk', 'stonks_1d'],  # List of topics
    bootstrap_servers=f'{ip_of_broker}:19092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserializer function
)

# Create an Elasticsearch client
es = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=('elastic', '123456')
)

es.indices.put_settings(
    index='stock_data',
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


# Function to clean data
def clean_data(data):
    # Implement your data cleaning logic here
    cleaned_data = data  # Placeholder line
    return cleaned_data


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
