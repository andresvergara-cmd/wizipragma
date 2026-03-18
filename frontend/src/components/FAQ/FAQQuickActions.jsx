import './FAQQuickActions.css'

/**
 * FAQQuickActions Component
 * Muestra acciones rápidas para FAQs más frecuentes
 */
const FAQQuickActions = ({ quickFAQs, onQuickFAQClick, onViewAll }) => {
  if (!quickFAQs || quickFAQs.length === 0) return null

  const handleClick = (faq) => {
    if (faq.isHelp) {
      // Si es el botón de ayuda, enviar mensaje de ayuda
      onQuickFAQClick?.('help')
    } else {
      // Si es una FAQ normal, enviar el ID
      onQuickFAQClick?.(faq.id)
    }
  }

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
            onClick={() => handleClick(faq)}
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
