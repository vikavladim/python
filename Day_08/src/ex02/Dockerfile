FROM python:3.9-slim

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y redis-server && pip install -r requirements.txt

CMD ["redis-server"]

