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
