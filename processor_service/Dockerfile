# Use the official Ubuntu base image
# FROM ubuntu:latest
FROM python:3.11

# Update and upgrade the system
RUN apt-get update && apt-get upgrade -y

# Extra for getting IP of broker (kafka server)
 RUN apt-get install iputils-ping -y

# Install Python 3 and pip
RUN apt-get install -y software-properties-common
# RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.11 python3.11-distutils python3-pip

# Install Python dependencies
RUN pip install kafka-python-ng
RUN pip install requests
RUN pip install msgpack
RUN pip install aiokafka
RUN pip install elasticsearch==7.10.1

# Set the working directory
WORKDIR /DataHarvester/processor_service

# Copy the application files
COPY . .

# Set the default command
CMD ["python3", "consumer_service.py"]
