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


@router.get("/{process_id}/timeline", response_model=ProcessTimeline)
def get_process_timeline(
    process_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    action: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    events, total = processes_service.get_process_timeline_paginated(
        db=db,
        process_id=process_id,
        page=page,
        limit=limit,
        order=order,
        action=action
    )

    if not events:
        raise HTTPException(status_code=404, detail="No events found for this process")

    # 🔹 Convertimos cada evento ORM -> Pydantic V2
    events_pydantic = [
        ProcessEventRead.model_validate({
            "id": e.id,
            "action": str(e.action),  # enum -> str
            "description": e.description,
            "old_value": e.old_value,
            "new_value": e.new_value,
            "created_at": e.created_at,
            "created_by": e.created_by
        })
        for e in events
    ]

    return ProcessTimeline(events=events_pydantic, total=total)