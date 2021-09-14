## Micro framework based on FastAPI

#### Features
- Json Web Token Authentication
- Registration users
- Password reset
- Send mails
- Background Tasks
- Files uploading
- Websockets
- Using brokers(Redis)
- Build for production using Docker
- Celery
- Flower
- Unit tests

#### How to use
- Run app
```bash
uvicorn core:app --reload 
```

Go to [localhost:8000](http://localhost:8000)

- Make database migrations

```bash
aerich migrate --name [your migration name]
```

- Commit migration

```aerich upgrade```
