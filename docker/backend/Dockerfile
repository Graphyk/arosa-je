FROM python:3.14.0a4-alpine3.21

RUN mkdir /app
WORKDIR /app
RUN apk add --no-cache \
    gcc \
    musl-dev \
    zlib-dev \
    jpeg-dev \
    libpng-dev

COPY backend/core/requirements*.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DJANGO_SUPERUSER_USERNAME=admin 
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com 
ENV DJANGO_SUPERUSER_PASSWORD=password 