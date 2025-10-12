from sqlalchemy import create_engine, text  # <-- importar text

DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/OlimpoDB"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.scalar()
        print("Conectado a:", version)
except Exception as e:
    print("Error al conectar:", e)
