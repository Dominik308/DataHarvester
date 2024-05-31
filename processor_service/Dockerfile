# Use the official Ubuntu base image
FROM ubuntu:latest

# Update and upgrade the system
RUN apt-get update && apt-get upgrade -y

# Install Python 3 and pip
RUN apt-get install -y python3 python3-pip

# Verify Python installation
RUN python3 --version && pip3 --version

# Set default python version
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Python dependencies
#COPY requirements.txt .
#RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get install -y python3-kafka python3-elasticsearch

# Set the working directory
WORKDIR /DataHarvester/processor_service

# Copy the application files
COPY . .

# Set the default command
CMD ["python", "processor_service.py"]
