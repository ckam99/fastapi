FROM python:3.9.7-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    libressl-dev libffi-dev gcc musl-dev python3-dev \
    postgresql-dev bash \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app

EXPOSE 3000

CMD [ "uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=3000" ]

