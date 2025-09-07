from pydantic import BaseModel
from sqlmodel import SQLModel, Field

# Datos del usuario que necesitamos para rellenar en formularios
class UsuarioBase(SQLModel):
    correo: str = Field(default=None, max_length=50, nullable=False)
    password: str = Field(default=None, max_length=50, nullable=False)
    nombre: str = Field(default=None, max_length=50, nullable=False)
    apellido: str = Field(default=None, max_length=50, nullable=False)
    fecha_nacimiento: str = Field(default=None, max_length=50, nullable=False)
    peso: str = Field(default=None, max_length=50, nullable=False)
    altura: str = Field(default=None, max_length=50, nullable=False)
    foto_perfil: str = Field(default=None, max_length=50, nullable=False)
    objetivo: str = Field(default=None, max_length=50, nullable=False)


class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    pass

# Generacion de id de manera automatica
class Usuario(UsuarioBase, table=True):
    id_usuario:int | None = Field(default=None, primary_key=True)


# class Rutina(BaseModel):
#     id_rutina: int
#     id_nivel_dificultad: int
#     nombre: str
#     descripcion: str
#     fecha_creacion: str
#     duracion: int
#     frecuencia_semanal: int 

# class Ejercicio(BaseModel):
#     id_ejercicio: int
#     id_nivel_dificultad: int
#     nombre: str
#     descripcion: str
#     video_demostrativo: str