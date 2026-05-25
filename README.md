# FlowCore API: Workflow Management & Business Process Automation Engine (BPM)

**Developed by:** José Carlos Lobo  
**Main Stack:** Python | FastAPI | PostgreSQL | Docker | WebSockets  

---

## 🌍 Language / Idioma

* For the technical documentation in English, please scroll down or click here: 👉 **[English Version](#english-version)**
* Para leer el caso de estudio de negocio adaptado a empresas en español, haz clic aquí: 👉 **[Versión en Español](#version-espanol)**

---

<a name="english-version"></a>
# English Version: Technical & Architectural Overview

## 🎯 Executive Summary & Business Value

In any organization, especially within highly regulated sectors like **banking and finance**, operational friction is a major source of hidden costs and compliance risks. Manual workflows, lack of approval visibility, and lost documentation lead to severe inefficiencies during critical processes like client onboarding, risk validation, or credit approvals.

**FlowCore** is a production-style backend system engineered to solve this organizational pain. It functions as a robust **Workflow Engine** that empowers businesses to define structured process templates, enforce strict conditional step sequences, assign role-based compliance permissions, and build a pixel-perfect audit log of every single corporate movement.

### 🏢 Real-World Corporate Use Cases:
* **Automated Client Onboarding (KYC):** Managing everything from data collection and background screening to final account activation.
* **Risk Assessment & Approval Pipelines:** Enforcing workflows where junior analysts initiate scoring, managers evaluate risk, and administrators authorize payouts.
* **Regulatory Compliance & Internal Audit:** Keeping an immutable record of who approved or rejected a specific business step, when, and why.

---

## 🚀 Key Features & Enterprise Value

* **Role-Based Access Control (RBAC):** Restricts critical operations based on corporate hierarchy (Admin, Manager, User), mirroring rigorous banking security frameworks.
* **Configurable Workflow Engine:** Business processes are dynamic and fully adaptable to custom logical sequences (`created` ➔ `document_validation` ➔ `risk_assessment` ➔ `approved`).
* **Event Timeline (Zero-Error Audit Log):** Every state transition, data modification, or human intervention generates an immutable event—providing a bulletproof log for regulatory audits.
* **Real-Time Operational Metrics:** System aggregates data on the fly (processes by status, events by user/type), allowing executives to pinpoint operational bottlenecks instantly via *WebSockets*.

---

## 🛠️ Architecture & Backend Best Practices

Built according to modern software engineering standards to guarantee high availability, scalability, and long-term maintainability:

* **Clean Layered Architecture:** Strict separation between input logic (API Routers), core business logic (Service Layer/Workflow Engine), and data persistence (PostgreSQL).
* **Financial-Grade Security:** Secure authentication and authorization powered by JWT tokens.
* **Professional Infrastructure:** Fully containerized with **Docker** for identical development and production environments, featuring database versioning via **Alembic** migrations.

Client ➔ [ FastAPI Routers ] ➔ [ Service Layer ] ➔ [ Workflow Engine ] ➔ [ PostgreSQL Database ]


---

## 📋 Quick Start Guide (Developers)

### Prerequisites
* Python 3.10+
* Docker and Docker Compose

### 1. Environment Setup
```bash
git clone [https://github.com/JCarlosWolf/flowcore-api.git](https://github.com/JCarlosWolf/flowcore-api.git)
cd flowcore-api
python -m venv .venv
Activate virtual environment:

Windows: .venv\Scripts\activate

Linux/macOS: source .venv/bin/activate

Bash
pip install -r requirements.txt
2. Configuration (.env)
Create a .env file in the root directory:

Fragmento de código
DB_HOST=localhost
DB_PORT=5432
DB_USER=flowcore_user
DB_PASSWORD=flowcore_pass
DB_NAME=flowcore
SECRET_KEY=super_secret_banking_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
3. Run Database & Migrations
Bash
# Start PostgreSQL via Docker
docker compose up -d

# Run database migrations
alembic upgrade head

# Seed demo data (Roles, users, and a workflow sample)
python scripts/demo_seed.py
python scripts/seed_roles_users.py
4. Launch the API
Bash
uvicorn app.main:app --reload
Interactive API Documentation (Swagger UI): http://localhost:8000/docs

📊 Core API Endpoints
POST /auth/login - User authentication and token issuance.

POST /clients - Client onboarding and registration.

POST /processes - Instantiating a new workflow instance based on templates.

POST /processes/{id}/status - Controlled and validated workflow state transitions.

GET /processes/{id}/timeline - Fetching the comprehensive audit log for a process.

GET /metrics - Operational dashboard (KPI aggregation).

✉️ Contact & Process Consulting
If your business is wasting hours on manual tracking, lacks visibility into its internal operations, or requires a secure backend to enforce complex business logic:

Developer: José Carlos Lobo

Specialty: Backend Automation & Business Process Optimization (Ex-Banking Professional with 35+ years of operational business experience).

LinkedIn: www.linkedin.com/in/josé-carlos-lobo-473b458a

Versión en Español: Caso de Estudio de Negocio
🎯 ¿Qué es FlowCore? (Perspectiva de Negocio)
En cualquier organización, especialmente en sectores altamente regulados como el financiero o el bancario, los mayores costes y errores no nacen de la falta de herramientas, sino de la fricción operativa: procesos manuales desordenados, falta de claridad en las aprobaciones, pérdida de documentos y la incapacidad de saber en tiempo real en qué fase se encuentra un expediente (ej. el onboarding de un cliente, la validación de un riesgo o la aprobación de un crédito).

FlowCore es un sistema backend robusto diseñado específicamente para solucionar este dolor. Es un Motor de Flujos de Trabajo (Workflow Engine) que permite a las empresas definir plantillas de procesos, encadenar pasos lógicos obligatorios, asignar roles de cumplimiento y auditar de forma milimétrica cada acción que ocurre en la empresa.

🏢 Casos de Uso Reales en la Empresa:
Onboarding Automatizado de Clientes (KYC): Desde la recepción de datos hasta la validación de firmas y la apertura final de cuenta.

Pipelines de Aprobación de Riesgos: Flujos donde un analista inicia el scoring, un Manager evalúa y un Administrator aprueba el desembolso.

Auditoría Interna y Cumplimiento Normativo (Compliance): Registro inalterable de quién, cuándo y por qué aprobó o rechazó un paso específico del negocio.

🚀 Características Clave y Valor Empresarial
Gobernanza y Control de Accesos (RBAC): Restringe las acciones críticas basándose en el rango del empleado (Administrador, Manager, Usuario), replicando las estrictas estructuras de seguridad bancaria.

Motor de Flujos Configurable: Los procesos no son rígidos; se adaptan a la secuencia lógica que el negocio requiera (Creado → Validación Documental → Evaluación de Riesgo → Aprobado).

Línea de Tiempo de Eventos (Auditoría Cero Errores): Cada cambio de estado, modificación de campo o intervención humana genera un evento inalterable. Una bitácora perfecta para controles regulatorios.

Métricas Operativas en Tiempo Real: El sistema consolida datos automáticamente (procesos por estado, eventos por usuario), permitiendo a los directivos detectar cuellos de botella operativos de inmediato mediante WebSockets.

🛠️ Arquitectura Técnica y Buenas Prácticas
El sistema ha sido construido bajo los estándares de la industria del software moderno, garantizando escalabilidad, seguridad y mantenibilidad:

Arquitectura Limpia en Capas: Separación estricta entre la lógica de entrada (API Routers), la lógica de negocio (Service Layer/Workflow Engine) y la capa de persistencia de datos (PostgreSQL).

Seguridad de Nivel Financiero: Autenticación y autorización mediante tokens securizados JWT.

Infraestructura Profesional: Contenerizado con Docker para despliegues idénticos en entornos locales o en la nube, y control de base de datos evolutivo con migraciones a través de Alembic.

✉️ Contacto y Consultoría de Procesos
Desarrollador: José Carlos Lobo

LinkedIn: www.linkedin.com/in/josé-carlos-lobo-473b458a
