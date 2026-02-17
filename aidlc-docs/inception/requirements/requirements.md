# Requirements Document - CENTLI Hackathon Demo

## Intent Analysis Summary

**User Request**: Evolucionar demo WiZi a CENTLI - sistema bancario agentic con capacidades transaccionales

**Request Type**: 
- Hackathon/Sprint de 8 horas
- Prototipo de alta fidelidad con datos mock
- Demo funcional para demostrar concepto

**Scope Estimate**: 
- Sistema completo pero con mocks
- Foco en 2 flujos principales: Transferencia P2P por voz + Compra de productos
- Multimodal (voz + texto + imágenes)

**Complexity Estimate**: 
- Alta complejidad técnica
- Timeline muy agresivo (8 horas)
- Requiere AWS Bedrock AgentCore + múltiples servicios AWS
- Equipo: 3 desarrolladores expertos en AWS serverless

---

## 1. CONTEXTO DEL PROYECTO

### 1.1 Estado Actual
- **Proyecto Base**: WiZi - PoC de coach financiero conversacional
- **Arquitectura Actual**: Lambda + DynamoDB + Bedrock Converse + WebSocket
- **Limitaciones**: Solo conversacional, sin capacidades transaccionales, sin autenticación

### 1.2 Objetivo del Hackathon
Crear **CENTLI** - prototipo funcional de orquestador bancario agentic que demuestre:
1. Transferencia P2P por voz ("envíale 50 lucas a mi hermano")
2. Compra de productos con optimización de beneficios
3. Capacidades multimodales (voz, texto, imágenes)
4. Arquitectura agentic con AWS Bedrock AgentCore

### 1.3 Definición de Éxito (8 horas)
- PoC funcional de transferencia P2P por voz
- PoC funcional de compra de productos
- Voz real (AWS Transcribe) + transferencias mock funcionales
- Demo impresionante para stakeholders
- Código de calidad hackathon (funciona, pero no producción)


---

## 2. REQUISITOS FUNCIONALES

### 2.1 Flujo Prioritario #1: Transferencia Social P2P por Voz

#### FR-001: Entrada por Voz
- Usuario dice: "CENTLI, envíale 50 lucas a mi hermano para el almuerzo"
- Sistema usa AWS Transcribe para speech-to-text
- Sistema procesa lenguaje natural para extraer: monto, destinatario, concepto

#### FR-002: Identificación de Contacto
- Sistema identifica "mi hermano" en CRM/contactos del usuario
- Si ambiguo, solicita clarificación
- Recupera datos del beneficiario (nombre, cuenta)

#### FR-003: Validación de Saldo
- Sistema consulta saldo actual en core bancario mock
- Valida que hay fondos suficientes
- Si insuficiente, notifica al usuario

#### FR-004: Autenticación por Voz
- Sistema valida identidad del usuario mediante voz (simulado/básico)
- Autenticación simple pero segura
- Confirmación implícita o explícita según configuración

#### FR-005: Ejecución de Transferencia
- Sistema ejecuta transferencia vía Action Group → Core Mock
- Actualiza saldos en mock (origen y destino)
- Genera registro de transacción

#### FR-006: Confirmación
- Sistema confirma con voz (AWS Polly): "Operación firme. 50,000 pesos enviados a Juan López"
- Muestra detalles en pantalla (monto, destinatario, nuevo saldo)

### 2.2 Flujo Prioritario #2: Compra de Productos con Beneficios

#### FR-007: Solicitud de Compra
- Usuario: "Quiero comprar una laptop en el marketplace"
- Sistema muestra productos disponibles del marketplace mock

#### FR-008: Optimización de Beneficios
- Sistema cruza producto con beneficios disponibles
- Identifica: cashback, puntos, meses sin intereses, descuentos
- Presenta opciones optimizadas al usuario

#### FR-009: Selección y Confirmación
- Usuario selecciona producto y forma de pago
- Sistema valida saldo/crédito disponible
- Solicita confirmación

