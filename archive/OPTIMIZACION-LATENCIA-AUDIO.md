# 🚀 Optimización de Latencia - Audio Bidireccional

**Fecha**: 13 de marzo de 2026
**Problema**: Latencia de ~20 segundos por conversación
**Solución**: Cambiar de Transcribe Batch a Transcribe Streaming

---

## 📊 Análisis de Latencia Actual

### Desglose del Tiempo (Primera Petición Exitosa)
```
Total: 20,607 ms (~20.6 segundos)

1. Transcribe STT (Batch):  ~16,000 ms (78% del tiempo)
   - Upload a S3:              ~200 ms
   - Start job:                ~100 ms
   - Polling (16 iteraciones): ~16,000 ms ← CUELLO DE BOTELLA
   - Download result:          ~100 ms
   - Cleanup:                  ~100 ms

2. Bedrock Agent:            ~3,000 ms (15% del tiempo)
   - Invoke agent:             ~100 ms
   - Generate response:        ~2,900 ms

3. Polly TTS:                  ~200 ms (1% del tiempo)
   - Synthesize speech:        ~200 ms

4. Network overhead:         ~1,400 ms (6% del tiempo)
```

### Problema Principal
**Transcribe Batch con Polling**: 16 segundos de espera activa

El código actual hace polling cada segundo durante hasta 60 segundos:
```python
while attempt < max_attempts:
    attempt += 1
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    job_status = status['TranscriptionJob']['TranscriptionJobStatus']
    
    if job_status == 'COMPLETED':
        break
    
    time.sleep(1)  # ← Espera 1 segundo entre cada check
```

---

## 🎯 Solución: Transcribe Streaming

### Ventajas
1. **Sin polling**: Procesa audio en tiempo real
2. **Latencia reducida**: ~2-3 segundos vs 16 segundos
3. **Mejor UX**: Respuesta casi inmediata
4. **Menos costos**: No requiere S3 temporal

### Arquitectura Propuesta

**Antes (Batch)**:
```
Audio → S3 → Start Job → Poll (16s) → Download → Text
```

**Después (Streaming)**:
```
Audio → Transcribe Stream → Text (2-3s)
```

### Latencia Esperada
```
Total estimado: ~5-6 segundos (reducción del 70%)

1. Transcribe STT (Streaming):  ~2,500 ms (42%)
   - Stream audio:                ~2,500 ms

2. Bedrock Agent:               ~3,000 ms (50%)
   - Generate response:           ~3,000 ms

3. Polly TTS:                     ~200 ms (3%)
   - Synthesize speech:            ~200 ms

4. Network overhead:              ~300 ms (5%)
```

---

## 🔧 Implementación

### Opción 1: Transcribe Streaming HTTP/2 (Recomendado)

**Ventajas**:
- Más simple de implementar
- No requiere WebSocket adicional
- Funciona con Lambda

**Código**:
```python
import boto3
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

async def transcribe_audio_streaming(audio_bytes: bytes, language_code='es-ES'):
    """
    Transcribe audio using Transcribe Streaming
    """
    client = TranscribeStreamingClient(region="us-east-1")
    
    # Create audio stream
    stream = await client.start_stream_transcription(
        language_code=language_code,
        media_sample_rate_hz=16000,
        media_encoding="pcm"
    )
    
    # Send audio
    async def write_chunks():
        async with stream.input_stream as input_stream:
            await input_stream.send_audio_event(audio_chunk=audio_bytes)
        await stream.input_stream.end_stream()
    
    # Receive transcription
    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())
    
    return handler.transcript
```

### Opción 2: Mantener Batch pero Optimizar

Si no podemos usar Streaming, optimizar el batch:

**Cambios**:
1. Reducir intervalo de polling: 1s → 0.5s
2. Usar exponential backoff
3. Timeout más agresivo: 60s → 30s

**Código**:
```python
# Polling optimizado
interval = 0.5  # Start with 500ms
max_interval = 2.0  # Max 2 seconds
attempt = 0

while attempt < max_attempts:
    attempt += 1
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        break
    
    time.sleep(interval)
    interval = min(interval * 1.2, max_interval)  # Exponential backoff
```

**Latencia esperada**: ~10-12 segundos (reducción del 40%)

---

## 📝 Recomendación

### Corto Plazo (Hoy)
**Opción 2**: Optimizar polling
- Cambio mínimo de código
- Reducción inmediata de latencia
- Sin riesgo

### Mediano Plazo (Esta Semana)
**Opción 1**: Implementar Transcribe Streaming
- Mejor experiencia de usuario
- Latencia óptima
- Requiere más testing

---

## 🐛 Problema de Segunda Petición

### Análisis
Los logs muestran que la primera petición funcionó perfectamente, pero no hay logs de una segunda invocación.

### Posibles Causas
1. **Frontend bloqueado**: Esperando respuesta anterior
2. **WebSocket desconectado**: Después de la primera petición
3. **Estado de UI**: Botón deshabilitado

### Verificación Necesaria
1. Revisar consola del navegador
2. Verificar estado del WebSocket
3. Comprobar si hay errores en el frontend

### Solución Temporal
Agregar timeout en el frontend para liberar el estado:
```javascript
// En ChatWidget.jsx
const handleVoiceMessage = async (audioBlob) => {
  setIsRecording(false)
  setIsProcessing(true)
  
  // Timeout de 30 segundos
  const timeout = setTimeout(() => {
    setIsProcessing(false)
    console.error('⏱️ Timeout: No response after 30s')
  }, 30000)
  
  try {
    // Send audio...
  } finally {
    clearTimeout(timeout)
    setIsProcessing(false)
  }
}
```

---

## 🎯 Plan de Acción

### Inmediato (Ahora)
1. ✅ Optimizar polling de Transcribe (Opción 2)
2. ✅ Agregar timeout en frontend
3. ✅ Desplegar cambios

### Seguimiento
1. Probar segunda petición
2. Medir latencia real
3. Verificar logs

### Futuro
1. Evaluar Transcribe Streaming
2. Implementar si es viable
3. Testing completo

---

**Próximo paso**: Implementar optimización de polling
