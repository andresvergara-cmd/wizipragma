# Arquitectura de Comfi - Asistente Virtual de Comfama

## 1. Visión General

Comfi es un asistente virtual inteligente para Comfama (Caja de Compensación Familiar de Antioquia, Colombia). Permite interactuar mediante texto y voz para consultar información sobre servicios: afiliación, créditos, subsidios, educación, recreación y atención al cliente.

Arquitectura serverless en AWS con WebSocket bidireccional, Amazon Bedrock (Claude 3.5 Sonnet v2), Transcribe Streaming para STT y Polly Neural para TTS.

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
│              CDN - Distribución E2UWNXJTS2NM3V                         │
│           db4aulosarsdo.cloudfront.net                                  │
└──────────────────────────┬──────────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌──────────────────────┐   ┌──────────────────────────────────────────────┐
│    Amazon S3         │   │        API Gateway WebSocket                 │
│  comfi-frontend-     │   │  wss://vvg621xawg.execute-api.              │
│  pragma              │   │  us-east-1.amazonaws.com/prod               │
│  (React Build)       │   │                                              │
└──────────────────────┘   │  Rutas:                                      │
                           │  ├── $connect    → centli-app-connect        │
                           │  ├── $disconnect → centli-app-disconnect     │
                           │  └── $default    → centli-app-message        │
                           └──────────┬───────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                  ▼
          ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
          │ Lambda       │  │ Lambda       │  │ Lambda           │
          │ app_connect  │  │ app_disconnect│ │ app_message     │
          │              │  │              │  │ (512MB, 45s)     │
          │ Crea sesión  │  │ Limpia       │  │                  │
          │ en DynamoDB  │  │ sesión       │  │ Enruta mensajes: │
          └──────┬───────┘  └──────┬───────┘  │ TEXT / AUDIO     │
                 │                 │          └────────┬─────────┘
                 ▼                 ▼                   │
          ┌──────────────────────────────┐             │
          │       Amazon DynamoDB        │    ┌────────┴─────────┐
          │    centli-sessions           │    │                  │
          │  - session_id (PK)           │    ▼                  ▼
          │  - connection_id             │  [TEXT]            [AUDIO]
          │  - user_id                   │    │                  │
          │  - state                     │    │         ┌────────┴────────┐
          │  - expires_at (4h TTL)       │    │         ▼                ▼
          └──────────────────────────────┘    │  ┌─────────────┐  ┌───────────┐
                                              │  │ Transcribe  │  │  Polly    │
                                              │  │ Streaming   │  │  Neural   │
                                              │  │ (~2-4s)     │  │  (Mia)    │
                                              │  │ es-US       │  │  es-MX    │
                                              │  │ 16kHz PCM   │  │  MP3 24kHz│
                                              │  └──────┬──────┘  └─────┬─────┘
                                              │         ▼               │
                                              ▼    Texto extraído       │
                                    ┌─────────────────────────┐         │
                                    │   Amazon Bedrock Agent  │         │
                                    │   Z6PCEKYNPS            │         │
                                    │   Claude 3.5 Sonnet v2  │◄────────┘
                                    └────────┬────────────────┘
                                             │
                                    ┌────────┴────────┐
                                    ▼                 ▼
                          ┌──────────────┐  ┌──────────────────┐
                          │  Knowledge   │  │  Respuesta       │
                          │  Base        │  │  (Streaming o    │
                          │  PDNW6DDDGZ  │  │   directa)      │
                          │  43 FAQs     │  └──────────────────┘
                          └──────┬───────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
          ┌──────────────────┐    ┌──────────────────────┐
          │   Amazon S3      │    │  Amazon OpenSearch    │
          │   comfi-         │    │  Serverless           │
          │   knowledge-     │    │  Titan Embed Text v2  │
          │   base-pragma    │    └──────────────────────┘
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
| Modalidades | Texto y Voz |

Componentes principales:
- `WebSocketContext.jsx`: Conexión WebSocket, streaming, ensamblaje de audio chunks, auto-reconexión
- `ChatContext.jsx`: Estado del chat, envío de mensajes texto/voz, conversión blob→base64
- `ChatWidget.jsx`: Interfaz de chat con grabación de voz (AudioContext + MediaRecorder), markdown, sugerencias
- `MarkdownMessage.jsx`: Renderizado de respuestas con formato markdown
- `FAQQuickActions`: Accesos rápidos a preguntas frecuentes
- `ComfiAvatar`: Avatar animado (estados: hablando, pensando, saludando)

Captura de audio:
- `AudioContext.createMediaStreamSource()` captura el micrófono (100% confiable)
- Rutea a `MediaStreamDestination` → `MediaRecorder` (compresión Opus/WebM)
- `timeslice: 500ms`, `audioBitsPerSecond: 32000` para archivos pequeños
- Máximo 15 segundos de grabación (límite 128KB WebSocket)

### 3.2 API Gateway WebSocket

| Aspecto | Detalle |
|---------|---------|
| Endpoint | wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod |
| Route Selection | `$request.body.action` |
| Región | us-east-1 |

