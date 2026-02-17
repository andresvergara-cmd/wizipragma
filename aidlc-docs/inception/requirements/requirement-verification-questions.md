# Requirements Verification Questions - CENTLI Evolution

Por favor responde las siguientes preguntas para clarificar los requisitos de la evolución de WiZi a CENTLI. Responde cada pregunta colocando la letra de tu elección después de la etiqueta [Answer]:

---

## SECCIÓN 1: CONTEXTO DE NEGOCIO Y TIMELINE

### Question 1
¿En qué etapa se encuentra actualmente la demo WiZi?

A) Proof of Concept (PoC) - solo demostración técnica
B) MVP con usuarios de prueba internos del banco
C) Piloto con usuarios reales externos (clientes del banco)
D) Beta pública con usuarios limitados
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 2
¿Cuál es el timeline objetivo para tener CENTLI en producción?

A) 3 meses o menos (urgente)
B) 3-6 meses (corto plazo)
C) 6-12 meses (mediano plazo)
D) Más de 12 meses (largo plazo)
E) Other (please describe after [Answer]: tag below)

[Answer]: E Debemos realizarlo en 8 horas

### Question 3
¿Cuántos usuarios piloto están planeados para la primera fase de CENTLI?

A) Menos de 100 usuarios (piloto muy limitado)
B) 100-1,000 usuarios (piloto pequeño)
C) 1,000-10,000 usuarios (piloto mediano)
D) Más de 10,000 usuarios (piloto grande)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 4
¿Cuál es el objetivo de volumen de transacciones diarias esperado?

A) Menos de 1,000 transacciones/día
B) 1,000-10,000 transacciones/día
C) 10,000-100,000 transacciones/día
D) Más de 100,000 transacciones/día
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## SECCIÓN 2: INTEGRACIÓN CORE BANCARIO

### Question 5
¿Qué core bancario utiliza el banco?

A) Temenos (T24/Transact)
B) Oracle FLEXCUBE
C) FIS (Systematics, IBS, etc.)
D) Mambu
E) Technisys
F) Core bancario propietario/custom
G) Other (please describe after [Answer]: tag below)

[Answer]: G en este momento no hay un core, genera un core mock

### Question 6
¿El core bancario tiene APIs REST/GraphQL disponibles?

A) Sí, APIs REST modernas bien documentadas
B) Sí, pero APIs legacy (SOAP, XML-RPC)
C) No, solo acceso directo a base de datos
D) No estoy seguro, necesito verificar
E) Other (please describe after [Answer]: tag below)

[Answer]: E, Genera Mock para esto

### Question 7
¿Qué operaciones del core bancario necesita CENTLI?

A) Solo consultas (saldos, movimientos, perfil) - read-only
B) Consultas + transferencias internas (entre cuentas del mismo banco)
C) Consultas + transferencias internas + SPEI/CoDi/DiMo
D) Todas las operaciones bancarias (incluye pagos de servicios, inversiones, etc.)
E) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 8
¿Existe un ambiente sandbox/desarrollo del core bancario para testing?

A) Sí, sandbox completo con datos sintéticos
B) Sí, pero limitado (no todas las operaciones disponibles)
C) No, solo ambiente de producción
D) No estoy seguro
E) Other (please describe after [Answer]: tag below)

[Answer]: E, no tenemos core bancario por lo tanto será un mock en AWS

---

## SECCIÓN 3: SISTEMAS DE PAGO MEXICANOS

### Question 9
¿El banco ya tiene integración con SPEI (Sistema de Pagos Electrónicos Interbancarios)?

A) Sí, integración completa y funcional
B) Sí, pero necesita modernización/mejoras
C) No, hay que construirla desde cero
D) No estoy seguro
E) Other (please describe after [Answer]: tag below)

[Answer]:  E,  como estamos simulando el banco, también haz mock de las pasarelas y sistemas de pagos

### Question 10
¿El banco ya tiene integración con CoDi (Cobro Digital)?

A) Sí, integración completa y funcional
B) Sí, pero necesita modernización/mejoras
C) No, hay que construirla desde cero
D) No aplica - no planeamos usar CoDi
E) Other (please describe after [Answer]: tag below)

[Answer]: E, Construirlo desde 0 pero en mock

### Question 11
¿El banco ya tiene integración con DiMo (Dinero Móvil)?

A) Sí, integración completa y funcional
B) Sí, pero necesita modernización/mejoras
C) No, hay que construirla desde cero
D) No aplica - no planeamos usar DiMo
E) Other (please describe after [Answer]: tag below)

[Answer]: E, Construirlo desde 0 pero en mock

---

## SECCIÓN 4: SEGURIDAD Y COMPLIANCE

