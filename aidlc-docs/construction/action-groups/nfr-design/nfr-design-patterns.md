# NFR Design Patterns - Unit 3: Action Groups

## Document Information
- **Unit**: Unit 3 (Action Groups - Backend Services)
- **Stage**: NFR Design
- **Created**: 2026-02-17
- **Context**: Patterns to achieve NFR requirements in hackathon context

---

## 1. Performance Patterns

### 1.1 Optimized DynamoDB Access Pattern

**Pattern**: Partition Key + Sort Key with GSI for alternate access

**Implementation**:
```python
# Primary access: Get account by user_id and account_id
response = accounts_table.get_item(
    Key={
        'user_id': user_id,
        'account_id': account_id
    },
    ConsistentRead=True  # Strong consistency for balance
)

# Alternate access: Query transactions by user_id (via GSI)
response = transactions_table.query(
    IndexName='user_id-timestamp-index',
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': user_id},
    ScanIndexForward=False,  # Descending order (newest first)
    Limit=20
)
```

**Benefits**:
- Single-digit millisecond latency
- No table scans
- Efficient pagination

**Target**: < 100ms per query

---

### 1.2 Lambda Warm-Up Pattern (Optional)

**Pattern**: Keep Lambda warm during demo with periodic invocations

**Implementation**:
```python
# In Lambda handler
def lambda_handler(event, context):
    # Detect warm-up event
    if event.get('source') == 'warmup':
        return {'statusCode': 200, 'body': 'warmed'}
    
    # Normal processing
    return process_event(event)
```

**EventBridge Rule** (optional):
```yaml
WarmUpRule:
  Type: AWS::Events::Rule
  Properties:
    ScheduleExpression: rate(5 minutes)
    Targets:
      - Arn: !GetAtt CoreBankingBalanceFunction.Arn
        Input: '{"source": "warmup"}'
```

**Benefits**:
- Reduces cold start latency
- Consistent performance during demo

**Trade-off**: Additional cost (~$0.10 for 8 hours)

**Recommendation**: Skip for demo, accept cold starts

---

### 1.3 Batch Processing Pattern

**Pattern**: Batch DynamoDB writes for efficiency

**Implementation**:
```python
def batch_write_transactions(transactions):
    with transactions_table.batch_writer() as batch:
        for transaction in transactions:
            batch.put_item(Item=transaction)
```

**Use Cases**:
- Seeding initial data
- Bulk transaction imports

**Benefits**:
- Up to 25 items per batch
- Reduced API calls
- Lower latency for bulk operations

---

## 2. Scalability Patterns

### 2.1 Event-Driven Asynchronous Pattern

**Pattern**: Decouple Action Groups via EventBridge events

**Flow**:
```
AgentCore → EventBridge → Lambda (Action Group) → DynamoDB
                                ↓
                          EventBridge (result event)
                                ↓
                          Lambda (next Action Group)
```

**Example - Purchase Flow**:
```python
# Marketplace Lambda publishes event
eventbridge.put_events(
    Entries=[{
        'Source': 'marketplace',
        'DetailType': 'PURCHASE_INITIATED',
        'Detail': json.dumps({
            'correlation_id': correlation_id,
            'user_id': user_id,
            'product_id': product_id,
            'amount': amount
        }),
        'EventBusName': 'centli-event-bus'
    }]
)

# Core Banking Lambda listens and processes payment
def lambda_handler(event, context):
    detail = event['detail']
    process_payment(detail)
    
    # Publish result event
    eventbridge.put_events(...)
```

**Benefits**:
- Loose coupling between Action Groups
- Independent scaling
- Automatic retry by EventBridge
- Easy to add new Action Groups

**Target**: < 10 events/second throughput

---

### 2.2 DynamoDB On-Demand Scaling Pattern

**Pattern**: Use on-demand capacity mode for auto-scaling

**Configuration**:
```yaml
AccountsTable:
  Type: AWS::DynamoDB::Table
  Properties:
    BillingMode: PAY_PER_REQUEST  # On-demand
    AttributeDefinitions:
      - AttributeName: user_id
        AttributeType: S
      - AttributeName: account_id
        AttributeType: S
    KeySchema:
      - AttributeName: user_id
        KeyType: HASH
      - AttributeName: account_id
        KeyType: RANGE
```

