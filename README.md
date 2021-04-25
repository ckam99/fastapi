## FastAPI with OAuth2 authencation

- Run app
```bash
uvicorn core:app --reload 
# or
python main.py
```
Go to [localhost:8000](http://localhost:8000)

- Make database migrations

```bash
aerich migrate
```

- Commit migration

```aerich upgrade```