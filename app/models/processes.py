from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base
from app.core.process_status import ProcessStatus


class Process(Base):

    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    description = Column(String(255), nullable=True)

    status = Column(
        Enum(ProcessStatus),
        default=ProcessStatus.CREATED,
        nullable=False
    )

    is_active = Column(Boolean, default=True, nullable=False)



    creator_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False
    )

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id"),
        nullable=True
    )

    template_id = Column(
        Integer,
        ForeignKey("process_templates.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



    creator = relationship(
        "User",
        back_populates="processes"
    )

    client = relationship(
        "Client",
        back_populates="processes"
    )

    workflow = relationship(
        "Workflow"
    )

    template = relationship(
        "ProcessTemplate",
        back_populates="processes"
    )

    events = relationship(
        "ProcessEvent",
        back_populates="process",
        cascade="all, delete-orphan",
        order_by="ProcessEvent.created_at"
    )