**Benefits**:
- Zero capacity planning
- Automatic scaling to handle spikes
- Pay only for what you use

**Cost**: ~$1.25 per million writes, ~$0.25 per million reads

---

## 3. Availability Patterns

### 3.1 Retry with Exponential Backoff Pattern

**Pattern**: Retry failed operations with increasing delays

**Implementation**:
```python
import time
from botocore.exceptions import ClientError

def retry_with_backoff(operation, max_retries=3):
    """Retry operation with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return operation()
        except ClientError as e:
            if e.response['Error']['Code'] in ['ProvisionedThroughputExceededException', 
                                                 'ThrottlingException']:
                if attempt == max_retries - 1:
                    raise
                
                # Exponential backoff: 100ms, 200ms, 400ms
                delay = 0.1 * (2 ** attempt)
                time.sleep(delay)
            else:
                raise

# Usage
def get_account_balance(user_id, account_id):
    def operation():
        return accounts_table.get_item(
            Key={'user_id': user_id, 'account_id': account_id}
        )
    
    return retry_with_backoff(operation)
```

**Benefits**:
- Handles transient failures
- Reduces error rate
- Graceful degradation

**Target**: 90% uptime with retries

---

### 3.2 Circuit Breaker Pattern (Simplified)

**Pattern**: Fail fast when downstream service is unavailable

**Implementation**:
```python
class SimpleCircuitBreaker:
    def __init__(self, failure_threshold=3, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, operation):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception('Circuit breaker is OPEN')
        
        try:
            result = operation()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'

# Usage
dynamodb_breaker = SimpleCircuitBreaker()

def get_balance_with_breaker(user_id, account_id):
    return dynamodb_breaker.call(
        lambda: get_account_balance(user_id, account_id)
    )
```

**Benefits**:
- Prevents cascading failures
- Fast failure when service is down
- Automatic recovery

**Recommendation**: Optional for demo, implement if time permits

---

## 4. Data Consistency Patterns

### 4.1 Optimistic Locking Pattern

**Pattern**: Use version attribute to prevent concurrent updates

**Implementation**:
```python
def transfer_with_optimistic_locking(from_account_id, to_account_id, amount):
    max_retries = 3
    
    for attempt in range(max_retries):
        # Read current balance and version
        from_account = accounts_table.get_item(
            Key={'user_id': user_id, 'account_id': from_account_id},
            ConsistentRead=True
        )['Item']
        
        current_balance = from_account['balance']
        current_version = from_account.get('version', 0)
        
        # Check sufficient funds
        if current_balance < amount:
            raise InsufficientFundsError()
        
        # Update with version check
        try:
            accounts_table.update_item(
                Key={'user_id': user_id, 'account_id': from_account_id},
                UpdateExpression='SET balance = :new_balance, version = :new_version',
                ConditionExpression='version = :current_version',
                ExpressionAttributeValues={
                    ':new_balance': current_balance - amount,
                    ':new_version': current_version + 1,
                    ':current_version': current_version
                }
            )
            break  # Success
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                if attempt == max_retries - 1:
                    raise ConcurrentUpdateError()
                time.sleep(0.1)  # Retry after delay
            else:
                raise
```

**Benefits**:
- Prevents lost updates
- No distributed locks needed
- Handles concurrent transfers

**Target**: < 3 retries for 99% of operations

---

### 4.2 Eventual Consistency with Compensation Pattern

**Pattern**: Use saga pattern for cross-Action Group transactions

