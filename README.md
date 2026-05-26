# FlowCore API: Workflow Management & Business Process Automation Engine (BPM)

**Developed by:** José Carlos Lobo  
**Main Stack:** Python | FastAPI | PostgreSQL | Docker | WebSockets  

---

## Language / Idioma

- [English Version](#english)
- [Versión en Español](#espanol)

---

<a id="english"></a>

# English Version

## 🎯 Executive Summary & Business Value

In any organization, especially within highly regulated sectors like **banking and finance**, operational friction is a major source of hidden costs and compliance risks. Manual workflows, lack of approval visibility, and lost documentation lead to severe inefficiencies during critical processes like client onboarding, risk validation, or credit approvals.

**FlowCore** is a production-style backend system engineered to solve this organizational pain. It functions as a robust **Workflow Engine** that empowers businesses to define structured process templates, enforce strict conditional step sequences, assign role-based compliance permissions, and build a pixel-perfect audit log of every single corporate movement.

---

## 🏢 Real-World Corporate Use Cases

- **Automated Client Onboarding (KYC):** Managing everything from data collection and background screening to final account activation.
- **Risk Assessment & Approval Pipelines:** Enforcing workflows where junior analysts initiate scoring, managers evaluate risk, and administrators authorize payouts.
- **Regulatory Compliance & Internal Audit:** Keeping an immutable record of who approved or rejected a specific business step, when, and why.

---

## 🚀 Key Features & Enterprise Value

- **Role-Based Access Control (RBAC):** Restricts critical operations based on corporate hierarchy (Admin, Manager, User), mirroring rigorous banking security frameworks.
- **Configurable Workflow Engine:** Business processes are dynamic and fully adaptable to custom logical sequences (`created` ➔ `document_validation` ➔ `risk_assessment` ➔ `approved`).
- **Event Timeline (Zero-Error Audit Log):** Every state transition, data modification, or human intervention generates an immutable event—providing a bulletproof log for regulatory audits.
- **Real-Time Operational Metrics:** System aggregates data on the fly (processes by status, events by user/type), allowing executives to pinpoint operational bottlenecks instantly via WebSockets.

---

## 🛠️ Architecture & Backend Best Practices

Built according to modern software engineering standards to guarantee high availability, scalability, and long-term maintainability:

- **Clean Layered Architecture:** Strict separation between input logic (API Routers), core business logic (Service Layer/Workflow Engine), and data persistence (PostgreSQL).
- **Financial-Grade Security:** Secure authentication and authorization powered by JWT tokens.
- **Professional Infrastructure:** Fully containerized with Docker for identical development and production environments, featuring database versioning via Alembic migrations.

```text
Client ➔ [ FastAPI Routers ] ➔ [ Service Layer ] ➔ [ Workflow Engine ] ➔ [ PostgreSQL Database ]
📋 Quick Start Guide (Developers)
Prerequisites
Python 3.10+
Docker and Docker Compose
1. Environment Setup
git clone https://github.com/JCarlosWolf/flowcore-api.git
cd flowcore-api

python -m venv .venv

Activate virtual environment:

Windows

.venv\Scripts\activate

Linux/macOS

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
2. Configuration (.env)

Create a .env file in the root directory:

DB_HOST=localhost
DB_PORT=5432
DB_USER=flowcore_user
DB_PASSWORD=flowcore_pass
DB_NAME=flowcore

SECRET_KEY=super_secret_banking_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
3. Run Database & Migrations
# Start PostgreSQL via Docker
docker compose up -d

# Run database migrations
alembic upgrade head

# Seed demo data
python scripts/demo_seed.py
python scripts/seed_roles_users.py
4. Launch the API
uvicorn app.main:app --reload

Interactive API Documentation (Swagger UI):

http://localhost:8000/docs
📊 Core API Endpoints
POST /auth/login → User authentication and token issuance
POST /clients → Client onboarding and registration
POST /processes → Create new workflow instances
POST /processes/{id}/status → Controlled workflow transitions
GET /processes/{id}/timeline → Full audit history
GET /metrics → Operational KPIs & metrics
✉️ Contact & Process Consulting

If your business is wasting hours on manual tracking, lacks visibility into its internal operations, or requires a secure backend to enforce complex business logic:

Developer: José Carlos Lobo

Specialty: Backend Automation & Business Process Optimization

LinkedIn:
https://www.linkedin.com/in/josé-carlos-lobo-473b458a

<a id="espanol"></a>

Version Espanol
🎯 ¿Qué es FlowCore? (Perspectiva de Negocio)

En cualquier organización, especialmente en sectores altamente regulados como el financiero o el bancario, los mayores costes y errores no nacen de la falta de herramientas, sino de la fricción operativa: procesos manuales desordenados, falta de claridad en las aprobaciones, pérdida de documentos y la incapacidad de saber en tiempo real en qué fase se encuentra un expediente.

FlowCore es un sistema backend robusto diseñado específicamente para solucionar este dolor. Es un Motor de Flujos de Trabajo (Workflow Engine) que permite a las empresas definir plantillas de procesos, encadenar pasos lógicos obligatorios, asignar roles de cumplimiento y auditar de forma milimétrica cada acción que ocurre en la empresa.

🏢 Casos de Uso Reales en la Empresa
Onboarding Automatizado de Clientes (KYC)
Pipelines de Aprobación de Riesgos
Auditoría Interna y Cumplimiento Normativo
🚀 Características Clave y Valor Empresarial
Gobernanza y Control de Accesos (RBAC)
Motor de Flujos Configurable
Línea de Tiempo de Eventos (Auditoría)
Métricas Operativas en Tiempo Real
🛠️ Arquitectura Técnica y Buenas Prácticas
Arquitectura Limpia en Capas
Seguridad con JWT
Docker + Alembic
PostgreSQL + FastAPI
✉️ Contacto y Consultoría de Procesos

Desarrollador: José Carlos Lobo

LinkedIn:
https://www.linkedin.com/in/josé-carlos-lobo-473b458a
