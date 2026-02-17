# NFR Requirements - Unit 3: Action Groups

## Document Information
- **Unit**: Unit 3 (Action Groups - Backend Services)
- **Stage**: NFR Requirements
- **Created**: 2026-02-17
- **Context**: 8-hour hackathon, demo quality focus

---

## 1. Performance Requirements

### 1.1 Response Time Targets

**Core Banking Operations**
- **Target**: < 1 second end-to-end
- **Rationale**: Balance between perceived performance and implementation complexity
- **Measurement**: From EventBridge event receipt to response event published
- **Operations**: Balance query, transfer execution, transaction history

**Marketplace Operations**
- **Target**: < 2 seconds end-to-end
- **Rationale**: Purchase flow involves multiple Action Groups (Marketplace → Core Banking)
- **Measurement**: From catalog request to purchase confirmation
- **Operations**: Product catalog, benefit calculation, purchase execution

**CRM Operations**
- **Target**: < 1 second end-to-end
- **Rationale**: Alias resolution is critical for UX, simple matching algorithm achievable
- **Measurement**: From alias query to beneficiary resolution
- **Operations**: Alias resolution, beneficiary lookup

### 1.2 Component Latency Targets

**DynamoDB Query Performance**
- **Target**: < 100ms per query
- **Rationale**: Well-designed GSI indexes with simple queries
- **Strategy**: Use partition key + sort key patterns, avoid scans

**EventBridge Event Delivery**
- **Target**: < 50ms (AWS managed, no control)
- **Note**: EventBridge provides sub-second delivery in same region

### 1.3 Performance Monitoring

**Metrics to Track**:
- Lambda execution duration (p50, p95, p99)
- DynamoDB query latency
- End-to-end operation latency
- Cold start frequency and duration

---

## 2. Scalability Requirements

### 2.1 Throughput Targets

**Concurrent Operations**
- **Target**: 1-10 concurrent operations
- **Rationale**: Single demo user, hackathon context
- **Peak Load**: 10 operations during demo scenarios

**EventBridge Throughput**
- **Target**: < 10 events/second
- **Rationale**: 1-2 users, each operation generates 1-3 events
- **Peak**: 10 events/second during rapid interactions

### 2.2 Lambda Concurrency

**Strategy**: No reserved concurrency
- **Rationale**: Low volume, AWS default limits sufficient
- **Account Default**: 1000 concurrent executions (shared)
- **Expected Usage**: < 10 concurrent Lambda invocations

### 2.3 DynamoDB Capacity

**Capacity Mode**: On-demand
- **Rationale**: Zero configuration, auto-scaling, minimal cost for low volume
- **Read/Write Units**: Auto-scaled by AWS
- **Cost**: Pay-per-request, ~$0.25 per million reads

### 2.4 Scaling Strategy

**Horizontal Scaling**: Automatic via Lambda
- Lambda scales automatically to handle concurrent requests
- No manual intervention required

**Vertical Scaling**: Not applicable
- Lambda memory fixed at 512MB (sufficient for demo)

---

## 3. Availability Requirements

### 3.1 Uptime Target

**Target**: 90% uptime (demo quality)
- **Rationale**: Focus on happy path, minimal error handling
- **Acceptable Downtime**: 10% (48 minutes in 8-hour hackathon)
- **Priority**: Speed of development over robustness

### 3.2 Error Handling Strategy

**DynamoDB Failures**
- **Strategy**: Retry with exponential backoff
- **Retries**: Up to 3 attempts
- **Backoff**: 100ms, 200ms, 400ms
- **Fallback**: Return error to AgentCore after retries exhausted

**Lambda Failures**
- **Strategy**: EventBridge automatic retry
- **Retries**: EventBridge retries failed Lambda invocations
- **Dead Letter Queue**: Not implemented (demo context)

### 3.3 Monitoring and Alerting

**Monitoring**: CloudWatch Logs + basic metrics
- Lambda execution errors
- DynamoDB throttling
- EventBridge delivery failures

**Alerting**: Not implemented (demo context)
- Manual monitoring during demo
- CloudWatch Logs Insights for debugging

