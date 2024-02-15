#!/bin/bash

# Start Celery worker in the background
celery -A polling_analyser worker --loglevel=info -P gevent &

# Start Django development server
python manage.py runserver 127.0.0.1:8000