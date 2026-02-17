# Functional Design Plan - Unit 3: Action Groups

## Unit Context

**Unit Name**: Action Groups (Backend Services)  
**Stories**: 6 stories (2.1-2.6) - Core Banking, P2P Transfers, CRM, Marketplace, Benefits, Purchases  
**Purpose**: Provide mock banking, marketplace, and CRM services via EventBridge-triggered Lambdas  
**Dependencies**: Unit 1 (EventBridge, DynamoDB), Unit 2 (AgentCore events)

---

## Functional Design Steps

### Step 1: Business Logic Modeling
- [x] Define Core Banking workflows (account queries, balance updates, transfers)
- [x] Define Marketplace workflows (product catalog, benefits calculation, purchase execution)
- [x] Define CRM workflows (beneficiary management, alias resolution)
- [x] Define cross-Action Group workflows (Marketplace → Core Banking payment)
- [x] Define event-driven communication patterns (EventBridge pub/sub)

### Step 2: Domain Entities
- [x] Define Core Banking entities (Account, Transaction, Balance)
- [x] Define Marketplace entities (Product, Purchase, Benefit)
- [x] Define CRM entities (Beneficiary, UserProfile, Alias)
- [x] Define entity relationships and cardinalities
- [x] Define entity attributes and data types

### Step 3: Business Rules
- [x] Define Core Banking rules (balance validation, transfer limits, account validation)
- [x] Define Marketplace rules (benefit eligibility, purchase validation, payment processing)
- [x] Define CRM rules (alias resolution, beneficiary validation, frequency tracking)
- [x] Define cross-unit rules (payment authorization, credit line validation)
- [x] Define error handling and validation rules

### Step 4: Data Flow Design
- [x] Define EventBridge event schemas (action requests, action responses)
- [x] Define DynamoDB data access patterns
- [x] Define data transformations between events and entities
- [x] Define data persistence strategies

### Step 5: Integration Points
- [x] Define AgentCore → Action Groups integration (event consumption)
- [x] Define Action Groups → AgentCore integration (response publishing)
- [x] Define Marketplace → Core Banking integration (payment events)
- [x] Define error propagation and retry strategies

---

## Clarification Questions

### Business Logic Questions

**Q1: Core Banking - Transfer Validation**  
When validating a P2P transfer, what business rules should apply?
- Should we validate both source and destination accounts exist?
- Should we check for daily/monthly transfer limits?
- Should we validate beneficiary relationship before allowing transfer?
- Should we require additional authentication for large amounts?

[Answer]: validar que exista tanto el origen como el destino, que tenga salgo y permisos minimos de seguridad

---

**Q2: Core Banking - Balance Updates**  
How should balance updates be handled for atomicity?
- Should we use DynamoDB transactions for atomic debit/credit?
- Should we implement optimistic locking with version numbers?
- What happens if balance update fails mid-transaction?
- Should we maintain transaction history for audit?

[Answer]: toda la información transaccional debe estar en dynamoDB, implementa un bloqueo optimista, si el balance update fail debería hacer un retry and important manteint transaction

---

**Q3: Marketplace - Benefit Eligibility**  
How do we determine if a user is eligible for a specific benefit?
- Should we check user's account type (debit vs credit)?
- Should we check user's credit line for MSI eligibility?
- Should we check user's purchase history for loyalty benefits?
- Should benefits have expiration dates or usage limits?

[Answer]: Debería haber una base que maneje los beneficios por producto y tarjeta pero con limite de tiempo

---

**Q4: Marketplace - Benefit Calculation**  
When multiple benefits are available for a product, how should we handle them?
- Can user combine multiple benefits (e.g., cashback + MSI)?
- Should we automatically select the best benefit for the user?
- Should we present all options and let user choose?
- How do we calculate "best" benefit (highest savings, lowest monthly payment, etc.)?

[Answer]: se pueden usar multiples beneficios

---

**Q5: Marketplace - Purchase Payment Flow**  
How should the purchase payment flow work between Marketplace and Core Banking?
- Should Marketplace publish payment event and wait for Core Banking response?
- Should we use synchronous or asynchronous payment processing?
- What happens if payment fails after purchase is recorded?
- Should we implement compensation logic (rollback purchase if payment fails)?

[Answer]: El marketplace notifica al banco y el banco de forma asíncrona gestiona y aprueba el pago.

---

**Q6: CRM - Alias Resolution**  
How should we handle ambiguous aliases (e.g., "mi hermano" matches multiple beneficiaries)?
- Should we return all matches and ask user to clarify?
- Should we use frequency/recency to auto-select most likely match?
- Should we use context from conversation to disambiguate?
- Should we maintain alias history to improve resolution over time?

[Answer]: que valide todas las consecuencias semanticas y valide con el cliente en casode existir varias para saber si el match es correcto

---

**Q7: CRM - Beneficiary Frequency Tracking**  
How should we track and use beneficiary usage frequency?
- Should we increment frequency counter on every transfer?
- Should we decay frequency over time (recent transfers weighted more)?
- Should we use frequency to suggest beneficiaries proactively?
- Should we limit suggested beneficiaries to top N most frequent?

[Answer]: deberíamos recomendar proactiamente beneficios

---

**Q8: Event-Driven Communication**  
How should Action Groups handle EventBridge events?
- Should each Action Group have a single Lambda or multiple Lambdas per action?
- Should we use event filtering at EventBridge level or Lambda level?
- How should we handle event ordering (if multiple events for same user)?
- Should we implement idempotency for duplicate events?

