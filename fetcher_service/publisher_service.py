import json
import pandas as pd
import time
import subprocess

from collections import defaultdict
from kafka import KafkaProducer
import yfinance as yf


def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


def clean_data(dirty_data: str) -> pd.DataFrame:
    """Function to clean and restructure stock market data"""
    if isinstance(dirty_data, str):
        dirty_data = json.loads(dirty_data)

    cleaned_data = []
    timestamps = list(dirty_data['Open'].keys())

    for timestamp in timestamps:
        row = {'Timestamp': pd.to_datetime(int(timestamp), unit='ms').strftime('%Y-%m-%d %H:%M:%S')}
        for key in ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']:
            row[key] = dirty_data[key].get(timestamp, 0)
        cleaned_data.append(row)

    df = pd.DataFrame(cleaned_data)
    df.sort_values('Timestamp', inplace=True)

    print("Successfully cleaned the data!")

    return df


def restructure_data(dirty_data: str) -> dict[str, dict[str, str]]:
    def empty_dict() -> {}:
        return {}

    df_cleaned_data = clean_data(dirty_data)
    restructured_data = defaultdict(empty_dict)

    for attribute, values in df_cleaned_data.to_dict().items():
        for timestamp, value in values.items():
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

# Fetch and send real-time market data
try:
    while True:
        ticker = yf.Ticker("AAPL")
        info = ticker.info
        if 'currentPrice' in info:
            print(f"Current price of {info['symbol']} is {info['currentPrice']} at {time.strftime('%d.%m.%Y %H:%M', time.localtime())}")
            data = {
                'symbol': info['symbol'],
                'price': info['currentPrice'],
                'time': time.strftime('%d.%m.%Y %H:%M', time.localtime())
            }
            producer.send('real_time', data)

        time.sleep(10)
except Exception as e:
    print(f"An error occurred: {e}")


# Ensure all messages are sent
producer.flush()

# Close the producer connection
producer.close()
