# Pull a base image
FROM python:3.10-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Create a working directory for the django project
WORKDIR /app
# Copy requirements to the container
COPY ./requirements.txt /requirements.txt
# Install the requirements to the container
RUN pip install --no-cache-dir pip -r /requirements.txt
# Copy the project files into the working directory
COPY . /app/
# Open a port on the container
EXPOSE 8000
