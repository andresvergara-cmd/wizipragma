# Plan: Activar Nova Sonic para Conversación Bidireccional

## Fecha
13 de marzo de 2026

## Objetivo
Implementar conversación de voz bidireccional usando Amazon Nova Sonic:
- Usuario habla → Nova Sonic STT → Texto → Bedrock Agent → Texto → Nova Sonic TTS → Audio → Usuario escucha

## Ventajas de Nova Sonic
✅ Streaming bidireccional (STT + TTS en un solo modelo)
✅ Mejor calidad para conversaciones de voz
✅ Integrado con Bedrock
✅ Soluciona el problema de tamaño de payload (streaming)

## Desafíos a Resolver

### 1. Dependencias Faltantes
Nova Sonic requiere:
- `pydub` - Para conversión de audio WebM a PCM
- `ffmpeg` - Requerido por pydub

**Solución**: Crear Lambda Layer con estas dependencias

### 2. Conversión de Audio
- Frontend graba en WebM
- Nova Sonic requiere PCM (16kHz, 16-bit, mono)

**Solución**: Usar pydub para convertir en Lambda

### 3. Tamaño de Payload
- Audio en base64 es muy grande para WebSocket (>128KB)
- Nova Sonic usa streaming

**Solución**: Usar streaming de Nova Sonic directamente

## Arquitectura Propuesta

### Flujo Completo
```
1. Usuario presiona 🎤 y habla
   ↓
2. Frontend graba audio (WebM)
   ↓
3. Frontend envía audio base64 vía WebSocket
   ↓
4. Lambda recibe audio
   ↓
5. Lambda convierte WebM → PCM (pydub)
   ↓
6. Lambda invoca Nova Sonic STT
   ↓
7. Nova Sonic transcribe → Texto
   ↓
8. Lambda envía texto a Bedrock Agent
   ↓
9. Bedrock Agent genera respuesta
   ↓
10. Lambda invoca Nova Sonic TTS con streaming
    ↓
11. Nova Sonic genera audio en chunks
    ↓
12. Lambda envía chunks vía WebSocket
    ↓
13. Frontend ensambla y reproduce audio
```

## Pasos de Implementación

### Paso 1: Crear Lambda Layer con Dependencias
```bash
# Crear directorio para layer
mkdir -p lambda-layer/python

# Instalar dependencias
pip install pydub -t lambda-layer/python/

# Descargar ffmpeg estático
# (ffmpeg-python no funciona en Lambda, necesitamos binario estático)
```

**Tiempo estimado**: 30 minutos

### Paso 2: Actualizar Lambda con Nova Sonic
**Archivos a modificar**:
- `app_message.py` - Agregar import de Nova Sonic
- `process_voice_message()` - Implementar STT con Nova Sonic
- `process_text_message()` - Agregar opción de TTS con Nova Sonic

**Tiempo estimado**: 45 minutos

### Paso 3: Actualizar Frontend
**Archivos a modificar**:
- `WebSocketContext.jsx` - Manejar chunks de audio
- `ChatWidget.jsx` - Mejorar UI de grabación

**Tiempo estimado**: 30 minutos

### Paso 4: Testing y Ajustes
- Probar STT (voz → texto)
- Probar TTS (texto → voz)
- Probar flujo completo
- Ajustar calidad de audio

**Tiempo estimado**: 45 minutos

## Tiempo Total Estimado
**2.5 - 3 horas**

## Alternativa Rápida (Sin Lambda Layer)

Si no queremos crear Lambda Layer, podemos:

### Opción A: Solo TTS con Nova Sonic (Sin STT)
- Mantener texto como input
- Usar Nova Sonic solo para TTS con streaming
- Evita necesidad de pydub/ffmpeg
- **Tiempo**: 1 hora

### Opción B: Usar S3 para Audio
- Subir audio a S3
- Lambda procesa desde S3
- Enviar URL de audio al frontend
- **Tiempo**: 1.5 horas

## Recomendación

### Para Demo Inmediato (Hoy)
**Opción A**: Solo TTS con Nova Sonic
- ✅ Resuelve problema de tamaño de payload
- ✅ Mejor calidad de voz
- ✅ Streaming funciona
- ❌ No hay STT (usuario sigue escribiendo)

### Para Implementación Completa (Mañana)
**Implementación Full**: STT + TTS con Lambda Layer
- ✅ Conversación bidireccional completa
- ✅ Usuario puede hablar
- ✅ Mejor experiencia de usuario
- ⏰ Requiere más tiempo

## ¿Qué Prefieres?

1. **Rápido (1 hora)**: Solo TTS con Nova Sonic, usuario escribe
2. **Completo (3 horas)**: STT + TTS, conversación de voz completa
3. **Híbrido (1.5 horas)**: TTS con Nova Sonic + S3 para audio

---

**Esperando tu decisión para proceder...**
