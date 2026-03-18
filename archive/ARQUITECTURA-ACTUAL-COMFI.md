# Arquitectura Actual - Sistema Comfi

## 📊 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                            USUARIO FINAL                             │
│                     (Navegador Web / Móvil)                         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         CLOUDFRONT CDN                               │
│  Distribution ID: E2UWNXJTS2NM3V                                    │
│  URL: https://db4aulosarsdo.cloudfront.net                          │
│  - Caché de assets estáticos                                        │
│  - Compresión Gzip/Brotli                                           │
│  - HTTPS/SSL                                                         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Origin Request
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         S3 BUCKET (Frontend)                         │
│  Bucket: comfi-frontend-pragma                                      │
│  - index.html                                                        │
│  - assets/index-*.js (React bundle)                                 │
│  - assets/index-*.css (Estilos)                                     │
│  - Componentes React:                                                │
│    • ChatWidget (chat principal)                                     │
│    • FAQCard, FAQQuickActions (componentes FAQ)                     │
│    • ComfiAvatar (avatar superhéroe)                                 │
│    • Layout, Home, Marketplace                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ WebSocket Connection
                             │ wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    API GATEWAY (WebSocket)                           │
│  API ID: vvg621xawg                                                 │
│  Type: WebSocket API                                                 │
│  Stage: prod                                                         │
│                                                                      │
│  Routes:                                                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ $connect    → Lambda: centli-app-connect                     │  │
│  │ $default    → Lambda: centli-app-message                     │  │
│  │ $disconnect → Lambda: centli-app-disconnect                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Lambda     │ │   Lambda     │ │   Lambda     │
    │ app-connect  │ │ app-message  │ │app-disconnect│
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           │                │                │
           ▼                ▼                ▼
    ┌─────────────────────────────────────────────┐
    │         DynamoDB: centli-sessions           │
    │  - session_id (PK)                          │
    │  - user_id                                  │
    │  - connection_id                            │
    │  - state (ACTIVE/CLOSED)                    │
    │  - created_at, expires_at                   │
    │  - message_count                            │
    └─────────────────────────────────────────────┘
                             
                             │ (app-message invoca)
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BEDROCK AGENT (AgentCore)                         │
│  Agent ID: Z6PCEKYNPS                                               │
│  Name: centli-agentcore                                             │
│  Model: Claude 3.5 Sonnet (us.anthropic.claude-3-5-sonnet-v2:0)   │
│  Status: PREPARED                                                    │
│                                                                      │
│  System Prompt (Instruction):                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Eres Comfi, asistente de Comfama (Colombia)                 │  │
│  │ - Identidad: Comfi de Comfama                                │  │
│  │ - País: Colombia (Antioquia)                                 │  │
│  │ - Moneda: COP (Pesos Colombianos)                            │  │
│  │ - Prohibido: Carlos, México, MXN, CENTLI                     │  │
│  │                                                               │  │
│  │ Capacidades:                                                  │  │
│  │ • Responder FAQs sobre afiliación                            │  │
│  │ • Información sobre créditos y subsidios                     │  │
│  │ • Tarifas y beneficios de Comfama                            │  │
│  │ • Servicios de caja de compensación                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Alias ID: BRUXPV975I                                               │
│  Memory: No configurado (stateless)                                 │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔧 Componentes Detallados

### 1. Frontend (React + Vite)

**Ubicación**: `frontend/`

**Componentes Principales**:
```
frontend/
├── src/
│   ├── components/
│   │   ├── Chat/
│   │   │   ├── ChatWidget.jsx          # Chat principal
│   │   │   └── ChatWidget.css
│   │   ├── FAQ/
│   │   │   ├── FAQCard.jsx             # Tarjetas FAQ
│   │   │   ├── FAQQuickActions.jsx     # Acciones rápidas
│   │   │   ├── FAQRelatedQuestions.jsx # Preguntas relacionadas
│   │   │   └── FAQFeedback.jsx         # Feedback usuario
│   │   ├── Logo/
│   │   │   └── ComfiAvatar.jsx         # Avatar superhéroe
│   │   └── Layout/
│   │       ├── Layout.jsx              # Layout principal
│   │       └── Layout.css
│   ├── context/
│   │   └── WebSocketContext.jsx        # Gestión WebSocket
│   ├── data/
│   │   └── faqData.js                  # 5 FAQs de Comfama
│   └── pages/
│       ├── Home.jsx                    # Página principal
│       ├── Marketplace.jsx             # Marketplace (legacy)
│       └── Transactions.jsx            # Transacciones (legacy)
└── .env.production
    └── VITE_WEBSOCKET_URL=wss://vvg621xawg...
```

