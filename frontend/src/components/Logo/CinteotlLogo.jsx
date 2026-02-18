// Cintéotl - Dios Azteca del Maíz
// Logo profesional inspirado en arte azteca para CENTLI Bank

const CinteotlLogo = ({ size = 40, className = '' }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Círculo base - profesional y limpio */}
      <circle cx="50" cy="50" r="48" fill="url(#gradientBg)" />
      <circle cx="50" cy="50" r="48" stroke="#ad37e0" strokeWidth="2" fill="none" opacity="0.3"/>
      
      {/* Gradiente de fondo */}
      <defs>
        <linearGradient id="gradientBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#FFD700" stopOpacity="0.15"/>
          <stop offset="100%" stopColor="#FFA500" stopOpacity="0.1"/>
        </linearGradient>
        <linearGradient id="godGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#FFD700"/>
          <stop offset="50%" stopColor="#FFA500"/>
          <stop offset="100%" stopColor="#FF8C00"/>
        </linearGradient>
        <linearGradient id="purpleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#ad37e0"/>
          <stop offset="100%" stopColor="#8e2bb8"/>
        </linearGradient>
      </defs>
      
      {/* Cuerpo del Dios - estilo azteca simplificado y profesional */}
      <g transform="translate(50, 50)">
        {/* Cabeza - forma geométrica azteca */}
        <rect x="-12" y="-25" width="24" height="20" fill="url(#godGradient)" rx="2"/>
        
        {/* Tocado/Corona - símbolo de divinidad */}
        <path
          d="M -15 -25 L -12 -35 L -8 -32 L -4 -38 L 0 -33 L 4 -38 L 8 -32 L 12 -35 L 15 -25 Z"
          fill="url(#purpleGradient)"
          stroke="#8e2bb8"
          strokeWidth="1"
        />
        
        {/* Plumas decorativas */}
        <circle cx="-10" cy="-34" r="2" fill="#4CAF50"/>
        <circle cx="0" cy="-36" r="2" fill="#FF5722"/>
        <circle cx="10" cy="-34" r="2" fill="#4CAF50"/>
        
        {/* Ojos - estilo azteca */}
        <circle cx="-5" cy="-18" r="2" fill="#2E7D32"/>
        <circle cx="5" cy="-18" r="2" fill="#2E7D32"/>
        <circle cx="-5" cy="-18" r="1" fill="white"/>
        <circle cx="5" cy="-18" r="1" fill="white"/>
        
        {/* Nariz - geométrica */}
        <rect x="-2" y="-14" width="4" height="6" fill="#FF8C00" rx="1"/>
        
        {/* Boca - línea estilizada */}
        <path d="M -4 -7 Q 0 -5 4 -7" stroke="#8B4513" strokeWidth="1.5" fill="none"/>
        
        {/* Cuerpo - forma rectangular azteca */}
        <rect x="-10" y="-5" width="20" height="18" fill="url(#godGradient)" rx="2"/>
        
        {/* Decoración del pecho - patrón azteca */}
        <rect x="-6" y="0" width="12" height="2" fill="#ad37e0"/>
        <rect x="-4" y="4" width="8" height="2" fill="#4CAF50"/>
        <circle cx="0" cy="9" r="2" fill="#FF5722"/>
        
        {/* Brazos - estilizados */}
        <rect x="-18" y="-2" width="8" height="12" fill="#FFA500" rx="2"/>
        <rect x="10" y="-2" width="8" height="12" fill="#FFA500" rx="2"/>
      </g>
      
      {/* Aura decorativa */}
      <circle cx="50" cy="50" r="45" stroke="#FFD700" strokeWidth="1" fill="none" opacity="0.3"/>
      <circle cx="50" cy="50" r="42" stroke="#FFA500" strokeWidth="0.5" fill="none" opacity="0.2"/>
    </svg>
  )
}

export default CinteotlLogo
