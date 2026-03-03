from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class MetricsQuery(BaseModel):
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None

class ProcessStatusMetrics(BaseModel):
    status_counts: Dict[str, int]  # {"created": 10, "completed": 5}

class EventTypeMetrics(BaseModel):
    event_counts: Dict[str, int]   # {"PROCESS_CREATED": 10, "STATUS_CHANGE": 5}

class UserEventMetrics(BaseModel):
    user_counts: Dict[str, int]    # {"Admin": 12, "Juan Perez": 3}

class MetricsResponse(BaseModel):
    processes_by_status: ProcessStatusMetrics
    events_by_type: EventTypeMetrics
    events_by_user: UserEventMetrics
