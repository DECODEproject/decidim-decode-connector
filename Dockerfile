FROM python:2.7-alpine

RUN apk add --no-cache openssl-dev libffi-dev build-base

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt