# Arquitectura de la Demo Comfi - Comfama

## 1. Visión General

Comfi es un asistente virtual inteligente desarrollado para Comfama (Caja de Compensación Familiar de Antioquia, Colombia). Permite a los usuarios interactuar mediante texto y voz para consultar información sobre servicios de Comfama: afiliación, créditos, subsidios, educación, recreación y atención al cliente.

La solución implementa una arquitectura serverless en AWS con comunicación bidireccional en tiempo real vía WebSocket, procesamiento de lenguaje natural con Amazon Bedrock, y capacidades de voz bidireccional con Amazon Transcribe (STT) y Amazon Polly (TTS).

## 2. Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USUARIO FINAL                                │
│                    (Navegador Web / Móvil)                              │
└──────────────────────────┬──────────────────────────────────────────────┘
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Amazon CloudFront                                   │
│              CDN - Distribución Frontend                                │
│           db4aulosarsdo.cloudfront.net                                  │
└──────────────────────────┬──────────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌──────────────────────┐   ┌──────────────────────────────────────────────┐
│    Amazon S3         │   │        API Gateway WebSocket                 │
│  Frontend Assets     │   │  wss://vvg621xawg.execute-api.              │
│  (React Build)       │   │  us-east-1.amazonaws.com/prod               │
│                      │   │                                              │
│  comfi-frontend-     │   │  Rutas:                                      │
│  pragma              │   │  ├── $connect    → Lambda app_connect        │
└──────────────────────┘   │  ├── $disconnect → Lambda app_disconnect     │
                           │  └── $default    → Lambda app_message        │
                           └──────────┬───────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                  ▼
          ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
          │ Lambda       │  │ Lambda       │  │ Lambda           │
          │ app_connect  │  │ app_disconnect│  │ app_message     │
          │              │  │              │  │ (Orquestador)    │
          │ Crea sesión  │  │ Limpia       │  │                  │
          │ en DynamoDB  │  │ sesión       │  │ Enruta mensajes: │
          └──────┬───────┘  └──────┬───────┘  │ TEXT / VOICE /   │
                 │                 │          │ IMAGE            │
                 ▼                 ▼          └────────┬─────────┘
          ┌──────────────────────────────┐             │
          │       Amazon DynamoDB        │             │
          │    centli-sessions           │    ┌────────┴─────────┐
          │                              │    │                  │
          │  Campos:                     │    ▼                  ▼
          │  - session_id                │  [TEXT]            [VOICE]
          │  - connection_id             │    │                  │
          │  - user_id                   │    │         ┌────────┴────────┐
          │  - state (ACTIVE/DISCONNECTED)│   │         ▼                ▼
          │  - message_count             │    │  ┌─────────────┐  ┌───────────┐
          │  - expires_at (4h TTL)       │    │  │  Amazon     │  │  Amazon   │
          └──────────────────────────────┘    │  │  Transcribe │  │  Polly    │
                                              │  │  (STT)      │  │  (TTS)    │
                                              │  │             │  │           │
                                              │  │ Audio→Texto │  │ Texto→Voz │
                                              │  │ es-ES       │  │ Voz: Mia  │
                                              │  │ WebM input  │  │ es-MX     │
                                              │  └──────┬──────┘  │ Neural    │
                                              │         │         │ MP3 24kHz │
                                              │         ▼         └─────┬─────┘
                                              │    Texto extraído       │
                                              │         │               │
                                              ▼         ▼               │
                                    ┌─────────────────────────┐         │
                                    │   Amazon Bedrock Agent  │         │
                                    │   ID: Z6PCEKYNPS        │         │
                                    │                         │         │
                                    │   Modelo: Claude 3.5    │         │
                                    │   Sonnet v2             │         │
                                    │                         │         │
                                    │   System Prompt:        │         │
                                    │   Identidad Comfi       │         │
                                    │   (Comfama, Colombia)   │         │
                                    └────────┬────────────────┘         │
                                             │                          │
                                    ┌────────┴────────┐                 │
                                    ▼                 ▼                 │
                          ┌──────────────┐  ┌──────────────────┐        │
                          │  Knowledge   │  │  Respuesta       │        │
                          │  Base        │  │  Texto           │────────┘
                          │  PDNW6DDDGZ  │  │  (Streaming)    │
                          │              │  └──────────────────┘
                          │  FAQ Comfama │
                          │  (35 preguntas)│
                          └──────┬───────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
          ┌──────────────────┐    ┌──────────────────────┐
          │   Amazon S3      │    │  Amazon OpenSearch    │
          │   comfi-         │    │  Serverless           │
          │   knowledge-     │    │                       │
          │   base-pragma    │    │  Índice vectorial     │
          │                  │    │  Embeddings:          │
          │   Documento:     │    │  Titan Embed Text v2  │
          │   FAQ_Comfama_   │    │                       │
          │   Centro_        │    └──────────────────────┘
          │   Conocimiento   │
          │   .docx          │
          └──────────────────┘
