from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict
from datetime import datetime
from app.models.processes import Process
from app.models.process_events import ProcessEvent
from app.models.users import User

def get_process_status_metrics(db: Session, from_date: datetime | None, to_date: datetime | None) -> Dict[str, int]:
    query = db.query(Process.status, func.count(Process.id)).group_by(Process.status)
    if from_date:
        query = query.filter(Process.created_at >= from_date)
    if to_date:
        query = query.filter(Process.created_at <= to_date)
    return dict(query.all())

def get_event_type_metrics(db: Session, from_date: datetime | None, to_date: datetime | None) -> Dict[str, int]:
    query = db.query(ProcessEvent.action, func.count(ProcessEvent.id)).group_by(ProcessEvent.action)
    if from_date:
        query = query.filter(ProcessEvent.created_at >= from_date)
    if to_date:
        query = query.filter(ProcessEvent.created_at <= to_date)
    return dict(query.all())

def get_user_event_metrics(db: Session, from_date: datetime | None, to_date: datetime | None) -> Dict[str, int]:
    query = (
        db.query(User.name, func.count(ProcessEvent.id))
        .join(ProcessEvent, ProcessEvent.created_by == User.id)
        .group_by(User.name)
    )
    if from_date:
        query = query.filter(ProcessEvent.created_at >= from_date)
    if to_date:
        query = query.filter(ProcessEvent.created_at <= to_date)
    return dict(query.all())
