import datetime as dt
import json
import os
import subprocess
import time
from threading import Thread

import yfinance as yf
from kafka import KafkaProducer
from model import stock_prediction

# Define global variables
time_between_data_frames = 10  # wait 10 seconds before sending next real time data


def output_command(command: str) -> str:
    """Outputs a passed command and return result as string"""
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE)

    if res.returncode != 0:
        raise RuntimeError(f"Failed executing command: {command}")

    return res.stdout.decode('utf-8')


def get_ip_of_broker(name: str) -> str:
    """Gets IP via ping command in linux shell"""
    command = f'ping -c1 {name} | head -n1 | cut -d" " -f3'
    ip = output_command(command)
    return ip[1:-2]


def send_stonk_data(stonk: str) -> None:
    # Fetch stock information
    stock = yf.Ticker(stonk)  # Replace 'AAPL' with your desired stock symbol

    # Fetch and send historical market data for different periods
    for period in ['2y']:
        period_data = stock.history(period=period)
        period_data['average'] = (period_data['High'] + period_data['Low'] + period_data['Close'] + period_data['Open']) / 4

        for date, frame_of_day in period_data.iterrows():
            data = {
                'symbol': stock.info['symbol'],
                'price': frame_of_day['average'],
                'timestamp': date.strftime('%Y-%m-%d' + ' 00:00:00')
            }
            producer.send(f'{stonk}_{period}', data)
            producer.flush()
            
    # Send Predicted Stock data
    num_predictions = int(os.environ["DAYS_OF_PREDICTIONS"])
    predicted_stock_data = stock_prediction(stonk, num_predictions)
    
    for i, predicted_price in enumerate(predicted_stock_data):
        prediction_date = dt.datetime.now() + dt.timedelta(days=i+1)
        data = {
            'symbol': stonk,
            'price': predicted_price,
            'timestamp': prediction_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        producer.send(f'{stonk}_prediction', data)
        producer.flush()

    # Fetch and send real-time market data
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


def get_stonks_for_specific_container() -> list[str]:
    """Asks Docker API for container name and returns all stocks for this container"""

    # Get Docker ID of container
    # command = "basename $(cat /proc/1/cpuset)"
    # container_id = output_command(command)
    container_id = os.environ["HOSTNAME"]

    # Get name of container
    url = f"http://localhost/containers/{container_id}/json"
    command = f"curl --unix-socket /var/run/docker.sock {url}"
    container_info = output_command(command)
    container_info = json.loads(container_info)
    container_aliases = list(container_info["NetworkSettings"]["Networks"].values())[0]["Aliases"]
    container_name = container_aliases[0]
    publisher_number = int(container_name.rsplit("-", 1)[1]) - 1  # Get number of container, "-1" for using as index

    # Get all stocks
    all_stonks = os.environ["STONKS"].split(",")
    stonk_number = int(os.environ["SERVICES"])  # Each "stonk_number", e.g. 3, stock to request from yfinance

    # Return stocks for this container
    return all_stonks[publisher_number::stonk_number]  # Start with publisher number and take each "stonk_number" stock


# Get connection info from environment variables
ip_of_broker = get_ip_of_broker("broker")
port_of_broker = os.environ["KAFKA_BROKER_PORT"]

# Create an instance of the KafkaProducer
producer = KafkaProducer(
    bootstrap_servers=f'{ip_of_broker}:{port_of_broker}',  # Kafka server address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializer function
)

# Send data for each stonk
stonks = get_stonks_for_specific_container()
print("STONKS: ", stonks)

for stonk in stonks:
    Thread(target=send_stonk_data, args=[stonk.lower()]).start()
