#!/usr/bin/env bash
set -e

if [ -n "$DB_HOST" ]; then
  echo "Waiting for database at ${DB_HOST}:${DB_PORT:-5432}..."
  until python -c "
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
sys.exit(0 if s.connect_ex(('${DB_HOST}', ${DB_PORT:-5432})) == 0 else 1)
"; do
    sleep 1
  done
  echo "Database is up."
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting ASGI server..."
exec gunicorn -k uvicorn.workers.UvicornWorker core.asgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-60}" \
  --graceful-timeout "${GUNICORN_GRACEFUL_TIMEOUT:-30}" \
  --max-requests "${GUNICORN_MAX_REQUESTS:-1000}" \
  --max-requests-jitter "${GUNICORN_MAX_REQUESTS_JITTER:-100}" \
  --access-logfile - \
  --access-logformat '{"ts":"%(t)s","remote_addr":"%(h)s","request_id":"%({X-Request-ID}i)s","method":"%(m)s","path":"%(U)s","query":"%(q)s","status":%(s)s,"bytes":%(B)s,"referrer":"%(f)s","ua":"%(a)s","request_time":%(L)s}'
