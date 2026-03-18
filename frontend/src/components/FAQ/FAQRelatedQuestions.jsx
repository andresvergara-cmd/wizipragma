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
