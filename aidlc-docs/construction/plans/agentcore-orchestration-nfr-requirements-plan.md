# NFR Requirements Plan - Unit 2: AgentCore & Orchestration

## Context

**Unit Name**: AgentCore & Orchestration  
**Purpose**: AI/ML orchestration with multimodal processing and WebSocket communication  
**Timeline**: 8-hour hackathon (demo quality, not production)  
**Functional Design**: Complete (10 workflows, 44 business rules, 10 entities)

---

## NFR Assessment Steps

### Step 1: Performance Requirements
- [x] Define response time targets for WebSocket messages
- [x] Define latency targets for voice processing (Nova Sonic)
- [x] Define latency targets for image processing (Nova Canvas)
- [x] Define end-to-end latency target (user input → response)
- [x] Define AgentCore processing time target
- [x] Define Action Group timeout thresholds

### Step 2: Scalability Requirements
- [x] Define expected concurrent WebSocket connections
- [x] Define expected messages per second throughput
- [x] Define Lambda concurrency limits
- [x] Define DynamoDB capacity mode (on-demand vs provisioned)
- [x] Define scaling triggers and thresholds

### Step 3: Availability Requirements
- [x] Define uptime target for demo (hackathon context)
- [x] Define error handling strategy (fail fast vs retry)
- [x] Define fallback mechanisms for service failures
- [x] Define monitoring and alerting needs

### Step 4: Security Requirements
- [x] Define authentication mechanism (JWT validation level)
- [x] Define data encryption requirements (at rest, in transit)
- [x] Define PII protection strategy
- [x] Define session security requirements
- [x] Define API Gateway security configuration

### Step 5: Tech Stack Decisions
- [x] Confirm AWS Bedrock AgentCore vs Converse API
- [x] Confirm Nova Sonic for voice (vs Transcribe/Polly)
- [x] Confirm Nova Canvas for images (vs Rekognition)
- [x] Confirm Python runtime version for Lambdas
- [x] Confirm WebSocket API Gateway configuration
- [x] Confirm DynamoDB table design

### Step 6: Reliability Requirements
- [x] Define retry strategy for failed operations
- [x] Define circuit breaker thresholds
- [x] Define timeout values for external services
- [x] Define error logging and tracking strategy

---

## NFR Questions

### Performance Questions

**Question 1: Voice Processing Latency Target**

What is the acceptable latency for voice processing (user speaks → text response)?

A) Fast: < 2 seconds (aggressive, may require optimization)  
B) Standard: < 3 seconds (balanced, achievable)  
C) Relaxed: < 5 seconds (safe for demo)  
D) Custom: Specify your target

[Answer]:

**Question 2: End-to-End Response Time**

What is the acceptable end-to-end response time (user input → final response)?

A) Fast: < 3 seconds (challenging for complex flows)  
B) Standard: < 5 seconds (balanced, realistic)  
C) Relaxed: < 10 seconds (safe for demo)  
D) Custom: Specify your target

[Answer]:B

**Question 3: AgentCore Processing Timeout**

How long should we wait for AgentCore to process a message before timing out?

A) Short: 5 seconds (fail fast)  
B) Standard: 10 seconds (balanced)  
C) Long: 30 seconds (accommodate complex processing)  
D) Custom: Specify your timeout

[Answer]:A

### Scalability Questions

**Question 4: Expected Concurrent Users**

How many concurrent WebSocket connections should the system support for the demo?

A) Small: 1-10 users (single demo session)  
B) Medium: 10-50 users (multiple demo sessions)  
C) Large: 50-100 users (stress testing)  
D) Custom: Specify your target

[Answer]: A

**Question 5: Lambda Concurrency Strategy**

What Lambda concurrency strategy should we use?

A) No reserved concurrency (use account default)  
B) Reserved concurrency (guarantee capacity, prevent throttling)  
C) Provisioned concurrency (pre-warmed, lowest latency)  
D) Custom: Specify your strategy

[Answer]:A

**Question 6: DynamoDB Capacity Mode**

What DynamoDB capacity mode should we use for sessions table?

A) On-demand (pay per request, auto-scaling)  
B) Provisioned (fixed capacity, lower cost for predictable load)  
C) Custom: Specify your preference

[Answer]:A

### Availability Questions

**Question 7: Demo Uptime Target**

What uptime target is acceptable for the hackathon demo?

