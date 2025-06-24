FROM python:3.13.5-alpine3.22

RUN mkdir /app
WORKDIR /app
RUN apk add --no-cache \
    gcc \
    musl-dev \
    zlib-dev \
    jpeg-dev \
    libpng-dev

COPY backend/core/requirements*.txt /app/
RUN pip install -r requirements.txt