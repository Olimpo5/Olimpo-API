# Olimpo API

API REST desarrollada con FastAPI para la gestión de rutinas de ejercicio, usuarios y ejercicios. Incluye integración con Google Gemini para chat en tiempo real mediante WebSockets.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
  - [Con Docker](#con-docker)
  - [Sin Docker](#sin-docker)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Archivos Principales](#archivos-principales)
- [Routers y Endpoints](#routers-y-endpoints)
- [WebSockets y API de Gemini](#websockets-y-api-de-gemini)
- [Base de Datos](#base-de-datos)

## 🔧 Requisitos Previos

- Python 3.13 o superior
- PostgreSQL 16 o superior
- Docker y Docker Compose (opcional, para ejecutar con Docker)
- API Key de Google Gemini (para funcionalidad de chat)

## 📦 Instalación y Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456
POSTGRES_DB=OlimpoDB
POSTGRES_HOST=localhost  # o 'postgres' si usas Docker
POSTGRES_PORT=5432
GEMINI_API_KEY=tu_api_key_aqui
```

**Nota:** Para obtener una API Key de Gemini, visita [Google AI Studio](https://makersuite.google.com/app/apikey).

## 🚀 Ejecución del Proyecto

### Con Docker

Esta es la forma más sencilla de ejecutar el proyecto, ya que Docker se encarga de configurar tanto la aplicación como la base de datos.

#### 1. Construir y ejecutar los contenedores

```bash
docker-compose up --build
```

Este comando:
- Construye la imagen de la aplicación desde el `dockerfile`
- Inicia el contenedor de PostgreSQL
- Inicia el contenedor de la API
- Configura automáticamente las conexiones entre servicios

#### 2. Acceder a los servicios

- **API:** http://localhost:8000
- **Documentación interactiva (Swagger):** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432

#### 3. Detener los contenedores

```bash
docker-compose down
```

Para eliminar también los volúmenes (incluyendo los datos de la base de datos):

```bash
docker-compose down -v
```

### Sin Docker

Si prefieres ejecutar el proyecto sin Docker, sigue estos pasos:

#### 1. Crear entorno virtual

```bash
python3 -m venv env
```

#### 2. Activar el entorno virtual

**En Windows:**
```bash
env\Scripts\activate
```

**En Linux/Mac:**
```bash
source env/bin/activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar PostgreSQL

Asegúrate de tener PostgreSQL ejecutándose. Puedes usar un contenedor Docker solo para la base de datos:

```bash
docker run -d \
  --name postgres_olimpo \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=OlimpoDB \
  -p 5432:5432 \
  postgres:16
```

O instala PostgreSQL localmente y crea la base de datos `OlimpoDB`.

#### 5. Conectarse a PostgreSQL (opcional)

Si usas el contenedor Docker de PostgreSQL:

```bash
docker exec -it postgres_olimpo psql -U postgres
```

#### 6. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La aplicación estará disponible en:
- **API:** http://localhost:8000
- **Documentación interactiva:** http://localhost:8000/docs

## 📁 Estructura del Proyecto

```
Olimpo-API/
├── app/
│   ├── __init__.py          # Inicialización del paquete app
│   ├── main.py              # Punto de entrada de la aplicación FastAPI
│   └── routers/             # Módulos de rutas/endpoints
│       ├── __init__.py
│       ├── usuarios.py      # Endpoints para gestión de usuarios
│       ├── rutinas.py       # Endpoints para gestión de rutinas
│       ├── ejercicios.py    # Endpoints para gestión de ejercicios
│       ├── equipo_necesario.py  # Endpoints para equipamiento
│       ├── grupos_musculares.py # Endpoints para grupos musculares
│       ├── nivel_dificultad.py  # Endpoints para niveles de dificultad
│       ├── tipo_trabajado.py    # Endpoints para tipos de trabajo
│       └── chat.py          # WebSocket endpoint para chat con Gemini
├── db.py                    # Configuración de la base de datos
├── models.py                # Modelos SQLModel de la base de datos
├── dockerfile               # Configuración para construir imagen Docker
├── docker-compose.yaml      # Orquestación de servicios Docker
├── requirements.txt         # Dependencias de Python
├── default.conf            # Configuración de Nginx (comentada)
└── README.md               # Este archivo
```

## 📄 Archivos Principales

### `app/main.py`

Este es el archivo principal de la aplicación FastAPI. Contiene:

- **Instanciación de FastAPI:** Crea la aplicación con un `lifespan` que inicializa las tablas de la base de datos al arrancar
- **Inclusión de routers:** Registra todos los routers de la aplicación:
  - `usuarios` - Gestión de usuarios
  - `rutinas` - Gestión de rutinas de ejercicio
  - `ejercicios` - Gestión de ejercicios
  - `equipo_necesario` - Gestión de equipamiento necesario
  - `grupos_musculares` - Gestión de grupos musculares
  - `nivel_dificultad` - Gestión de niveles de dificultad
  - `tipo_trabajado` - Gestión de tipos de trabajo muscular
  - `chat` - WebSocket para chat con Gemini
- **Configuración CORS:** Permite peticiones desde cualquier origen (configurado para React Native)
- **Endpoint raíz:** Retorna un mensaje de bienvenida

### `db.py`

Gestiona la conexión a PostgreSQL:

- **Variables de entorno:** Lee la configuración de conexión desde variables de entorno o usa valores por defecto
- **Engine de SQLAlchemy:** Crea el motor de base de datos con la cadena de conexión
- **Función `crearTablasDB`:** Se ejecuta al iniciar la aplicación y crea todas las tablas definidas en `models.py`
- **Dependencia `DBsesion`:** Proporciona sesiones de base de datos a los endpoints mediante inyección de dependencias

### `models.py`

Define todos los modelos de datos usando SQLModel:

- **Usuario:** Información de usuarios (correo, contraseña, nombre, apellido, fecha de nacimiento, peso, altura, foto de perfil, objetivo)
- **Rutina:** Rutinas de ejercicio asociadas a usuarios
- **Ejercicio:** Ejercicios individuales con descripción y video demostrativo
- **EquipoNecesario:** Equipamiento necesario para ejercicios
- **GrupoMuscular:** Grupos musculares del cuerpo
- **NivelDificultad:** Niveles de dificultad (principiante, intermedio, avanzado)
- **TipoTrabajado:** Tipos de trabajo muscular (primario, secundario, etc.)
- **Tablas de relación:** `EjercicioRutina`, `RutinaGrupoMuscular`, `EjercicioGrupoMuscular`

## 🛣️ Routers y Endpoints

La carpeta `app/routers/` contiene todos los módulos de endpoints organizados por funcionalidad:

### `usuarios.py`

Gestiona las operaciones CRUD para usuarios:

- `POST /usuarios` - Crear un nuevo usuario
- `GET /usuarios` - Listar todos los usuarios
- `GET /usuarios/{usuario_id}` - Obtener un usuario específico
- `PATCH /usuarios/{usuario_id}` - Actualizar un usuario
- `DELETE /usuarios/{usuario_id}` - Eliminar un usuario

### `rutinas.py`

Gestiona rutinas de ejercicio:

- `POST /rutinas` - Crear una nueva rutina
- `POST /rutinas/{id_usuario}` - Crear una rutina asociada a un usuario
- `GET /rutinas` - Listar todas las rutinas
- `GET /usuarios/{id_usuario}/rutinas` - Listar rutinas de un usuario específico
- `PATCH /rutinas/{id_rutina}` - Actualizar una rutina
- `DELETE /usuarios/{usuario_id}/rutinas/{rutina_id}` - Eliminar una rutina de un usuario

**Endpoints relacionales:**
- `GET /rutinas/{id_rutina}/ejercicios` - Ver ejercicios de una rutina
- `GET /rutinas/{id_rutina}/grupo_muscular` - Ver grupos musculares de una rutina

### `ejercicios.py`

Gestiona ejercicios individuales:

- `POST /ejercicios` - Crear un nuevo ejercicio
- `GET /ejercicios` - Listar todos los ejercicios
- `GET /ejercicios/{ejercicio_id}` - Obtener un ejercicio específico
- `PATCH /ejercicios/{ejercicio_id}` - Actualizar un ejercicio
- `DELETE /ejercicio/{ejercicio_id}` - Eliminar un ejercicio

**Endpoints relacionales:**
- `GET /ejercicios/{id_ejercicio}/rutinas` - Ver rutinas que usan un ejercicio
- `GET /rutinas/grupo_muscular/{id_ejercicio}` - Ver grupos musculares trabajados por un ejercicio
- `GET /rutinas/equipoNecesario/{id_ejercicio}` - Ver equipo necesario para un ejercicio

### `equipo_necesario.py`

Gestiona el equipamiento necesario:

- `POST /equipoNecesario` - Crear un nuevo tipo de equipo
- `GET /equipoNecesario` - Listar todo el equipamiento
- `GET /equipoNecesario/{id_equipo_necesario}` - Obtener un equipo específico
- `PATCH /equipoNecesario/{id_equipo_necesario}` - Actualizar un equipo
- `DELETE /equipoNecesario/{id_equipo_necesario}` - Eliminar un equipo

**Endpoints relacionales:**
- `GET /EquipoNecesario/{id_equipo_necesario}` - Ver ejercicios que usan un equipo específico

### `grupos_musculares.py`

Gestiona los grupos musculares:

- `POST /grupo_muscular` - Crear un nuevo grupo muscular
- `GET /grupo_muscular` - Listar todos los grupos musculares
- `GET /grupo_muscular/{grupo_id}` - Obtener un grupo específico
- `PATCH /grupo_muscular/{grupo_id}` - Actualizar un grupo muscular
- `DELETE /grupo_muscular/{grupo_id}` - Eliminar un grupo muscular

**Endpoints relacionales:**
- `GET /grupo_muscular/{grupo_id}/ejercicios` - Ver ejercicios que trabajan un grupo muscular
- `GET /grupo_muscular/{grupo_id}/rutinas` - Ver rutinas enfocadas en un grupo muscular

### `nivel_dificultad.py`

Gestiona los niveles de dificultad:

- `POST /nivel_dificultad` - Crear un nuevo nivel
- `GET /nivel_dificultad` - Listar todos los niveles
- `GET /nivel_dificultad/{nivel_id}` - Obtener un nivel específico
- `PATCH /nivel_dificultad/{ejercicio_id}` - Actualizar un nivel
- `DELETE /nivel_dificultad/{nivel_id}` - Eliminar un nivel

### `tipo_trabajado.py`

Gestiona los tipos de trabajo muscular:

- `POST /tipo_trabajado` - Crear un nuevo tipo
- `GET /tipo_trabajado` - Listar todos los tipos
- `GET /tipo_trabajado/{id_tipo}` - Obtener un tipo específico
- `PATCH /tipo_trabajado/{id_tipo}` - Actualizar un tipo
- `DELETE /tipo_trabajado/{id_tipo}` - Eliminar un tipo

## 🔌 WebSockets y API de Gemini

### Implementación en `chat.py`

El módulo `chat.py` implementa un endpoint WebSocket que integra Google Gemini para proporcionar chat en tiempo real.

#### Configuración

```python
from google import genai

# Inicializa el cliente de Gemini con la API key desde variables de entorno
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
```

#### Endpoint WebSocket

**Ruta:** `ws/chat`

**Funcionamiento:**

1. **Aceptación de conexión:** El servidor acepta la conexión WebSocket del cliente
2. **Bucle de mensajes:** Mantiene la conexión abierta en un bucle infinito
3. **Recepción de mensajes:** Recibe mensajes de texto del cliente
4. **Procesamiento con Gemini:** Envía el mensaje a la API de Gemini usando el modelo `gemini-2.5-flash`
5. **Envío de respuesta:** Retorna la respuesta generada por Gemini al cliente
6. **Manejo de errores:** Captura excepciones y envía mensajes de error al cliente

**Ejemplo de uso desde el cliente:**

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onopen = () => {
  console.log('Conectado al chat');
  ws.send('Hola, ¿qué ejercicios recomiendas para principiantes?');
};

ws.onmessage = (event) => {
  console.log('Respuesta:', event.data);
};

ws.onerror = (error) => {
  console.error('Error:', error);
};
```

**Características:**

- **Tiempo real:** La comunicación es bidireccional e instantánea
- **Modelo:** Utiliza `gemini-2.5-flash` para respuestas rápidas
- **Manejo de errores:** Captura y reporta errores de forma amigable
- **Persistencia:** La conexión se mantiene abierta para múltiples intercambios

## 🗄️ Base de Datos

### PostgreSQL

El proyecto utiliza PostgreSQL 16 como base de datos relacional. Las tablas se crean automáticamente al iniciar la aplicación mediante SQLModel.

### Modelos Principales

- **Usuario:** Almacena información de usuarios del sistema
- **Rutina:** Rutinas de ejercicio personalizadas
- **Ejercicio:** Catálogo de ejercicios disponibles
- **Relaciones:** Tablas intermedias conectan usuarios, rutinas, ejercicios, grupos musculares y equipamiento

### Inicialización

Las tablas se crean automáticamente cuando la aplicación inicia gracias a la función `crearTablasDB` en `db.py`, que se ejecuta en el `lifespan` de FastAPI.

## 📚 Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a la documentación interactiva:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Estas interfaces permiten probar todos los endpoints directamente desde el navegador.

## 🤝 Contribución

Para nuevos colaboradores:

1. Clona el repositorio
2. Crea un archivo `.env` con las variables de entorno necesarias
3. Ejecuta el proyecto siguiendo las instrucciones anteriores
4. Revisa la documentación de los endpoints en `/docs`
5. Familiarízate con la estructura de modelos en `models.py`

## 📝 Notas Adicionales

- El proyecto está configurado para desarrollo con CORS abierto (permite cualquier origen)
- La base de datos se inicializa automáticamente al arrancar la aplicación
- Los WebSockets requieren una API Key válida de Google Gemini
- El proyecto utiliza SQLModel, que combina SQLAlchemy y Pydantic para validación y ORM
