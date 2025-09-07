from fastapi import FastAPI
from models import Usuario, Rutina, Ejercicio

# Instanciamos FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hola Mundo"}

# Array que contiene los usuarios creados por mientras
db_usuarios = []

#endpoint para crear usuarios
@app.post("/usuarios", response_model=Usuario)
def crear_Usuario(datos_usuario: Usuario):
    usuario = Usuario.model_validate(datos_usuario.model_dump())
    usuario.id_usuario = len(db_usuarios)
    db_usuarios.append(usuario)
    return usuario

#endpoint para listar los usuarios creados
@app.get("/usuarios", response_model=db_usuarios)
def lista_usuarios():
    return db_usuarios

@app.post("/rutina")
def crear_Rutina(datos_rutina: Rutina):
    return datos_rutina

@app.post("/ejercicio")
def crear_ejercicio(datos_ejercicio: Ejercicio):
    return datos_ejercicio