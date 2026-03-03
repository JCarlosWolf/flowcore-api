from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.db.database import get_db
from app.schemas.metrics import MetricsResponse
from app.services import metrics_service

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

@router.get("/", response_model=MetricsResponse)
def get_metrics(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db: Session = Depends(get_db),

):
    """
    Devuelve métricas de procesos y eventos.
    Opcionalmente filtra por rango de fechas.
    """
    processes_by_status = metrics_service.get_process_status_metrics(db, from_date, to_date)
    events_by_type = metrics_service.get_event_type_metrics(db, from_date, to_date)
    events_by_user = metrics_service.get_user_event_metrics(db, from_date, to_date)

    return MetricsResponse(
        processes_by_status={"status_counts": processes_by_status},
        events_by_type={"event_counts": events_by_type},
        events_by_user={"user_counts": events_by_user}
    )
