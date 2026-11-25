# Curso Agentic Software Development · Proyecto de prácticas (Python)

API REST de gestión de solicitudes con Python, FastAPI y pytest. Sobre este proyecto se practica el flujo:

**Historia → Planner → Especificación aprobada → Developer → Tester → Reviewer → Correcciones → PR**

## Requisitos
Python 3.12 o superior, Git, VS Code con GitHub Copilot y GitHub CLI.

## Puesta en marcha (Windows, PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.\scripts\check.ps1                                          # ruff + formato + mypy + pytest
.venv\Scripts\python -m uvicorn app.main:app --reload        # http://localhost:8000  ·  docs: /docs
```
Si PowerShell no deja ejecutar `scripts\check.ps1`, usa: `powershell -ExecutionPolicy Bypass -File .\scripts\check.ps1`.

En Linux o macOS, cambia `.venv\Scripts\python` por `.venv/bin/python`.

## Uso de la API
### `POST /requests` (H1 · crear una solicitud)
Crea una solicitud. Los datos se guardan en memoria.

```powershell
curl -X POST http://localhost:8000/requests -H "Content-Type: application/json" `
  -d '{"title": "Laptop request", "description": "I need a new laptop."}'
```

- **Cuerpo:** objeto JSON con `title` y `description`, ambos obligatorios y de tipo texto. Se recortan los espacios de los extremos y después se comprueba la longitud: `title` de 1 a 100 caracteres y `description` de 1 a 1000. Los campos extra se ignoran.
- **Respuesta `201 Created`:** `id`, `title`, `description` (ya recortados), `status` (`"open"`) y `created_at` (fecha y hora ISO 8601 con zona horaria).
- **Error `400 Bad Request`:** JSON malformado, campos ausentes, valores que no son texto, vacíos o fuera de los límites. Cuerpo: `{"error": "<mensaje>"}`.

Más ejemplos en `docs/api.http`.

## Contenido
| Ruta | Para qué sirve |
|---|---|
| `.github/copilot-instructions.md` | Reglas generales del proyecto para Copilot |
| `AGENTS.md` | Entorno, comandos, flujo de trabajo y reglas operativas para los agentes |
| `docs/arquitectura.md` | Estructura y capas del código |
| `docs/specs/_plantilla.md` | Plantilla de especificación de una historia |
| `docs/backlog/` | Historias H1–H6 (se crean como issues con `scripts/crear-issues.ps1`) |
| `docs/api.http` | Peticiones de prueba manual (extensión REST Client) |
| `.github/ISSUE_TEMPLATE/historia.md` | Plantilla para nuevas historias |
| `.github/pull_request_template.md` | Plantilla de PR con la Definition of Done |
| `.github/workflows/ci.yml` | CI: ruff, formato, mypy, tests y auditoría de dependencias |

Los agentes (`.github/agents/`) no vienen incluidos: se construyen durante el curso.
