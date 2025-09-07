from fastapi import FastAPI, HTTPException, status
from models import Usuario, UsuarioUpdate, UsuarioCreate#, Rutina, Ejercicio
from db import DBsesion, crearTablasDB
from sqlmodel import select

# Instanciamos FastAPI
app = FastAPI(lifespan=crearTablasDB)

@app.get("/")
def root():
    return {"message": "Hola Mundo"}

# Array que contiene los usuarios creados por mientras
db_usuarios = []

#endpoint para crear usuarios
@app.post("/usuarios", response_model=Usuario)
def crear_Usuario(datos_usuario: UsuarioCreate, session: DBsesion):
    usuario = Usuario.model_validate(datos_usuario.model_dump())
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

#endpoint para listar los usuarios creados
@app.get("/usuarios", response_model=db_usuarios)
def lista_usuarios(session: DBsesion):
    return session.exec(select(Usuario)).all()


#Mostrar un usuario por su numero de id
@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def ver_usuario(usuario_id:int, session: DBsesion):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el usuario")
    return usuario_db

#Eliminar un usuario por su numero de id
@app.delete("/usuarios/{usuario_id}")
def borrar_usuario(usuario_id:int, session: DBsesion):
    usuario_db = session.get(Usuario, usuario_id)
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")
    session.delete(usuario_db)
    session.commit()
    return {"detail": "Usuario eliminado"}

# Actualizar un usuario por su numero de id
@app.patch("/usuarios/{usuario_id}", response_model=Usuario, status_code=status.HTTP_201_CREATED)
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

# @app.post("/rutina")
# def crear_Rutina(datos_rutina: Rutina):
#     return datos_rutina

# @app.post("/ejercicio")
# def crear_ejercicio(datos_ejercicio: Ejercicio):
#     return datos_ejercicio