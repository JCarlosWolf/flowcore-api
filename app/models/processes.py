from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Process(Base):
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), default="created")
    is_active = Column(Boolean, default=True, nullable=False)

    # 🔑 Foreign Keys
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 RELACIONES
    creator = relationship(
        "User",
        back_populates="processes"
    )

    client = relationship(
        "Client",
        back_populates="processes"
    )

    events = relationship(
        "ProcessEvent",
        back_populates="process",
        cascade="all, delete-orphan",
        order_by="ProcessEvent.created_at"
    )
