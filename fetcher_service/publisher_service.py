import json
from kafka import KafkaProducer
import yfinance as yf

# Create an instance of the KafkaProducer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka server address
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