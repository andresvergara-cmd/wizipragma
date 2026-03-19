# Comfi - Asistente Virtual Inteligente de Comfama

Asistente conversacional con IA para Comfama (Caja de Compensación Familiar de Antioquia, Colombia). Permite consultar información sobre servicios de Comfama mediante texto y voz, usando AWS Bedrock y arquitectura serverless.

[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![Claude 3.5](https://img.shields.io/badge/Claude-3.5%20Sonnet%20v2-8A2BE2)](https://www.anthropic.com/claude)
[![React 18](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev/)
[![Serverless](https://img.shields.io/badge/Architecture-Serverless-green)](https://aws.amazon.com/serverless/)

---

## Demo en Vivo

**URL**: https://db4aulosarsdo.cloudfront.net

---

## Qué puede hacer Comfi

| Capacidad | Ejemplo | Tecnología |
|-----------|---------|------------|
| FAQ Comfama | "¿Cómo me afilio?" | Knowledge Base (RAG) |
| Voz bidireccional | Hablar y escuchar respuestas | Transcribe Streaming + Polly |
| Respuestas en streaming | Texto en tiempo real | Bedrock Agent + WebSocket |
| Markdown enriquecido | Listas, negritas, enlaces | React Markdown renderer |

Categorías de FAQ soportadas: afiliación, certificados, cuenta digital, subsidios, créditos, educación y atención al cliente (43 preguntas).

---

## Arquitectura

```
Usuario (Web/Móvil)
       │
       ▼
CloudFront ──► S3 (React Frontend)
       │
       ▼ WebSocket (WSS)
API Gateway ──► Lambda centli-app-connect    → DynamoDB (sesiones)
            ──► Lambda centli-app-disconnect → DynamoDB
            ──► Lambda centli-app-message    → Bedrock Agent (Claude 3.5 Sonnet v2)
                    │                              │
                    ├── Transcribe Streaming (STT)  ├── Knowledge Base (FAQ Comfama)
                    └── Polly Neural (TTS)          └── OpenSearch Serverless
```

### Servicios AWS

| Servicio | Uso |
|----------|-----|
| Amazon Bedrock Agent | Agente conversacional (Claude 3.5 Sonnet v2) |
| Bedrock Knowledge Base | RAG con FAQ de Comfama (43 preguntas) |
| Amazon Transcribe Streaming | Speech-to-Text en tiempo real (~2-4s) |
| Amazon Polly (Neural) | Text-to-Speech (voz Mia, es-MX, MP3 24kHz) |
| API Gateway WebSocket | Comunicación bidireccional en tiempo real |
| AWS Lambda (3 funciones) | Connect, Disconnect, Message |
| Amazon DynamoDB | Gestión de sesiones |
| Amazon S3 | Frontend, documentos KB, audio temporal |
| Amazon CloudFront | CDN para frontend |
| Amazon OpenSearch Serverless | Almacenamiento vectorial para embeddings |

---

## Estructura del Proyecto

```
├── src_aws/
│   ├── app_message/          # Lambda principal (orquestador de mensajes)
│   │   ├── app_message.py    # Handler: texto, voz, imagen
│   │   ├── transcribe_stt.py # Transcribe Streaming STT
│   │   ├── polly_tts.py      # Polly Neural TTS
│   │   └── amazon_transcribe/ # SDK de Transcribe Streaming
│   ├── app_connect/          # Lambda de conexión WebSocket
│   ├── app_disconnect/       # Lambda de desconexión
│   ├── app_inference/        # Código legacy (NO usado en producción)
│   └── [action groups]/      # Lambdas de Action Groups (mock)
│
├── frontend/                 # React 18 + Vite
│   ├── src/
│   │   ├── components/       # Chat, FAQ, Layout, Logo, Product
│   │   ├── context/          # WebSocketContext, ChatContext
│   │   ├── pages/            # Home, Marketplace, ProductDetail, Transactions
│   │   └── data/             # FAQ data, mock products
│   └── .env.production
│
├── tests/                    # Tests unitarios
├── docs/                     # Documentación técnica
├── scripts/                  # Scripts de deployment y testing
└── knowledge-base-docs/      # Documentos fuente para Knowledge Base
```

> **IMPORTANTE**: `src_aws/app_inference/` es código legacy del prototipo original. La Lambda de producción (`centli-app-message`) usa el código de `src_aws/app_message/`. Nunca desplegar `app_inference` a producción.

---

## Inicio Rápido

### Prerrequisitos

- Node.js 18+
- Python 3.10+
- AWS CLI configurado con credenciales válidas

### Frontend (desarrollo local)

```bash
cd frontend
npm install
npm run dev
```

### Build y Deploy

```bash
# Build frontend
cd frontend && npm run build

# Deploy a S3
aws s3 sync dist/ s3://comfi-frontend-pragma/ --delete

# Invalidar CloudFront
aws cloudfront create-invalidation --distribution-id E2UWNXJTS2NM3V --paths "/*"
```

### Deploy Lambda (app_message)

```bash
cd src_aws/app_message
zip -r function.zip app_message.py transcribe_stt.py polly_tts.py amazon_transcribe/
aws lambda update-function-code --function-name centli-app-message --zip-file fileb://function.zip
```

---

## Testing

```bash
# Tests unitarios
cd tests
python -m pytest unit/ -v

# Test E2E de voz
python scripts/test_voice_complete.py
```

---

## Pipeline de Voz

El flujo de voz bidireccional funciona así:

1. **Captura**: `AudioContext` → `MediaStreamDestination` → `MediaRecorder` (WebM/Opus, 32kbps)
2. **Envío**: Base64 → WebSocket → Lambda
3. **STT**: ffmpeg (WebM→WAV 16kHz) → Transcribe Streaming API (~2-4s)
4. **Agente**: Texto → Bedrock Agent → Respuesta
5. **TTS**: Polly Neural (Mia, es-MX) → MP3 → chunks base64 → WebSocket → Frontend
6. **Reproducción**: Audio element en el navegador

---

## Documentación

- [Arquitectura detallada](docs/ARQUITECTURA-COMFI.md) - Diagrama completo, componentes y flujos
- [Deployment](docs/DEPLOYMENT.md) - Guía de despliegue
- [Quick Start](docs/QUICK-START.md) - Guía rápida para desarrolladores

---

## Recursos AWS

| Recurso | Identificador |
|---------|---------------|
| Región | us-east-1 |
| CloudFront | E2UWNXJTS2NM3V (`db4aulosarsdo.cloudfront.net`) |
| WebSocket API | vvg621xawg |
| Lambda Message | centli-app-message (512MB, 45s timeout) |
| Bedrock Agent | Z6PCEKYNPS (alias TSTALIASID) |
| Knowledge Base | PDNW6DDDGZ |
| DynamoDB | centli-sessions |
| S3 Frontend | comfi-frontend-pragma |
| S3 Knowledge Base | comfi-knowledge-base-pragma |
| Lambda Layer | nova-sonic-dependencies:1 (ffmpeg + pydub) |

---

## Equipo

Desarrollado por el equipo Pragma para el hackathon AWS.

## Licencia

MIT
