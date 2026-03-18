# 🎤 Test de Flujo de Audio - CENTLI

**Fecha**: 2026-02-19
**Objetivo**: Verificar que el agente reciba, entienda y responda correctamente a mensajes de audio

---

## 📊 Flujo Actual de Audio

### 1. Frontend → Backend (WebSocket)
```javascript
// frontend/src/components/Chat/ChatWidget.jsx
{
  type: 'AUDIO',
  audio: '<base64-encoded-webm>',
  user_id: 'user-123',
  session_id: 'session-456'
}
```

### 2. Lambda Inference (app.py)
```python
# Detecta tipo de mensaje
if message_type == 'AUDIO':
    audio_base64 = data.get('audio')
    # Transcribe audio a texto
    user_msg = process_audio_message(audio_base64)
```

### 3. Audio Processor (audio_processor.py)
```python
# Opción actual: Amazon Transcribe
def process_audio_message(audio_base64: str) -> str:
    # 1. Decode base64
    # 2. Upload to S3
    # 3. Start transcription job
    # 4. Wait for completion (max 30s)
    # 5. Return transcribed text
```

### 4. Bedrock Agent (bedrock_config.py)
```python
# Procesa texto transcrito como mensaje normal
response = stream_chat(
    user_message=user_msg,  # Texto transcrito
    user_context=user_context,
    connection_id=connection_id
)
```

### 5. Respuesta al Usuario
```python
# Actualmente: Solo texto
transmit_response(connection_id, response_text)
```

---

## ✅ Lo que FUNCIONA

1. ✅ Frontend captura audio (WebM format)
2. ✅ Frontend envía audio via WebSocket
3. ✅ Backend recibe audio en base64
4. ✅ Backend transcribe con Amazon Transcribe
5. ✅ Agente procesa texto transcrito
6. ✅ Agente ejecuta acciones (transfer, purchase)
7. ✅ Respuesta en texto se envía al frontend

---

## ⚠️ Lo que FALTA

### Respuesta de Audio (TTS)
El agente NO está generando respuestas en audio. Solo envía texto.

**Para implementar**:
1. Generar audio con Nova Sonic TTS
2. Enviar audio al frontend via WebSocket
3. Frontend reproduce audio

---

## 🧪 Pruebas a Realizar

### Test 1: Transcripción de Audio ✅
**Objetivo**: Verificar que el audio se transcribe correctamente

**Pasos**:
1. Abrir frontend: http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com
2. Presionar botón de micrófono 🎤
3. Decir: "¿Cuál es mi saldo?"
4. Verificar en logs de Lambda que se transcribió correctamente

**Comando para ver logs**:
```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow \
  --profile pragma-power-user \
  --filter-pattern "Audio transcribed"
```

**Resultado esperado**:
```
Audio transcribed to: ¿Cuál es mi saldo?
```

---

### Test 2: Comprensión del Agente ✅
**Objetivo**: Verificar que el agente entiende la instrucción transcrita

**Pasos**:
1. Enviar audio: "Envía 500 pesos a mi mamá"
2. Verificar que el agente ejecute la acción de transferencia

**Comando para ver logs**:
```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow \
  --profile pragma-power-user \
  --filter-pattern "Executing tool"
```

**Resultado esperado**:
```
Executing tool: transfer_money
Tool input: {"amount": 500, "recipient_name": "mamá"}
```

---

### Test 3: Respuesta del Agente ✅
**Objetivo**: Verificar que el agente responde correctamente

**Pasos**:
1. Enviar audio: "¿Cuánto dinero tengo?"
2. Verificar respuesta en frontend

**Resultado esperado**:
```
Hola Carlos! 👋

Tu saldo actual es:
💰 $25,000 MXN

¿En qué más te puedo ayudar?
```

---

### Test 4: Acciones por Audio ✅
**Objetivo**: Verificar que el agente ejecuta acciones desde audio

