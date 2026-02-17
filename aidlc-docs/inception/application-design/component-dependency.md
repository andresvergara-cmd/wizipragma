# Component Dependencies - CENTLI

## Overview

This document defines dependency relationships, communication patterns, and data flow between CENTLI components.

---

## Dependency Matrix

| Component | Depends On | Dependency Type | Communication Pattern |
|-----------|------------|-----------------|----------------------|
| Frontend UI | Orchestration Service | Required | WebSocket (bidirectional) |
| Frontend UI | S3 | Optional | HTTPS (image upload) |
| Orchestration Service | AgentCore | Required | Synchronous invoke |
| Orchestration Service | Session Storage (DynamoDB) | Required | Synchronous read/write |
| Orchestration Service | S3 | Optional | Synchronous write (images) |
| Orchestration Service | Managed Memory | Required | Synchronous sync |
| AgentCore | Nova Sonic | Required | Synchronous invoke |
| AgentCore | Nova Canvas | Optional | Synchronous invoke |
| AgentCore | Managed Memory | Required | Synchronous read/write |
| AgentCore | EventBridge | Required | Asynchronous publish |
| EventBridge | Core Banking Mock | Required | Asynchronous trigger |
| EventBridge | Marketplace Mock | Required | Asynchronous trigger |
| EventBridge | CRM Mock | Required | Asynchronous trigger |
| Core Banking Mock | DynamoDB (Accounts) | Required | Synchronous read/write |
| Core Banking Mock | DynamoDB (Transactions) | Required | Synchronous write |
| Core Banking Mock | EventBridge | Required | Asynchronous publish (responses) |
| Marketplace Mock | DynamoDB (Products) | Required | Synchronous read |
| Marketplace Mock | DynamoDB (Purchases) | Required | Synchronous write |
| Marketplace Mock | EventBridge | Required | Asynchronous publish (responses, payment events) |
| Marketplace Mock | Core Banking Mock | Indirect | Via EventBridge (payment) |
| CRM Mock | DynamoDB (Beneficiaries) | Required | Synchronous read/write |
| CRM Mock | EventBridge | Required | Asynchronous publish (responses) |

---

## Communication Patterns

### Pattern 1: Synchronous Request-Response

**Used For**: Real-time operations requiring immediate response

**Examples**:
- Frontend ↔ Orchestration Service (WebSocket)
- Orchestration Service → AgentCore (invoke)
- AgentCore → Nova Sonic (voice processing)
- Action Groups → DynamoDB (data operations)

**Characteristics**:
- Blocking operation
- Immediate response expected
- Timeout handling required
- Error propagation direct

**Implementation**:
```python
# Example: Orchestration Service → AgentCore
response = agentcore_client.invoke_agent(
    agent_id=AGENT_ID,
    session_id=session_id,
    input_text=message
)
```

---

### Pattern 2: Asynchronous Event-Driven

**Used For**: Decoupled operations, multi-step workflows

**Examples**:
- AgentCore → EventBridge → Action Groups
- Action Groups → EventBridge → AgentCore (responses)
- Marketplace Mock → EventBridge → Core Banking Mock (payment)

**Characteristics**:
- Non-blocking operation
- Eventual consistency
- Retry logic built-in
- Loose coupling

**Implementation**:
```python
# Example: AgentCore publishes action event
eventbridge_client.put_events(
    Entries=[{
        'Source': 'centli.agentcore',
        'DetailType': 'ActionRequest',
        'Detail': json.dumps({
            'action_type': 'TRANSFER',
            'action_data': {...},
            'request_id': request_id
        })
    }]
)
```

---

### Pattern 3: Streaming

**Used For**: Real-time audio/video data transfer

**Examples**:
- Frontend → Orchestration Service (audio streaming)
- Orchestration Service → Frontend (audio response streaming)

**Characteristics**:
- Continuous data flow
- Low latency required
- Chunked processing
- Backpressure handling

**Implementation**:
```javascript
// Example: Frontend streams audio
const mediaRecorder = new MediaRecorder(stream);
mediaRecorder.ondataavailable = (event) => {
    websocket.send(JSON.stringify({
        type: 'VOICE_CHUNK',
        data: event.data,
        is_final: false
    }));
};
```

---

### Pattern 4: Cache-Aside with Sync

