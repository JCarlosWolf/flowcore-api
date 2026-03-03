from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.clients import Client
from app.schemas.clients import ClientCreate, ClientUpdate, ClientRead
from app.core.dependencies import require_role

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.post(
    "/",
    response_model=ClientRead,
    dependencies=[Depends(require_role("ADMIN"))]
)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    new_client = Client(**client.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client



@router.get(
    "/",
    response_model=List[ClientRead],
    dependencies=[Depends(require_role("ADMIN"))]
)
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()



@router.get(
    "/{client_id}",
    response_model=ClientRead,
    dependencies=[Depends(require_role("ADMIN"))]
)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client



@router.put(
    "/{client_id}",
    response_model=ClientRead,
    dependencies=[Depends(require_role("ADMIN"))]
)
def update_client(
    client_id: int,
    data: ClientUpdate,
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client



@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role("ADMIN"))]
)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
