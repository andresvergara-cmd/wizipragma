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

[Answer]:

---

**Question 2: Marketplace Operation Latency**

What is the acceptable latency for Marketplace operations (catalog, purchase)?

A) Fast: < 1 second (challenging for purchase flow)  
B) Standard: < 2 seconds (balanced, realistic)  
C) Relaxed: < 3 seconds (safe for demo)  
D) Custom: Specify your target

[Answer]:

---

**Question 3: CRM Alias Resolution Latency**

What is the acceptable latency for alias resolution (semantic matching)?

A) Fast: < 500ms (requires efficient matching algorithm)  
B) Standard: < 1 second (balanced)  
C) Relaxed: < 2 seconds (safe for complex matching)  
D) Custom: Specify your target

[Answer]:

---

**Question 4: DynamoDB Query Performance**

What query performance target should we aim for?

A) Fast: < 50ms (requires optimized indexes)  
B) Standard: < 100ms (balanced)  
C) Relaxed: < 200ms (safe for demo)  
D) Custom: Specify your target

[Answer]:

---

### Scalability Questions

**Question 5: Expected Concurrent Operations**

How many concurrent Action Group operations should the system support?

A) Small: 1-10 concurrent operations (single demo user)  
B) Medium: 10-50 concurrent operations (multiple demo users)  
C) Large: 50-100 concurrent operations (stress testing)  
D) Custom: Specify your target

[Answer]:

---

**Question 6: Lambda Concurrency Strategy**

What Lambda concurrency strategy should we use for Action Groups?

A) No reserved concurrency (use account default)  
B) Reserved concurrency per Lambda (guarantee capacity)  
C) Provisioned concurrency (pre-warmed, lowest latency)  
D) Custom: Specify your strategy

[Answer]:

---

**Question 7: DynamoDB Capacity Mode**

What DynamoDB capacity mode should we use for Action Group tables?

A) On-demand (pay per request, auto-scaling, recommended for demo)  
B) Provisioned (fixed capacity, lower cost for predictable load)  
C) Custom: Specify your preference

[Answer]:

---

**Question 8: EventBridge Throughput**

What EventBridge event throughput should we plan for?

A) Low: < 10 events/second (single user demo)  
B) Medium: 10-50 events/second (multiple users)  
C) High: 50-100 events/second (stress testing)  
D) Custom: Specify your target

[Answer]:

---

### Availability Questions

**Question 9: Demo Uptime Target**

What uptime target is acceptable for the hackathon demo?

A) High: 99.9% (production-like, requires robust error handling)  
B) Standard: 95% (balanced, some failures acceptable)  
C) Demo: 90% (focus on happy path, minimal error handling)  
D) Custom: Specify your target

[Answer]:

---

**Question 10: DynamoDB Failure Fallback**

What should happen if DynamoDB operations fail during demo?

A) Fail fast: Return error immediately  
B) Retry: Attempt retry with exponential backoff  
C) Cache: Use in-memory cache as fallback  
D) Queue: Queue for later processing

[Answer]:

---

### Data Consistency Questions

**Question 11: Read Consistency Model**

What read consistency model should we use for DynamoDB?

A) Strong consistency (always latest data, higher latency)  
B) Eventual consistency (faster, may read stale data)  
C) Hybrid: Strong for critical reads, eventual for others  
D) Custom: Specify your preference

[Answer]:

---

**Question 12: Optimistic Locking Retry Strategy**

How should we handle optimistic locking conflicts (version mismatches)?

A) No retries: Fail immediately on conflict  
B) Simple retries: Retry up to 3 times with fixed delay  
C) Exponential backoff: Retry with increasing delays  
D) Custom: Specify your strategy

[Answer]:

---

**Question 13: Cross-Action Group Consistency**

How should we handle consistency across Action Groups (e.g., Marketplace → Core Banking)?

A) Strict: Implement distributed transactions (complex)  
B) Eventual: Use event-driven eventual consistency (recommended)  
C) Compensating: Use saga pattern with compensation logic  
D) Custom: Specify your approach

[Answer]:

---

### Security Questions

**Question 14: Event Authentication**

How should we authenticate EventBridge events between Action Groups?

A) No authentication: Trust internal events (fast, less secure)  
B) Event signature: Sign events with HMAC (balanced)  
C) IAM roles: Use IAM role-based access control (most secure)  
D) Custom: Specify your approach

