from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import EjercicioBase, EjercicioCreate, EjercicioUpdate, Ejercicio
from db import DBsesion

router = APIRouter()
tag_ejercicio = "Ejercicios"

#Crear un nuevo ejercicio
@router.post("/ejercicios", response_model=Ejercicio, tags=[tag_ejercicio])
def crear_Ejercicio(datos_ejercicio: EjercicioCreate, session: DBsesion):
    ejercicio = Ejercicio.model_validate(datos_ejercicio.model_dump())
    session.add(ejercicio)
    session.commit()
    session.refresh(ejercicio)
    return ejercicio


#Listar los ejercicios
@router.get("/ejercicios", tags=[tag_ejercicio])
def listar_Ejercicios(session: DBsesion):
    return session.exec(select(Ejercicio)).all()


#Obtener ejercicio por id
@router.get("/ejercicios/{ejercicio_id}", tags=[tag_ejercicio])
def obtener_Ejercicio(ejercicio_id:int, session:DBsesion):
    ejercicio_db = session.get(Ejercicio, ejercicio_id)
    if not ejercicio_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ejercicio no encontado")
    return ejercicio_db

# Actualizar un ejercicio
@router.patch("/ejercicios/{ejercicio_id}", tags=[tag_ejercicio])
def actualizar_ejercicio(ejercicio_id:int, datosEjercicio:EjercicioUpdate, session:DBsesion):
    ejercicio_db = session.get(Ejercicio, ejercicio_id)
    if not ejercicio_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ejercicio no encontrado")
    
    diccionario_ejercicio = datosEjercicio.model_dump(exclude_unset=True)
    ejercicio_db.sqlmodel_update(diccionario_ejercicio)
    session.add(ejercicio_db)
    session.commit()
    session.refresh(ejercicio_db)
    return ejercicio_db

# Eliminar un ejercicio
@router.delete("/ejercicio/{ejercicio_id}", tags=[tag_ejercicio])
def eliminar_ejercicio(ejercicio_id:int, session:DBsesion):
    ejercicio_db = session.get(Ejercicio, ejercicio_id)
    if not ejercicio_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ejercicio no encontrado")
    
    session.delete(ejercicio_db)
    session.commit()
    return {"detail": "Ejercicio eliminado"}