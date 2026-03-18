# 💬 Flujos Conversacionales para Comfi

## 🎯 Principios de Diseño Conversacional

### 1. Claridad
- Respuestas concisas (máximo 3 líneas de texto)
- Un objetivo por mensaje
- Lenguaje natural mexicano

### 2. Confianza
- Confirmaciones explícitas para acciones financieras
- Mostrar información completa antes de ejecutar
- Opciones de cancelar en cualquier momento

### 3. Personalización
- Usar nombre del usuario cuando esté disponible
- Recordar contexto de la conversación
- Adaptar tono según la situación

### 4. Feedback
- Estados visuales claros (loading, success, error)
- Confirmaciones inmediatas
- Progreso visible en tareas largas

---

## 📊 FLUJO 1: Consulta de Saldo

### Diagrama de Flujo

\`\`\`mermaid
graph TD
    A[Usuario: "¿Cuál es mi saldo?"] --> B{Usuario autenticado?}
    B -->|Sí| C[Comfi: Consultando saldo...]
    B -->|No| D[Comfi: Necesito verificar tu identidad]
    D --> E[Solicitar autenticación]
    E --> C
    C --> F[Mostrar BalanceCard]
    F --> G{Usuario quiere más info?}
    G -->|Sí| H[Mostrar transacciones recientes]
    G -->|No| I[Fin - Ofrecer ayuda adicional]
\`\`\`

### Ejemplo de Diálogo

**Usuario**: "¿Cuál es mi saldo?"

**Comfi** (con avatar `comfi-thinking`):
```
Un momento, consultando tu saldo... 🔍
```

**Comfi** (con avatar `comfi-speaking` + BalanceCard):
```
[BalanceCard Component]
💰 Saldo disponible
$15,234.50 MXN

[Botones]
[Transferir] [Ver detalle]

¿Necesitas algo más?
```

**Opciones de seguimiento**:
- "Ver mis últimas transacciones"
- "Hacer una transferencia"
- "No, gracias"

---

## 💸 FLUJO 2: Transferencia de Dinero

### Diagrama de Flujo

\`\`\`mermaid
graph TD
    A[Usuario: "Quiero transferir dinero"] --> B[Comfi: ¿A quién?]
    B --> C[Usuario: Proporciona destinatario]
    C --> D[Comfi: ¿Cuánto?]
    D --> E[Usuario: Proporciona monto]
    E --> F{Validar saldo suficiente}
    F -->|Sí| G[Comfi: ¿Concepto?]
    F -->|No| H[Comfi: Saldo insuficiente]
    H --> I[Ofrecer alternativas]
    G --> J[Usuario: Proporciona concepto]
    J --> K[Mostrar TransferConfirmation]
    K --> L{Usuario confirma?}
    L -->|Sí| M[Procesar transferencia]
    L -->|No| N[Cancelar - Volver al inicio]
    M --> O{Éxito?}
    O -->|Sí| P[Mostrar SuccessMessage]
    O -->|No| Q[Mostrar ErrorMessage]
    P --> R[Ofrecer comprobante]
\`\`\`

### Ejemplo de Diálogo

**Usuario**: "Quiero transferir dinero"

**Comfi** (con avatar `comfi-speaking`):
```
Perfecto, te ayudo con tu transferencia 💸

¿A quién quieres transferir?
Puedes decirme el nombre o número de cuenta.
```

**Usuario**: "A Juan Pérez"

**Comfi** (con avatar `comfi-thinking`):
```
Buscando a Juan Pérez en tus contactos... 🔍
```

**Comfi** (con avatar `comfi-speaking`):
```
Encontré a Juan Pérez
Cuenta: **** 1234

¿Cuánto quieres transferir?
```

**Usuario**: "$500"

**Comfi** (con avatar `comfi-speaking`):
```
Perfecto, $500 MXN

¿Cuál es el concepto de la transferencia?
(Opcional - puedes omitirlo)
```

**Usuario**: "Pago de comida"

**Comfi** (con avatar `comfi-speaking` + TransferConfirmation):
```
[TransferConfirmation Component]
✓ Confirma tu transferencia

Para: Juan Pérez
Cuenta: **** 1234
Monto: $500.00 MXN
Concepto: Pago de comida