#### FR-010: Ejecución de Compra
- Sistema ejecuta compra vía Action Group → Marketplace Mock
- Aplica beneficios automáticamente
- Actualiza saldo y puntos

#### FR-011: Confirmación con Beneficios
- Sistema confirma: "Sustento actualizado. Laptop adquirida con 12 MSI + 500 pesos cashback"
- Muestra resumen de compra y beneficios aplicados


### 2.3 Capacidades Multimodales

#### FR-012: Entrada de Voz
- **AWS Bedrock Nova Sonic** para speech-to-text
- Modelo multimodal de Bedrock para procesamiento de audio
- Soporte para español de México
- Procesamiento en tiempo real
- Integración nativa con AgentCore

#### FR-013: Salida de Voz
- **AWS Bedrock Nova Sonic** para text-to-speech
- Modelo multimodal de Bedrock para generación de audio
- Voz en español mexicano natural
- Respuestas contextuales y expresivas
- Integración nativa con AgentCore

#### FR-014: Entrada de Texto
- WebSocket para chat en tiempo real
- Soporte para comandos escritos
- Mismo procesamiento que voz

#### FR-015: Entrada de Imágenes
- Capacidad de recibir imágenes (ej. foto de recibo, productos)
- **AWS Bedrock Nova Canvas** para análisis de imágenes
- Modelo multimodal de Bedrock para comprensión visual
- Extracción de información relevante (texto, objetos, contexto)
- Integración nativa con AgentCore

### 2.4 Capacidades Agentic (AWS Bedrock AgentCore)

#### FR-016: Percepción Multimodal
- Interpretar voz, texto e imágenes
- Analizar contexto emocional (básico)
- Detectar urgencia del usuario

#### FR-017: Memoria Ancestral (Managed Memory)
- Recordar beneficiarios frecuentes
- Mantener historial de conversación
- Recordar patrones de gasto
- Almacenar preferencias del usuario

#### FR-018: Orquestación de Acción (Action Groups)
- Action Group: Core Bancario Mock
  - Consultar saldo
  - Ejecutar transferencia P2P
  - Consultar movimientos
- Action Group: Marketplace Mock
  - Listar productos
  - Ejecutar compra
  - Aplicar beneficios
- Action Group: CRM/Contactos
  - Buscar beneficiarios
  - Resolver "mi hermano", "mi mamá", etc.

#### FR-019: Anticipación Proactiva (Fase 2 - Opcional)
- Alertas de pagos próximos a vencer
- Sugerencias de optimización de beneficios
- Solo si tiempo permite en hackathon


### 2.5 Core Bancario Mock

#### FR-020: Gestión de Cuentas
- Crear/consultar cuentas de usuario
- Mantener saldos actualizados
- Validar existencia de cuentas

#### FR-021: Transferencias P2P
- Ejecutar transferencia entre cuentas
- Validar saldo suficiente
- Actualizar saldos origen y destino
- Generar registro de transacción

#### FR-022: Consultas
- Consultar saldo actual
- Consultar últimos movimientos
- Consultar datos de perfil

#### FR-023: Validaciones Básicas
- Validar monto positivo
- Validar cuenta destino existe
- Validar fondos suficientes
- Validar límites de transacción (opcional)

### 2.6 Marketplace Mock

#### FR-024: Catálogo de Productos
- Listar productos disponibles
- Filtrar por categoría
- Buscar productos
- Mostrar detalles (precio, descripción, imagen)

#### FR-025: Gestión de Beneficios
- Asociar beneficios a productos
- Calcular cashback
- Calcular puntos de lealtad
- Ofrecer meses sin intereses
- Aplicar descuentos

#### FR-026: Ejecución de Compra
- Procesar compra de producto
- Aplicar beneficios automáticamente
- Actualizar saldo del usuario
- Generar comprobante

### 2.7 CRM/Contactos Mock

