# Use the official python base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
	python3-dev default-libmysqlclient-dev build-essential \
	&& rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
COPY requirements.txt requirements.txt
RUN apt-get update -y
RUN pip install --upgrade pip
RUN apt-get update && apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
# RUN apt install python3-pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY the application code to the container
COPY . .

# Expose the port that Flask is running on
EXPOSE 3306

# Command to stdeart the server
CMD ["waitress-serve", "--host=0.0.0.0", "--port=3306", "api_main:app"]
