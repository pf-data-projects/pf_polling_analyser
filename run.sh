#!/bin/bash

# Start Redis in the background
redis-server --save 60 1 --loglevel warning &

# Start Celery worker in the background
celery -A polling_analyser worker --loglevel=info &

# Start Gunicorn server
exec gunicorn --bind 0.0.0.0:3000 --timeout 3600 polling_analyser.wsgi