#### FR-027: Gestión de Beneficiarios
- Almacenar beneficiarios frecuentes del usuario
- Asociar alias ("mi hermano", "mi mamá")
- Almacenar datos de cuenta

#### FR-028: Resolución de Contactos
- Resolver alias a beneficiario real
- Manejar ambigüedades
- Sugerir contactos frecuentes


---

## 3. REQUISITOS NO FUNCIONALES

### 3.1 Performance

#### NFR-001: Latencia de Respuesta
- Transcripción de voz: < 2 segundos
- Procesamiento AgentCore: < 3 segundos
- Respuesta total (voz a voz): < 5 segundos
- **Justificación**: Demo debe sentirse fluida

#### NFR-002: Throughput
- No crítico para hackathon (<100 usuarios)
- Arquitectura debe ser escalable conceptualmente
- **Justificación**: Es demo, no producción

### 3.2 Seguridad

#### NFR-003: Autenticación
- Autenticación por voz simple (simulada/básica)
- Validación de identidad antes de transacciones
- **Justificación**: Demo de concepto, no producción

#### NFR-004: Datos Sensibles
- Todos los datos son mock/sintéticos
- No usar datos reales de clientes
- Máscaras de PII en logs
- **Justificación**: Hackathon, no maneja datos reales

#### NFR-005: Encriptación
- HTTPS para todas las comunicaciones
- Encriptación en tránsito (TLS)
- Encriptación en reposo para DynamoDB
- **Justificación**: Buenas prácticas básicas

### 3.3 Disponibilidad

#### NFR-006: SLA
- No hay SLA formal para hackathon
- Sistema debe funcionar durante demo (2-3 horas)
- **Justificación**: Es demo, no producción

#### NFR-007: Disaster Recovery
- No requerido para hackathon
- Single-region es suficiente
- **Justificación**: Alcance de demo

### 3.4 Escalabilidad

#### NFR-008: Arquitectura Escalable
- Diseño serverless permite escalar
- No optimización prematura
- **Justificación**: Demo conceptual de arquitectura

### 3.5 Usabilidad

#### NFR-009: Experiencia de Usuario
- Interfaz simple e intuitiva
- Respuestas en español de México
- Tono cálido y profesional (personalidad CENTLI)
- **Justificación**: Demo debe impresionar

#### NFR-010: Accesibilidad
- Soporte multimodal (voz + texto)
- Alternativas para usuarios con discapacidades
- **Justificación**: Inclusión y mejores prácticas


### 3.6 Mantenibilidad

#### NFR-011: Código Limpio
- Código legible y bien estructurado
- Comentarios en secciones críticas
- Separación de concerns
- **Justificación**: Facilitar evolución post-hackathon

#### NFR-012: Documentación
- README con instrucciones de deployment
- Documentación de arquitectura
- Documentación de APIs mock
- **Justificación**: Transferencia de conocimiento

### 3.7 Testabilidad

#### NFR-013: Testing
- Testing manual básico de flujos principales
- Validación de integración entre componentes
- No tests automatizados exhaustivos
- **Justificación**: Nivel hackathon, tiempo limitado

### 3.8 Compliance

#### NFR-014: Regulaciones
- No compliance CNBV requerido (es demo)
- Seguir mejores prácticas de seguridad AWS
- **Justificación**: Demo, no producción

---

## 4. RESTRICCIONES

### 4.1 Restricciones de Tiempo
- **Timeline**: 8 horas de hackathon
- **Equipo**: 3 desarrolladores trabajando en paralelo
- **Priorización**: Foco en flujos P2P y compra

### 4.2 Restricciones Técnicas
- **Cloud Provider**: AWS exclusivamente
- **Cuenta AWS**: Una sola cuenta compartida
- **Repositorio**: Un solo repo GitHub
- **Región AWS**: Single-region (us-east-1 recomendado)

