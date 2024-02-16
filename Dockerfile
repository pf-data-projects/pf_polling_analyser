
FROM python:3.9-alpine

WORKDIR /app

RUN pip install --upgrade pip

# Install PostgreSQL development files
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Install build dependencies
RUN apk add --no-cache build-base libffi-dev musl-dev linux-headers

# Install build tools, Python dev files, and C++ compiler
RUN apk add --no-cache \
    build-base \
    python3-dev \
    musl-dev \
    openssl-dev \
    # C++ build tools
    cmake \
    make \
    # Arrow dependencies
    boost-dev \
    # Additional dependencies for Arrow
    autoconf \
    zlib-dev \
    flex \
    bison \
    # Additional dependencies for pyzmq
    zeromq-dev

# Install build dependencies for Arrow and pyarrow
RUN apk add --no-cache \
    gcc \
    g++ \
    automake \
    libtool \
    bzip2-dev \
    lz4-dev \
    zstd-dev \
    wget

# Download and extract Apache Arrow source code
RUN wget https://github.com/apache/arrow/archive/refs/tags/apache-arrow-12.0.0.tar.gz -O arrow.tar.gz \
    && tar -xzf arrow.tar.gz \
    && rm arrow.tar.gz

# Navigate to the Apache Arrow C++ source directory, build, and install
RUN cd arrow-apache-arrow-12.0.0/cpp \
    && mkdir build \
    && cd build \
    && cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local -DARROW_CSV=ON -DARROW_JSON=ON -DARROW_FILESYSTEM=ON \
    && make \
    && make install

ENV ARROW_HOME=/usr/local
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV PYARROW_CMAKE_OPTIONS="-DCMAKE_PREFIX_PATH=/usr/local"

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