### Question 12
¿El banco tiene certificación CNBV para banca digital?

A) Sí, certificación completa vigente
B) En proceso de certificación
C) No, esto es parte del proyecto
D) No estoy seguro
E) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 13
¿Qué sistema de autenticación utilizan actualmente?

A) Usuario/contraseña tradicional
B) Biometría (huella, facial) en app móvil
C) Token físico/OTP
D) Autenticación multifactor (MFA) completa
E) No tienen sistema de autenticación aún
F) Other (please describe after [Answer]: tag below)

[Answer]: E

### Question 14
¿Qué nivel de autenticación requiere CENTLI para transacciones?

A) Biometría pasiva para todo (bajo fricción)
B) Biometría pasiva para bajo riesgo, MFA para alto riesgo
C) Siempre MFA para cualquier transacción
D) Depende del monto y tipo de transacción
E) Other (please describe after [Answer]: tag below)

[Answer]: E, Queremos que tenga seguridad para generar transacciones de voz sencillo pero seguro

### Question 15
¿Qué auditorías de seguridad se requieren?

A) Solo auditoría interna del banco
B) Auditoría CNBV obligatoria
C) Certificaciones internacionales (SOC 2, ISO 27001)
D) Todas las anteriores
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## SECCIÓN 5: INTEGRACIÓN RETAIL Y BENEFICIOS

### Question 16
¿El banco ya tiene acuerdos comerciales con retailers mexicanos?

A) Sí, acuerdos firmados con múltiples retailers (Oxxo, Walmart, Liverpool, etc.)
B) Sí, pero solo con algunos retailers
C) No, hay que establecer acuerdos comerciales
D) No estoy seguro
E) Other (please describe after [Answer]: tag below)

[Answer]: E, el banco tendrá su propio market place

### Question 17
¿Los retailers tienen APIs para consultar/aplicar beneficios?

A) Sí, APIs REST modernas disponibles
B) Sí, pero APIs legacy o limitadas
C) No, integración manual o batch
D) No estoy seguro
E) Other (please describe after [Answer]: tag below)

[Answer]: E, Crealos mock

### Question 18
¿Qué tipos de beneficios debe gestionar CENTLI?

A) Solo cashback
B) Cashback + puntos de lealtad
C) Cashback + puntos + meses sin intereses (MSI)
D) Todos los anteriores + descuentos + promociones especiales
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## SECCIÓN 6: ARQUITECTURA Y TECNOLOGÍA

### Question 19
¿Hay presupuesto aprobado para AWS Bedrock AgentCore?

A) Sí, presupuesto aprobado sin restricciones
B) Sí, pero con límite mensual específico
C) No, necesita aprobación
D) No estoy seguro del costo de AgentCore
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 20
¿Cuál es el presupuesto mensual estimado para AWS (si conocido)?

A) Menos de $5,000 USD/mes
B) $5,000 - $20,000 USD/mes
C) $20,000 - $50,000 USD/mes
D) Más de $50,000 USD/mes
E) No hay presupuesto definido aún
F) Other (please describe after [Answer]: tag below)

[Answer]: E

### Question 21
¿Qué capacidades multimodales necesita CENTLI?

A) Solo texto (como WiZi actual)
B) Texto + voz (speech-to-text y text-to-speech)
C) Texto + voz + imágenes (ej. fotos de recibos)
D) Todas las anteriores + video
E) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 22
¿Qué canales de comunicación debe soportar CENTLI?

A) Solo app móvil
B) App móvil + web
C) App móvil + web + WhatsApp/SMS
D) Todos los anteriores + asistentes de voz (Alexa, Google)
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## SECCIÓN 7: DATOS Y PRIVACIDAD

