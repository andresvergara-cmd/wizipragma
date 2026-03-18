# Equipo de Agentes Especializados para CENTLI

## 🎯 Objetivo
Desarrollar una interfaz conversacional mejorada para CENTLI que incluya:
- Recomendación de servicios financieros
- Respuestas a preguntas frecuentes (FAQ)
- Recomendación de productos financieros personalizados
- Resumen de cuenta
- Agendamiento de citas

---

## 👥 Equipo de Agentes

### 1. 🎨 CENTLI UX/UI Designer (`centli-ux-designer`)

**Especialidad**: Diseño de experiencia de usuario e interfaz conversacional

**Responsabilidades**:
- Diseñar flujos conversacionales intuitivos
- Crear mockups de respuestas del chat
- Definir estados de la interfaz (loading, success, error)
- Diseñar componentes React para respuestas enriquecidas
- Optimizar la experiencia de voz

**Cuándo usarlo**:
- "Diseña el flujo conversacional para recomendación de productos"
- "Crea mockups para confirmaciones visuales de transferencias"
- "Optimiza la experiencia de onboarding conversacional"

**Ubicación**: `.kiro/agents/centli-ux-designer.md`

---

### 2. ⚙️ CENTLI AgentCore Developer (`centli-agentcore-agent`)

**Especialidad**: Desarrollo de backend con AWS Bedrock AgentCore

**Responsabilidades**:
- Implementar nuevas herramientas (tools) para el agente
- Optimizar prompts del sistema
- Desarrollar lógica de negocio para funcionalidades financieras
- Integrar con servicios AWS (DynamoDB, Lambda, Bedrock)

**Cuándo usarlo**:
- "Implementa el tool recommend_financial_service"
- "Optimiza el system prompt para mejores respuestas"
- "Crea el tool para responder preguntas frecuentes"

**Ubicación**: `.kiro/agents/centli-agentcore-agent.md`

---

### 3. 💻 CENTLI Frontend Developer (`centli-frontend-agent`)

**Especialidad**: Desarrollo frontend con React y WebSocket

**Responsabilidades**:
- Desarrollar componentes React para el chat widget
- Implementar integración con WebSocket
- Crear componentes visuales para respuestas enriquecidas
- Implementar funcionalidad de voz mejorada

**Cuándo usarlo**:
- "Crea el componente TransactionCard para mostrar transferencias"
- "Implementa el indicador de 'escribiendo...'"
- "Mejora la visualización de audio mientras graba"

**Ubicación**: `.kiro/agents/centli-frontend-agent.md`

---

## 🚀 Workflow de Desarrollo

### Fase 1: Diseño (UX/UI Designer)
1. Definir flujo conversacional
2. Crear mockups de respuestas
3. Especificar componentes visuales
4. Documentar guías de estilo

### Fase 2: Backend (AgentCore Developer)
1. Implementar tools en Python
2. Actualizar system prompt
3. Crear tests unitarios
4. Desplegar a Lambda

### Fase 3: Frontend (Frontend Developer)
1. Crear componentes React
2. Integrar con WebSocket
3. Implementar estilos
4. Probar en local

### Fase 4: Integración y Testing
1. Probar flujo completo end-to-end
2. Ajustar UX basado en pruebas
3. Optimizar performance
4. Desplegar a producción

---

## 📋 Funcionalidades Planificadas

### 1. Recomendación de Servicios Financieros
- **UX**: Flujo conversacional + mockup de ServiceCard
- **Backend**: Tool `recommend_financial_service`
- **Frontend**: Componente `ServiceCard`

### 2. Respuestas a Preguntas Frecuentes
- **UX**: Flujo de FAQ + mockup de FAQCard
- **Backend**: Tool `answer_faq`
- **Frontend**: Componente `FAQCard`

### 3. Recomendación de Productos Financieros
- **UX**: Flujo de recomendación + mockup de ProductCard
- **Backend**: Tool `recommend_product`
- **Frontend**: Componente `ProductCard` (mejorado)

### 4. Resumen de Cuenta
- **UX**: Flujo de consulta + mockup de SummaryCard
- **Backend**: Tool `get_account_summary`
- **Frontend**: Componente `SummaryCard`

### 5. Agendamiento de Citas
- **UX**: Flujo de agendamiento + mockup de AppointmentCard
- **Backend**: Tool `schedule_appointment`
- **Frontend**: Componente `AppointmentCard`

---

## 🎯 Cómo Usar los Agentes

### Opción 1: Invocar directamente
```
@centli-ux-designer Diseña el flujo conversacional para recomendación de servicios
```

### Opción 2: Dejar que Kiro sugiera
Simplemente describe tu tarea y Kiro sugerirá el agente apropiado:
```
"Necesito implementar el tool para recomendar productos financieros"
→ Kiro sugerirá usar centli-agentcore-agent
```

### Opción 3: Workflow completo
```
1. @centli-ux-designer Diseña el flujo para recomendación de servicios
2. @centli-agentcore-agent Implementa el tool recommend_financial_service
3. @centli-frontend-agent Crea el componente ServiceCard
```

---

## 📁 Estructura del Proyecto

```
.
├── .kiro/agents/                    # Agentes personalizados
│   ├── centli-ux-designer.md
│   ├── centli-agentcore-agent.md
│   └── centli-frontend-agent.md
│
├── src_aws/app_inference/           # Backend (Lambda)
│   ├── action_tools.py              # Tools del agente
│   ├── bedrock_config.py            # Configuración Bedrock
│   ├── app.py                       # Lambda handler
│   └── data_config.py               # Acceso a DynamoDB
│
├── frontend/src/                    # Frontend (React)
│   ├── components/Chat/             # Chat widget
│   ├── context/                     # Contextos (WebSocket, Chat)
│   └── pages/                       # Páginas (Home, Marketplace, etc.)
│
└── EQUIPO-AGENTES-CENTLI.md        # Este documento
```

---

## 🔄 Estado Actual

### ✅ Completado
- Equipo de 3 agentes especializados creado
- Diseño Comfama implementado en frontend
- Funcionalidades básicas: transferencias y compras
- Chat multimodal (texto + voz)

### 🚧 En Progreso
- Definir flujos conversacionales para nuevas funcionalidades
- Implementar nuevos tools en backend
- Crear componentes de respuesta enriquecida

### 📝 Pendiente
- Implementar las 5 funcionalidades planificadas
- Testing end-to-end
- Optimización de performance
- Despliegue a producción

---

## 💡 Próximos Pasos

1. **Empezar con UX/UI Designer**:
   ```
   @centli-ux-designer Diseña el flujo conversacional completo para las 5 nuevas funcionalidades
   ```

2. **Implementar Backend**:
   ```
   @centli-agentcore-agent Implementa los 5 tools planificados
   ```

3. **Desarrollar Frontend**:
   ```
   @centli-frontend-agent Crea los componentes de respuesta enriquecida
   ```

4. **Integrar y Probar**:
   - Probar cada funcionalidad en local
   - Ajustar basado en feedback
   - Desplegar a producción

---

## 📞 Contacto y Soporte

Para cualquier duda sobre el uso de los agentes o el desarrollo de CENTLI:
- Revisa la documentación de cada agente en `.kiro/agents/`
- Consulta los archivos de código fuente
- Usa Kiro para preguntas específicas

---

¡El equipo de agentes está listo para desarrollar la interfaz conversacional de CENTLI! 🚀