[Botones]
[Cancelar] [✓ Confirmar]
```

**Usuario**: [Click en Confirmar]

**Comfi** (con avatar `comfi-loading`):
```
Procesando tu transferencia... ⏳
```

**Comfi** (con avatar `comfi-celebrate` + SuccessMessage):
```
[SuccessMessage Component]
¡Listo! ✅

Tu transferencia se realizó exitosamente

$500.00 MXN → Juan Pérez
Referencia: TRF-2024-001234

[Botón]
[Descargar comprobante]

¿Necesitas algo más?
```

---

## 🛒 FLUJO 3: Recomendación de Productos

### Diagrama de Flujo

\`\`\`mermaid
graph TD
    A[Usuario: "¿Qué productos tienen?"] --> B[Comfi: Analizar perfil]
    B --> C{Tiene productos activos?}
    C -->|Sí| D[Mostrar productos complementarios]
    C -->|No| E[Mostrar productos básicos]
    D --> F[Mostrar ProductRecommendation]
    E --> F
    F --> G{Usuario interesado?}
    G -->|Sí| H[Mostrar detalles del producto]
    G -->|No| I[Mostrar más opciones]
    H --> J{Usuario quiere solicitar?}
    J -->|Sí| K[Iniciar proceso de solicitud]
    J -->|No| L[Guardar interés para después]
\`\`\`

### Ejemplo de Diálogo

**Usuario**: "¿Qué productos financieros tienen?"

**Comfi** (con avatar `comfi-thinking`):
```
Déjame revisar qué productos podrían interesarte... 🔍
```

**Comfi** (con avatar `comfi-speaking`):
```
Basándome en tu perfil, te recomiendo estos productos:
```

**Comfi** (ProductRecommendation Component):
```
[ProductRecommendation Component]
🎯 Recomendado para ti

[Imagen del producto]

Crédito Personal Comfama
Hasta $50,000 MXN con tasa preferencial

✓ Tasa desde 12% anual
✓ Plazo hasta 36 meses
✓ Sin comisión por apertura
✓ Aprobación en 24 horas

[Botones]
[Ver más] [Solicitar]
```

**Usuario**: [Click en "Ver más"]

**Comfi** (con avatar `comfi-speaking`):
```
Crédito Personal Comfama 💰

Características:
• Monto: $5,000 - $50,000 MXN
• Tasa: 12% - 18% anual (según perfil)
• Plazo: 12, 24 o 36 meses
• Sin garantía hipotecaria

Requisitos:
✓ Ser afiliado a Comfama
✓ Antigüedad mínima 6 meses
✓ Ingresos comprobables

¿Te gustaría solicitar este crédito?
```

**Usuario**: "Sí, quiero solicitarlo"

**Comfi** (con avatar `comfi-celebrate`):
```
¡Excelente decisión! 🎉

Para continuar, necesito algunos datos:

1. ¿Cuánto necesitas? ($5,000 - $50,000)
2. ¿En cuántos meses? (12, 24 o 36)
3. ¿Para qué lo usarás?

Empecemos: ¿Cuánto necesitas?
```

---

## ❓ FLUJO 4: Preguntas Frecuentes (FAQ)

### Diagrama de Flujo

\`\`\`mermaid
graph TD
    A[Usuario: Pregunta] --> B[Comfi: Buscar en FAQ]
    B --> C{Encontró respuesta?}
    C -->|Sí| D[Mostrar FAQCard]
    C -->|No| E[Buscar en conocimiento general]
    E --> F{Encontró respuesta?}
    F -->|Sí| G[Mostrar respuesta + sugerir FAQ relacionados]
    F -->|No| H[Ofrecer contacto con humano]
    D --> I{Usuario satisfecho?}
    I -->|Sí| J[Solicitar feedback]
    I -->|No| K[Ofrecer más información]
    K --> L[Mostrar FAQs relacionados]
\`\`\`

### Ejemplo de Diálogo

**Usuario**: "¿Cómo me afilio a Comfama?"

**Comfi** (con avatar `comfi-thinking`):
```
Buscando información sobre afiliación... 🔍
```

**Comfi** (con avatar `comfi-speaking` + FAQCard):
```
[FAQCard Component]
✅ Encontré información sobre: Afiliación a Comfama

📋 ¿Cómo afiliarme a Comfama?

Para afiliarte a Comfama necesitas:

1. Ser trabajador de una empresa afiliada
2. Completar el formulario de registro
3. Presentar documentos:
   • Cédula de identidad
   • Certificado laboral
   • Comprobante de domicilio

