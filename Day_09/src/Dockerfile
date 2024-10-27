FROM python:3.9-slim

COPY ex00 /app
WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++
RUN pip install setuptools && pip install cython


