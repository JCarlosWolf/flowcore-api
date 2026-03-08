from fastapi import FastAPI, HTTPException, Request
from app.routers import (auth, users, roles,
                         clients, processes, process_events,
                         metrics, ws, dashboard)
from app.core.ws_manager import broadcast_worker
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import asyncio

app = FastAPI(title="Process Manager API")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(clients.router)
app.include_router(processes.router)
app.include_router(process_events.router)
app.include_router(metrics.router)
app.include_router(ws.router)
app.include_router(dashboard.router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_worker())

# Manejo de errores HTTP
app.add_exception_handler(HTTPException, http_exception_handler)

# Manejo de errores genéricos
app.add_exception_handler(Exception, generic_exception_handler)

@app.get("/health")
def health_check():
    return {"status": "ok"}