Puedes hacerlo:
• En línea: www.comfama.com/afiliacion
• Presencial: En cualquier sede Comfama
• Por teléfono: 604 444 4444

[Botones de acción]
[Iniciar afiliación en línea] [Ver sedes]

Preguntas relacionadas:
• ¿Cuánto cuesta la afiliación?
• ¿Qué beneficios tengo al afiliarme?
• ¿Cuánto tarda el proceso?

¿Te fue útil esta información?
[👍 Sí] [👎 No]
```

**Usuario**: [Click en "¿Cuánto cuesta la afiliación?"]

**Comfi** (con avatar `comfi-speaking` + FAQCard):
```
[FAQCard Component]
💰 Tarifa de afiliación

El costo de afiliación depende de tu salario:

• Hasta 2 SMMLV: 2% del salario
• De 2 a 4 SMMLV: 3% del salario
• Más de 4 SMMLV: 4% del salario

Este aporte es mensual y se descuenta automáticamente de tu nómina.

Ejemplo:
Si ganas $2,000,000 mensuales (≈3 SMMLV):
Aporte: $60,000 mensuales (3%)

[Botón]
[Calcular mi tarifa]

¿Necesitas más información?
```

---

## 🎓 FLUJO 5: Onboarding Conversacional

### Diagrama de Flujo

\`\`\`mermaid
graph TD
    A[Primer uso detectado] --> B[Comfi: Saludo inicial]
    B --> C[Explicar capacidades]
    C --> D[Mostrar ejemplos de uso]
    D --> E[Ofrecer tour guiado]
    E --> F{Usuario acepta tour?}
    F -->|Sí| G[Iniciar tour paso a paso]
    F -->|No| H[Ir directo al chat]
    G --> I[Paso 1: Consultas]
    I --> J[Paso 2: Transacciones]
    J --> K[Paso 3: Voz]
    K --> L[Paso 4: Ayuda]
    L --> M[Finalizar tour]
    M --> N[Ofrecer primera acción]
\`\`\`

### Ejemplo de Diálogo

**Comfi** (con avatar `comfi-wave`, animación de saludo):
```
¡Hola! Soy Comfi 👋

Tu asistente personal de Comfama.
Estoy aquí para ayudarte con todo lo que necesites.

¿Es tu primera vez usando el chat?
[Sí, muéstrame cómo funciona] [No, ya sé usarlo]
```

**Usuario**: [Click en "Sí, muéstrame cómo funciona"]

**Comfi** (con avatar `comfi-speaking`):
```
¡Perfecto! Te haré un tour rápido 🎯

Son solo 4 pasos y toma menos de 1 minuto.

[Botón]
[Comenzar tour]
```

**Usuario**: [Click en "Comenzar tour"]

**Comfi** (con avatar `comfi-speaking`, Paso 1/4):
```
📊 Paso 1 de 4: Consultas

Puedo ayudarte a consultar:
• Tu saldo actual
• Tus transacciones
• Productos disponibles
• Información de tu cuenta

Ejemplo: "¿Cuál es mi saldo?"

[Botón]
[Siguiente →]
```

**Comfi** (con avatar `comfi-speaking`, Paso 2/4):
```
💸 Paso 2 de 4: Transacciones

Puedo ayudarte a:
• Transferir dinero
• Pagar servicios
• Comprar productos
• Solicitar créditos

Ejemplo: "Quiero transferir $500 a Juan"

[Botón]
[Siguiente →]
```

**Comfi** (con avatar `comfi-listening`, Paso 3/4):
```
🎤 Paso 3 de 4: Usa tu voz

Puedes hablar conmigo en lugar de escribir:

1. Click en el botón del micrófono 🎤
2. Di lo que necesitas
3. Yo te responderé

¡Es más rápido y natural!

[Botón]
[Siguiente →]
```

**Comfi** (con avatar `comfi-celebrate`, Paso 4/4):
```
❓ Paso 4 de 4: Siempre estoy aquí

Si tienes dudas:
• Pregúntame lo que sea
• Puedo explicarte cualquier cosa
• Estoy disponible 24/7

Ejemplo: "¿Cómo funciona el crédito?"

[Botón]
[¡Listo, comenzar! 🎉]
```

**Comfi** (con avatar `comfi-wave`):
```
¡Perfecto! Ya estás listo para usar Comfi 🎉