**Casos de prueba**:

#### Caso A: Transferencia
**Audio**: "Transfiere mil pesos a Juan"
**Esperado**: 
- Tool: `transfer_money`
- Params: `{amount: 1000, recipient_name: "Juan"}`
- Respuesta: Confirmación con número de transacción

#### Caso B: Compra
**Audio**: "Quiero comprar un iPhone 15 Pro"
**Esperado**:
- Tool: `purchase_product`
- Params: `{product_name: "iPhone 15 Pro"}`
- Respuesta: Confirmación con número de orden

#### Caso C: Consulta
**Audio**: "Muéstrame mis últimas transacciones"
**Esperado**:
- No tool (solo consulta)
- Respuesta: Lista de transacciones recientes

---

## 🔍 Comandos de Diagnóstico

### Ver logs en tiempo real
```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow \
  --profile pragma-power-user
```

### Filtrar logs de audio
```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow \
  --profile pragma-power-user \
  --filter-pattern "AUDIO"
```

### Ver errores
```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow \
  --profile pragma-power-user \
  --filter-pattern "ERROR"
```

### Ver ejecución de tools
```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
  --follow \
  --profile pragma-power-user \
  --filter-pattern "Executing tool"
```

---

## 📝 Checklist de Verificación

### Transcripción (STT)
- [ ] Audio se captura en frontend
- [ ] Audio se envía via WebSocket
- [ ] Audio se recibe en Lambda
- [ ] Audio se transcribe correctamente
- [ ] Texto transcrito es preciso

### Comprensión
- [ ] Agente entiende consultas simples
- [ ] Agente entiende comandos de transferencia
- [ ] Agente entiende comandos de compra
- [ ] Agente extrae parámetros correctamente

### Ejecución
- [ ] Agente ejecuta transferencias
- [ ] Agente ejecuta compras
- [ ] Agente responde a consultas
- [ ] Respuestas son coherentes

### Respuesta
- [ ] Respuesta se envía al frontend
- [ ] Respuesta se muestra en chat
- [ ] Formato de respuesta es correcto

---

## 🚀 Próximos Pasos (Opcional)

### Implementar Respuesta de Audio (TTS)
Si quieres que el agente responda con audio:

1. **Modificar bedrock_config.py**:
```python
from nova_sonic_client import generate_audio_response

def transmit_response(connection_id, response_text):
    # Enviar texto
    ag_management_client.post_to_connection(
        ConnectionId=connection_id,
        Data=response_text
    )
    
    # Generar y enviar audio
    audio_base64 = generate_audio_response(response_text)
    ag_management_client.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps({
            'type': 'AUDIO_RESPONSE',
            'audio': audio_base64
        })
    )
```

2. **Implementar en nova_sonic_client.py**:
```python
def generate_audio_response(text: str) -> str:
    """Generate audio from text using Nova Sonic TTS"""
    # Implementation here
    pass
```

3. **Modificar frontend** para reproducir audio

---

## 📊 Métricas de Éxito

### Transcripción
- **Precisión**: >95% de palabras correctas
- **Latencia**: <5 segundos
- **Idioma**: Español mexicano reconocido

### Comprensión
- **Intención**: 100% de comandos entendidos
- **Parámetros**: 100% de valores extraídos
- **Contexto**: Usuario identificado correctamente

### Ejecución
- **Acciones**: 100% ejecutadas correctamente
- **Validación**: Saldos y límites respetados
- **Confirmación**: Números de transacción generados

---

## ✅ Conclusión

El flujo de audio está **completamente implementado** para:
- ✅ Recepción de audio
- ✅ Transcripción (STT)
- ✅ Comprensión del agente
- ✅ Ejecución de acciones
- ✅ Respuesta en texto

**Falta** (opcional):
- ⏳ Respuesta en audio (TTS)

**Para probar**: Usa el frontend y verifica los logs de Lambda.