```

## 3. Componentes del Sistema

### 3.1 Frontend (React 18 + Vite)

| Aspecto | Detalle |
|---------|---------|
| Framework | React 18 con Vite |
| Hosting | Amazon S3 + CloudFront |
| URL | https://db4aulosarsdo.cloudfront.net |
| Comunicación | WebSocket bidireccional |
| Modalidades | Texto, Voz (MediaRecorder API), Imágenes |

Componentes principales:
- `WebSocketContext.jsx`: Gestión de conexión WebSocket, streaming de mensajes, ensamblaje de audio chunks
- `ChatWidget.jsx`: Interfaz de chat con soporte multimodal
- `CinteotlLogo.jsx`: Avatar animado de Comfi (estados: hablando, pensando, saludando)

Funcionalidades del frontend:
- Streaming de respuestas en tiempo real
- Grabación de audio con MediaRecorder API (formato WebM)
- Reproducción de audio TTS (MP3) con soporte de chunks
- Auto-reconexión WebSocket (máximo 5 intentos, 3s entre intentos)
- Indicadores de "escribiendo" y procesamiento

### 3.2 API Gateway WebSocket

| Aspecto | Detalle |
|---------|---------|
| Tipo | WebSocket API |
| Endpoint | wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod |
| Stage | prod |
| Región | us-east-1 |

Rutas configuradas:
| Ruta | Lambda | Función |
|------|--------|---------|
| `$connect` | `centli-app-connect` | Crear sesión en DynamoDB |
| `$disconnect` | `centli-app-disconnect` | Marcar sesión como DISCONNECTED |
| `$default` | `centli-app-message` | Procesar mensajes (texto/voz/imagen) |

### 3.3 Lambda Functions

#### centli-app-connect
- Handler: `app_connect.lambda_handler`
- Función: Crea sesión en DynamoDB al conectarse un usuario
- Modo demo: Asigna `user_id: demo-user-comfi` sin autenticación
- TTL de sesión: 4 horas

#### centli-app-disconnect
- Handler: `app_disconnect.lambda_handler`
- Función: Marca la sesión como `DISCONNECTED` en DynamoDB

#### centli-app-message (Orquestador Principal)
- Handler: `app_message.lambda_handler`
- Runtime: Python 3.11
- Memoria: 512 MB
- Timeout: 30 segundos
- Función: Enruta mensajes según tipo:
  - `TEXT` → Bedrock Agent con streaming
  - `VOICE/AUDIO` → Transcribe STT → Bedrock Agent → Polly TTS
  - `IMAGE` → Placeholder (no implementado)

### 3.4 Amazon Bedrock Agent

| Aspecto | Detalle |
|---------|---------|
| Agent ID | Z6PCEKYNPS |
| Alias | TSTALIASID |
| Modelo | us.anthropic.claude-3-5-sonnet-20241022-v2:0 |
| Rol IAM | CentliBedrockAgentRole |
| Idle TTL | 600 segundos |
| Orquestación | DEFAULT |

El agente tiene configurado un system prompt extenso que define:
- Identidad: Comfi, asistente de Comfama
- Ubicación: Antioquia, Colombia
- Moneda: Pesos Colombianos (COP)
- Servicios: Afiliación, créditos, subsidios, educación, recreación, salud, cultura
- Información de contacto: (604) 360 70 80 / 018000 415 455 / www.comfama.com

### 3.5 Knowledge Base (RAG)

| Aspecto | Detalle |
|---------|---------|
| KB ID | PDNW6DDDGZ |
| Nombre | comfi-knowledge-base |
| Tipo | VECTOR |
| Embedding | Amazon Titan Embed Text v2 |
| Storage | OpenSearch Serverless |
| Fuente | S3: comfi-knowledge-base-pragma |
| Rol IAM | ComfiKnowledgeBaseRole |

Documento fuente: `FAQ_Comfama_Centro_Conocimiento.docx` (38 KB)

Categorías del FAQ (35 preguntas):
| Categoría | Preguntas | Temas |
|-----------|-----------|-------|
| Afiliación | 8 | Cómo afiliarse, beneficiarios, pensionados, beneficios |
| Certificados | 3 | Certificado de afiliación, carné, certificados financieros |
| Cuenta digital | 4 | Crear cuenta, actualizar datos, problemas de sesión |
| Subsidios | 9 | Subsidio al desempleo, requisitos, documentos, postulación |
| Créditos | 3 | Cuota monetaria, requisitos, servicios financieros |
| Educación | 3 | Inscripción a cursos, programas educativos |
| Atención | 5 | Canales de contacto, teléfono, PQR, correo |

### 3.6 Amazon Transcribe (STT)

| Aspecto | Detalle |
|---------|---------|
| Idioma | es-ES (Español) |
| Formato entrada | WebM (desde navegador) |
| Almacenamiento temporal | S3: centli-assets-777937796305 |
| Polling | Backoff exponencial (0.3s → 1.5s, máx 40 intentos) |

Flujo STT:
1. Audio base64 del frontend → Decodificar a bytes
2. Subir WebM a S3 (temporal)
3. Iniciar TranscriptionJob
4. Polling hasta completar
5. Extraer texto transcrito
6. Limpiar archivos temporales

### 3.7 Amazon Polly (TTS)

| Aspecto | Detalle |
|---------|---------|
| Voz | Mia (Neural) |
| Idioma | es-MX (Español México) |
| Engine | Neural |
| Formato salida | MP3 |
| Sample Rate | 24 kHz |
| Límite texto | 3000 caracteres |

Flujo TTS:
1. Texto de respuesta del agente
2. Polly sintetiza a MP3
3. Codificar a base64
4. Si > 100KB: dividir en chunks
5. Enviar por WebSocket al frontend

### 3.8 Amazon DynamoDB

Tabla principal: `centli-sessions`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| session_id | String (PK) | ID único de sesión |
| connection_id | String | ID de conexión WebSocket |
| user_id | String | ID del usuario |
| state | String | ACTIVE / DISCONNECTED |
| created_at | Number | Timestamp de creación |
| expires_at | Number | Timestamp de expiración (4h) |
| last_activity | Number | Última actividad |
| message_count | Number | Contador de mensajes |

### 3.9 Amazon S3

| Bucket | Uso |
|--------|-----|
| comfi-knowledge-base-pragma | Documentos FAQ para Knowledge Base |
| centli-assets-777937796305 | Audio temporal para Transcribe |
| Frontend bucket | Build de React para CloudFront |

## 4. Flujos de Datos

### 4.1 Flujo de Texto

```
Usuario escribe mensaje
    │
    ▼
