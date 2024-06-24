import json
import os
import subprocess
import time
from threading import Thread

import yfinance as yf
from kafka import KafkaProducer


def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


def send_stonk_data(stonk: str) -> None:
    # Fetch stock information
    stock = yf.Ticker(stonk)  # Replace 'AAPL' with your desired stock symbol

    # Fetch and send historical market data for different periods
    # TODO: Fetch every day one time and delete old data after one day
    for period in ['1y', '1mo', '5d']:
        for date, frame_of_day in stock.history(period=period).iterrows():
            data = {
                'symbol': stock.info['symbol'],
                'price': frame_of_day['High'],
                'timestamp': date.strftime('%d.%m.%Y')
            }
            producer.send(f'{stonk}_{period}', data)
            producer.flush()

    time.sleep(10)

    # Fetch and send real-time market data
    # TODO: Fetch every day each 10 seconds and delete old data after one day
    try:
        while True:
            ticker = yf.Ticker(stonk)
            info = ticker.info
            if 'currentPrice' in info:
                print(f"Current price of {info['symbol']} is {info['currentPrice']} at {time.strftime('%d.%m.%Y %H:%M', time.localtime())}")
                data = {
                    'symbol': info['symbol'],
                    'price': info['currentPrice'],
                    'timestamp': time.strftime('%d.%m.%Y %H:%M', time.localtime())
                }
                producer.send(f'{stonk}_real_time', data)

                producer.flush()

            time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the producer connection
    producer.close()
    
    
time.sleep(10)  # Wait for ending creation of broker
ip_of_broker = get_ip_of_broker("broker")

# Create an instance of the KafkaProducer
producer = KafkaProducer(
    bootstrap_servers=f'{ip_of_broker}:19092',  # Kafka server address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializer function
)

# Send data for each stonk
stonks = os.environ["STONKS"].split(",")

for stonk in stonks:
    Thread(target=send_stonk_data, args=[stonk.lower()]).start()