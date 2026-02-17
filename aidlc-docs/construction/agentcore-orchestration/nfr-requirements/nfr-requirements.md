# NFR Requirements - Unit 2: AgentCore & Orchestration

## Overview

This document defines all non-functional requirements for the AgentCore & Orchestration unit, including performance, scalability, availability, security, and reliability requirements.

**Context**: 8-hour hackathon, demo quality (not production), focus on Must Have stories

---

## 1. Performance Requirements

### 1.1 Response Time Targets

| Metric | Target | Rationale |
|--------|--------|-----------|
| Voice Processing Latency | < 3 seconds | Balanced, achievable with Nova Sonic batch processing |
| End-to-End Response Time | < 5 seconds | Realistic for complex flows (voice → AgentCore → Action Group → response) |
| AgentCore Processing Timeout | 5 seconds | Fail fast approach, prevents long waits |
| Action Group Timeout | 3 seconds | Fast fail for better UX (from functional design) |
| WebSocket Message Latency | < 500ms | Near real-time for text messages |

### 1.2 Latency Breakdown

**Voice Flow** (Target: < 3 seconds):
```
User speaks (variable)
  → Audio upload: ~200ms
  → Nova Sonic transcription: ~1-2s
  → AgentCore processing: ~500ms
  → Response generation: ~300ms
Total: ~2-3 seconds
```

**End-to-End Flow** (Target: < 5 seconds):
```
User input (voice/text)
  → Orchestration Service: ~100ms
  → AgentCore processing: ~500ms
  → EventBridge publish: ~50ms
  → Action Group processing: ~1-2s
  → EventBridge response: ~50ms
  → AgentCore response generation: ~500ms
  → WebSocket delivery: ~100ms
Total: ~2.3-3.3 seconds (within 5s target)
```

### 1.3 Performance Optimization Strategies

**Lambda Optimization**:
- Use Python 3.11 (good performance, stable)
- Minimize cold starts (keep functions warm during demo)
- Optimize imports (lazy loading where possible)

**AgentCore Optimization**:
- Use Claude 3.7 Sonnet (balanced speed/quality)
- Keep prompts concise
- Cache frequent intents (if time permits)

**DynamoDB Optimization**:
- Use on-demand capacity (auto-scaling)
- Design efficient query patterns (GSI for user lookups)
- Enable DAX caching (if latency issues arise)

---

## 2. Scalability Requirements

### 2.1 Capacity Targets

| Resource | Target | Rationale |
|----------|--------|-----------|
| Concurrent WebSocket Connections | 1-10 users | Single demo session, small audience |
| Messages per Second | 10-20 msg/s | Low throughput for demo |
| Lambda Concurrency | Account default | No reserved concurrency needed for small scale |
| DynamoDB Capacity | On-demand | Auto-scaling, pay per request |

### 2.2 Scaling Strategy

**Horizontal Scaling**:
- Lambda: Auto-scales by default (no action needed)
- DynamoDB: On-demand mode handles scaling automatically
- API Gateway: Scales automatically

**Vertical Scaling**:
- Lambda memory: 512MB default (increase to 1024MB if needed)
- AgentCore: Managed service (no scaling configuration)

### 2.3 Load Expectations

**Demo Scenario**:
- 1-5 concurrent users during demo
- 2-3 messages per user per minute
- Total: 10-15 messages per minute
- Peak: 20-30 messages per minute (stress test)

**Resource Utilization**:
- Lambda invocations: ~100-200 per hour
- DynamoDB reads: ~500-1000 per hour
- DynamoDB writes: ~200-400 per hour
- S3 uploads: ~10-20 images per hour (if image feature used)

---

## 3. Availability Requirements

### 3.1 Uptime Target

**Target**: 95% uptime during demo period

**Rationale**:
- Balanced target for hackathon (some failures acceptable)
- Focus on happy path, minimal error handling
- Allows for quick fixes during demo if issues arise

**Acceptable Downtime**:
- Demo period: 8 hours
- 95% uptime = 24 minutes of acceptable downtime
- Sufficient buffer for troubleshooting and fixes

### 3.2 Error Handling Strategy

**Primary Strategy**: Retry with exponential backoff

**Retry Configuration**:
- Max retries: 3
- Backoff schedule:
  - Retry 1: Immediate
  - Retry 2: 1 second delay
  - Retry 3: 2 seconds delay
- Total max time: ~3 seconds

**Failure Scenarios**:
1. **AgentCore Failure**: Retry up to 3 times, then show error
2. **Nova Service Failure**: Retry up to 3 times, then show error
3. **Action Group Failure**: Retry up to 3 times, then show error
4. **WebSocket Disconnect**: Attempt reconnection, store response for 5 minutes

### 3.3 Fallback Mechanisms

