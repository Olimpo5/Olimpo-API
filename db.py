from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Session, create_engine, SQLModel

sqlite_name = "db.sqlite"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

def crearTablasDB(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def iniciarDB():
    with Session(engine) as session:
        yield session

DBsesion = Annotated[Session, Depends(iniciarDB)]