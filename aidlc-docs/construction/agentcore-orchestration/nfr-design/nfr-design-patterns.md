# NFR Design Patterns - Unit 2: AgentCore & Orchestration

## Overview

This document defines the design patterns used to implement non-functional requirements for the AgentCore & Orchestration unit.

**Context**: Hackathon demo, pragmatic patterns, AWS-native solutions

---

## 1. Performance Patterns

### 1.1 Asynchronous Processing Pattern

**Purpose**: Minimize response latency by processing tasks asynchronously

**Implementation**:
```
User Request → WebSocket (immediate ack)
  ↓
Lambda (async processing)
  ↓
AgentCore (async)
  ↓
EventBridge (async)
  ↓
Action Groups (async)
  ↓
Response → WebSocket
```

**Benefits**:
- Non-blocking user experience
- Better resource utilization
- Handles variable processing times

**Trade-offs**:
- More complex error handling
- Requires correlation (request_id)

---

### 1.2 Batch Processing Pattern (Voice)

**Purpose**: Optimize voice processing latency vs accuracy

**Implementation**:
- Wait for complete audio utterance
- Process entire audio in single Nova Sonic call
- Better accuracy than streaming for short utterances

**Configuration**:
- Max audio duration: 60 seconds
- Min audio duration: 0.5 seconds
- Processing time: ~1-2 seconds

**Benefits**:
- Better transcription accuracy
- Simpler implementation
- Predictable latency

---

### 1.3 Parallel Processing Pattern (Multimodal)

**Purpose**: Process voice and image inputs simultaneously

**Implementation**:
```python
async def process_multimodal(voice_data, image_data):
    # Process both in parallel
    voice_task = process_voice(voice_data)
    image_task = process_image(image_data)
    
    # Wait for both to complete
    voice_result, image_result = await asyncio.gather(
        voice_task, image_task
    )
    
    # Merge results
    return merge_results(voice_result, image_result)
```

**Benefits**:
- Reduced total latency
- Better resource utilization
- Improved user experience

---

### 1.4 Connection Pooling Pattern

**Purpose**: Reuse connections to external services

**Implementation**:
- Boto3 client reuse across Lambda invocations
- Connection pooling for DynamoDB
- HTTP connection pooling for Bedrock APIs

**Configuration**:
```python
# Global client (reused across invocations)
bedrock_client = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
```

**Benefits**:
- Reduced connection overhead
- Lower latency
- Better performance

---

## 2. Scalability Patterns

### 2.1 Stateless Lambda Pattern

**Purpose**: Enable horizontal scaling of Lambda functions

**Implementation**:
- No local state in Lambda functions
- All state stored in DynamoDB or Managed Memory
- Each invocation is independent

**Benefits**:
- Unlimited horizontal scaling
- No state synchronization needed
- Simple deployment

---

### 2.2 Auto-Scaling Pattern

**Purpose**: Automatically scale resources based on demand

**Implementation**:
- Lambda: Auto-scales by default (no configuration)
- DynamoDB: On-demand capacity mode (auto-scaling)
- API Gateway: Auto-scales automatically

**Configuration**:
- No manual scaling configuration needed
- AWS handles scaling automatically

**Benefits**:
- No capacity planning needed
- Pay only for what you use
- Handles traffic spikes

---

### 2.3 Event-Driven Architecture Pattern

**Purpose**: Decouple components for independent scaling

**Implementation**:
```
AgentCore → EventBridge → Action Groups
```

**Benefits**:
- Components scale independently
- Loose coupling
- Easy to add new Action Groups

---

## 3. Availability Patterns

### 3.1 Retry with Exponential Backoff Pattern

**Purpose**: Handle transient failures gracefully

**Implementation**:
```python
def retry_with_backoff(operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return operation()
        except TransientError as e:
            if attempt < max_retries - 1:
                delay = 2 ** attempt  # Exponential: 1s, 2s, 4s
                time.sleep(delay)
                continue
            else:
                raise e
```

