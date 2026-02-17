# Estado de Modelos de Voz e Imágenes - CENTLI

## 📋 Resumen Ejecutivo

**Modelos Especificados en Diseño**:
- ✅ **Voz**: AWS Bedrock Nova Sonic (transcripción y síntesis)
- ✅ **Imágenes**: AWS Bedrock Nova Canvas (análisis de imágenes)

**Estado de Implementación**:
- ⚠️ **Voz**: Especificado pero NO implementado (placeholder)
- ⚠️ **Imágenes**: Especificado pero NO implementado (placeholder)

**Razón**: Enfoque del hackathon en funcionalidad core (texto + Action Groups). Voz e imágenes quedaron como "Could Have" (baja prioridad).

---

## 🎯 Modelos Especificados

### 1. Nova Sonic (Voz)

**Modelo**: `amazon.nova-sonic-v1:0`  
**Propósito**: Procesamiento de voz bidireccional  
**Capacidades**:
- Speech-to-Text (transcripción)
- Text-to-Speech (síntesis)
- Soporte para español mexicano (es-MX)

**Especificado en**:
- `aidlc-docs/construction/agentcore-orchestration/nfr-requirements/tech-stack-decisions.md`
- `aidlc-docs/inception/requirements/requirements.md` (FR-012, FR-013)

**Configuración Diseñada**:
```yaml
Language: es-MX (Mexican Spanish)
Voice: Neutral gender, professional tone
Speaking rate: Normal
Processing mode: Batch (< 3s latency target)
```

### 2. Nova Canvas (Imágenes)

**Modelo**: `amazon.nova-canvas-v1:0`  
**Propósito**: Análisis de imágenes  
**Capacidades**:
- Object detection (detección de objetos)
- Text extraction / OCR (extracción de texto)
- Scene understanding (comprensión de escena)

**Especificado en**:
- `aidlc-docs/construction/agentcore-orchestration/nfr-requirements/tech-stack-decisions.md`
- `aidlc-docs/inception/requirements/requirements.md` (FR-015)

**Configuración Diseñada**:
```yaml
Analysis types: Object detection, text extraction, scene understanding
Confidence threshold: 0.7 (70%)
Max objects: 10 per image
```

---

## 🔍 Estado de Implementación

### Frontend (Unit 4)

#### Voz - `frontend/js/voice-manager.js`

**Estado**: ⚠️ Parcialmente implementado (captura de audio solamente)

**Implementado**:
- ✅ Captura de audio usando MediaRecorder API
- ✅ Grabación en formato WebM
- ✅ Límite de 30 segundos
- ✅ Conversión a base64
- ✅ Envío por WebSocket

**NO Implementado**:
- ❌ Integración con Nova Sonic (transcripción)
- ❌ Reproducción de respuestas de voz
- ❌ Síntesis de texto a voz

**Código Actual**:
```javascript
// voice-manager.js - Solo captura
async startRecording() {
  this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  this.mediaRecorder = new MediaRecorder(this.stream, {
    mimeType: 'audio/webm'
  });
  // ... captura y envío
}
```

#### Imágenes - `frontend/js/image-manager.js`

**Estado**: ⚠️ Parcialmente implementado (captura de imagen solamente)

**Implementado**:
- ✅ Selección de archivo de imagen
- ✅ Validación de formato (JPEG, PNG)
- ✅ Compresión de imagen
- ✅ Preview de imagen
- ✅ Conversión a base64
- ✅ Envío por WebSocket

**NO Implementado**:
- ❌ Integración con Nova Canvas (análisis)
- ❌ Procesamiento de resultados de análisis
- ❌ Visualización de objetos detectados

**Código Actual**:
```javascript
// image-manager.js - Solo captura y compresión
async compressImage(file) {
  // Comprime imagen a JPEG
  canvas.toBlob((blob) => resolve(blob), 'image/jpeg', 0.8);
}
```

### Backend (Unit 2)

#### Voz - `src_aws/app_message/app_message.py`

**Estado**: ❌ NO implementado (placeholder)

**Código Actual**:
```python
def process_voice_message(audio_data: str, session_id: str, user_id: str, connection_id: str) -> dict:
    """
    Process voice message (base64 audio).
    
    Note: Simplified for hackathon. Full implementation would:
    1. Decode base64 audio
    2. Invoke Nova Sonic for transcription
    3. Process text through AgentCore
    4. Invoke Nova Sonic for synthesis
    5. Return audio response
    """
    try:
        # Placeholder: Return text response
        return {
            "type": "TEXT",
            "content": "Voice processing not yet implemented. Please use text.",
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
    except Exception as e:
        print(f"ERROR: Voice processing failed: {str(e)}")
        return {"error": f"Voice processing failed: {str(e)}"}
```

**Mensaje al Usuario**: "Voice processing not yet implemented. Please use text."

#### Imágenes - `src_aws/app_message/app_message.py`

**Estado**: ❌ NO implementado (placeholder)

