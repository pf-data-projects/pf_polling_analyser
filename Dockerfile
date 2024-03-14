# Use a Python 3.9 image based on Debian slim
FROM python:3.9-slim

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install system dependencies
# Debian's package manager is `apt-get`. We'll update the package lists and install the necessary packages.
# Note: Debian slim images include more out-of-the-box than Alpine, so some packages like python3-dev are not needed.
RUN apt-get update && apt-get install -y \
    dos2unix \
    postgresql-client libpq-dev gcc libffi-dev libssl-dev \
    build-essential cmake make \
    # For Arrow dependencies and pyzmq, if needed. Adjust as necessary for your project's specific dependencies.
    libboost-all-dev \
    autoconf zlib1g-dev flex bison \
    libzmq3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Redis. Note: In production, it's recommended to use a separate Redis service rather than installing it in the same container.
RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install uvicorn gunicorn httptools uvloop

# Copy your application code to the container
COPY . .

# Adjust settings.py for ALLOWED_HOSTS
RUN sed -i 's/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = ["*"]/g' ./*/settings.py

# Set build arguments
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

# Install requirements
RUN pip3 install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Copy and make the run.sh script executable
COPY run.sh /app/run.sh
RUN dos2unix /app/run.sh && chmod +x /app/run.sh

# Uncomment to start the application using the run.sh script
CMD ["/bin/sh", "/app/run.sh"]

# Uncomment to use gunicorn directly
# CMD gunicorn --bind 0.0.0.0:3000 --timeout 3600 polling_analyser.wsgi

