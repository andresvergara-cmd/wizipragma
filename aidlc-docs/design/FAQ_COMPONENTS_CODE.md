# 💻 Código Completo de Componentes FAQ
## Implementación React Lista para Producción

---

## 📁 Estructura de Archivos

```
frontend/src/
├── components/
│   └── FAQ/
│       ├── FAQCard.jsx
│       ├── FAQCard.css
│       ├── FAQCategoryGrid.jsx
│       ├── FAQCategoryGrid.css
│       ├── FAQQuickActions.jsx
│       ├── FAQQuickActions.css
│       ├── FAQRelatedQuestions.jsx
│       ├── FAQRelatedQuestions.css
│       ├── FAQFeedback.jsx
│       ├── FAQFeedback.css
│       ├── FAQSuggestions.jsx
│       ├── FAQSuggestions.css
│       └── index.js
├── hooks/
│   └── useFAQ.js
├── utils/
│   └── faqMatcher.js
└── data/
    ├── faqData.js
    └── faqCategories.js
```

---

## 🎨 COMPONENTE 1: FAQCard.jsx

```jsx
import { useState } from 'react'
import FAQRelatedQuestions from './FAQRelatedQuestions'
import FAQFeedback from './FAQFeedback'
import './FAQCard.css'

/**
 * FAQCard Component
 * Muestra una respuesta FAQ con formato enriquecido
 * 
 * @param {Object} faq - Objeto FAQ con toda la información
 * @param {Function} onActionClick - Callback para acciones del FAQ
 * @param {Function} onRelatedClick - Callback para preguntas relacionadas
 * @param {Function} onFeedback - Callback para feedback del usuario
 * @param {boolean} isPersonalized - Si la respuesta está personalizada
 */
const FAQCard = ({ 
  faq, 
  onActionClick, 
  onRelatedClick,
  onFeedback,
  isPersonalized = false 
}) => {
  const [showFeedback, setShowFeedback] = useState(false)
  const [feedbackGiven, setFeedbackGiven] = useState(false)
  const [isExpanded, setIsExpanded] = useState(true)

  if (!faq) return null

  const handleFeedback = (isHelpful, comment = '') => {
    setFeedbackGiven(true)
    onFeedback?.(faq.id, isHelpful, comment)
    
    if (!isHelpful) {
      setShowFeedback(true)
    } else {
      // Mostrar mensaje de agradecimiento
      setTimeout(() => {
        setShowFeedback(false)
      }, 2000)
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      afiliacion: '#e6007e',
      creditos: '#ad37e0',
      subsidios: '#00a651',
      servicios: '#0066cc',
      cuenta: '#ff6b00'
    }
    return colors[category] || '#ad37e0'
  }

  const toggleExpand = () => {
    setIsExpanded(!isExpanded)
  }

  return (
    <div className="faq-card" data-faq-id={faq.id}>
      {/* Header */}
      <div 
        className="faq-card-header"
        style={{ borderLeftColor: getCategoryColor(faq.category) }}
      >
        <div className="faq-category">
          <span className="faq-icon">{faq.categoryIcon}</span>
          <span className="faq-category-name">{faq.categoryName}</span>
          {isPersonalized && (
            <span className="faq-personalized-badge">
              ✨ Personalizado
            </span>
          )}
        </div>
        
        <div className="faq-header-actions">
          {!feedbackGiven && (
            <div className="faq-feedback-quick">
              <button 
                className="feedback-btn helpful"
                onClick={() => handleFeedback(true)}
                title="Útil"
                aria-label="Marcar como útil"
              >
                👍
              </button>
              <button 
                className="feedback-btn not-helpful"
                onClick={() => handleFeedback(false)}
                title="No útil"
                aria-label="Marcar como no útil"
              >
                👎
              </button>
            </div>
          )}
          
          <button
            className="faq-expand-btn"
            onClick={toggleExpand}
            aria-label={isExpanded ? 'Contraer' : 'Expandir'}
          >
            {isExpanded ? '▼' : '▶'}
          </button>
        </div>
      </div>

      {/* Question */}
      <div className="faq-question" onClick={toggleExpand}>
        {faq.question}
      </div>

      {/* Collapsible Content */}
      {isExpanded && (
        <div className="faq-content">
          {/* Short Answer (always visible) */}
          <div className="faq-short-answer">
            {faq.shortAnswer}
          </div>

          {/* Detailed Answer */}
          <div className="faq-answer">
            {isPersonalized && faq.personalizedAnswer ? (
              <div dangerouslySetInnerHTML={{ __html: faq.personalizedAnswer }} />
            ) : (
              <div dangerouslySetInnerHTML={{ __html: faq.detailedAnswer }} />
            )}
          </div>

          {/* Actions */}
          {faq.actions && faq.actions.length > 0 && (
            <div className="faq-actions">
              {faq.actions.map((action, index) => (
                <button
                  key={index}
                  className="faq-action-btn"
                  onClick={() => onActionClick?.(action)}
                  aria-label={action.label}
                >
                  {action.label}
                </button>
              ))}
            </div>
          )}

          {/* Related Questions */}
          {faq.relatedQuestions && faq.relatedQuestions.length > 0 && (
            <FAQRelatedQuestions
              relatedQuestions={faq.relatedQuestions}
              onRelatedClick={onRelatedClick}
            />
          )}

          {/* Feedback Form */}
          {showFeedback && !feedbackGiven && (
            <FAQFeedback
              faqId={faq.id}
              onSubmit={handleFeedback}
              onEscalate={() => onActionClick?.({ action: 'escalate_to_human' })}
            />
          )}

          {/* Thank You Message */}
          {feedbackGiven && !showFeedback && (
            <div className="faq-thank-you">
              ✅ ¡Gracias por tu feedback! Nos ayuda a mejorar.
            </div>
          )}

          {/* Escalation Option */}
          {!showFeedback && (
            <div className="faq-escalate">
              <button 
                className="faq-escalate-btn"
                onClick={() => onActionClick?.({ action: 'escalate_to_human' })}
              >
                ¿Necesitas más ayuda? Habla con un asesor
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default FAQCard
```


