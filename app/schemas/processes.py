from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.schemas.process_events import ProcessEventRead
from app.core.process_status import ProcessStatus


class ProcessBase(BaseModel):
    name: str
    description: Optional[str] = None
    client_id: int
    template_id: int


class ProcessCreate(ProcessBase):
    pass


class ProcessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProcessStatus] = None


class ProcessRead(ProcessBase):
    id: int
    status: ProcessStatus
    created_at: datetime

    class Config:
        from_attributes = True


class ProcessTimeline(BaseModel):
    events: List[ProcessEventRead]
    total: int


# Alias para compatibilidad con imports antiguos
ProcessReadWithEvents = ProcessTimeline


class ProcessMetrics(BaseModel):
    total_duration_seconds: int
    time_by_status: Dict[ProcessStatus, int]


class ProcessStatusRead(BaseModel):
    process_id: int
    current_status: ProcessStatus
    metrics: ProcessMetrics


class ProcessOut(BaseModel):
    id: int
    name: str
    client_id: int
    creator_id: int
    template_id: Optional[int]

    class Config:
        from_attributes = True