**Configuration**:
- Max retries: 3
- Backoff: Exponential (1s, 2s, 4s)
- Total max time: ~7 seconds

**Retryable Errors**:
- Timeout errors
- Service unavailable (503)
- Throttling errors (429)

**Non-Retryable Errors**:
- Validation errors (400)
- Authentication errors (401)
- Not found errors (404)

---

### 3.2 Timeout Pattern

**Purpose**: Prevent indefinite waits, fail fast

**Implementation**:
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

def with_timeout(operation, timeout_seconds):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    try:
        result = operation()
        signal.alarm(0)  # Cancel alarm
        return result
    except TimeoutError:
        # Handle timeout
        raise
```

**Timeout Configuration**:
- AgentCore: 5 seconds
- Nova Sonic: 10 seconds
- Nova Canvas: 15 seconds
- Action Groups: 3 seconds
- DynamoDB: 2 seconds

---

### 3.3 Graceful Degradation Pattern

**Purpose**: Maintain partial functionality when services fail

**Implementation**:
- If voice fails: Fall back to text-only mode
- If image fails: Continue without image analysis
- If Action Group fails: Show error, allow retry

**Example**:
```python
try:
    voice_result = process_voice(audio)
except VoiceProcessingError:
    # Degrade to text-only
    return {"mode": "text", "message": "Voice unavailable, use text"}
```

---

## 4. Security Patterns

### 4.1 Defense in Depth Pattern

**Purpose**: Multiple layers of security

**Layers**:
1. **Network**: WSS (WebSocket Secure), HTTPS only
2. **Authentication**: JWT validation on connection
3. **Authorization**: User existence check, biometric flag
4. **Data**: Encryption at rest and in transit
5. **Logging**: PII masking, audit trails

---

### 4.2 Least Privilege Pattern

**Purpose**: Grant minimum necessary permissions

**Implementation**:
- Lambda execution role: Only required permissions
- DynamoDB: Read/write only to specific tables
- S3: Access only to specific bucket
- EventBridge: Publish only to specific bus

**IAM Policy Example**:
```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:Query"
  ],
  "Resource": "arn:aws:dynamodb:*:*:table/centli-sessions"
}
```

---

### 4.3 Encryption Pattern

**Purpose**: Protect data at rest and in transit

**At Rest**:
- DynamoDB: Server-side encryption (SSE)
- S3: Default encryption (AES-256)
- Managed Memory: Bedrock handles encryption

**In Transit**:
- WebSocket: WSS (TLS 1.2+)
- API calls: HTTPS (TLS 1.2+)
- EventBridge: Encrypted by default

---

### 4.4 PII Masking Pattern

**Purpose**: Protect sensitive data in logs

**Implementation**:
```python
def mask_pii(data):
    if 'account_number' in data:
        data['account_number'] = f"******{data['account_number'][-4:]}"
    if 'email' in data:
        email = data['email']
        data['email'] = f"{email[:2]}***@{email.split('@')[1]}"
    return data
```

**Masked Fields**:
- Account numbers: Show last 4 digits
- Email: Show first 2 chars + domain
- Phone: Show last 4 digits
- Biometric: Never log

---

## 5. Reliability Patterns

### 5.1 Idempotency Pattern

**Purpose**: Safe to retry operations without side effects

**Implementation**:
- Use request_id for deduplication
- Check if operation already completed
- Return cached result if duplicate

**Example**:
```python
def process_transfer(request_id, transfer_data):
    # Check if already processed
    existing = get_transaction(request_id)
    if existing:
        return existing  # Idempotent
    
    # Process new transfer
    result = execute_transfer(transfer_data)
    store_transaction(request_id, result)
    return result
```

---

### 5.2 Request Correlation Pattern

**Purpose**: Track requests across distributed system

**Implementation**:
- Generate request_id (UUID) for each request
- Pass request_id through all components
- Log request_id in all operations
- Use request_id to correlate responses

**Flow**:
```
User Request → request_id generated
  → AgentCore (with request_id)
  → EventBridge (with request_id)
  → Action Group (with request_id)
  → Response (with request_id)
