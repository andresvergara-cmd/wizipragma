# Application Design Plan - CENTLI

## Context Summary

**Project**: Evolution from WiZi (conversational advisor) to CENTLI (transactional banking agent)

**Key Business Capabilities**:
1. Transferencia P2P por voz (voice-driven peer-to-peer transfers)
2. Compra de productos con optimización de beneficios (product purchases with benefit optimization)
3. Orquestación agentic multimodal (multimodal agentic orchestration)

**Functional Areas**:
- AgentCore Orchestration (AWS Bedrock AgentCore)
- Voice Processing (Nova Sonic - speech-to-text & text-to-speech)
- Image Processing (Nova Canvas - image analysis)
- Core Banking Operations (mock)
- Marketplace & Benefits (mock)
- CRM & Beneficiaries (mock)
- Frontend Multimodal UI

**Design Scope**: Standard depth (hackathon context, 8-hour timeline, 3 developers)

---

## Application Design Execution Plan

### Phase 1: Component Identification
- [x] Identify main functional components based on requirements and user stories
- [x] Define component boundaries and responsibilities
- [x] Map components to user stories (Dev 1, Dev 2, Dev 3 stacks)
- [x] Validate component organization supports parallel development

### Phase 2: Component Methods Definition
- [x] Define method signatures for each component
- [x] Specify input/output types for methods
- [x] Document high-level purpose of each method
- [x] Note: Detailed business rules deferred to Functional Design (CONSTRUCTION phase)

### Phase 3: Service Layer Design
- [x] Identify orchestration services
- [x] Define service responsibilities
- [x] Design service interaction patterns
- [x] Specify service-to-component communication

### Phase 4: Component Dependencies
- [x] Create dependency matrix
- [x] Define communication patterns (synchronous/asynchronous)
- [x] Document data flow between components
- [x] Identify integration points

### Phase 5: Design Artifacts Generation
- [x] Generate components.md with component definitions
- [x] Generate component-methods.md with method signatures
- [x] Generate services.md with service definitions
- [x] Generate component-dependency.md with dependency relationships
- [x] Validate design completeness and consistency

---

## Design Clarification Questions

### Component Organization

**Q1**: Los 6 componentes preliminares identificados en el execution plan son:
1. Infrastructure Foundation
2. AgentCore Orchestrator
3. Core Banking Mock (Action Group)
4. Marketplace Mock (Action Group)
5. CRM Mock (Action Group)
6. Frontend Multimodal UI

¿Esta organización de componentes es correcta o prefieres una estructura diferente? Por ejemplo, ¿deberíamos separar Nova Sonic y Nova Canvas como componentes independientes del AgentCore Orchestrator?

[Answer]: Está bien como lo tienes

---

**Q2**: Para el componente "Infrastructure Foundation", ¿debería ser tratado como un componente de aplicación o simplemente como configuración de infraestructura (SAM template, DynamoDB schemas, IAM roles)? En otras palabras, ¿necesita métodos de aplicación o solo definiciones de recursos?

[Answer]: "Infrastructure Foundation" debería ser solo configuración:

SAM template con todas las definiciones
Scripts de deployment simples
Sin lógica de aplicación compleja

---

### Component Methods - AgentCore Orchestrator

**Q3**: El AgentCore Orchestrator necesita métodos para:
- Procesar mensajes entrantes (texto/voz/imagen)
- Invocar Action Groups apropiados
- Gestionar Managed Memory
- Generar respuestas (texto/voz)

¿Hay algún método adicional crítico que debamos incluir en este componente? Por ejemplo, ¿necesitamos métodos explícitos para validación de autenticación o manejo de sesiones?

[Answer]: si validacion de autenticacion, manejo de sesiones y biometria

---

### Component Methods - Action Groups

**Q4**: Para los 3 Action Groups (CoreBanking, Marketplace, CRM), ¿prefieres que cada Action Group tenga:
- **Opción A**: Un solo método genérico `executeAction(actionName, parameters)` que rutea internamente
- **Opción B**: Métodos específicos por cada acción (ej. `getBalance()`, `executeTransfer()`, `listProducts()`)
- **Opción C**: Mix - método genérico + métodos específicos para acciones complejas

[Answer]: B

---

### Service Layer Design

**Q5**: ¿Necesitamos un servicio de orquestación explícito entre el WebSocket API Gateway y el AgentCore, o el Lambda de inferencia puede manejar esta orquestación directamente?

