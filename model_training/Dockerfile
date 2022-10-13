
FROM python:3.10.4-slim-buster

WORKDIR /app

COPY ./model_training/requirements.txt /app
RUN pip install -r requirements.txt

COPY ./model_training/model_train.py /app
