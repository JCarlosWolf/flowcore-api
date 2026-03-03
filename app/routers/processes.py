from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.core.roles import RoleEnum
from app.models.users import User
from app.schemas.process_events import ProcessEventRead
from app.schemas.processes import (
    ProcessCreate,
    ProcessUpdate,
    ProcessRead,
    ProcessTimeline,
    ProcessStatusRead,
    ProcessOut
)
from app.services import processes_service
from app.schemas.process_status import ProcessStatusUpdate


router = APIRouter(
    prefix="/processes",
    tags=["Processes"]
)

@router.get("/ping")
def ping():
    return {"ok": True}

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

    # 🔹 Convertimos cada evento ORM → Pydantic V2
    events_pydantic = [
        ProcessEventRead.model_validate({
            "id": e.id,
            "action": str(e.action),
            "description": e.description,
            "old_value": e.old_value,
            "new_value": e.new_value,
            "created_at": e.created_at,
            "created_by": e.created_by
        })
        for e in events
    ]

    return ProcessTimeline(events=events_pydantic, total=total)

@router.get("/{process_id}/status", response_model=ProcessStatusRead)
def get_process_status(
    process_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    process = processes_service.get_process(db, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    current_status = processes_service.get_current_status(db, process_id)
    metrics = processes_service.get_process_metrics(db, process_id)
    return {
        "process_id": process_id,
        "current_status": current_status,
        "metrics": metrics
    }


@router.get("/", response_model=List[ProcessOut])
def list_processes(
    db: Session = Depends(get_db),
    ):
    return processes_service.get_all_processes(db, only_active=True)


@router.post("/", response_model=ProcessRead, status_code=status.HTTP_201_CREATED)
def create_process(
    process: ProcessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN))
):
    return processes_service.create_process(db, process, current_user)

@router.get("/{process_id}", response_model=ProcessRead)
def get_process(
    process_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    process = processes_service.get_process(db, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    return process

@router.put("/{process_id}", response_model=ProcessRead)
def update_process(
    process_id: int,
    process_update: ProcessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN))
):
    process = processes_service.get_process(db, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    return processes_service.update_process(db, process, process_update, current_user)

@router.delete("/{process_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process(
    process_id: int,
    db: Session = Depends(get_db),

):
    processes_service.delete_process(db, process_id)




@router.post(
    "/{process_id}/status",
    response_model=ProcessRead
)
def update_process_status(
    process_id: int,
    data: ProcessStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    process = processes_service.get_process(db, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    return processes_service.change_process_status(
        db=db,
        process=process,
        new_status=data.status,
        current_user=current_user
    )

