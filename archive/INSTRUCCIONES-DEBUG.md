# 🔍 Instrucciones de Debug - Audio Bidireccional

## Fecha
13 de marzo de 2026, 15:55 PM

## ✅ Logs Detallados Implementados

He agregado logs exhaustivos en todo el flujo end-to-end para identificar exactamente dónde se está quedando pegado el proceso.

## 📊 Logs Implementados

### Lambda Handler (app_message.py)
```
🚀 LAMBDA HANDLER STARTED
📡 Connection ID: ...
🌐 Domain: ...
🎭 Stage: ...
✅ API Gateway client initialized
📦 Parsing message body...
📝 Message type: AUDIO
📏 Content length: ...
🔍 Getting session...
✅ Session found
🎯 Processing message type: AUDIO
🎤 Calling process_voice_message...
✅ Message processed successfully
✅ LAMBDA HANDLER COMPLETED SUCCESSFULLY
```

### Voice Processing (process_voice_message)
```
🎤 PROCESS_VOICE_MESSAGE STARTED
📊 Audio data length: ...
🆔 Session ID: ...
👤 User ID: ...
📡 Connection ID: ...

STEP 1: TRANSCRIBE STT (Audio → Text)
📥 Importing transcribe_stt module...
✅ Module imported successfully
🎯 Calling transcribe_audio()...
✅ Transcription completed
📝 Transcribed text: '...'
📤 Sending transcription to client...
✅ Transcription sent to client

STEP 2: BEDROCK AGENT (Text → Response)
🤖 Agent ID: ...
🏷️ Agent Alias ID: ...
📤 Invoking Bedrock Agent...
✅ Bedrock Agent invoked
📥 Extracting agent response...
✅ Response extracted
📝 Response text: '...'

STEP 3: POLLY TTS (Text → Audio)
📥 Importing polly_tts module...
✅ Module imported successfully
🎯 Calling synthesize_speech()...
✅ Speech synthesized
📊 Audio size: ... bytes
📤 Sending audio...
✅ Audio sent successfully

✅ PROCESS_VOICE_MESSAGE COMPLETED
```

### Transcribe STT (transcribe_stt.py)
```
🎙️ TRANSCRIBE_AUDIO STARTED
📊 Input audio length: ...
🆔 Session ID: ...
🔓 Decoding base64...
✅ Decoded to ... bytes
📤 Uploading to S3: ...
✅ Upload completed
🚀 Starting transcription job: ...
✅ Transcription job started
⏳ Polling for completion...
⏳ Status: IN_PROGRESS (attempt 5/60)
⏳ Status: IN_PROGRESS (attempt 10/60)
✅ Transcription completed!
📥 Transcript URI: ...
📥 Downloading transcript...
✅ Transcript downloaded
📝 Transcription: '...'
🧹 Cleaning up...
✅ S3 file deleted
✅ Transcription job deleted
✅ TRANSCRIBE_AUDIO COMPLETED
```

## 🧪 Cómo Probar con Logs

### Paso 1: Abrir Terminal para Logs
```bash
# En una terminal, ejecutar:
./monitor-logs.sh

# O manualmente:
aws logs tail /aws/lambda/centli-app-message --follow --region us-east-1
```

### Paso 2: Abrir Aplicación en Navegador
```
URL: https://db4aulosarsdo.cloudfront.net
```

### Paso 3: Grabar Mensaje de Voz
1. Click en botón 🎤
2. Permitir acceso al micrófono
3. Hablar: "Hola Comfi"
4. Click en ⏹️ para detener

### Paso 4: Observar Logs en Terminal

**Deberías ver**:
```
🚀 LAMBDA HANDLER STARTED
📡 Connection ID: aKDBTcxtoAMCJig=
📦 Parsing message body...
📝 Message type: AUDIO
🎤 Calling process_voice_message...

🎤 PROCESS_VOICE_MESSAGE STARTED
📊 Audio data length: 45678 chars

STEP 1: TRANSCRIBE STT (Audio → Text)
🎙️ TRANSCRIBE_AUDIO STARTED
📤 Uploading to S3: s3://centli-assets-777937796305/transcribe-temp/...
🚀 Starting transcription job: transcribe-session-...
⏳ Polling for completion...
⏳ Status: IN_PROGRESS (attempt 5/60)
✅ Transcription completed!
📝 Transcription: 'Hola Comfi'
✅ TRANSCRIBE_AUDIO COMPLETED

STEP 2: BEDROCK AGENT (Text → Response)
📤 Invoking Bedrock Agent...
✅ Response extracted
📝 Response text: 'Hola, soy Comfi...'

STEP 3: POLLY TTS (Text → Audio)
✅ Speech synthesized
📤 Sending audio...
✅ Audio sent successfully

✅ PROCESS_VOICE_MESSAGE COMPLETED
✅ LAMBDA HANDLER COMPLETED SUCCESSFULLY
```

