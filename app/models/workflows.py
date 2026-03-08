from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class Workflow(Base):

    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    is_active = Column(Boolean, default=True)

    steps = relationship(
        "WorkflowStep",
        back_populates="workflow",
        cascade="all, delete-orphan",
        order_by="WorkflowStep.step_order"
    )