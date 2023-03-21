FROM node:lts-alpine AS build-stage

WORKDIR /opt/k8s-wizard/frontend
ENV PATH frontend/node_modules/.bin:$PATH

COPY frontend/ .

RUN npm install; \
    npm install @vue/cli@v5.0.8 -g; \
    npm run build

FROM python:3.10-alpine AS backend

ENV PATH=$PATH:/home/gunicorn/.local/bin
ENV PYTHONPATH $PYTHONPATH:/home/gunicorn/k8s-wizard/backend

WORKDIR /home/gunicorn/k8s-wizard/backend

COPY start.sh /home/gunicorn/k8s-wizard/
COPY backend/requirements.txt .

RUN addgroup -S gunicorn; \
    adduser -S gunicorn -G gunicorn; \
    chown -R gunicorn /home/gunicorn/k8s-wizard/backend; \
    chmod +x /home/gunicorn/k8s-wizard/start.sh; \
    pip install --upgrade pip; \
    pip install --no-cache-dir -r requirements.txt

USER gunicorn

COPY backend/ .
COPY --from=build-stage /opt/k8s-wizard/frontend/dist/ /home/gunicorn/k8s-wizard/frontend/dist/

ENV BUILD="prod"
ENV PYTHONUNBUFFERED="1"
ENV WORKERS="1"
EXPOSE 8000

COPY data/ /home/gunicorn/k8s-wizard/data/
WORKDIR /home/gunicorn/k8s-wizard
CMD [ "/home/gunicorn/k8s-wizard/start.sh" ]
