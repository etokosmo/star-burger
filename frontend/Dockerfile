# syntax = docker/dockerfile:1.3-labs
ARG NODEJS_VERSION=16

FROM node:${NODEJS_VERSION}-buster-slim
# FIX npm bug https://github.com/npm/cli/issues/4414
RUN npm install -g npm@8.18.0

WORKDIR /code/
COPY package.json package-lock.json /code/
RUN npm ci --dev
COPY . /code/

EXPOSE 3000
