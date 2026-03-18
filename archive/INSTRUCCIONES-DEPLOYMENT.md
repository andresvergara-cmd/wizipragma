# 🚀 Instrucciones de Deployment - Corrección de Audio

## Problema Encontrado

Gracias a los logs detallados, identificamos el error exacto:

```
❌ ERROR: Parameter validation failed:
Invalid value for parameter Settings.MaxSpeakerLabels, value: 1, valid min value: 2
```

**Solución**: Removimos el parámetro `MaxSpeakerLabels` de la configuración de Transcribe.

## 📋 Pasos para Desplegar

### Paso 1: Configurar Credenciales de AWS

Ejecuta el script de configuración:

```bash
./configure-aws-credentials.sh
```

El script te pedirá:
1. **AWS Access Key ID**: [Pegar tu Access Key ID]
2. **AWS Secret Access Key**: [Pegar tu Secret Access Key]
3. **AWS Session Token**: [Pegar tu Session Token]

El script verificará automáticamente que las credenciales sean válidas.

### Paso 2: Desplegar la Corrección

Una vez configuradas las credenciales, ejecuta:

```bash
./deploy-lambda-fix.sh
```

Este script:
1. ✅ Empaqueta el código corregido
2. ✅ Despliega a Lambda `centli-app-message`
3. ✅ Espera a que Lambda esté lista
4. ✅ Limpia archivos temporales

### Paso 3: Probar la Funcionalidad

#### 3.1 Monitorear Logs (Terminal 1)

```bash
./monitor-logs.sh
```

#### 3.2 Probar en Navegador (Terminal 2)

1. Abrir: https://db4aulosarsdo.cloudfront.net
2. Click en botón 🎤
3. Hablar: "Hola Comfi"
4. Click en ⏹️

#### 3.3 Verificar Logs

Deberías ver en la terminal:

```
🎙️ TRANSCRIBE_AUDIO STARTED
📤 Uploading to S3: s3://centli-assets-777937796305/transcribe-temp/...
✅ Upload completed
🚀 Starting transcription job: transcribe-session-...
✅ Transcription job started
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
```

#### 3.4 Verificar en Navegador

Deberías ver:
- ✅ Mensaje: "🎤 Hola Comfi" (transcripción)
- ✅ Respuesta de Comfi en texto
- ✅ Audio se reproduce automáticamente

## 🔧 Troubleshooting

### Error: "Credenciales inválidas"

**Causa**: Las credenciales ingresadas son incorrectas o expiraron.

**Solución**:
1. Obtener nuevas credenciales de AWS Console
2. Ejecutar `./configure-aws-credentials.sh` de nuevo
3. Pegar las nuevas credenciales

### Error: "Lambda timeout"

**Causa**: Transcribe está tardando más de 30 segundos.

**Solución**:
1. Grabar audio más corto (<10 segundos)
2. Verificar que el audio tenga voz clara
3. Reintentar

### Error: "No se escucha el audio"

**Causa**: Problema con Polly TTS o reproducción en navegador.

**Solución**:
1. Verificar logs para ver si hay error en TTS
2. Verificar volumen del navegador
3. Probar en Chrome (mejor soporte)

## 📊 Flujo Completo

```
Usuario habla (3 segundos)
    ↓
Frontend graba WebM (~23KB)
    ↓
Lambda recibe y sube a S3
    ↓
Transcribe procesa (5-15 segundos)
    ↓
Lambda obtiene transcripción
    ↓
Frontend muestra: "🎤 [texto]"
    ↓
Lambda invoca Bedrock Agent (2-5 segundos)
    ↓
Agent genera respuesta
    ↓
Lambda invoca Polly TTS (1-3 segundos)
    ↓
Polly genera audio MP3
    ↓
Lambda envía audio al frontend
    ↓
Frontend reproduce audio
    ↓
Usuario escucha respuesta
```

**Tiempo total**: 10-25 segundos

## ✅ Criterios de Éxito

### Logs
- ✅ No hay errores (❌)
- ✅ Todos los pasos completan con ✅
- ✅ Transcripción es correcta
- ✅ Audio se envía exitosamente

### Frontend
- ✅ Aparece transcripción
- ✅ Aparece respuesta de Comfi
- ✅ Audio se reproduce automáticamente
- ✅ Audio se escucha claro

## 📝 Archivos Modificados

- ✅ `src_aws/app_message/transcribe_stt.py` - Removido MaxSpeakerLabels
- ✅ `src_aws/app_message/app_message.py` - Logs detallados
- ✅ Scripts de deployment creados

## 💰 Costos

- **Por conversación**: ~$0.017
- **1000 conversaciones**: ~$17.00

## 🎓 Lecciones Aprendidas

1. **Logs detallados son esenciales** - Encontramos el problema en 1 minuto
2. **Validación de parámetros** - AWS valida antes de ejecutar
3. **Documentación es clave** - Leer docs de AWS evita errores
4. **Testing sistemático** - Logs con emojis facilitan debug

## 📚 Documentación Relacionada

- `SOLUCION-AUDIO-FINAL.md` - Detalles técnicos de la solución
- `TRANSCRIBE-POLLY-DEPLOYMENT.md` - Arquitectura completa
- `TRANSCRIBE-POLLY-TESTING.md` - Plan de pruebas
- `INSTRUCCIONES-DEBUG.md` - Guía de debugging

---

**Última actualización**: 13 de marzo de 2026, 16:05 PM
**Status**: ✅ Listo para desplegar
**Tiempo estimado**: 5 minutos
