
FROM python:3.11.4-alpine

WORKDIR /app

# Install Redis
RUN apk update && apk add redis

RUN pip install uvicorn gunicorn httptools uvloop

COPY . .

RUN sed -i 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \["*"\]/g' ./*/settings.py

ARG SECRET_KEY
ARG API_TOKEN

ARG ALLOWED_HOSTS
ARG DATABASE_URL
ARG CLOUDINARY_URL
ARG ZEET_ENVIRONMENT
ARG GUNICORN_CMD_ARGS
ARG UVICORN_HOST
ARG API_SECRET
ARG GIT_COMMIT_SHA
ARG PYTHONUNBUFFERED
ARG ZEET_APP
ARG ZEET_PROJECT

RUN pip3 install -r requirements.txt

RUN python manage.py collectstatic --noinput

# Copy and make the run.sh script executable
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Start the application using the run.sh script
CMD ["/app/run.sh"]

# CMD gunicorn --bind 0.0.0.0:3000 --timeout 3600 polling_analyser.wsgi
