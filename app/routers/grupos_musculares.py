from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import GrupoMuscularBase, GrupoMuscularCreate, GrupoMuscularUpdate, GrupoMuscular
from db import DBsesion

router = APIRouter()
router_tag = "Grupos Musculares"

# Endpoint para crear un grupo muscular
@router.post("/grupo_muscular", response_model=GrupoMuscular, tags=[router_tag])
def crear_grupo_muscular(datos_grupo: GrupoMuscularCreate, session:DBsesion):
    grupo = GrupoMuscular.model_validate(datos_grupo.model_dump())
    session.add(grupo)
    session.commit()
    session.refresh(grupo)
    return grupo


# Endpoint para listar los grupos musculares
@router.get("/grupo_muscular", tags=[router_tag])
def listar_grupos_musculares(session:DBsesion):
    return session.exec(select(GrupoMuscular)).all()

# Endpoint para obtener un grupo muscular por id
@router.get("/grupo_muscular/{grupo_id}", tags=[router_tag])
def obtener_grupo_muscular(grupo_id:int, session:DBsesion):
    grupo = session.get(GrupoMuscular, grupo_id)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo

# Endpoint para actualizar un grupo muscular
@router.patch("/grupo_muscular/{grupo_id}", tags=[router_tag])
def actualizar_grupo_muscular(grupo_id:int, datos_grupo:GrupoMuscularUpdate, session:DBsesion):
    grupo = session.get(GrupoMuscular, grupo_id)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    grupo_dict = datos_grupo.model_dump(exclude_unset=True)
    grupo.sqlmodel_update(grupo_dict)
    session.add(grupo)
    session.commit()
    session.refresh(grupo)
    return grupo

# Endpoint para eliminar grupo muscular
@router.delete("/grupo_muscular/{grupo_id}", tags=[router_tag])
def eliminar_grupo_muscular(grupo_id:int, session:DBsesion):
    grupo = session.get(GrupoMuscular, grupo_id)
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    session.delete(grupo)
    session.commit()
    return {"detail": "Grupo Eliminado"}