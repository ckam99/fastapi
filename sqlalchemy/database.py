from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL='sqlite:///db.sqlite3'

engine=create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine )

BaseModel = declarative_base()


def get_db():
   try:
   	  db = SessionLocal()
   	  yield db
   finally:
   	  db.close()
      
