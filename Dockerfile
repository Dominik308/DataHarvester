# From ubuntu/debian/...
FROM ubuntu

# Install python3
RUN apt update
RUN apt upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Set default python version
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python --version RUN python3 --version

# Add file to container
ADD ./test.py .
RUN sed -i 's/\r$//' test.py

# Run script in unbuffered mode
ENTRYPOINT python3 -u test.py
