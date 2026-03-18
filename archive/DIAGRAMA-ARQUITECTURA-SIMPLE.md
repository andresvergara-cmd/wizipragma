# Diagrama de Arquitectura Simplificado - Comfi

## Vista de Alto Nivel

```
┌─────────────┐
│   USUARIO   │
│  (Browser)  │
└──────┬──────┘
       │
       │ HTTPS
       ▼
┌─────────────────────┐
│   CloudFront CDN    │
│  db4aulosarsdo...   │
└──────┬──────────────┘
       │
       │ Origin
       ▼
┌─────────────────────┐
│    S3 Bucket        │
│ comfi-frontend-...  │
│  (React App)        │
└──────┬──────────────┘
       │
       │ WebSocket
       │ wss://vvg621xawg...
       ▼
┌─────────────────────┐
│   API Gateway       │
│   (WebSocket)       │
│                     │
│  $connect    ───────┼──→ Lambda: app-connect
│  $default    ───────┼──→ Lambda: app-message  ──┐
│  $disconnect ───────┼──→ Lambda: app-disconnect │
└─────────────────────┘                           │
                                                  │
                                                  │ invoke_agent()
                                                  ▼
                                        ┌──────────────────────┐
                                        │   Bedrock Agent      │
                                        │   (Z6PCEKYNPS)       │
                                        │                      │
                                        │  Claude 3.5 Sonnet   │
                                        │  "Soy Comfi..."      │
                                        └──────────────────────┘
```

## Flujo de Conversación

```
1. Usuario → "¿Cómo me afilio a Comfama?"
   ↓
2. Frontend (React) → WebSocket
   ↓
3. API Gateway → Lambda app-message
   ↓
4. Lambda → Bedrock Agent (invoke_agent)
   ↓
5. Bedrock Agent → Claude 3.5 Sonnet
   - System Prompt: "Eres Comfi de Comfama..."
   - Procesa pregunta
   - Genera respuesta
   ↓
6. Respuesta streaming ← Lambda ← Agent
   ↓
7. WebSocket ← API Gateway
   ↓
8. Frontend muestra respuesta en tiempo real
```

## Componentes Clave

### Frontend
- **Ubicación**: S3 bucket `comfi-frontend-pragma`
- **CDN**: CloudFront `E2UWNXJTS2NM3V`
- **URL**: https://db4aulosarsdo.cloudfront.net
- **Tech**: React + Vite + WebSocket

### Backend
- **WebSocket**: API Gateway `vvg621xawg`
- **Lambdas**: 
  - `centli-app-connect` (conexión)
  - `centli-app-message` (mensajes)
  - `centli-app-disconnect` (desconexión)

### IA
- **Bedrock Agent**: `Z6PCEKYNPS`
- **Modelo**: Claude 3.5 Sonnet
- **Identidad**: Comfi de Comfama (Colombia)

### Datos
- **DynamoDB**: `centli-sessions` (sesiones WebSocket)

## URLs Importantes

```
Frontend:  https://db4aulosarsdo.cloudfront.net
WebSocket: wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
Cuenta:    777937796305 (us-east-1)
```

## Estado Actual

✅ **Funcionando**:
- Frontend desplegado y accesible
- WebSocket conecta correctamente
- Bedrock Agent responde como Comfi
- NO menciona Carlos/México/MXN

⚠️ **Pendiente**:
- Esperar 5 minutos para propagación completa
- Probar en ventana incógnita
- Verificar respuestas sobre Comfama

## Comandos Rápidos

```bash
# Ver logs
aws logs tail /aws/lambda/centli-app-message --follow

# Test
python3 scripts/test-websocket-identity.py

# Verificar Agent
aws bedrock-agent get-agent --agent-id Z6PCEKYNPS --region us-east-1
```
