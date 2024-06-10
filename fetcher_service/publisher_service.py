import json
import time
import subprocess

from kafka import KafkaProducer
import yfinance as yf


def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


time.sleep(10)  # Wait for ending creation of broker
ip_of_broker = get_ip_of_broker("broker")

# Create an instance of the KafkaProducer
producer = KafkaProducer(
    bootstrap_servers=f'{ip_of_broker}:19092',  # Kafka server address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializer function
)

# Fetch stock information
stock = yf.Ticker("AAPL")  # Replace 'AAPL' with your desired stock symbol

# Fetch and send historical market data for different periods
for period in ['2y', '1y', '6mo', '1mo', '5d', '1d']:
    history = stock.history(period=period)
    history_json = history.to_json()

    # Send the historical market data to the Kafka topic
    producer.send(f'stonks_{period}', history_json)

# Ensure all messages are sent
producer.flush()

# Close the producer connection
producer.close()