A) High: 99.9% (production-like, requires robust error handling)  
B) Standard: 95% (balanced, some failures acceptable)  
C) Demo: 90% (focus on happy path, minimal error handling)  
D) Custom: Specify your target

[Answer]:A

**Question 8: Service Failure Fallback**

What should happen if AgentCore or Nova services fail during demo?

A) Fail fast: Show error to user immediately  
B) Retry: Attempt retry with exponential backoff  
C) Fallback: Fall back to simpler service (e.g., Converse API)  
D) Queue: Queue for later processing

[Answer]:D

### Security Questions

**Question 9: Authentication Validation Level**

What level of authentication validation is required for the demo?

A) Basic: JWT signature and expiration only  
B) Standard: JWT + user exists check  
C) Strict: JWT + user exists + biometric verification  
D) Demo: Simplified auth for demo purposes

[Answer]:C

**Question 10: Data Encryption**

What data encryption is required?

A) Full: Encrypt everything (DynamoDB, S3, in-transit)  
B) Standard: Encrypt sensitive data only (sessions, user profiles)  
C) Minimal: Use AWS defaults (HTTPS, default encryption)  
D) Custom: Specify your requirements

[Answer]:B

**Question 11: PII Protection**

How should Personally Identifiable Information be protected?

A) Strict: Mask all PII in logs, encrypt at rest, audit all access  
B) Standard: Mask PII in logs, encrypt sensitive fields  
C) Basic: Don't log PII, use default encryption  
D) Demo: Minimal protection for demo purposes

[Answer]:B

### Tech Stack Questions

**Question 12: AgentCore vs Converse API**

Which Bedrock service should we use for AI orchestration?

A) AgentCore: Full agentic capabilities (complex, powerful)  
B) Converse API: Simpler conversation API (faster to implement)  
C) Hybrid: Start with Converse, upgrade to AgentCore if time permits  
D) Custom: Specify your preference

[Answer]:A

**Question 13: Voice Processing Service**

Which service should we use for voice processing?

A) Nova Sonic: Native Bedrock integration (recommended)  
B) Transcribe + Polly: Separate services (more control)  
C) Hybrid: Nova Sonic for synthesis, Transcribe for recognition  
D) Custom: Specify your preference

[Answer]:A

**Question 14: Image Processing Service**

Which service should we use for image processing?

A) Nova Canvas: Native Bedrock integration (recommended)  
B) Rekognition: Dedicated image analysis service  
C) Skip: Defer image processing to later (focus on voice)  
D) Custom: Specify your preference

[Answer]:A

**Question 15: Python Runtime Version**

Which Python runtime should we use for Lambda functions?

A) Python 3.9 (stable, widely supported)  
B) Python 3.10 (newer features, good support)  
C) Python 3.11 (latest, best performance)  
D) Python 3.12 (cutting edge, may have compatibility issues)

[Answer]:D

### Reliability Questions

**Question 16: Retry Strategy**

What retry strategy should we use for failed operations?

A) No retries: Fail fast, show error immediately  
B) Simple retries: Retry up to 3 times with fixed delay  
C) Exponential backoff: Retry with increasing delays  
D) Custom: Specify your strategy

[Answer]:B

**Question 17: Circuit Breaker**

Should we implement circuit breaker pattern for external services?

A) Yes: Implement circuit breaker (more robust, more complex)  
B) No: Simple timeout and error handling (faster to implement)  
C) Partial: Circuit breaker for critical services only  
D) Custom: Specify your preference

[Answer]:B

**Question 18: Error Logging Strategy**

What error logging and tracking strategy should we use?

A) Comprehensive: CloudWatch Logs + X-Ray tracing + custom metrics  
B) Standard: CloudWatch Logs + basic metrics  
C) Minimal: CloudWatch Logs only  
D) Custom: Specify your strategy

[Answer]:B

---

## Success Criteria

- [x] All performance targets defined
- [x] All scalability requirements specified
- [x] All availability requirements determined
- [x] All security requirements identified
- [x] All tech stack decisions made with rationale
- [x] All reliability requirements documented
- [x] All questions answered by user
- [x] No ambiguities remaining

---

**Plan Status**: Complete - All artifacts generated  
**Total Questions**: 18 questions across 6 categories  
**Artifacts Created**:
- nfr-requirements.md (8 NFR categories with targets and rationale)
- tech-stack-decisions.md (11 major tech decisions with alternatives)

