from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.workflows import Workflow
from app.models.workflow_steps import WorkflowStep
from app.models.process_templates import ProcessTemplate
from app.models.clients import Client


def seed_workflow(db: Session):

    workflow = Workflow(
        name="Client Onboarding"
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    steps = [
        "created",
        "document_validation",
        "risk_assessment",
        "approved"
    ]

    for i, step in enumerate(steps):

        db.add(
            WorkflowStep(
                workflow_id=workflow.id,
                name=step,
                step_order=i + 1
            )
        )

    db.commit()

    return workflow


def seed_template(db: Session, workflow_id: int):

    template = ProcessTemplate(
        name="Client Onboarding Template",
        description="Standard onboarding workflow",
        workflow_id=workflow_id
    )

    db.add(template)
    db.commit()

    return template


def seed_client(db: Session):

    client = Client(
        name="Demo Company",
        email="demo@company.com",
        phone="123456789"
    )

    db.add(client)
    db.commit()

    return client


def run():

    db = SessionLocal()

    workflow = seed_workflow(db)

    seed_template(db, workflow.id)

    seed_client(db)

    print("Demo data created successfully 🚀")


if __name__ == "__main__":
    run()