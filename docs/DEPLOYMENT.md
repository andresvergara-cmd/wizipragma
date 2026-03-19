# Guía de Deployment - Comfi

## Prerrequisitos

- AWS CLI configurado con credenciales válidas
- Python 3.10+
- Node.js 18+
- Región: us-east-1

---

## Arquitectura Desplegada

```
CloudFront (E2UWNXJTS2NM3V) → S3 (comfi-frontend-pragma)
API Gateway WebSocket (vvg621xawg) → Lambda centli-app-message (512MB, 45s)
                                   → Bedrock Agent (Z6PCEKYNPS)
                                   → Transcribe Streaming + Polly Neural
                                   → DynamoDB (centli-sessions)
```

---

## 1. Frontend

### Build y Deploy

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://comfi-frontend-pragma/ --delete
aws cloudfront create-invalidation --distribution-id E2UWNXJTS2NM3V --paths "/*"
```

### Variables de entorno

```bash
# frontend/.env.production
VITE_WEBSOCKET_URL=wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
```

---

## 2. Lambda app_message

### Empaquetar y desplegar

```bash
cd src_aws/app_message
zip -r function.zip app_message.py transcribe_stt.py polly_tts.py amazon_transcribe/
aws lambda update-function-code \
  --function-name centli-app-message \
  --zip-file fileb://function.zip \
  --region us-east-1
```

### Configuración de la Lambda

| Parámetro | Valor |
|-----------|-------|
| Runtime | Python 3.11 |
| Memoria | 512 MB |
| Timeout | 45 segundos |
| Layer | nova-sonic-dependencies:1 (ffmpeg + pydub) |

### Variables de entorno de la Lambda

| Variable | Valor |
|----------|-------|
| SESSIONS_TABLE | centli-sessions |
| EVENT_BUS_NAME | centli-event-bus |
| AGENTCORE_ID | Z6PCEKYNPS |
| AGENTCORE_ALIAS_ID | TSTALIASID |
| ASSETS_BUCKET | centli-assets-777937796305 |

> **IMPORTANTE**: Nunca desplegar `src_aws/app_inference/` a `centli-app-message`. Es código legacy que romperá la Lambda.

---

## 3. Lambdas Connect/Disconnect

```bash
# app_connect
cd src_aws/app_connect
zip app_connect.zip app_connect.py
aws lambda update-function-code --function-name centli-app-connect --zip-file fileb://app_connect.zip

# app_disconnect
cd src_aws/app_disconnect
zip app_disconnect.zip app_disconnect.py
aws lambda update-function-code --function-name centli-app-disconnect --zip-file fileb://app_disconnect.zip
```

---

## 4. Knowledge Base

### Actualizar FAQ

1. Editar/regenerar el documento FAQ:
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 scripts/generate_faq_docx.py
   ```

2. Subir a S3:
   ```bash
   aws s3 cp knowledge-base-docs/FAQ_Comfama_Centro_Conocimiento_v2.docx \
     s3://comfi-knowledge-base-pragma/
   ```

3. Sincronizar Knowledge Base:
   ```bash
   aws bedrock-agent start-ingestion-job \
     --knowledge-base-id PDNW6DDDGZ \
     --data-source-id ELUSMDMG9H
   ```

---

## 5. Verificación Post-Deploy

### Frontend
- Abrir https://db4aulosarsdo.cloudfront.net (hard refresh: Cmd+Shift+R)
- Verificar indicador "En línea"
- Enviar mensaje de texto
- Probar grabación de voz

### Lambda
```bash
aws logs tail /aws/lambda/centli-app-message --follow --region us-east-1
```

### Tests E2E
```bash
python scripts/test_voice_complete.py
```

---

## 6. Permisos IAM

### CentliLambdaExecutionRole
- DynamoDB: CRUD en centli-sessions
- Bedrock: InvokeAgent
- Transcribe: StartStreamTranscription, StartTranscriptionJob, GetTranscriptionJob
- Polly: SynthesizeSpeech
- S3: PutObject, GetObject, DeleteObject en centli-assets-*
- API Gateway: ManageConnections (post_to_connection)

### CentliBedrockAgentRole
- Bedrock: InvokeModel
- Bedrock: Retrieve, RetrieveAndGenerate
- OpenSearch Serverless: APIAccessAll

---

## 7. Troubleshooting

| Problema | Solución |
|----------|----------|
| "No pude entender el audio" | Verificar que el blob > 500 bytes en consola del navegador |
| Lambda timeout | Verificar timeout es 45s, no 30s |
| Knowledge Base no responde | Verificar permisos bedrock:Retrieve en el rol del agente |
| Frontend no carga | Verificar invalidación de CloudFront completada |
| WebSocket desconectado | Verificar que la Lambda $connect funciona y DynamoDB accesible |
