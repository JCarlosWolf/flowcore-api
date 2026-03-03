
from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel




class ProcessEventBase(BaseModel):
    event_type: str
    description: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None



class ProcessEventCreate(BaseModel):
    process_id: int
    description: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None



class ProcessEventRead(BaseModel):
    id: int
    action: str
    description: Optional[str]
    old_value: Optional[str]
    new_value: Optional[str]
    created_at: datetime
    created_by: Optional[int]

    class Config:
        from_attributes = True  # Pydantic V2


class ProcessEventQuery(BaseModel):
    page: int = 1
    limit: int = 20
    order: Literal["asc", "desc"] = "desc"
    action: Optional[str] = None
