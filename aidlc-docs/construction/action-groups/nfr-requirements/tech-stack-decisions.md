# Tech Stack Decisions - Unit 3: Action Groups

## Document Information
- **Unit**: Unit 3 (Action Groups - Backend Services)
- **Stage**: NFR Requirements
- **Created**: 2026-02-17
- **Context**: 8-hour hackathon, AWS serverless architecture

---

## 1. Runtime and Language

### Python 3.11

**Decision**: Use Python 3.11 for all Action Group Lambda functions

**Rationale**:
- **Performance**: 10-60% faster than Python 3.9/3.10 (PEP 659 adaptive interpreter)
- **AWS Support**: Fully supported in AWS Lambda since November 2023
- **Consistency**: Matches Unit 2 (AgentCore & Orchestration) runtime
- **Libraries**: Excellent boto3 compatibility, mature ecosystem
- **Developer Experience**: Modern syntax, better error messages

**Alternatives Considered**:
- Python 3.9: Stable but slower performance
- Python 3.12: Cutting edge, potential compatibility issues
- Node.js: Different language from Unit 2, team expertise in Python

**Dependencies**:
- boto3 (AWS SDK) - included in Lambda runtime
- Standard library only (no external dependencies for speed)

---

## 2. Database Technology

### Amazon DynamoDB

**Decision**: Use DynamoDB as primary data store for all Action Groups

**Rationale**:
- **Serverless**: No server management, auto-scaling
- **Performance**: Single-digit millisecond latency
- **Cost**: On-demand pricing, minimal cost for demo volume
- **Integration**: Native AWS integration with Lambda, EventBridge
- **Consistency**: Supports both strong and eventual consistency

**Table Design Strategy**: Multiple tables (one per entity type)

**Tables**:
1. `centli-accounts` - User bank accounts
2. `centli-transactions` - Transaction history
3. `centli-products` - Product catalog
4. `centli-beneficiaries` - User beneficiaries and aliases
5. `centli-purchases` - Purchase history
6. `centli-retailers` - Retailer information

**Rationale for Multiple Tables**:
- **Simplicity**: Clear entity boundaries, easy to understand
- **Debugging**: Easier to inspect data in AWS Console
- **Access Patterns**: Simple queries, no complex joins
- **Development Speed**: Faster to implement in hackathon
- **Trade-off**: More tables vs simpler code (acceptable for demo)

**Alternatives Considered**:
- Single Table Design: Complex, requires advanced DynamoDB knowledge
- RDS/Aurora: Requires VPC, slower cold starts, overkill for demo
- DocumentDB: MongoDB-compatible, but more complex setup

---

## 3. Event-Driven Architecture

### Amazon EventBridge

**Decision**: Use EventBridge as event bus for inter-service communication

**Rationale**:
- **Already Deployed**: Part of Unit 1 (Infrastructure Foundation)
- **Loose Coupling**: Action Groups don't need to know about each other
- **Reliability**: Built-in retry and dead-letter queue support
- **Scalability**: Handles millions of events per second
- **Observability**: Native CloudWatch integration

**Event Schema Format**: JSON with loose validation

**Example Event**:
```json
{
  "version": "1.0",
  "event_type": "TRANSFER_REQUEST",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-17T10:30:00Z",
  "source": "core-banking",
  "user_id": "user-123",
  "data": {
    "from_account": "acc-456",
    "to_account": "acc-789",
    "amount": 5000,
    "currency": "MXN"
  }
}
```

**Rationale for Loose Validation**:
- **Speed**: Faster to implement, no schema registry needed
- **Flexibility**: Easy to add fields during development
- **Debugging**: JSON is human-readable in CloudWatch Logs
- **Trade-off**: Less type safety vs development speed (acceptable for demo)

**Alternatives Considered**:
- Strict JSON Schema: More robust, but slower to implement
- Avro/Protobuf: Efficient, but adds complexity
- Direct Lambda invocation: Tight coupling, not recommended

---

## 4. Lambda Architecture

### Multiple Lambdas per Action Group (9 Lambdas Total)

**Decision**: Create separate Lambda function for each action

**Lambda Functions**:

**Core Banking (3 Lambdas)**:
1. `centli-core-banking-balance` - Get account balance
2. `centli-core-banking-transfer` - Execute transfer
3. `centli-core-banking-transactions` - Get transaction history

**Marketplace (3 Lambdas)**:
4. `centli-marketplace-catalog` - Get product catalog
5. `centli-marketplace-benefits` - Calculate benefits
6. `centli-marketplace-purchase` - Execute purchase

