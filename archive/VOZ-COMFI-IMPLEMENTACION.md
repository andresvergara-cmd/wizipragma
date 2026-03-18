# Implementación de Voz para Comfi

## ✅ Completado

Se ha implementado la funcionalidad de voz para el asistente Comfi usando Amazon Polly.

## Componentes Implementados

### 1. Backend - Amazon Polly TTS
**Archivo**: `src_aws/app_inference/polly_tts.py`

**Funcionalidades**:
- Síntesis de texto a voz usando Amazon Polly Neural
- Voz: **Mia** (es-MX) - Femenina, amigable y clara
- Formato: MP3 a 24kHz
- Soporte para SSML (control avanzado de pronunciación)
- Manejo de textos largos (hasta 3000 caracteres)

**Funciones principales**:
```python
synthesize_speech(text, voice_id='Mia') -> dict
synthesize_speech_ssml(ssml_text, voice_id='Mia') -> dict
get_available_voices(language_code='es-MX') -> list
```

### 2. Backend - Handler de Mensajes
**Archivo**: `src_aws/app_message/app_message.py`

**Cambios**:
- Agregado parámetro `include_audio` en `process_text_message()`
- Generación automática de audio cuando se solicita
- Respuesta incluye tanto texto como audio en base64

**Flujo**:
1. Usuario envía mensaje con `includeAudio: true`
2. Bedrock Agent genera respuesta de texto
3. Polly sintetiza el texto a audio
4. Se envía texto + audio al frontend

### 3. Frontend - WebSocket Context
**Archivo**: `frontend/src/context/WebSocketContext.jsx`

**Cambios**:
- Agregado estado `isPlayingAudio`
- Función `playAudio(audioBase64)` para reproducir audio
- Función `stopAudio()` para detener reproducción
- Soporte para `includeAudio` en mensajes

### 4. Frontend - Chat Context
**Archivo**: `frontend/src/context/ChatContext.jsx`

**Cambios**:
- Agregado estado `voiceEnabled` (toggle global)
- `sendTextMessage()` ahora acepta parámetro `withVoice`
- Expone funciones `playAudio` y `stopAudio`

### 5. Frontend - Chat Widget
**Archivo**: `frontend/src/components/Chat/ChatWidget.jsx`

**Cambios**:
- Botón toggle de voz en el header (🔊/🔇)
- Indicador visual cuando la voz está activa
- Animación de pulso cuando está habilitada

**Archivo CSS**: `frontend/src/components/Chat/ChatWidget.css`
- Estilos para botón de voz
- Animación `voicePulse` para indicador activo

## Cómo Funciona

### Flujo Completo

1. **Usuario activa voz**:
   - Click en botón 🔊 en el header
   - `voiceEnabled` se activa

2. **Usuario envía mensaje**:
   - Frontend envía `{message: "...", includeAudio: true}`
   - Lambda recibe y procesa

3. **Backend genera respuesta**:
   - Bedrock Agent genera texto
   - Polly sintetiza audio (MP3)
   - Respuesta: `{text: "...", audio: "base64..."}`

4. **Frontend reproduce**:
   - Recibe audio en base64
   - Convierte a Blob
   - Crea Audio element
   - Reproduce automáticamente

## Voces Disponibles

### Español de México (es-MX) - RECOMENDADO
- **Mia** (Femenina) ✅ - Voz actual de Comfi
- **Andrés** (Masculina)

### Español de España (es-ES)
- **Lucia** (Femenina)
- **Sergio** (Masculina)

### Español de Estados Unidos (es-US)
- **Lupe** (Femenina)
- **Pedro** (Masculina)

## Configuración

### Cambiar Voz

Editar `src_aws/app_inference/polly_tts.py`:

```python
VOICE_ID = 'Lucia'  # Cambiar a otra voz
LANGUAGE_CODE = 'es-ES'  # Cambiar idioma si es necesario
```

### Ajustar Calidad de Audio

```python
SAMPLE_RATE = '24000'  # 24kHz (alta calidad)
# Opciones: '8000', '16000', '22050', '24000'
```

