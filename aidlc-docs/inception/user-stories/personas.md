# User Personas - CENTLI

## Persona 1: Usuario Bancario

### Perfil Demográfico
- **Nombre**: Carlos Méndez
- **Edad**: 32 años
- **Ocupación**: Ingeniero de Software
- **Ubicación**: Ciudad de México
- **Nivel Socioeconómico**: Medio-Alto
- **Educación**: Licenciatura en Ingeniería

### Características Tecnológicas
- **Tech-Savvy**: Alto - usa apps bancarias regularmente
- **Dispositivos**: iPhone 14, MacBook Pro
- **Preferencias**: Interacciones rápidas, interfaces modernas
- **Experiencia Digital**: Experto en banca digital

### Contexto Financiero
- **Ingreso Anual**: $600,000 MXN
- **Saldo Promedio**: $50,000 MXN
- **Línea de Crédito**: $100,000 MXN
- **Comportamiento**: Hace 5-10 transferencias/mes, compras online frecuentes

### Objetivos y Motivaciones
- Realizar transacciones bancarias de forma rápida y eficiente
- Minimizar tiempo en tareas financieras rutinarias
- Maximizar beneficios (cashback, puntos, MSI)
- Tener control total de sus finanzas desde su móvil

### Pain Points
- Apps bancarias tradicionales requieren muchos clics
- Proceso de transferencia es tedioso (buscar beneficiario, ingresar datos, confirmar)
- Pierde beneficios porque no sabe qué retailers ofrecen cashback
- Necesita recordar fechas de pago manualmente

### Escenarios de Uso
1. **Transferencia Urgente**: "Necesito enviarle dinero a mi hermano para el almuerzo, pero estoy manejando"
2. **Compra Inteligente**: "Quiero comprar una laptop pero no sé dónde me dan mejores beneficios"
3. **Gestión Rápida**: "Necesito revisar mi saldo mientras estoy en una junta"

### Expectativas de CENTLI
- Poder hacer transferencias solo con voz mientras hace otras cosas
- Que el sistema recuerde a sus beneficiarios frecuentes
- Recibir recomendaciones proactivas de beneficios
- Experiencia fluida sin fricciones

---

## Persona 2: Comprador

### Perfil Demográfico
- **Nombre**: Ana Rodríguez
- **Edad**: 28 años
- **Ocupación**: Diseñadora Gráfica Freelance
- **Ubicación**: Guadalajara
- **Nivel Socioeconómico**: Medio
- **Educación**: Licenciatura en Diseño

### Características Tecnológicas
- **Tech-Savvy**: Medio-Alto - usa e-commerce regularmente
- **Dispositivos**: Samsung Galaxy S23, iPad
- **Preferencias**: Busca mejores precios y beneficios
- **Experiencia Digital**: Competente en compras online

### Contexto Financiero
- **Ingreso Anual**: $350,000 MXN (variable)
- **Saldo Promedio**: $25,000 MXN
- **Línea de Crédito**: $50,000 MXN
- **Comportamiento**: Compras online 2-3 veces/semana, busca promociones

### Objetivos y Motivaciones
- Encontrar las mejores ofertas y beneficios al comprar
- Maximizar cashback y puntos de lealtad
- Usar meses sin intereses para compras grandes
- Gestionar su presupuesto de forma inteligente

### Pain Points
- Difícil comparar beneficios entre diferentes retailers
- Pierde oportunidades de cashback porque no sabe qué banco usar
- Proceso de aplicar cupones/beneficios es manual y tedioso
- No sabe cuándo tiene promociones disponibles

### Escenarios de Uso
1. **Compra Planificada**: "Necesito una laptop para trabajo, quiero la mejor oferta con MSI"
2. **Compra Impulsiva**: "Vi un producto que me gusta, ¿qué beneficios tengo?"
3. **Optimización**: "¿En qué tienda me conviene más comprar esto?"

### Expectativas de CENTLI
- Ver automáticamente qué beneficios tiene disponibles
- Comparación clara de opciones (cashback vs MSI vs descuento)
- Aplicación automática de beneficios sin pasos manuales
- Notificaciones de promociones relevantes

---

## Persona 3: Beneficiario

### Perfil Demográfico
- **Nombre**: Juan López
- **Edad**: 35 años
- **Ocupación**: Profesor de Secundaria
- **Ubicación**: Monterrey
- **Nivel Socioeconómico**: Medio
- **Educación**: Licenciatura en Educación

### Características Tecnológicas
- **Tech-Savvy**: Medio - usa apps básicas
- **Dispositivos**: Xiaomi Redmi Note 11
- **Preferencias**: Simplicidad, claridad
- **Experiencia Digital**: Usuario casual de banca móvil

### Contexto Financiero
- **Ingreso Anual**: $280,000 MXN
- **Saldo Promedio**: $15,000 MXN
- **Línea de Crédito**: $30,000 MXN
- **Comportamiento**: Recibe transferencias de familiares regularmente

### Objetivos y Motivaciones
- Recibir dinero de forma rápida y segura
- Saber quién le envió dinero y por qué
- Tener notificaciones claras de transacciones
- Mantener registro de transferencias recibidas

### Pain Points
- A veces no sabe quién le envió dinero hasta que revisa la app
- Notificaciones bancarias son genéricas y poco informativas
- Difícil rastrear transferencias específicas en historial
- Preocupación por seguridad de transacciones

### Escenarios de Uso
1. **Recepción de Dinero**: "Mi hermano me envió dinero para el almuerzo"
2. **Verificación**: "¿Ya me llegó la transferencia que esperaba?"
3. **Historial**: "Necesito ver cuánto me ha enviado mi familia este mes"

### Expectativas de CENTLI
- Notificaciones claras y personalizadas de transferencias recibidas
- Información completa (quién envió, monto, concepto)
- Confirmación inmediata de recepción
- Seguridad en todas las transacciones

---

## Mapeo Persona-Story

### Usuario Bancario (Carlos)
- Stories de Transferencia P2P por Voz
- Stories de Gestión de Beneficiarios
- Stories de Consulta de Saldo
- Stories de Managed Memory
- Stories de Autenticación por Voz

### Comprador (Ana)
- Stories de Compra de Productos
- Stories de Optimización de Beneficios
- Stories de Marketplace
- Stories de Aplicación de Cashback/MSI
- Stories de Comparación de Ofertas

### Beneficiario (Juan)
- Stories de Recepción de Transferencias
- Stories de Notificaciones
- Stories de Historial de Transacciones
- Stories de Verificación de Seguridad

---

## Notas de Implementación

### Prioridad de Personas para Hackathon
1. **Usuario Bancario** (Must Have) - Persona principal para demo
2. **Comprador** (Must Have) - Segunda persona principal para demo
3. **Beneficiario** (Should Have) - Importante pero secundario para demo

### Datos de Prueba
- Crear perfiles de prueba para cada persona en DynamoDB
- Incluir relaciones (Carlos → Juan como "mi hermano")
- Preparar transacciones históricas para contexto
- Configurar beneficios relevantes para Ana

### Consideraciones de UX
- Carlos prefiere voz (manos libres)
- Ana prefiere visual (comparar opciones)
- Juan prefiere notificaciones claras (seguridad)
