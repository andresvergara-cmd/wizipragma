# UI Validation Rules - Unit 4: Frontend Multimodal UI

## Overview

This document defines validation rules, error handling, and UX patterns for the CENTLI frontend.

---

## 1. Input Validation Rules

### 1.1 Text Message Validation

**Rules**:
- **Required**: Message cannot be empty or whitespace only
- **Min Length**: 1 character (after trim)
- **Max Length**: 500 characters
- **Allowed Characters**: All UTF-8 characters (support Spanish)

**Validation Logic**:
```javascript
function validateTextMessage(message) {
  const trimmed = message.trim();
  
  if (trimmed.length === 0) {
    return { valid: false, error: 'El mensaje no puede estar vacío' };
  }
  
  if (trimmed.length > 500) {
    return { valid: false, error: 'El mensaje no puede exceder 500 caracteres' };
  }
  
  return { valid: true };
}
```

**UI Feedback**:
- Show character counter: "X/500"
- Disable send button if empty
- Show inline error if > 500 characters
- Red border on input field for errors

---

### 1.2 Image Upload Validation

**Rules**:
- **File Type**: JPEG, PNG, GIF only
- **Max File Size**: 5MB
- **Min Dimensions**: 100x100 pixels
- **Max Dimensions**: 4096x4096 pixels

**Validation Logic**:
```javascript
function validateImage(file) {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
  const maxSize = 5 * 1024 * 1024; // 5MB
  
  if (!allowedTypes.includes(file.type)) {
    return { 
      valid: false, 
      error: 'Formato no soportado. Use JPEG, PNG o GIF' 
    };
  }
  
  if (file.size > maxSize) {
    return { 
      valid: false, 
      error: 'La imagen no puede exceder 5MB' 
    };
  }
  
  return { valid: true };
}
```

**UI Feedback**:
- Show error toast for invalid files
- Display file size in preview
- Show compression indicator if needed

---

### 1.3 Voice Recording Validation

**Rules**:
- **Microphone Permission**: Required
- **Max Duration**: 60 seconds
- **Min Duration**: 1 second
- **Audio Format**: WebM (browser default)

**Validation Logic**:
```javascript
function validateVoiceRecording(duration, hasPermission) {
  if (!hasPermission) {
    return { 
      valid: false, 
      error: 'Se requiere permiso de micrófono' 
    };
  }
  
  if (duration < 1000) {
    return { 
      valid: false, 
      error: 'La grabación es demasiado corta' 
    };
  }
  
  if (duration > 60000) {
    return { 
      valid: false, 
      error: 'La grabación no puede exceder 60 segundos' 
    };
  }
  
  return { valid: true };
}
```

**UI Feedback**:
- Show recording timer
- Auto-stop at 60 seconds
- Show permission error modal
- Disable voice button if no permission

---

### 1.4 Transaction Confirmation Validation

**Rules**:
- **Amount**: Must be > 0
- **Account**: Must be selected
- **Confirmation**: User must explicitly confirm

**Validation Logic**:
```javascript
function validateTransactionConfirmation(transaction) {
  if (!transaction.amount || transaction.amount <= 0) {
    return { 
      valid: false, 
      error: 'Monto inválido' 
    };
  }
  
  if (!transaction.source_account) {
    return { 
      valid: false, 
      error: 'Debe seleccionar una cuenta' 
    };
  }
  
  return { valid: true };
}
```

**UI Feedback**:
- Disable confirm button if invalid
- Show validation errors in modal
- Highlight invalid fields

---

## 2. Browser Compatibility

### 2.1 Supported Browsers

**Desktop**:
- Chrome 90+ ✅
- Firefox 88+ ✅
- Safari 14+ ✅
- Edge 90+ ✅

**Mobile**:
- iOS Safari 14+ ✅
- Chrome Mobile 90+ ✅
- Samsung Internet 14+ ✅

**Unsupported**:
- Internet Explorer (all versions) ❌
- Opera Mini ❌

---

### 2.2 Feature Detection

**Required Features**:
- WebSocket API
- MediaRecorder API (for voice)
- File API (for image upload)
- LocalStorage
- ES6+ JavaScript

**Detection Logic**:
```javascript
function checkBrowserSupport() {
  const features = {
    websocket: 'WebSocket' in window,
    mediaRecorder: 'MediaRecorder' in window,
    fileApi: 'File' in window && 'FileReader' in window,
    localStorage: 'localStorage' in window,
    es6: typeof Symbol !== 'undefined'
  };
  
  const unsupported = Object.entries(features)
    .filter(([key, supported]) => !supported)
    .map(([key]) => key);
  
  return {
    supported: unsupported.length === 0,
    missing: unsupported
  };
}
```

