import requests
import json
from kafka import KafkaProducer
import time

API_KEY = 'XAT89MLQFJCLL8YD'
BASE_URL = 'https://www.alphavantage.co/query'
KAFKA_TOPIC = 'stock_data'
KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def fetch_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': 'XAT89MLQFJCLL8YD'
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def main():
    symbol = 'AAPL'  # Example stock symbol
    while True:
        data = fetch_stock_data(symbol)
        producer.send(KAFKA_TOPIC, data)
        time.sleep(300)  # Fetch data every 5 minutes

if __name__ == '__main__':
    main()