### 4.3 Restricciones de Alcance
- **Datos**: Solo datos mock/sintéticos
- **Integraciones**: Solo mocks, no sistemas reales
- **Canales**: Foco en web/móvil, WhatsApp/SMS opcional
- **Testing**: Nivel hackathon, no exhaustivo

### 4.4 Restricciones de Presupuesto
- **AWS**: Presupuesto aprobado sin restricciones específicas
- **Servicios Costosos**: Bedrock AgentCore aprobado
- **Optimización**: No crítica para demo

---

## 5. DEPENDENCIAS

### 5.1 Dependencias de AWS Services
- **AWS Bedrock AgentCore**: Núcleo de inteligencia agentic
- **AWS Bedrock Nova Sonic**: Modelo multimodal para audio (speech-to-text y text-to-speech)
- **AWS Bedrock Nova Canvas**: Modelo multimodal para análisis de imágenes
- **AWS Lambda**: Compute serverless
- **AWS DynamoDB**: Persistencia de datos
- **AWS API Gateway**: WebSocket y REST APIs
- **AWS S3**: Almacenamiento de imágenes y audio

### 5.2 Dependencias de Datos
- **Datos Sintéticos**: Usuarios, cuentas, transacciones, productos
- **Datos de Configuración**: Beneficios, límites, reglas de negocio

### 5.3 Dependencias de Equipo
- **3 Desarrolladores**: Expertos en AWS serverless
- **Colaboración**: GitHub para código compartido
- **Comunicación**: Coordinación en tiempo real


---

## 6. CASOS DE USO DETALLADOS

### 6.1 Caso de Uso: Transferencia P2P por Voz

**Actor**: Usuario de CENTLI

**Precondiciones**:
- Usuario autenticado en la aplicación
- Usuario tiene saldo suficiente
- Beneficiario existe en CRM

**Flujo Principal**:
1. Usuario activa CENTLI por voz o botón
2. Usuario dice: "Envíale 50 lucas a mi hermano para el almuerzo"
3. Sistema transcribe voz a texto (Transcribe)
4. Sistema procesa con AgentCore:
   - Extrae: monto=50000, destinatario="mi hermano", concepto="almuerzo"
   - Invoca Action Group CRM para resolver "mi hermano" → Juan López
   - Invoca Action Group Core para validar saldo
5. Sistema valida identidad por voz (simulado)
6. Sistema invoca Action Group Core para ejecutar transferencia
7. Sistema confirma con voz (Polly): "Operación firme. 50,000 pesos enviados a Juan López"
8. Sistema muestra detalles en pantalla

**Flujo Alternativo 1: Saldo Insuficiente**:
- En paso 4, si saldo insuficiente
- Sistema responde: "No tienes saldo suficiente. Tu saldo actual es 30,000 pesos"
- Fin del caso de uso

**Flujo Alternativo 2: Beneficiario Ambiguo**:
- En paso 4, si "mi hermano" resuelve a múltiples contactos
- Sistema pregunta: "Tienes dos contactos con ese alias. ¿Te refieres a Juan López o Pedro López?"
- Usuario clarifica
- Continúa en paso 5

**Postcondiciones**:
- Saldo del usuario reducido en 50,000
- Saldo del beneficiario incrementado en 50,000
- Transacción registrada en historial
- Conversación guardada en Managed Memory

### 6.2 Caso de Uso: Compra de Producto con Beneficios

**Actor**: Usuario de CENTLI

**Precondiciones**:
- Usuario autenticado
- Usuario tiene saldo o crédito disponible
- Productos disponibles en marketplace

**Flujo Principal**:
1. Usuario: "Quiero comprar una laptop"
2. Sistema muestra catálogo de laptops del marketplace
3. Usuario selecciona laptop específica
4. Sistema invoca Action Group Marketplace para consultar beneficios
5. Sistema presenta opciones:
   - "Opción A: 12 meses sin intereses + 5% cashback (500 pesos)"
   - "Opción B: Pago de contado con 10% descuento (1,000 pesos)"
