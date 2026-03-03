import asyncio
from typing import Dict, List
from fastapi import WebSocket
from asyncio import Queue

# Conexiones
process_connections: Dict[int, List[WebSocket]] = {}
metrics_connections: List[WebSocket] = []

# Cola de broadcast
broadcast_queue: Queue = Queue()


async def broadcast_worker():
    while True:
        event_data = await broadcast_queue.get()
        await _broadcast(event_data)
        broadcast_queue.task_done()


async def _broadcast(payload: dict):
    process_id = payload.get("process_id")

    # Timeline por proceso
    if process_id in process_connections:
        websockets = process_connections[process_id]
        await asyncio.gather(
            *[ws.send_json(payload) for ws in websockets if ws.client_state.name == "CONNECTED"],
            return_exceptions=True
        )

    # Canal global métricas
    if metrics_connections:
        await asyncio.gather(
            *[ws.send_json({"metrics_update": True}) for ws in metrics_connections],
            return_exceptions=True
        )
