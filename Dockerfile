# Backend için Python imajı
FROM python:3.11-slim

WORKDIR /app

# Sistem bağımlılıkları (DuckDB ve diğerleri için gerekebilir)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# FastAPI'yi çalıştır
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