6. Usuario selecciona opción
7. Sistema valida saldo/crédito disponible
8. Sistema solicita confirmación: "¿Confirmas la compra de Laptop HP por 10,000 pesos con 12 MSI?"
9. Usuario confirma
10. Sistema ejecuta compra vía Action Group Marketplace
11. Sistema actualiza saldo y aplica beneficios
12. Sistema confirma: "Sustento actualizado. Laptop adquirida con 12 MSI + 500 pesos cashback"

**Flujo Alternativo: Crédito Insuficiente**:
- En paso 7, si crédito insuficiente
- Sistema sugiere: "Tu línea de crédito es insuficiente. ¿Deseas pagar de contado?"
- Usuario decide
- Continúa o termina

**Postcondiciones**:
- Compra registrada
- Saldo/crédito actualizado
- Beneficios aplicados
- Producto marcado como comprado


---

## 7. MODELO DE DATOS

### 7.1 Usuario
```json
{
  "userId": "string (PK)",
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "phone": "string",
  "accountNumber": "string",
  "balance": "number",
  "creditLine": {
    "limit": "number",
    "available": "number"
  },
  "preferences": {
    "language": "string",
    "voiceEnabled": "boolean"
  }
}
```

### 7.2 Transacción
```json
{
  "transactionId": "string (PK)",
  "userId": "string",
  "type": "string (P2P, PURCHASE, etc.)",
  "amount": "number",
  "fromAccount": "string",
  "toAccount": "string",
  "concept": "string",
  "timestamp": "string (ISO)",
  "status": "string (COMPLETED, PENDING, FAILED)"
}
```

### 7.3 Beneficiario
```json
{
  "beneficiaryId": "string (PK)",
  "userId": "string (FK)",
  "name": "string",
  "alias": "string (mi hermano, mi mamá)",
  "accountNumber": "string",
  "bank": "string",
  "frequency": "number"
}
```

### 7.4 Producto
```json
{
  "productId": "string (PK)",
  "name": "string",
  "description": "string",
  "price": "number",
  "category": "string",
  "imageUrl": "string",
  "benefits": [
    {
      "type": "string (CASHBACK, MSI, DISCOUNT, POINTS)",
      "value": "number",
      "description": "string"
    }
  ]
}
```

### 7.5 Conversación (Managed Memory)
```json
{
  "sessionId": "string (PK)",
  "userId": "string",
  "messages": [
    {
      "role": "string (user, assistant)",
      "content": "string",
      "timestamp": "string (ISO)",
      "modality": "string (voice, text, image)"
    }
  ],
  "context": {
    "recentBeneficiaries": ["string"],
    "recentProducts": ["string"],
    "userIntent": "string"
  }
}
```

---

## 8. ARQUITECTURA DE ALTO NIVEL

### 8.1 Componentes Principales

```
Usuario (Voz/Texto/Imagen)
    |
    v
[API Gateway WebSocket/REST]
    |
    v
[Lambda: Orchestrator]
    |
    v
[AWS Bedrock AgentCore]
    |
    +-- [Managed Memory] (DynamoDB)
    |
    +-- [Bedrock Nova Sonic] (Audio: Speech-to-Text & Text-to-Speech)
    |
    +-- [Bedrock Nova Canvas] (Image Analysis)
    |
    +-- [Action Groups]
        |
        +-- [AG: Core Bancario Mock] --> [Lambda: Core Mock] --> [DynamoDB: Accounts]
        |
        +-- [AG: Marketplace Mock] --> [Lambda: Marketplace] --> [DynamoDB: Products]
        |
        +-- [AG: CRM Mock] --> [Lambda: CRM] --> [DynamoDB: Beneficiaries]
```

### 8.2 Flujo de Datos

1. **Entrada**: Usuario habla → Nova Sonic → Texto
2. **Procesamiento**: Texto → AgentCore → Análisis de intención
3. **Acción**: AgentCore invoca Action Group apropiado
4. **Ejecución**: Action Group ejecuta lógica de negocio en mock
5. **Respuesta**: Resultado → AgentCore → Genera respuesta
6. **Salida**: Texto → Nova Sonic → Voz + Pantalla

