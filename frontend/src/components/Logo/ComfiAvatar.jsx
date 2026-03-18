// Comfi - Avatar de Comfama
// Avatar personalizado para el asistente conversacional

const ComfiAvatar = ({ size = 40, className = '', animated = false }) => {
  return (
    <div 
      className={`comfi-avatar-container ${className} ${animated ? 'comfi-animated' : ''}`}
      style={{ width: size, height: size }}
    >
      <img 
        src="/comfi-avatar.png" 
        alt="Comfi - Asistente de Comfama"
        className="comfi-avatar-image"
        style={{ 
          width: '100%', 
          height: '100%',
          objectFit: 'cover',
          borderRadius: '50%'
        }}
      />
    </div>
  )
}

export default ComfiAvatar