**No Complex Fallbacks** (simplified for hackathon):
- No circuit breaker implementation
- No fallback to alternative services (e.g., Converse API)
- Simple timeout and error handling
- Clear error messages to user

**Error Messages**:
- AgentCore timeout: "El servicio está tardando más de lo esperado. Por favor intenta de nuevo."
- Action Group failure: "No pudimos completar la operación. Por favor intenta de nuevo."
- Network error: "Problema de conexión. Verifica tu red e intenta de nuevo."

### 3.4 Monitoring and Alerting

**Monitoring** (Standard):
- CloudWatch Logs for all Lambda functions
- Basic CloudWatch metrics (invocations, errors, duration)
- No X-Ray tracing (simplified for hackathon)
- No custom metrics (use defaults)

**Alerting**:
- Manual monitoring during demo (no automated alerts)
- CloudWatch dashboard for real-time visibility
- Log aggregation for troubleshooting

---

## 4. Security Requirements

### 4.1 Authentication

**Level**: Standard + Simulated Biometric

**JWT Validation**:
- Validate signature (using secret key)
- Validate expiration (`exp` claim)
- Validate required claims (`user_id`, `email`, `iat`)

**User Existence Check**:
- Query DynamoDB `centli-user-profiles` table
- Verify user record exists
- Reject if user not found

**Simulated Biometric**:
- Check `biometric_verified` flag in JWT token
- No actual biometric verification implementation
- Sufficient for demo purposes
- Can be enhanced post-hackathon if needed

**Token Structure**:
```json
{
  "user_id": "string",
  "email": "string",
  "exp": "timestamp",
  "iat": "timestamp",
  "biometric_verified": "boolean"
}
```

### 4.2 Data Encryption

**Level**: Standard (encrypt sensitive data only)

**At Rest**:
- DynamoDB: Enable encryption for `centli-sessions` table
- DynamoDB: Enable encryption for `centli-user-profiles` table
- S3: Enable default encryption for `centli-assets` bucket
- Managed Memory: Bedrock handles encryption automatically

**In Transit**:
- WebSocket: WSS (WebSocket Secure) only
- API calls: HTTPS only
- EventBridge: Encrypted by default

**Key Management**:
- Use AWS managed keys (no custom KMS keys for hackathon)
- Sufficient for demo security requirements

### 4.3 PII Protection

**Level**: Standard (mask PII in logs, encrypt sensitive fields)

**PII Masking in Logs**:
- Account numbers: Show last 4 digits only (`******7890`)
- Email addresses: Show first 2 chars + domain (`us***@example.com`)
- Phone numbers: Show last 4 digits only (`***-***-5678`)
- Biometric data: Never log

**Sensitive Field Encryption**:
- User profiles: Encrypt email, phone fields
- Sessions: Encrypt user_id, connection_id
- Conversation history: Encrypt in Managed Memory

**Compliance**:
- No formal compliance requirements for demo
- Follow AWS best practices
- Prepare for future compliance (GDPR, PCI-DSS) if needed

### 4.4 API Gateway Security

**Configuration**:
- WSS (WebSocket Secure) only
- Require authentication token in connection request
- Rate limiting: 100 requests per minute per IP (default)
- CORS: Allow localhost origins only (for demo)

**Authorization**:
- Token validation on `$connect` route
- Reject invalid tokens immediately
- No authorization on `$disconnect` (cleanup only)
- Token validation on `$default` route (message handler)

---

## 5. Reliability Requirements

### 5.1 Retry Strategy

**Configuration**: Simple retries with fixed delay

**Retry Logic**:
```python
max_retries = 3
retry_delay = 1  # second

for attempt in range(max_retries):
    try:
        result = operation()
        return result
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
            continue
        else:
            raise e
```

**Retryable Operations**:
- AgentCore invocations
- Nova Sonic/Canvas API calls
- DynamoDB operations
- EventBridge publish operations

**Non-Retryable Errors**:
- Validation errors (400 Bad Request)
- Authentication errors (401 Unauthorized)
- Authorization errors (403 Forbidden)
- Not found errors (404 Not Found)

### 5.2 Circuit Breaker

**Implementation**: No circuit breaker (simplified for hackathon)

**Rationale**:
- Circuit breaker adds complexity
- Simple timeout and error handling sufficient for demo
- Can be added post-hackathon if needed

**Alternative**: Simple timeout handling
- Set timeout for all external service calls
- Fail fast if timeout exceeded
- Log timeout errors for analysis

### 5.3 Timeout Configuration

| Service | Timeout | Rationale |
|---------|---------|-----------|
| AgentCore | 5 seconds | Fail fast approach |
| Nova Sonic | 10 seconds | Voice processing can take longer |
| Nova Canvas | 15 seconds | Image analysis can take longer |
| Action Groups | 3 seconds | Fast fail for better UX |
| DynamoDB | 2 seconds | Database should be fast |
| EventBridge | 1 second | Event publish should be fast |

