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
| Transferencias | "Envía $50.000 a mi mamá" | Tool Use |
| Compras | "Compra un plan de recreación" | Tool Use |
| Voz bidireccional | Hablar y escuchar respuestas | Transcribe + Polly |

Categorías de FAQ soportadas: afiliación, certificados, cuenta digital, subsidios, créditos, educación y atención al cliente (35 preguntas).

---

## Arquitectura

```
Usuario (Web/Móvil)
       │
       ▼
CloudFront ──► S3 (React Frontend)
       │
       ▼ WebSocket
API Gateway ──► Lambda app_connect    → DynamoDB (sesiones)
            ──► Lambda app_disconnect → DynamoDB
            ──► Lambda app_message    → Bedrock Agent (Claude 3.5 Sonnet v2)
                    │                        │
                    ├── Transcribe (STT)     ├── Knowledge Base (FAQ Comfama)
                    └── Polly (TTS)         └── OpenSearch Serverless
```

### Servicios AWS

| Servicio | Uso |
|----------|-----|
| Amazon Bedrock Agent | Agente conversacional (Claude 3.5 Sonnet v2) |
| Bedrock Knowledge Base | RAG con FAQ de Comfama (35 preguntas) |
| Amazon Transcribe | Speech-to-Text |
| Amazon Polly | Text-to-Speech (voz Mia, neural) |
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
│   ├── app_inference/        # Lambda principal (message handler)
│   │   ├── app.py            # Handler
│   │   ├── bedrock_config.py # Configuración Bedrock + Tool Use
│   │   ├── action_tools.py   # Tools: answer_faq, transfer_money, purchase_product
│   │   ├── audio_processor.py # Transcribe STT + Polly TTS
│   │   └── identity_validator.py # Validación de identidad Comfi
│   ├── app_connect/          # Lambda de conexión WebSocket
│   └── app_disconnect/       # Lambda de desconexión
│
├── frontend/                 # React 18 + Vite
│   ├── src/
│   │   ├── components/       # ChatWidget, Layout, Logo, ProductCard
│   │   ├── context/          # WebSocketContext, ChatContext
│   │   ├── pages/            # Home, Marketplace, ProductDetail, Transactions
│   │   └── data/             # Mock data
│   └── .env.production
│
├── tests/                    # Tests unitarios e integración
├── docs/                     # Documentación técnica detallada
├── scripts/                  # Scripts de deployment
├── knowledge-base-docs/      # Documentos fuente para Knowledge Base
└── infrastructure/           # Templates SAM/CloudFormation
```

---

## Inicio Rápido

### Prerrequisitos

- Node.js 18+
- Python 3.10+
- AWS CLI configurado con acceso a Bedrock

### Backend

```bash
cd src_aws/app_inference
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Deployment

Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para instrucciones completas.

---

## Testing

```bash
# Tests unitarios
cd tests
pytest unit/ -v

# Tests de integración
pytest integration/ -v
```

---

## Documentación

- [Arquitectura detallada](docs/ARQUITECTURA-COMFI.md) - Diagrama completo y componentes
- [Deployment](docs/DEPLOYMENT.md) - Guía de despliegue
- [Quick Start](docs/QUICK-START.md) - Guía rápida para desarrolladores

---

## Origen del Proyecto

Este proyecto evolucionó desde Wizi Plus, un coach financiero conversacional desarrollado como prototipo. La versión actual fue adaptada para Comfama como demo de asistente virtual inteligente con capacidades de voz y RAG. La documentación del diseño original se encuentra en `aidlc-docs/` y los archivos de trabajo del proceso de desarrollo en `archive/`.

---

## Equipo

Desarrollado por el equipo Pragma para el hackathon AWS.

---

## Licencia

MIT
