from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.dependencies import get_current_user_from_ws
from app.core.ws_manager import process_connections, metrics_connections
from app.models.users import User

router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/process/{process_id}")
async def process_ws(
    websocket: WebSocket,
    process_id: int,

):
    await websocket.accept()

    if process_id not in process_connections:
        process_connections[process_id] = []

    process_connections[process_id].append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        process_connections[process_id].remove(websocket)


@router.websocket("/metrics")
async def metrics_ws(
    websocket: WebSocket,

):
    await websocket.accept()
    metrics_connections.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        metrics_connections.remove(websocket)
