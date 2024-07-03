FROM docker.elastic.co/elasticsearch/elasticsearch:8.14.0

# Switch to root user for installing with apt
USER root

# Update and upgrade the system
RUN apt-get update && apt-get upgrade -y

# Install python3 and pip
RUN apt-get install -y software-properties-common
RUN apt-get install -y python3 python3-distutils python3-pip

# Install Python dependencies
RUN pip install elasticsearch==8.14.0

# Switch back to default user
USER elasticsearch

# Set the working directory
WORKDIR /DataHarvester/health_check

# Copy the application files
COPY . .