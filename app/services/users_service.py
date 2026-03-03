from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email.lower(),
        hashed_password=hashed_pwd,
        role_id=user.role_id,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user



def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.processes:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete user with associated processes"
        )

    db.delete(user)
    db.commit()

    return {"detail": "User deleted"}
