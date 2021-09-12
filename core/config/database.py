from sqlmodel import create_engine, Session
from core.settings import DATABASES
import os

SQLALCHEMY_DATABASE_URL = DATABASES[os.environ.get('DB_ENGINE', 'sqlite')]

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       echo=True)
session = Session(bind=engine)
