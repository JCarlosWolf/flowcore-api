import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Settings:
    # =========================
    # DATABASE
    # =========================
    DB_USER: str = os.getenv("DB_USER", "flowcore_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "flowcore_pass")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5433")
    DB_NAME: str = os.getenv("DB_NAME", "flowcore")

    # =========================
    # JWT
    # =========================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_this_secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )

    # =========================
    # DATABASE URL
    # =========================
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Instancia global de configuración
settings = Settings()