¿En qué puedo ayudarte hoy?

Sugerencias rápidas:
[Ver mi saldo] [Hacer transferencia] [Ver productos]
```

---

## 🔔 FLUJO 6: Notificaciones y Alertas

### Diagrama de Flujo

\`\`\`mermaid
graph TD
    A[Evento detectado] --> B{Tipo de evento}
    B -->|Transacción| C[Notificar transacción]
    B -->|Saldo bajo| D[Alertar saldo bajo]
    B -->|Pago próximo| E[Recordar pago]
    B -->|Oferta| F[Notificar oferta]
    C --> G[Mostrar detalles]
    D --> H[Sugerir acciones]
    E --> I[Ofrecer pagar ahora]
    F --> J[Mostrar oferta]
    G --> K{Usuario quiere más info?}
    K -->|Sí| L[Expandir información]
    K -->|No| M[Cerrar notificación]
\`\`\`

### Ejemplo de Diálogo

**Comfi** (con avatar `comfi-glow`, notificación proactiva):
```
🔔 Nueva transacción detectada

Se realizó un cargo en tu cuenta:

💳 Compra en Éxito
Monto: $125.50 MXN
Fecha: Hoy, 14:32

Saldo actual: $15,109.00 MXN

[Ver detalle] [Reportar problema]
```

**Comfi** (con avatar `comfi-speaking`, alerta de saldo bajo):
```
⚠️ Alerta de saldo bajo

Tu saldo actual es de $234.50 MXN

Tienes un pago programado de $500 MXN
para mañana.

¿Quieres hacer una transferencia desde
otra cuenta?

[Transferir fondos] [Ver opciones]
```

**Comfi** (con avatar `comfi-celebrate`, oferta especial):
```
🎁 ¡Oferta especial para ti!

Crédito Personal con tasa preferencial
Solo por hoy: 10% de descuento en comisiones

Hasta $30,000 MXN
Tasa desde 10% anual

Válido hasta las 23:59 de hoy

[Ver oferta] [Solicitar ahora]
```

---

## 🎯 FLUJO 7: Manejo de Errores

### Diagrama de Flujo

\`\`\`mermaid
graph TD
    A[Error detectado] --> B{Tipo de error}
    B -->|No entendí| C[Pedir clarificación]
    B -->|Error técnico| D[Disculparse + explicar]
    B -->|Acción no permitida| E[Explicar restricción]
    B -->|Timeout| F[Ofrecer reintentar]
    C --> G[Sugerir reformular]
    D --> H[Ofrecer alternativa]
    E --> I[Sugerir acción válida]
    F --> J[Reintentar automáticamente]
    G --> K{Usuario reformula?}
    K -->|Sí| L[Procesar nueva entrada]
    K -->|No| M[Ofrecer ayuda humana]
\`\`\`

### Ejemplo de Diálogo

**Usuario**: "asdfghjkl"

**Comfi** (con avatar `comfi-thinking`):
```
Mmm, no entendí bien 🤔

¿Podrías reformular tu pregunta?

Puedo ayudarte con:
• Consultar saldo
• Hacer transferencias
• Ver productos
• Responder preguntas

¿Qué necesitas?
```

**Usuario**: "Quiero transferir $10,000,000"

**Comfi** (con avatar `comfi-error`):
```
Ups, hay un problema ⚠️

Tu saldo actual ($15,234.50 MXN) no es
suficiente para esta transferencia.

¿Qué te gustaría hacer?
[Transferir otro monto] [Ver mi saldo] [Solicitar crédito]
```

**Usuario**: "Elimina mi cuenta"

**Comfi** (con avatar `comfi-speaking`):
```
Entiendo tu solicitud, pero no puedo
eliminar cuentas desde el chat 🔒

Para cancelar tu cuenta, necesitas:
1. Llamar al 604 444 4444
2. Visitar una sede Comfama
3. Enviar solicitud por correo

¿Hay algo más en lo que pueda ayudarte?
```

**Comfi** (con avatar `comfi-error`, error técnico):
```
Ups, algo salió mal 😔

Tuve un problema al procesar tu solicitud.

[Botón]
[Intentar de nuevo]

Si el problema persiste, puedes:
• Llamar al 604 444 4444
• Escribir a ayuda@comfama.com

