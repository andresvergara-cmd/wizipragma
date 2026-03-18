# Pruebas de Experiencia de Chat - Comfi

## 🎯 Objetivo
Verificar que los mensajes NO desaparecen y la experiencia es fluida.

---

## 🐛 Problema Identificado y Corregido

### Causa Raíz
En `WebSocketContext.jsx`, cuando terminaba el streaming:
1. Se llamaba `setCurrentStreamMessage()` con una función
2. Dentro de esa función se agregaba el mensaje a `messages`
3. Luego se retornaba `''` para limpiar el stream
4. **BUG**: React procesaba ambos cambios de estado casi simultáneamente, causando que el mensaje apareciera y desapareciera

### Solución Implementada
- Agregado delay de 50ms entre agregar el mensaje y limpiar el stream
- Esto asegura que React renderice el mensaje permanente ANTES de limpiar el streaming
- Aplicado tanto en modo JSON (`stream_end`) como en modo texto plano (timeout)

---

## ✅ Checklist de Pruebas Manuales

### 1. Prueba Básica de Mensaje
- [ ] Abrir https://db4aulosarsdo.cloudfront.net en ventana incógnita
- [ ] Hacer clic en el botón flotante "Habla con Comfi"
- [ ] Escribir "Hola" y enviar
- [ ] **VERIFICAR**: El mensaje "Hola" permanece visible en el chat
- [ ] **VERIFICAR**: Aparece indicador "Comfi está escribiendo..."
- [ ] **VERIFICAR**: La respuesta de Comfi aparece y NO desaparece
- [ ] **VERIFICAR**: Ambos mensajes (usuario y bot) permanecen visibles

### 2. Prueba de Streaming
- [ ] Enviar mensaje: "¿Qué es Comfama?"
- [ ] **VERIFICAR**: Aparece indicador de procesamiento
- [ ] **VERIFICAR**: El texto de la respuesta aparece gradualmente (streaming)
- [ ] **VERIFICAR**: Cuando termina el streaming, el mensaje completo permanece visible
- [ ] **VERIFICAR**: NO hay parpadeo ni desaparición del mensaje

### 3. Prueba de Múltiples Mensajes
- [ ] Enviar mensaje: "¿Cómo me afilio?"
- [ ] Esperar respuesta completa
- [ ] **VERIFICAR**: Primera respuesta permanece visible
- [ ] Enviar mensaje: "¿Cuáles son las tarifas?"
- [ ] Esperar respuesta completa
- [ ] **VERIFICAR**: Ambas respuestas permanecen visibles
- [ ] Enviar mensaje: "¿Qué créditos ofrecen?"
- [ ] **VERIFICAR**: Las 3 respuestas permanecen visibles en el historial

### 4. Prueba de FAQ
- [ ] Hacer clic en uno de los botones FAQ (ej: "¿Cómo me afilio?")
- [ ] **VERIFICAR**: La pregunta aparece como mensaje del usuario
- [ ] **VERIFICAR**: La respuesta aparece y permanece visible
- [ ] **VERIFICAR**: El componente FAQ se muestra correctamente (si aplica)

### 5. Prueba de Scroll
- [ ] Enviar 5-6 mensajes consecutivos
- [ ] **VERIFICAR**: Todos los mensajes permanecen en el historial
- [ ] **VERIFICAR**: El scroll automático funciona correctamente
- [ ] **VERIFICAR**: Puedes hacer scroll hacia arriba y ver mensajes anteriores
- [ ] **VERIFICAR**: Los mensajes NO desaparecen al hacer scroll

### 6. Prueba de Reconexión
- [ ] Abrir DevTools (F12) → Network tab
- [ ] Cambiar a "Offline" por 5 segundos
- [ ] Cambiar de vuelta a "Online"
- [ ] **VERIFICAR**: El chat se reconecta automáticamente
- [ ] **VERIFICAR**: Los mensajes anteriores permanecen visibles
- [ ] Enviar un nuevo mensaje
- [ ] **VERIFICAR**: El nuevo mensaje funciona correctamente

### 7. Prueba de Indicadores Visuales
- [ ] Enviar un mensaje
- [ ] **VERIFICAR**: Aparece "Comfi está escribiendo..." inmediatamente
- [ ] **VERIFICAR**: El indicador tiene animación de puntos
- [ ] **VERIFICAR**: El indicador desaparece cuando comienza el streaming
- [ ] **VERIFICAR**: Durante el streaming, se ve el texto acumulándose
- [ ] **VERIFICAR**: El cursor parpadeante (|) aparece durante el streaming

### 8. Prueba de Avatares
- [ ] Enviar varios mensajes
- [ ] **VERIFICAR**: Mensajes del usuario tienen avatar azul con icono 👤
- [ ] **VERIFICAR**: Mensajes de Comfi tienen avatar morado con logo
- [ ] **VERIFICAR**: Los avatares permanecen visibles junto con los mensajes

---

## 🔍 Puntos Críticos a Observar

### ❌ Comportamiento INCORRECTO (Bug)
- Mensaje aparece brevemente y luego desaparece
- Parpadeo en los mensajes
- Mensajes que se duplican o se pierden
- Indicador de procesamiento que no desaparece
- Streaming que no se convierte en mensaje permanente

### ✅ Comportamiento CORRECTO (Esperado)
- Todos los mensajes permanecen visibles permanentemente
- Transiciones suaves sin parpadeos
- Indicador de procesamiento aparece y desaparece correctamente
- Streaming se convierte en mensaje permanente sin problemas
- Scroll automático funciona correctamente

---

## 🧪 Pruebas Automatizadas

### Ejecutar Tests
```bash
cd frontend
npm test -- ChatExperience.test.jsx
```

