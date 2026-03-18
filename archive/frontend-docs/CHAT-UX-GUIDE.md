# Guía de UX del Chat Widget de Comfi

## 🎯 Visión General

El Chat Widget de Comfi implementa una experiencia conversacional multimodal con feedback visual constante, animaciones fluidas y diseño optimizado para la marca Comfama.

---

## 🎨 Principios de Diseño

### 1. **Feedback Visual Constante**
El usuario siempre sabe qué está pasando:
- ✅ Indicador de procesamiento al enviar mensaje
- ✅ Animación de "escribiendo..." durante respuesta
- ✅ Estados de conexión visibles
- ✅ Confirmación visual de acciones

### 2. **Jerarquía Visual Clara**
- **Bot (Comfi)**: Avatar morado, mensajes a la izquierda
- **Usuario**: Avatar azul, mensajes a la derecha
- **Estados**: Colores diferenciados (morado para procesamiento, rojo para grabación)

### 3. **Animaciones Significativas**
Cada animación tiene un propósito:
- Entrada de mensajes: Indica nuevo contenido
- Pulsaciones: Indica actividad en progreso
- Hover effects: Indica interactividad
- Transiciones: Suavizan cambios de estado

---

## 🔧 Componentes y Estados

### Estados del Chat

```jsx
// Estados principales
const [isProcessing, setIsProcessing] = useState(false)  // Esperando respuesta
const [isRecording, setIsRecording] = useState(false)    // Grabando audio
const [selectedImage, setSelectedImage] = useState(null) // Imagen seleccionada

// Estados del contexto
const { 
  messages,           // Array de mensajes
  isTyping,          // Bot está escribiendo (legacy)
  isConnected,       // WebSocket conectado
  isStreaming,       // Respuesta en streaming
  currentStreamMessage // Contenido del stream actual
} = useChat()
```

### Flujo de Estados

```
Usuario envía mensaje
    ↓
isProcessing = true
    ↓
"Comfi está escribiendo..." (indicador con puntos animados)
    ↓
Backend comienza streaming
    ↓
isStreaming = true, isProcessing = false
    ↓
Muestra mensaje con gradiente animado + cursor parpadeante
    ↓
Stream completa
    ↓
isStreaming = false
    ↓
Mensaje final guardado en messages[]
```

---

## 🎭 Indicadores Visuales

### 1. Indicador de Procesamiento

**Cuándo se muestra**: Después de enviar mensaje, antes de recibir respuesta

