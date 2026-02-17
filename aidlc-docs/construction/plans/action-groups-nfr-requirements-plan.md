# NFR Requirements Plan - Unit 3: Action Groups

## Context

**Unit Name**: Action Groups (Backend Services)  
**Purpose**: Mock banking, marketplace, and CRM services via EventBridge-triggered Lambdas  
**Timeline**: 8-hour hackathon (demo quality, not production)  
**Functional Design**: Complete (12 workflows, 19 business rules, 13 entities)  
**Dependencies**: Unit 1 (EventBridge, DynamoDB), Unit 2 (AgentCore events)

---

## NFR Assessment Steps

### Step 1: Performance Requirements
- [ ] Define response time targets for Action Group operations
- [ ] Define latency targets for Core Banking operations (balance, transfer)
- [ ] Define latency targets for Marketplace operations (catalog, purchase)
- [ ] Define latency targets for CRM operations (alias resolution)
- [ ] Define DynamoDB query performance targets
- [ ] Define EventBridge event delivery latency

### Step 2: Scalability Requirements
- [ ] Define expected concurrent Action Group invocations
- [ ] Define expected events per second throughput
- [ ] Define Lambda concurrency limits per Action Group
- [ ] Define DynamoDB capacity mode and throughput
- [ ] Define scaling strategy for high load

### Step 3: Availability Requirements
- [ ] Define uptime target for demo (hackathon context)
- [ ] Define error handling strategy (retry vs fail)
- [ ] Define fallback mechanisms for DynamoDB failures
- [ ] Define monitoring and alerting needs

### Step 4: Data Consistency Requirements
- [ ] Define consistency model (strong vs eventual)
- [ ] Define optimistic locking retry strategy
- [ ] Define transaction isolation requirements
- [ ] Define data synchronization strategy across Action Groups

### Step 5: Security Requirements
- [ ] Define event authentication mechanism
- [ ] Define data encryption requirements (DynamoDB)
- [ ] Define PII protection strategy for financial data
- [ ] Define access control for Action Group Lambdas

### Step 6: Tech Stack Decisions
- [ ] Confirm Python runtime version for Lambdas
- [ ] Confirm DynamoDB table design (single vs multiple tables)
- [ ] Confirm EventBridge event schema format
- [ ] Confirm Lambda architecture (single vs multiple per action)
- [ ] Confirm error handling library/framework

### Step 7: Reliability Requirements
- [ ] Define retry strategy for failed operations
- [ ] Define idempotency implementation approach
- [ ] Define timeout values for Lambda functions
- [ ] Define error logging and tracking strategy
- [ ] Define compensation logic for failed transactions

---

## NFR Questions

### Performance Questions

**Question 1: Core Banking Operation Latency**

What is the acceptable latency for Core Banking operations (balance query, transfer)?

A) Fast: < 500ms (aggressive, requires optimization)  
B) Standard: < 1 second (balanced, achievable)  
C) Relaxed: < 2 seconds (safe for demo)  
D) Custom: Specify your target

[Answer]: B - Standard: < 1 second. Para un demo de hackathon, 1 segundo es un balance perfecto entre performance percibida y complejidad de implementación.

---

**Question 2: Marketplace Operation Latency**

What is the acceptable latency for Marketplace operations (catalog, purchase)?

A) Fast: < 1 second (challenging for purchase flow)  
B) Standard: < 2 seconds (balanced, realistic)  
C) Relaxed: < 3 seconds (safe for demo)  
D) Custom: Specify your target

[Answer]: B - Standard: < 2 seconds. El flujo de compra involucra múltiples Action Groups (Marketplace → Core Banking), 2 segundos es realista.

---

**Question 3: CRM Alias Resolution Latency**

What is the acceptable latency for alias resolution (semantic matching)?

A) Fast: < 500ms (requires efficient matching algorithm)  
B) Standard: < 1 second (balanced)  
C) Relaxed: < 2 seconds (safe for complex matching)  
D) Custom: Specify your target

