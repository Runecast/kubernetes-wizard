FROM node:lts-alpine AS build-stage

WORKDIR /opt/k8s-wizard/frontend
ENV PATH frontend/node_modules/.bin:$PATH

RUN npm install @vue/cli@v5.0.8 -g
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

RUN npm run build


FROM python:3.9-buster AS prod-backend

ENV PATH="${PATH}:/home/gunicorn/.local/bin"
ENV PYTHONPATH "${PYTHONPATH}:/home/gunicorn/k8s-wizard/"

RUN groupadd -g 1000 gunicorn  \
 && useradd -u 1000 -g 1000 --create-home --shell /bin/bash gunicorn
WORKDIR /home/gunicorn/k8s-wizard/backend/
COPY start.sh ..
RUN chown -R gunicorn /home/gunicorn/k8s-wizard/backend \
 && chmod +x /home/gunicorn/k8s-wizard/start.sh

USER gunicorn

COPY backend/requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY --from=build-stage /opt/k8s-wizard/frontend/ /home/gunicorn/k8s-wizard/frontend/
COPY backend/ .
