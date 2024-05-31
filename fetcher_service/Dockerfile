# Use the official Ubuntu base image
FROM ubuntu:latest

# Update and upgrade the system
RUN apt-get update && apt-get upgrade -y

# Install Python 3.11 and pip
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.11 python3.11-distutils python3-pip

# Verify Python installation
RUN python3.11 --version && pip3 --version

# Install Python dependencies
RUN apt-get install -y python3-requests
RUN apt-get install -y python3-kafka

# Set the working directory
WORKDIR /DataHarvester/fetcher_service

# Copy the application files
COPY . .

# Set the default command
CMD ["python3", "fetcher_service.py"]
