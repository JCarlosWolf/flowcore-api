# FlowCore API

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Python](https://img.shields.io/badge/Python-3.11-yellow)

FlowCore is a backend system for managing business processes using configurable workflows, process templates and event tracking.

This project demonstrates a production-style backend architecture built with **FastAPI, PostgreSQL, SQLAlchemy and WebSockets**.

It was developed as a **backend portfolio project** to showcase workflow engines, event systems, real-time updates and scalable API design.

---

# Features

- JWT Authentication
- Role-based access control (Admin / Manager / User)
- Workflow engine with configurable steps
- Process templates
- Process lifecycle management
- Event timeline (audit log)
- Real-time updates via WebSockets
- Metrics aggregation API
- PostgreSQL database
- Alembic migrations
- Clean layered architecture

---

# Architecture

The API follows a layered architecture separating API logic, business logic and persistence.


Client
↓
FastAPI Routers
↓
Service Layer
↓
Workflow Engine
↓
PostgreSQL


### Project Structure


app
├ core # configuration, security, enums
├ db # database connection
├ models # SQLAlchemy ORM models
├ routers # API endpoints
├ schemas # Pydantic validation schemas
├ services # business logic
└ scripts # demo seed scripts

alembic # database migrations
tests # API tests


---

# Domain Model

The system models business workflows using the following entities:


ProcessTemplate
│
▼
Workflow
│
▼
WorkflowSteps
│
▼
Process
│
▼
ProcessEvents


### Process

Represents an instance of a business workflow.

Examples:

- client onboarding
- verification processes
- approval pipelines

---

### Workflow

Defines the ordered sequence of steps a process must follow.

Example:


created → document_validation → risk_assessment → approved


---

### Process Events

Every important change generates an event:

- process created
- field updated
- status changed

These events create a **timeline (audit log)** for each process.

---

# Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- WebSockets
- Pydantic
- JWT Authentication
- Docker

---

# Installation

## Clone repository


git clone https://github.com/JCarlosWolf/flowcore-api.git

cd flowcore-api


## Create virtual environment


python -m venv .venv


## Activate environment

Windows


.venv\Scripts\activate


Linux / macOS


source .venv/bin/activate


## Install dependencies


pip install -r requirements.txt


---

# Environment Variables

Create a `.env` file in the project root:


DB_HOST=localhost
DB_PORT=5432
DB_USER=flowcore_user
DB_PASSWORD=flowcore_pass
DB_NAME=flowcore

SECRET_KEY=super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


---

# Run Database

Using Docker:


docker compose up -d


---

# Run Migrations


alembic upgrade head


---

# Seed Demo Data


python scripts/demo_seed.py
python scripts/seed_roles_users.py


This creates:

- demo workflow
- process template
- demo client
- admin user

---

# Run API


uvicorn app.main:app --reload


Swagger documentation:


http://localhost:8000/docs


---

# Example API Flow

### Login


POST /auth/login


### Create client


POST /clients


### Create process


POST /processes


### Change process status


POST /processes/{id}/status


### View timeline


GET /processes/{id}/timeline


---

# Metrics API

The system aggregates workflow metrics.


GET /metrics


Returns:

- processes by status
- events by type
- events by user

---

# WebSockets

Real-time updates are available through WebSocket channels.

### Process timeline updates


ws://localhost:8000/ws/process/{process_id}


### Metrics updates


ws://localhost:8000/ws/metrics


---

# Testing

Run tests with:


pytest


---

# Author

Backend portfolio project demonstrating a workflow-based process management a
