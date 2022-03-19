## Run web app

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Run celery worker

```bash
celery -A core.celery worker  --loglevel=info
```
