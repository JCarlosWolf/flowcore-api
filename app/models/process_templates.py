from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class ProcessTemplate(Base):

    __tablename__ = "process_templates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    description = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id"),
        nullable=False
    )

    workflow = relationship("Workflow")

    processes = relationship(
        "Process",
        back_populates="template"
    )