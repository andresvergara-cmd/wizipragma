# Unit of Work Plan - CENTLI

## Context Summary

**Project**: CENTLI - Transactional banking agent with multimodal capabilities

**Application Design Summary**:
- 7 components identified (6 application + 1 infrastructure configuration)
- Event-driven architecture with EventBridge
- 3 developers working in parallel (Dev 1: Frontend, Dev 2: Backend/Mocks, Dev 3: AgentCore/AI)
- 19 user stories organized by stack técnico

**Preliminary Units** (from execution plan):
1. Infrastructure Foundation
2. AgentCore Orchestrator
3. Core Banking Mock (Action Group)
4. Marketplace Mock (Action Group)
5. CRM Mock (Action Group)
6. Frontend Multimodal UI

**Decomposition Goal**: Define final units of work with clear boundaries, dependencies, and story mappings for 8-hour hackathon execution

---

## Unit of Work Execution Plan

### Phase 1: Validate Preliminary Units
- [x] Review preliminary units against application design components
- [x] Validate unit boundaries align with developer assignments (Dev 1, 2, 3)
- [x] Confirm each unit can be developed independently (loose coupling)
- [x] Verify units support parallel development

### Phase 2: Define Unit Details
- [x] Document each unit's purpose and responsibilities
- [x] Specify technology stack per unit
- [x] Define deployment artifacts per unit
- [x] Identify integration points between units

### Phase 3: Map Stories to Units
- [x] Assign each of 19 user stories to appropriate unit
- [x] Verify story distribution supports 8-hour timeline
- [x] Ensure Must Have stories (15) are covered
- [x] Validate developer workload balance

### Phase 4: Define Unit Dependencies
- [x] Create dependency matrix showing unit relationships
- [x] Identify critical path units (must complete first)
- [x] Define integration contracts between units
- [x] Specify data exchange formats

### Phase 5: Define Development Sequence
- [x] Determine optimal unit development order
- [x] Identify parallelization opportunities
- [x] Define integration checkpoints (hours 4, 6)
- [x] Plan final integration and testing (hours 7-8)

### Phase 6: Generate Unit Artifacts
- [x] Generate unit-of-work.md with complete unit definitions
- [x] Generate unit-of-work-dependency.md with dependency matrix
- [x] Generate unit-of-work-story-map.md with story assignments
- [x] Validate all artifacts are complete and consistent

---

## Unit Decomposition Questions

### Unit Boundaries

**Q1**: Los 6 componentes de aplicación identificados en Application Design son:
1. AgentCore Orchestrator
2. Orchestration Service (3 Lambdas: Connect, Disconnect, Message)
3. Core Banking Mock (Action Group)
4. Marketplace Mock (Action Group)
5. CRM Mock (Action Group)
6. Frontend Multimodal UI

¿Deberían estos 6 componentes convertirse directamente en 6 unidades de trabajo, o prefieres una agrupación diferente?

Por ejemplo:
- **Opción A**: 6 unidades (1:1 con componentes)
- **Opción B**: 5 unidades (agrupar AgentCore + Orchestration Service en una sola unidad "Backend Orchestration")
- **Opción C**: 4 unidades (agrupar los 3 Action Groups en una sola unidad "Action Groups")
- **Opción D**: Otra agrupación

[Answer]: C

---

**Q2**: Para la unidad "Infrastructure Foundation" (SAM template, DynamoDB, EventBridge, IAM), ¿debería ser:
- **Opción A**: Una unidad independiente que se despliega primero
- **Opción B**: Parte de cada unidad (cada dev maneja su propia infraestructura)
- **Opción C**: Distribuida entre unidades según responsabilidad (ej. Core Banking maneja sus tablas)

Contexto: Opción A es más limpia pero requiere coordinación. Opción B/C permite más autonomía pero puede causar conflictos en SAM template.

[Answer]: C

---

### Story Assignment

**Q3**: Las 19 user stories están actualmente organizadas por stack técnico:
- Dev 1 (Frontend): 7 stories (8.5 horas)
- Dev 2 (Backend/Mocks): 6 stories (10 horas)
- Dev 3 (AgentCore/AI): 6 stories (10.5 horas)

¿Esta asignación de stories a developers debe mantenerse tal cual, o prefieres redistribuir para balancear mejor la carga de trabajo?

Nota: Dev 1 tiene menos horas estimadas (8.5h vs 10h/10.5h de otros devs).

[Answer]: debe mantenerse tal cual

---

### Unit Dependencies

**Q4**: Para el orden de desarrollo de unidades, ¿prefieres:
- **Opción A**: Secuencial estricto (Infrastructure → AgentCore → Action Groups → Frontend)
- **Opción B**: Paralelo máximo (todos empiezan simultáneamente con mocks/stubs)
- **Opción C**: Híbrido (Infrastructure primero, luego paralelo con contratos definidos)

Contexto: Opción A es más segura pero lenta. Opción B es más rápida pero requiere coordinación. Opción C balancea ambos.

[Answer]: B

---

**Q5**: Para la integración entre unidades, ¿cuándo deben ocurrir los checkpoints de integración?
- **Opción A**: Hora 4 (primera integración) y Hora 6 (integración completa)
- **Opción B**: Hora 2, 4, 6 (integraciones incrementales)
- **Opción C**: Hora 6 solamente (integración big-bang)
- **Opción D**: Otra estrategia

[Answer]: B

---

### Deployment Strategy

