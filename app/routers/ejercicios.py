from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import EjercicioBase, EjercicioCreate, EjercicioUpdate, Ejercicio
from db import DBsesion

router = APIRouter()
tag_ejercicio = "Ejercicios"

@router.post("/ejercicios", response_model=Ejercicio, tags=[tag_ejercicio])
def crear_Ejercicio(datos_ejercicio: EjercicioCreate, session: DBsesion):
    ejercicio = Ejercicio.model_validate(datos_ejercicio.model_dump())
    session.add(ejercicio)
    session.commit()
    session.refresh(ejercicio)
    return ejercicio