**Código Actual**:
```python
def process_image_message(image_data: str, session_id: str, user_id: str, connection_id: str) -> dict:
    """
    Process image message (base64 image).
    
    Note: Simplified for hackathon. Full implementation would:
    1. Decode base64 image
    2. Upload to S3
    3. Invoke Nova Canvas for analysis
    4. Process results through AgentCore
    5. Return response
    """
    try:
        # Placeholder: Return text response
        return {
            "type": "TEXT",
            "content": "Image processing not yet implemented. Please use text.",
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
    except Exception as e:
        print(f"ERROR: Image processing failed: {str(e)}")
        return {"error": f"Image processing failed: {str(e)}"}
```

**Mensaje al Usuario**: "Image processing not yet implemented. Please use text."

---

## 📊 Tabla de Estado

| Componente | Modelo Especificado | Frontend | Backend | Estado General |
|------------|---------------------|----------|---------|----------------|
| **Voz - Entrada** | Nova Sonic | ✅ Captura | ❌ Transcripción | ⚠️ Parcial |
| **Voz - Salida** | Nova Sonic | ❌ Reproducción | ❌ Síntesis | ❌ No implementado |
| **Imagen - Entrada** | Nova Canvas | ✅ Captura | ❌ Análisis | ⚠️ Parcial |
| **Imagen - Salida** | Nova Canvas | ❌ Visualización | ❌ Procesamiento | ❌ No implementado |

---

## 🏗️ Arquitectura Diseñada vs Implementada

### Arquitectura Diseñada (Documentación)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flujo de Voz Diseñado                         │
└─────────────────────────────────────────────────────────────────┘

Frontend                    Backend                    AWS Bedrock
   │                           │                            │
   │ 1. Captura audio          │                            │
   ├──────────────────────────>│                            │
   │                           │ 2. Invoke Nova Sonic       │
   │                           ├───────────────────────────>│
   │                           │    (Speech-to-Text)        │
   │                           │<───────────────────────────┤
   │                           │ 3. Texto transcrito        │
   │                           │                            │
   │                           │ 4. Invoke AgentCore        │
   │                           ├───────────────────────────>│
   │                           │    (Claude 3.5 Sonnet)     │
   │                           │<───────────────────────────┤
   │                           │ 5. Respuesta texto         │
   │                           │                            │
   │                           │ 6. Invoke Nova Sonic       │
   │                           ├───────────────────────────>│
   │                           │    (Text-to-Speech)        │
   │                           │<───────────────────────────┤
   │                           │ 7. Audio sintetizado       │
   │<──────────────────────────┤                            │
   │ 8. Reproduce audio        │                            │
```

### Arquitectura Implementada (Actual)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flujo de Voz Actual                           │
└─────────────────────────────────────────────────────────────────┘

Frontend                    Backend                    AWS Bedrock
   │                           │                            │
   │ 1. Captura audio ✅       │                            │
   ├──────────────────────────>│                            │
   │                           │ 2. ❌ NO IMPLEMENTADO      │
   │                           │    (Nova Sonic)            │
   │                           │                            │
   │<──────────────────────────┤                            │
   │ 3. Mensaje: "Not          │                            │
   │    implemented"           │                            │
```

---

## 🎯 Razón de No Implementación

### Contexto del Hackathon

**Priorización MoSCoW**:
- **Must Have**: Texto + AgentCore + Action Groups ✅
- **Should Have**: WebSocket + Frontend básico ✅
- **Could Have**: Voz + Imágenes ⚠️ (NO implementado)
- **Won't Have**: Autenticación biométrica real ❌

**Decisión del Equipo**:
1. Enfoque en funcionalidad core (texto)
2. Demostrar AgentCore + Action Groups
3. Voz e imágenes como "demo de concepto" (captura solamente)
4. Tiempo limitado (8 horas)

**Documentado en**:
- `aidlc-docs/inception/user-stories/stories.md` (US-012, US-013, US-015 marcadas como "Could Have")
- `aidlc-docs/construction/plans/agentcore-orchestration-code-generation-plan.md` (voz e imagen como "simplified placeholders")

---

## 🔧 Implementación Completa Requerida

### Para Nova Sonic (Voz)

#### Backend - `src_aws/app_message/app_message.py`

