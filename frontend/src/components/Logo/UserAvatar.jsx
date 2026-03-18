// UserAvatar - Avatar personalizado para mensajes del usuario
// Genera iniciales y colores basados en el nombre del usuario

const UserAvatar = ({ size = 36, userName = 'Usuario', className = '' }) => {
  // Obtener iniciales del nombre
  const getInitials = (name) => {
    return name
      .split(' ')
      .map(word => word[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  // Generar color basado en el nombre (consistente)
  const getColorFromName = (name) => {
    const colors = [
      '#4a90e2', // Azul
      '#50c878', // Verde esmeralda
      '#ff6b6b', // Rojo coral
      '#ffa500', // Naranja
      '#9b59b6', // Púrpura
      '#3498db', // Azul cielo
    ]
    const index = name.charCodeAt(0) % colors.length
    return colors[index]
  }

  const initials = getInitials(userName)
  const bgColor = getColorFromName(userName)

  return (
    <div 
      className={`user-avatar-container ${className}`}
      style={{ 
        width: size, 
        height: size,
        background: `linear-gradient(135deg, ${bgColor} 0%, ${bgColor}dd 100%)`,
      }}
    >
      <span className="user-initials" style={{ fontSize: `${size * 0.4}px` }}>
        {initials}
      </span>
    </div>
  )
}

export default UserAvatar
