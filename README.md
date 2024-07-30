DataHarvester

Stock Data Visualization and Prediction
Welcome to the Stock Data Visualization and Prediction project! This application utilizes Python, Docker, Elasticsearch, Apache Kafka, and Kibana to visualize stock data and employs a linear regression model to predict stock trends. The project demonstrates a complete data pipeline, from data ingestion to visualization and prediction.

Features
Real-time data ingestion: Fetch stock data and stream it using Apache Kafka.
Data storage and search: Store and index data using Elasticsearch.
Data visualization: Visualize stock data using Kibana.
Predictive modeling: Train and deploy a linear regression model to predict stock trends.
Containerized environment: Use Docker to containerize the application for easy deployment and scalability.

Architecture
The architecture of the application is composed of several components working together:
Data Ingestion: A Python script fetches stock data from a reliable API and sends it to Kafka.
Message Broker: Apache Kafka acts as the message broker, ensuring reliable and scalable data streaming.
Data Storage: Data from Kafka is consumed and stored in Elasticsearch.
Visualization: Kibana is used to create interactive and real-time visualizations of the stock data stored in Elasticsearch.
Prediction: A linear regression model is trained on historical stock data to predict future trends. The model is implemented in Python and can be updated periodically.

Technologies Used
Python: For data ingestion, processing, and machine learning model.
Docker: To containerize the application, ensuring consistency across different environments.
Elasticsearch: For storing and indexing stock data, enabling efficient search and retrieval.
Apache Kafka: For real-time data streaming and handling high-throughput data ingestion.
Kibana: For visualizing the stock data in an interactive and real-time manner.
