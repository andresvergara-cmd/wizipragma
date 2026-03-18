# Ejemplos de Código - Chat Widget UX

## 🎯 Casos de Uso Comunes

### 1. Agregar Nuevo Indicador de Estado

```jsx
// 1. Agregar estado en ChatWidget.jsx
const [isNewState, setIsNewState] = useState(false)

// 2. Agregar lógica de control
useEffect(() => {
  // Ejemplo: activar cuando hay un error
  if (messages.length > 0 && messages[messages.length - 1].isError) {
    setIsNewState(true)
    setTimeout(() => setIsNewState(false), 3000)
  }
}, [messages])

// 3. Renderizar en el JSX
{isNewState && (
  <div className="message bot error-indicator">
    <div className="message-avatar">
      <ComfiAvatar size={28} className="comfi-avatar comfi-error" />
    </div>
    <div className="message-bubble error">
      <span className="error-icon">⚠️</span>
      <span className="error-text">Hubo un problema</span>
    </div>
  </div>
)}
```

```css
/* 4. Agregar estilos en ChatWidget.css */
.message-bubble.error {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.1) 0%, rgba(244, 67, 54, 0.05) 100%);
  border: 1px solid rgba(244, 67, 54, 0.3);
  animation: errorShake 0.5s ease;
}

@keyframes errorShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}
```

### 2. Personalizar Animación de Entrada

```css
/* Animación desde arriba */
@keyframes messageSlideInTop {
  0% {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Animación con rotación */
@keyframes messageRotateIn {
  0% {
    opacity: 0;
    transform: rotate(-5deg) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: rotate(0) scale(1);
  }
}

/* Aplicar a mensajes específicos */
.message.special {
  animation: messageRotateIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### 3. Agregar Timestamp a Mensajes

```jsx
// En ChatWidget.jsx
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('es-CO', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// En el renderizado de mensajes
<div className={`message ${msg.type}`}>
  {msg.type === 'bot' && (
    <div className="message-avatar">
      <ComfiAvatar size={28} className="comfi-avatar" />
    </div>
  )}
  
  <div className="message-content">
    <div className="message-bubble">
      {msg.content}
    </div>
    <div className="message-timestamp">
      {formatTimestamp(msg.timestamp)}
    </div>
  </div>
  
  {msg.type === 'user' && (
    <div className="message-avatar user-avatar"></div>
  )}
</div>
```

```css
/* Estilos para timestamp */
.message-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.message-timestamp {
  font-size: 0.7rem;
  color: #999;
  padding: 0 0.5rem;
}

.message.user .message-timestamp {
  text-align: right;
}
```
