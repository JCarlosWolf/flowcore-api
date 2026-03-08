from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class WorkflowStep(Base):

    __tablename__ = "workflow_steps"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id"),
        nullable=False
    )

    name = Column(String(100), nullable=False)

    step_order = Column(Integer, nullable=False)

    workflow = relationship(
        "Workflow",
        back_populates="steps"
    )