### 5.4 Error Logging

**Strategy**: Standard (CloudWatch Logs + basic metrics)

**Log Levels**:
- ERROR: Failures, exceptions, timeouts
- WARN: Retries, slow operations, degraded performance
- INFO: Successful operations, key events
- DEBUG: Detailed execution flow (disabled in production)

**Log Format**:
```json
{
  "timestamp": "ISO 8601",
  "level": "ERROR|WARN|INFO|DEBUG",
  "message": "Human-readable message",
  "context": {
    "user_id": "string",
    "session_id": "string",
    "request_id": "string",
    "operation": "string"
  },
  "error": {
    "type": "string",
    "message": "string",
    "stack_trace": "string"
  }
}
```

**Metrics**:
- Lambda invocations (count)
- Lambda errors (count)
- Lambda duration (milliseconds)
- DynamoDB read/write capacity (units)
- API Gateway requests (count)
- API Gateway errors (count)

---

## 6. Maintainability Requirements

### 6.1 Code Quality

**Standards**:
- PEP 8 style guide for Python
- Type hints for function signatures
- Docstrings for all functions and classes
- Comments for complex logic

**Testing**:
- Unit tests for business logic (if time permits)
- Integration tests for critical flows (manual during demo)
- No automated test suite (hackathon constraint)

### 6.2 Documentation

**Required Documentation**:
- README with setup instructions
- API documentation (OpenAPI schemas for Action Groups)
- Deployment guide (SAM commands)
- Troubleshooting guide (common issues and fixes)

**Code Documentation**:
- Inline comments for complex logic
- Function docstrings with parameters and return values
- Module-level docstrings with purpose and usage

### 6.3 Operational Requirements

**Deployment**:
- SAM CLI for infrastructure deployment
- Single command deployment (`sam deploy`)
- Environment variables for configuration
- No manual configuration steps

**Monitoring**:
- CloudWatch dashboard for key metrics
- Log aggregation for troubleshooting
- Manual monitoring during demo

**Troubleshooting**:
- Clear error messages in logs
- Request ID tracking for correlation
- Session ID tracking for user flows

---

## 7. Usability Requirements

### 7.1 User Experience

**Response Time Perception**:
- < 1 second: Instant (text messages)
- 1-3 seconds: Fast (voice processing)
- 3-5 seconds: Acceptable (complex operations)
- > 5 seconds: Slow (show loading indicator)

**Error Handling UX**:
- Clear, user-friendly error messages (Spanish)
- No technical jargon in user-facing errors
- Actionable guidance ("intenta de nuevo", "verifica tu red")

**Voice UX**:
- Natural, conversational responses
- Mexican Spanish accent and vocabulary
- Professional, friendly tone (CENTLI brand)

### 7.2 Accessibility

**Not Required for Hackathon Demo**:
- Screen reader support
- Keyboard navigation
- High contrast mode
- Accessibility compliance (WCAG)

**Future Enhancement**:
- Can be added post-hackathon
- Important for production deployment

---

## 8. NFR Summary

### 8.1 Key Requirements

| Category | Requirement | Target | Priority |
|----------|-------------|--------|----------|
| Performance | Voice latency | < 3s | High |
| Performance | End-to-end response | < 5s | High |
| Scalability | Concurrent users | 1-10 | Medium |
| Availability | Uptime | 95% | Medium |
| Security | Authentication | Standard + simulated biometric | High |
| Security | Encryption | Standard (sensitive data) | Medium |
| Reliability | Retry strategy | 3 retries with fixed delay | High |
| Reliability | Error logging | CloudWatch Logs + basic metrics | Medium |

### 8.2 Trade-offs

**Simplified for Hackathon**:
- No circuit breaker (simple timeout instead)
- No fallback services (retry only)
- No automated alerts (manual monitoring)
- No comprehensive testing (manual testing)
- Simulated biometric (no actual verification)

**Rationale**:
- 8-hour timeline requires pragmatic choices
- Focus on Must Have stories
- Demo quality, not production quality
- Can be enhanced post-hackathon

### 8.3 Risk Mitigation

**High-Risk Areas**:
1. **AgentCore complexity**: Mitigated by starting early, testing frequently
2. **Voice latency**: Mitigated by batch processing, realistic targets
3. **Integration complexity**: Mitigated by clear contracts, early integration testing

**Contingency Plans**:
- If AgentCore issues: Simplify prompts, reduce complexity
- If voice latency issues: Increase timeout, optimize processing
- If integration issues: Test individual components, fix incrementally

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**NFR Requirements**: 8 categories with specific targets and rationale for hackathon context

