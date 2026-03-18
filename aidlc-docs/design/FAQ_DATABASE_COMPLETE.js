// frontend/src/data/faqData.js
// Base de Conocimiento FAQ Completa para Comfi
// Inspirado en Comfama - Caja de Compensación Familiar

/**
 * ESTRUCTURA DE FAQ:
 * - id: Identificador único
 * - category: Categoría del FAQ
 * - categoryName: Nombre de la categoría
 * - categoryIcon: Emoji de la categoría
 * - question: Pregunta del usuario
 * - shortAnswer: Respuesta corta (1-2 líneas)
 * - detailedAnswer: Respuesta detallada (HTML)
 * - personalized: Si requiere personalización
 * - relatedQuestions: Array de FAQs relacionados
 * - actions: Array de acciones disponibles
 * - tags: Array de keywords para búsqueda
 * - priority: high | medium | low
 * - lastUpdated: Fecha de última actualización
 */

export const faqData = [
  // ============================================
  // CATEGORÍA 1: AFILIACIÓN Y TARIFAS
  // ============================================
  
  {
    id: 'faq-afiliacion-001',
    category: 'afiliacion',
    categoryName: 'Afiliación y Tarifas',
    categoryIcon: '👥',
    question: '¿Cómo me afilio a Comfama?',
    shortAnswer: 'Tu empleador te afilia automáticamente al pagar aportes parafiscales.',
    detailedAnswer: `
      <p>La afiliación a Comfama es <strong>automática</strong> cuando tu empleador 
      realiza los aportes parafiscales (4% del salario). No necesitas hacer ningún 
      trámite adicional.</p>
      
      <p><strong>Pasos:</strong></p>
      <ol>
        <li>Tu empleador te registra en el sistema</li>
        <li>Recibes tu número de afiliación</li>
        <li>Puedes activar tu cuenta digital</li>
        <li>Accedes a todos los beneficios</li>
      </ol>
    `,
    personalized: false,
    relatedQuestions: [
      { id: 'faq-afiliacion-002', questionPreview: '¿Cuál es mi tarifa de afiliación?' },
      { id: 'faq-afiliacion-003', questionPreview: '¿Cómo actualizo mis datos?' }
    ],
    actions: [
      { type: 'button', label: 'Activar cuenta digital', action: 'activate_account' },
      { type: 'button', label: 'Verificar mi afiliación', action: 'check_affiliation' }
    ],
    tags: ['afiliación', 'registro', 'empleador', 'alta', 'inscripción', 'como afiliarme'],
    priority: 'high',
    lastUpdated: '2024-01-15'
  },

  {
    id: 'faq-afiliacion-002',
    category: 'afiliacion',
    categoryName: 'Afiliación y Tarifas',
    categoryIcon: '👥',
    question: '¿Cuál es mi tarifa de afiliación?',
    shortAnswer: 'Tu tarifa depende de tu salario. Es el 4% que aporta tu empleador.',
    detailedAnswer: `
      <p>La tarifa de afiliación es el <strong>4% de tu salario mensual</strong>, 
      que aporta tu empleador directamente. Tú no pagas nada de tu bolsillo.</p>
      
      <p><strong>Ejemplo:</strong></p>
      <ul>
        <li>💰 Salario: $2,000,000 COP</li>
        <li>📊 Aporte mensual: $80,000 COP (4%)</li>
        <li>✅ Pagado por: Tu empleador</li>
      </ul>
      
      <p>Este aporte te da acceso a todos los servicios de Comfama.</p>
    `,
    personalized: true,
    relatedQuestions: [
      { id: 'faq-afiliacion-001', questionPreview: '¿Cómo me afilio a Comfama?' },
      { id: 'faq-subsidios-001', questionPreview: '¿Qué subsidios están disponibles?' }
    ],
    actions: [
      { type: 'button', label: 'Ver mi tarifa actual', action: 'show_my_rate' },
      { type: 'button', label: 'Calcular beneficios', action: 'calculate_benefits' }
    ],
    tags: ['tarifa', 'aporte', 'salario', 'costo', 'cuota', 'cuanto pago'],
    priority: 'high',
    lastUpdated: '2024-01-15'
  },

  {
    id: 'faq-afiliacion-003',
    category: 'afiliacion',
    categoryName: 'Afiliación y Tarifas',
    categoryIcon: '👥',
    question: '¿Cómo actualizo mis datos personales?',
    shortAnswer: 'Puedes actualizar tus datos en línea, en nuestras sedes o por teléfono.',
    detailedAnswer: `
      <p>Mantener tus datos actualizados es importante para recibir todos los beneficios.</p>
      
      <p><strong>Opciones para actualizar:</strong></p>
      
      <p><strong>1. En línea</strong> (más rápido)</p>
      <ul>
        <li>Ingresa a tu cuenta</li>
        <li>Ve a "Mi perfil"</li>
        <li>Actualiza la información</li>
        <li>Guarda los cambios</li>
      </ul>
      
      <p><strong>2. En nuestras sedes</strong></p>
      <ul>
        <li>Lleva tu cédula</li>
        <li>Acércate al módulo de atención</li>
        <li>Solicita actualización de datos</li>
      </ul>
      
      <p><strong>3. Por teléfono</strong></p>
      <ul>
        <li>Llama al 604 360 6060</li>
        <li>Opción 2: Actualización de datos</li>
        <li>Sigue las instrucciones</li>
      </ul>
    `,
    personalized: false,
    relatedQuestions: [
      { id: 'faq-cuenta-003', questionPreview: '¿Cómo cambio mi contraseña?' },
      { id: 'faq-afiliacion-001', questionPreview: '¿Cómo me afilio?' }
    ],
    actions: [
      { type: 'button', label: 'Actualizar ahora', action: 'update_profile' },
      { type: 'button', label: 'Ver sedes cercanas', action: 'find_offices' }
    ],
    tags: ['actualización', 'datos', 'perfil', 'cambiar', 'modificar', 'actualizar datos'],
    priority: 'medium',
    lastUpdated: '2024-01-15'
  },

  // ============================================
  // CATEGORÍA 2: CRÉDITOS Y SERVICIOS FINANCIEROS
  // ============================================

  {
    id: 'faq-creditos-001',
    category: 'creditos',
    categoryName: 'Créditos y Servicios Financieros',
    categoryIcon: '💰',
    question: '¿Qué tipos de créditos ofrece Comfama?',
    shortAnswer: 'Ofrecemos créditos de vivienda, educación, libre inversión y vehículo.',
    detailedAnswer: `
      <p>Comfama ofrece diferentes líneas de crédito para apoyar tu bienestar:</p>
      
      <p><strong>🏠 Crédito de Vivienda</strong></p>
      <ul>
        <li>Compra de vivienda nueva o usada</li>
        <li>Mejoramiento de vivienda</li>
        <li>Tasas preferenciales</li>
        <li>Hasta 20 años plazo</li>
      </ul>
      
      <p><strong>📚 Crédito de Educación</strong></p>
      <ul>
        <li>Pregrado y posgrado</li>
        <li>Cursos y diplomados</li>
        <li>Sin codeudor</li>
        <li>Hasta 5 años plazo</li>
      </ul>
      
      <p><strong>💰 Crédito de Libre Inversión</strong></p>
      <ul>
        <li>Para cualquier necesidad</li>
        <li>Aprobación rápida</li>
        <li>Hasta 4 años plazo</li>
        <li>Tasas competitivas</li>
      </ul>
      
      <p><strong>🚗 Crédito de Vehículo</strong></p>
      <ul>
        <li>Compra de vehículo nuevo o usado</li>
        <li>Hasta 5 años plazo</li>
        <li>Tasas preferenciales</li>
      </ul>
    `,
    personalized: false,
    relatedQuestions: [
      { id: 'faq-creditos-002', questionPreview: '¿Cuáles son los requisitos?' },
      { id: 'faq-creditos-003', questionPreview: '¿Cómo consulto mi saldo?' }
    ],
    actions: [
      { type: 'button', label: 'Simular crédito', action: 'simulate_credit' },
      { type: 'button', label: 'Ver requisitos', action: 'show_requirements' },
      { type: 'button', label: 'Solicitar crédito', action: 'apply_credit' }
    ],
    tags: ['crédito', 'préstamo', 'financiación', 'tipos', 'opciones', 'que creditos hay'],
    priority: 'high',
    lastUpdated: '2024-01-15'
  },

  {
    id: 'faq-creditos-002',
    category: 'creditos',
    categoryName: 'Créditos y Servicios Financieros',
    categoryIcon: '💰',
    question: '¿Qué requisitos necesito para solicitar un crédito?',
    shortAnswer: 'Ser afiliado activo, tener capacidad de pago y presentar documentación.',
    detailedAnswer: `
      <p>Los requisitos varían según el tipo de crédito, pero en general necesitas:</p>
      
      <p><strong>Requisitos Generales:</strong></p>
      <ul>
        <li>✅ Ser afiliado activo de Comfama</li>
        <li>✅ Tener al menos 6 meses de afiliación</li>
        <li>✅ Capacidad de pago demostrable</li>
        <li>✅ No tener créditos en mora</li>
      </ul>
      
      <p><strong>Documentación:</strong></p>
      <ul>
        <li>📄 Cédula de ciudadanía</li>
        <li>📄 Certificado laboral (no mayor a 30 días)</li>
        <li>📄 Últimos 3 desprendibles de pago</li>
        <li>📄 Extractos bancarios (últimos 3 meses)</li>
      </ul>
      
      <p><strong>Requisitos Específicos por Tipo:</strong></p>
      <ul>
        <li>🏠 <strong>Vivienda:</strong> Promesa de compraventa, avalúo</li>
        <li>📚 <strong>Educación:</strong> Carta de admisión, costos</li>
        <li>🚗 <strong>Vehículo:</strong> Cotización del vehículo</li>
      </ul>
    `,
    personalized: true,
    relatedQuestions: [
      { id: 'faq-creditos-001', questionPreview: '¿Qué tipos de créditos ofrecen?' },
      { id: 'faq-creditos-003', questionPreview: '¿Cómo consulto mi saldo?' }
    ],
    actions: [
      { type: 'button', label: 'Verificar mi elegibilidad', action: 'check_eligibility' },
      { type: 'button', label: 'Iniciar solicitud', action: 'start_application' }
    ],
    tags: ['requisitos', 'documentos', 'elegibilidad', 'que necesito', 'solicitar credito'],
    priority: 'high',
    lastUpdated: '2024-01-15'
  },

  {
    id: 'faq-creditos-003',
    category: 'creditos',
    categoryName: 'Créditos y Servicios Financieros',
    categoryIcon: '💰',
    question: '¿Cómo puedo consultar el saldo de mi crédito?',
    shortAnswer: 'Consulta tu saldo en línea, por app, teléfono o en nuestras sedes.',
    detailedAnswer: `
      <p>Tienes varias opciones para consultar el saldo de tu crédito:</p>
      
      <p><strong>1. En Línea</strong> 💻 (Recomendado)</p>
      <ul>
        <li>Ingresa a comfama.com</li>
        <li>Ve a "Mi cuenta"</li>
        <li>Selecciona "Mis créditos"</li>
        <li>Verás saldo, cuotas y estado</li>
      </ul>
      
      <p><strong>2. App Móvil</strong> 📱</p>
      <ul>
        <li>Descarga la app Comfama</li>
        <li>Ingresa con tu usuario</li>
        <li>Toca "Créditos"</li>
        <li>Consulta toda la información</li>
      </ul>
      
      <p><strong>3. Por Teléfono</strong> ☎️</p>
      <ul>
        <li>Llama al 604 360 6060</li>
        <li>Opción 3: Créditos</li>
        <li>Sigue las instrucciones</li>
      </ul>
      
      <p><strong>4. En Nuestras Sedes</strong> 🏢</p>
      <ul>
        <li>Acércate con tu cédula</li>
        <li>Solicita estado de cuenta</li>
        <li>Recibe información impresa</li>
      </ul>
    `,
    personalized: true,
    relatedQuestions: [
      { id: 'faq-cuenta-001', questionPreview: '¿Cómo consulto mi saldo?' },
      { id: 'faq-creditos-002', questionPreview: '¿Qué requisitos necesito?' }
    ],
    actions: [
      { type: 'button', label: 'Ver mi saldo ahora', action: 'show_credit_balance' },
      { type: 'button', label: 'Descargar estado de cuenta', action: 'download_statement' }
    ],
    tags: ['saldo', 'consulta', 'estado de cuenta', 'cuanto debo', 'mi credito'],
    priority: 'high',
    lastUpdated: '2024-01-15'
  },

  // Continúa con más FAQs...
  // Total: 52 FAQs completos en el archivo final

]

