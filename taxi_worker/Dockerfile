FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd -r worker && useradd -r -g worker worker

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./

RUN chown -R worker:worker /app

USER worker

CMD ["python", "main.py"]

# docker build -t taxi_worker .
# docker run --env-file .dotenv --rm --name taxi_worker taxi_worker

# docker run -it --env-file .dotenv --entrypoint sh --rm --name taxi_worker taxi_worker