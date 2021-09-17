from sqlmodel import SQLModel, create_engine

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def create_db_schemas():
    SQLModel.metadata.create_all(engine)

