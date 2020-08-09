# Base image
FROM python:3 AS builder

RUN apt-get update

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /image_service

COPY ./proto/image.proto proto/
COPY data data/
COPY saved_model saved_model/
COPY image_pb2.py ./
COPY image_pb2_grpc.py ./
COPY imgServiceServer.py ./
COPY imgServiceMisc.py ./
COPY start.sh ./
CMD  ["./start.sh"]