**Purchase Flow with Compensation**:
```python
# Step 1: Marketplace reserves inventory
def reserve_inventory(product_id, quantity):
    # Update product inventory
    products_table.update_item(
        Key={'product_id': product_id},
        UpdateExpression='SET reserved = reserved + :qty',
        ExpressionAttributeValues={':qty': quantity}
    )
    
    # Publish event
    publish_event('INVENTORY_RESERVED', {
        'product_id': product_id,
        'quantity': quantity,
        'correlation_id': correlation_id
    })

# Step 2: Core Banking processes payment
def process_payment(user_id, amount, correlation_id):
    try:
        # Deduct from account
        transfer_funds(user_id, amount)
        
        # Publish success
        publish_event('PAYMENT_COMPLETED', {
            'user_id': user_id,
            'amount': amount,
            'correlation_id': correlation_id
        })
    except Exception as e:
        # Publish failure - triggers compensation
        publish_event('PAYMENT_FAILED', {
            'user_id': user_id,
            'amount': amount,
            'correlation_id': correlation_id,
            'error': str(e)
        })

# Step 3: Marketplace compensates on payment failure
def handle_payment_failed(event):
    detail = event['detail']
    product_id = detail['product_id']
    quantity = detail['quantity']
    
    # Release reserved inventory
    products_table.update_item(
        Key={'product_id': product_id},
        UpdateExpression='SET reserved = reserved - :qty',
        ExpressionAttributeValues={':qty': quantity}
    )
    
    # Publish compensation complete
    publish_event('INVENTORY_RELEASED', detail)
```

**Benefits**:
- Handles distributed transactions
- Automatic rollback on failure
- Maintains data consistency

**Trade-off**: Temporary inconsistency acceptable

---

### 4.3 Idempotency Pattern

**Pattern**: Track request IDs to prevent duplicate processing

**Implementation**:
```python
def process_with_idempotency(request_id, operation):
    """Process operation with idempotency guarantee"""
    
    # Check if already processed
    try:
        response = idempotency_table.get_item(
            Key={'request_id': request_id},
            ConsistentRead=True
        )
        
        if 'Item' in response:
            # Already processed, return cached result
            return {
                'status': 'duplicate',
                'result': response['Item']['result']
            }
    except ClientError:
        pass
    
    # Process operation
    result = operation()
    
    # Store result with TTL
    idempotency_table.put_item(
        Item={
            'request_id': request_id,
            'result': result,
            'processed_at': datetime.now().isoformat(),
            'ttl': int(time.time()) + 86400  # 24 hours
        }
    )
    
    return {'status': 'processed', 'result': result}

# Usage
def handle_transfer_request(event):
    request_id = event['detail']['request_id']
    
    return process_with_idempotency(
        request_id,
        lambda: execute_transfer(event['detail'])
    )
```

**Benefits**:
- Prevents duplicate transfers
- Safe to retry failed operations
- 24-hour idempotency window

---

## 5. Security Patterns

### 5.1 Least Privilege IAM Pattern

**Pattern**: Grant minimal permissions per Lambda

**Implementation**:
```yaml
CoreBankingBalanceFunctionRole:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Statement:
        - Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    Policies:
      - PolicyName: DynamoDBReadAccess
        PolicyDocument:
          Statement:
            - Effect: Allow
              Action:
                - dynamodb:GetItem
                - dynamodb:Query
              Resource:
                - !GetAtt AccountsTable.Arn
                - !Sub '${AccountsTable.Arn}/index/*'
      - PolicyName: EventBridgePublish
        PolicyDocument:
          Statement:
            - Effect: Allow
              Action: events:PutEvents
              Resource: !GetAtt EventBus.Arn
```

**Benefits**:
- Minimal attack surface
- Prevents unauthorized access
- Follows AWS best practices

---

### 5.2 PII Masking Pattern

**Pattern**: Mask sensitive data in logs

**Implementation**:
```python
import re
import json

def mask_pii(data):
    """Mask sensitive fields in log data"""
    if isinstance(data, dict):
        masked = {}
        for key, value in data.items():
            if key in ['account_number', 'balance', 'amount']:
                masked[key] = '***'
            elif key == 'account_id':
                # Show last 4 digits only
                masked[key] = f"***{value[-4:]}" if len(value) > 4 else '***'
            else:
                masked[key] = mask_pii(value)
        return masked
    elif isinstance(data, list):
        return [mask_pii(item) for item in data]
    else:
        return data

def log_event(level, message, data=None):
    """Log with PII masking"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'message': message,
        'data': mask_pii(data) if data else None
    }
    print(json.dumps(log_entry))

# Usage
log_event('INFO', 'Transfer executed', {
    'from_account': 'acc-123456',
    'to_account': 'acc-789012',
    'amount': 5000
})
# Output: {"from_account": "***3456", "to_account": "***9012", "amount": "***"}
```

**Benefits**:
- Protects sensitive data
- Complies with privacy regulations
- Still allows debugging

---

## 6. Reliability Patterns

