from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import EquipoNecesarioBase, EquipoNecesarioCreate, EquipoNecesarioUpdate, EquipoNecesario
from db import DBsesion

router = APIRouter()
tag_router = "Equipo Necesario"

# Crear equipo necesario
@router.post("/equipoNecesario", response_model=EquipoNecesario, tags=[tag_router])
def crear_EquipoNecesario(datos_equipo:EquipoNecesarioCreate, session:DBsesion):
    equipo = EquipoNecesario.model_validate(datos_equipo.model_dump())
    session.add(equipo)
    session.commit()
    session.refresh(equipo)
    return equipo

# listar el equipo necesario
@router.get("/equipoNecesario", tags=[tag_router])
def listar_EquipoNecesario(session:DBsesion):
    return session.exec(select(EquipoNecesario)).all()


# Obtener un equipo por su numero de id
@router.get("/equipoNecesario/{id_equipo_necesario}", tags=[tag_router])
def obtener_equipo(id_equipo:int, session:DBsesion):
    equipo_db = session.get(EquipoNecesario, id_equipo)
    if not equipo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontado")
    return equipo_db



# Actualizar el equipo necesario
@router.patch("/equipoNecesario/{id_equipo_necesario}", tags=[tag_router])
def actualizar_equipo_necesario(equipo_id:int, datos_equipo:EquipoNecesarioUpdate, session:DBsesion):
    equipo_db = session.get(EquipoNecesario, equipo_id)
    if not equipo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    
    equipo_dict = datos_equipo.model_dump(exclude_unset=True)
    equipo_db.sqlmodel_update(equipo_dict)
    session.add(equipo_db)
    session.commit()
    session.refresh(equipo_db)
    return equipo_db

# Eliminar el equipo necesario
@router.delete("/equipoNecesario/{id_equipo_necesario}", tags=[tag_router])
def eliminar_equipo_necesario(equipo_id:int, session: DBsesion):
    equipo_db = session.get(EquipoNecesario, equipo_id)
    if not equipo_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    session.delete(equipo_db)
    session.commit()
    return {"detail": "Equipo eliminado exitosamente"}  


# ENDPOINT RELACIONAL

# Endpoint para ver los ejercicios que usan un determinado equipo
@router.get("/EquipoNecesario/{id_equipo_necesario}", tags=[tag_router])
def listar_ejercicios_por_equipo(id_equipo:int, session:DBsesion):
    equipo = session.get(EquipoNecesario, id_equipo)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    ejercicios = equipo.ejercicios  

    return {"equipo_id": id_equipo, "nombre_equipo": equipo.nombre, "ejercicios": ejercicios}