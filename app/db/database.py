from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Crear el motor de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
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