**Used For**: Session state management

**Examples**:
- Orchestration Service ↔ Local Session Storage ↔ Managed Memory

**Characteristics**:
- Read from cache first
- Write to both cache and backing store
- Periodic synchronization
- Conflict resolution

**Implementation**:
```python
# Example: Read session with cache-aside
def get_session(session_id):
    # Try local cache first
    session = local_cache.get(session_id)
    if session:
        return session
    
    # Fallback to Managed Memory
    session = managed_memory.get(session_id)
    if session:
        local_cache.set(session_id, session)
    
    return session
```

---

## Data Flow Diagrams

### Flow 1: User Message Processing (Text)

```
[User Browser]
    |
    | 1. WebSocket message (text)
    v
[Orchestration Service]
    |
    | 2. Invoke with message
    v
[AgentCore]
    |
    | 3. Recognize intent
    | 4. Publish action event
    v
[EventBridge]
    |
    | 5. Route to Action Group
    v
[Action Group Lambda]
    |
    | 6. Process action
    | 7. Query/Update DynamoDB
    v
[DynamoDB]
    |
    | 8. Return result
    v
[Action Group Lambda]
    |
    | 9. Publish response event
    v
[EventBridge]
    |
    | 10. Route to AgentCore
    v
[AgentCore]
    |
    | 11. Generate response
    v
[Orchestration Service]
    |
    | 12. Send via WebSocket
    v
[User Browser]
```

**Latency Breakdown**:
- Step 1-2: ~50ms (WebSocket + Lambda cold start)
- Step 2-3: ~500ms (AgentCore processing)
- Step 4-5: ~100ms (EventBridge routing)
- Step 6-7: ~200ms (Action Group processing)
- Step 8-10: ~100ms (Response routing)
- Step 11-12: ~300ms (Response generation)
- **Total**: ~1.25 seconds

---

### Flow 2: Voice Input Processing

```
[User Browser]
    |
    | 1. Audio stream (chunks)
    v
[Orchestration Service]
    |
    | 2. Buffer audio chunks
    | 3. Invoke Nova Sonic
    v
[Nova Sonic]
    |
    | 4. Transcribe to text
    v
[Orchestration Service]
    |
    | 5. Send text to AgentCore
    v
[AgentCore]
    |
    | (Continue as Flow 1)
```

**Additional Latency**:
- Audio streaming: ~500ms (real-time)
- Nova Sonic transcription: ~1-2 seconds
- **Total added**: ~1.5-2.5 seconds

---

### Flow 3: P2P Transfer with Beneficiary Resolution

```
[User] "Envíale 50 lucas a mi hermano"
    |
    v
[AgentCore] Recognizes: TRANSFER, alias="mi hermano", amount=50000
    |
    | Event: QUERY_BENEFICIARY
    v
[EventBridge] → [CRM Mock]
    |
    | Query beneficiaries by alias
    v
[DynamoDB: Beneficiaries]
    |
    | Returns: Juan López (account: 123456)
    v
[CRM Mock] → [EventBridge] → [AgentCore]
    |
    | Event: VALIDATE_FUNDS
    v
[EventBridge] → [Core Banking Mock]
    |
    | Check balance
    v
[DynamoDB: Accounts]
    |
    | Balance: 100,000 MXN (sufficient)
    v
[Core Banking Mock] → [EventBridge] → [AgentCore]
    |
    | Generate confirmation request
    v
[User] Confirms transfer
    |
    | Event: EXECUTE_TRANSFER
    v
[EventBridge] → [Core Banking Mock]
    |
    | Atomic update: debit 50,000 from user, credit 50,000 to Juan
    v
[DynamoDB: Accounts + Transactions]
    |
    | Transaction recorded
    v
[Core Banking Mock] → [EventBridge] → [AgentCore]
    |
    | Generate success message
    v
[User] "Operación firme. 50,000 pesos enviados a Juan López"
```

**Total Steps**: 11 steps  
**Total Latency**: ~5-7 seconds (includes user confirmation)

---

### Flow 4: Product Purchase with Payment

