from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, payload: dict()):
    user = models.User(**payload)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_user_posts(db: Session, user_id: int):
    return db.query(models.Post).filter(models.Post.uder_id == user_id).all()


def create_user_post(db: Session, payload: dict, user_id: int):
    payload['user_id'] = user_id
    post = create_post(db,payload)
    return post
    
def create_post(db: Session, payload: dict):
    post = models.Post(**payload)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post