---

## 4. Data Consistency Requirements

### 4.1 Read Consistency Model

**Strategy**: Hybrid consistency
- **Strong Consistency**: Balance queries, transaction history (critical data)
- **Eventual Consistency**: Product catalog, beneficiary list (non-critical)
- **Rationale**: Optimize latency without sacrificing correctness

### 4.2 Write Consistency

**Optimistic Locking**
- **Strategy**: Version attribute on entities
- **Conflict Resolution**: Retry up to 3 times with fixed delay (100ms)
- **Rationale**: Low concurrency, conflicts rare

### 4.3 Cross-Action Group Consistency

**Strategy**: Eventual consistency via EventBridge
- **Pattern**: Event-driven, asynchronous communication
- **Example**: Purchase → Inventory Update → Payment → Confirmation
- **Rationale**: Simplicity, leverages existing EventBridge infrastructure
- **Trade-off**: Temporary inconsistencies acceptable for demo

### 4.4 Transaction Isolation

**Level**: Read Committed (DynamoDB default)
- **Rationale**: Sufficient for demo, no complex transactions
- **Note**: DynamoDB doesn't support ACID transactions across tables

---

## 5. Security Requirements

### 5.1 Authentication and Authorization

**Event Authentication**
- **Strategy**: IAM role-based access control
- **Implementation**: EventBridge rules invoke Lambdas via IAM roles
- **Rationale**: AWS native, no custom implementation needed

**Lambda Execution Role**
- **Permissions**: DynamoDB read/write, EventBridge publish, CloudWatch Logs
- **Principle**: Least privilege per Lambda function

### 5.2 Data Encryption

**Encryption at Rest**
- **Strategy**: DynamoDB default encryption (AWS managed keys)
- **Rationale**: Enabled by default, no configuration needed
- **Coverage**: All DynamoDB tables

**Encryption in Transit**
- **Strategy**: TLS 1.2+ (AWS SDK default)
- **Coverage**: All AWS service communication

### 5.3 PII Protection

**Logging Strategy**
- **Mask**: Account numbers, balances in CloudWatch Logs
- **Allow**: User names, aliases (for debugging)
- **Implementation**: Custom logging utility function

**Data Retention**
- **CloudWatch Logs**: 7 days retention (demo context)
- **DynamoDB**: No automatic deletion (manual cleanup post-demo)

---

## 6. Tech Stack Decisions

### 6.1 Runtime and Language

**Python Runtime**: Python 3.11
- **Rationale**: Best performance, excellent AWS Lambda support, consistent with Unit 2
- **Libraries**: boto3 (AWS SDK), standard library only

### 6.2 Database Design

**DynamoDB Table Design**: Multiple tables (one per entity type)
- **Tables**: Accounts, Transactions, Products, Beneficiaries, Purchases, Retailers
- **Rationale**: Simple, clear, easy to debug in hackathon
- **Trade-off**: More tables, but simpler access patterns

**Table Structure**:
```
centli-accounts
  PK: user_id
  SK: account_id
  
centli-transactions
  PK: account_id
  SK: timestamp#transaction_id
  GSI: user_id (for user transaction history)
  
centli-products
  PK: product_id
  SK: retailer_id
  
centli-beneficiaries
  PK: user_id
  SK: beneficiary_id
  GSI: alias (for alias resolution)
  
centli-purchases
  PK: user_id
  SK: timestamp#purchase_id
  
centli-retailers
  PK: retailer_id
```

### 6.3 Lambda Architecture

**Strategy**: Multiple Lambdas per action (9 Lambdas total)
- **Core Banking**: 3 Lambdas (balance, transfer, transactions)
- **Marketplace**: 3 Lambdas (catalog, benefits, purchase)
- **CRM**: 3 Lambdas (resolve-alias, get-beneficiaries, add-beneficiary)

**Rationale**: Better separation of concerns, easier debugging, independent scaling

### 6.4 Event Schema