```
[User] Selects laptop + 12 MSI benefit
    |
    v
[AgentCore] Recognizes: PURCHASE, product_id, benefit_option
    |
    | Event: CALCULATE_BENEFITS
    v
[EventBridge] → [Marketplace Mock]
    |
    | Verify benefit eligibility
    v
[DynamoDB: Products]
    |
    | Returns: 12 MSI available, 5% cashback
    v
[Marketplace Mock] → [EventBridge] → [AgentCore]
    |
    | Generate confirmation request
    v
[User] Confirms purchase
    |
    | Event: EXECUTE_PURCHASE
    v
[EventBridge] → [Marketplace Mock]
    |
    | Event: PROCESS_PAYMENT (to Core Banking)
    v
[EventBridge] → [Core Banking Mock]
    |
    | Debit amount from credit line
    v
[DynamoDB: Accounts]
    |
    | Credit line reduced
    v
[Core Banking Mock] → [EventBridge] → [Marketplace Mock]
    |
    | Record purchase + apply benefits
    v
[DynamoDB: Purchases]
    |
    | Purchase recorded with benefits
    v
[Marketplace Mock] → [EventBridge] → [AgentCore]
    |
    | Generate success message
    v
[User] "Sustento actualizado. Laptop adquirida con 12 MSI + 500 pesos cashback"
```

**Total Steps**: 13 steps  
**Total Latency**: ~6-8 seconds (includes user confirmation)

---

## Dependency Graph

### Visual Representation

```
                    [User Browser]
                          |
                          | WebSocket
                          v
                [Orchestration Service]
                    |           |
                    |           | S3 (images)
                    v           v
              [AgentCore]    [S3 Bucket]
                |   |   |
                |   |   +-- Nova Sonic (voice)
                |   |
                |   +------ Nova Canvas (images)
                |
                | EventBridge
                v
          [EventBridge Bus]
            /      |      \
           /       |       \
          v        v        v
    [Core      [Market    [CRM
    Banking]   place]     Mock]
       |          |         |
       v          v         v
    [DynamoDB Tables]
    - Accounts
    - Transactions
    - Products
    - Purchases
    - Beneficiaries
    - Sessions
```

---

## Critical Dependencies

### Tier 1: System Cannot Function Without
1. **Orchestration Service**: Entry point for all user interactions
2. **AgentCore**: Core intelligence and orchestration
3. **EventBridge**: Component communication backbone
4. **DynamoDB**: Data persistence layer

**Failure Impact**: Complete system outage

**Mitigation**:
- Multi-AZ deployment for DynamoDB
- Lambda reserved concurrency
- EventBridge automatic retry
- Circuit breaker pattern in Orchestration Service

---

### Tier 2: Core Features Degraded
1. **Nova Sonic**: Voice input/output
2. **Core Banking Mock**: P2P transfers
3. **Marketplace Mock**: Product purchases

**Failure Impact**: Specific features unavailable, system partially functional

**Mitigation**:
- Text fallback if Nova Sonic fails
- Graceful error messages for Action Group failures
- Retry logic with exponential backoff

---

### Tier 3: Enhanced Features Unavailable
1. **Nova Canvas**: Image processing
2. **CRM Mock**: Beneficiary alias resolution
3. **S3**: Image storage

**Failure Impact**: Enhanced features unavailable, core features work

**Mitigation**:
- Skip image processing if Nova Canvas unavailable
- Direct account number input if CRM fails
- Temporary storage if S3 unavailable

---

## Integration Points

### Integration 1: Orchestration Service ↔ AgentCore

**Protocol**: AWS SDK (boto3)  
**Authentication**: IAM role  
**Data Format**: JSON  
**Error Handling**: Retry with exponential backoff (3 attempts)

**Request**:
```python
{
    "agent_id": "string",
    "session_id": "string",
    "input_text": "string",
    "user_id": "string",
    "metadata": {
        "auth_token": "string",
        "biometric_data": {}
    }
}
```

**Response**:
```python
{
    "output_text": "string",
    "action_events": [],
    "session_state": {},
    "audio_url": "string (optional)"
}
```

---

### Integration 2: AgentCore ↔ EventBridge

**Protocol**: EventBridge PutEvents API  
**Authentication**: IAM role  
**Data Format**: JSON (CloudEvents-like)  
**Error Handling**: Built-in retry (3 attempts)