**Flujo Alternativo con Imagen**:
1. **Entrada**: Usuario envía imagen → Nova Canvas → Análisis visual
2. **Procesamiento**: Descripción/datos → AgentCore → Análisis de intención
3. **Continúa**: Igual que flujo principal desde paso 3


---

## 9. PLAN DE IMPLEMENTACIÓN (8 HORAS)

### 9.1 División de Trabajo (3 Desarrolladores)

**Desarrollador 1: Infraestructura y AgentCore**
- Hora 1-2: Setup AWS Bedrock AgentCore + Managed Memory
- Hora 3-4: Configurar Action Groups (esqueletos)
- Hora 5-6: Integrar Nova Sonic (audio) + Nova Canvas (imágenes)
- Hora 7-8: Testing e integración final

**Desarrollador 2: Core Bancario Mock + CRM Mock**
- Hora 1-2: Lambda + DynamoDB para Core Mock (cuentas, saldos)
- Hora 3-4: Implementar transferencias P2P
- Hora 5-6: Lambda + DynamoDB para CRM Mock (beneficiarios)
- Hora 7-8: Testing e integración con AgentCore

**Desarrollador 3: Marketplace Mock + Frontend**
- Hora 1-2: Lambda + DynamoDB para Marketplace (productos, beneficios)
- Hora 3-4: Implementar lógica de compra y beneficios
- Hora 5-6: Frontend básico (WebSocket + UI simple)
- Hora 7-8: Testing e integración final

### 9.2 Hitos Críticos

**Hora 2**: Infraestructura base desplegada
- AgentCore configurado
- DynamoDB tables creadas
- Lambdas base desplegadas

**Hora 4**: Mocks funcionales
- Core Mock: transferencias P2P funcionando
- Marketplace Mock: compras funcionando
- CRM Mock: resolución de contactos funcionando

**Hora 6**: Integración completa
- AgentCore conectado a todos los Action Groups
- Voz (Transcribe + Polly) funcionando
- Flujos end-to-end funcionando

**Hora 8**: Demo lista
- Testing completo de flujos principales
- Frontend pulido
- Demo rehearsal

### 9.3 Priorización de Features

**Must Have (Crítico para demo)**:
- Transferencia P2P por voz
- Compra de producto con beneficios
- Voz (Transcribe + Polly)
- Core Mock básico
- Marketplace Mock básico

**Should Have (Importante pero no crítico)**:
- CRM con resolución de alias
- Múltiples beneficios (cashback, MSI, descuentos)
- Managed Memory persistente
- UI pulida

**Could Have (Nice to have)**:
- Imágenes (Rekognition/Textract)
- Alertas proactivas
- WhatsApp/SMS
- Múltiples canales

**Won't Have (Fuera de alcance)**:
- Video
- Autenticación biométrica real
- Compliance CNBV
- Testing exhaustivo
- Multi-región


---

## 10. RIESGOS Y MITIGACIONES

### 10.1 Riesgos Técnicos

**Riesgo 1: Complejidad de Bedrock AgentCore**
- **Probabilidad**: Alta
- **Impacto**: Alto
- **Mitigación**: 
  - Desarrollador 1 es experto en Bedrock
  - Tener documentación de AgentCore lista
  - Fallback a Bedrock Converse si AgentCore falla

**Riesgo 2: Integración de Voz (Nova Sonic)**
- **Probabilidad**: Media
- **Impacto**: Alto
- **Mitigación**:
  - Probar Nova Sonic en primeras 2 horas
  - Ventaja: Integración nativa con AgentCore
  - Fallback a texto si voz falla
  - Usar ejemplos de AWS Bedrock bien documentados

