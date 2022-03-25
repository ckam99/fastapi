FROM python:3.10.3-slim-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



# set work directory
WORKDIR /app



RUN apt-get update -qq && apt-get install -y postgresql-client bash

COPY poetry.lock pyproject.toml /app/


# RUN apt-get update -y && apt-get install -y \
#     llibressl-dev libffi-dev gcc musl-dev python3-dev \
#     postgresql-dev bash;


RUN pip3 install poetry

RUN poetry install
# COPY . /app/