// ============================================
// CATEGORÍAS FAQ
// ============================================

export const faqCategories = [
  {
    id: 'afiliacion',
    name: 'Afiliación y Tarifas',
    icon: '👥',
    color: '#e6007e',
    description: 'Todo sobre tu afiliación y tarifas',
    questionCount: 12
  },
  {
    id: 'creditos',
    name: 'Créditos y Servicios Financieros',
    icon: '💰',
    color: '#ad37e0',
    description: 'Información sobre créditos y servicios',
    questionCount: 15
  },
  {
    id: 'subsidios',
    name: 'Subsidios y Beneficios',
    icon: '🎁',
    color: '#00a651',
    description: 'Conoce tus subsidios y beneficios',
    questionCount: 10
  },
  {
    id: 'servicios',
    name: 'Servicios y Programas',
    icon: '🏫',
    color: '#0066cc',
    description: 'Educación, recreación y más',
    questionCount: 8
  },
  {
    id: 'cuenta',
    name: 'Cuenta y Transacciones',
    icon: '📊',
    color: '#ff6b00',
    description: 'Gestiona tu cuenta y transacciones',
    questionCount: 7
  }
]

// ============================================
// QUICK ACTIONS (FAQs más frecuentes)
// ============================================

export const quickFAQs = [
  {
    id: 'faq-afiliacion-001',
    icon: '👥',
    shortQuestion: '¿Cómo me afilio?'
  },
  {
    id: 'faq-afiliacion-002',
    icon: '💰',
    shortQuestion: '¿Cuál es mi tarifa?'
  },
  {
    id: 'faq-creditos-001',
    icon: '🏠',
    shortQuestion: 'Tipos de créditos'
  },
  {
    id: 'faq-creditos-003',
    icon: '📊',
    shortQuestion: 'Consultar saldo'
  },
  {
    id: 'faq-subsidios-001',
    icon: '🎁',
    shortQuestion: 'Subsidios disponibles'
  },
  {
    id: 'faq-afiliacion-003',
    icon: '📝',
    shortQuestion: 'Actualizar datos'
  }
]

// ============================================
// UTILIDADES
// ============================================

/**
 * Obtiene FAQ por ID
 */
export const getFAQById = (faqId) => {
  return faqData.find(faq => faq.id === faqId)
}

/**
 * Obtiene FAQs por categoría
 */
export const getFAQsByCategory = (categoryId) => {
  return faqData.filter(faq => faq.category === categoryId)
}

/**
 * Obtiene FAQs relacionados
 */
export const getRelatedFAQs = (faqId) => {
  const currentFAQ = getFAQById(faqId)
  if (!currentFAQ || !currentFAQ.relatedQuestions) {
    return []
  }
  
  return currentFAQ.relatedQuestions
    .map(related => getFAQById(related.id))
    .filter(Boolean)
}

/**
 * Busca FAQs por texto
 */
export const searchFAQs = (searchText) => {
  const lowerSearch = searchText.toLowerCase()
  
  return faqData.filter(faq => 
    faq.question.toLowerCase().includes(lowerSearch) ||
    faq.shortAnswer.toLowerCase().includes(lowerSearch) ||
    faq.tags.some(tag => tag.toLowerCase().includes(lowerSearch))
  )
}

export default faqData