[Answer]: B - Standard: < 1 second. La resolución de alias es crítica para UX, pero con matching simple (lowercase, fuzzy) 1 segundo es suficiente.

---

**Question 4: DynamoDB Query Performance**

What query performance target should we aim for?

A) Fast: < 50ms (requires optimized indexes)  
B) Standard: < 100ms (balanced)  
C) Relaxed: < 200ms (safe for demo)  
D) Custom: Specify your target

[Answer]: B - Standard: < 100ms. Con índices GSI bien diseñados y queries simples, 100ms es alcanzable sin sobre-optimización.

---

### Scalability Questions

**Question 5: Expected Concurrent Operations**

How many concurrent Action Group operations should the system support?

A) Small: 1-10 concurrent operations (single demo user)  
B) Medium: 10-50 concurrent operations (multiple demo users)  
C) Large: 50-100 concurrent operations (stress testing)  
D) Custom: Specify your target

[Answer]: A - Small: 1-10 concurrent operations. Es un demo de hackathon con 1-2 usuarios simultáneos máximo. Optimizar para más sería over-engineering.

---

**Question 6: Lambda Concurrency Strategy**

What Lambda concurrency strategy should we use for Action Groups?

A) No reserved concurrency (use account default)  
B) Reserved concurrency per Lambda (guarantee capacity)  
C) Provisioned concurrency (pre-warmed, lowest latency)  
D) Custom: Specify your strategy

[Answer]: A - No reserved concurrency. Para un demo con bajo volumen, el default de AWS es suficiente. Evitamos complejidad y costos innecesarios.

---

**Question 7: DynamoDB Capacity Mode**

What DynamoDB capacity mode should we use for Action Group tables?

A) On-demand (pay per request, auto-scaling, recommended for demo)  
B) Provisioned (fixed capacity, lower cost for predictable load)  
C) Custom: Specify your preference

[Answer]: A - On-demand. Perfecto para hackathon: cero configuración de capacity, auto-scaling automático, y costos mínimos con bajo volumen.

---

**Question 8: EventBridge Throughput**

What EventBridge event throughput should we plan for?

A) Low: < 10 events/second (single user demo)  
B) Medium: 10-50 events/second (multiple users)  
C) High: 50-100 events/second (stress testing)  
D) Custom: Specify your target

[Answer]: A - Low: < 10 events/second. Demo con 1-2 usuarios, cada operación genera 1-3 eventos. 10 eventos/seg es más que suficiente.

---

### Availability Questions

**Question 9: Demo Uptime Target**

What uptime target is acceptable for the hackathon demo?

A) High: 99.9% (production-like, requires robust error handling)  
B) Standard: 95% (balanced, some failures acceptable)  
C) Demo: 90% (focus on happy path, minimal error handling)  
D) Custom: Specify your target

[Answer]: C - Demo: 90%. Enfoque en happy path para el demo. Error handling básico es suficiente, priorizamos velocidad de desarrollo.

---

**Question 10: DynamoDB Failure Fallback**

What should happen if DynamoDB operations fail during demo?

A) Fail fast: Return error immediately  
B) Retry: Attempt retry with exponential backoff  
C) Cache: Use in-memory cache as fallback  
D) Queue: Queue for later processing

[Answer]: B - Retry. Retry simple (3 intentos con backoff) maneja transient failures sin complejidad de cache o queues. Balance perfecto para demo.

---

### Data Consistency Questions

**Question 11: Read Consistency Model**

What read consistency model should we use for DynamoDB?

A) Strong consistency (always latest data, higher latency)  
B) Eventual consistency (faster, may read stale data)  
C) Hybrid: Strong for critical reads, eventual for others  
D) Custom: Specify your preference

[Answer]: C - Hybrid. Strong consistency para balance/transactions (crítico), eventual para catálogo/beneficiarios (no crítico). Optimiza latency sin sacrificar correctness.