**Riesgo 3: Coordinación entre 3 Desarrolladores**
- **Probabilidad**: Media
- **Impacto**: Medio
- **Mitigación**:
  - Definir interfaces claras entre componentes
  - Usar feature branches en GitHub
  - Sincronización cada 2 horas

**Riesgo 4: Tiempo Insuficiente**
- **Probabilidad**: Alta
- **Impacto**: Alto
- **Mitigación**:
  - Priorización estricta (Must Have primero)
  - Mocks ultra-simples si es necesario
  - Preparar componentes reutilizables de WiZi

### 10.2 Riesgos de Alcance

**Riesgo 5: Scope Creep**
- **Probabilidad**: Media
- **Impacto**: Alto
- **Mitigación**:
  - Stick to Must Have features
  - No agregar features durante hackathon
  - Timeboxing estricto

### 10.3 Riesgos de Demo

**Riesgo 6: Demo Falla Durante Presentación**
- **Probabilidad**: Media
- **Impacto**: Crítico
- **Mitigación**:
  - Testing exhaustivo en hora 7-8
  - Tener video backup de demo funcionando
  - Datos de prueba bien preparados
  - Rehearsal de demo

---

## 11. CRITERIOS DE ACEPTACIÓN

### 11.1 Criterios Funcionales

**CA-001**: Usuario puede ejecutar transferencia P2P por voz
- Entrada: "Envíale 50 lucas a mi hermano"
- Salida: Transferencia ejecutada, confirmación por voz

**CA-002**: Usuario puede comprar producto con beneficios
- Entrada: "Quiero comprar una laptop"
- Salida: Producto comprado, beneficios aplicados

**CA-003**: Sistema procesa voz correctamente
- Entrada: Audio en español mexicano
- Salida: Transcripción correcta, respuesta por voz

**CA-004**: Mocks funcionan correctamente
- Core Mock: Transferencias actualizan saldos
- Marketplace Mock: Compras aplican beneficios
- CRM Mock: Resuelve alias a beneficiarios

### 11.2 Criterios No Funcionales

**CA-005**: Respuesta en tiempo razonable
- Latencia total < 5 segundos para flujo completo

**CA-006**: Demo es impresionante
- UI limpia y profesional
- Voz natural y fluida
- Flujos sin errores

**CA-007**: Código es mantenible
- Estructura clara
- Comentarios en secciones críticas
- README con instrucciones

---

## 12. RESUMEN DE REQUISITOS

### Requisitos Funcionales: 28 requisitos
- Transferencia P2P: 6 requisitos (FR-001 a FR-006)
- Compra de productos: 5 requisitos (FR-007 a FR-011)
- Multimodal: 4 requisitos (FR-012 a FR-015)
- Agentic: 4 requisitos (FR-016 a FR-019)
- Core Mock: 4 requisitos (FR-020 a FR-023)
- Marketplace Mock: 3 requisitos (FR-024 a FR-026)
- CRM Mock: 2 requisitos (FR-027 a FR-028)

### Requisitos No Funcionales: 14 requisitos
- Performance: 2 requisitos (NFR-001 a NFR-002)
- Seguridad: 3 requisitos (NFR-003 a NFR-005)
- Disponibilidad: 2 requisitos (NFR-006 a NFR-007)
- Escalabilidad: 1 requisito (NFR-008)
- Usabilidad: 2 requisitos (NFR-009 a NFR-010)
- Mantenibilidad: 2 requisitos (NFR-011 a NFR-012)
- Testabilidad: 1 requisito (NFR-013)
- Compliance: 1 requisito (NFR-014)

### Casos de Uso: 2 casos principales
- Transferencia P2P por voz
- Compra de producto con beneficios

### Componentes Principales: 7 componentes
- AWS Bedrock AgentCore
- Core Bancario Mock
- Marketplace Mock
- CRM Mock
- AWS Transcribe
- AWS Polly
- Frontend (WebSocket + UI)

### Timeline: 8 horas
### Equipo: 3 desarrolladores expertos
### Objetivo: Demo funcional impresionante para stakeholders
