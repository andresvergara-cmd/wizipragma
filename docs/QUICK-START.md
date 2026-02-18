# ⚡ Quick Start - CENTLI

Guía rápida para desarrolladores que se unen al proyecto.

---

## 🎯 Lo Esencial

**Demo**: https://d210pgg1e91kn6.cloudfront.net

**WebSocket**: wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev

**Lambda**: `poc-wizi-mex-lambda-inference-model-dev`

**AWS Profile**: `pragma-power-user`

---

## 🚀 Setup en 5 Minutos

### 1. Clonar y Configurar

```bash
git clone https://github.com/andresvergara-cmd/wizipragma.git
cd wizipragma
git checkout feature/hackaton
```

### 2. Backend

```bash
cd src_aws/app_inference
pip install -r requirements.txt
export AWS_PROFILE=pragma-power-user
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Probar

```bash
# Test completo
python scripts/test-tool-use-complete.py

# Debe mostrar:
# ✅ Test 1: Transfer - PASSED
# ✅ Test 2: Purchase - PASSED
# ✅ Test 3: Balance Query - PASSED
```

---

## 📁 Estructura Clave

```
wizipragma/
├── src_aws/app_inference/
│   ├── app.py                  # Handler WebSocket
│   ├── bedrock_config.py       # Tool Use + Streaming
│   ├── action_tools.py         # transfer_money(), purchase_product()
│   └── audio_processor.py      # Amazon Transcribe
│
├── frontend/src/
│   ├── components/Chat/        # ChatWidget con voz
│   └── context/                # WebSocket + Chat context
│
├── scripts/
│   ├── deploy-tool-use-fix.sh  # Deploy Lambda
│   ├── deploy-frontend.sh      # Deploy Frontend
│   └── test-tool-use-complete.py  # Tests E2E
│
└── docs/
    ├── DEPLOYMENT.md           # Guía completa
    ├── TOOL-USE-WORKING.md     # Documentación técnica
    └── AUDIO-SETUP-COMPLETO.md # Setup de audio
```

---

## 🔧 Comandos Útiles

### Deploy

```bash
# Backend
./scripts/deploy-tool-use-fix.sh

# Frontend
cd frontend && npm run build && ./scripts/deploy-frontend.sh
```

### Testing

```bash
# Test completo
python scripts/test-tool-use-complete.py

# Test solo transferencias
python scripts/test-simple-transfer.py

# Test audio
python scripts/test-audio-complete.py
```

### Logs

```bash
# Ver logs en tiempo real
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow --profile pragma-power-user
```

---

## 💡 Conceptos Clave

### Tool Use

El agente puede ejecutar acciones automáticamente:

```python
# action_tools.py
def transfer_money(amount: float, recipient_name: str) -> dict:
    """Ejecuta transferencia y retorna TRF-XXXXXXXX"""
    return {
        "success": True,
        "transaction_id": f"TRF-{uuid.uuid4().hex[:8].upper()}"
    }
```

### Streaming

Respuestas en tiempo real via WebSocket:

```python
# bedrock_config.py
for event in response['stream']:
    if 'contentBlockDelta' in event:
        chunk = event['contentBlockDelta']['delta']['text']
        yield chunk  # Stream al frontend
```

### Audio

Transcripción con Amazon Transcribe:

```python
# audio_processor.py
def transcribe_audio(audio_base64: str) -> str:
    """Convierte audio a texto"""
    # 1. Decode base64
    # 2. Upload a S3
    # 3. Start Transcribe job
    # 4. Poll hasta completar
    # 5. Return texto
```

---

## 🎯 Flujos Principales

### 1. Transferencia

```
Usuario: "Envía $500 a mi mamá"
    ↓
Lambda recibe via WebSocket
    ↓
Bedrock analiza → Tool Use
    ↓
Lambda ejecuta transfer_money(500, "mamá")
    ↓
Genera TRF-XXXXXXXX
    ↓
Bedrock formatea respuesta
    ↓
Stream al usuario
```

### 2. Compra

```
Usuario: "Compra un iPhone 15 Pro"
    ↓
Lambda recibe via WebSocket
    ↓
Bedrock analiza → Tool Use
    ↓
Lambda ejecuta purchase_product("iPhone 15 Pro")
    ↓
Genera ORD-XXXXXXXX
    ↓
Bedrock formatea respuesta
    ↓
Stream al usuario
```

### 3. Audio

```
Usuario: Click micrófono → Habla
    ↓
Frontend graba con MediaRecorder
    ↓
Envía audio base64 via WebSocket
    ↓
Lambda transcribe con Transcribe
    ↓
Procesa como mensaje de texto
    ↓
Stream respuesta
```

---

## 🐛 Debugging

### Lambda no responde

```bash
# Ver última actualización
aws lambda get-function \
  --function-name poc-wizi-mex-lambda-inference-model-dev \
  --profile pragma-power-user \
  --query 'Configuration.LastModified'

# Ver logs
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --profile pragma-power-user
```

### Tool Use no ejecuta

```bash
# Verificar action_tools.py está en Lambda
aws lambda get-function \
  --function-name poc-wizi-mex-lambda-inference-model-dev \
  --profile pragma-power-user \
  --query 'Code.Location' \
  | xargs curl -o lambda.zip

unzip -l lambda.zip | grep action_tools
```

### Audio no funciona

1. Verificar HTTPS (audio requiere HTTPS)
2. Verificar permisos IAM (Transcribe + S3)
3. Verificar bucket S3: `poc-wizi-mex-audio-temp`

---

## 📚 Documentación

- [README.md](../README.md) - Overview del proyecto
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guía de deployment
- [TOOL-USE-WORKING.md](TOOL-USE-WORKING.md) - Documentación técnica Tool Use
- [AUDIO-SETUP-COMPLETO.md](AUDIO-SETUP-COMPLETO.md) - Setup de audio
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Guía de contribución

---

## 🎯 Próximos Pasos

1. **Familiarízate con el código**
   - Lee `bedrock_config.py` (lógica principal)
   - Lee `action_tools.py` (herramientas)
   - Lee `ChatWidget.jsx` (frontend)

2. **Ejecuta tests**
   - `python scripts/test-tool-use-complete.py`
   - Prueba el demo en vivo

3. **Haz un cambio pequeño**
   - Agrega un nuevo tool
   - Mejora el frontend
   - Agrega tests

4. **Lee CONTRIBUTING.md**
   - Workflow de desarrollo
   - Estándares de código
   - Proceso de PR

---

## 💬 Preguntas Frecuentes

**¿Cómo agrego un nuevo tool?**

1. Define función en `action_tools.py`
2. Agrega tool definition en `bedrock_config.py`
3. Actualiza `execute_tool()` en `bedrock_config.py`
4. Deploy: `./scripts/deploy-tool-use-fix.sh`

**¿Cómo pruebo localmente?**

Usa los scripts de test:
```bash
python scripts/test-tool-use-complete.py
```

**¿Cómo veo logs?**

```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow --profile pragma-power-user
```

**¿Cómo despliego cambios?**

```bash
# Backend
./scripts/deploy-tool-use-fix.sh

# Frontend
cd frontend && npm run build && ./scripts/deploy-frontend.sh
```

---

## 🚀 ¡Listo!

Ya puedes empezar a contribuir. Si tienes dudas, revisa la documentación o pregunta al equipo.

**Demo**: https://d210pgg1e91kn6.cloudfront.net

**¡Bienvenido al equipo!** 🎉