**Event Schema**:
```json
{
    "Source": "centli.agentcore",
    "DetailType": "ActionRequest",
    "Detail": {
        "action_type": "string",
        "action_data": {},
        "user_id": "string",
        "session_id": "string",
        "request_id": "string",
        "timestamp": "ISO 8601"
    }
}
```

---

### Integration 3: EventBridge ↔ Action Groups

**Protocol**: Lambda invoke (async)  
**Authentication**: IAM role  
**Data Format**: JSON  
**Error Handling**: Dead letter queue + retry

**Lambda Event**:
```json
{
    "version": "0",
    "id": "event-id",
    "detail-type": "ActionRequest",
    "source": "centli.agentcore",
    "account": "aws-account-id",
    "time": "ISO 8601",
    "region": "us-east-1",
    "resources": [],
    "detail": {
        "action_type": "TRANSFER",
        "action_data": {...},
        "request_id": "string"
    }
}
```

---

### Integration 4: Action Groups ↔ DynamoDB

**Protocol**: AWS SDK (boto3)  
**Authentication**: IAM role  
**Data Format**: DynamoDB JSON  
**Error Handling**: Exponential backoff (built-in)

**Operations**:
- `get_item`: Retrieve single item
- `put_item`: Create/update item
- `query`: Query with index
- `update_item`: Atomic update
- `transact_write_items`: Atomic multi-item transaction

---

### Integration 5: Frontend ↔ Orchestration Service

**Protocol**: WebSocket (WSS)  
**Authentication**: JWT token in query params  
**Data Format**: JSON  
**Error Handling**: Automatic reconnection

**Message Format**:
```json
{
    "type": "TEXT | VOICE | IMAGE | COMMAND",
    "content": "string | base64",
    "metadata": {
        "timestamp": "ISO 8601",
        "message_id": "string"
    }
}
```

---

## Deployment Dependencies

### Deployment Order

1. **Infrastructure Foundation** (SAM template)
   - DynamoDB tables
   - S3 bucket
   - EventBridge bus
   - IAM roles

2. **Action Group Lambdas** (parallel)
   - Core Banking Mock
   - Marketplace Mock
   - CRM Mock

3. **AgentCore Configuration**
   - Bedrock Agent setup
   - Action Group registration
   - Managed Memory configuration

4. **Orchestration Service** (parallel with AgentCore)
   - Connect Lambda
   - Disconnect Lambda
   - Message Lambda
   - API Gateway WebSocket

5. **Frontend Deployment**
   - Build static assets
   - Upload to S3
   - Configure CloudFront (optional)

### Rollback Strategy

**If deployment fails at any stage**:
1. Identify failed component
2. Roll back to previous version of failed component
3. Verify dependencies still functional
4. Re-attempt deployment with fixes

**Critical**: Action Groups can be deployed independently without affecting other components (loose coupling via EventBridge)

---

## Performance Considerations

### Latency Budget

| Component | Target Latency | Max Acceptable |
|-----------|---------------|----------------|
| WebSocket RTT | <50ms | <100ms |
| AgentCore Processing | <500ms | <1000ms |
| EventBridge Routing | <100ms | <200ms |
| Action Group Processing | <200ms | <500ms |
| DynamoDB Operations | <10ms | <50ms |
| Nova Sonic (voice) | <2s | <3s |
| **Total End-to-End** | **<3s** | **<5s** |

### Throughput Targets

| Component | Target TPS | Max Capacity |
|-----------|-----------|--------------|
| Orchestration Service | 100 | 1000 (Lambda scaling) |
| AgentCore | 50 | 200 (Bedrock limits) |
| EventBridge | 1000 | 10000+ |
| Action Groups | 100 each | 1000 each |
| DynamoDB | 1000 | On-demand (unlimited) |

### Bottleneck Analysis

**Likely Bottlenecks**:
1. **AgentCore**: Bedrock has rate limits (~50 TPS per agent)
2. **Nova Sonic**: Voice processing is compute-intensive
3. **Lambda Cold Starts**: First invocation adds ~1-2s latency

**Mitigation**:
- Reserved concurrency for critical Lambdas
- Provisioned concurrency for Orchestration Service
- Request throttling at API Gateway
- Caching for frequent queries

---

**Document Status**: Complete  
**Created**: 2026-02-16  
**Dependencies**: 7 components with 15+ integration points  
**Architecture**: Event-driven, loosely coupled, highly scalable