¿Quieres intentar otra cosa?
```

---

## 📱 FLUJO 8: Contexto Multi-Sesión

### Diagrama de Flujo

\`\`\`mermaid
graph TD
    A[Usuario regresa] --> B{Hay conversación previa?}
    B -->|Sí| C[Cargar contexto]
    B -->|No| D[Iniciar nueva sesión]
    C --> E{Conversación reciente?}
    E -->|Sí| F[Ofrecer continuar]
    E -->|No| G[Resumir y cerrar]
    F --> H{Usuario quiere continuar?}
    H -->|Sí| I[Retomar conversación]
    H -->|No| J[Iniciar nueva]
    G --> J
\`\`\`

### Ejemplo de Diálogo

**Comfi** (con avatar `comfi-wave`, usuario regresa):
```
¡Hola de nuevo! 👋

Veo que hace 2 horas estábamos hablando
sobre una transferencia a Juan Pérez.

¿Quieres continuar con eso o prefieres
empezar algo nuevo?

[Continuar transferencia] [Empezar de nuevo]
```

**Usuario**: [Click en "Continuar transferencia"]

**Comfi** (con avatar `comfi-speaking`):
```
Perfecto, retomemos 💸

Estábamos por transferir:
• Destinatario: Juan Pérez
• Monto: $500 MXN
• Concepto: Pago de comida

¿Quieres proceder con esta transferencia?

[Sí, confirmar] [No, cambiar datos]
```

---

## 🎨 Componentes Visuales Recomendados

### 1. BalanceCard
```jsx
<BalanceCard
  balance={15234.50}
  currency="MXN"
  lastUpdate="Hace 5 minutos"
  actions={[
    { label: 'Transferir', onClick: handleTransfer },
    { label: 'Ver detalle', onClick: handleDetail }
  ]}
/>
```

### 2. TransferConfirmation
```jsx
<TransferConfirmation
  transfer={{
    recipient: 'Juan Pérez',
    account: '**** 1234',
    amount: 500,
    concept: 'Pago de comida'
  }}
  onConfirm={handleConfirm}
  onCancel={handleCancel}
/>
```

### 3. ProductRecommendation
```jsx
<ProductRecommendation
  product={{
    name: 'Crédito Personal',
    image: '/images/credito.jpg',
    description: 'Hasta $50,000 con tasa preferencial',
    features: [
      'Tasa desde 12% anual',
      'Plazo hasta 36 meses',
      'Sin comisión por apertura'
    ]
  }}
  onViewMore={handleViewMore}
  onApply={handleApply}
/>
```

### 4. FAQCard
```jsx
<FAQCard
  faq={{
    id: 'faq-001',
    question: '¿Cómo me afilio?',
    answer: 'Para afiliarte necesitas...',
    actions: [
      { label: 'Iniciar afiliación', type: 'primary' }
    ],
    relatedFAQs: ['faq-002', 'faq-003']
  }}
  onActionClick={handleAction}
  onRelatedClick={handleRelated}
  onFeedback={handleFeedback}
/>
```

### 5. SuccessMessage
```jsx
<SuccessMessage
  title="¡Listo!"
  message="Tu transferencia se realizó exitosamente"
  details={{
    amount: '$500.00 MXN',
    recipient: 'Juan Pérez',
    reference: 'TRF-2024-001234'
  }}
  action={{
    label: 'Descargar comprobante',
    onClick: handleDownload
  }}
/>
```

### 6. ErrorMessage
```jsx
<ErrorMessage
  title="Ups, algo salió mal"
  message="No pudimos procesar tu solicitud"
  errorCode="ERR-500"
  retry={handleRetry}
  support={{
    phone: '604 444 4444',
    email: 'ayuda@comfama.com'
  }}
/>
```

---

## 📊 Métricas de Éxito por Flujo

### Consulta de Saldo
- ✅ Tiempo de respuesta < 2 segundos
- ✅ Tasa de éxito > 99%
- ✅ Satisfacción > 4.5/5

### Transferencia
- ✅ Tasa de completación > 85%
- ✅ Tasa de error < 5%
- ✅ Tiempo promedio < 60 segundos

### Recomendación de Productos
- ✅ Click-through rate > 15%
- ✅ Tasa de solicitud > 5%
- ✅ Engagement > 30 segundos

### FAQ
- ✅ Tasa de resolución > 80%
- ✅ Feedback positivo > 75%
- ✅ Escalación a humano < 20%

---

**Diseñado con ❤️ para Comfama**
