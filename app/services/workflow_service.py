from sqlalchemy.orm import Session
from app.models.workflow_steps import WorkflowStep


def get_workflow_steps(db: Session, workflow_id: int):

    steps = (
        db.query(WorkflowStep)
        .filter(WorkflowStep.workflow_id == workflow_id)
        .order_by(WorkflowStep.step_order)
        .all()
    )

    return steps


def validate_workflow_transition(
    db: Session,
    workflow_id: int,
    current_status: str,
    new_status: str
):

    steps = get_workflow_steps(db, workflow_id)

    step_names = [step.name for step in steps]

    if current_status not in step_names:
        raise ValueError(f"Current status not in workflow: {current_status}")

    if new_status not in step_names:
        raise ValueError(f"New status not in workflow: {new_status}")

    current_index = step_names.index(current_status)
    new_index = step_names.index(new_status)

    if new_index != current_index + 1:
        raise ValueError(
            f"Invalid workflow transition: {current_status} → {new_status}"
        )
