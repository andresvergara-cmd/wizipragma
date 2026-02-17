// Cintéotl - Dios Azteca del Maíz
// Logo estilizado para CENTLI

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
      {/* Mazorca de maíz central */}
      <ellipse cx="50" cy="55" rx="18" ry="30" fill="#FFD700" stroke="#FFA500" strokeWidth="2"/>
      
      {/* Granos de maíz */}
      <circle cx="44" cy="45" r="3" fill="#FFA500"/>
      <circle cx="50" cy="45" r="3" fill="#FFA500"/>
      <circle cx="56" cy="45" r="3" fill="#FFA500"/>
      <circle cx="44" cy="52" r="3" fill="#FFA500"/>
      <circle cx="50" cy="52" r="3" fill="#FFA500"/>
      <circle cx="56" cy="52" r="3" fill="#FFA500"/>
      <circle cx="44" cy="59" r="3" fill="#FFA500"/>
      <circle cx="50" cy="59" r="3" fill="#FFA500"/>
      <circle cx="56" cy="59" r="3" fill="#FFA500"/>
      <circle cx="47" cy="66" r="3" fill="#FFA500"/>
      <circle cx="53" cy="66" r="3" fill="#FFA500"/>
      
      {/* Hojas superiores - estilo azteca */}
      <path
        d="M 50 25 Q 35 20 30 15 Q 28 12 32 10 Q 40 15 50 20"
        fill="#4CAF50"
        stroke="#2E7D32"
        strokeWidth="1.5"
      />
      <path
        d="M 50 25 Q 65 20 70 15 Q 72 12 68 10 Q 60 15 50 20"
        fill="#4CAF50"
        stroke="#2E7D32"
        strokeWidth="1.5"
      />
      <path
        d="M 50 22 Q 40 18 35 12 Q 33 9 37 8 Q 43 12 50 18"
        fill="#66BB6A"
        stroke="#2E7D32"
        strokeWidth="1.5"
      />
      <path
        d="M 50 22 Q 60 18 65 12 Q 67 9 63 8 Q 57 12 50 18"
        fill="#66BB6A"
        stroke="#2E7D32"
        strokeWidth="1.5"
      />
      
      {/* Hojas laterales */}
      <path
        d="M 32 50 Q 20 48 15 45 Q 12 43 14 40 Q 22 42 32 45"
        fill="#4CAF50"
        stroke="#2E7D32"
        strokeWidth="1.5"
      />
      <path
        d="M 68 50 Q 80 48 85 45 Q 88 43 86 40 Q 78 42 68 45"
        fill="#4CAF50"
        stroke="#2E7D32"
        strokeWidth="1.5"
      />
      
      {/* Detalles aztecas - patrones geométricos */}
      <circle cx="50" cy="35" r="2" fill="#8B4513"/>
      <circle cx="50" cy="72" r="2" fill="#8B4513"/>
      
      {/* Aura/resplandor - representando la divinidad */}
      <circle cx="50" cy="50" r="45" stroke="#FFD700" strokeWidth="1" fill="none" opacity="0.3"/>
      <circle cx="50" cy="50" r="42" stroke="#FFA500" strokeWidth="0.5" fill="none" opacity="0.2"/>
    </svg>
  )
}

export default CinteotlLogo
