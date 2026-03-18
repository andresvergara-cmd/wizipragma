// ProcessingIndicator - Indicadores visuales de procesamiento
// Muestra diferentes estados: sending, processing, thinking

import ComfiAvatar from '../Logo/ComfiAvatar'
import './ProcessingIndicator.css'

const ProcessingIndicator = ({ state = 'processing' }) => {
  const getIndicatorContent = () => {
    switch (state) {
      case 'sending':
        return {
          avatar: 'comfi-pulse',
          icon: null,
          text: 'Enviando...',
          className: 'processing-immediate'
        }
      
      case 'processing':
      case 'thinking':
        return {
          avatar: 'comfi-thinking',
          icon: '🧠',
          text: 'Comfi está pensando...',
          className: 'processing-thinking'
        }
      
      case 'typing':
        return {
          avatar: 'comfi-thinking',
          icon: null,
          text: 'Comfi está escribiendo...',
          className: 'processing-typing'
        }
      
      default:
        return {
          avatar: 'comfi-thinking',
          icon: null,
          text: 'Procesando...',
          className: 'processing-default'
        }
    }
  }

  const { avatar, icon, text, className } = getIndicatorContent()

  return (
    <div className="message bot">
      <div className="message-avatar">
        <ComfiAvatar 
          size={28} 
          className={`comfi-avatar ${avatar}`} 
          animated={true} 
        />
      </div>
      <div className={`message-bubble ${className}`}>
        <div className="processing-content">
          {icon && (
            <div className="processing-icon">
              {icon}
            </div>
          )}
          <div className="processing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <span className="processing-label">{text}</span>
      </div>
    </div>
  )
}

export default ProcessingIndicator
