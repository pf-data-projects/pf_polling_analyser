
FROM python:3.7

WORKDIR /app

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

CMD gunicorn --bind 0.0.0.0:3000 --timeout 3600 polling_analyser.wsgi
