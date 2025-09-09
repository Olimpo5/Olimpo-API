from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import TipoTrabajadoBase, TipoTrabajadoCreate, TipoTrabajadoUpdate, TipoTrabajado
from db import DBsesion

router = APIRouter()
tag_router = "Tipo trabajado"

# Endpoint para crear tipos de trabajo
@router.post("/tipo_trabajado", response_model=TipoTrabajado, tags=[tag_router])
def crear_tipo(session:DBsesion, datos:TipoTrabajadoCreate):
    tipo = TipoTrabajado.model_validate(datos.model_dump())
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo


# Endpoint para listar los tipos de trabajo
@router.get("/tipo_trabajado", tags=[tag_router])
def listar_tipos(session:DBsesion):
    return session.exec(select(TipoTrabajado)).all()

# Endpoint para listar por id de tipo trabajado
@router.get("/tipo_trabajado/{id_tipo}", tags=[tag_router])
def listar_tipo(session:DBsesion, id_tipo:int):
    tipo = session.get(TipoTrabajado, id_tipo)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="tipo no encontrado")
    return tipo


# Endpoint para actualizar tipo
@router.patch("/tipo_trabajado/{id_tipo}", tags=[tag_router])
def actualizar_tipo(session:DBsesion, id_tipo:int, datos_tipo:TipoTrabajadoUpdate):
    tipo = session.get(TipoTrabajado, id_tipo)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el tipo")
    
    tipo_dict = datos_tipo.model_dump(exclude_unset=True)
    tipo.sqlmodel_update(tipo_dict)
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo


# Endpoint para eliminar tipo
@router.delete("/tipo_trabajado/{id_tipo}", tags=[tag_router])
def eliminar_tipo(session:DBsesion, id_tipo:int):
    tipo = session.get(TipoTrabajado, id_tipo)
    if not tipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el tipo")
    session.delete(tipo)
    session.commit()
    return {"detail": "Tipo eliminado"}
