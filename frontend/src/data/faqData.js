// Base de Conocimiento FAQ para Comfi
// Inspirado en Comfama - Caja de Compensación Familiar

export const faqData = {
  'faq-afiliacion-001': {
    id: 'faq-afiliacion-001',
    category: 'afiliacion',
    categoryName: 'Afiliación y Tarifas',
    categoryIcon: '👥',
    question: '¿Cómo me afilio a Comfama?',
    shortAnswer: 'Tu empleador te afilia automáticamente al pagar aportes parafiscales.',
    detailedAnswer: `La afiliación a Comfama es automática cuando tu empleador realiza los aportes parafiscales (4% del salario). No necesitas hacer ningún trámite adicional.

Pasos:
1. Tu empleador te registra en el sistema
2. Recibes tu número de afiliación
3. Puedes activar tu cuenta digital
4. Accedes a todos los beneficios`,
    relatedQuestions: [
      { id: 'faq-afiliacion-002', questionPreview: '¿Cuál es mi tarifa de afiliación?' }
    ],
    actions: [
      { type: 'button', label: 'Activar cuenta digital', action: 'activate_account' },
      { type: 'button', label: 'Verificar mi afiliación', action: 'check_affiliation' }
    ]
  },
  'faq-afiliacion-002': {
    id: 'faq-afiliacion-002',
    category: 'afiliacion',
    categoryName: 'Afiliación y Tarifas',
    categoryIcon: '👥',
    question: '¿Cuál es mi tarifa de afiliación?',
    shortAnswer: 'Tu tarifa depende de tu salario. Es el 4% que aporta tu empleador.',
    detailedAnswer: `La tarifa de afiliación es el 4% de tu salario mensual, que aporta tu empleador directamente. Tú no pagas nada de tu bolsillo.

Ejemplo:
• Salario: $2,000,000 COP
• Aporte mensual: $80,000 COP (4%)
• Pagado por: Tu empleador

Este aporte te da acceso a todos los servicios de Comfama.`,
    relatedQuestions: [
      { id: 'faq-afiliacion-001', questionPreview: '¿Cómo me afilio a Comfama?' }
    ],
    actions: [
      { type: 'button', label: 'Ver mi tarifa actual', action: 'show_my_rate' }
    ]
  },
  'faq-creditos-001': {
    id: 'faq-creditos-001',
    category: 'creditos',
    categoryName: 'Créditos y Servicios Financieros',
    categoryIcon: '💰',
    question: '¿Qué tipos de créditos ofrece Comfama?',
    shortAnswer: 'Ofrecemos créditos de vivienda, educación, libre inversión y vehículo.',
    detailedAnswer: `Comfama ofrece diferentes líneas de crédito para apoyar tu bienestar:

🏠 Crédito de Vivienda
• Compra de vivienda nueva o usada
• Mejoramiento de vivienda
• Tasas preferenciales
• Hasta 20 años plazo

📚 Crédito de Educación
• Pregrado y posgrado
• Cursos y diplomados
• Sin codeudor
• Hasta 5 años plazo

💰 Crédito de Libre Inversión
• Para cualquier necesidad
• Aprobación rápida
• Hasta 4 años plazo

🚗 Crédito de Vehículo
• Compra de vehículo nuevo o usado
• Hasta 5 años plazo`,
    relatedQuestions: [
      { id: 'faq-creditos-002', questionPreview: '¿Qué requisitos necesito?' }
    ],
    actions: [
      { type: 'button', label: 'Simular crédito', action: 'simulate_credit' },
      { type: 'button', label: 'Ver requisitos', action: 'show_requirements' }
    ]
  },
  'faq-creditos-002': {
    id: 'faq-creditos-002',
    category: 'creditos',
    categoryName: 'Créditos y Servicios Financieros',
    categoryIcon: '💰',
    question: '¿Qué requisitos necesito para solicitar un crédito?',
    shortAnswer: 'Ser afiliado activo, tener capacidad de pago y presentar documentación.',
    detailedAnswer: `Los requisitos varían según el tipo de crédito, pero en general necesitas:

Requisitos Generales:
✅ Ser afiliado activo de Comfama
✅ Tener al menos 6 meses de afiliación
✅ Capacidad de pago demostrable
✅ No tener créditos en mora

Documentación:
📄 Cédula de ciudadanía
📄 Certificado laboral (no mayor a 30 días)
📄 Últimos 3 desprendibles de pago
📄 Extractos bancarios (últimos 3 meses)`,
    relatedQuestions: [
      { id: 'faq-creditos-001', questionPreview: '¿Qué tipos de créditos ofrecen?' }
    ],
    actions: [
      { type: 'button', label: 'Verificar elegibilidad', action: 'check_eligibility' }
    ]
  },
  'faq-subsidios-001': {
    id: 'faq-subsidios-001',
    category: 'subsidios',
    categoryName: 'Subsidios y Beneficios',
    categoryIcon: '🎁',
    question: '¿Qué subsidios ofrece Comfama?',
    shortAnswer: 'Ofrecemos subsidios de vivienda, educación, salud y recreación.',
    detailedAnswer: `Comfama ofrece diversos subsidios para mejorar tu calidad de vida:

🏠 Subsidio de Vivienda
• Compra de vivienda VIS
• Mejoramiento de vivienda
• Hasta $30 millones

📚 Subsidio de Educación
• Útiles escolares
• Uniformes
• Matrículas

🏥 Subsidio de Salud
• Medicamentos
• Exámenes médicos
• Tratamientos especiales

🎉 Subsidio de Recreación
• Vacaciones recreativas
• Eventos culturales
• Actividades deportivas`,
    relatedQuestions: [],
    actions: [
      { type: 'button', label: 'Ver subsidios disponibles', action: 'show_subsidies' }
    ]
  }
}

export const quickFAQs = [
  {
    id: 'faq-afiliacion-001',
    icon: '👥',
    shortQuestion: '¿Cómo me afilio a Comfama?'
  },
  {
    id: 'faq-subsidios-001',
    icon: '🎁',
    shortQuestion: '¿Qué subsidios ofrece Comfama?'
  },
  {
    id: 'faq-creditos-001',
    icon: '💰',
    shortQuestion: '¿Qué tipos de créditos ofrece Comfama?'
  },
  {
    id: 'faq-educacion-001',
    icon: '📚',
    shortQuestion: '¿Cómo me inscribo a cursos?'
  },
  {
    id: 'faq-atencion-001',
    icon: '📞',
    shortQuestion: '¿Cuáles son los canales de atención?'
  },
  {
    id: 'help',
    icon: '❓',
    shortQuestion: 'Ayuda',
    isHelp: true
  }
]

export const getFAQById = (faqId) => {
  return faqData[faqId]
}

export default faqData