### 6.1 Correlation ID Pattern

**Pattern**: Track requests across services with correlation_id

**Implementation**:
```python
import uuid

def generate_correlation_id():
    """Generate unique correlation ID"""
    return str(uuid.uuid4())

def propagate_correlation_id(event):
    """Extract or generate correlation ID"""
    return event.get('detail', {}).get('correlation_id') or generate_correlation_id()

def lambda_handler(event, context):
    correlation_id = propagate_correlation_id(event)
    
    # Add to all logs
    logger = setup_logger(correlation_id)
    logger.info('Processing event')
    
    # Add to all published events
    publish_event('TRANSFER_COMPLETED', {
        'correlation_id': correlation_id,
        'user_id': user_id,
        'amount': amount
    })
    
    return {'correlation_id': correlation_id}
```

**Benefits**:
- End-to-end request tracing
- Easy debugging across services
- Performance analysis

---

### 6.2 Structured Logging Pattern

**Pattern**: Use JSON structured logs with consistent schema

**Implementation**:
```python
import json
import logging
from datetime import datetime

class StructuredLogger:
    def __init__(self, lambda_name, correlation_id):
        self.lambda_name = lambda_name
        self.correlation_id = correlation_id
    
    def log(self, level, message, **kwargs):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'lambda': self.lambda_name,
            'correlation_id': self.correlation_id,
            'message': message,
            **kwargs
        }
        print(json.dumps(log_entry))
    
    def info(self, message, **kwargs):
        self.log('INFO', message, **kwargs)
    
    def error(self, message, **kwargs):
        self.log('ERROR', message, **kwargs)
    
    def warning(self, message, **kwargs):
        self.log('WARNING', message, **kwargs)

# Usage
logger = StructuredLogger('core-banking-transfer', correlation_id)
logger.info('Transfer initiated', user_id=user_id, amount=amount)
logger.error('Insufficient funds', user_id=user_id, balance=balance, requested=amount)
```

**Benefits**:
- Easy to query in CloudWatch Logs Insights
- Consistent log format
- Machine-readable

**CloudWatch Logs Insights Query**:
```
fields @timestamp, message, correlation_id, user_id
| filter level = "ERROR"
| sort @timestamp desc
| limit 20
```

---

### 6.3 Dead Letter Queue Pattern (Optional)

**Pattern**: Capture failed events for manual review

**Implementation**:
```yaml
CoreBankingTransferFunction:
  Type: AWS::Serverless::Function
  Properties:
    Handler: transfer.lambda_handler
    Runtime: python3.11
    DeadLetterQueue:
      Type: SQS
      TargetArn: !GetAtt FailedEventsQueue.Arn

FailedEventsQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: centli-failed-events
    MessageRetentionPeriod: 1209600  # 14 days
```

**Benefits**:
- No lost events
- Manual review and replay
- Debugging failed scenarios

**Recommendation**: Skip for demo, implement if time permits

---

## 7. Pattern Summary

| Pattern | Purpose | Priority | Complexity |
|---------|---------|----------|------------|
| Optimized DynamoDB Access | Performance | High | Low |
| Event-Driven Asynchronous | Scalability | High | Low |
| Retry with Backoff | Availability | High | Low |
| Optimistic Locking | Consistency | High | Medium |
| Saga with Compensation | Consistency | High | Medium |
| Idempotency | Reliability | High | Low |
| Least Privilege IAM | Security | High | Low |
| PII Masking | Security | Medium | Low |
| Correlation ID | Reliability | High | Low |
| Structured Logging | Reliability | High | Low |
| Circuit Breaker | Availability | Low | Medium |
| Lambda Warm-Up | Performance | Low | Low |
| Dead Letter Queue | Reliability | Low | Low |

**Recommendation for Hackathon**:
- Implement all High priority patterns
- Skip Low priority patterns (time constraints)
- Implement Medium priority if time permits

---

## 8. Next Steps

1. ✅ NFR Design Patterns complete
2. ⏳ Generate Logical Components diagram
3. ⏳ Generate Infrastructure Design
4. ⏳ Generate Code Generation Plan
5. ⏳ Implement Action Groups

---

**Document Status**: Complete  
**Approved By**: [Pending approval]  
**Next Artifact**: Logical Components
