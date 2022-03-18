# FastAPI with Apache Kafka

requirements

- poetry
- kafka
- python3.9

### Install dependencies

```bash
poetry install
```

### Run server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Remarque** if you note kafka installed then run `docker-compose -f kafka.yml up`
