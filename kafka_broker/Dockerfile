FROM apache/kafka:latest

# Switch to root user for installing with apk
USER root

# Install python
RUN apk add --no-cache \
       python3 \
       py3-pip \
       wget \
       ca-certificates

# Install python dependencies
RUN pip install kafka-python-ng --break-system-packages

# Switch back to default user
USER appuser

# Set the working directory
WORKDIR /DataHarvester/health_check

# Copy the application files
COPY . .