Contexto: Actualmente existe `app_inference` Lambda que maneja WebSocket messages. ¿Debería evolucionar a un servicio de orquestación o mantener su rol actual?

[Answer]: Evoluciona a un servicio de orquestacion

---

**Q6**: Para la gestión de sesiones y contexto de usuario, ¿prefieres:
- **Opción A**: Managed Memory de Bedrock maneja todo el contexto (sin servicio adicional)
- **Opción B**: Servicio de sesión explícito que coordina con Managed Memory
- **Opción C**: Servicio de sesión que gestiona contexto localmente (DynamoDB) y sincroniza con Managed Memory

[Answer]: C

---

### Component Dependencies & Communication

**Q7**: Para la comunicación entre AgentCore y los Action Groups, ¿los Action Groups deben:
- **Opción A**: Ser invocados directamente por AgentCore (Bedrock maneja invocación)
- **Opción B**: Tener una capa de adaptador/proxy entre AgentCore y Action Groups
- **Opción C**: Usar un patrón de event bus para desacoplar

Contexto: Bedrock AgentCore tiene integración nativa con Action Groups vía Lambda, pero podemos agregar capas adicionales si es necesario.

[Answer]: C

---

**Q8**: Para el procesamiento de voz (Nova Sonic), ¿debería:
- **Opción A**: Ser invocado directamente por AgentCore (integración nativa Bedrock)
- **Opción B**: Tener un servicio de procesamiento de voz separado que coordina con AgentCore
- **Opción C**: Ser manejado por el Lambda de orquestación antes de llegar a AgentCore

[Answer]: A

---

### Error Handling & Resilience

**Q9**: Para el manejo de errores en los Action Groups (ej. saldo insuficiente, producto no encontrado), ¿prefieres:
- **Opción A**: Action Groups retornan errores estructurados, AgentCore los interpreta y genera respuesta al usuario
- **Opción B**: Action Groups lanzan excepciones, Lambda de orquestación las captura y maneja
- **Opción C**: Cada Action Group maneja sus propios errores y retorna respuestas user-friendly

[Answer]: A

---

### Data Flow & State Management

**Q10**: Para el flujo de datos en transacciones (ej. transferencia P2P), ¿la validación de saldo debe ocurrir:
- **Opción A**: En el Action Group CoreBanking (validación + ejecución en un solo lugar)
- **Opción B**: En el AgentCore antes de invocar Action Group (validación preventiva)
- **Opción C**: En ambos lugares (AgentCore valida, Action Group re-valida antes de ejecutar)

[Answer]: C

---

## Instructions for Completion

1. **Fill all [Answer]: tags** with your responses
2. **Be specific** - avoid vague answers like "depends" or "mix of both" without clear criteria
3. **Consider the 8-hour timeline** - simpler designs may be more appropriate
4. **Think about parallel development** - design should support 3 developers working simultaneously
5. **Save this file** after completing all answers
6. **Notify me** when all questions are answered

---

## Follow-up Questions (Ambiguity Resolution)

### Q7 Follow-up: Event Bus Implementation

Tu respuesta a Q7 fue "Opción C: Usar un patrón de event bus para desacoplar".

**Contexto de Preocupación**: 
- Un event bus (como EventBridge o SNS/SQS) agrega complejidad significativa
- Para un hackathon de 8 horas, esto podría consumir tiempo valioso
- Bedrock AgentCore ya tiene integración nativa con Action Groups vía Lambda

**Pregunta de Clarificación**:
¿Realmente necesitas un event bus completo, o te refieres a un patrón más simple de desacoplamiento?

**Opciones Refinadas**:
- **Opción C1**: Event bus real (EventBridge/SNS) - Desacoplamiento completo pero complejo
- **Opción C2**: Patrón de mensajería simple (DynamoDB Streams o cola in-memory) - Desacoplamiento ligero
- **Opción C3**: Invocación directa con abstracción (AgentCore → Action Groups directo, pero con interface clara) - Simple y rápido

Considerando tu timeline de 8 horas, ¿cuál de estas opciones prefieres?

[Answer]: Opción C1 - Event bus real (EventBridge/SNS)

---

**Status**: All questions answered  
**Created**: 2026-02-16  
**Questions**: 10 questions answered + 1 follow-up answered
