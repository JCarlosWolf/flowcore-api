from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import require_role
from app.core.roles import RoleEnum
from app.db.database import get_db
from app.models.roles import Role
from app.schemas.roles import RoleCreate, RoleUpdate, RoleResponse
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

# CREATE
@router.post("/", response_model=RoleResponse, dependencies=[Depends(require_role(RoleEnum.ADMIN))])

def create_role(
    data: RoleCreate,
    db: Session = Depends(get_db),

):
    existing = db.query(Role).filter(Role.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = Role(name=data.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


# READ ALL
@router.get("/", response_model=list[RoleResponse], dependencies=[Depends(require_role(RoleEnum.ADMIN))])

def list_roles(
    db: Session = Depends(get_db),


):
    return db.query(Role).all()


# READ ONE
@router.get("/{role_id}", response_model=RoleResponse, dependencies=[Depends(require_role(RoleEnum.ADMIN))])
def get_role(
    role_id: int,
    db: Session = Depends(get_db),

):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


# UPDATE
@router.put("/{role_id}", response_model=RoleResponse, dependencies=[Depends(require_role(RoleEnum.ADMIN))])
def update_role(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),

):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    role.name = data.name
    db.commit()
    db.refresh(role)
    return role


# DELETE
@router.delete("/{role_id}", dependencies=[Depends(require_role(RoleEnum.ADMIN))], status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(role)
    db.commit()
