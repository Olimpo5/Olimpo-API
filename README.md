# Olimpo API

## Inicia el proyecto

```bash
python3 -m venv env

source /env/bin/activate

pip -r requirements.txt
```

## Running the Application

You can run the application locally using the following `uvicorn` command. This is recommended for development and testing purposes.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Creacion del contendor de postgres

docker run -d \
  --name postgres_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=mi_basedatos \
  -p 5432:5432 \
  postgres:16
```

conectarse al contenedor en postgres docker exec -it postgres_olimpo psql -U postgres
