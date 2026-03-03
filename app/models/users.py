from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 Relaciones
    processes = relationship(
        "Process",
        back_populates="creator"
    )

    role = relationship(
        "Role",
        back_populates="users"
    )
    events = relationship(
        "ProcessEvent",
        back_populates="user",
        cascade="all, delete-orphan"
    )