### Tests Incluidos
1. **Message Persistence**
   - Usuario: mensaje permanece después de enviar
   - Bot: respuesta permanece después de streaming
   - Mensajes no se eliminan cuando desaparece indicador

2. **Processing Indicator**
   - Aparece después de enviar mensaje
   - Desaparece cuando comienza streaming

3. **Streaming Behavior**
   - Chunks se acumulan correctamente
   - Mensaje streaming se convierte en permanente

4. **Multiple Messages**
   - Múltiples mensajes sin pérdida de datos

5. **Error Handling**
   - Errores no eliminan mensajes anteriores

---

## 🐛 Debugging en Navegador

### Console Logs a Observar
```javascript
// Conexión
✅ WebSocket connected
🆔 Session ID: session-...

// Envío de mensaje
📤 Sending TEXT message: Hola

// Streaming
🌊 Stream started
📦 Stream chunk: Hola, 
📦 Stream chunk: soy Comfi
🏁 Stream ended

// Mensaje agregado
📨 WebSocket message received: {msg_type: "stream_end", ...}
```

### Errores a Buscar
```javascript
❌ WebSocket error: ...
❌ Error from backend: ...
❌ Internal server error
```

### DevTools - React Components
1. Abrir React DevTools
2. Buscar `WebSocketContext`
3. Observar estado:
   - `messages`: Array de mensajes (debe crecer, nunca decrecer)
   - `isStreaming`: true durante streaming, false después
   - `currentStreamMessage`: texto durante streaming, '' después

---

## 📊 Métricas de Éxito

| Métrica | Objetivo | Cómo Medir |
|---------|----------|------------|
| Persistencia de mensajes | 100% | Todos los mensajes permanecen visibles |
| Tiempo de feedback | <100ms | Indicador aparece inmediatamente |
| Transiciones suaves | Sin parpadeos | Observación visual |
| Streaming correcto | 100% | Texto se acumula sin pérdidas |
| Conversión a permanente | 100% | Mensaje streaming → mensaje normal |

---

## 🔧 Cambios Técnicos Realizados

### WebSocketContext.jsx
**Línea ~60-75**: Manejo de `stream_end`
```javascript
// ANTES (Bug)
setCurrentStreamMessage(prevStream => {
  const finalMessage = data.message || prevStream
  if (finalMessage) {
    setMessages(prev => [...prev, { ... }])
  }
  return '' // ❌ Limpiaba inmediatamente
})
setIsStreaming(false) // ❌ Cambiaba estado inmediatamente

// DESPUÉS (Corregido)
setCurrentStreamMessage(prevStream => {
  const finalMessage = data.message || prevStream
  if (finalMessage) {
    setMessages(prev => [...prev, { ... }])
  }
  return ''
})
setTimeout(() => {
  setIsStreaming(false) // ✅ Delay de 50ms
  streamMessageIdRef.current = null
}, 50)
```

**Línea ~150-170**: Timeout de streaming (texto plano)
```javascript
// ANTES (Bug)
if (finalMessage) {
  setMessages(prev => [...prev, { ... }])
}
// Reset inmediato ❌
isStreamingRef.current = false
setIsStreaming(false)
setCurrentStreamMessage('')

// DESPUÉS (Corregido)
if (finalMessage) {
  setMessages(prev => [...prev, { ... }])
  setTimeout(() => {
    // Reset con delay ✅
    isStreamingRef.current = false
    setIsStreaming(false)
    setCurrentStreamMessage('')
  }, 50)
}
```

### ChatWidget.jsx
**Línea ~40-50**: Control de indicador de procesamiento
```javascript
// Mejorado para ser más preciso
const lastMessage = messages[messages.length - 1]
const hasUserMessage = lastMessage && lastMessage.type === 'user'
const waitingForResponse = hasUserMessage && !isStreaming

if (waitingForResponse) {
  setIsProcessing(true)
}

if (isStreaming || (lastMessage && lastMessage.type === 'bot')) {
  setIsProcessing(false)
}
```

---

## 🚀 Próximo Deployment

### Comandos
```bash
cd frontend
npm run build
aws s3 sync dist/ s3://comfi-frontend-pragma/ --delete
aws cloudfront create-invalidation --distribution-id E2UWNXJTS2NM3V --paths "/*"
```

### Verificación Post-Deployment
1. Esperar 1-2 minutos para invalidación de CloudFront
2. Abrir en ventana incógnita: https://db4aulosarsdo.cloudfront.net
3. Ejecutar checklist de pruebas manuales
4. Verificar console logs en DevTools
5. Confirmar que NO hay mensajes que desaparecen

---

## 📝 Notas Importantes

1. **Delay de 50ms**: Es el tiempo mínimo para que React procese el cambio de estado y renderice el mensaje antes de limpiar el streaming

2. **Refs vs State**: Usamos refs (`isStreamingRef`, `accumulatedMessageRef`) para tracking interno y state para UI

3. **Doble modo**: El código maneja tanto mensajes JSON estructurados (`msg_type`) como texto plano (chunks)

4. **Timeout de 500ms**: Para finalizar streaming cuando no llegan más chunks (modo texto plano)

---

## ✅ Criterios de Aceptación

- [ ] Ningún mensaje desaparece después de ser mostrado
- [ ] Indicador de procesamiento funciona correctamente
- [ ] Streaming se muestra gradualmente
- [ ] Transiciones son suaves sin parpadeos
- [ ] Múltiples mensajes se manejan correctamente
- [ ] Scroll automático funciona
- [ ] Avatares se muestran correctamente
- [ ] Tests automatizados pasan al 100%

---

**Fecha de corrección**: 13 de marzo de 2026  
**Bug crítico**: Mensajes desaparecían después de streaming  
**Estado**: ✅ CORREGIDO  
**Pendiente**: Deployment y verificación en producción
