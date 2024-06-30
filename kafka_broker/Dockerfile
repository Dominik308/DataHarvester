FROM apache/kafka:latest

# Setze den Benutzer auf root, um die Installation durchzuführen
# USER root

# # Installiere Build-Tools und Abhängigkeiten
# RUN apk add --no-cache --virtual .build-deps \
#        gcc \
#        libc-dev \
#        make \
#        wget \
#        openssl-dev \
#        zlib-dev \
#        musl-dev \
#        linux-headers \
#        ca-certificates \
#    && wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz \
#    && tar xzf Python-3.11.0.tgz \
#    && cd Python-3.11.0 \
#    && ./configure --enable-optimizations \
#    && make altinstall \
#    && cd .. \
#    && rm -rf Python-3.11.0 Python-3.11.0.tgz \
#    && apk del .build-deps

# # Setze den Benutzer zurück auf kafka
# USER kafka

# Setze den Benutzer auf root, um die Installation durchzuführen
USER root

# Installiere Python und andere notwendige Pakete
RUN apk add --no-cache \
       python3 \
       py3-pip \
       wget \
       ca-certificates

# Setze den Benutzer zurück auf kafka


# Install Python dependencies
RUN pip install kafka-python-ng --break-system-packages

# Set the working directory
WORKDIR /DataHarvester/health_check

# Copy the application files
COPY . .

# Do a health check = try connecting to kafka broker
HEALTHCHECK --start-period=30s --timeout=5s --interval=1m --retries=2 CMD python3  health_check.py || exit 1