---

## 🎨 COMPONENTE 2: FAQRelatedQuestions.jsx

```jsx
import './FAQRelatedQuestions.css'

/**
 * FAQRelatedQuestions Component
 * Muestra preguntas relacionadas al FAQ actual
 */
const FAQRelatedQuestions = ({ relatedQuestions, onRelatedClick }) => {
  if (!relatedQuestions || relatedQuestions.length === 0) return null

  return (
    <div className="faq-related">
      <div className="faq-related-title">
        📌 También te puede interesar:
      </div>
      <div className="faq-related-list">
        {relatedQuestions.map((related, index) => (
          <button
            key={related.id || index}
            className="faq-related-item"
            onClick={() => onRelatedClick?.(related.id)}
          >
            <span className="related-arrow">→</span>
            <span className="related-text">{related.questionPreview}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

export default FAQRelatedQuestions
```

---

## 🎨 COMPONENTE 3: FAQFeedback.jsx

```jsx
import { useState } from 'react'
import './FAQFeedback.css'

/**
 * FAQFeedback Component
 * Captura feedback detallado del usuario
 */
const FAQFeedback = ({ faqId, onSubmit, onEscalate }) => {
  const [comment, setComment] = useState('')
  const [selectedReason, setSelectedReason] = useState('')

  const reasons = [
    'La información no era lo que buscaba',
    'La respuesta no fue clara',
    'Necesito información más específica',
    'La información está desactualizada',
    'Otro motivo'
  ]

  const handleSubmit = () => {
    if (comment.trim() || selectedReason) {
      onSubmit?.(false, `${selectedReason}${comment ? ': ' + comment : ''}`)
    }
  }

  return (
    <div className="faq-feedback-form">
      <div className="feedback-title">
        ¿Qué podemos mejorar?
      </div>

      <div className="feedback-reasons">
        {reasons.map((reason, index) => (
          <label key={index} className="feedback-reason-item">
            <input
              type="radio"
              name="feedback-reason"
              value={reason}
              checked={selectedReason === reason}
              onChange={(e) => setSelectedReason(e.target.value)}
            />
            <span>{reason}</span>
          </label>
        ))}
      </div>

      <textarea
        className="feedback-textarea"
        placeholder="Cuéntanos más detalles (opcional)..."
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        rows={3}
      />

      <div className="feedback-actions">
        <button 
          className="feedback-submit-btn"
          onClick={handleSubmit}
        >
          Enviar feedback
        </button>
        <button 
          className="feedback-escalate-btn"
          onClick={onEscalate}
        >
          Hablar con asesor
        </button>
      </div>
    </div>
  )
}

export default FAQFeedback
```

