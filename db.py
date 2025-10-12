from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Session, create_engine, SQLModel
import os
from dotenv import load_dotenv

# Cargar variables desde .env (opcional)
load_dotenv()

# 🔧 Datos de conexión a PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123456")
POSTGRES_DB = os.getenv("POSTGRES_DB", "OlimpoDB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")  # API corre local
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Connection string PostgreSQL
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Crear engine
engine = create_engine(DATABASE_URL, echo=True)

# Crear tablas al iniciar FastAPI
def crearTablasDB(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    print("Tablas creadas o verificadas en OlimpoDB.")
    yield

# Dependencia de sesión para endpoints
def iniciarDB():
    with Session(engine) as session:
        yield session

DBsesion = Annotated[Session, Depends(iniciarDB)]