Frontend (WebSocket) ──────► API Gateway ──────► Lambda app_message
                                                      │
                                                      ▼
                                                Bedrock Agent
                                                (Claude 3.5 Sonnet)
                                                      │
                                              ┌───────┴───────┐
                                              ▼               ▼
                                        Knowledge Base    Respuesta
                                        (si es FAQ)       directa
                                              │               │
                                              └───────┬───────┘
                                                      ▼
                                              Streaming chunks
                                                      │
                                                      ▼
Usuario ve respuesta ◄──── Frontend ◄──── WebSocket ◄─┘
(en tiempo real)
```

### 4.2 Flujo de Voz (Bidireccional)

```
Usuario graba audio (WebM)
    │
    ▼
Frontend codifica base64 ──► API Gateway ──► Lambda app_message
                                                   │
                                                   ▼
                                            Amazon Transcribe
                                            (Audio → Texto)
                                                   │
                                                   ▼
                                            Bedrock Agent
                                            (Texto → Respuesta)
                                                   │
                                                   ▼
                                            Amazon Polly
                                            (Respuesta → Audio MP3)
                                                   │
                                                   ▼
                                            Base64 chunks
                                                   │
                                                   ▼
Usuario escucha respuesta ◄── Frontend ◄── WebSocket
(audio MP3)
```

## 5. Servicios AWS Utilizados

| Servicio | Uso en Comfi |
|----------|-------------|
| Amazon CloudFront | CDN para frontend React |
| Amazon S3 | Hosting frontend, documentos KB, audio temporal |
| API Gateway (WebSocket) | Comunicación bidireccional en tiempo real |
| AWS Lambda (3 funciones) | Lógica serverless (connect, disconnect, message) |
| Amazon Bedrock Agent | Agente conversacional con Claude 3.5 Sonnet v2 |
| Bedrock Knowledge Base | RAG con FAQ de Comfama |
| Amazon OpenSearch Serverless | Almacenamiento vectorial para embeddings |
| Amazon Titan Embed Text v2 | Modelo de embeddings para Knowledge Base |
| Amazon DynamoDB | Gestión de sesiones |
| Amazon Transcribe | Speech-to-Text (voz del usuario → texto) |
| Amazon Polly | Text-to-Speech (respuesta → voz neural) |
| AWS IAM | Roles y permisos de seguridad |

## 6. Seguridad

- Comunicación HTTPS/WSS en todos los canales
- Sesiones con TTL de 4 horas
- Roles IAM con permisos mínimos necesarios:
  - `CentliBedrockAgentRole`: InvokeModel, Retrieve KB, acceso OpenSearch
  - `ComfiKnowledgeBaseRole`: S3 GetObject, InvokeModel, acceso OpenSearch
  - `CentliLambdaExecutionRole`: DynamoDB, Bedrock, Transcribe, Polly, S3
- Validación de identidad del agente (identity_validator.py)
- Audio temporal en S3 con limpieza automática post-transcripción

## 7. Región y Cuenta AWS

| Aspecto | Valor |
|---------|-------|
| Región | us-east-1 (N. Virginia) |
| Cuenta AWS | 777937796305 |
