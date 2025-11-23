from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import Usuario, UsuarioUpdate, UsuarioCreate#, Rutina, Ejercicio
from db import DBsesion, crearTablasDB
from sqlmodel import select
from .routers import usuarios, rutinas, ejercicios, equipo_necesario, grupos_musculares, nivel_dificultad, tipo_trabajado, chat

# Instanciamos FastAPI
app = FastAPI(lifespan=crearTablasDB)
app.include_router(usuarios.router)
app.include_router(rutinas.router)
app.include_router(ejercicios.router)
app.include_router(equipo_necesario.router)
app.include_router(grupos_musculares.router)
app.include_router(nivel_dificultad.router)
app.include_router(tipo_trabajado.router)

#Agregando endpoint websocket de gemini
app.include_router(chat.router, tags=["WebSockets"])

# Configuracion CORS para react native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenido al Olimpo"}
