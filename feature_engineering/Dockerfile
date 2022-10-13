
FROM python:3.10.4-slim-buster

WORKDIR /app

COPY ./feature_engineering/requirements.txt /app
RUN pip install -r requirements.txt

COPY ./feature_engineering/feat_eng.py /app
