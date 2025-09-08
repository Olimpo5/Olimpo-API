from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import NivelDificultad, NivelDificultadBase, NivelDificultadCreate, NivelDificultadUpdate
from db import DBsesion

router = APIRouter()
router_tag = "Nivel de Dificultad"

# Endpoint para crear un nivel de dificultad
@router.post("/nivel_dificultad", response_model=NivelDificultad,tags=[router_tag])
def crear_nivel_dificultad(datos_dificultad:NivelDificultadCreate, session: DBsesion):
    nivel = NivelDificultad.model_validate(datos_dificultad.model_dump())
    session.add(nivel)
    session.commit()
    session.refresh(nivel)
    return nivel


# Endpoint para listar los niveles de dificultad existentes
@router.get("/nivel_dificultad", tags=[router_tag])
def listar_niveles(session:DBsesion):
    return session.exec(select(NivelDificultad)).all()

# Endpoint para listar un nivel especifico
@router.get("/nivel_dificultad/{nivel_id}", tags=[router_tag])
def obtener_nivel(nivel_id:int, session:DBsesion):
    nivel = session.get(NivelDificultad, nivel_id)
    if not nivel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el nivel")
    
    return nivel


# Endpoint para actualizar un nivel
@router.patch("/nivel_dificultad/{ejercicio_id}", tags=[router_tag])
def actualizar_nivel(nivel_id:int, datos_nivel:NivelDificultadUpdate, session:DBsesion):
    nivel = session.get(NivelDificultad, nivel_id)
    if not nivel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el nivel")
    nivel_diccionario = datos_nivel.model_dump(exclude_unset=True)
    nivel.sqlmodel_update(nivel_diccionario)
    session.add(nivel)
    session.commit()
    session.refresh(nivel)
    return nivel     


# Endpoint para eliminar un nivel
@router.delete("/nivel_dificultad/{nivel_id}", tags=[router_tag])
def eliminar_nivel(nivel_id:int, session:DBsesion):
    nivel = session.get(NivelDificultad, nivel_id)
    if not nivel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el nivel")
    session.delete(nivel)
    session.commit()
    return {"detail": "Se elimino el nivel"} 