[Answer]:

---

**Question 15: Financial Data Encryption**

How should we encrypt sensitive financial data (balances, transactions)?

A) Full encryption: Encrypt all fields at rest and in transit  
B) Selective encryption: Encrypt sensitive fields only (balance, account numbers)  
C) Default encryption: Use DynamoDB default encryption  
D) Custom: Specify your requirements

[Answer]:

---

**Question 16: PII Protection in Logs**

How should we handle PII (account numbers, names) in CloudWatch logs?

A) Strict: Mask all PII in logs, no exceptions  
B) Standard: Mask sensitive fields (account numbers, balances)  
C) Minimal: Log everything for debugging (demo only)  
D) Custom: Specify your approach

[Answer]:

---

### Tech Stack Questions

**Question 17: Python Runtime Version**

Which Python runtime should we use for Action Group Lambdas?

A) Python 3.9 (stable, widely supported)  
B) Python 3.10 (newer features, good support)  
C) Python 3.11 (latest, best performance, recommended)  
D) Python 3.12 (cutting edge, may have compatibility issues)

[Answer]:

---

**Question 18: DynamoDB Table Design**

What DynamoDB table design should we use?

A) Single table design (all entities in one table, complex)  
B) Multiple tables (one per entity type, simpler, recommended for demo)  
C) Hybrid: Group related entities (e.g., accounts + transactions)  
D) Custom: Specify your design

[Answer]:

---

**Question 19: Lambda Architecture**

How many Lambda functions should we create per Action Group?

A) Single Lambda per Action Group (3 Lambdas total, simpler)  
B) Multiple Lambdas per action (9 Lambdas total, better separation, recommended)  
C) Monolithic: Single Lambda for all Action Groups (not recommended)  
D) Custom: Specify your architecture

[Answer]:

---

**Question 20: EventBridge Event Schema**

What event schema format should we use?

A) JSON with strict schema validation (robust, more overhead)  
B) JSON with loose validation (flexible, faster to implement, recommended)  
C) Avro/Protobuf (efficient, more complex)  
D) Custom: Specify your format

[Answer]:

---

### Reliability Questions

**Question 21: Retry Strategy for Failed Operations**

What retry strategy should we use for failed Action Group operations?

A) No retries: Fail fast, let AgentCore handle  
B) Simple retries: Retry up to 3 times with fixed delay (recommended)  
C) Exponential backoff: Retry with increasing delays  
D) Custom: Specify your strategy

[Answer]:

---

**Question 22: Idempotency Implementation**

How should we implement idempotency for duplicate events?

A) Request ID tracking: Store request_id in DynamoDB (recommended)  
B) Event deduplication: Use EventBridge deduplication  
C) No idempotency: Accept duplicate processing (not recommended)  
D) Custom: Specify your approach

[Answer]:

---

**Question 23: Lambda Timeout Values**

What timeout values should we use for Action Group Lambdas?

A) Short: 5 seconds (fail fast)  
B) Standard: 10 seconds (balanced, recommended)  
C) Long: 30 seconds (accommodate slow operations)  
D) Custom: Specify your timeouts

[Answer]:

---

**Question 24: Error Logging Strategy**

What error logging and tracking strategy should we use?

A) Comprehensive: CloudWatch Logs + X-Ray tracing + custom metrics  
B) Standard: CloudWatch Logs + basic metrics (recommended)  
C) Minimal: CloudWatch Logs only  
D) Custom: Specify your strategy

[Answer]:

---

**Question 25: Compensation Logic for Failed Transactions**

How should we handle compensation when transactions fail (e.g., payment fails after purchase)?

A) Automatic: Implement automatic compensation logic (recommended)  
B) Manual: Log failures for manual intervention  
C) No compensation: Accept inconsistencies (not recommended)  
D) Custom: Specify your approach

[Answer]:

---

## Success Criteria

- [ ] All performance targets defined
- [ ] All scalability requirements specified
- [ ] All availability requirements determined
- [ ] All data consistency requirements identified
- [ ] All security requirements identified
- [ ] All tech stack decisions made with rationale
- [ ] All reliability requirements documented
- [ ] All questions answered by user
- [ ] No ambiguities remaining

---

**Plan Status**: Awaiting user answers  
**Total Questions**: 25 questions across 7 categories  
**Next Step**: Collect answers and generate NFR requirements artifacts

