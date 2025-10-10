from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import Ejercicio, EjercicioCreate, EjercicioUpdate
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


# ENDPOINT RELACIONALES DE LA TABLA EJERCICIO

#endpoints para ver las rutinas donde se utiliza un ejercicio
@router.get("/rutinas/{id_ejercicio}", tags=[tag_ejercicio])
def listar_rutinas_ejercicio(id_ejercicio:int, session:DBsesion):
    ejercicio = session.get(Ejercicio, id_ejercicio)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    query = (
        select(Rutina)
        .join(EjercicioRutina, EjercicioRutina.id_rutina == Rutina.id_rutina)
        .where(EjercicioRutina.id_ejercicio == id_ejercicio)
    )
    rutinas = session.exec(query).all()

    return {"ejercicio_id": id_ejercicio, "rutinas": rutinas}


# Endpoint para ver los grupos musculares trabajados por ejercicio
@router.get("/rutinas/grupo_muscular/{id_ejercicio}", tags=[tag_ejercicio])
def listar_gruposMusculares_ejercicio(id_ejercicio: int, session:DBsesion):
    ejercicio = session.get(Ejercicio, id_ejercicio)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    query = (
        select(GrupoMuscular)
        .join(EjercicioGrupoMuscular, EjercicioGrupoMuscular.id_grupo_muscular == GrupoMuscular.id_grupo_muscular)
        .where(EjercicioGrupoMuscular.id_ejercicio == id_ejercicio)
    )
    grupos = session.exec(query).all()

    return {"ejercicio_id": id_ejercicio, "grupos_musculares": grupos}
    

# Endpoint para ver el equipo necesario para un ejercicio
@router.get("/rutinas/equipoNecesario/{id_ejercicio}", tags=[tag_ejercicio])
def listar_equipoNecesario_ejercicio(id_ejercicio:int, session:DBsesion):
    ejercicio = session.get(Ejercicio, id_ejercicio)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    if not ejercicio.equipo_necesario:
        return {"ejercicio_id": id_ejercicio, "equipo_necesario": None}

    return {"ejercicio_id": id_ejercicio, "equipo_necesario": ejercicio.equipo_necesario}
