# 💻 Snippets de Código - Mejoras UX Chat Comfi

## 📋 Índice

1. [ChatWidget.jsx - Cambios Completos](#chatwidgetjsx)
2. [ChatWidget.css - Nuevos Estilos](#chatwidgetcss)
3. [FAQQuickActions.jsx - Modo Compacto](#faqquickactionsjsx)
4. [FAQQuickActions.css - Estilos Compactos](#faqquickactionscss)

---

## ChatWidget.jsx

### Imports a Agregar

```jsx
import ProcessingIndicator from './ProcessingIndicator'
import UserAvatar from '../Logo/UserAvatar'
import '../Logo/UserAvatar.css'
```

### Estado a Agregar

```jsx
// Agregar después de los estados existentes
const [processingState, setProcessingState] = useState('idle')
// Estados: 'idle', 'sending', 'processing', 'streaming'

const [showAllActions, setShowAllActions] = useState(false)
```

### handleSendMessage Modificado

```jsx
const handleSendMessage = (e) => {
  e?.preventDefault()
  if (inputValue.trim() || selectedImage) {
    // Cambiar a estado 'sending' inmediatamente
    setProcessingState('sending')
    
    // Animación del botón
    const sendBtn = document.querySelector('.send-btn')
    sendBtn?.classList.add('sending-animation')
    
    sendTextMessage(inputValue)
    setInputValue('')
    setSelectedImage(null)
    setShowFAQQuickActions(false)
    
    // Después de 300ms, cambiar a 'processing'
    setTimeout(() => {
      sendBtn?.classList.remove('sending-animation')
      setProcessingState('processing')
    }, 300)
  }
}
```

### useEffect para Sincronizar Estados

```jsx
// Agregar después de los useEffect existentes
useEffect(() => {
  if (isStreaming) {
    setProcessingState('streaming')
  } else if (processingState === 'streaming') {
    setProcessingState('idle')
  }
}, [isStreaming, processingState])
```

### Welcome Section Compacta

```jsx
{messages.length === 0 && showQuickActions ? (
  <div className="welcome-section-compact">
    <div className="welcome-logo-compact">
      <ComfiAvatar size={60} className="comfi-avatar comfi-wave" animated={true} />
    </div>
    <h2 className="welcome-title">¡Hola! Soy Comfi 👋</h2>
    <p className="welcome-subtitle">¿En qué puedo ayudarte?</p>
    
    {showFAQQuickActions && (
      <FAQQuickActions
        quickFAQs={quickFAQs.slice(0, 3)}
        onQuickFAQClick={handleQuickFAQClick}
        compact={true}
      />
    )}
    
    {showAllActions ? (
      <div className="quick-actions-grid">
        {quickActions.map((action, index) => (
          <button
            key={index}
            className="quick-action-btn"
            onClick={() => handleQuickAction(action.action)}
          >
            <span className="quick-action-icon">{action.icon}</span>
            <span className="quick-action-text">{action.text}</span>
          </button>
        ))}
      </div>
    ) : (
      <>
        <div className="quick-actions-grid-compact">
          {quickActions.slice(0, 4).map((action, index) => (
            <button
              key={index}
              className="quick-action-btn-compact"
              onClick={() => handleQuickAction(action.action)}
            >
              <span className="quick-action-icon">{action.icon}</span>
              <span className="quick-action-text">{action.text}</span>
            </button>
          ))}
        </div>
        
        <button 
          className="show-more-btn" 
          onClick={() => setShowAllActions(true)}
        >
          Ver más opciones ↓
        </button>
      </>
    )}
  </div>
) : (
  // ... resto del código de mensajes
)}
```

### Indicadores de Procesamiento

```jsx
{/* Reemplazar los indicadores existentes con: */}

{/* Indicador de envío */}
{processingState === 'sending' && (
  <ProcessingIndicator state="sending" />
)}

{/* Indicador de procesamiento */}
{processingState === 'processing' && (
  <ProcessingIndicator state="processing" />
)}

{/* Streaming message - mantener como está */}
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

### Avatar de Usuario

```jsx
{/* Reemplazar el avatar de usuario existente con: */}

{msg.type === 'user' && (
  <div className="message-avatar">
    <UserAvatar 
      size={36} 
      userName="Usuario"
      className="user-avatar-animated"
    />
  </div>
)}
```

---

## ChatWidget.css

### Estilos para Welcome Section Compacta

```css
/* Agregar al final del archivo */

/* ============================================ */
/* WELCOME SECTION COMPACTA */
/* ============================================ */

.welcome-section-compact {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem 1rem 0.5rem;
  gap: 0.75rem;
  animation: fadeInUp 0.6s ease;
}

.welcome-logo-compact {
  margin-bottom: 0.25rem;
}

.welcome-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.2;
}

.welcome-subtitle {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

/* ============================================ */
/* QUICK ACTIONS COMPACTAS */
/* ============================================ */

.quick-actions-grid-compact {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  width: 100%;
  max-width: 400px;
}

.quick-action-btn-compact {
  background: white;
  border: 2px solid #e8e8e8;
  border-radius: 12px;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  min-height: 75px;
  position: relative;
  overflow: hidden;
}

.quick-action-btn-compact::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(173, 55, 224, 0.1);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.quick-action-btn-compact:hover {
  border-color: #ad37e0;
  background: linear-gradient(135deg, rgba(173, 55, 224, 0.05) 0%, rgba(173, 55, 224, 0.02) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(173, 55, 224, 0.15);
}

.quick-action-btn-compact:hover::before {
  width: 300px;
  height: 300px;
}

.quick-action-btn-compact .quick-action-icon {
  font-size: 1.5rem;
  z-index: 1;
}

.quick-action-btn-compact .quick-action-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: #333;
  line-height: 1.2;
  z-index: 1;
}

/* ============================================ */
/* BOTÓN VER MÁS */
/* ============================================ */

.show-more-btn {
  background: transparent;
  border: 1px dashed #d0d0d0;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: #666;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.25rem;
  width: 100%;
  max-width: 400px;
}

.show-more-btn:hover {
  border-color: #ad37e0;
  color: #ad37e0;
  background: rgba(173, 55, 224, 0.03);
  border-style: solid;
}

/* ============================================ */
/* ANIMACIÓN DE ENVÍO */
/* ============================================ */

.send-btn.sending-animation {
  animation: sendPulse 0.3s ease-out;
}

@keyframes sendPulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.85);
    box-shadow: 0 0 20px rgba(173, 55, 224, 0.6);
  }
  100% {
    transform: scale(1);
  }
}

.send-btn.sending-animation::after {
  content: '✨';
  position: absolute;
  font-size: 1.5rem;
  animation: particleFloat 0.6s ease-out forwards;
  pointer-events: none;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

@keyframes particleFloat {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(calc(-50% + 20px), calc(-50% - 30px)) scale(0);
    opacity: 0;
  }
}

/* ============================================ */
/* RESPONSIVE - MOBILE */
/* ============================================ */

@media (max-width: 768px) {
  .welcome-section-compact {
    padding: 0.75rem 0.75rem 0.5rem;
    gap: 0.5rem;
  }
  
  .welcome-logo-compact {
    margin-bottom: 0;
  }
  
  .welcome-title {
    font-size: 1.25rem;
  }
  
  .welcome-subtitle {
    font-size: 0.85rem;
  }
  
  .quick-action-btn-compact {
    padding: 0.625rem;
    min-height: 65px;
  }
  
  .quick-action-btn-compact .quick-action-icon {
    font-size: 1.25rem;
  }
  
  .quick-action-btn-compact .quick-action-text {
    font-size: 0.7rem;
  }
}
```

---

## FAQQuickActions.jsx

### Componente Completo con Modo Compacto

```jsx
import './FAQQuickActions.css'

/**
 * FAQQuickActions Component
 * Muestra acciones rápidas para FAQs más frecuentes
 * @param {boolean} compact - Modo compacto para welcome screen
 */
const FAQQuickActions = ({ quickFAQs, onQuickFAQClick, onViewAll, compact = false }) => {
  if (!quickFAQs || quickFAQs.length === 0) return null

  return (
    <div className={`faq-quick-actions ${compact ? 'compact' : ''}`}>
      <div className="quick-actions-header">
        <span className="quick-icon">⚡</span>
        <span className="quick-title">Preguntas frecuentes</span>
      </div>

      <div className="quick-actions-grid">
        {quickFAQs.map((faq) => (
          <button
            key={faq.id}
            className="quick-action-item"
            onClick={() => onQuickFAQClick?.(faq.id)}
          >
            <span className="quick-faq-icon">{faq.icon || '❓'}</span>
            <span className="quick-faq-text">{faq.shortQuestion}</span>
          </button>
        ))}
      </div>

      {onViewAll && !compact && (
        <button className="view-all-btn" onClick={onViewAll}>
          Ver todas las preguntas →
        </button>
      )}
    </div>
  )
}

export default FAQQuickActions
```

---

## FAQQuickActions.css

### Estilos para Modo Compacto

```css
/* Agregar al final del archivo existente */

/* ============================================ */
/* MODO COMPACTO */
/* ============================================ */

.faq-quick-actions.compact {
  margin: 0.5rem 0;
  width: 100%;
  max-width: 400px;
}

.faq-quick-actions.compact .quick-actions-header {
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
}

.faq-quick-actions.compact .quick-icon {
  font-size: 1rem;
}

.faq-quick-actions.compact .quick-title {
  font-size: 0.85rem;
}

.faq-quick-actions.compact .quick-actions-grid {
  grid-template-columns: 1fr;
  gap: 0.5rem;
}

.faq-quick-actions.compact .quick-action-item {
  padding: 0.625rem 0.875rem;
  min-height: auto;
  font-size: 0.85rem;
  text-align: left;
  justify-content: flex-start;
}

.faq-quick-actions.compact .quick-faq-icon {
  font-size: 1.1rem;
}

.faq-quick-actions.compact .quick-faq-text {
  font-size: 0.85rem;
}

/* Responsive para modo compacto */
@media (max-width: 768px) {
  .faq-quick-actions.compact .quick-actions-header {
    font-size: 0.8rem;
  }
  
  .faq-quick-actions.compact .quick-action-item {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }
  
  .faq-quick-actions.compact .quick-faq-icon {
    font-size: 1rem;
  }
  
  .faq-quick-actions.compact .quick-faq-text {
    font-size: 0.8rem;
  }
}
```

---

## 🎯 Orden de Implementación

### Paso 1: Copiar Componentes Nuevos
1. ✅ `ProcessingIndicator.jsx` (ya creado)
2. ✅ `ProcessingIndicator.css` (ya creado)
3. ✅ `UserAvatar.jsx` (ya creado)
4. ✅ `UserAvatar.css` (ya creado)

### Paso 2: Modificar ChatWidget
1. Agregar imports
2. Agregar estados
3. Modificar `handleSendMessage`
4. Agregar `useEffect` para estados
5. Reemplazar welcome section
6. Reemplazar indicadores de procesamiento
7. Reemplazar avatar de usuario

### Paso 3: Actualizar CSS
1. Agregar estilos de welcome section compacta
2. Agregar estilos de quick actions compactas
3. Agregar estilos de botón "Ver más"
4. Agregar animación de envío
5. Agregar responsive

### Paso 4: Modificar FAQQuickActions
1. Agregar prop `compact`
2. Aplicar clase condicional
3. Ocultar botón "Ver todas" en modo compacto

### Paso 5: Actualizar CSS de FAQ
1. Agregar estilos para modo compacto
2. Agregar responsive para modo compacto

---

## 🧪 Testing Rápido

### Test 1: Indicador de Procesamiento
```javascript
// En la consola del navegador
// 1. Abrir chat
// 2. Escribir mensaje
// 3. Enviar
// 4. Verificar que aparece "Enviando..." inmediatamente
// 5. Verificar que cambia a "Comfi está pensando..." después de 300ms
```

### Test 2: Layout Compacto
```javascript
// En DevTools
// 1. Abrir chat
// 2. Medir altura de .welcome-section-compact
// 3. Debe ser < 500px
// 4. No debe haber scroll
```

### Test 3: Avatar de Usuario
```javascript
// En la consola del navegador
// 1. Enviar mensaje
// 2. Verificar que aparece avatar con iniciales
// 3. document.querySelector('.user-avatar-container')
// 4. Debe existir y tener estilos
```

---

**Documento creado por**: Kiro - Diseñador UX/UI
**Versión**: 1.0
