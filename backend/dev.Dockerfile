FROM python:3.9-buster

ENV PATH="${PATH}:/home/gunicorn/.local/bin"
ENV PYTHONPATH "${PYTHONPATH}:/home/gunicorn/k8s-wizard/"

RUN groupadd -g 1000 gunicorn  \
 && useradd -u 1000 -g 1000 --create-home --shell /bin/bash gunicorn
WORKDIR /home/gunicorn/k8s-wizard/backend/
RUN chown -R gunicorn /home/gunicorn/k8s-wizard/backend
USER gunicorn

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . .
