FROM python:3.9.5-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

WORKDIR /django

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt