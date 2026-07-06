FROM python:3.10-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    mongodb-clients \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create necessary directories
RUN mkdir -p videos logs

CMD ["python", "main.py"]
