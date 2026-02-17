# Business Case: CENTLI - Orquestador de Inteligencia Financiera Multimodal

## Executive Summary

**Proyecto**: Evolución de WiZi (demo) a CENTLI (producción)

**Visión**: Transformar el coach financiero conversacional actual en un orquestador bancario agentic de grado producción que integra el core bancario con la vida diaria del usuario en México.

**Cambio Fundamental**: De asistente pasivo (responde preguntas) a agente activo (ejecuta transacciones, optimiza beneficios, anticipa necesidades).

## 1. Estado Actual vs. Visión Futura

### Estado Actual (WiZi Demo)
- **Rol**: Coach financiero conversacional
- **Capacidades**: 
  - Responder preguntas sobre finanzas personales
  - Analizar perfil y transacciones
  - Recomendar retailers con beneficios
  - Mantener historial conversacional
- **Arquitectura**: Serverless básico (Lambda + DynamoDB + Bedrock)
- **Limitaciones**:
  - Solo conversacional (no transaccional)
  - Sin autenticación
  - Sin integración con core bancario
  - Sin capacidades agentic
  - Datos sintéticos

### Visión Futura (CENTLI Producción)
- **Rol**: Orquestador de Inteligencia Bancaria 4.0
- **Identidad**: CENTLI (náhuatl: centli = maíz/unidad/abundancia)
- **Personalidad**: Sabio, sólido, eficiente, vigilante
- **Filosofía**: Seguridad institucional milenaria + agilidad tecnológica cuántica

## 2. Capacidades Nuevas Requeridas

### 2.1 AWS Bedrock AgentCore (Agentic AI)
**Principio**: "Unidad" - integración total del ecosistema financiero

#### Percepción Multimodal
- Interpretar voz y texto
- Analizar contexto emocional
- Detectar urgencia del usuario
- **Gap Actual**: Solo texto vía WebSocket

#### Memoria Ancestral (Managed Memory)
- Recordar patrones de comportamiento
- Mantener lista de beneficiarios frecuentes
- Anticipar necesidades (ej. pago de servicios antes de fecha límite)
- **Gap Actual**: Solo historial conversacional básico

#### Orquestación de Acción (Action Groups)
- Ejecutar transacciones bancarias (SPEI, CoDi, DiMo)
- Conectar con retailers para beneficios
- Activar cashback, puntos, meses sin intereses
- **Gap Actual**: Cero capacidades transaccionales

### 2.2 Integración con Ecosistema Mexicano

#### Sistemas de Pago
- **SPEI**: Transferencias interbancarias
- **CoDi**: Cobro Digital (QR)
- **DiMo**: Dinero Móvil
- **Gap Actual**: No hay integración con sistemas de pago

#### Compliance y Regulación
- **CNBV**: Comisión Nacional Bancaria y de Valores
- Encriptación grado bancario
- Máscaras de PII en toda interacción
- **Gap Actual**: Sin compliance bancario

#### Autenticación
- Biometría pasiva para bajo riesgo
- Validación adicional para movimientos inusuales
- **Gap Actual**: Sin autenticación

### 2.3 Integración Retail Activa

#### Motor de Beneficios "Tlazohcamati"
- Búsqueda activa de cashback
- Optimización de puntos
- Meses sin intereses
- **Retailers**: Oxxo, Walmart, Liverpool, etc.
- **Gap Actual**: Solo recomendaciones pasivas

#### Transformación Transaccional
- Convertir compra simple en decisión financiera inteligente
- Aplicar beneficios automáticamente
- **Gap Actual**: No hay ejecución transaccional

## 3. Requisitos de Producción

### 3.1 Seguridad (Vigilancia del Guerrero)
**Prioridad**: Absoluta

- Protección de activos como prioridad #1
- Cumplimiento estricto CNBV
- Encriptación grado bancario
- Biometría pasiva + validación adicional
- Máscaras de datos sensibles (PII)
- Detección de movimientos inusuales

### 3.2 Experiencia de Usuario

#### Lenguaje y Cultura
- Español de México impecable, nivel ejecutivo
- Matiz cultural: Conceptos de prosperidad
- Términos clave: "Operación firme", "Sustento actualizado"
- Reconocimiento del ecosistema financiero mexicano

#### Estructura de Interacción
- Respuestas en Markdown para móviles
- Confirmaciones con datos clave (Monto, Destinatario, Concepto)
- Cierre proactivo asegurando orden financiero

### 3.3 Arquitectura Agentic

#### AWS Bedrock AgentCore
- Agents con Action Groups
- Managed Memory para contexto persistente
- Knowledge Bases para información bancaria
- Guardrails para seguridad

#### Integraciones
- Core bancario (transacciones, saldos, movimientos)
- Sistemas de pago mexicanos (SPEI, CoDi, DiMo)
- APIs de retailers para beneficios
- Sistemas de autenticación/biometría

## 4. Transformación Arquitectónica

### De Conversacional a Transaccional

#### Actual (WiZi)
```
Usuario → WebSocket → Lambda → Bedrock (Converse) → Respuesta
                         ↓
                    DynamoDB (datos estáticos)
```

