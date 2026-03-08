from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.process_event_types import ProcessEventType
from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.process_events import (
    ProcessEventCreate,
    ProcessEventRead
)
from app.schemas.processes import ProcessTimeline
from app.services import process_events_service, processes_service
from app.services.process_events_service import create_event


router = APIRouter(
    prefix="/process-events",
    tags=["Process Events"]
)


@router.get(
    "/process/{process_id}",
    response_model=List[ProcessEventRead]
)
def list_events_by_process(
    process_id: int,
    db: Session = Depends(get_db),

):
    return process_events_service.get_events_by_process(db, process_id)


@router.post("/", response_model=ProcessEventRead, status_code=201)
def create_process_event(
    event: ProcessEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_event(
        db=db,
        process_id=event.process_id,
        action=ProcessEventType.FIELD_UPDATED,
        description=event.description,
        old_value=event.old_value,
        new_value=event.new_value,
        created_by = current_user.id

    )


class TimelinePaginated(BaseModel):
    total: int
    page: int
    limit: int
    events: list[ProcessEventRead]


