## Micro framework based on FastAPI
#### Dependencies
- Uvicorn
- Celery
- Redis
- Postgresql
- Nginx
- PyTest
- Docker

#### Features
- Json Web Token Authentication
- Registration and Authentication
- Emails sending
- Background Tasks
- Files uploading
- Websockets
- Queue messagings
- Unit tests
- Cli commands

#### How to use
- Run app
```bash
python manage.py serve
```

Go to [localhost:8000](http://localhost:8000)

- Make database migrations

```bash
aerich migrate --name [your migration name]
```

- Commit migration

```aerich upgrade```
