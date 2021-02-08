#  pull official base image
FROM python:3.8-slim

# https://docs.docker.com/compose/django/
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# install Django and other dependencies
COPY requirements.txt /app/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/
RUN chmod +x /app/entrypoint.sh
EXPOSE 8000


ENTRYPOINT ["sh", "/app/entrypoint.sh"]