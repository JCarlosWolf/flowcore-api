from enum import Enum

class ProcessStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
