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
