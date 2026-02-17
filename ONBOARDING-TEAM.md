# 🚀 CENTLI Hackathon - Guía de Onboarding para el Equipo

## 📋 Contexto del Proyecto

**Proyecto**: CENTLI - Asistente Bancario Multimodal con IA  
**Framework**: AIDLC (AI-Driven Lifecycle)  
**Timeline**: 8 horas de hackathon  
**Estado Actual**: Units 1 y 2 completas, Unit 3 en progreso, Unit 4 pendiente

---

## 👥 Asignación de Roles

### Developer 1: Frontend Specialist
- **Unidad**: Unit 4 (Frontend Multimodal UI)
- **Tecnologías**: HTML5, CSS3, JavaScript, WebSocket API
- **Historias**: 7 stories (WebSocket, Voice, Chat, Images, UI)

### Developer 2: Backend Specialist
- **Unidad**: Unit 3 (Action Groups - Backend Services)
- **Tecnologías**: Python 3.11, AWS Lambda, DynamoDB, EventBridge
- **Historias**: 6 stories (Core Banking, Marketplace, CRM)

### Developer 3: Integration Specialist
- **Unidad**: Testing & Integration (Unit 2 ya completo)
- **Tecnologías**: Python, AWS, Testing frameworks
- **Rol**: Integración, testing, soporte a otros devs

---

## 🔧 Setup Inicial (TODOS)

### 1. Clonar el Repositorio

```bash
git clone git@github.com:andresvergara-cmd/wizipragma.git
cd wizipragma
git checkout feature/hackaton
```

### 2. Instalar Dependencias

**Python (Backend - Dev 2 y 3)**:
```bash
# Crear virtual environment
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install boto3 aws-sam-cli
```

**Node.js (Frontend - Dev 1)**:
```bash
# Si necesitas herramientas de desarrollo
npm install
```

### 3. Configurar AWS CLI

```bash
# Configurar el profile de AWS
aws configure --profile 777937796305_Ps-HackatonAgentic-Mexico

# Verificar configuración
aws sts get-caller-identity --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**Credenciales**: Solicitar al líder del equipo

### 4. Verificar Deployment Actual

```bash
# Ver el stack desplegado
aws cloudformation describe-stacks \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --stack-name centli-hackathon

# Ver WebSocket URL
aws cloudformation describe-stacks \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --stack-name centli-hackathon \
  --query 'Stacks[0].Outputs[?OutputKey==`WebSocketURL`].OutputValue' \
  --output text
