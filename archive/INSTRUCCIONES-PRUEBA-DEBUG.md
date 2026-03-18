# Instrucciones para Probar y Debuggear el Chat

## 🚀 Deployment Completado

**Versión desplegada**: `index-DVLPHw7R.js`  
**Fecha**: 13 de marzo de 2026, 13:37 UTC  
**Invalidation ID**: IDM0PPSXFQELQZT6E7K2JMFYPG

---

## 🔍 Cambios Implementados

### 1. Timeout Aumentado
- **Antes**: 500ms para finalizar streaming
- **Ahora**: 1000ms (1 segundo)
- **Razón**: Dar más tiempo para que lleguen todos los chunks

### 2. Delay Aumentado
- **Antes**: 50ms entre agregar mensaje y limpiar stream
- **Ahora**: 100ms
- **Razón**: Asegurar que React renderice el mensaje antes de limpiar

### 3. Logs Mejorados
- Agregados logs detallados en cada paso del proceso
- Logs de longitud de chunks
- Logs cuando se guarda el mensaje final
- Logs cuando se actualiza el array de mensajes

---

## 📝 Instrucciones de Prueba

### Paso 1: Abrir el Chat
1. Abre Chrome o Firefox
2. Presiona **F12** para abrir DevTools
3. Ve a la pestaña **Console**
4. Abre en ventana incógnita: https://db4aulosarsdo.cloudfront.net
5. Haz clic en el botón "Habla con Comfi"

### Paso 2: Enviar un Mensaje
1. Escribe: **"Hola"**
2. Presiona Enter o haz clic en el botón de enviar
3. **OBSERVA LA CONSOLA** - Deberías ver:

```
📤 Sending TEXT message: Hola
📋 Messages array updated, count: 1
📋 Last message: {id: "msg-...", type: "user", content: "Hola", ...}
```

### Paso 3: Observar el Streaming
Cuando llegue la respuesta, deberías ver en la consola:

```
📦 Streaming chunk received (length: XX): [texto del chunk]
🌊 Starting stream (plain text mode)
🆔 Stream message ID: msg-1710418627000
📊 Accumulated length: XX
📦 Streaming chunk received (length: XX): [más texto]
📊 Accumulated length: XXX
...
🏁 Stream ended (timeout)
💾 Saving final message: [texto completo]
📝 Messages array updated, total: 2
📋 Messages array updated, count: 2
📋 Last message: {id: "msg-...", type: "bot", content: "[respuesta completa]", ...}
🧹 Cleaning up stream state
```

### Paso 4: Verificar en la UI
1. **VERIFICA** que el mensaje del usuario ("Hola") permanece visible
2. **VERIFICA** que la respuesta de Comfi aparece y NO desaparece
3. **VERIFICA** que ambos mensajes están en el historial

---

## 🐛 Qué Buscar en los Logs

### ✅ Comportamiento CORRECTO

```javascript
// 1. Mensaje del usuario se agrega
📋 Messages array updated, count: 1

// 2. Comienza streaming
🌊 Starting stream (plain text mode)
🆔 Stream message ID: msg-1710418627000

// 3. Chunks se acumulan
📦 Streaming chunk received (length: 50): Hola, soy Comfi...
📊 Accumulated length: 50
📦 Streaming chunk received (length: 30): tu asistente...
📊 Accumulated length: 80

// 4. Stream termina y se guarda
🏁 Stream ended (timeout)
💾 Saving final message: Hola, soy Comfi, tu asistente...
📝 Messages array updated, total: 2

// 5. Array se actualiza
📋 Messages array updated, count: 2
📋 Last message: {type: "bot", content: "Hola, soy Comfi..."}

// 6. Se limpia el estado
🧹 Cleaning up stream state
```

### ❌ Comportamiento INCORRECTO (Bug)

```javascript
// Si ves esto, el bug persiste:

// 1. Mensaje se guarda
📝 Messages array updated, total: 2
📋 Messages array updated, count: 2

// 2. PERO luego el count vuelve a 1
📋 Messages array updated, count: 1  // ❌ PROBLEMA

// O si ves:
🧹 Cleaning up stream state
📋 Messages array updated, count: 1  // ❌ Se perdió el mensaje
```

