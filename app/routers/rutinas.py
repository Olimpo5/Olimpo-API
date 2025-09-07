from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import RutinaBase, RutinaCreate, RutinaUpdate, Rutina
from db import DBsesion

router = APIRouter()
rutina_tag = "Rutinas"

# endpoint para crear rutinas
@router.post("/rutinas", response_model=Rutina, tags=[rutina_tag])
def crear_rutina(datos_rutina: RutinaCreate, session:DBsesion):
    rutina = Rutina.model_validate(datos_rutina.model_dump())
    session.add(rutina)
    session.commit()
    session.refresh(rutina)
    return rutina


# endpoint para listar rutinas
@router.get("/rutinas", tags=[rutina_tag])
def listar_rutinas(session: DBsesion):
    return session.exec(select(Rutina)).all()