```

---

## 📚 Documentos Clave a Leer

### TODOS deben leer:
1. **`aidlc-docs/TEAM-DISTRIBUTION-PLAN.md`** ← EMPEZAR AQUÍ
   - Plan completo de distribución de trabajo
   - Timeline y coordinación
   - Flujo AIDLC por desarrollador

2. **`README.md`**
   - Descripción general del proyecto
   - Arquitectura de alto nivel

3. **`aidlc-docs/aidlc-state.md`**
   - Estado actual del proyecto
   - Qué está completo y qué falta

### Developer 1 (Frontend) debe leer:
1. **`aidlc-docs/inception/application-design/unit-of-work.md`**
   - Sección "Unit 4: Frontend Multimodal UI"
   - Responsabilidades y tecnologías

2. **`aidlc-docs/inception/user-stories/stories.md`**
   - Stories 1.1 a 1.7 (tus historias asignadas)

3. **`.kiro/agents/centli-frontend-agent.md`**
   - Tu agente especializado de IA

### Developer 2 (Backend) debe leer:
1. **`aidlc-docs/inception/application-design/unit-of-work.md`**
   - Sección "Unit 3: Action Groups"
   - Responsabilidades y tecnologías

2. **`aidlc-docs/construction/action-groups/functional-design/`**
   - `business-logic-model.md` - Workflows y procesos
   - `domain-entities.md` - Entidades y atributos
   - `business-rules.md` - Reglas de negocio

3. **`aidlc-docs/construction/plans/action-groups-nfr-requirements-plan.md`**
   - 25 preguntas NFR que debes responder

4. **`.kiro/agents/centli-backend-agent.md`**
   - Tu agente especializado de IA

### Developer 3 (Integration) debe leer:
1. **`aidlc-docs/inception/application-design/unit-of-work.md`**
   - Sección "Integration Contracts"
   - Entender cómo se comunican las unidades

2. **`aidlc-docs/construction/agentcore-orchestration/`**
   - Unit 2 completo (tu responsabilidad mantener)

3. **`BEDROCK-SETUP-STATUS.md`**
   - Estado de Bedrock AgentCore

4. **`.kiro/agents/centli-test-agent.md`**
   - Tu agente especializado de IA

---

## 🎯 Primeros Pasos por Rol

### Developer 1 (Frontend):

**Paso 1**: Leer documentación asignada (30 min)

**Paso 2**: Crear plan NFR para Unit 4
```bash
# Abrir Kiro o tu IDE favorito
# Pedir al AI: "Crea el plan NFR Requirements para Unit 4 (Frontend)"
# Ubicación: aidlc-docs/construction/plans/frontend-nfr-requirements-plan.md
```

**Paso 3**: Responder preguntas NFR (~20 preguntas sobre performance, UX, etc.)

**Paso 4**: Esperar a que AI genere artefactos NFR

**Paso 5**: Continuar con siguiente etapa AIDLC

---

### Developer 2 (Backend):

**Paso 1**: Leer documentación asignada (30 min)
- Especialmente los 3 documentos de Functional Design

**Paso 2**: Responder 25 preguntas NFR
```bash
# Abrir: aidlc-docs/construction/plans/action-groups-nfr-requirements-plan.md
# Responder las 25 preguntas en el archivo
# Categorías: Performance, Scalability, Security, Tech Stack, etc.
```

**Paso 3**: Notificar al equipo cuando termines
```bash
# Hacer commit y push
git add aidlc-docs/construction/plans/action-groups-nfr-requirements-plan.md
git commit -m "feat: Unit 3 NFR questions answered"
git push origin feature/hackaton
```

**Paso 4**: Pedir al AI que genere artefactos NFR
```bash
# En Kiro o tu IDE con AI
# Prompt: "Ya respondí las preguntas NFR de Unit 3, continúa con el marco AIDLC"
```

**Paso 5**: Continuar con siguiente etapa AIDLC

---

### Developer 3 (Integration):

**Paso 1**: Leer documentación asignada (30 min)

**Paso 2**: Verificar deployment de Unit 2
```bash
# Probar WebSocket
node test-bedrock-agent.js

# Ver logs de Lambda
aws logs tail /aws/lambda/centli-app-message \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --since 10m
```

**Paso 3**: Preparar framework de testing
```bash
# Crear directorio de tests
mkdir -p tests/integration

# Crear test data
mkdir -p data/test-data
```

**Paso 4**: Crear escenarios de prueba
```bash
# Documentar escenarios en:
# tests/integration/test-scenarios.md
```

**Paso 5**: Estar disponible para ayudar a Dev 1 y Dev 2

---

## 🔄 Flujo AIDLC (Framework de Desarrollo)

Cada desarrollador sigue este flujo para su unidad:

```
1. NFR Requirements (1h)
   ├─ Responder preguntas (~20-25 preguntas)
   ├─ AI genera artefactos (nfr-requirements.md, tech-stack-decisions.md)
   └─ Revisar y aprobar
   
2. NFR Design (30min)
   ├─ AI genera patrones de diseño (nfr-design-patterns.md)
   ├─ AI genera componentes lógicos (logical-components.md)
   └─ Revisar y aprobar
   
3. Infrastructure Design (30min)
   ├─ AI genera diseño de infraestructura (infrastructure-design.md)
   ├─ AI genera arquitectura de deployment (deployment-architecture.md)
   └─ Revisar y aprobar
   
