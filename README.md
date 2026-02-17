# Wizipragma

Proyecto colaborativo con arquitectura modular para desarrollo de AI Agent, Frontend y Backend.

## Estructura del Proyecto

```
wizipragma/
├── agent/              # AI Agent (TypeScript + AgentCore)
├── backend/            # Backend API (Python)
├── frontend/           # Frontend (TypeScript/React)
├── shared/             # Tipos y contratos compartidos
│   ├── types/          # Interfaces TypeScript
│   ├── contracts/      # Especificaciones OpenAPI
│   └── schemas/        # Esquemas de validación
├── integration-tests/  # Tests de integración
├── docker/             # Configuración Docker
└── docs/               # Documentación

```

## Arquitectura

- **Frontend**: Aplicación React con TypeScript (Puerto 3001)
- **Backend**: API REST con Python/FastAPI (Puerto 3000)
- **AI Agent**: Agente IA con TypeScript y AgentCore (Puerto 3002)

## Equipo

- **Developer 1**: AI Agent
- **Developer 2**: Frontend
- **Developer 3**: Backend

## Workflow de Git

### Convención de Branches

- Feature: `{component}/{feature-name}`
  - Ejemplos: `agent/authentication`, `backend/user-api`, `frontend/dashboard`
- Bugfix: `{component}/fix/{bug-description}`
- Hotfix: `hotfix/{issue-description}`

### Proceso

1. Crear feature branch desde `develop`
2. Implementar cambios
3. Ejecutar tests locales
4. Crear Pull Request
5. Revisión de código
6. Merge a `develop`

## Configuración Inicial

Cada componente tiene su propio README con instrucciones de setup específicas.

## Documentación

- [Especificación de API](shared/contracts/api-spec.yaml)
- [Tipos Compartidos](shared/types/)
- [Documentación Completa](docs/)

## Licencia

MIT
