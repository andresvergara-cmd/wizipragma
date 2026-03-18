# Plan de Pruebas: Transcribe + Polly

## Fecha
13 de marzo de 2026

## Objetivo
Garantizar que la implementación de Transcribe STT + Polly TTS funcione correctamente para conversación bidireccional.

## Arquitectura Implementada

```
Usuario habla → Frontend graba WebM → WebSocket → Lambda
                                                      ↓
                                            Amazon Transcribe STT
                                                      ↓
                                                   Texto
                                                      ↓
                                              Bedrock Agent
                                                      ↓
                                              Texto respuesta
                                                      ↓
                                              Amazon Polly TTS
                                                      ↓
                                            Audio MP3 (chunks)
                                                      ↓
                                            WebSocket → Frontend
                                                      ↓
                                            Usuario escucha
```

## Componentes Implementados

### 1. Backend (Lambda)

#### transcribe_stt.py
- ✅ Función `transcribe_audio(audio_base64, session_id)`
- ✅ Sube audio a S3 temporal
- ✅ Inicia job de Transcribe
- ✅ Polling hasta completar (max 60 segundos)
- ✅ Retorna texto transcrito
- ✅ Limpia archivos temporales

#### polly_tts.py (ya existente)
- ✅ Función `synthesize_speech(text)`
- ✅ Usa voz Mia (es-MX, Neural)
- ✅ Retorna audio MP3 en base64
- ✅ Maneja textos largos (max 3000 chars)

#### app_message.py (actualizado)
- ✅ `process_voice_message()` usa Transcribe + Polly
- ✅ Envía transcripción al frontend
- ✅ Procesa con Bedrock Agent
- ✅ Divide audio en chunks si es muy grande (>100KB)
- ✅ Envía chunks al frontend

### 2. Frontend (React)

#### WebSocketContext.jsx (actualizado)
- ✅ Detecta mensajes `transcription`
- ✅ Detecta mensajes `audio_chunk`
- ✅ Detecta mensajes `audio_response`
- ✅ Función `assembleAndPlayAudio()` soporta MP3 y PCM
- ✅ Reproduce audio MP3 con Audio element

## Plan de Pruebas

### Fase 1: Pruebas Unitarias (Backend)

#### Test 1.1: Transcribe STT
```bash
# Crear audio de prueba
python3 << EOF
import base64
import boto3

# Generar audio de prueba con Polly
polly = boto3.client('polly', region_name='us-east-1')
response = polly.synthesize_speech(
    Text='Hola, esta es una prueba',
    OutputFormat='mp3',
    VoiceId='Mia',
    Engine='neural'
)

audio_bytes = response['AudioStream'].read()
audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# Guardar para prueba
with open('/tmp/test_audio.txt', 'w') as f:
    f.write(audio_base64)

print(f"Audio de prueba generado: {len(audio_base64)} chars")
EOF

# Probar transcripción
python3 << EOF
import sys
sys.path.append('src_aws/app_message')

from transcribe_stt import transcribe_audio

with open('/tmp/test_audio.txt', 'r') as f:
    audio_base64 = f.read()

result = transcribe_audio(audio_base64, 'test-session-123')
print(f"Transcripción: {result}")
EOF
```

**Resultado esperado**: "Hola, esta es una prueba" (o similar)

#### Test 1.2: Polly TTS
```bash
python3 << EOF
import sys
sys.path.append('src_aws/app_message')

from polly_tts import synthesize_speech

result = synthesize_speech("Hola, soy Comfi de Comfama")
print(f"Audio generado: {result['size_bytes']} bytes")
print(f"Base64 length: {len(result['audio_base64'])} chars")
EOF
```

**Resultado esperado**: Audio MP3 generado (~50KB)

#### Test 1.3: Flujo Completo Lambda
```bash
# Invocar Lambda con mensaje de voz
aws lambda invoke \
  --function-name centli-app-message \
  --payload file://test-voice-payload.json \
  --region us-east-1 \
  /tmp/lambda-response.json

cat /tmp/lambda-response.json
```

**Resultado esperado**: statusCode 200, sin errores

### Fase 2: Pruebas de Integración

#### Test 2.1: WebSocket Connection
```bash
# Verificar que WebSocket esté activo
wscat -c wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
```

**Resultado esperado**: Conexión exitosa

#### Test 2.2: Enviar Mensaje de Texto
```javascript
// En consola del navegador
const ws = new WebSocket('wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod')

ws.onopen = () => {
  console.log('✅ Connected')
  
  ws.send(JSON.stringify({
    action: 'sendMessage',
    data: {
      user_id: 'test-user',
      session_id: 'test-session-' + Date.now(),
      type: 'TEXT',
      message: 'Hola Comfi'
    }
  }))
}

ws.onmessage = (event) => {
  console.log('📨 Message:', event.data)
}
```

**Resultado esperado**: Respuesta del agente en texto

### Fase 3: Pruebas End-to-End (E2E)

#### Test 3.1: Grabación de Voz
1. Abrir https://db4aulosarsdo.cloudfront.net
2. Click en botón 🎤
3. Permitir acceso al micrófono
4. Hablar: "¿Cómo me afilio a Comfama?"
5. Click en ⏹️ para detener

**Resultado esperado**:
- ✅ Botón cambia a ⏹️ durante grabación
- ✅ Aparece mensaje "🎤 ¿Cómo me afilio a Comfama?" (transcripción)
- ✅ Aparece respuesta de Comfi (texto)
- ✅ Se reproduce audio automáticamente

#### Test 3.2: Verificar Transcripción
**Casos de prueba**:
1. "¿Cuáles son los beneficios de Comfama?"
2. "¿Cómo solicito un crédito?"
3. "¿Dónde están las oficinas?"
4. "¿Cuánto cuesta la afiliación?"
5. "Gracias, adiós"

