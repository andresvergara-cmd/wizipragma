# User Stories Generation Plan - CENTLI Hackathon

## Execution Checklist

### Phase 1: Persona Definition
- [x] Identify primary user personas based on requirements
- [x] Define persona characteristics (demographics, goals, pain points)
- [x] Create persona profiles with relevant attributes
- [x] Document persona motivations and context

### Phase 2: Story Identification
- [x] Extract user-facing features from requirements
- [x] Identify user journeys and workflows
- [x] Map features to personas
- [x] Prioritize stories based on Must Have / Should Have / Could Have

### Phase 3: Story Writing
- [x] Write stories in standard format: "As a [persona], I want [goal], so that [benefit]"
- [x] Ensure stories follow INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [x] Add context and background for each story
- [x] Include technical notes where relevant

### Phase 4: Acceptance Criteria
- [x] Define clear acceptance criteria for each story
- [x] Use Given-When-Then format where appropriate
- [x] Include edge cases and error scenarios
- [x] Ensure criteria are testable and measurable

### Phase 5: Story Organization
- [x] Group stories by epic or feature area
- [x] Assign priority levels (Must Have, Should Have, Could Have)
- [x] Map stories to 8-hour timeline
- [x] Identify dependencies between stories

### Phase 6: Validation
- [x] Verify all stories are user-centered
- [x] Check INVEST criteria compliance
- [x] Ensure acceptance criteria are complete
- [x] Validate stories cover all requirements

---

## Context-Appropriate Questions

Please answer the following questions to guide user story generation:


### Question 1: User Personas
¿Qué personas de usuario debemos definir para CENTLI?

A) Solo "Usuario Bancario" (persona única genérica)
B) "Usuario Bancario" + "Beneficiario" (quien recibe transferencias)
C) "Usuario Bancario" + "Comprador" + "Beneficiario" (roles diferenciados)
D) Múltiples perfiles de Usuario Bancario (ej. joven tech-savvy, adulto tradicional, senior)
E) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 2: Story Granularity
¿Qué nivel de granularidad prefieres para las user stories?

A) Stories grandes (épicas) - una story por flujo completo (ej. "Como usuario quiero hacer transferencias P2P")
B) Stories medianas - una story por paso principal (ej. "Como usuario quiero identificar beneficiario", "Como usuario quiero confirmar transferencia")
C) Stories pequeñas - una story por acción específica (ej. "Como usuario quiero que el sistema valide mi saldo")
D) Mix según complejidad - stories grandes para flujos simples, pequeñas para flujos complejos
E) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 3: Story Organization
¿Cómo prefieres organizar las user stories?

A) Por flujo de usuario (todas las stories de P2P juntas, todas las de compra juntas)
B) Por prioridad (Must Have primero, luego Should Have, luego Could Have)
C) Por componente técnico (stories de voz, stories de core mock, stories de marketplace)
D) Por épica (épica de Transferencias con sub-stories, épica de Compras con sub-stories)
E) Other (please describe after [Answer]: tag below)

[Answer]: E, escoge la mejor forma para que 3 personas desarrolen con kiro de forma simultanea

### Question 4: Acceptance Criteria Format
¿Qué formato prefieres para los criterios de aceptación?

A) Lista simple de bullets (- Criterio 1, - Criterio 2)
B) Given-When-Then (Given contexto, When acción, Then resultado)
C) Checklist de validación ([ ] Criterio 1, [ ] Criterio 2)
D) Mix según tipo de story (Given-When-Then para flujos, bullets para features simples)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 5: Story Scope for 8-Hour Hackathon
Dado el timeline de 8 horas, ¿qué alcance de stories debemos crear?

A) Solo Must Have (transferencia P2P + compra) - mínimo viable
B) Must Have + Should Have (incluye CRM, beneficios múltiples) - alcance completo planeado
C) Must Have + Should Have + Could Have (incluye imágenes, alertas) - alcance aspiracional
D) Todas las stories pero marcadas claramente por prioridad
E) Other (please describe after [Answer]: tag below)

[Answer]: E

### Question 6: Technical Details in Stories
¿Cuánto detalle técnico incluir en las user stories?

