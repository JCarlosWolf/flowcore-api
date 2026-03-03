from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi.encoders import jsonable_encoder
from app.models.process_events import ProcessEvent
from app.schemas.process_events import ProcessEventRead
from app.core.ws_manager import broadcast_queue
from app.core.metrics_cache import increment_user_event


def create_event(
    db: Session,
    process_id: int,
    action: str,
    description: str | None,
    old_value: str | None,
    new_value: str | None,
    created_by: int
) -> ProcessEvent:
    """
    Crea un evento de proceso, lo guarda en DB,
    actualiza métricas y lo envía por WebSocket (no bloqueante).
    """


    event = ProcessEvent(
        process_id=process_id,
        action=action,
        description=description,
        old_value=old_value,
        new_value=new_value,
        created_by=created_by
    )
    db.add(event)
    db.commit()
    db.refresh(event)


    increment_user_event(created_by)


    event_payload = jsonable_encoder(
        ProcessEventRead.model_validate(event)
    )


    event_payload["process_id"] = process_id


    broadcast_queue.put_nowait(event_payload)

    return event


def get_events_by_process(
    db: Session,
    process_id: int
) -> List[ProcessEvent]:

    return (
        db.query(ProcessEvent)
        .filter(ProcessEvent.process_id == process_id)
        .order_by(ProcessEvent.created_at.asc())
        .all()
    )


def get_process_timeline_paginated(
    db: Session,
    process_id: int,
    page: int,
    limit: int,
    order: str,
    action: str | None
) -> Tuple[List[ProcessEvent], int]:

    query = db.query(ProcessEvent).filter(
        ProcessEvent.process_id == process_id
    )

    if action:
        query = query.filter(ProcessEvent.action == action)

    total = query.count()

    ordering = asc(ProcessEvent.created_at) if order == "asc" else desc(ProcessEvent.created_at)

    events = (
        query.order_by(ordering)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return events, total
