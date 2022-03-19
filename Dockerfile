FROM python:3.10.3-slim-bullseye


RUN apt-get update -qq && apt-get install -y postgresql-client

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml /app/


# RUN apt-get update -y && apt-get install -y \
#     llibressl-dev libffi-dev gcc musl-dev python3-dev \
#     postgresql-dev bash;


RUN pip3 install poetry \
    && rm -rf /root/.cache/pip 

RUN poetry install
# COPY . /app/