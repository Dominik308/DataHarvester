import json
import subprocess
import time
import pandas as pd

from elasticsearch import Elasticsearch
from kafka import KafkaConsumer


def get_ip_of_broker(name: str) -> str:
    """Gets IP via ping command in linux shell"""
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


def clean_data(data: str) -> pd.DataFrame:
    """Function to clean and restructure stock market data"""
    if isinstance(data, str):
        data = json.loads(data)
    
    cleaned_data = []
    
    timestamps = list(data['Open'].keys())
    
    for timestamp in timestamps:
        row = {'Timestamp': pd.to_datetime(int(timestamp), unit='ms').strftime('%Y-%m-%d %H:%M:%S')}
        for key in ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']:
            row[key] = data[key].get(timestamp, 0)
        cleaned_data.append(row)
    
    df = pd.DataFrame(cleaned_data)
    df.sort_values('Timestamp', inplace=True)
    
    print("Successfully cleaned the data!")
    
    return df



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
    print("RAW DATA", raw_data)

    # Clean the data
    cleaned_data = clean_data(raw_data)

    # Convert the cleaned data to a dictionary
    cleaned_data_dict = cleaned_data.to_dict(orient='records')

    # Send the cleaned data to Elasticsearch
    for record in cleaned_data_dict:
        es.index(index='stock_data', body=record)
