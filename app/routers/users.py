from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.roles import RoleEnum
from app.db.database import get_db
from app.models.users import User
from app.models.roles import Role
from app.schemas.users import (
    UserCreate,
    UserUpdate,
    UserOut,
    UserResponse
)
from app.core.security import hash_password
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleEnum.ADMIN))]
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    hashed_pwd = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email.lower(),
        hashed_password=hashed_pwd,
        role_id=user.role_id,  # 🔥 ESTA LÍNEA FALTABA
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user



@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_role(RoleEnum.ADMIN))
):
    return db.query(User).all()



@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(RoleEnum.ADMIN))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user



@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(RoleEnum.ADMIN))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.hashed_password = hash_password(user_update.password)
    if user_update.role_id is not None:
        role = db.query(Role).filter(Role.id == user_update.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Rol inválido")
        user.role_id = user_update.role_id
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    db.commit()
    db.refresh(user)

    return user

@router.get("/", response_model=List[UserOut])
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),

):
    query = db.query(User).filter(User.is_active == True)

    users = query.offset((page - 1) * limit).limit(limit).all()
    return users


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),

):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.is_active = False
    db.commit()

    return {"message": "Usuario desactivado correctamente"}