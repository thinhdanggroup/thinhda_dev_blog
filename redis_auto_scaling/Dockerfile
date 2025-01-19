# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y vim

# Copy the requirements file into the container
COPY requirements.txt ./


# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable for the Celery configuration module
ENV CELERY_CONFIG_MODULE=celeryconfig

# for debug
#CMD ["tail", "-f", "/dev/null"]

# Define the command to run the Celery worker
CMD ["celery", "-A", "tasks", "worker", "-Q", "low_priority,high_priority", "--loglevel=info"]