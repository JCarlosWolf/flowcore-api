from pydantic import BaseModel
from app.core.process_status import ProcessStatus


class ProcessStatusUpdate(BaseModel):
    status: ProcessStatus
