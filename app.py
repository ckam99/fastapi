from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
import uvicorn

app = FastAPI()

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)


@app.get('/')
def index():
    return {'message': 'hello'}


if __name__ == '__main__':
    uvicorn.run(app=app)