**UI Feedback**:
- Show warning banner for unsupported browsers
- Disable unsupported features gracefully
- Provide fallback for missing features

---

### 2.3 Fallback Strategies

**WebSocket Not Supported**:
- Show error message
- Suggest upgrading browser
- No fallback (WebSocket is critical)

**MediaRecorder Not Supported**:
- Hide voice input button
- Show "Voice not supported" message
- Text input still works

**File API Not Supported**:
- Hide image upload button
- Show "Image upload not supported" message

---

## 3. Accessibility Requirements

### 3.1 Keyboard Navigation

**Requirements**:
- All interactive elements accessible via Tab
- Enter key to submit forms
- ESC key to close modals
- Arrow keys for navigation (optional)

**Tab Order**:
```
1. Text input field
2. Send button
3. Voice button
4. Image button
5. Chat messages (focusable for screen readers)
6. Modal buttons (when modal open)
```

**Implementation**:
```javascript
// Ensure proper tabindex
<input type="text" tabindex="1" />
<button tabindex="2">Send</button>

// Trap focus in modal
function trapFocusInModal(modal) {
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
  });
}
```

---

### 3.2 Screen Reader Support

**ARIA Labels**:
```html
<!-- Connection status -->
<div role="status" aria-live="polite" aria-label="Estado de conexión">
  Conectado
</div>

<!-- Chat messages -->
<div role="log" aria-live="polite" aria-label="Historial de chat">
  <div role="article" aria-label="Mensaje del usuario">...</div>
  <div role="article" aria-label="Mensaje del asistente">...</div>
</div>

<!-- Buttons -->
<button aria-label="Enviar mensaje">
  <span aria-hidden="true">📤</span>
</button>

<button aria-label="Grabar mensaje de voz">
  <span aria-hidden="true">🎤</span>
</button>

<!-- Loading states -->
<div role="status" aria-live="polite" aria-busy="true">
  Cargando...
</div>
```

**Screen Reader Announcements**:
- New message received: "Nuevo mensaje del asistente"
- Connection status change: "Conexión perdida" / "Reconectado"
- Error occurred: "Error: [mensaje]"
- Transaction confirmed: "Transacción confirmada exitosamente"

---

### 3.3 Visual Accessibility

**Color Contrast**:
- Text: Minimum 4.5:1 contrast ratio (WCAG AA)
- Large text: Minimum 3:1 contrast ratio
- Interactive elements: Minimum 3:1 contrast ratio

**Font Sizes**:
- Body text: 16px minimum
- Small text: 14px minimum
- Headings: 20px+ (responsive)

**Focus Indicators**:
- Visible focus outline on all interactive elements
- 2px solid outline with high contrast color
- Never remove focus outline (`:focus { outline: none }` ❌)

**Implementation**:
```css
/* Focus styles */
button:focus,
input:focus,
a:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  body {
    background: white;
    color: black;
  }
  
  button {
    border: 2px solid black;
  }
}
```

---

## 4. Performance Targets

### 4.1 Page Load Performance

**Targets**:
- **First Contentful Paint (FCP)**: < 1.5 seconds
- **Largest Contentful Paint (LCP)**: < 2.5 seconds
- **Time to Interactive (TTI)**: < 3 seconds
- **Total Page Size**: < 500KB (excluding images)

**Optimization Strategies**:
- Minify HTML, CSS, JavaScript
- Compress images (WebP format)
- Lazy load images
- Use CDN for static assets (if available)
- Cache static resources

---

### 4.2 Runtime Performance

**Targets**:
- **WebSocket Message Latency**: < 500ms (network dependent)
- **UI Response Time**: < 100ms (for user interactions)
- **Animation Frame Rate**: 60fps (smooth animations)
- **Memory Usage**: < 100MB (for 1-hour session)

**Monitoring**:
```javascript
// Measure WebSocket latency
function measureLatency() {
  const start = performance.now();
  websocket.send(JSON.stringify({ type: 'PING' }));
  
  websocket.addEventListener('message', (event) => {
    if (event.data.type === 'PONG') {
      const latency = performance.now() - start;
      console.log(`Latency: ${latency}ms`);
    }
  });
}

// Monitor memory usage
if (performance.memory) {
  setInterval(() => {
    const used = performance.memory.usedJSHeapSize / 1048576;
    console.log(`Memory: ${used.toFixed(2)}MB`);
  }, 60000); // Every minute
}
```

---

### 4.3 Network Performance

**Targets**:
- **WebSocket Connection Time**: < 1 second
- **Image Upload Time**: < 3 seconds (for 5MB image)
- **Voice Message Send Time**: < 2 seconds (for 60s audio)