**Características**:
- React 18 con Vite
- WebSocket para comunicación en tiempo real
- Streaming de respuestas del agente
- Avatar animado con 10 estados
- Componentes FAQ integrados
- Tema Comfama (rosa #e6007e)

### 2. Backend Lambda Functions

#### Lambda: centli-app-connect
**Código**: `src_aws/app_connect/app_connect.py`

**Función**: Maneja conexiones WebSocket
- Valida token (opcional en modo demo)
- Crea sesión en DynamoDB
- Genera session_id único
- Retorna 200 (success) o 401/403 (auth failure)

**Modo Demo**: Permite conexiones sin token usando `user_id = 'demo-user-comfi'`

#### Lambda: centli-app-message
**Código**: `src_aws/app_message/app_message.py`

**Función**: Procesa mensajes del usuario
- Recibe mensaje del WebSocket
- Obtiene sesión de DynamoDB
- Invoca Bedrock Agent con `invoke_agent()`
- Transmite respuesta streaming al usuario
- Actualiza contador de mensajes

**Handler**: `app_message.lambda_handler`

**Variables de Entorno**:
```json
{
  "AGENTCORE_ID": "Z6PCEKYNPS",
  "AGENTCORE_ALIAS_ID": "BRUXPV975I",
  "SESSIONS_TABLE": "centli-sessions",
  "EVENT_BUS_NAME": "centli-event-bus",
  "ASSETS_BUCKET": "centli-assets-777937796305",
  "LOG_LEVEL": "INFO",
  "AWS_ACCOUNT_ID": "777937796305"
}
```

#### Lambda: centli-app-disconnect
**Código**: `src_aws/app_disconnect/app_disconnect.py`

**Función**: Limpia sesiones al desconectar
- Marca sesión como CLOSED en DynamoDB
- Limpia recursos asociados

### 3. Bedrock Agent (AgentCore)

**Agent ID**: Z6PCEKYNPS  
**Nombre**: centli-agentcore  
**Modelo**: Claude 3.5 Sonnet v2  
**Región**: us-east-1

**Configuración**:
- Foundation Model: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- Alias: BRUXPV975I
- Status: PREPARED
- Memory: No configurado (stateless)
- Action Groups: No configurados
- Knowledge Bases: No configuradas

**System Prompt**: Ver sección "System Prompt" arriba

### 4. DynamoDB Tables

#### Tabla: centli-sessions
**Función**: Almacena sesiones WebSocket activas

**Schema**:
```
{
  "session_id": "session_1710318000_demo-user-comfi",  // PK
  "user_id": "demo-user-comfi",
  "connection_id": "aKDBTcxtoAMCJig=",
  "state": "ACTIVE",                                    // ACTIVE | CLOSED
  "created_at": 1710318000,                            // Unix timestamp
  "expires_at": 1710332400,                            // +4 horas
  "last_activity": 1710318000,
  "message_count": 5,
  "user_preferences": {
    "language": "es-MX",
    "voice_gender": "neutral",
    "voice_speed": "normal"
  }
}
```

**TTL**: 4 horas desde creación

### 5. Otros Componentes (Legacy - No Usados Actualmente)

Estos componentes existen pero NO están siendo usados en la implementación actual de Comfi:

#### src_aws/app_inference/
- `bedrock_config.py` - Código con FAQ tools y validador de identidad
- `action_tools.py` - Implementación de FAQs
- `identity_validator.py` - Validador de identidad
- **Estado**: NO desplegado, código legacy

#### Action Groups Lambdas
- `centli-core-banking-*` (balance, transactions, transfer)
- `centli-crm-*` (beneficiaries, alias)
- `centli-marketplace-*` (catalog, purchase, benefits)
- **Estado**: Desplegadas pero NO conectadas al AgentCore actual

#### EventBridge
- Event Bus: `centli-event-bus`
- **Estado**: Configurado pero NO usado

## 🔄 Flujo de Datos Completo

### Flujo de Mensaje Usuario → Respuesta

```
1. Usuario escribe mensaje en ChatWidget
   ↓
2. WebSocketContext.sendMessage()
   - Payload: {action: "sendMessage", data: {message, user_id, session_id}}
   ↓
3. WebSocket envía a API Gateway (vvg621xawg)
   ↓
4. API Gateway route $default → Lambda centli-app-message
   ↓
5. Lambda centli-app-message:
   - Obtiene sesión de DynamoDB
   - Invoca Bedrock Agent con invoke_agent()
   ↓
6. Bedrock Agent (Z6PCEKYNPS):
   - Procesa mensaje con Claude 3.5 Sonnet
   - Aplica system prompt (identidad Comfi)
   - Genera respuesta
   ↓
7. Lambda recibe respuesta streaming del Agent
   ↓
8. Lambda transmite chunks al WebSocket
   - apigateway.post_to_connection()
   ↓
9. WebSocket envía chunks al frontend
   ↓
10. WebSocketContext.onmessage():
    - Acumula chunks en currentStreamMessage
    - Actualiza UI en tiempo real
    ↓
11. ChatWidget muestra respuesta streaming
    - Efecto de escritura en tiempo real
```

## 📦 Recursos AWS

### Cuenta AWS
- **Account ID**: 777937796305
- **Nombre**: pra_hackaton_agentic_mexico
- **Región**: us-east-1

### Recursos Principales
```
CloudFront:
  - Distribution: E2UWNXJTS2NM3V
  - URL: https://db4aulosarsdo.cloudfront.net

S3:
  - Bucket: comfi-frontend-pragma
  - Región: us-east-1

API Gateway:
  - API ID: vvg621xawg
  - Type: WebSocket
  - Stage: prod
  - URL: wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod

Lambda Functions:
  - centli-app-connect (Python 3.11)
  - centli-app-message (Python 3.11)
  - centli-app-disconnect (Python 3.11)

DynamoDB:
  - centli-sessions

Bedrock:
  - Agent: Z6PCEKYNPS (centli-agentcore)
  - Model: Claude 3.5 Sonnet v2
```

## 🔐 Seguridad y Permisos

### IAM Roles
- Lambda Execution Roles con permisos para:
  - DynamoDB (read/write en centli-sessions)
  - Bedrock Agent (invoke_agent)
  - API Gateway Management (post_to_connection)
  - CloudWatch Logs

### Autenticación
- **Modo Actual**: Demo (sin autenticación)
- **Producción**: Requiere JWT token en query params

## 📊 Métricas y Monitoreo

### CloudWatch Log Groups
```
/aws/lambda/centli-app-connect
/aws/lambda/centli-app-message
/aws/lambda/centli-app-disconnect
```

### Comandos de Monitoreo
```bash
# Ver logs en tiempo real
aws logs tail /aws/lambda/centli-app-message --follow

# Ver métricas de API Gateway
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiId,Value=vvg621xawg

# Ver estado del Bedrock Agent
aws bedrock-agent get-agent --agent-id Z6PCEKYNPS
```

## 🚀 Deployment

### Frontend
```bash
cd frontend
npm run build
aws s3 sync dist/ s3://comfi-frontend-pragma/ --delete
aws cloudfront create-invalidation --distribution-id E2UWNXJTS2NM3V --paths "/*"
```

### Backend Lambdas
```bash
# app-connect
cd src_aws/app_connect
zip -r app_connect.zip .
aws lambda update-function-code --function-name centli-app-connect --zip-file fileb://app_connect.zip

# app-message
cd src_aws/app_message
zip -r app_message.zip .
aws lambda update-function-code --function-name centli-app-message --zip-file fileb://app_message.zip
```

### Bedrock Agent
```bash
./scripts/update-agentcore-final.sh
```

## 📝 Notas Importantes

1. **Código de app_inference NO se usa**: El código con FAQs y validador en `src_aws/app_inference/` NO está desplegado. El sistema usa `app_message` que invoca el Bedrock Agent directamente.

2. **Action Groups no conectados**: Las Lambdas de Action Groups existen pero NO están configuradas en el Bedrock Agent actual.

3. **Modo Demo**: El sistema permite conexiones sin autenticación para facilitar pruebas.

4. **Stateless**: El Bedrock Agent no tiene memoria configurada, cada conversación es independiente.

5. **FAQs en Frontend**: Los FAQs están implementados en el frontend (`faqData.js`) pero el agente responde basándose en su system prompt, no en tools específicos.

---

**Última actualización**: 13 de marzo de 2026  
**Versión**: 1.0 (Post-corrección de identidad)