**CRM (3 Lambdas)**:
7. `centli-crm-resolve-alias` - Resolve beneficiary alias
8. `centli-crm-get-beneficiaries` - List beneficiaries
9. `centli-crm-add-beneficiary` - Add new beneficiary

**Rationale**:
- **Separation of Concerns**: Each Lambda has single responsibility
- **Independent Scaling**: Each action scales independently
- **Easier Debugging**: Isolated CloudWatch Log streams
- **Smaller Code**: Faster cold starts, easier to understand
- **Parallel Development**: Team can work on different Lambdas simultaneously

**Configuration**:
- **Memory**: 512 MB (sufficient for demo)
- **Timeout**: 10 seconds
- **Runtime**: Python 3.11
- **Concurrency**: No reserved concurrency (use account default)

**Alternatives Considered**:
- Single Lambda per Action Group (3 total): Simpler deployment, but larger code
- Monolithic Lambda: Not recommended, tight coupling

---

## 5. Data Access Patterns

### DynamoDB Access Patterns

**Design Principle**: One table per entity, simple partition key + sort key

**Access Patterns by Table**:

**centli-accounts**:
- Get account by user_id and account_id
- List all accounts for user_id
```
PK: user_id
SK: account_id
```

**centli-transactions**:
- Get transaction by account_id and transaction_id
- List transactions for account_id (sorted by timestamp)
- List transactions for user_id (via GSI)
```
PK: account_id
SK: timestamp#transaction_id
GSI: user_id (PK) + timestamp (SK)
```

**centli-products**:
- Get product by product_id
- List products by retailer_id
```
PK: product_id
SK: retailer_id
```

**centli-beneficiaries**:
- Get beneficiary by user_id and beneficiary_id
- Resolve alias to beneficiary (via GSI)
```
PK: user_id
SK: beneficiary_id
GSI: alias (PK) + user_id (SK)
```

**centli-purchases**:
- Get purchase by user_id and purchase_id
- List purchases for user_id (sorted by timestamp)
```
PK: user_id
SK: timestamp#purchase_id
```

**centli-retailers**:
- Get retailer by retailer_id
```
PK: retailer_id
```

**Consistency Strategy**:
- **Strong Consistency**: Balance queries, transaction history
- **Eventual Consistency**: Product catalog, beneficiary list

---

## 6. Error Handling and Reliability

### Retry Strategy

**Decision**: Simple retry with fixed delay

**Configuration**:
- **Max Retries**: 3 attempts
- **Delay**: 100ms fixed delay between retries
- **Scope**: DynamoDB operations, EventBridge publish

**Implementation**:
```python
def retry_operation(operation, max_retries=3, delay=0.1):
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
```

**Rationale**:
- **Simplicity**: Easy to implement and understand
- **Sufficient**: Low concurrency, transient failures rare
- **Trade-off**: No exponential backoff vs simplicity (acceptable for demo)

### Idempotency

**Decision**: Request ID tracking in DynamoDB

**Implementation**:
- Add `request_id` attribute to entities
- Check for duplicate `request_id` before processing
- Store `request_id` with 24-hour TTL

**Example**:
```python
def is_duplicate(table, request_id):
    response = table.get_item(
        Key={'request_id': request_id},
        ConsistentRead=True
    )
    return 'Item' in response

def process_with_idempotency(table, request_id, operation):
    if is_duplicate(table, request_id):
        return {"status": "duplicate", "message": "Already processed"}
    
    result = operation()
    
    # Store request_id to prevent duplicates
    table.put_item(Item={
        'request_id': request_id,
        'processed_at': datetime.now().isoformat(),
        'ttl': int(time.time()) + 86400  # 24 hours
    })
    
    return result
```

**Rationale**:
- **Reliability**: Prevents duplicate processing
- **Control**: Full control over idempotency window
- **Simplicity**: No external dependencies

---

## 7. Logging and Monitoring

### CloudWatch Logs + Basic Metrics

**Decision**: Structured JSON logging with correlation_id

**Log Format**:
```json
{
  "timestamp": "2026-02-17T10:30:00.123Z",
  "level": "INFO",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "lambda": "core-banking-transfer",
  "event_type": "TRANSFER_REQUEST",
  "user_id": "user-123",
  "message": "Transfer executed successfully",
  "details": {
    "from_account": "***",
    "to_account": "***",
    "amount": 5000,
    "duration_ms": 234
  }
}
```

