import subprocess
import time

from kafka import KafkaConsumer


def get_ip_of_broker(name: str) -> str:
    ip = subprocess.run('ping -c1 broker | head -n1 | cut -d" " -f3', shell=True, stdout=subprocess.PIPE)
    return ip.stdout.decode('utf-8')[1:-2]


time.sleep(10)  # Wait for ending creation of broker
ip_of_broker = get_ip_of_broker("broker")
consumer = KafkaConsumer('my-topic',
                         bootstrap_servers=f'{ip_of_broker}:19092',
                         auto_offset_reset='earliest',
                         consumer_timeout_ms=1000)

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
