
FROM python:3.10.4-slim-buster

WORKDIR /app

COPY ./data_download/requirements.txt /app
RUN pip install -r requirements.txt

COPY ./data_download/data_download.py /app
