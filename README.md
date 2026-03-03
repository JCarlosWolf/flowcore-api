# Process Manager 🚀

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.99-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 📌 Descripción
**Process Manager** es una API REST construida con **FastAPI**, diseñada para gestionar:

- Procesos con historial de eventos.
- Clientes y usuarios.
- Roles y permisos de acceso.
- Métricas en tiempo real.
- Notificaciones mediante **WebSockets**.

**Python, FastAPI, SQLAlchemy, Pydantic, JWT y WebSockets**.

---

## 🛠 Tecnologías
- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **SQLite / PostgreSQL** (según configuración)
- **JWT Authentication**
- **Pytest** para testing
- **WebSockets** para actualizaciones en tiempo real

---

## 📁 Estructura del proyecto
/app
/models # Modelos de base de datos
/routers # Endpoints de la API
/schemas # Schemas Pydantic
/services # Lógica de negocio
/core # Seguridad, roles, WS manager
/tests # Tests unitarios y de integración
main.py # Entrada principal
requirements.txt # Dependencias

yaml
Copiar código

---

## 🔐 Roles y permisos

| Rol     | Acciones permitidas |
|---------|-------------------|
| **ADMIN** | CRUD usuarios, roles, clientes y procesos |
| **USER**  | Consultar procesos, clientes y métricas |

> Todos los endpoints críticos requieren validación de rol mediante `require_role(RoleEnum.ADMIN)`.

---

## 🚀 Instalación

1. Clonar repositorio:
```bash
git clone https://github.com/tu-usuario/process-manager.git
cd process-manager
Crear y activar entorno virtual:

bash
Copiar código
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Instalar dependencias:

bash
Copiar código
pip install -r requirements.txt
Inicializar la base de datos:

bash
Copiar código
# Si usas Alembic
alembic upgrade head
Correr la aplicación:

bash
Copiar código
uvicorn app.main:app --reload
La API estará disponible en http://127.0.0.1:8000.

📚 Endpoints principales
Autenticación
POST /auth/login → Obtener JWT.

GET /auth/me → Información del usuario actual.

Usuarios (solo ADMIN)
POST /users → Crear usuario.

GET /users → Listar usuarios.

GET /users/{id} → Ver usuario.

PUT /users/{id} → Actualizar usuario.

DELETE /users/{id} → Eliminar usuario.

Roles (solo ADMIN)
CRUD completo en /roles.

Clientes (solo ADMIN)
CRUD completo en /clients.

Procesos
POST /processes → Crear proceso (ADMIN).

GET /processes → Listar procesos.

GET /processes/{id} → Obtener proceso.

PUT /processes/{id} → Actualizar proceso (ADMIN).

DELETE /processes/{id} → Eliminar proceso (ADMIN).

POST /processes/{id}/status → Cambiar estado del proceso.

GET /processes/{id}/timeline → Timeline de eventos.

Eventos de procesos
GET /process-events/process/{id} → Listar eventos de un proceso.

POST /process-events → Crear evento manual.

GET /process-events/{id}/timeline → Timeline paginado.

Métricas
GET /metrics → Métricas por procesos, eventos y usuarios.

WebSockets
/ws/process/{id} → Actualización de eventos de un proceso.

/ws/metrics → Actualización de métricas en tiempo real.

⚡ Pruebas
Ejecuta los tests con Pytest:

bash
Copiar código
pytest --disable-warnings -v
📊 Métricas incluidas
Conteo de procesos por estado.

Conteo de eventos por tipo.

Conteo de eventos por usuario.

🗺 Diagrama de Roles y Acceso
text
Copiar código
       ┌───────────────┐
       │     ADMIN     │
       │ CRUD: Users   │
       │ CRUD: Roles   │
       │ CRUD: Clients │
       │ CRUD: Processes │
       └───────────────┘
               │
               ▼
       ┌───────────────┐
       │     USER      │
       │ Read: Users   │
       │ Read: Processes │
       │ Read: Metrics │
       └───────────────┘
