from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import RutinaBase, RutinaCreate, RutinaUpdate, Rutina, Usuario
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


# endpoint para crear rutinas basadas en un id de usuario
@router.post("/rutinas/{id_usuario}", response_model=Rutina, tags=["Rutinas"])
def crear_rutina_usuario(id_usuario: int, datos_rutina: RutinaCreate, session: DBsesion):
    # Verificar si el usuario existe
    usuario = session.exec(select(Usuario).where(Usuario.id_usuario == id_usuario)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Crear la rutina asociada al usuario
    rutina = Rutina.model_validate(datos_rutina.model_dump())
    rutina.usuario_id = id_usuario

    session.add(rutina)
    session.commit()
    session.refresh(rutina)

    return rutina

# endpoint para listar las rutinas de un usuario
@router.get("/usuarios/{id_usuario}/rutinas", response_model=list[Rutina], tags=["Rutinas"])
def listar_rutinas_de_usuario(id_usuario: int, session: DBsesion):
    # Verifica si el usuario existe
    usuario = session.exec(select(Usuario).where(Usuario.id_usuario == id_usuario)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Buscar las rutinas asociadas al usuario
    rutinas = session.exec(select(Rutina).where(Rutina.usuario_id == id_usuario)).all()
    return rutinas

# endpoint para actualizar rutinas
@router.patch("/rutinas/{id_rutina}", response_model=Rutina, status_code=status.HTTP_201_CREATED, tags=[rutina_tag])
def actualizar_rutina(rutina_id:int, datos_rutina: RutinaUpdate, session:DBsesion):
    rutina_db = session.get(Rutina, rutina_id)
    if not rutina_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rutina no encontrada")
    
    rutina_dict = datos_rutina.model_dump(exclude_unset=True)
    rutina_db.sqlmodel_update(rutina_dict)
    session.add(rutina_db)
    session.commit()
    session.refresh(rutina_db)
    return rutina_db



# endpoint para eliminar rutinas
@router.delete("/usuarios/{usuario_id}/rutinas/{rutina_id}", tags=["Rutinas"])
def eliminar_rutina_de_usuario(
    usuario_id: int,
    rutina_id: int,
    session: DBsesion
):
    # Verificar si la rutina existe y pertenece al usuario
    rutina = session.exec(
        select(Rutina)
        .where(Rutina.id_rutina == rutina_id, Rutina.usuario_id == usuario_id)
    ).first()

    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada para este usuario.")

    # Eliminar rutina
    session.delete(rutina)
    session.commit()

    return {"mensaje": f"Rutina con ID {rutina_id} eliminada correctamente para el usuario {usuario_id}."}