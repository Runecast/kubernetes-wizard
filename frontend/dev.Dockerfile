FROM node:lts-alpine

WORKDIR /opt/k8s-wizard/frontend

ENV PATH /node_modules/.bin:$PATH


RUN npm install @vue/cli@v5.0.8 -g
COPY package*.json ./
RUN npm install
