# Quick Start - Comfi

Guía rápida para desarrolladores que se unen al proyecto.

---

## Lo Esencial

- **Demo**: https://db4aulosarsdo.cloudfront.net
- **WebSocket**: wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
- **Lambda principal**: `centli-app-message`
- **Región**: us-east-1

---

## Setup en 5 Minutos

### 1. Clonar

```bash
git clone <repo-url>
cd comfi
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# Abre http://localhost:5173
```

### 3. Probar

Abre la demo en https://db4aulosarsdo.cloudfront.net y prueba:
- Texto: "¿Cómo me afilio a Comfama?"
- Voz: Click en 🎤, habla, click para detener

---

## Estructura Clave

```
src_aws/app_message/        # Lambda de producción (orquestador)
├── app_message.py          # Handler: TEXT, AUDIO
├── transcribe_stt.py       # Transcribe Streaming STT
├── polly_tts.py            # Polly Neural TTS
└── amazon_transcribe/      # SDK Transcribe Streaming

src_aws/app_connect/        # Lambda $connect
src_aws/app_disconnect/     # Lambda $disconnect

frontend/src/
├── components/Chat/        # ChatWidget, MarkdownMessage
├── context/                # WebSocketContext, ChatContext
├── pages/                  # Home, Marketplace
└── data/                   # faqData, mockProducts
```

> `src_aws/app_inference/` es código legacy. NO usar en producción.

---

## Comandos de Deploy

### Frontend

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://comfi-frontend-pragma/ --delete
aws cloudfront create-invalidation --distribution-id E2UWNXJTS2NM3V --paths "/*"
```

### Lambda app_message

```bash
cd src_aws/app_message
zip -r function.zip app_message.py transcribe_stt.py polly_tts.py amazon_transcribe/
aws lambda update-function-code --function-name centli-app-message --zip-file fileb://function.zip
```

---

## Tests

```bash
# Unitarios
python -m pytest tests/unit/ -v

# E2E voz (requiere credenciales AWS)
python scripts/test_voice_complete.py
```

---

## Flujos Principales

### Texto
```
Usuario escribe → WebSocket → Lambda → Bedrock Agent (streaming) → chunks → Frontend
```

### Voz
```
Usuario graba → WebM base64 → Lambda → ffmpeg → Transcribe Streaming (~2-4s)
→ Bedrock Agent → Polly TTS → MP3 chunks → Frontend reproduce
```

---

## Debugging

### Ver logs de Lambda

```bash
aws logs tail /aws/lambda/centli-app-message --follow --region us-east-1
```

### Audio no funciona

1. Verificar HTTPS (audio requiere contexto seguro)
2. Verificar permisos del micrófono en el navegador
3. Revisar consola del navegador: debe mostrar `🎤 Recording started (AudioContext → MediaRecorder...)`
4. El blob final debe ser > 500 bytes

### Respuestas vacías

1. Verificar que el WebSocket está conectado (indicador "En línea")
2. Revisar logs de Lambda en CloudWatch
3. Verificar que el Bedrock Agent está activo

---

## Documentación

- [README.md](../README.md) - Overview del proyecto
- [Arquitectura](ARQUITECTURA-COMFI.md) - Diagrama y componentes
- [Deployment](DEPLOYMENT.md) - Guía de despliegue
- [Contributing](../CONTRIBUTING.md) - Guía de contribución
