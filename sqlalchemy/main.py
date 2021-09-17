from fastapi import FastAPI,HTTPException,Depends
from typing import List
from sqlalchemy.orm import Session

import services
import models
import schemas
from database import engine, SessionLocal

models.BaseModel.metadata.create_all(bind=engine)

app=FastAPI()


def get_db():
   try:
   	  db = SessionLocal()
   	  yield db
   finally:
   	  db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_user(db=db, payload=user.dict())


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{user_id}/posts/", response_model=List[schemas.Post])
def get_user_posts(
    user_id: int, db: Session = Depends(get_db)
):
    return services.get_user_post(db=db, user_id=user_id)


@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_user_posts(
    user_id: int, payload: schemas.BasePost, db: Session = Depends(get_db)
):
    return services.create_user_post(db=db, payload=payload.dict(), user_id=user_id)


@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = services.get_posts(db, skip=skip, limit=limit)
    return posts

@app.post("/posts/", response_model=schemas.Post)
def create_posts(payload: schemas.PostCreate, db: Session = Depends(get_db)
):
    return services.create_post(db=db, payload=payload.dict())
    