**Apariencia**:
- Avatar de Comfi con animación "thinking"
- Burbuja con 3 puntos animados
- Texto: "Comfi está escribiendo..."
- Color: Morado Comfama (#ad37e0)

**Código**:
```jsx
{isProcessing && !isStreaming && (
  <div className="message bot processing-message">
    <div className="message-avatar">
      <ComfiAvatar size={28} className="comfi-avatar comfi-thinking" animated={true} />
    </div>
    <div className="message-bubble processing">
      <div className="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <span className="typing-text">Comfi está escribiendo...</span>
    </div>
  </div>
)}
```

### 2. Streaming de Respuesta

**Cuándo se muestra**: Mientras el backend envía chunks de texto

**Apariencia**:
- Avatar de Comfi con animación "speaking"
- Burbuja con gradiente animado de fondo
- Cursor parpadeante al final del texto
- Sombra pulsante

**Código**:
```jsx
{isStreaming && currentStreamMessage && (
  <div className="message bot">
    <div className="message-avatar">
      <ComfiAvatar size={28} className="comfi-avatar comfi-speaking" animated={true} />
    </div>
    <div className="message-bubble streaming">
      {currentStreamMessage}
      <span className="cursor-blink">|</span>
    </div>
  </div>
)}
```

### 3. Avatar del Usuario

**Apariencia**:
- Gradiente azul (#4a90e2 → #357abd)
- Icono de usuario (👤)
- Efecto de brillo animado cada 3 segundos
- Posicionado a la derecha

**CSS**:
```css
.message-avatar.user-avatar {
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.message-avatar.user-avatar::after {
  /* Efecto de brillo */
  animation: avatarShine 3s ease-in-out infinite;
}
```

---

## 🎬 Animaciones

### Entrada de Mensajes

**Bot (desde abajo)**:
```css
@keyframes messageSlideIn {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
```

**Usuario (desde la derecha)**:
```css
@keyframes messageSlideInRight {
  0% {
    opacity: 0;
    transform: translateX(20px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}
```

### Indicador de Procesamiento

**Entrada con bounce**:
```css
@keyframes processingBounce {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.8);
  }
  50% {
    transform: translateY(-5px) scale(1.05);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
```

**Pulsación continua**:
```css
@keyframes processingPulse {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(173, 55, 224, 0.1);
  }
  50% {
    box-shadow: 0 4px 16px rgba(173, 55, 224, 0.25);
  }
}
```

### Streaming

**Gradiente animado**:
```css
@keyframes streamGradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
```

---

## 📐 Layout Optimizado

### Pantalla de Bienvenida

**Objetivo**: Mostrar FAQ sin scroll en pantallas de 680px

**Optimizaciones aplicadas**:
```css
/* Reducción de espaciado */
.welcome-section {
  padding: 1rem 1rem 0.75rem;  /* Antes: 1.5rem 1rem 1rem */
}

.welcome-section h2 {
  font-size: 1.4rem;  /* Antes: 1.5rem */
  margin-bottom: 0.25rem;
}

.welcome-section p {
  font-size: 0.9rem;  /* Antes: 0.95rem */
  margin-bottom: 1rem;  /* Antes: 1.25rem */
}

/* Botones más compactos */
.quick-action-btn {
  padding: 0.75rem;  /* Antes: 0.875rem */
  min-height: 75px;  /* Antes: 85px */
}

.quick-action-icon {
  font-size: 1.5rem;  /* Antes: 1.75rem */
}
```

**Resultado**: ~15% de reducción en altura vertical

---

## 🎨 Paleta de Colores

### Colores Principales

```css
/* Comfama Brand */
--comfama-purple: #ad37e0;
--comfama-purple-dark: #8b2bb3;

/* Usuario */
--user-blue: #4a90e2;
--user-blue-dark: #357abd;

/* Estados */
--success-green: #4caf50;
--error-red: #f44336;
--recording-red: #f44336;

/* Neutrales */
--text-primary: #1a1a1a;
--text-secondary: #666;
--border-light: #e8e8e8;
--background-light: #f5f5f7;
```

### Uso de Colores

| Elemento | Color | Uso |
|----------|-------|-----|
| Avatar Bot | Morado | Identidad de Comfi |
| Avatar Usuario | Azul | Diferenciación |
| Indicador Procesamiento | Morado | Actividad del bot |
| Indicador Grabación | Rojo | Alerta de grabación activa |
| Botón Enviar | Morado | Acción principal |
| Estado Online | Verde | Conexión activa |
| Estado Offline | Rojo | Sin conexión |

---

## 🔄 Scroll Automático

### Implementación

```jsx
const messagesEndRef = useRef(null)

useEffect(() => {
  scrollToBottom()
}, [messages, currentStreamMessage, isStreaming])

const scrollToBottom = () => {
  if (messagesEndRef.current) {
    messagesEndRef.current.scrollIntoView({ 
      behavior: 'smooth',
      block: 'end',
      inline: 'nearest'
    })
  }
}

// En el JSX
<div ref={messagesEndRef} />
```

### Comportamiento
- Se activa cuando cambian los mensajes
- Se activa durante streaming (cada chunk)
- Animación suave (`behavior: 'smooth'`)
- Scroll al final del contenedor

---

## 📱 Responsive Design

### Breakpoints

```css
@media (max-width: 768px) {
  .chat-widget-container {
    max-width: 100%;
    width: 100%;
    height: 100vh;
    border-radius: 20px 20px 0 0;
  }

  .quick-actions-grid {
    grid-template-columns: 1fr;  /* Una columna en móvil */
  }

  .message-bubble {
    max-width: 85%;  /* Más ancho en móvil */
  }
}
```

### Consideraciones Móviles
- Chat ocupa pantalla completa
- Botones de acción en una columna
- Touch targets mínimo 44px
- Animaciones optimizadas

---

## ♿ Accesibilidad

### Implementado
- ✅ Contraste de colores WCAG AA
- ✅ Tamaños de fuente legibles (mínimo 0.75rem)
- ✅ Estados de conexión visibles
- ✅ Feedback visual para todas las acciones

### Por Implementar
- ⏳ ARIA labels para indicadores
- ⏳ Soporte para `prefers-reduced-motion`
- ⏳ Navegación por teclado mejorada
- ⏳ Screen reader announcements

### Ejemplo de Mejora

```jsx
// Agregar ARIA labels
<div 
  className="message-bubble processing"
  role="status"
  aria-live="polite"
  aria-label="Comfi está escribiendo una respuesta"
>
  {/* contenido */}
</div>

// Respetar preferencias de animación
@media (prefers-reduced-motion: reduce) {
  .message {
    animation: none;
    opacity: 1;
  }
  
  .typing-indicator span {
    animation: none;
  }
}
```

---

## 🧪 Testing

### Tests Implementados

Ver `ChatWidget.test.jsx` para tests completos:

1. **Indicador de Procesamiento**
   - Aparece al enviar mensaje
   - Desaparece al iniciar streaming

2. **Avatar del Usuario**
   - Se muestra en mensajes del usuario
   - Posicionado a la derecha

3. **Layout Inicial**
   - Muestra pantalla de bienvenida
   - Oculta después del primer mensaje

4. **Animaciones**
   - Cursor parpadeante durante streaming
   - Clases CSS aplicadas correctamente

5. **Scroll Automático**
   - Se ejecuta al agregar mensajes

6. **Estados de Conexión**
   - Muestra estado correcto
   - Deshabilita input cuando desconectado

### Ejecutar Tests

```bash
cd frontend
npm run test
```

---

## 🐛 Debugging

### Console Logs Útiles

```jsx
// Agregar en useEffect de isProcessing
useEffect(() => {
  console.log('🔄 Processing state:', {
    isProcessing,
    isStreaming,
    lastMessage: messages[messages.length - 1]
  })
}, [isProcessing, isStreaming, messages])
```

### Verificar Animaciones

```javascript
// En DevTools Console
document.querySelectorAll('.message').forEach(msg => {
  console.log('Animation:', getComputedStyle(msg).animation)
})
```

### Verificar Estados

```javascript
// React DevTools
// Buscar ChatWidget component
// Ver hooks: isProcessing, isStreaming, messages
```

---

## 📚 Recursos Adicionales

### Archivos Relacionados
- `ChatWidget.jsx`: Componente principal
- `ChatWidget.css`: Estilos y animaciones
- `ChatContext.jsx`: Estado global del chat
- `WebSocketContext.jsx`: Conexión WebSocket
- `ComfiAvatar.jsx`: Avatar animado de Comfi

### Documentación
- `UX-IMPROVEMENTS.md`: Resumen de mejoras implementadas
- `CHAT-UX-GUIDE.md`: Esta guía
- `frontend/README.md`: Documentación general del frontend

### Referencias de Diseño
- Tema Comfama: Morado #ad37e0
- Inspiración: WhatsApp, Telegram, Intercom
- Animaciones: Material Design, Framer Motion

---

## 🚀 Próximos Pasos

### Mejoras Planificadas

1. **Timestamps**
   ```jsx
   <div className="message-timestamp">
     {formatTime(message.timestamp)}
   </div>
   ```

2. **Indicador de Lectura**
   ```jsx
   <div className="message-status">
     {message.sent && '✓'}
     {message.delivered && '✓✓'}
     {message.read && '✓✓' /* azul */}
   </div>
   ```

3. **Sonidos Sutiles**
   ```jsx
   const playSound = (type) => {
     const audio = new Audio(`/sounds/${type}.mp3`)
     audio.volume = 0.3
     audio.play()
   }
   ```

4. **Modo Oscuro**
   ```css
   @media (prefers-color-scheme: dark) {
     .chat-widget-container {
       background: #1a1a1a;
       color: #ffffff;
     }
   }
   ```

---

## 💡 Tips para Desarrolladores

### 1. Agregar Nuevo Indicador

```jsx
// 1. Crear estado
const [isNewState, setIsNewState] = useState(false)

// 2. Agregar lógica de control
useEffect(() => {
  // Condiciones para activar/desactivar
}, [dependencies])

// 3. Renderizar indicador
{isNewState && (
  <div className="new-indicator">
    {/* contenido */}
  </div>
)}

// 4. Agregar estilos en CSS
.new-indicator {
  animation: newAnimation 0.3s ease;
}
```

### 2. Modificar Animaciones

```css
/* Ajustar duración */
.message {
  animation: messageSlideIn 0.6s ease;  /* Antes: 0.4s */
}

/* Cambiar easing */
.message {
  animation: messageSlideIn 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* Agregar delay */
.message:nth-child(2) {
  animation-delay: 0.1s;
}
```

### 3. Personalizar Colores

```css
/* Crear variables CSS */
:root {
  --brand-primary: #ad37e0;
  --brand-secondary: #8b2bb3;
}

/* Usar en componentes */
.message-bubble {
  background: var(--brand-primary);
}
```

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisar esta guía
2. Consultar `UX-IMPROVEMENTS.md`
3. Revisar tests en `ChatWidget.test.jsx`
4. Contactar al equipo de frontend

---

**Última actualización**: 2024
**Versión**: 1.0.0
**Autor**: Equipo Frontend Comfi
