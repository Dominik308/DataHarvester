FROM docker.elastic.co/kibana/kibana:8.14.0

# Set the working directory
WORKDIR /DataHarvester/health_check_as_upload_config_file

# Copy the application files
COPY . .

# Remove Windows line endings
RUN sed -i 's/\r$//' export.ndjson