---

**Question 12: Optimistic Locking Retry Strategy**

How should we handle optimistic locking conflicts (version mismatches)?

A) No retries: Fail immediately on conflict  
B) Simple retries: Retry up to 3 times with fixed delay  
C) Exponential backoff: Retry with increasing delays  
D) Custom: Specify your strategy

[Answer]: B - Simple retries. Con bajo volumen de concurrencia (1-10 ops), conflictos serán raros. 3 retries con delay fijo es suficiente y simple.

---

**Question 13: Cross-Action Group Consistency**

How should we handle consistency across Action Groups (e.g., Marketplace → Core Banking)?

A) Strict: Implement distributed transactions (complex)  
B) Eventual: Use event-driven eventual consistency (recommended)  
C) Compensating: Use saga pattern with compensation logic  
D) Custom: Specify your approach

[Answer]: B - Eventual consistency. EventBridge ya provee el modelo event-driven. Para demo, eventual consistency es suficiente y evita complejidad de sagas/transactions.

---

### Security Questions

**Question 14: Event Authentication**

How should we authenticate EventBridge events between Action Groups?

A) No authentication: Trust internal events (fast, less secure)  
B) Event signature: Sign events with HMAC (balanced)  
C) IAM roles: Use IAM role-based access control (most secure)  
D) Custom: Specify your approach

[Answer]: C - IAM roles. AWS ya provee IAM integration con EventBridge. Es seguro, sin overhead de implementación, y es best practice de AWS.

---

**Question 15: Financial Data Encryption**

How should we encrypt sensitive financial data (balances, transactions)?

A) Full encryption: Encrypt all fields at rest and in transit  
B) Selective encryption: Encrypt sensitive fields only (balance, account numbers)  
C) Default encryption: Use DynamoDB default encryption  
D) Custom: Specify your requirements

[Answer]: C - Default encryption. DynamoDB encryption at rest está habilitado por default. Para demo, es suficiente. TLS in-transit ya está incluido en AWS SDK.

---

**Question 16: PII Protection in Logs**

How should we handle PII (account numbers, names) in CloudWatch logs?

A) Strict: Mask all PII in logs, no exceptions  
B) Standard: Mask sensitive fields (account numbers, balances)  
C) Minimal: Log everything for debugging (demo only)  
D) Custom: Specify your approach

[Answer]: B - Standard. Maskear account numbers y balances en logs. Nombres/alias pueden quedar para debugging. Balance entre seguridad y debuggability.

---

### Tech Stack Questions

**Question 17: Python Runtime Version**

Which Python runtime should we use for Action Group Lambdas?

A) Python 3.9 (stable, widely supported)  
B) Python 3.10 (newer features, good support)  
C) Python 3.11 (latest, best performance, recommended)  
D) Python 3.12 (cutting edge, may have compatibility issues)

[Answer]: C - Python 3.11. Mejor performance que 3.9/3.10, excelente soporte en AWS Lambda, y compatible con boto3. Consistente con Unit 2.

---

**Question 18: DynamoDB Table Design**

What DynamoDB table design should we use?

A) Single table design (all entities in one table, complex)  
B) Multiple tables (one per entity type, simpler, recommended for demo)  
C) Hybrid: Group related entities (e.g., accounts + transactions)  
D) Custom: Specify your design

[Answer]: B - Multiple tables. Una tabla por entity type (Accounts, Transactions, Products, Beneficiaries, Purchases, Retailers). Simple, claro, fácil de debuggear en hackathon.

---

**Question 19: Lambda Architecture**

How many Lambda functions should we create per Action Group?

A) Single Lambda per Action Group (3 Lambdas total, simpler)  
B) Multiple Lambdas per action (9 Lambdas total, better separation, recommended)  
C) Monolithic: Single Lambda for all Action Groups (not recommended)  
D) Custom: Specify your architecture

