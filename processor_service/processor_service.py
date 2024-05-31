from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

KAFKA_TOPIC = 'stock_data'
KAFKA_SERVER = 'localhost:9092'
ES_HOST = 'localhost'

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER,
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

es = Elasticsearch([{'host': ES_HOST, 'port': 9200}])

def process_and_index(data):
    for time, info in data['Time Series (5min)'].items():
        doc = {
            'symbol': data['Meta Data']['2. Symbol'],
            'time': time,
            'data': info
        }
        es.index(index='stocks', doc_type='_doc', body=doc)

def main():
    for message in consumer:
        data = message.value
        process_and_index(data)

if __name__ == '__main__':
    main()
