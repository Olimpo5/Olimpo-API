from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

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

class Usuario(UsuarioBase, table=True):
    id_usuario:int | None = Field(default=None, primary_key=True)
    rutinas: list["Rutina"] = Relationship(back_populates="usuario")

# Modelo de Rutina
class RutinaBase(SQLModel):
    nombre: str = Field(default=None, max_length=50, nullable=False)
    descripcion: str = Field(default=None, max_length=50, nullable=False)
    fecha_creacion: str = Field(default=None, max_length=50, nullable=False)
    duracion_minutos: int = Field(default=None, nullable=True)
    frecuencia_semanal: int = Field(default=None, nullable=True)

class RutinaCreate(RutinaBase):
    pass

class RutinaUpdate(RutinaBase):
    pass

class Rutina(RutinaBase, table=True):
    id_rutina: int | None = Field(default=None, primary_key=True)
    usuario_id: int | None = Field(default=None, foreign_key="usuario.id_usuario")
    usuario : Optional[Usuario] = Relationship(back_populates="rutinas")
    # id_nivel_dificultad: int | None = Field(default=None, foreign_key="")



# class Ejercicio(BaseModel):
#     id_ejercicio: int
#     id_nivel_dificultad: int
#     nombre: str
#     descripcion: str
#     video_demostrativo: str