| Ruta | Lambda | Función |
|------|--------|---------|
| `$connect` | `centli-app-connect` | Crear sesión en DynamoDB |
| `$disconnect` | `centli-app-disconnect` | Marcar sesión DISCONNECTED |
| `$default` | `centli-app-message` | Procesar mensajes TEXT/AUDIO |

### 3.3 Lambda centli-app-message (Orquestador)

| Aspecto | Detalle |
|---------|---------|
| Runtime | Python 3.11 |
| Memoria | 512 MB |
| Timeout | 45 segundos |
| Layer | nova-sonic-dependencies:1 (ffmpeg + pydub) |
| Código fuente | `src_aws/app_message/` |

Flujo TEXT:
1. Recibe mensaje → Busca sesión en DynamoDB
2. Invoca Bedrock Agent con streaming
3. Envía chunks de texto al frontend vía `post_to_connection`

Flujo AUDIO:
1. Recibe base64 audio → Decodifica
2. ffmpeg convierte WebM→WAV (16kHz, mono)
3. Transcribe Streaming API (~2-4s) → texto
4. Envía transcripción al frontend
5. Invoca Bedrock Agent → respuesta texto
6. Envía respuesta texto al frontend
7. Polly Neural sintetiza MP3 → envía audio chunks

### 3.4 Amazon Transcribe Streaming (STT)

| Aspecto | Detalle |
|---------|---------|
| API | Transcribe Streaming (tiempo real) |
| Idioma | es-US |
| Formato entrada | PCM 16kHz mono 16-bit |
| SDK | amazon-transcribe (incluido en Lambda) |
| Latencia | ~2-4 segundos |
| Fallback | Batch Transcribe (si streaming falla) |

### 3.5 Amazon Polly (TTS)

| Aspecto | Detalle |
|---------|---------|
| Voz | Mia (Neural) |
| Idioma | es-MX |
| Formato | MP3, 24 kHz |
| Límite | 3000 caracteres |
| Chunking | Si > 100KB, divide en chunks para WebSocket |

### 3.6 Amazon Bedrock Agent

| Aspecto | Detalle |
|---------|---------|
| Agent ID | Z6PCEKYNPS |
| Alias | TSTALIASID |
| Modelo | us.anthropic.claude-3-5-sonnet-20241022-v2:0 |
| Knowledge Base | PDNW6DDDGZ (43 FAQs de Comfama) |
| Embedding | Amazon Titan Embed Text v2 |
| Vector Store | OpenSearch Serverless |

### 3.7 Amazon DynamoDB

Tabla: `centli-sessions`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| session_id | String (PK) | ID único de sesión |
| connection_id | String | ID de conexión WebSocket |
| user_id | String | ID del usuario |
| state | String | ACTIVE / DISCONNECTED |
| created_at | Number | Timestamp de creación |
| expires_at | Number | TTL (4 horas) |
| last_activity | Number | Última actividad |
| message_count | Number | Contador de mensajes |

### 3.8 Buckets S3

| Bucket | Uso |
|--------|-----|
| comfi-frontend-pragma | Build de React para CloudFront |
| comfi-knowledge-base-pragma | Documento FAQ para Knowledge Base |
| centli-assets-777937796305 | Audio temporal (fallback batch Transcribe) |

## 4. Flujos de Datos

### 4.1 Flujo de Texto

```
Usuario escribe → WebSocket → Lambda app_message
                                    │
                                    ▼
                              Bedrock Agent (streaming)
                              ├── Knowledge Base (si es FAQ)
                              └── Respuesta directa
                                    │
                                    ▼ chunks de texto
Usuario ve respuesta ◄── WebSocket ◄─┘
(en tiempo real)
```

### 4.2 Flujo de Voz

```
Usuario graba (AudioContext → MediaRecorder → WebM/Opus)
    │
    ▼ base64
Lambda app_message
    │
    ├── ffmpeg: WebM → WAV 16kHz mono
    ├── Transcribe Streaming: WAV → texto (~2-4s)
    ├── Envía transcripción al frontend
    ├── Bedrock Agent: texto → respuesta
    ├── Envía respuesta texto al frontend
    └── Polly Neural: respuesta → MP3 → chunks base64
                                          │
Usuario escucha ◄── WebSocket ◄───────────┘
```

## 5. Seguridad

- HTTPS/WSS en todos los canales
- Sesiones con TTL de 4 horas
- Roles IAM con permisos mínimos:
  - `CentliBedrockAgentRole`: InvokeModel, Retrieve KB, OpenSearch
  - `ComfiKnowledgeBaseRole`: S3 GetObject, InvokeModel, OpenSearch
  - `CentliLambdaExecutionRole`: DynamoDB, Bedrock, Transcribe, Polly, S3
- Audio temporal en S3 con limpieza post-transcripción

## 6. Región y Cuenta

| Aspecto | Valor |
|---------|-------|
| Región | us-east-1 |
| Cuenta | 777937796305 |
