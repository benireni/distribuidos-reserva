# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install git and other necessary dependencies
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN python -m venv .distribuidos-venv && \
    .distribuidos-venv/bin/pip install --upgrade pip && \
    .distribuidos-venv/bin/pip install -r requirements.txt && \
    .distribuidos-venv/bin/pip install pymongo kafka-python git+https://github.com/dpkp/kafka-python.git

# Copy the application code
COPY . .

# Command to run the main script
CMD [".distribuidos-venv/bin/python", "./source/routes.py"]