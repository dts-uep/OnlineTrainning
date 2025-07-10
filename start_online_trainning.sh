#!/bin/bash

# Need to source to project folder beforehand
echo "[*] Activating virtual environment..."
source venv/bin/activate

echo "[*] Starting Redis..."
sudo systemctl start redis

echo "[*] Killing Old workers..."
pkill -f 'celery worker'

echo "[*] Starting Celery workers..."
celery -A celery_app.task worker --loglevel=info -n worker@%h &

echo "[*] Starting Flask via Gunicorn..."
gunicorn -w 2 -b 0.0.0.0:5000 app:app
