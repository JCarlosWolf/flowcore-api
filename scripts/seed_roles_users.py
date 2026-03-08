from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from passlib.context import CryptContext
from app.models.users import User
from app.models.roles import Role

# Configurar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_roles_and_admin():
    db: Session = SessionLocal()
    try:
        # Crear roles si no existen
        roles = ["admin", "user"]
        for role_name in roles:
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                role = Role(name=role_name)
                db.add(role)
        db.commit()

        # Obtener el role_id de admin
        admin_role = db.query(Role).filter(Role.name == "admin").first()

        # Crear usuario admin si no existe
        admin_email = "admin@example.com"
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            hashed_password = pwd_context.hash("12345678")  # Cambia contraseña si quieres
            admin_user = User(
                name="Admin",
                email=admin_email,
                hashed_password=hashed_password,
                is_active=True,
                role_id=admin_role.id,
                created_at=datetime.utcnow()
            )
            db.add(admin_user)
            db.commit()

        print("Roles y usuario admin creados correctamente ✅")

    except Exception as e:
        db.rollback()
        print("Error:", e)
    finally:
        db.close()

if __name__ == "__main__":
    create_roles_and_admin()
