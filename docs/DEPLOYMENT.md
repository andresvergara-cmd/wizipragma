# 🚀 Guía de Deployment - CENTLI

Esta guía detalla cómo desplegar CENTLI en AWS.

---

## 📋 Prerrequisitos

- AWS CLI configurado con perfil `pragma-power-user`
- Python 3.10+
- Node.js 18+
- Acceso a AWS Bedrock (Claude 3.7 Sonnet)
- Permisos IAM necesarios

---

## 🏗️ Arquitectura Desplegada

```
CloudFront (Frontend)
    ↓
API Gateway (WebSocket)
    ↓
Lambda (Inference)
    ↓
├── AWS Bedrock (Claude 3.7)
├── Amazon Transcribe (Audio)
├── DynamoDB (User Data)
└── S3 (Audio Temp)
```

---

## 1️⃣ Backend (Lambda)

### Desplegar Lambda con Tool Use

```bash
cd src_aws/app_inference
./scripts/deploy-tool-use-fix.sh
```

Este script:
- Empaqueta el código Lambda
- Incluye `action_tools.py` y `audio_processor.py`
- Actualiza la función `poc-wizi-mex-lambda-inference-model-dev`
- Configura variables de entorno

### Verificar Deployment

```bash
aws lambda get-function \
  --function-name poc-wizi-mex-lambda-inference-model-dev \
  --profile pragma-power-user \
  --query 'Configuration.LastModified'
```

---

## 2️⃣ Audio (Amazon Transcribe)

### Desplegar Audio Processor

```bash
./scripts/deploy-audio-transcribe.sh
```

Este script:
- Crea bucket S3 `poc-wizi-mex-audio-temp`
- Configura lifecycle policy (1 día)
- Actualiza Lambda con `audio_processor.py`

### Agregar Permisos IAM

**IMPORTANTE**: Debes agregar permisos manualmente en la consola AWS.

1. Ve a IAM Console
2. Busca el rol: `poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD`
3. Agrega inline policy con este JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::poc-wizi-mex-audio-temp/*"
    }
  ]
}
```

### Verificar Audio

```bash
python scripts/test-audio-complete.py
```

---

## 3️⃣ Frontend (CloudFront)

### Build y Deploy

```bash
cd frontend

# Build
npm run build

# Deploy a S3
aws s3 sync dist/ s3://poc-wizi-mex-frontend \
  --profile pragma-power-user \
  --delete

# Invalidar cache de CloudFront
aws cloudfront create-invalidation \
  --distribution-id E3XXXXXXXXXX \
  --paths "/*" \
  --profile pragma-power-user
```

### Verificar Frontend

Abre: https://d210pgg1e91kn6.cloudfront.net

---

## 4️⃣ Configuración de Variables

### Backend (.env)

```bash
# src_aws/app_inference/.env
AWS_PROFILE=pragma-power-user
REGION_NAME=us-east-1
DYNAMODB_TABLE_USERS=poc-wizi-mex-users
DYNAMODB_TABLE_ACCOUNTS=poc-wizi-mex-accounts
DYNAMODB_TABLE_BENEFICIARIES=poc-wizi-mex-beneficiaries
DYNAMODB_TABLE_PRODUCTS=poc-wizi-mex-products
S3_AUDIO_BUCKET=poc-wizi-mex-audio-temp
```

### Frontend (.env.production)

```bash
# frontend/.env.production
VITE_WEBSOCKET_URL=wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
VITE_API_URL=https://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
```

---

## 5️⃣ Testing Post-Deployment

### Test Completo

```bash
python scripts/test-tool-use-complete.py
```

Debe mostrar:
```
✅ Test 1: Transfer - PASSED (TRF-XXXXXXXX)
✅ Test 2: Purchase - PASSED (ORD-XXXXXXXX)
✅ Test 3: Balance Query - PASSED

Total: 3 passed, 0 failed
```

### Test Manual

1. Abre: https://d210pgg1e91kn6.cloudfront.net
2. Prueba texto: "Envía $500 a mi mamá"
3. Prueba voz: Click en micrófono → "Compra un iPhone"
4. Verifica IDs de transacción

---

## 6️⃣ Monitoreo

### CloudWatch Logs

```bash
# Ver logs de Lambda
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow \
  --profile pragma-power-user
```

### Métricas

- **Invocations**: Número de requests
- **Duration**: Tiempo de ejecución
- **Errors**: Errores de Lambda
- **Throttles**: Requests limitados

---

## 7️⃣ Rollback

### Revertir Lambda

```bash
# Listar versiones
aws lambda list-versions-by-function \
  --function-name poc-wizi-mex-lambda-inference-model-dev \
  --profile pragma-power-user

# Revertir a versión anterior
aws lambda update-alias \
  --function-name poc-wizi-mex-lambda-inference-model-dev \
  --name PROD \
  --function-version <VERSION> \
  --profile pragma-power-user
```

### Revertir Frontend

```bash
# Desplegar versión anterior desde Git
git checkout <COMMIT_ANTERIOR>
cd frontend
npm run build
./scripts/deploy-frontend.sh
```

---

## 8️⃣ Troubleshooting

### Lambda no responde

```bash
# Verificar configuración
aws lambda get-function-configuration \
  --function-name poc-wizi-mex-lambda-inference-model-dev \
  --profile pragma-power-user

# Verificar logs
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --profile pragma-power-user
```

### Audio no funciona

1. Verificar permisos IAM (Transcribe + S3)
2. Verificar bucket S3 existe
3. Verificar HTTPS (audio requiere HTTPS)
4. Ver logs de Lambda

### Tool Use no ejecuta

1. Verificar `action_tools.py` está en Lambda
2. Verificar logs de Bedrock
3. Verificar formato de tool definitions
4. Probar con test: `python scripts/test-tool-use-complete.py`

---

## 9️⃣ Costos Estimados

### Por Request

- **Lambda**: $0.0000002 por invocación
- **Bedrock**: ~$0.003 por request (Claude 3.7)
- **Transcribe**: $0.024 por minuto de audio
- **API Gateway**: $0.001 por millón de mensajes

### Por Usuario/Mes (estimado)

- 100 requests/mes: ~$0.30
- 10 minutos audio/mes: ~$0.24
- **Total**: ~$0.54/usuario/mes

### Optimizaciones

- Usar Lambda Provisioned Concurrency para latencia
- Cachear respuestas comunes
- Comprimir audio antes de transcribir
- Usar Bedrock batch para múltiples requests

---

## 🔟 Checklist de Deployment

### Pre-Deployment

- [ ] Tests pasan localmente
- [ ] Variables de entorno configuradas
- [ ] Permisos IAM verificados
- [ ] Backup de versión actual

### Deployment

- [ ] Backend desplegado
- [ ] Audio configurado
- [ ] Frontend desplegado
- [ ] Cache invalidado

### Post-Deployment

- [ ] Tests de integración pasan
- [ ] Frontend carga correctamente
- [ ] Audio funciona
- [ ] Tool Use ejecuta acciones
- [ ] Logs sin errores

### Validación

- [ ] Demo completo funciona
- [ ] Transferencias generan IDs
- [ ] Compras generan IDs
- [ ] Consultas responden correctamente

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa logs de CloudWatch
2. Ejecuta tests de diagnóstico
3. Verifica configuración de IAM
4. Contacta al equipo de desarrollo

---

**✅ Sistema listo para producción**

**🚀 URL Demo**: https://d210pgg1e91kn6.cloudfront.net
