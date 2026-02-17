# Plan de Desarrollo - Unidad 4: Frontend Multimodal UI

**Developer**: Dev 1 (Frontend Specialist)  
**Fecha**: 2026-02-17  
**Estado**: En Progreso

## Estado Actual

### ✅ Completado
- **Story 1.1**: WebSocket Connection (parcial)
  - Conexión WebSocket básica implementada
  - Envío y recepción de mensajes
  - Reconexión automática
  - Gestión de sesiones

- **Story 1.4**: Chat Interface (completo)
  - Interfaz de chat moderna
  - Mensajes de usuario y bot diferenciados
  - Markdown rendering
  - Auto-scroll
  - Typing indicator
  - Streaming de respuestas

### ⏳ Pendiente

#### Story 1.2: Voice Input UI (1.5h)
**Prioridad**: Must Have

**Funcionalidades a implementar**:
- [ ] Botón de micrófono en la UI
- [ ] Captura de audio con MediaRecorder API
- [ ] Indicador visual de grabación
- [ ] Envío de audio vía WebSocket
- [ ] Manejo de permisos de micrófono
- [ ] Conversión de audio a formato compatible

**Archivos a modificar**:
- `index.html` - Agregar botón de voz y controles

**Integración**:
- Enviar audio como base64 en mensaje WebSocket
- Formato: `{type: "VOICE", content: "base64_audio_data"}`

---

#### Story 1.3: Voice Output UI (1h)
**Prioridad**: Must Have

**Funcionalidades a implementar**:
- [ ] Reproducción de audio de respuestas
- [ ] Indicador visual de "CENTLI hablando"
- [ ] Controles de pausa/stop
- [ ] Control de volumen
- [ ] Cola de reproducción

**Archivos a modificar**:
- `index.html` - Agregar componente de audio player

**Integración**:
- Recibir audio como base64 en respuesta WebSocket
- Formato: `{type: "VOICE", content: "base64_audio_data"}`

---

#### Story 1.5: Transaction Confirmation UI (1h)
**Prioridad**: Must Have

**Funcionalidades a implementar**:
- [ ] Modal de confirmación de transacción
- [ ] Mostrar detalles: monto, destinatario, concepto
- [ ] Botones Confirmar/Cancelar
- [ ] Feedback de éxito/error
- [ ] Recibo de transacción

**Archivos a crear**:
- Componente modal dentro de `index.html`

**Integración**:
- Detectar cuando el bot solicita confirmación
- Mostrar modal con datos extraídos
- Enviar confirmación al backend

---

#### Story 1.6: Product Catalog UI (1.5h)
**Prioridad**: Must Have

**Funcionalidades a implementar**:
- [ ] Grid de productos con imágenes
- [ ] Tarjetas de producto (nombre, precio, beneficios)
- [ ] Vista detallada de producto
- [ ] Comparación de beneficios
- [ ] Filtros por categoría
- [ ] Búsqueda de productos

**Archivos a crear**:
- Componente de catálogo dentro de `index.html`

**Integración**:
- Recibir lista de productos del backend
- Formato: `{type: "CATALOG", products: [...]}`

---

#### Story 1.7: Image Upload UI (1h)
**Prioridad**: Could Have

**Funcionalidades a implementar**:
- [ ] Botón de cámara/galería
- [ ] File picker
- [ ] Preview de imagen
- [ ] Compresión de imagen
- [ ] Envío vía WebSocket
- [ ] Indicador de progreso

**Archivos a modificar**:
- `index.html` - Agregar botón de imagen

**Integración**:
- Enviar imagen como base64
- Formato: `{type: "IMAGE", content: "base64_image_data"}`

---

## Orden de Implementación Recomendado

### Fase 1: Multimodal Input/Output (3h)
1. **Story 1.2**: Voice Input UI (1.5h)
2. **Story 1.3**: Voice Output UI (1h)
3. **Story 1.7**: Image Upload UI (1h) - Si hay tiempo

### Fase 2: Transacciones y Catálogo (2.5h)
4. **Story 1.5**: Transaction Confirmation UI (1h)
5. **Story 1.6**: Product Catalog UI (1.5h)

### Fase 3: Testing e Integración (1h)
6. Pruebas de integración con backend
7. Ajustes de UI/UX
8. Optimización de rendimiento

**Total estimado**: 6.5 horas

---

## Consideraciones Técnicas

### WebSocket Endpoint
- Actualizar `YOUR-WEB-SOCKET-ENDPOINT` con el endpoint real
- Formato: `wss://your-api-id.execute-api.region.amazonaws.com/prod`

### Formatos de Mensaje

**Envío (Frontend → Backend)**:
```json
{
  "action": "sendMessage",
  "data": {
    "user_id": "user-001",
    "session_id": "session-123",
    "message": "texto" | "base64_audio" | "base64_image",
    "type": "TEXT" | "VOICE" | "IMAGE"
  }
}
```

**Recepción (Backend → Frontend)**:
```json
{
  "msg_type": "agent_response" | "stream_start" | "stream_end",
  "message": "texto",
  "is_response": true,
  "data": {
    "type": "TEXT" | "VOICE" | "CATALOG" | "CONFIRMATION",
    "content": "...",
    "products": [...],
    "transaction": {...}
  }
}
```

### Browser APIs Necesarias
- **MediaRecorder API**: Captura de audio
- **Audio API**: Reproducción de audio
- **File API**: Upload de imágenes
- **Canvas API**: Compresión de imágenes

### Compatibilidad
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ⚠️ Requiere permisos explícitos para micrófono
- Mobile: ✅ Compatible con ajustes

---

## Deployment

### Opción 1: S3 + CloudFront (Recomendado)
```bash
# Subir a S3
aws s3 cp index.html s3://centli-frontend-bucket/
aws s3 cp index.html s3://centli-frontend-bucket/ --acl public-read

# Configurar CloudFront (opcional)
# Crear distribución apuntando al bucket S3
```

### Opción 2: API Gateway HTTP
- Servir `index.html` desde Lambda
- Configurar ruta `/` en API Gateway

### Variables de Configuración
```javascript
const CONFIG = {
  WEBSOCKET_ENDPOINT: process.env.WEBSOCKET_ENDPOINT || "wss://...",
  API_ENDPOINT: process.env.API_ENDPOINT || "https://...",
  REGION: "us-east-1"
};
```

---

## Testing

### Tests Manuales
- [ ] Conexión WebSocket exitosa
- [ ] Envío y recepción de mensajes de texto
- [ ] Captura y envío de audio
- [ ] Reproducción de audio de respuesta
- [ ] Upload de imágenes
- [ ] Confirmación de transacciones
- [ ] Visualización de catálogo de productos
- [ ] Responsive design (móvil y desktop)

### Tests de Integración
- [ ] Frontend → AgentCore (WebSocket)
- [ ] Flujo completo de transferencia
- [ ] Flujo completo de compra
- [ ] Manejo de errores

---

## Próximos Pasos

1. **Actualizar WebSocket endpoint** en `index.html`
2. **Implementar Story 1.2** (Voice Input)
3. **Implementar Story 1.3** (Voice Output)
4. **Implementar Story 1.5** (Transaction Confirmation)
5. **Implementar Story 1.6** (Product Catalog)
6. **Testing e integración**
7. **Deploy a S3**

---

**Documento creado**: 2026-02-17  
**Última actualización**: 2026-02-17  
**Estado**: Plan inicial - Listo para implementación
