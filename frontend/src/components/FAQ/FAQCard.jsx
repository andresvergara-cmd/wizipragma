import { useState } from 'react'
import FAQRelatedQuestions from './FAQRelatedQuestions'
import FAQFeedback from './FAQFeedback'
import './FAQCard.css'

/**
 * FAQCard Component
 * Muestra una respuesta FAQ con formato enriquecido
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
        </div>
      </div>

      {/* Question */}
      <div className="faq-question" onClick={toggleExpand}>
        {faq.question}
      </div>

      {/* Content */}
      {isExpanded && (
        <div className="faq-content">
          {/* Short Answer */}
          <div className="faq-short-answer">
            {faq.shortAnswer}
          </div>

          {/* Detailed Answer */}
          <div className="faq-answer">
            {faq.detailedAnswer}
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
