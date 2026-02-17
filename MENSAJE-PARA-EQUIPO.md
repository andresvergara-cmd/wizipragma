# 📧 Mensaje para el Equipo

---

## Para copiar y enviar por Slack/Teams/Email:

---

**Asunto**: 🚀 CENTLI Hackathon - Setup y Distribución de Trabajo

Hola equipo! 👋

Ya tenemos todo listo para empezar el hackathon. He subido al repo toda la documentación y el código base. Aquí está lo que necesitan hacer:

## 🔧 Setup Rápido (15 minutos)

1. **Clonar el repo**:
```bash
git clone git@github.com:andresvergara-cmd/wizipragma.git
cd wizipragma
git checkout feature/hackaton
```

2. **Instalar dependencias**:
```bash
# Python (Backend)
python3 -m venv venv
source venv/bin/activate
pip install boto3 aws-sam-cli

# Node.js (Frontend - si aplica)
npm install
```

3. **Configurar AWS**:
```bash
aws configure --profile 777937796305_Ps-HackatonAgentic-Mexico
```
*(Les paso las credenciales por mensaje privado)*

## 📋 Asignación de Roles

**Developer 1 (Frontend)**: [Nombre]
- Unit 4: Frontend Multimodal UI
- Tecnologías: HTML5, CSS3, JavaScript, WebSocket
- 7 stories de UI

**Developer 2 (Backend)**: [Nombre]  
- Unit 3: Action Groups (Backend Services)
- Tecnologías: Python, Lambda, DynamoDB, EventBridge
- 6 stories de backend

**Developer 3 (Integration)**: [Nombre]
- Testing & Integration
- Unit 2 ya está completo (mantener y probar)
- Soporte a otros devs

## 📚 Documentos CLAVE a Leer

**TODOS deben leer primero**:
1. `ONBOARDING-TEAM.md` ← **EMPEZAR AQUÍ** (guía completa de setup)
2. `aidlc-docs/TEAM-DISTRIBUTION-PLAN.md` (plan de trabajo detallado)
3. `aidlc-docs/aidlc-state.md` (estado actual del proyecto)

**Cada uno debe leer su sección específica** (está en ONBOARDING-TEAM.md)

## 🎯 Primeros Pasos por Rol

### Developer 1 (Frontend):
1. Leer docs de Unit 4 (30 min)
2. Crear plan NFR para frontend
3. Responder ~20 preguntas NFR
4. Esperar a que AI genere artefactos

### Developer 2 (Backend):
1. Leer docs de Unit 3 (30 min)
2. Leer Functional Design artifacts (ya generados)
3. Responder 25 preguntas NFR en: `aidlc-docs/construction/plans/action-groups-nfr-requirements-plan.md`
4. Hacer commit y push cuando termines

### Developer 3 (Integration):
1. Leer docs de Unit 2 (30 min)
2. Verificar deployment actual
3. Preparar framework de testing
4. Estar disponible para ayudar

## 🔄 Framework AIDLC

Estamos usando el framework AIDLC (AI-Driven Lifecycle). Cada uno seguirá este flujo:

```
NFR Requirements → NFR Design → Infrastructure Design → Code Generation → Testing
```

**Importante**: No saltar etapas. Cada etapa genera documentos que guían la siguiente.

## ⏱️ Timeline

- **Hora 0-1**: Setup + NFR Requirements
- **Hora 1-2**: NFR Design + Infrastructure Design
- **Hora 2-4**: Code Generation Planning
- **Hora 4-6**: Code Generation Execution
- **Hora 6-8**: Integration Testing + Demo Prep

## 🤝 Coordinación

- **Standups**: Cada 2 horas (5 minutos)
- **Checkpoints**: Hora 2, 4, y 6
- **Git**: Trabajar en `feature/hackaton`, commits frecuentes
- **Comunicación**: Canal de Slack/Teams

## 📦 Estado Actual

✅ **Unit 1**: Infrastructure Foundation (completo)  
✅ **Unit 2**: AgentCore & Orchestration (completo y desplegado)  
🔄 **Unit 3**: Action Groups (Functional Design completo, NFR pendiente)  
⏳ **Unit 4**: Frontend (todo pendiente)

**WebSocket URL**: `wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod`

## ❓ Preguntas

Si tienen dudas:
1. Revisar `ONBOARDING-TEAM.md` (tiene TODO explicado)
2. Preguntar en el canal del equipo
3. Contactarme directamente

## 🚀 ¡Empecemos!

Una vez que todos completen el setup:
1. Confirmen en el canal que están listos
2. Hacemos un standup rápido (5 min)
3. ¡A trabajar en paralelo!

**¡Éxito en el hackathon! 💪**

---

*Documentos clave*:
- `ONBOARDING-TEAM.md` - Guía completa de setup
- `aidlc-docs/TEAM-DISTRIBUTION-PLAN.md` - Plan de trabajo
- `README.md` - Descripción del proyecto

---