---

## 🔧 Debugging Adicional

### Ver Estado de React
1. Instala React DevTools (extensión de Chrome/Firefox)
2. Abre React DevTools
3. Busca el componente `WebSocketProvider`
4. Observa el estado:
   - `messages`: Array de mensajes (debe crecer, nunca decrecer)
   - `isStreaming`: true durante streaming, false después
   - `currentStreamMessage`: texto durante streaming, '' después

### Ver Mensajes WebSocket
1. En DevTools, ve a la pestaña **Network**
2. Filtra por **WS** (WebSocket)
3. Haz clic en la conexión WebSocket
4. Ve a la pestaña **Messages**
5. Observa los mensajes que llegan del servidor

---

## 📊 Escenarios de Prueba

### Prueba 1: Mensaje Simple
```
Usuario: "Hola"
Esperado: Respuesta de Comfi visible y permanente
```

### Prueba 2: Pregunta sobre Comfama
```
Usuario: "¿Qué es Comfama?"
Esperado: Respuesta larga con streaming visible, luego permanente
```

### Prueba 3: Múltiples Mensajes
```
Usuario: "Hola"
[Esperar respuesta]
Usuario: "¿Cómo me afilio?"
[Esperar respuesta]
Usuario: "¿Cuáles son las tarifas?"
Esperado: Los 3 pares de mensajes visibles en el historial
```

### Prueba 4: FAQ
```
Usuario: Hacer clic en botón FAQ "¿Cómo me afilio?"
Esperado: Pregunta y respuesta visibles
```

---

## 🚨 Si el Problema Persiste

### Opción 1: Captura de Pantalla de Logs
1. Reproduce el problema
2. Captura de pantalla de la consola completa
3. Comparte la captura

### Opción 2: Copiar Logs
1. Reproduce el problema
2. Haz clic derecho en la consola
3. "Save as..." o copia todo el texto
4. Comparte los logs

### Opción 3: Video
1. Graba la pantalla mientras reproduces el problema
2. Muestra tanto la UI como la consola
3. Comparte el video

---

## 🔍 Información Técnica

### Flujo de Datos Actual

```
1. Usuario envía mensaje
   ↓
2. WebSocket envía a Lambda
   ↓
3. Lambda invoca Bedrock Agent
   ↓
4. Bedrock Agent responde con chunks de TEXTO PLANO
   ↓
5. Lambda envía cada chunk al WebSocket
   ↓
6. Frontend recibe chunks (modo texto plano, no JSON)
   ↓
7. Frontend acumula chunks en accumulatedMessageRef
   ↓
8. Frontend muestra streaming en currentStreamMessage
   ↓
9. Después de 1000ms sin chunks, timeout se activa
   ↓
10. Frontend guarda mensaje en array messages
   ↓
11. Después de 100ms, limpia estado de streaming
   ↓
12. Mensaje debe permanecer visible
```

### Problema Conocido
El backend está enviando **texto plano** en lugar de mensajes JSON estructurados. El frontend maneja esto en el bloque `catch` del `onmessage`, pero puede haber problemas de sincronización.

### Posible Solución Alternativa
Si el problema persiste, podríamos modificar el Lambda para enviar mensajes JSON estructurados:
```python
# En lugar de:
apigateway.post_to_connection(
    ConnectionId=connection_id,
    Data=chunk_text.encode('utf-8')
)

# Usar:
apigateway.post_to_connection(
    ConnectionId=connection_id,
    Data=json.dumps({
        "msg_type": "stream_chunk",
        "message": chunk_text
    }).encode('utf-8')
)
```

---

## ✅ Checklist de Verificación

- [ ] Abrí el sitio en ventana incógnita
- [ ] Abrí DevTools (F12) y fui a Console
- [ ] Envié un mensaje "Hola"
- [ ] Vi los logs en la consola
- [ ] El mensaje del usuario permanece visible
- [ ] La respuesta de Comfi aparece
- [ ] La respuesta de Comfi NO desaparece
- [ ] Ambos mensajes están en el historial
- [ ] Copié los logs de la consola (si hay problema)

---

**Próximo paso**: Prueba el chat y comparte los logs de la consola para que pueda ver exactamente qué está pasando.