## 🔍 Identificar el Problema

### Si se queda en "Comfi está escribiendo..."

**Buscar en logs dónde se detiene**:

#### Caso 1: No hay logs
```
❌ Problema: Lambda no se está ejecutando
✅ Solución: Verificar WebSocket connection
```

#### Caso 2: Se detiene en "TRANSCRIBE_AUDIO STARTED"
```
❌ Problema: Error al subir a S3 o iniciar Transcribe
✅ Solución: Verificar permisos de S3 y Transcribe
```

#### Caso 3: Se detiene en "Polling for completion"
```
❌ Problema: Transcribe está tardando mucho o falló
✅ Solución: Verificar job de Transcribe en consola AWS
```

#### Caso 4: Se detiene en "Invoking Bedrock Agent"
```
❌ Problema: Error al invocar Bedrock Agent
✅ Solución: Verificar permisos de Bedrock y Agent ID
```

#### Caso 5: Se detiene en "Calling synthesize_speech"
```
❌ Problema: Error en Polly TTS
✅ Solución: Verificar permisos de Polly
```

## 📋 Checklist de Verificación

### Antes de Probar
- [ ] Terminal abierta con `./monitor-logs.sh`
- [ ] Navegador abierto en https://db4aulosarsdo.cloudfront.net
- [ ] Micrófono funcionando
- [ ] Permisos de micrófono otorgados

### Durante la Prueba
- [ ] Click en 🎤
- [ ] Hablar claramente
- [ ] Click en ⏹️
- [ ] Observar logs en terminal

### Después de la Prueba
- [ ] Identificar último log exitoso
- [ ] Identificar primer log de error (si hay)
- [ ] Copiar logs completos
- [ ] Reportar hallazgos

## 🚨 Errores Comunes y Soluciones

### Error: "Session not found"
**Causa**: WebSocket no está conectado correctamente
**Solución**: Recargar página y reconectar

### Error: "STT failed"
**Causa**: Problema con Transcribe o S3
**Logs a buscar**: "❌ ERROR IN TRANSCRIBE_AUDIO"
**Solución**: Verificar permisos y bucket S3

### Error: "TTS failed"
**Causa**: Problema con Polly
**Logs a buscar**: "⚠️ TTS WARNING"
**Solución**: Verificar permisos de Polly (no crítico, respuesta en texto funciona)

### Error: Lambda timeout
**Causa**: Transcribe tardando más de 30 segundos
**Solución**: Aumentar timeout de Lambda o grabar audio más corto

## 📊 Comandos Útiles

### Ver logs recientes
```bash
aws logs tail /aws/lambda/centli-app-message --since 5m --region us-east-1
```

### Buscar errores
```bash
aws logs filter-log-events \
  --log-group-name /aws/lambda/centli-app-message \
  --filter-pattern "ERROR" \
  --start-time $(($(date +%s) * 1000 - 3600000)) \
  --region us-east-1
```

### Ver jobs de Transcribe
```bash
aws transcribe list-transcription-jobs \
  --status IN_PROGRESS \
  --region us-east-1
```

### Ver archivos en S3
```bash
aws s3 ls s3://centli-assets-777937796305/transcribe-temp/ --recursive --region us-east-1
```

## 📝 Formato de Reporte

Si encuentras un problema, reporta:

```
PROBLEMA: [Descripción breve]

ÚLTIMO LOG EXITOSO:
[Copiar último log con ✅]

PRIMER LOG DE ERROR:
[Copiar primer log con ❌ o ⚠️]

LOGS COMPLETOS:
[Copiar todos los logs desde LAMBDA HANDLER STARTED]

COMPORTAMIENTO EN FRONTEND:
[Qué ves en el navegador]

CONSOLA DEL NAVEGADOR (F12):
[Copiar logs de consola JavaScript]
```

## ✅ Próximos Pasos

1. **Ejecutar**: `./monitor-logs.sh` en terminal
2. **Abrir**: https://db4aulosarsdo.cloudfront.net en navegador
3. **Probar**: Grabar mensaje de voz
4. **Observar**: Logs en terminal
5. **Reportar**: Hallazgos con formato de reporte

---

**Lambda actualizada**: 2026-03-13T19:55:05Z
**Logs detallados**: ✅ Implementados
**Status**: 🟢 Listo para debug
