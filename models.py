from pydantic import BaseModel

# Datos del usuario que necesitamos para rellenar en formularios
class UsuarioBase(BaseModel):
    correo: str
    password: str
    nombre: str
    apellido: str
    fecha_nacimiento: str
    peso: str
    altura: str
    foto_perfil: str
    objetivo: str

# Generacion de id de manera automatica
class Usuario(UsuarioBase):
    id_usuario:int | None = None


class Rutina(BaseModel):
    id_rutina: int
    id_nivel_dificultad: int
    nombre: str
    descripcion: str
    fecha_creacion: str
    duracion: int
    frecuencia_semanal: int 

class Ejercicio(BaseModel):
    id_ejercicio: int
    id_nivel_dificultad: int
    nombre: str
    descripcion: str
    video_demostrativo: str