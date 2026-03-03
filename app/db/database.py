import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables de entorno desde .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construir la URL de conexión a MySQL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Crear fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Clase base para los modelos
Base = declarative_base()


# Dependencia para FastAPI
def get_db():
    """
    Abre una sesión de base de datos por petición
    y la cierra siempre al final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



