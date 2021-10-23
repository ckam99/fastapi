FROM python:3.9.7-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /app

EXPOSE 3000

CMD [ "uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=3000" ]

