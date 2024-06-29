import datetime as dt
import json
import os
import subprocess
import time
from threading import Thread

import yfinance as yf
from kafka import KafkaProducer


time_between_data_frames = 10  # wait 10 seconds before sending next real time data


def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run(f'ping -c1 {name} | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


def send_stonk_data(stonk: str) -> None:
    # Fetch stock information
    stock = yf.Ticker(stonk)  # Replace 'AAPL' with your desired stock symbol

    # Fetch and send historical market data for different periods
    # TODO: Fetch every day one time and delete old data after one day
    for period in ['2y']:
        period_data = stock.history(period=period)
        period_data['average'] = (period_data['High'] + period_data['Low'] + period_data['Close'] + period_data['Open']) / 4

        for date, frame_of_day in period_data.iterrows():
            data = {
                'symbol': stock.info['symbol'],
                'price': frame_of_day['average'],
                'timestamp': date.strftime('%Y-%m-%d') + " 00:00:00"
            }
            producer.send(f'{stonk}_{period}', data)
            producer.flush()


    # Fetch and send real-time market data
    # TODO: Fetch every day each 10 seconds and delete old data after one day
    try:
        while True:
            ticker = yf.Ticker(stonk)
            info = ticker.info

            if 'currentPrice' in info:
                data = {
                    'symbol': info['symbol'],
                    'price': info['currentPrice'],
                    'timestamp': (dt.datetime.now() + dt.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
                }
                producer.send(f'{stonk}_real_time', data)
                producer.flush()
                time.sleep(time_between_data_frames)  # Wait 10 second before next sending data
    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the producer connection
    producer.close()
    
    
time.sleep(10)  # Wait for ending creation of broker
ip_of_broker = get_ip_of_broker("broker")
port_of_broker = os.environ["KAFKA_BROKER_PORT"]

# Create an instance of the KafkaProducer
producer = KafkaProducer(
    bootstrap_servers=f'{ip_of_broker}:{port_of_broker}',  # Kafka server address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializer function
)

# Send data for each stonk
stonks = os.environ["STONKS"].split(",")

for stonk in stonks:
    Thread(target=send_stonk_data, args=[stonk.lower()]).start()