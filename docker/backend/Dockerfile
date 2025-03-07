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