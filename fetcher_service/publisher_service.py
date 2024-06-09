import time
import requests as r
import subprocess

from kafka import KafkaProducer
from kafka.errors import KafkaError


def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


time.sleep(10)  # Wait for ending creation of broker
ip_of_broker = get_ip_of_broker("broker")
producer = KafkaProducer(bootstrap_servers=f'{ip_of_broker}:19092')
future = producer.send('my-topic', b'raw_bytes')

try:
    record_metadata = future.get(timeout=5)
    producer.flush()
    print(record_metadata)
except KafkaError as ex:
    # Decide what to do if produce request failed...
    print(ex)
    # exit()
finally:
    time.sleep(3)
