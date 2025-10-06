FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./

RUN useradd -u 1001 -r -s /usr/sbin/nologin fastapiuser \
    && chown -R fastapiuser:fastapiuser /app

USER fastapiuser

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--no-use-colors", "--limit-concurrency", "768", "--port", "8000"]

# docker build -t taxi_be .
# docker run -p 8000:8000 --env-file .dotenv --rm --name taxi_be taxi_be

# docker run -it -p 8000:8000 --env-file .dotenv --entrypoint sh --rm --name taxi_be taxi_be