**Para cada caso**:
- ✅ Transcripción correcta (>80% precisión)
- ✅ Respuesta relevante del agente
- ✅ Audio se reproduce correctamente

#### Test 3.3: Verificar Audio
**Verificaciones**:
- ✅ Audio se escucha claro
- ✅ Volumen adecuado
- ✅ Sin cortes o distorsión
- ✅ Voz femenina (Mia)
- ✅ Acento mexicano/neutral

#### Test 3.4: Manejo de Errores
**Casos de error**:
1. Grabar sin hablar (silencio)
2. Grabar con mucho ruido de fondo
3. Grabar muy corto (<1 segundo)
4. Grabar muy largo (>30 segundos)

**Resultado esperado**:
- ✅ Mensaje de error amigable
- ✅ No se rompe la aplicación
- ✅ Usuario puede intentar de nuevo

### Fase 4: Pruebas de Rendimiento

#### Test 4.1: Latencia
**Medir tiempos**:
1. Tiempo de transcripción (Transcribe)
2. Tiempo de respuesta (Bedrock Agent)
3. Tiempo de síntesis (Polly)
4. Tiempo total (inicio → audio)

**Objetivo**: <10 segundos total

#### Test 4.2: Concurrencia
**Simular múltiples usuarios**:
- 5 usuarios simultáneos
- 10 usuarios simultáneos
- 20 usuarios simultáneos

**Verificar**:
- ✅ Todas las solicitudes se procesan
- ✅ No hay timeouts
- ✅ Calidad de audio consistente

#### Test 4.3: Tamaño de Audio
**Casos**:
1. Respuesta corta (1 frase, ~5 segundos)
2. Respuesta media (2-3 frases, ~15 segundos)
3. Respuesta larga (párrafo, ~30 segundos)

**Verificar**:
- ✅ Audio se divide en chunks si es necesario
- ✅ Chunks se ensamblan correctamente
- ✅ No hay pérdida de audio

### Fase 5: Pruebas de Compatibilidad

#### Test 5.1: Navegadores
**Probar en**:
- ✅ Chrome (desktop)
- ✅ Firefox (desktop)
- ✅ Safari (desktop)
- ✅ Chrome (mobile)
- ✅ Safari (mobile)

#### Test 5.2: Dispositivos
**Probar en**:
- ✅ Laptop (micrófono integrado)
- ✅ Desktop (micrófono USB)
- ✅ Smartphone (micrófono integrado)
- ✅ Tablet (micrófono integrado)

## Checklist de Deployment

### Pre-Deployment
- [ ] Código revisado y probado localmente
- [ ] Permisos de IAM configurados
- [ ] Variables de entorno verificadas
- [ ] S3 bucket para transcribe-temp creado

### Deployment
- [ ] Lambda actualizada con nuevo código
- [ ] Permisos de Transcribe agregados
- [ ] Permisos de S3 agregados
- [ ] Frontend desplegado
- [ ] CloudFront invalidado

### Post-Deployment
- [ ] Logs de Lambda sin errores
- [ ] Test de conexión WebSocket exitoso
- [ ] Test de mensaje de texto exitoso
- [ ] Test de mensaje de voz exitoso
- [ ] Audio se reproduce correctamente

## Monitoreo

### CloudWatch Logs
```bash
# Ver logs en tiempo real
aws logs tail /aws/lambda/centli-app-message --follow --region us-east-1

# Buscar errores
aws logs filter-log-events \
  --log-group-name /aws/lambda/centli-app-message \
  --filter-pattern "ERROR" \
  --region us-east-1
```

### Métricas Clave
1. **Transcribe**:
   - Tiempo promedio de transcripción
   - Tasa de error
   - Costo por transcripción

2. **Polly**:
   - Tiempo promedio de síntesis
   - Tamaño promedio de audio
   - Costo por síntesis

3. **Lambda**:
   - Duración promedio
   - Errores
   - Throttles

## Costos Estimados

### Amazon Transcribe
- **Precio**: $0.024 por minuto (español)
- **Estimado**: 1000 conversaciones × 30 segundos = 500 minutos
- **Costo**: $12.00

### Amazon Polly
- **Precio**: $16.00 por 1M caracteres (Neural)
- **Estimado**: 1000 respuestas × 300 caracteres = 300K caracteres
- **Costo**: $4.80

### Total
- **1000 conversaciones**: ~$17.00
- **Por conversación**: ~$0.017

## Rollback Plan

Si algo falla:

1. **Revertir Lambda**:
```bash
# Listar versiones
aws lambda list-versions-by-function \
  --function-name centli-app-message \
  --region us-east-1

# Revertir a versión anterior
aws lambda update-function-code \
  --function-name centli-app-message \
  --s3-bucket centli-assets-777937796305 \
  --s3-key lambda-backups/app_message_backup.zip \
  --region us-east-1
```

2. **Revertir Frontend**:
```bash
cd frontend
git checkout HEAD~1 -- src/context/WebSocketContext.jsx
npm run build
./deploy-frontend.sh
```

## Criterios de Éxito

✅ **Funcionalidad**:
- Usuario puede grabar voz
- Transcripción es precisa (>80%)
- Agente responde correctamente
- Audio se reproduce automáticamente

✅ **Rendimiento**:
- Latencia total <10 segundos
- Sin errores en logs
- Funciona con 10+ usuarios simultáneos

✅ **Calidad**:
- Audio claro y sin distorsión
- Voz natural (Neural)
- Acento apropiado

✅ **Confiabilidad**:
- Manejo de errores robusto
- Cleanup de recursos temporales
- Sin memory leaks

---

**Última actualización**: 13 de marzo de 2026
**Status**: ⏳ Listo para deployment