A) Cero - solo perspectiva de usuario, sin mencionar tecnología
B) Mínimo - mencionar tecnología solo cuando es relevante para el usuario (ej. "por voz")
C) Moderado - incluir notas técnicas al final de cada story
D) Alto - incluir detalles de implementación (AWS services, APIs)
E) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 7: Error Scenarios
¿Cómo manejar escenarios de error en las stories?

A) Stories separadas para cada escenario de error (ej. "Como usuario quiero ver error de saldo insuficiente")
B) Incluir escenarios de error en acceptance criteria de la story principal
C) Una story genérica de "manejo de errores" que cubre todos los casos
D) Solo documentar happy path, errores se manejan en implementación
E) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 8: Story Dependencies
¿Cómo documentar dependencias entre stories?

A) No documentar - asumir que todas las stories son independientes
B) Mencionar dependencias en la descripción de cada story
C) Crear diagrama de dependencias separado
D) Usar numeración que refleje orden de implementación
E) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 9: Demo Validation
¿Las stories deben incluir criterios específicos para validar la demo?

A) Sí - cada story debe tener sección "Demo Validation" con pasos específicos
B) Sí - pero solo para Must Have stories
C) No - acceptance criteria son suficientes para validación
D) Crear checklist de demo separado basado en stories
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 10: Story Estimation
¿Debemos incluir estimaciones de esfuerzo en las stories?

A) Sí - en horas (ej. 1h, 2h, 3h)
B) Sí - en story points (ej. 1, 2, 3, 5, 8)
C) Sí - en t-shirt sizes (S, M, L, XL)
D) No - solo prioridad (Must/Should/Could Have)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Story Breakdown Approaches

### Approach A: User Journey-Based
**Description**: Stories follow the natural flow of user interactions
**Example**:
- Epic: Transferencia P2P por Voz
  - Story 1: Iniciar transferencia por voz
  - Story 2: Identificar beneficiario
  - Story 3: Validar saldo
  - Story 4: Confirmar transferencia
  - Story 5: Recibir confirmación

**Pros**: Natural, fácil de entender, refleja experiencia real del usuario
**Cons**: Puede crear dependencias entre stories

### Approach B: Feature-Based
**Description**: Stories organizadas por capacidades del sistema
**Example**:
- Epic: Capacidades de Voz
  - Story 1: Entrada de voz (speech-to-text)
  - Story 2: Salida de voz (text-to-speech)
- Epic: Transacciones
  - Story 3: Transferencia P2P
  - Story 4: Compra de productos

**Pros**: Agrupa funcionalidad similar, facilita división de trabajo
**Cons**: Menos centrado en usuario, puede perder contexto de journey

### Approach C: Persona-Based
**Description**: Stories agrupadas por tipo de usuario
**Example**:
- Persona: Usuario Bancario
  - Story 1: Enviar dinero a beneficiario
  - Story 2: Comprar producto
  - Story 3: Ver historial
- Persona: Beneficiario
  - Story 4: Recibir notificación de transferencia

**Pros**: Enfoque fuerte en diferentes necesidades de usuarios
**Cons**: Puede duplicar stories si múltiples personas hacen lo mismo

### Approach D: Epic-Based (Hierarchical)
**Description**: Stories estructuradas como épicas con sub-stories
**Example**:
- Epic: Banca por Voz
  - Sub-Epic: Transferencias
    - Story 1.1: P2P por voz
    - Story 1.2: Validación de identidad
  - Sub-Epic: Compras
    - Story 2.1: Compra con beneficios
    - Story 2.2: Aplicación de cashback

**Pros**: Estructura clara, fácil navegación, refleja arquitectura
**Cons**: Puede ser over-engineering para proyecto pequeño

### Recommended Approach for This Project
Given the 8-hour hackathon context with 2 main flows (P2P + Compra), I recommend:
- **Hybrid: Epic-Based + Priority-Based**
- 2 main epics (Transferencia P2P, Compra de Productos)
- Stories dentro de cada épica organizadas por journey
- Prioridad clara (Must/Should/Could) para cada story
- Permite foco en Must Have mientras documenta alcance completo

---

Please fill in all [Answer]: tags above before proceeding.
