FROM alpine:3.6

ARG zenroom_tag=bfa60a9e48b781c09fd9b4fe4bfef865bc127075

WORKDIR /code/zenroom

RUN apk update
RUN apk upgrade
RUN apk add --no-cache git openssh git

RUN git clone \
    https://github.com/DECODEproject/zenroom.git \
    . \
 && git checkout ${zenroom_tag} \
 && git submodule init \
 && git submodule update

RUN apk add --no-cache make cmake gcc musl-dev musl musl-utils
RUN make musl-system


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
