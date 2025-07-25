FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmagic1 \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY app/ app/

RUN mkdir -p /app/input /app/output


RUN chmod +x main.py

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the main script
CMD ["python", "main.py"]
