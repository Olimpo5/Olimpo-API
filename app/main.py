from fastapi import FastAPI, HTTPException, status
from models import Usuario, UsuarioUpdate, UsuarioCreate#, Rutina, Ejercicio
from db import DBsesion, crearTablasDB
from sqlmodel import select
from .routers import usuarios, rutinas

# Instanciamos FastAPI
app = FastAPI(lifespan=crearTablasDB)
app.include_router(usuarios.router)
app.include_router(rutinas.router)

@app.get("/")
def root():
    return {"message": "Hola Mundo"}


# @app.post("/rutina")
# def crear_Rutina(datos_rutina: Rutina):
#     return datos_rutina

# @app.post("/ejercicio")
# def crear_ejercicio(datos_ejercicio: Ejercicio):
#     return datos_ejercicio