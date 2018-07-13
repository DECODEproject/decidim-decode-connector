FROM python:2.7-alpine

RUN apk add --no-cache openssl-dev libffi-dev build-base

WORKDIR /code
COPY requirements.txt /code/
COPY chainspacecontract/ /code/chainspacecontract/

RUN pip install -r requirements.txt
RUN pip install -e chainspacecontract

COPY . /code
