from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.db.database import get_db
from app.models.users import User
from app.core.security import SECRET_KEY, ALGORITHM
from app.core.oauth2 import oauth2_scheme
from fastapi import WebSocket, WebSocketException
from app.core.jwt import decode_access_token
from sqlalchemy.orm import Session

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        raise credentials_exception

    return user


def require_role(*allowed_roles: str):
    """
    Uso:
    - require_role("ADMIN")
    - require_role("ADMIN", "MANAGER")
    """

    def role_checker(user: User = Depends(get_current_user)):
        if user.role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role assigned"
            )
        allowed = [r.value if hasattr(r, "value")
                   else r for r in allowed_roles]
        #if user.role.name not in allowed_roles:
        if user.role.name not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return user

    return role_checker


async def get_current_user_from_ws(websocket: WebSocket) -> User:
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        raise WebSocketException(code=1008, reason="JWT required")

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    except Exception:
        await websocket.close(code=1008)
        raise WebSocketException(code=1008, reason="Invalid token")

    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await websocket.close(code=1008)
        raise WebSocketException(code=1008, reason="User not found")

    return user