FROM dyne/zenroom:0.8.1
FROM python:2.7-alpine

RUN apk add --no-cache openssl-dev libffi-dev build-base

WORKDIR /code
COPY requirements.txt /code/
COPY chainspacecontract/ /code/chainspacecontract/

COPY --from=0 /code/zenroom/src/zenroom-static /usr/bin/zenroom
COPY --from=0 /code/zenroom/examples/elgamal  /opt/contracts/

RUN pip install -r requirements.txt
RUN pip install -e chainspacecontract

COPY . /code
