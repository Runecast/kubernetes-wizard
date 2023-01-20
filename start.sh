#! /usr/bin/env sh
set -e

if [ -f /home/gunicorn/k8s-wizard/backend/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

if [ -f /home/gunicorn/k8s-wizard/backend/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/home/gunicorn/k8s-wizard/backend/gunicorn_conf.py
fi
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornH11Worker"}

# Start Gunicorn
exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE" --workers ${WORKERS:-1}
