FROM python:3.9-slim
RUN apt-get update && apt-get install -y redis-server && pip install redis
COPY . /app
WORKDIR /app

RUN apt-get install -y ansible

CMD ["redis-server"]