**Optimization**:
- Compress images before upload (80% quality)
- Use WebSocket binary frames for audio/images (if supported)
- Show upload progress indicators

---

## 5. Error Handling Patterns

### 5.1 Error Categories

**Network Errors**:
- WebSocket connection failed
- WebSocket disconnected
- Request timeout
- Server unreachable

**Validation Errors**:
- Invalid input
- File too large
- Unsupported file type
- Missing required field

**Business Logic Errors**:
- Insufficient funds
- Transaction declined
- Product out of stock
- Account not found

**System Errors**:
- Browser not supported
- Permission denied (microphone, camera)
- LocalStorage full
- JavaScript error

---

### 5.2 Error Display Strategy

**Toast Notifications** (for minor errors):
- Network errors (auto-retry)
- Validation errors
- Success confirmations

**Modal Dialogs** (for critical errors):
- Browser not supported
- Permission denied
- Transaction failed
- System errors

**Inline Errors** (for form validation):
- Invalid input
- Required field missing
- Format errors

---

### 5.3 Error Messages

**User-Friendly Messages**:
```javascript
const errorMessages = {
  // Network
  'WEBSOCKET_FAILED': 'No se pudo conectar. Verifica tu conexión a internet.',
  'WEBSOCKET_DISCONNECTED': 'Conexión perdida. Reconectando...',
  'REQUEST_TIMEOUT': 'La solicitud tardó demasiado. Intenta de nuevo.',
  
  // Validation
  'MESSAGE_EMPTY': 'El mensaje no puede estar vacío.',
  'MESSAGE_TOO_LONG': 'El mensaje es demasiado largo (máx. 500 caracteres).',
  'FILE_TOO_LARGE': 'El archivo es demasiado grande (máx. 5MB).',
  'FILE_TYPE_INVALID': 'Formato no soportado. Use JPEG, PNG o GIF.',
  
  // Business Logic
  'INSUFFICIENT_FUNDS': 'Saldo insuficiente para completar la transacción.',
  'TRANSACTION_DECLINED': 'La transacción fue rechazada. Contacta a tu banco.',
  'PRODUCT_OUT_OF_STOCK': 'Producto agotado. Intenta con otro producto.',
  
  // System
  'BROWSER_NOT_SUPPORTED': 'Tu navegador no es compatible. Usa Chrome, Firefox o Safari.',
  'PERMISSION_DENIED': 'Se requiere permiso para acceder al micrófono.',
  'STORAGE_FULL': 'Almacenamiento local lleno. Limpia el historial.'
};
```

---

### 5.4 Error Recovery Actions

**Automatic Recovery**:
- WebSocket reconnection (max 3 attempts)
- Retry failed requests (max 2 attempts)
- Queue messages during disconnection

**User-Initiated Recovery**:
- Manual reconnect button
- Retry button for failed operations
- Clear cache/history button
- Refresh page button

---

## 6. Loading States

### 6.1 Loading Indicators

**Spinner** (for short operations < 2s):
- Sending message
- Connecting to WebSocket
- Processing voice input

**Progress Bar** (for long operations > 2s):
- Uploading image
- Downloading large response
- Processing transaction

**Skeleton Screen** (for initial load):
- Loading chat history
- Loading product catalog
- Loading transaction details

---

### 6.2 Loading Messages

```javascript
const loadingMessages = {
  'CONNECTING': 'Conectando...',
  'SENDING_MESSAGE': 'Enviando mensaje...',
  'UPLOADING_IMAGE': 'Subiendo imagen...',
  'PROCESSING_VOICE': 'Procesando audio...',
  'LOADING_PRODUCTS': 'Cargando productos...',
  'CONFIRMING_TRANSACTION': 'Confirmando transacción...'
};
```

---

## 7. Empty States

### 7.1 Empty Chat

**Display**:
- Welcome message: "¡Hola! Soy CENTLI, tu asistente bancario. ¿En qué puedo ayudarte?"
- Suggested actions:
  - "Ver mi saldo"
  - "Hacer una transferencia"
  - "Ver productos"

---

### 7.2 No Products

**Display**:
- Message: "No hay productos disponibles en este momento."
- Action: "Intenta de nuevo más tarde"

---

### 7.3 No Connection

**Display**:
- Message: "Sin conexión. Verifica tu internet."
- Action: "Reintentar conexión"

---

## Success Criteria

- [x] All validation rules documented
- [x] Browser compatibility defined
- [x] Accessibility requirements specified
- [x] Performance targets set
- [x] Error handling patterns defined
- [x] Loading and empty states documented

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17  
**Next Step**: Present for user approval

