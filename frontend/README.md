# Comfi Frontend

Frontend React para Comfi, el asistente virtual de Comfama.

## Stack

- React 18 + Vite
- WebSocket bidireccional
- AudioContext + MediaRecorder para captura de voz
- Markdown rendering para respuestas enriquecidas

## Estructura

```
src/
├── components/
│   ├── Chat/           # ChatWidget, MarkdownMessage
│   ├── FAQ/            # FAQQuickActions
│   ├── Layout/         # Header, navegación
│   ├── Logo/           # ComfiAvatar, CinteotlLogo
│   └── Product/        # ProductCard
├── context/
│   ├── WebSocketContext.jsx  # Conexión WS, streaming, audio
│   └── ChatContext.jsx       # Estado del chat, envío mensajes
├── pages/
│   ├── Home.jsx
│   ├── Marketplace.jsx
│   ├── ProductDetail.jsx
│   └── Transactions.jsx
└── data/
    ├── faqData.js        # Preguntas rápidas
    └── mockProducts.js   # Productos mock
```

## Desarrollo

```bash
npm install
npm run dev
```

## Build y Deploy

```bash
npm run build
aws s3 sync dist/ s3://comfi-frontend-pragma/ --delete
aws cloudfront create-invalidation --distribution-id E2UWNXJTS2NM3V --paths "/*"
```

## Variables de Entorno

```bash
# .env.production
VITE_WEBSOCKET_URL=wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
```

## Captura de Audio

El sistema de grabación usa un enfoque híbrido para máxima confiabilidad:

1. `getUserMedia()` obtiene el stream del micrófono
2. `AudioContext.createMediaStreamSource()` procesa el audio (100% confiable)
3. Se rutea a `MediaStreamDestination` → `MediaRecorder` (compresión Opus/WebM)
4. `timeslice: 500ms` captura datos incrementalmente
5. `audioBitsPerSecond: 32000` mantiene archivos pequeños (< 128KB para WebSocket)
6. Máximo 15 segundos de grabación

Este enfoque resuelve el problema de `MediaRecorder` produciendo blobs vacíos cuando graba directamente del stream del micrófono.
