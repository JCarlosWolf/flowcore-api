from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.processes import Process
from app.models.process_events import ProcessEvent
from app.models.users import User
from app.core.roles import RoleEnum
from app.core.dependencies import require_role

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(RoleEnum.ADMIN))  # Solo Admin ve el dashboard
):
    # Total de procesos
    total_processes = db.query(Process).count()

    # Total por estado
    total_by_status = {
        status: db.query(Process).filter(Process.status == status).count()
        for status in ["CREATED", "IN_PROGRESS", "COMPLETED"]
    }

    # Procesos activos pero no completados (vencidos o en progreso)
    active_unfinished = db.query(Process).filter(Process.is_active==True, Process.status!="COMPLETED").count()

    # Eventos por usuario
    events_per_user = (
        db.query(User.name, func.count(ProcessEvent.id))
        .join(ProcessEvent, ProcessEvent.created_by == User.id)
        .group_by(User.name)
        .all()
    )

    return {
        "total_processes": total_processes,
        "total_by_status": total_by_status,
        "active_unfinished_processes": active_unfinished,
        "events_per_user": dict(events_per_user)
    }