[Answer]: B - Multiple Lambdas per action (9 total). Mejor separation of concerns, más fácil de debuggear, y permite scaling independiente. Vale la pena la complejidad adicional.

---

**Question 20: EventBridge Event Schema**

What event schema format should we use?

A) JSON with strict schema validation (robust, more overhead)  
B) JSON with loose validation (flexible, faster to implement, recommended)  
C) Avro/Protobuf (efficient, more complex)  
D) Custom: Specify your format

[Answer]: B - JSON con loose validation. Rápido de implementar, fácil de debuggear, flexible para cambios durante hackathon. Schema validation estricta es overkill para demo.

---

### Reliability Questions

**Question 21: Retry Strategy for Failed Operations**

What retry strategy should we use for failed Action Group operations?

A) No retries: Fail fast, let AgentCore handle  
B) Simple retries: Retry up to 3 times with fixed delay (recommended)  
C) Exponential backoff: Retry with increasing delays  
D) Custom: Specify your strategy

[Answer]: B - Simple retries (3 intentos, 100ms delay). Maneja transient failures sin complejidad de exponential backoff. Suficiente para demo con bajo volumen.

---

**Question 22: Idempotency Implementation**

How should we implement idempotency for duplicate events?

A) Request ID tracking: Store request_id in DynamoDB (recommended)  
B) Event deduplication: Use EventBridge deduplication  
C) No idempotency: Accept duplicate processing (not recommended)  
D) Custom: Specify your approach

[Answer]: A - Request ID tracking en DynamoDB. Simple de implementar (check-then-write pattern), confiable, y nos da control total sobre idempotency window.

---

**Question 23: Lambda Timeout Values**

What timeout values should we use for Action Group Lambdas?

A) Short: 5 seconds (fail fast)  
B) Standard: 10 seconds (balanced, recommended)  
C) Long: 30 seconds (accommodate slow operations)  
D) Custom: Specify your timeouts

[Answer]: B - Standard: 10 seconds. Suficiente para DynamoDB ops + EventBridge publish + retries. Evita timeouts innecesarios sin desperdiciar recursos.

---

**Question 24: Error Logging Strategy**

What error logging and tracking strategy should we use?

A) Comprehensive: CloudWatch Logs + X-Ray tracing + custom metrics  
B) Standard: CloudWatch Logs + basic metrics (recommended)  
C) Minimal: CloudWatch Logs only  
D) Custom: Specify your strategy

[Answer]: B - Standard: CloudWatch Logs + basic metrics. Logs estructurados con correlation_id, métricas básicas (errors, latency). X-Ray es overkill para demo.

---

**Question 25: Compensation Logic for Failed Transactions**

How should we handle compensation when transactions fail (e.g., payment fails after purchase)?

A) Automatic: Implement automatic compensation logic (recommended)  
B) Manual: Log failures for manual intervention  
C) No compensation: Accept inconsistencies (not recommended)  
D) Custom: Specify your approach

[Answer]: A - Automatic compensation. Implementar rollback automático para purchase flow (revert inventory, refund payment). Crítico para demo creíble, no tan complejo con eventos.

---

## Success Criteria

- [x] All performance targets defined
- [x] All scalability requirements specified
- [x] All availability requirements determined
- [x] All data consistency requirements identified
- [x] All security requirements identified
- [x] All tech stack decisions made with rationale
- [x] All reliability requirements documented
- [x] All questions answered by user
- [x] No ambiguities remaining

---

**Plan Status**: Complete - All questions answered, artifacts generated  
**Total Questions**: 25 questions across 7 categories  
**Artifacts Generated**:
- `aidlc-docs/construction/action-groups/nfr-requirements/nfr-requirements.md`
- `aidlc-docs/construction/action-groups/nfr-requirements/tech-stack-decisions.md`

**Next Step**: User approval to proceed to NFR Design stage