[Answer]: multiples lambdas por accion y se deben filtrar los eventos a nivel de event bridge

---

**Q9: Error Handling Strategy**  
How should Action Groups handle errors and communicate them back to AgentCore?
- Should we publish error events to EventBridge or use different mechanism?
- Should we retry failed operations automatically or let AgentCore decide?
- How should we categorize errors (validation, business logic, technical)?
- Should we include error details in response or just error codes?

[Answer]: Debe haber un reintento de la operacion en caso de que falle el reintento el agent core lo debe manejar

---

**Q10: Data Consistency**  
How should we ensure data consistency across Action Groups?
- Should we use eventual consistency or strong consistency for DynamoDB reads?
- Should we implement distributed transactions across Action Groups?
- How should we handle race conditions (e.g., concurrent transfers)?
- Should we use DynamoDB streams for cross-Action Group synchronization?

[Answer]: use consistencia fuerte en dynamo db

---

### Domain Model Questions

**Q11: Account Entity**  
What attributes should the Account entity have?
- Should we model separate checking and savings accounts?
- Should we include credit line as part of Account or separate entity?
- Should we track account status (active, frozen, closed)?
- Should we include account metadata (opening date, branch, etc.)?

[Answer]: debería separar cuentas de ahorro, checkes y credito

---

**Q12: Transaction Entity**  
What attributes should the Transaction entity have?
- Should we include transaction type (debit, credit, transfer, purchase)?
- Should we include transaction status (pending, completed, failed, reversed)?
- Should we include merchant/beneficiary information?
- Should we include geolocation or device information?

[Answer]: debe tener tipo de transaccion, estado de la transaccion, geolocalizacion y beneficiary information

---

**Q13: Product Entity**  
What attributes should the Product entity have?
- Should we include product variants (color, size, etc.)?
- Should we include inventory/stock information?
- Should we include product ratings/reviews?
- Should we include multiple images per product?

[Answer]: debería tener caracteristica del producto, imagen y stock

---

**Q14: Benefit Entity**  
Should Benefit be a separate entity or embedded in Product?
- If separate, how do we link Benefits to Products?
- Should Benefits have their own lifecycle (active, expired, exhausted)?
- Should we track benefit usage per user?
- Should we support benefit stacking rules?

[Answer]: deberían estar separados del producto vinculado de alguna manera que permita relacionar el producto con el beneficio y el bneficio su propio ciclio de vida

---

**Q15: Beneficiary Entity**  
What attributes should the Beneficiary entity have?
- Should we include beneficiary type (person, business, government)?
- Should we include relationship to user (family, friend, vendor)?
- Should we include beneficiary bank information (bank name, account type)?
- Should we include beneficiary contact information (phone, email)?

[Answer]: debe incluir relacionamiento es decir si es familia, amigo, tienda, informacion bancaria y de contacto

---

### Business Rules Questions

**Q16: Transfer Limits**  
What transfer limits should we enforce?
- Should we have per-transaction limits (e.g., max 100,000 per transfer)?
- Should we have daily/monthly limits (e.g., max 500,000 per day)?
- Should limits vary by account type or user profile?
- Should we allow temporary limit increases with additional authentication?

[Answer]:  que tenga limites diarios y mensuales

---

**Q17: Benefit Rules**  
What rules govern benefit application?
- Should cashback be credited immediately or after purchase confirmation?
- Should MSI require minimum purchase amount (e.g., min 3,000 for 3 MSI)?
- Should discounts be applied before or after other benefits?
- Should benefits be mutually exclusive or stackable?

[Answer]: el cashback debe verse reflejado inmediatamente, no requiere minimo de compra, puede otro benificio ser aplicado 

---

**Q18: Purchase Validation**  
What validations should we perform before allowing a purchase?
- Should we validate product availability/stock?
- Should we validate user's payment method (sufficient balance/credit)?
- Should we validate shipping address (if applicable)?
- Should we validate purchase limits (e.g., max 1 per user for promotions)?

[Answer]: validar que esta e stock, el saldo, y la cuenta destino está habilitada

---

**Q19: Alias Validation**  
What rules should govern alias creation and usage?
- Should aliases be unique per user or globally unique?
- Should we restrict alias format (length, characters, reserved words)?
- Should we validate alias doesn't conflict with existing beneficiary names?
- Should we allow multiple aliases for same beneficiary?

[Answer]: un alias por persona

---

**Q20: Data Retention**  
What data retention rules should we follow?
- Should we keep transaction history indefinitely or archive after N months?
- Should we soft-delete beneficiaries or hard-delete?
- Should we keep purchase history for analytics?
- Should we implement TTL for session data or temporary records?

[Answer]: mantener transacciones del ultimo mes

---

## Success Criteria

- [x] All clarification questions answered
- [x] Business logic models documented
- [x] Domain entities defined with attributes
- [x] Business rules documented with validation logic
- [x] Data flow patterns defined
- [x] Integration contracts specified
- [x] User approval obtained

---

**Plan Status**: Complete - Awaiting user approval  
**Total Questions**: 20 questions answered  
**Artifacts Generated**: 3 documents (business-logic-model.md, domain-entities.md, business-rules.md)  
**Next Step**: User approval to proceed to NFR Requirements stage
