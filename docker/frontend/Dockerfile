FROM node:22.15.1-alpine3.20

RUN mkdir app
WORKDIR /app

COPY frontend/package.json /app/
RUN yarn install