#### Futuro (CENTLI)
```
Usuario → Multimodal → AgentCore → Action Groups → Core Bancario
                          ↓              ↓              ↓
                    Managed Memory   Retailers    SPEI/CoDi/DiMo
                          ↓              ↓              ↓
                    Knowledge Base  Beneficios   Transacciones
                          ↓
                    Guardrails (Seguridad CNBV)
```

## 5. Casos de Uso Clave

### Caso 1: Transferencia SPEI Inteligente
**Usuario**: "Envía $5,000 a mi mamá"
**CENTLI**:
1. Identifica beneficiario frecuente (Managed Memory)
2. Valida saldo y límites
3. Aplica biometría pasiva
4. Ejecuta SPEI vía Action Group
5. Confirma: "Operación firme. $5,000 MXN enviados a María López vía SPEI"

### Caso 2: Compra con Optimización de Beneficios
**Usuario**: "Quiero comprar una laptop en Liverpool"
**CENTLI**:
1. Consulta beneficios disponibles (Action Group → Retailers)
2. Identifica: 12 MSI + 5% cashback
3. Calcula ahorro total
4. Presenta opciones optimizadas
5. Ejecuta compra con beneficios aplicados
6. Confirma: "Sustento actualizado. Laptop adquirida con 12 MSI + $500 cashback"

### Caso 3: Anticipación Proactiva
**CENTLI** (sin solicitud):
"Tu pago de luz vence en 3 días. ¿Deseas que lo procese ahora? Tienes 2% de descuento por pago anticipado en CFE."

## 6. Métricas de Éxito

### Funcionales
- Tasa de éxito transaccional > 99.5%
- Tiempo de respuesta < 2 segundos
- Precisión de recomendaciones > 90%

### Negocio
- Adopción de usuarios activos
- Volumen de transacciones procesadas
- Beneficios capturados para usuarios (cashback, puntos)
- NPS (Net Promoter Score)

### Técnicas
- Disponibilidad > 99.9%
- Cumplimiento CNBV 100%
- Cero brechas de seguridad

## 7. Fases de Implementación Sugeridas

### Fase 1: Fundación Agentic
- Migrar de Bedrock Converse a AgentCore
- Implementar Action Groups básicos (consultas)
- Agregar Managed Memory
- Implementar autenticación

### Fase 2: Capacidades Transaccionales
- Integrar core bancario (read-only)
- Implementar SPEI/CoDi/DiMo
- Agregar Guardrails de seguridad
- Compliance CNBV

### Fase 3: Optimización Retail
- Integrar APIs de retailers
- Motor de beneficios "Tlazohcamati"
- Ejecución transaccional completa

### Fase 4: Inteligencia Proactiva
- Anticipación de necesidades
- Alertas inteligentes
- Optimización continua

## 8. Preguntas Pendientes para Requirements Analysis

### Técnicas
1. ¿Qué core bancario utilizan? ¿Tiene APIs REST/GraphQL?
2. ¿Ya tienen integraciones con SPEI/CoDi/DiMo o hay que construirlas?
3. ¿Qué sistema de autenticación/biometría tienen?
4. ¿Presupuesto estimado para Bedrock AgentCore? (más costoso que Converse)

### Negocio
5. ¿Cuántos usuarios piloto para CENTLI?
6. ¿Timeline para producción?
7. ¿Qué retailers ya tienen acuerdos de beneficios?
8. ¿Quién es el sponsor ejecutivo del proyecto?

### Compliance
9. ¿Ya tienen certificación CNBV para banca digital?
10. ¿Qué auditorías de seguridad se requieren?
11. ¿Hay requisitos específicos de encriptación?
12. ¿Necesitan SOC 2, ISO 27001?

### Datos
13. ¿Los datos actuales son sintéticos o reales anonimizados?
14. ¿Cómo se sincronizarán datos del core bancario?
15. ¿Qué tan en tiempo real deben ser las transacciones?

## 9. Riesgos y Consideraciones

### Alto Riesgo
- **Seguridad**: Cualquier brecha es catastrófica en banca
- **Compliance**: Incumplimiento CNBV puede detener operaciones
- **Disponibilidad**: Downtime afecta transacciones reales de dinero

### Medio Riesgo
- **Costo**: Bedrock AgentCore + Action Groups es significativamente más costoso
- **Complejidad**: Arquitectura agentic es más compleja que conversacional
- **Integraciones**: Dependencia de APIs de terceros (retailers, core bancario)

### Mitigación
- Testing exhaustivo en sandbox
- Rollout gradual por fases
- Monitoreo 24/7
- Plan de rollback para cada fase

## 10. Conclusión

La evolución de WiZi a CENTLI representa un salto cuántico:
- De **conversacional** a **transaccional**
- De **reactivo** a **proactivo**
- De **demo** a **producción bancaria**

Requiere transformación arquitectónica completa con AWS Bedrock AgentCore, integraciones profundas con ecosistema bancario mexicano, y cumplimiento estricto de regulaciones CNBV.

El éxito dependerá de:
1. Seguridad impecable
2. Experiencia de usuario fluida
3. Integración perfecta con core bancario
4. Optimización real de beneficios para usuarios