**Q6**: Para el deployment de unidades, ¿prefieres:
- **Opción A**: Un solo SAM template con todos los recursos (monorepo)
- **Opción B**: SAM templates separados por unidad (multi-repo o mono-repo con múltiples templates)
- **Opción C**: SAM template base + templates anidados por unidad

Contexto: Opción A es más simple para hackathon. Opción B/C es más modular pero complejo.

[Answer]: C

---

### Code Organization (Greenfield)

**Q7**: Para la organización del código en el repositorio, ¿prefieres:
- **Opción A**: Estructura plana (todos los Lambdas en src/, frontend en raíz)
- **Opción B**: Estructura por unidad (src/unit1/, src/unit2/, etc.)
- **Opción C**: Estructura por tipo (src/lambdas/, src/frontend/, src/infrastructure/)
- **Opción D**: Otra estructura

Contexto: Considera que 3 developers trabajarán en paralelo y necesitan minimizar conflictos de merge.

[Answer]: C

---

### Testing Strategy

**Q8**: Para las pruebas de unidades, ¿prefieres:
- **Opción A**: Testing por unidad (cada unidad se prueba independientemente)
- **Opción B**: Testing de integración end-to-end (probar flujos completos)
- **Opción C**: Mix (unit tests + integration tests)
- **Opción D**: Testing manual solamente (nivel hackathon)

[Answer]: C

---

### Critical Path

**Q9**: ¿Cuál unidad consideras más crítica y debe completarse primero?
- **Opción A**: AgentCore Orchestrator (núcleo de inteligencia)
- **Opción B**: Infrastructure Foundation (base para todo)
- **Opción C**: Core Banking Mock (flujo P2P prioritario)
- **Opción D**: Todas en paralelo (sin critical path)

[Answer]: D

---

### Rollback Strategy

**Q10**: Si una unidad falla durante el hackathon, ¿cuál es la estrategia de fallback?
- **Opción A**: Simplificar la unidad (reducir scope, usar mocks más simples)
- **Opción B**: Eliminar la unidad y ajustar demo (ej. sin imágenes si Nova Canvas falla)
- **Opción C**: Tener versiones pre-construidas de backup
- **Opción D**: No hay fallback, arreglar sobre la marcha

[Answer]: A

---

### Agent Assignment Strategy

**Q11**: ¿Quieres usar agentes especializados de Kiro para acelerar el desarrollo durante la fase de CONSTRUCTION?

**Contexto**: En la fase de CONSTRUCTION, cada unidad pasa por diseño y generación de código. Puedes usar agentes especializados de Kiro que trabajen en paralelo, simulando tu equipo de 3 developers.

**Opciones**:

**Opción A**: Un agente por unidad/developer (3 agentes especializados) - RECOMENDADO
- **CENTLI-Frontend-Agent**: Maneja Unit 6 (Frontend Multimodal UI)
  - Contexto: Stories Dev 1, component-methods.md (Frontend), services.md
  - Genera: WebSocket manager, Voice UI, Chat interface, Product catalog
  
- **CENTLI-Backend-Agent**: Maneja Units 3, 4, 5 (Action Groups)
  - Contexto: Stories Dev 2, component-methods.md (Action Groups), services.md
  - Genera: Core Banking Lambda, Marketplace Lambda, CRM Lambda
  
- **CENTLI-AgentCore-Agent**: Maneja Unit 2 (AgentCore + Orchestration)
  - Contexto: Stories Dev 3, component-methods.md (AgentCore), services.md
  - Genera: AgentCore config, Orchestration Service, Nova Sonic/Canvas integration

**Ventajas**: Paralelización real, contexto enfocado, especialización por dominio, menos conflictos

**Opción B**: Agentes por tipo de tarea (3 agentes: Infra, Code, Test)
- **CENTLI-Infra-Agent**: Genera SAM templates, DynamoDB schemas, IAM policies
- **CENTLI-Code-Agent**: Genera código Python/JavaScript para todas las unidades
- **CENTLI-Test-Agent**: Genera y ejecuta tests de integración

**Ventajas**: Consistencia en estilo, reutilización across unidades, especialización por tipo de trabajo

**Opción C**: Agente único con contexto completo
- Un solo agente maneja todas las unidades secuencialmente
- Más simple pero menos especializado y más lento

**Opción D**: No usar agentes especializados
- Yo (el agente actual) manejo todo el desarrollo
- Sin paralelización, pero más control directo

**Opción E**: Híbrido - Agentes por unidad + Agente de testing
- 3 agentes especializados por unidad (Opción A)
- 1 agente adicional de testing que valida todo al final
- Mejor de ambos mundos: especialización + validación centralizada

¿Qué estrategia de agentes prefieres?

[Answer]: E

---

**Si eliges Opción A, B, o E**: ¿Quieres que los agentes especializados se creen automáticamente durante la fase de Code Generation, o prefieres crearlos manualmente antes de empezar CONSTRUCTION?

[Answer]: Crealos automaticamente pero yo los quiero después personalizar

---

## Instructions for Completion

1. **Fill all [Answer]: tags** with your responses
2. **Be specific** - avoid vague answers like "depends" or "mix" without clear criteria
3. **Consider the 8-hour timeline** - simpler approaches may be more appropriate
4. **Think about 3 developers** - design should minimize conflicts and maximize parallelism
5. **Save this file** after completing all answers
6. **Notify me** when all questions are answered

---

**Status**: Awaiting user input  
**Created**: 2026-02-16  
**Questions**: 11 questions requiring answers (10 original + 1 agent strategy)
