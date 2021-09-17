from fastapi import FastAPI
from generics.database import connect_db
from generics.middlewares import register_cors

from routes import users, posts
app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)


@app.on_event('startup')
def on_start():
    connect_db(app)
    register_cors(app)