```python
import boto3
import base64

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def process_voice_message(audio_data: str, session_id: str, user_id: str, connection_id: str) -> dict:
    """Process voice message through Nova Sonic."""
    try:
        # 1. Decode base64 audio
        audio_bytes = base64.b64decode(audio_data)
        
        # 2. Invoke Nova Sonic for transcription
        transcribe_response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-sonic-v1:0',
            body=json.dumps({
                'audio': audio_data,
                'task': 'transcribe',
                'language': 'es-MX'
            })
        )
        
        transcribed_text = json.loads(transcribe_response['body'].read())['text']
        
        # 3. Process text through AgentCore
        agent_response = bedrock_agent.invoke_agent(
            agentId=AGENTCORE_ID,
            agentAliasId=os.environ.get('AGENTCORE_ALIAS_ID'),
            sessionId=session_id,
            inputText=transcribed_text
        )
        
        response_text = extract_agent_response(agent_response)
        
        # 4. Invoke Nova Sonic for synthesis
        synthesis_response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-sonic-v1:0',
            body=json.dumps({
                'text': response_text,
                'task': 'synthesize',
                'language': 'es-MX',
                'voice': 'neutral'
            })
        )
        
        audio_output = json.loads(synthesis_response['body'].read())['audio']
        
        return {
            "type": "VOICE",
            "content": audio_output,  # base64 audio
            "text": response_text,     # texto para fallback
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
        
    except Exception as e:
        print(f"ERROR: Voice processing failed: {str(e)}")
        return {"error": f"Voice processing failed: {str(e)}"}
```

#### Frontend - `frontend/js/voice-manager.js`

```javascript
// Agregar reproducción de audio
playAudioResponse(base64Audio) {
  const audioBlob = this.base64ToBlob(base64Audio, 'audio/webm');
  const audioUrl = URL.createObjectURL(audioBlob);
  const audio = new Audio(audioUrl);
  audio.play();
}

base64ToBlob(base64, mimeType) {
  const byteCharacters = atob(base64);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: mimeType });
}
```

### Para Nova Canvas (Imágenes)

#### Backend - `src_aws/app_message/app_message.py`

```python
def process_image_message(image_data: str, session_id: str, user_id: str, connection_id: str) -> dict:
    """Process image message through Nova Canvas."""
    try:
        # 1. Decode base64 image
        image_bytes = base64.b64decode(image_data)
        
        # 2. Upload to S3
        s3_key = f"images/{session_id}/{uuid.uuid4()}.jpg"
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=ASSETS_BUCKET,
            Key=s3_key,
            Body=image_bytes,
            ContentType='image/jpeg'
        )
        
        # 3. Invoke Nova Canvas for analysis
        analysis_response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            body=json.dumps({
                'image': image_data,
                'tasks': ['object_detection', 'text_extraction', 'scene_understanding'],
                'confidence_threshold': 0.7,
                'max_objects': 10
            })
        )
        
        analysis_results = json.loads(analysis_response['body'].read())
        
        # 4. Format results for AgentCore
        analysis_text = format_analysis_for_agent(analysis_results)
        
        # 5. Process through AgentCore
        agent_response = bedrock_agent.invoke_agent(
            agentId=AGENTCORE_ID,
            agentAliasId=os.environ.get('AGENTCORE_ALIAS_ID'),
            sessionId=session_id,
            inputText=f"Analiza esta imagen: {analysis_text}"
        )
        
        response_text = extract_agent_response(agent_response)
        
        return {
            "type": "IMAGE_ANALYSIS",
            "content": response_text,
            "analysis": analysis_results,
            "s3_key": s3_key,
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
        
    except Exception as e:
        print(f"ERROR: Image processing failed: {str(e)}")
        return {"error": f"Image processing failed: {str(e)}"}

def format_analysis_for_agent(analysis_results):
    """Format Nova Canvas results for AgentCore."""
    objects = analysis_results.get('objects', [])
    text = analysis_results.get('text', '')
    scene = analysis_results.get('scene', '')
    
    return f"Objetos detectados: {', '.join([o['label'] for o in objects])}. Texto: {text}. Escena: {scene}"
```

---

## 📝 Conclusión

**Respuesta a la pregunta**: "¿Qué modelo se está usando para voz e imágenes?"

**Modelos Especificados**:
- ✅ **Voz**: AWS Bedrock Nova Sonic (`amazon.nova-sonic-v1:0`)
- ✅ **Imágenes**: AWS Bedrock Nova Canvas (`amazon.nova-canvas-v1:0`)

**Estado de Implementación**:
- ⚠️ **Voz**: Especificado en diseño, pero NO implementado en código (placeholder)
- ⚠️ **Imágenes**: Especificado en diseño, pero NO implementado en código (placeholder)

**Funcionalidad Actual**:
- ✅ Frontend captura audio e imágenes
- ❌ Backend NO procesa con Nova Sonic/Canvas
- ❌ Usuario recibe mensaje: "Not yet implemented. Please use text."

**Razón**:
- Priorización del hackathon: Enfoque en texto + AgentCore + Action Groups
- Voz e imágenes clasificadas como "Could Have" (baja prioridad)
- Tiempo limitado (8 horas)

**Para Implementar**:
- Agregar código de invocación de Nova Sonic (transcripción + síntesis)
- Agregar código de invocación de Nova Canvas (análisis de imágenes)
- Actualizar frontend para reproducir audio y mostrar resultados de análisis
- Estimado: 4-6 horas adicionales de desarrollo

---

**Validado por**: AI Agent (Kiro)  
**Fecha**: 2026-02-17T18:30:00Z  
**Ambiente**: AWS us-east-1 (Cuenta: 777937796305)