### Question 23
¿Los datos actuales en data/*.json son reales o sintéticos?

A) Datos reales anonimizados de clientes
B) Datos sintéticos generados para demo
C) Mezcla de datos reales y sintéticos
D) No estoy seguro
E) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 24
¿Cómo se sincronizarán los datos del core bancario con CENTLI?

A) Tiempo real vía APIs (cada consulta va al core)
B) Near real-time con caché (actualización cada minutos)
C) Batch periódico (actualización cada horas/días)
D) Híbrido (algunos datos real-time, otros batch)
E) Other (please describe after [Answer]: tag below)

[Answer]: A, E el core es mockeado pero debemos simular la funcionalidad de la A

### Question 25
¿Qué datos sensibles (PII) debe manejar CENTLI?

A) Nombre, email, teléfono (PII básico)
B) PII básico + datos financieros (saldos, transacciones)
C) PII básico + financiero + datos biométricos
D) Todos los anteriores + documentos de identidad (INE, RFC)
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## SECCIÓN 8: CAPACIDADES AGENTIC

### Question 26
¿Qué nivel de autonomía debe tener CENTLI para ejecutar transacciones?

A) Siempre requiere confirmación explícita del usuario
B) Puede ejecutar transacciones de bajo monto sin confirmación
C) Puede ejecutar transacciones recurrentes/conocidas sin confirmación
D) Alta autonomía con límites configurables por usuario
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 27
¿CENTLI debe poder anticipar necesidades proactivamente?

A) Sí, alertas proactivas críticas (ej. "pago vence mañana")
B) Sí, alertas + sugerencias de optimización
C) Sí, alertas + sugerencias + ejecución automática (con límites)
D) No, solo debe responder a solicitudes del usuario
E) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 28
¿Qué debe recordar CENTLI sobre el usuario (Managed Memory)?

A) Solo historial de conversación
B) Historial + beneficiarios frecuentes
C) Historial + beneficiarios + patrones de gasto
D) Todo lo anterior + preferencias + metas financieras
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## SECCIÓN 9: CALIDAD Y OPERACIONES

### Question 29
¿Qué SLA (Service Level Agreement) se requiere para CENTLI?

A) 99% disponibilidad (7.2 horas downtime/mes)
B) 99.9% disponibilidad (43 minutos downtime/mes)
C) 99.99% disponibilidad (4.3 minutos downtime/mes)
D) 99.999% disponibilidad (26 segundos downtime/mes)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 30
¿Se requiere disaster recovery multi-región?

A) Sí, activo-activo en múltiples regiones AWS
B) Sí, activo-pasivo (región primaria + backup)
C) No, single-region es suficiente
D) No estoy seguro
E) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 31
¿Qué nivel de testing se requiere antes de producción?

A) Testing manual básico
B) Testing automatizado (unit + integration tests)
C) Testing automatizado + QA manual + UAT con usuarios
D) Todo lo anterior + penetration testing + load testing
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## SECCIÓN 10: EQUIPO Y ORGANIZACIÓN

### Question 32
¿Quién es el sponsor ejecutivo del proyecto CENTLI?

A) CTO/CIO del banco
B) VP de Innovación Digital
C) Director de Banca Digital
D) Múltiples sponsors
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 33
¿Qué equipo técnico está disponible para el proyecto?

A) Solo equipo externo/consultores
B) Equipo mixto (internos + externos)
C) Principalmente equipo interno del banco
D) No hay equipo asignado aún
E) Other (please describe after [Answer]: tag below)

[Answer]: E, tres desarrolladores a traves del mismo repositorio github con kiro y una sola cuenta de AWS

### Question 34
¿Qué experiencia tiene el equipo con AWS y arquitecturas serverless?

A) Expertos - múltiples proyectos serverless en producción
B) Intermedio - algunos proyectos serverless
C) Básico - conocimiento teórico, poca experiencia práctica
D) Ninguna - necesitan capacitación
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## SECCIÓN 11: PRIORIDADES Y FASES

### Question 35
¿Cuál es la prioridad #1 para la primera fase de CENTLI?

A) Seguridad y compliance (CNBV)
B) Capacidades transaccionales (SPEI, transferencias)
C) Experiencia de usuario (multimodal, voz)
D) Optimización de beneficios retail
E) Other (please describe after [Answer]: tag below)

[Answer]: E, El Flujo de "Transferencia Social" (P2P)
Usuario: "Bankia, envíale 50 lucas a mi hermano para el almuerzo".Acción IA: Identifica al contacto "hermano" en el CRM, verifica saldo, valida la voz del usuario en segundo plano y ejecuta la transferencia vía API.KPI: Reducción de clics de 8 (promedio app) a 0.

### Question 36
¿Qué funcionalidades pueden esperar para una fase 2?

A) Capacidades avanzadas de voz/multimodal
B) Integraciones con retailers
C) Funciones de inversión/ahorro
D) Expansión a otros países
E) Other (please describe after [Answer]: tag below)

[Answer]: E, El Flujo de "Retail Inteligente" (Cashback/Promos)
Usuario: "Voy a pagar en el Éxito, ¿qué promos tengo?"Acción IA: Cruza geolocalización con la base de aliados retail, activa el cupón de cashback automáticamente y prepara el código QR o link de pago.KPI: Incremento en el uso de beneficios del banco en un 30%.

### Question 37
¿Hay alguna funcionalidad que NO debe incluirse en CENTLI?

A) No, todas las capacidades descritas son necesarias
B) Sí, algunas funcionalidades deben excluirse
C) No estoy seguro, necesito discutir con stakeholders
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

Por favor completa todas las respuestas y avísame cuando hayas terminado para que pueda analizar tus respuestas y proceder con el análisis de requisitos.