4. Code Generation (2-3h)
   ├─ AI genera plan con checkboxes
   ├─ Revisar y aprobar plan
   ├─ AI genera código
   ├─ Desarrollador revisa código
   ├─ Desarrollador prueba código
   └─ Desarrollador corrige issues
   
5. Integration Testing (2h)
   ├─ Probar con otras unidades
   ├─ Corregir issues de integración
   └─ Preparar demo
```

**Importante**: No saltar etapas. Cada etapa genera artefactos que guían la siguiente.

---

## 🤝 Coordinación del Equipo

### Comunicación:
- **Slack/Teams**: Canal dedicado para el hackathon
- **Standups**: Cada 2 horas (rápidos, 5 minutos)
- **Blockers**: Reportar inmediatamente

### Checkpoints de Integración:
- **Hora 2**: Verificar que todos tienen NFR completo
- **Hora 4**: Primera prueba de integración (Unit 2 + Unit 3)
- **Hora 6**: Prueba de integración completa (todas las unidades)

### Git Workflow:
```bash
# Trabajar en feature/hackaton
git checkout feature/hackaton

# Hacer commits frecuentes
git add .
git commit -m "feat: descripción del cambio"
git push origin feature/hackaton

# Pull antes de push para evitar conflictos
git pull origin feature/hackaton
```

### Resolución de Conflictos:
- **Conflictos de código**: Dev 3 media
- **Conflictos de diseño**: Referirse a artefactos AIDLC
- **Blockers técnicos**: Pedir ayuda al equipo

---

## 🆘 Recursos de Ayuda

### Documentación AWS:
- [AWS Lambda](https://docs.aws.amazon.com/lambda/)
- [DynamoDB](https://docs.aws.amazon.com/dynamodb/)
- [EventBridge](https://docs.aws.amazon.com/eventbridge/)
- [API Gateway WebSocket](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api.html)
- [Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)

### Comandos Útiles:

**Ver logs de Lambda**:
```bash
aws logs tail /aws/lambda/FUNCTION_NAME \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --follow
```

**Desplegar cambios**:
```bash
sam build
sam deploy --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**Probar WebSocket**:
```bash
node test-bedrock-agent.js
```

### Contactos:
- **Líder Técnico**: [Tu nombre]
- **AWS Support**: [Contacto si aplica]
- **Slack Channel**: #centli-hackathon

---

## ✅ Checklist de Onboarding

Marca cuando completes cada paso:

### Todos:
- [ ] Repositorio clonado
- [ ] Branch `feature/hackaton` checked out
- [ ] Dependencias instaladas
- [ ] AWS CLI configurado
- [ ] Deployment verificado
- [ ] `TEAM-DISTRIBUTION-PLAN.md` leído
- [ ] Tu rol y responsabilidades entendidos

### Developer 1 (Frontend):
- [ ] Documentación de Unit 4 leída
- [ ] Plan NFR creado
- [ ] Preguntas NFR respondidas
- [ ] Listo para generar código

### Developer 2 (Backend):
- [ ] Documentación de Unit 3 leída
- [ ] Functional Design artifacts leídos
- [ ] 25 preguntas NFR respondidas
- [ ] Listo para siguiente etapa

### Developer 3 (Integration):
- [ ] Documentación de Unit 2 leída
- [ ] Deployment de Unit 2 verificado
- [ ] Framework de testing preparado
- [ ] Listo para integration testing

---

## 🎉 ¡Estamos Listos!

Una vez que todos completen el onboarding:
1. Hacer un standup rápido (5 min)
2. Confirmar que todos entienden su rol
3. Empezar a trabajar en paralelo
4. Comunicarse frecuentemente

**¡Éxito en el hackathon! 🚀**

---

**Documento creado**: 2026-02-17  
**Última actualización**: 2026-02-17  
**Versión**: 1.0

