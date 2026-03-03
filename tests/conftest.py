import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import (get_db)
from app.core import ws_manager
from app.models import User, Role
from sqlalchemy.orm import Session

# =========================
# Deshabilitar worker WS
# =========================
@pytest.fixture(autouse=True, scope="session")
def disable_ws_worker(monkeypatch):
    monkeypatch.setattr(ws_manager, "broadcast_worker", lambda: None)

# =========================
# Fixture DB Session
# =========================
@pytest.fixture()
def db_session():
    from app.db.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# Fixture Client
# =========================
@pytest.fixture()
def client(db_session: Session):
    # Sobrescribe get_db para usar DB de test
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

# =========================
# Fixture admin token
# =========================
@pytest.fixture()
def admin_token(db_session: Session):
    # Crear rol admin si no existe
    role = db_session.query(Role).filter_by(name="admin").first()
    if not role:
        role = Role(name="admin")
        db_session.add(role)
        db_session.commit()
        db_session.refresh(role)

    # Crear usuario admin si no existe
    user = db_session.query(User).filter_by(email="admin@test.com").first()
    if not user:
        user = User(name="Admin", email="admin@test.com", password="12345678", role_id=role.id)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    # Aquí asumimos que tienes función create_access_token(user)
    from app.core.security import create_access_token
    token = create_access_token({"sub": str(user.id)})
    return f"Bearer {token}"
