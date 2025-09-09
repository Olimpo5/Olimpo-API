# Olimpo API

## Inicia el proyecto

```bash
python3 -m venv env

source /env/bin/activate

pip -r requirements.txt
```
    
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