```

---

### 5.3 Structured Logging Pattern

**Purpose**: Consistent, queryable logs

**Log Format**:
```json
{
  "timestamp": "2026-02-17T10:15:30Z",
  "level": "INFO",
  "message": "Transfer completed",
  "context": {
    "user_id": "user_123",
    "session_id": "session_456",
    "request_id": "req_789",
    "operation": "transfer"
  },
  "metrics": {
    "duration_ms": 1234,
    "amount": 50000
  }
}
```

**Benefits**:
- Easy to search and filter
- Consistent across services
- Machine-readable

---

### 5.4 Health Check Pattern

**Purpose**: Monitor service health

**Implementation**:
- Lambda: CloudWatch metrics (invocations, errors, duration)
- DynamoDB: CloudWatch metrics (read/write capacity, throttles)
- API Gateway: CloudWatch metrics (requests, errors, latency)

**Monitoring**:
- Manual dashboard review during demo
- No automated alerts (hackathon simplification)

---

## 6. Maintainability Patterns

### 6.1 Configuration as Code Pattern

**Purpose**: Externalize configuration, avoid hardcoding

**Implementation**:
- Environment variables for configuration
- SAM template parameters
- No hardcoded values in code

**Example**:
```python
import os

AGENTCORE_TIMEOUT = int(os.environ.get('AGENTCORE_TIMEOUT', '5'))
DYNAMODB_TABLE = os.environ['SESSIONS_TABLE']
EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']
```

---

### 6.2 Dependency Injection Pattern

**Purpose**: Testable, flexible code

**Implementation**:
```python
class OrchestrationService:
    def __init__(self, agentcore_client, dynamodb_client, eventbridge_client):
        self.agentcore = agentcore_client
        self.dynamodb = dynamodb_client
        self.eventbridge = eventbridge_client
    
    def process_message(self, message):
        # Use injected dependencies
        session = self.dynamodb.get_session(message.session_id)
        result = self.agentcore.process(message.content)
        self.eventbridge.publish(result)
```

**Benefits**:
- Easy to test (mock dependencies)
- Flexible (swap implementations)
- Clear dependencies

---

### 6.3 Error Handling Pattern

**Purpose**: Consistent error handling across services

**Implementation**:
```python
class ServiceError(Exception):
    def __init__(self, message, error_code, retryable=False):
        self.message = message
        self.error_code = error_code
        self.retryable = retryable

def handle_error(error):
    if isinstance(error, ServiceError):
        if error.retryable:
            # Retry logic
            return retry_operation()
        else:
            # Return error to user
            return error_response(error.message, error.error_code)
    else:
        # Unexpected error
        log_error(error)
        return error_response("Internal error", "INTERNAL_ERROR")
```

---

## 7. Pattern Summary

| Pattern | Category | Purpose | Priority |
|---------|----------|---------|----------|
| Asynchronous Processing | Performance | Minimize latency | High |
| Batch Processing (Voice) | Performance | Optimize voice accuracy | High |
| Parallel Processing (Multimodal) | Performance | Reduce total latency | Medium |
| Stateless Lambda | Scalability | Enable horizontal scaling | High |
| Auto-Scaling | Scalability | Handle variable load | High |
| Retry with Backoff | Availability | Handle transient failures | High |
| Timeout | Availability | Fail fast | High |
| Defense in Depth | Security | Multiple security layers | High |
| Least Privilege | Security | Minimize permissions | High |
| Encryption | Security | Protect data | High |
| Idempotency | Reliability | Safe retries | Medium |
| Request Correlation | Reliability | Track requests | High |
| Structured Logging | Reliability | Queryable logs | Medium |
| Configuration as Code | Maintainability | Externalize config | Medium |

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Design Patterns**: 17 patterns across 7 categories for hackathon implementation

