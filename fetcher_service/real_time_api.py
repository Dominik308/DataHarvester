import json
import time
import subprocess

from kafka import KafkaProducer
import yfinance as yf

def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


time.sleep(10)
ip_of_broker = get_ip_of_broker("broker")

# Create an instance of the KafkaProducer
producer = KafkaProducer(
    bootstrap_servers=f'{ip_of_broker}:19092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

ticker = yf.Ticker("AAPL")

try:
    while True:
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
