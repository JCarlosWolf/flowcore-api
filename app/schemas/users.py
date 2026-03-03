
from pydantic import BaseModel, EmailStr, constr, ConfigDict
from typing import Optional
from datetime import datetime
from pydantic import validator


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role_id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: constr(min_length=1, max_length=50)
    email: EmailStr
    password: constr(min_length=8, max_length=72)

    @validator("password")
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v

    role_id: int


class UserUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=50)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6, max_length=72)] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    is_active: bool

    class Config:
        from_attributes = True