### Usar SSML para Control Avanzado

```python
ssml = '''<speak>
    <prosody rate="medium" pitch="medium">
        ¡Hola! Soy Comfi.
        <break time="300ms"/>
        ¿En qué puedo ayudarte?
    </prosody>
</speak>'''

result = synthesize_speech_ssml(ssml)
```

## Deployment

### Backend

1. Actualizar Lambda `centli-app-message`:
```bash
cd src_aws/app_message
zip -r function.zip .
aws lambda update-function-code \
  --function-name centli-app-message \
  --zip-file fileb://function.zip
```

2. Agregar permisos de Polly al rol de Lambda:
```json
{
  "Effect": "Allow",
  "Action": [
    "polly:SynthesizeSpeech",
    "polly:DescribeVoices"
  ],
  "Resource": "*"
}
```

### Frontend

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://comfi-frontend-pragma/ --delete
aws cloudfront create-invalidation \
  --distribution-id E2UWNXJTS2NM3V \
  --paths "/*"
```

## Testing

### Test Backend (Polly)

```bash
cd src_aws/app_inference
python3 polly_tts.py
```

Salida esperada:
```
✅ Synthesis successful: XXXXX bytes

📢 Available voices for es-MX:
  - Mia (Female)
  - Andrés (Male)
```

### Test Frontend

1. Abrir https://db4aulosarsdo.cloudfront.net
2. Click en botón 🔊 para activar voz
3. Hacer una pregunta
4. Verificar que se reproduce audio automáticamente

## Costos

### Amazon Polly Neural Voices
- **Precio**: $16 USD por 1 millón de caracteres
- **Ejemplo**: 
  - Respuesta promedio: 200 caracteres
  - 1000 respuestas = $3.20 USD
  - 10,000 respuestas = $32 USD

### Optimización de Costos

1. **Caché de respuestas comunes**:
   - Guardar audio de FAQs en S3
   - Reutilizar para preguntas frecuentes

2. **Truncar respuestas largas**:
   - Límite actual: 3000 caracteres
   - Considerar límite más bajo (500-1000)

3. **Voz opcional**:
   - Usuario decide cuándo activar
   - No todas las respuestas necesitan audio

## Próximos Pasos

### Mejoras Sugeridas

1. **Caché de Audio**:
   - Guardar audio de FAQs en S3
   - Reducir llamadas a Polly

2. **Control de Velocidad**:
   - Botón para ajustar velocidad de reproducción
   - Opciones: 0.75x, 1x, 1.25x, 1.5x

3. **Subtítulos**:
   - Mostrar texto mientras se reproduce audio
   - Resaltar palabra actual

4. **Personalización**:
   - Permitir al usuario elegir voz
   - Guardar preferencia en localStorage

5. **Indicador Visual**:
   - Animación de onda de audio
   - Barra de progreso de reproducción

6. **Auto-play Inteligente**:
   - Solo reproducir si usuario está activo
   - Pausar si cambia de pestaña

## Troubleshooting

### Audio no se reproduce

1. Verificar que el navegador soporte audio:
```javascript
const audio = new Audio()
console.log('Audio supported:', audio.canPlayType('audio/mpeg'))
```

2. Verificar permisos de autoplay:
   - Chrome requiere interacción del usuario
   - Safari puede bloquear autoplay

3. Verificar base64:
```javascript
console.log('Audio base64 length:', audioBase64.length)
console.log('First 100 chars:', audioBase64.substring(0, 100))
```

### Error en Polly

1. Verificar permisos IAM del rol Lambda
2. Verificar límite de caracteres (max 3000)
3. Verificar región (debe ser us-east-1)

### Latencia alta

1. Considerar pre-generar audio de FAQs
2. Usar formato OGG (más compacto que MP3)
3. Reducir sample rate a 16kHz

## Documentación

- [Amazon Polly Docs](https://docs.aws.amazon.com/polly/)
- [Polly Neural Voices](https://docs.aws.amazon.com/polly/latest/dg/neural-voices.html)
- [SSML Reference](https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

## Fecha de Implementación

13 de marzo de 2026
