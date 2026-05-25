# FlowCore API: Motor de Automatización y Trazabilidad de Procesos de Negocio (BPM)

**Desarrollado por:** José Carlos Lobo  
**Stack Principal:** Python | FastAPI | PostgreSQL | Docker | WebSockets  

---

## 🎯 ¿Qué es FlowCore? (Perspectiva de Negocio)

En cualquier organización, especialmente en sectores altamente regulados como el **financiero o el bancario**, los mayores costes y errores no nacen de la falta de herramientas, sino de la **fricción operativa**: procesos manuales desordenados, falta de claridad en las aprobaciones, pérdida de documentos y la incapacidad de saber en tiempo real en qué fase se encuentra un expediente (ej. el onboarding de un cliente, la validación de un riesgo o la aprobación de un crédito).

**FlowCore** es un sistema backend robusto diseñado específicamente para solucionar este dolor. Es un **Motor de Flujos de Trabajo (Workflow Engine)** que permite a las empresas definir plantillas de procesos, encadenar pasos lógicos obligatorios, asignar roles de cumplimiento y auditar de forma milimétrica cada acción que ocurre en la empresa.

### 🏢 Casos de Uso Reales en la Empresa:
* **Onboarding Automatizado de Clientes (KYC):** Desde la recepción de datos hasta la validación de firmas y la apertura final de cuenta.
* **Pipelines de Aprobación de Riesgos:** Flujos donde un analista inicia el scoring, un Manager evalúa y un Administrador aprueba el desembolso.
* **Auditoría Interna y Cumplimiento Normativo (Compliance):** Registro inalterable de quién, cuándo y por qué aprobó o rechazó un paso específico del negocio.

---

## 🚀 Características Clave y Valor Empresarial

* **Gobernanza y Control de Accesos (RBAC):** Restringe las acciones críticas basándose en el rango del empleado (Administrador, Manager, Usuario), replicando las estrictas estructuras de seguridad bancaria.
* **Motor de Flujos Configurable:** Los procesos no son rígidos; se adaptan a la secuencia lógica que el negocio requiera (`Creado` → `Validación Documental` → `Evaluación de Riesgo` → `Aprobado`).
* **Línea de Tiempo de Eventos (Auditoría Cero Errores):** Cada cambio de estado, modificación de campo o intervención humana genera un evento inalterable. Una bitácora perfecta para controles regulatorios.
* **Métricas Operativas en Tiempo Real:** El sistema consolida datos automáticamente (procesos por estado, eventos por usuario), permitiendo a los directivos detectar cuellos de botella operativos de inmediato mediante *WebSockets*.

---

## 🛠️ Arquitectura Técnica y Buenas Prácticas

El sistema ha sido construido bajo los estándares de la industria del software moderno, garantizando escalabilidad, seguridad y mantenibilidad:

* **Arquitectura Limpia en Capas:** Separación estricta entre la lógica de entrada (API Routers), la lógica de negocio (Service Layer/Workflow Engine) y la capa de persistencia de datos (PostgreSQL).
* **Seguridad de Nivel Financiero:** Autenticación y autorización mediante tokens securizados JWT.
* **Infraestructura Profesional:** Contenerizado con **Docker** para despliegues idénticos en entornos locales o en la nube, y control de base de datos evolutivo con migraciones a través de **Alembic**.

Cliente ➔ [ FastAPI Routers ] ➔ [ Capa de Servicio ] ➔ [ Motor FlowCore ] ➔ [ Base de Datos PostgreSQL ]


---

## 📋 Guía de Inicio Rápido (Desarrolladores)

### Requisitos Previos
* Python 3.10+
* Docker y Docker Compose

### 1. Clonar e Instalar Entorno
```bash
git clone [https://github.com/JCarlosWolf/flowcore-api.git](https://github.com/JCarlosWolf/flowcore-api.git)
cd flowcore-api
python -m venv .venv
Activar entorno:

Windows: .venv\Scripts\activate

Linux/macOS: source .venv/bin/activate

Bash
pip install -r requirements.txt
2. Configuración de Variables (.env)
Crea un archivo .env en la raíz del proyecto con la siguiente estructura:

Fragmento de código
DB_HOST=localhost
DB_PORT=5432
DB_USER=flowcore_user
DB_PASSWORD=flowcore_pass
DB_NAME=flowcore
SECRET_KEY=super_secret_key_bancaria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
3. Levantar Infraestructura y Base de Datos
Bash
# Levantar base de datos en Docker
docker compose up -d

# Ejecutar migraciones de base de datos
alembic upgrade head

# Cargar datos de demostración (Estructura de roles y flujo demo)
python scripts/demo_seed.py
python scripts/seed_roles_users.py
4. Ejecutar la API
Bash
uvicorn app.main:app --reload
Acceso a la documentación interactiva (Swagger): http://localhost:8000/docs

📊 Endpoints Clave del Sistema
POST /auth/login - Autenticación y obtención de credenciales de acceso.

POST /clients - Alta y registro de clientes en el sistema.

POST /processes - Instanciación de un nuevo flujo de trabajo basado en plantillas.

POST /processes/{id}/status - Transición controlada y validada del estado del proceso.

GET /processes/{id}/timeline - Recuperación de la auditoría completa del expediente.

GET /metrics - Cuadro de mando operativo (Kpis de rendimiento del negocio).

✉️ Contacto y Consultoría de Procesos
Si tu empresa sufre pérdidas de tiempo por tareas manuales, falta de trazabilidad en sus flujos internos o necesitas integrar lógica de negocio compleja en tus sistemas de forma segura:

Desarrollador: José Carlos Lobo

Especialidad: Automatización Backend y Optimización de Procesos Operativos (Ex-Banca con más de 35 años de experiencia de negocio).

LinkedIn: www.linkedin.com/in/josé-carlos-lobo-473b458a

Backend portfolio project demonstrating a workflow-based process management architecture built with FastAPI and PostgreSQL.
