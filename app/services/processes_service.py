from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from collections import defaultdict
from typing import List, Optional, Tuple
from app.schemas.processes import ProcessCreate, ProcessUpdate
from app.services.process_events_service import create_event
from app.models.users import User
from app.core.process_status import ProcessStatus
from app.models.processes import Process
from app.models.process_events import ProcessEvent
from app.core.process_event_types import ProcessEventType



def create_process(
    db: Session,
    data: ProcessCreate,
    current_user: User
) -> Process:
    try:
        process = Process(
            **data.model_dump(),
            creator_id=current_user.id
        )

        db.add(process)
        db.flush()  # obtiene ID sin commit

        create_event(
            db=db,
            process_id=process.id,
            action=ProcessEventType.PROCESS_CREATED,
            #event_type=ProcessEventType.PROCESS_CREATED,
            description="Proceso creado",
            old_value=None,
            new_value=None,
            created_by=current_user.id
        )

        db.commit()
        db.refresh(process)
        return process

    except Exception:
        db.rollback()
        raise



def get_process(db: Session, process_id: int) -> Optional[Process]:
    return db.query(Process).filter(Process.id == process_id).first()



def get_all_processes(
    db: Session,
    only_active: bool = True
) -> List[Process]:
    query = db.query(Process)
    if only_active:
        query = query.filter(Process.is_active == True)
    return query.all()



def update_process(
    db: Session,
    process: Process,
    data: ProcessUpdate,
    current_user: User
) -> Process:

    for field, new_value in data.model_dump(exclude_unset=True).items():
        old_value = getattr(process, field, None)

        if old_value != new_value:
            setattr(process, field, new_value)

            create_event(
                db=db,
                process_id=process.id,
                action=ProcessEventType.FIELD_UPDATED,
                description=f"Campo '{field}' actualizado",
                old_value=str(old_value),
                new_value=str(new_value),
                created_by=current_user.id
            )

    db.commit()
    db.refresh(process)
    return process



def soft_delete_process(db: Session, process: Process):
    process.is_active = False
    db.commit()



def delete_process(db: Session, process_id: int):
    process = get_process(db, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    db.delete(process)
    db.commit()
    return True



def get_process_timeline(
    db,
    process_id: int,
    skip: int = 0,
    limit: int = 50
):
    return (
        db.query(ProcessEvent)
        .filter(ProcessEvent.process_id == process_id)
        .order_by(ProcessEvent.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_process_timeline_paginated(
    db: Session,
    process_id: int,
    page: int = 1,
    limit: int = 20,
    order: str = "desc",
    action: Optional[str] = None
) -> Tuple[List[ProcessEvent], int]:

    query = db.query(ProcessEvent).filter(ProcessEvent.process_id == process_id)

    if action:
        query = query.filter(ProcessEvent.action == action)

    total = query.count()
    ordering = asc(ProcessEvent.created_at) if order == "asc" else desc(ProcessEvent.created_at)

    events = (
        query
        .order_by(ordering)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return events, total



def get_current_status(db: Session, process_id: int) -> ProcessStatus:
    last_event = (
        db.query(ProcessEvent)
        .filter(
            ProcessEvent.process_id == process_id,
            ProcessEvent.action == ProcessEventType.STATUS_CHANGED


    )
        .order_by(ProcessEvent.created_at.desc())
        .first()
    )

    if not last_event or not last_event.new_value:
        return ProcessStatus.CREATED

    try:
        return ProcessStatus(last_event.new_value)
    except ValueError:
        return ProcessStatus.CREATED


def get_process_metrics(db: Session, process_id: int):
    events = (
        db.query(ProcessEvent)
        .filter(
            ProcessEvent.process_id == process_id,
            ProcessEvent.action == ProcessEventType.STATUS_CHANGED
        )
        .order_by(ProcessEvent.created_at.asc())
        .all()
    )

    if not events:
        return {
            "total_duration_seconds": 0,
            "time_by_status": {}
        }

    time_by_status = defaultdict(int)

    for i in range(len(events) - 1):
        current = events[i]
        next_event = events[i + 1]

        delta = int(
            (next_event.created_at - current.created_at).total_seconds()
        )

        try:
            status = ProcessStatus(current.new_value)
            time_by_status[status] += delta
        except ValueError:
            continue

    total = sum(time_by_status.values())

    return {
        "total_duration_seconds": total,
        "time_by_status": dict(time_by_status)
    }




def change_process_status(
    db: Session,
    process: Process,
    new_status: ProcessStatus,
    current_user: User
) -> Process:

    old_status = process.status

    if old_status == new_status:
        return process

    process.status = new_status
    db.commit()
    db.refresh(process)


    create_event(
        db=db,
        process_id=process.id,
        action=ProcessEventType.STATUS_CHANGED,
        description=f"Estado cambiado de {old_status} a {new_status}",
        old_value=str(old_status),
        new_value=str(new_status),
        created_by=current_user.id
    )

    return process