---

## 🎨 COMPONENTE 4: FAQCategoryGrid.jsx

```jsx
import './FAQCategoryGrid.css'

/**
 * FAQCategoryGrid Component
 * Muestra grid de categorías FAQ para exploración
 */
const FAQCategoryGrid = ({ categories, onCategoryClick }) => {
  if (!categories || categories.length === 0) return null

  return (
    <div className="faq-category-grid-container">
      <div className="faq-category-grid-header">
        <h3>¿En qué puedo ayudarte hoy?</h3>
        <p>Explora nuestras categorías de ayuda</p>
      </div>

      <div className="faq-category-grid">
        {categories.map((category) => (
          <button
            key={category.id}
            className="faq-category-card"
            onClick={() => onCategoryClick?.(category.id)}
            style={{ borderTopColor: category.color }}
          >
            <div className="category-icon">{category.icon}</div>
            <div className="category-name">{category.name}</div>
            <div className="category-description">{category.description}</div>
            <div className="category-count">
              {category.questionCount} preguntas
            </div>
          </button>
        ))}
      </div>

      <div className="faq-category-footer">
        <p>O escribe tu pregunta directamente en el chat</p>
      </div>
    </div>
  )
}

export default FAQCategoryGrid
```

---

## 🎨 COMPONENTE 5: FAQQuickActions.jsx

```jsx
import './FAQQuickActions.css'

/**
 * FAQQuickActions Component
 * Muestra acciones rápidas para FAQs más frecuentes
 */
const FAQQuickActions = ({ quickFAQs, onQuickFAQClick, onViewAll }) => {
  if (!quickFAQs || quickFAQs.length === 0) return null

  return (
    <div className="faq-quick-actions">
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

      {onViewAll && (
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

## 🎨 COMPONENTE 6: FAQSuggestions.jsx

```jsx
import './FAQSuggestions.css'

/**
 * FAQSuggestions Component
 * Muestra sugerencias cuando no hay match exacto
 */
const FAQSuggestions = ({ suggestions, onSuggestionClick, onReformulate }) => {
  if (!suggestions || suggestions.length === 0) return null

  return (
    <div className="faq-suggestions">
      <div className="suggestions-header">
        <span className="suggestions-icon">❓</span>
        <h3>¿Te refieres a alguna de estas preguntas?</h3>
      </div>

      <div className="suggestions-list">
        {suggestions.map((suggestion, index) => (
          <button
            key={suggestion.id || index}
            className="suggestion-item"
            onClick={() => onSuggestionClick?.(suggestion.id)}
          >
            <div className="suggestion-number">{index + 1}️⃣</div>
            <div className="suggestion-content">
              <div className="suggestion-question">{suggestion.question}</div>
              <div className="suggestion-preview">{suggestion.shortAnswer}</div>
            </div>
            <div className="suggestion-confidence">
              {Math.round(suggestion.confidence * 100)}% match
            </div>
          </button>
        ))}
      </div>

      <div className="suggestions-footer">
        <p>O escribe tu pregunta de otra forma</p>
        {onReformulate && (
          <button className="reformulate-btn" onClick={onReformulate}>
            Reformular pregunta
          </button>
        )}
      </div>
    </div>
  )
}

export default FAQSuggestions
```

---

## 🎨 COMPONENTE 7: index.js (Barrel Export)

```javascript
// frontend/src/components/FAQ/index.js

export { default as FAQCard } from './FAQCard'
export { default as FAQCategoryGrid } from './FAQCategoryGrid'
export { default as FAQQuickActions } from './FAQQuickActions'
export { default as FAQRelatedQuestions } from './FAQRelatedQuestions'
export { default as FAQFeedback } from './FAQFeedback'
export { default as FAQSuggestions } from './FAQSuggestions'
```