**PII Masking**:
- Mask account numbers: `"account": "***"`
- Mask balances: `"balance": "***"`
- Allow user_id, names for debugging

**Metrics**:
- Lambda execution duration (p50, p95, p99)
- Error count by Lambda
- DynamoDB query latency
- EventBridge publish success rate

**Rationale**:
- **Debuggability**: Structured logs easy to query
- **Correlation**: Track requests across services
- **Security**: PII protection in logs
- **Trade-off**: No X-Ray tracing vs simplicity (acceptable for demo)

**Alternatives Considered**:
- X-Ray Tracing: Comprehensive, but adds complexity
- Custom Metrics: More detailed, but slower to implement

---

## 8. Security

### IAM Role-Based Access Control

**Decision**: Use IAM roles for authentication and authorization

**Lambda Execution Role Permissions**:
```yaml
- DynamoDB:
  - GetItem
  - PutItem
  - UpdateItem
  - Query
  - Scan (limited use)
  
- EventBridge:
  - PutEvents
  
- CloudWatch Logs:
  - CreateLogGroup
  - CreateLogStream
  - PutLogEvents
```

**Principle of Least Privilege**:
- Each Lambda has minimal permissions
- No cross-account access
- No public endpoints (EventBridge only)

### Data Encryption

**Decision**: Use AWS default encryption

**Encryption at Rest**:
- DynamoDB: AWS managed keys (default)
- CloudWatch Logs: AWS managed keys (default)

**Encryption in Transit**:
- TLS 1.2+ for all AWS service communication (SDK default)

**Rationale**:
- **Zero Configuration**: Enabled by default
- **Compliance**: Meets basic security requirements
- **Cost**: No additional cost
- **Trade-off**: No customer-managed keys vs simplicity (acceptable for demo)

---

## 9. Compensation Logic

### Automatic Compensation via EventBridge

**Decision**: Implement saga pattern with compensation events

**Purchase Flow Example**:

**Success Path**:
```
1. PURCHASE_INITIATED
2. INVENTORY_RESERVED
3. PAYMENT_COMPLETED
4. PURCHASE_CONFIRMED
```

**Failure Path with Compensation**:
```
1. PURCHASE_INITIATED
2. INVENTORY_RESERVED
3. PAYMENT_FAILED
4. COMPENSATION_REQUIRED
5. INVENTORY_RELEASED
6. USER_NOTIFIED
```

**Implementation**:
- Each Action Group listens for compensation events
- Compensation logic reverses previous actions
- Idempotency ensures compensation runs once

**Rationale**:
- **Reliability**: Handles partial failures gracefully
- **Consistency**: Maintains data integrity
- **Simplicity**: Leverages existing EventBridge infrastructure
- **Demo Quality**: Shows understanding of distributed systems

---

## 10. Tech Stack Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Runtime | Python 3.11 | Performance, consistency with Unit 2 |
| Database | DynamoDB (multiple tables) | Serverless, simple access patterns |
| Event Bus | EventBridge | Already deployed, loose coupling |
| Lambda Architecture | 9 separate Lambdas | Separation of concerns, easier debugging |
| Event Format | JSON (loose validation) | Speed, flexibility, debuggability |
| Retry Strategy | Simple (3 retries, 100ms) | Sufficient for low volume |
| Idempotency | Request ID tracking | Reliability, control |
| Logging | CloudWatch Logs + JSON | Structured, correlation_id |
| Security | IAM + default encryption | AWS native, zero config |
| Compensation | Saga pattern via events | Reliability, consistency |

---

## 11. Trade-offs and Justifications

### Chosen: Speed of Development
- Multiple tables (vs single table design)
- Loose event validation (vs strict schema)
- Simple retries (vs exponential backoff)
- No X-Ray tracing (vs comprehensive observability)

### Sacrificed: Production Robustness
- No provisioned concurrency (cold starts acceptable)
- No dead-letter queues (manual monitoring)
- No customer-managed encryption keys
- Minimal error handling (focus on happy path)

### Justification
8-hour hackathon timeline requires pragmatic decisions. Focus on working demo over production-ready system.

---

## 12. Next Steps

1. ✅ Tech Stack Decisions complete
2. ⏳ Generate NFR Design artifacts (patterns, components)
3. ⏳ Generate Infrastructure Design (SAM template updates)
4. ⏳ Generate Code Generation Plan
5. ⏳ Implement Action Groups

---

**Document Status**: Complete  
**Approved By**: [Pending approval]  
**Next Stage**: NFR Design
