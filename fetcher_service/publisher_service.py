import json
import time
import subprocess

from kafka import KafkaProducer
import yfinance as yf


def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


def restructure_data(data):
    data = json.loads(data)

    restructured_data = {}
    for attribute, values in data.items():
        for timestamp, value in values.items():
            if timestamp not in restructured_data:
                restructured_data[timestamp] = {}

            restructured_data[timestamp][attribute] = value

    return restructured_data


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
for period in ['1y', '1mo', '5d']:
    history = stock.history(period=period)
    history_json = restructure_data(history.to_json())

    print("Send data to Kafka!")

    # Send the historical market data to the Kafka topic
    producer.send(f'stonks_{period}', history_json)

# Ensure all messages are sent
producer.flush()

# Close the producer connection
producer.close()
