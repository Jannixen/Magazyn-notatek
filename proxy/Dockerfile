FROM nginxinc/nginx-unprivileged:1-alpine

USER root
COPY ./default.conf /etc/nginx/conf.d/default.conf

COPY ca.crt /etc/ssl/certs/
COPY ca.key /etc/ssl/private/

RUN apk add vim
RUN apk add openssl
