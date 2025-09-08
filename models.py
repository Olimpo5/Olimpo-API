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
    id_nivel_dificultad: int | None = Field(default=None, foreign_key="niveldificultad.id_nivel_dificultad")
    ejercicio_rutinas: list["EjercicioRutina"] = Relationship(back_populates="rutina")
    
    grupos_musculares: list["RutinaGrupoMuscular"] = Relationship(back_populates="rutina")




#Tabla Ejercicio_Rutina (tabla de detalle)
class EjercicioRutina(SQLModel, table=True):
    id_ejercicio_rutina: int | None = Field(default=None, primary_key=True, nullable=False)
    id_ejercicio: int | None = Field(default=None, foreign_key="ejercicio.id_ejercicio")
    id_rutina: int | None = Field(default=None, foreign_key="rutina.id_rutina")
    id_nivel_dificultad: int | None = Field(default=None, foreign_key="niveldificultad.id_nivel_dificultad", nullable=False)
    rutina: Optional["Rutina"] = Relationship(back_populates="ejercicio_rutinas")
    ejercicio: Optional["Ejercicio"] = Relationship(back_populates="ejercicio_rutinas")




# Tabla Nivel Dificultad (Tabla de Detalle)
class NivelDificultad(SQLModel, table=True):
    id_nivel_dificultad: int | None = Field(default=None, nullable=False, primary_key=True)
    nombre: str = Field(nullable=False, max_length=50)
    descripcion: str = Field(nullable=False, max_length=50)
    valor_numerico: int = Field(nullable=False)






# Modelo de Ejercicios
class EjercicioBase(SQLModel):
    nombre: str = Field(default=None, max_length=50, nullable=False)
    descripcion: str = Field(default=None, max_length=50, nullable=False)
    video_demostrativo: str = Field(default=None, nullable=False)

class EjercicioCreate(EjercicioBase):
    pass

class EjercicioUpdate(EjercicioBase):
   pass

class Ejercicio(EjercicioBase, table=True):
    id_ejercicio: int | None = Field(default=None, primary_key=True)
    id_nivel_dificultad: int | None = Field(default=None, foreign_key="niveldificultad.id_nivel_dificultad")
    id_equipo_necesario: int | None = Field(default=None, foreign_key="equiponecesario.id_equipo_necesario")
    ejercicio_rutinas: list["EjercicioRutina"] = Relationship(back_populates="ejercicio")

    grupos_musculares: list["EjercicioGrupoMuscular"] = Relationship(back_populates="ejercicio")
    equipo_necesario: Optional["EquipoNecesario"] = Relationship(back_populates="ejercicios")





#Modelo Equipo Necesario
class EquipoNecesarioBase(SQLModel):
    nombre: str = Field(max_length=50, nullable=False)
    descripcion: str = Field(max_length=50, nullable=False)
    url_equipo: str = Field(max_length=50, nullable=False)
    cantidad: int = Field(nullable=True)

class EquipoNecesarioCreate(EquipoNecesarioBase):
    pass

class EquipoNecesarioUpdate(EquipoNecesarioBase):
    pass

class EquipoNecesario(EquipoNecesarioBase, table=True):
    id_equipo_necesario: int = Field(nullable=False, primary_key=True)
    ejercicios: list["Ejercicio"] = Relationship(back_populates="equipo_necesario")





#Modelo Grupo Muscular

class GrupoMuscularBase(SQLModel):
    nombre: str = Field(max_length=50, nullable=False)
    descripcion: str = Field(max_length=50, nullable=False)

class GrupoMuscularCreate(GrupoMuscularBase):
    pass

class GrupoMuscularUpdate(GrupoMuscularBase):
    pass

class GrupoMuscular(SQLModel, table=True):
    id_grupo_muscular: int = Field(nullable=False, primary_key=True)
    
    ejercicios_enfocados: list["EjercicioGrupoMuscular"] = Relationship(back_populates="grupo_muscular")
    rutinas_enfocadas: list["RutinaGrupoMuscular"] = Relationship(back_populates="grupo_muscular")



# Tabla de Detalle Rutina Grupo Muscular

class RutinaGrupoMuscular(SQLModel, table=True):
    id_rutina_grupo_muscular: int = Field(nullable=False, primary_key=True)
    id_grupo_muscular: int = Field(nullable=False, foreign_key="grupomuscular.id_grupo_muscular")
    id_rutina: int = Field(nullable=False, foreign_key="rutina.id_rutina")
    nombre: str = Field(nullable=False, max_length=50)
    descripcion: str = Field(nullable=False, max_length=50)

    #Codigo sin checar aun
    rutina: Optional["Rutina"] = Relationship(back_populates="grupos_musculares")
    grupo_muscular: Optional["GrupoMuscular"] = Relationship(back_populates="rutinas_enfocadas")


# Tabla de Detalle Ejercicio Grupo Muscular
class EjercicioGrupoMuscular(SQLModel, table=True):
    id_ejercicio_grupo_muscular: int = Field(nullable=False, primary_key=True)
    id_grupo_muscular: int = Field(nullable=False, foreign_key="grupomuscular.id_grupo_muscular")
    id_ejercicio: int = Field(nullable=False, foreign_key="ejercicio.id_ejercicio")
    id_tipo_trabajado: int = Field(foreign_key="tipotrabajado.id_tipo_trabajado")
    nombre: str = Field(max_length=50, nullable=False)
    descripcion: str = Field(max_length=50, nullable=False)

    # Codigo sin checar aun
    ejercicio: Optional["Ejercicio"] = Relationship(back_populates="grupos_musculares")
    grupo_muscular: Optional["GrupoMuscular"] = Relationship(back_populates="ejercicios_enfocados")
    tipo_trabajado: Optional["TipoTrabajado"] = Relationship(back_populates="ejercicio_grupo_muscular")


# Falta la tabla de Tipo Trabajado
class TipoTrabajado(SQLModel, table=True):
    id_tipo_trabajado: int = Field(primary_key=True, nullable=False, default=None)
    nombre: str = Field(max_length=50, nullable=False)
    descripcion: str = Field(max_length=50, nullable=False)
    ejercicio_grupo_muscular: list["EjercicioGrupoMuscular"] = Relationship(back_populates="tipo_trabajado")
