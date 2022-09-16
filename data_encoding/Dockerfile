
FROM python:3.10.4-slim-buster

WORKDIR /app

COPY ./data_encoding/requirements.txt /app
RUN pip install -r requirements.txt

COPY ./data_encoding/data_encoding.py /app
