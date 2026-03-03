from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from app.core.process_event_types import ProcessEventType


class ProcessEvent(Base):
    __tablename__ = "process_events"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False)

    action = Column(Enum(ProcessEventType), nullable=False)
    description = Column(String(255), nullable=True)

    old_value = Column(String(255), nullable=True)
    new_value = Column(String(255), nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 RELACIONES
    process = relationship("Process", back_populates="events")
    user = relationship("User")
