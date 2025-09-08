from fastapi import APIRouter, status, HTTPException
from sqlmodel import select
from models import Usuario, UsuarioUpdate, UsuarioCreate#, Rutina, Ejercicio
from db import DBsesion, crearTablasDB

router = APIRouter()

#endpoint para crear un usuarios
@router.post("/usuarios", response_model=Usuario, tags=["Usuarios"])
def crear_Usuario(datos_usuario: UsuarioCreate, session: DBsesion):
    usuario = Usuario.model_validate(datos_usuario.model_dump())
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

#endpoint para listar los usuarios creados
@router.get("/usuarios", tags=["Usuarios"])
def lista_usuarios(session: DBsesion):
    return session.exec(select(Usuario)).all()


#Mostrar un usuario por su numero de id
@router.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
def ver_usuario(usuario_id:int, session: DBsesion):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el usuario")
    return usuario_db

#Eliminar un usuario por su numero de id
@router.delete("/usuarios/{usuario_id}", tags=["Usuarios"])
def borrar_usuario(usuario_id:int, session: DBsesion):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")
    session.delete(usuario_db)
    session.commit()
    return {"detail": "Usuario eliminado"}

# Actualizar un usuario por su numero de id
@router.patch("/usuarios/{usuario_id}", response_model=Usuario, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def actualizar_usuario(usuario_id:int, datos_usuario: UsuarioUpdate, session: DBsesion):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el usuario")

    usuario_diccionario = datos_usuario.model_dump(exclude_unset=True)
    usuario_db.sqlmodel_update(usuario_diccionario)
    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)
    return usuario_db