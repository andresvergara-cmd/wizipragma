# Requirements Clarification Questions - CENTLI

He detectado contradicciones importantes en tus respuestas que necesitan clarificación antes de proceder con el análisis de requisitos.

---

## CONTRADICCIÓN 1: Timeline vs. Alcance del Proyecto

**Respuestas Contradictorias:**
- **Q2**: Timeline de **8 horas** para completar CENTLI
- **Q4**: Expectativa de **>100,000 transacciones/día**
- **Q21**: Capacidades **multimodales completas** (texto + voz + imágenes + video)
- **Q22**: **Múltiples canales** (app móvil + web + WhatsApp/SMS)
- **Q31**: Testing **exhaustivo** (automatizado + QA + UAT + penetration + load testing)

**Problema**: El alcance descrito requiere semanas/meses de desarrollo, pero el timeline es de 8 horas.

### Clarification Question 1
¿Qué significa "8 horas" en el contexto de este proyecto?

A) Completar TODO el sistema CENTLI funcional en 8 horas (imposible con el alcance descrito)
B) Completar un MVP/demo funcional básico en 8 horas (alcance muy reducido)
C) Completar la arquitectura y diseño en 8 horas, implementación después
D) Es un hackathon/sprint de 8 horas para demostrar concepto
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## CONTRADICCIÓN 2: Estado del Proyecto vs. Expectativas de Producción

**Respuestas Contradictorias:**
- **Q1**: Estado actual es **PoC (Proof of Concept)** - solo demostración técnica
- **Q3**: Solo **<100 usuarios** piloto
- **Q4**: Expectativa de **>100,000 transacciones/día** (volumen de producción masivo)
- **Q29**: SLA de **99.9%** disponibilidad (producción enterprise)

**Problema**: Un PoC con <100 usuarios no necesita arquitectura para >100K transacciones/día.

### Clarification Question 2
¿Cuál es el objetivo real para las primeras 8 horas?

A) PoC/Demo funcional para presentación (no necesita escalar a 100K tx/día)
B) Arquitectura completa lista para producción (diseño para 100K tx/día, implementación parcial)
C) Sistema funcional básico con capacidad de escalar después
D) Prototipo de alta fidelidad con datos mock
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## CONTRADICCIÓN 3: Alcance Multimodal vs. Timeline

**Respuestas Contradictorias:**
- **Q2**: Timeline de **8 horas**
- **Q21**: **Todas las modalidades** (texto + voz + imágenes + video)
- **Q22**: **Múltiples canales** (móvil + web + WhatsApp + SMS)

**Problema**: Implementar voz, imágenes, video, y múltiples canales requiere integraciones complejas (AWS Transcribe, Polly, Rekognition, Textract, Twilio, WhatsApp Business API, etc.)

### Clarification Question 3
Para el entregable de 8 horas, ¿qué modalidades y canales son REALMENTE necesarios?

A) Solo texto vía WebSocket (como WiZi actual) - factible en 8 horas
B) Texto + voz básica (Transcribe/Polly) - muy ajustado para 8 horas
C) Todas las modalidades pero simuladas/mock - factible en 8 horas
D) Arquitectura diseñada para todas, implementación solo texto - factible en 8 horas
E) Other (please describe after [Answer]: tag below)

[Answer]: E, Todas las modalidades de voz, textoo e imagenes con datos simulados

---

## CONTRADICCIÓN 4: Core Bancario Mock vs. Complejidad

**Respuestas Contradictorias:**
- **Q5-Q8**: Todo el core bancario es **mock en AWS**
- **Q7**: Necesita **TODAS las operaciones bancarias** (consultas, transferencias, SPEI, pagos servicios, inversiones)
- **Q9-Q11**: SPEI, CoDi, DiMo también son **mock**
- **Q2**: Timeline de **8 horas**

**Problema**: Crear mocks realistas de core bancario + SPEI + CoDi + DiMo + operaciones complejas es trabajo significativo.

### Clarification Question 4
¿Qué nivel de realismo necesitan los mocks para las 8 horas?

A) Mocks ultra-simples (respuestas hardcoded, sin lógica de negocio) - factible en 8 horas
B) Mocks con lógica básica (validaciones, actualización de saldos) - ajustado para 8 horas
C) Mocks realistas (simulan comportamiento real de sistemas bancarios) - imposible en 8 horas
D) Solo diseño de APIs mock, implementación después - factible en 8 horas
E) Other (please describe after [Answer]: tag below)

[Answer]: E, mock con logica básica, validaciones, consulta de saldo, transferencias entre personas y comppra de productos.

---

## CONTRADICCIÓN 5: Testing Exhaustivo vs. Timeline

**Respuestas Contradictorias:**
- **Q2**: Timeline de **8 horas**
- **Q31**: Testing **exhaustivo** (automatizado + QA manual + UAT + penetration testing + load testing)

**Problema**: Testing exhaustivo requiere días/semanas, no horas.

### Clarification Question 5
¿Qué nivel de testing se requiere para el entregable de 8 horas?

A) Sin testing formal (solo validación manual básica) - factible en 8 horas
B) Tests unitarios básicos para funciones críticas - muy ajustado para 8 horas
C) Plan de testing documentado, ejecución después - factible en 8 horas
D) Testing exhaustivo es para producción final, no para las 8 horas
E) Other (please describe after [Answer]: tag below)

[Answer]: E, lo suficiente para garantizar calidad en un hackaton

---

## CONTRADICCIÓN 6: Prioridad #1 vs. Alcance

**Respuestas Contradictorias:**
- **Q35**: Prioridad #1 es **"Transferencia Social P2P por voz"**
- **Q21**: Requiere capacidades de **voz completas**
- **Q14**: Autenticación por **voz simple pero segura**
- **Q2**: Timeline de **8 horas**

**Problema**: Implementar transferencias P2P con autenticación por voz requiere múltiples componentes (Transcribe, autenticación biométrica de voz, Action Groups, core mock, etc.)

### Clarification Question 6
Para el flujo de "Transferencia Social P2P por voz" en 8 horas, ¿qué es aceptable?

A) Demo simulado (usuario habla, sistema muestra lo que haría, no ejecuta realmente)
B) Flujo funcional con voz mock (texto simulando voz, transferencia real en mock)
C) Voz real (Transcribe) + transferencia mock funcional
D) Arquitectura completa diseñada, implementación parcial
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## PREGUNTA ADICIONAL: Definición de "Completado"

### Clarification Question 7
Después de 8 horas, ¿qué debe estar "completado" para considerar el proyecto exitoso?

A) Arquitectura documentada + diseño detallado + plan de implementación
B) PoC funcional del flujo P2P (aunque sea simplificado)
C) Sistema completo funcional en producción (imposible en 8 horas con este alcance)
D) Demo impresionante para stakeholders (funcionalidad mock pero presentable)
E) Other (please describe after [Answer]: tag below)

[Answer]: B, E, transferencia y compra tambien

---

Por favor responde estas 7 preguntas de clarificación para que pueda entender correctamente el alcance realista del proyecto y generar requisitos apropiados.
