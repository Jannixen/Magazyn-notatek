FROM python:3.8-alpine

USER root

COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY Notatki/Notatki /app
WORKDIR /app


RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

