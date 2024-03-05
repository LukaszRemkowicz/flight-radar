FROM python:3.11-slim-buster as development

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /flight_radar

RUN ln -sf /usr/share/zoneinfo/Europe/Warsaw /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Europe/Warsaw /etc/localtime

RUN pip install --upgrade pip --no-cache-dir

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libjpeg-dev \
    gcc \
    libc-dev \
    libpq-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

# Install Pipenv and project dependencies
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile
# Install psycopg2 separately due to potential issues with Pipenv
RUN pipenv install psycopg2-binary

# Install additional development dependencies
RUN pipenv install --deploy --ignore-pipfile --dev

COPY ./flight_radar /flight_radar