**Format**: JSON with loose validation
- **Rationale**: Fast to implement, easy to debug, flexible for changes
- **Structure**:
```json
{
  "event_type": "TRANSFER_REQUEST",
  "correlation_id": "uuid",
  "timestamp": "ISO8601",
  "user_id": "string",
  "data": {
    // Event-specific payload
  }
}
```

---

## 7. Reliability Requirements

### 7.1 Retry Strategy

**Failed Operations**
- **Strategy**: Simple retries (3 attempts, 100ms fixed delay)
- **Rationale**: Handles transient failures, sufficient for low volume
- **Scope**: DynamoDB operations, EventBridge publish

### 7.2 Idempotency

**Implementation**: Request ID tracking in DynamoDB
- **Pattern**: Check-then-write (query by request_id before processing)
- **Storage**: Separate idempotency table or attribute on entity
- **Window**: 24 hours (demo context)

**Example**:
```python
def is_duplicate(request_id):
    response = table.get_item(Key={'request_id': request_id})
    return 'Item' in response
```

### 7.3 Timeout Configuration

**Lambda Timeout**: 10 seconds
- **Rationale**: Sufficient for DynamoDB ops + EventBridge publish + retries
- **Breakdown**: 5s for business logic, 3s for retries, 2s buffer

### 7.4 Error Logging

**Strategy**: CloudWatch Logs + basic metrics
- **Log Format**: Structured JSON with correlation_id
- **Metrics**: Error count, latency (p50, p95, p99)
- **Correlation**: correlation_id propagated across all events

**Log Example**:
```json
{
  "timestamp": "2026-02-17T10:30:00Z",
  "level": "ERROR",
  "correlation_id": "abc-123",
  "lambda": "core-banking-transfer",
  "error": "InsufficientFunds",
  "details": {"account_id": "***", "amount": 5000}
}
```

### 7.5 Compensation Logic

**Strategy**: Automatic compensation for failed transactions
- **Scope**: Purchase flow (inventory, payment, confirmation)
- **Implementation**: Compensation events via EventBridge

**Purchase Flow Compensation**:
1. Purchase initiated → Inventory reserved
2. Payment fails → Publish COMPENSATION_REQUIRED event
3. Marketplace listens → Releases inventory
4. User notified → Purchase failed

**Example Events**:
```json
// Success path
PURCHASE_INITIATED → INVENTORY_RESERVED → PAYMENT_COMPLETED → PURCHASE_CONFIRMED

// Failure path with compensation
PURCHASE_INITIATED → INVENTORY_RESERVED → PAYMENT_FAILED → COMPENSATION_REQUIRED → INVENTORY_RELEASED
```

---

## 8. NFR Summary

### 8.1 Key Decisions

| Category | Decision | Rationale |
|----------|----------|-----------|
| Performance | < 1s (banking), < 2s (marketplace) | Balanced, achievable |
| Scalability | 1-10 concurrent ops | Demo context |
| Availability | 90% uptime | Focus on happy path |
| Consistency | Hybrid (strong + eventual) | Optimize latency |
| Security | IAM + default encryption | AWS native |
| Tech Stack | Python 3.11, multiple tables | Performance + simplicity |
| Reliability | Simple retries + idempotency | Sufficient for demo |

### 8.2 Trade-offs

**Chosen**: Speed of development, demo quality
**Sacrificed**: Production robustness, comprehensive error handling

**Justification**: 8-hour hackathon timeline, focus on working demo over production-ready system

### 8.3 Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Cold starts | Accept latency, no provisioned concurrency |
| DynamoDB throttling | On-demand mode auto-scales |
| Event delivery failures | EventBridge automatic retries |
| Data inconsistencies | Compensation logic for critical flows |
| Debugging complexity | Structured logs with correlation_id |

---

## 9. Next Steps

1. ✅ NFR Requirements complete
2. ⏳ Generate NFR Design artifacts (patterns, components)
3. ⏳ Generate Infrastructure Design (DynamoDB tables, Lambdas, EventBridge rules)
4. ⏳ Generate Code Generation Plan
5. ⏳ Implement Action Groups

---

**Document Status**: Complete  
**Approved By**: [Pending approval]  
**Next Stage**: NFR Design
