# Tech Stack Decisions - Unit 2: AgentCore & Orchestration

## Overview

This document records all technology stack decisions for the AgentCore & Orchestration unit with rationale and alternatives considered.

**Context**: 8-hour hackathon, demo quality, AWS-native services preferred

---

## 1. AI/ML Orchestration

### Decision: AWS Bedrock AgentCore

**Selected**: AWS Bedrock AgentCore with Claude 3.7 Sonnet

**Rationale**:
- Full agentic capabilities (intent recognition, action orchestration, memory management)
- Native integration with Action Groups via EventBridge
- Built-in Managed Memory (conversation history)
- Native integration with Nova Sonic and Nova Canvas
- Production-ready, managed service (no infrastructure management)

**Alternatives Considered**:
- **Bedrock Converse API**: Simpler but lacks agentic capabilities, would require manual orchestration
- **Custom LLM integration**: Too complex for hackathon timeline
- **LangChain/LlamaIndex**: Adds dependency complexity, not AWS-native

**Trade-offs**:
- **Pros**: Powerful, integrated, managed
- **Cons**: Learning curve, more complex than Converse API
- **Mitigation**: Start early, use documentation, test frequently

**Configuration**:
- Model: Claude 3.7 Sonnet (balanced speed/quality)
- Temperature: 0.7 (balanced creativity/consistency)
- Max tokens: 2048 (sufficient for responses)
- Managed Memory: Enabled (DynamoDB backend)

---

## 2. Voice Processing

### Decision: AWS Bedrock Nova Sonic

**Selected**: Nova Sonic for both transcription and synthesis

**Rationale**:
- Native Bedrock integration (single SDK, consistent API)
- Supports Mexican Spanish (es-MX)
- Good quality for demo purposes
- Simpler than managing separate services
- Batch processing mode (wait for complete utterance)

**Alternatives Considered**:
- **Amazon Transcribe + Polly**: More control, but requires managing two services
- **Hybrid (Nova Sonic synthesis + Transcribe recognition)**: Unnecessary complexity
- **Third-party services**: Not AWS-native, adds dependencies

**Trade-offs**:
- **Pros**: Integrated, simple, good quality
- **Cons**: Less control than separate services
- **Mitigation**: Test early, adjust configuration if needed

**Configuration**:
- Language: es-MX (Mexican Spanish)
- Voice: Neutral gender, professional tone
- Speaking rate: Normal
- Processing mode: Batch (< 3s latency target)

---

## 3. Image Processing

### Decision: AWS Bedrock Nova Canvas

**Selected**: Nova Canvas for image analysis

**Rationale**:
- Native Bedrock integration (consistent with voice)
- Object detection, text extraction (OCR), scene understanding
- Good for product image analysis
- Simpler than Rekognition for this use case

**Alternatives Considered**:
- **Amazon Rekognition**: More features, but overkill for demo
- **Skip image processing**: Defer to later (Could Have story)
- **Third-party services**: Not AWS-native

**Trade-offs**:
- **Pros**: Integrated, sufficient features, simple
- **Cons**: Less specialized than Rekognition
- **Mitigation**: Test with sample product images

**Configuration**:
- Analysis types: Object detection, text extraction, scene understanding
- Confidence threshold: 0.7 (70%)
- Max objects: 10 per image

---

## 4. Runtime and Language

### Decision: Python 3.11

**Selected**: Python 3.11 for all Lambda functions

**Rationale**:
- Latest stable version with good AWS support
- Better performance than 3.9/3.10
- Good compatibility with Boto3 and AWS SDKs
- Widely supported libraries
- Safer than 3.12 (too new, potential compatibility issues)

**Alternatives Considered**:
- **Python 3.12**: Too new, potential compatibility issues
- **Python 3.10**: Stable but slightly older
- **Python 3.9**: Most stable but older features
- **Node.js**: Not team's primary language

**Trade-offs**:
- **Pros**: Modern, performant, stable
- **Cons**: Slightly newer than 3.10 (minimal risk)
- **Mitigation**: Test early, use well-supported libraries

**Dependencies**:
- boto3: AWS SDK (latest)
- aws-lambda-powertools: Logging, tracing utilities
- pydantic: Data validation (if needed)

---

## 5. WebSocket Communication

### Decision: API Gateway WebSocket API

**Selected**: AWS API Gateway WebSocket API

**Rationale**:
- Managed service (no server management)
- Native Lambda integration
- Built-in connection management
- Scales automatically
- Standard AWS service

**Alternatives Considered**:
- **Custom WebSocket server**: Too complex, requires infrastructure management
- **Third-party services (Pusher, Ably)**: Not AWS-native, adds cost
- **HTTP polling**: Poor UX, inefficient

**Trade-offs**:
- **Pros**: Managed, scalable, integrated
- **Cons**: Limited customization vs custom server
- **Mitigation**: Use standard patterns, test connection handling

**Configuration**:
- Routes: `$connect`, `$disconnect`, `$default`
- Authorization: Custom authorizer (JWT validation)
- Timeout: 10 minutes (idle connection)
- Message size: 128KB max

---

## 6. Data Storage

### 6.1 Session Storage

**Decision**: DynamoDB with On-Demand Capacity

**Selected**: DynamoDB table `centli-sessions`

**Rationale**:
- Fast, scalable NoSQL database
- On-demand capacity (auto-scaling, pay per request)
- TTL support (automatic session cleanup)
- GSI for user lookups
- Managed service

**Alternatives Considered**:
- **ElastiCache Redis**: Overkill for demo, adds complexity
- **RDS**: Relational not needed, slower for key-value lookups
- **S3**: Not suitable for real-time session data

**Schema**:
```
Primary Key: session_id (String)
GSI: user_id (String)
TTL: expires_at (Number)
Attributes: connection_id, state, created_at, last_activity, message_count, user_preferences
```

### 6.2 Conversation History

**Decision**: Bedrock Managed Memory

**Selected**: Bedrock Managed Memory (DynamoDB backend)

**Rationale**:
- Native AgentCore integration
- Automatic conversation history management
- DynamoDB backend (consistent with session storage)
- Managed by Bedrock (no manual management)

**Alternatives Considered**:
- **Custom DynamoDB table**: More control, but requires manual management
- **S3**: Not suitable for real-time access
- **No memory**: Poor UX, no context awareness

**Configuration**:
- Retention: 24 hours (demo purposes)
- Max messages: 100 per session
- Automatic cleanup: Enabled

### 6.3 Image Storage

**Decision**: S3 with Lifecycle Policy

**Selected**: S3 bucket `centli-assets-{account-id}`

**Rationale**:
- Standard object storage for images
- Presigned URLs for secure upload/download
- Lifecycle policy for automatic cleanup (7 days)
- Integrated with Nova Canvas

**Alternatives Considered**:
- **DynamoDB**: Not suitable for binary data
- **EFS**: Overkill for simple image storage

**Configuration**:
- Encryption: Default (AES-256)
- Lifecycle: Delete after 7 days
- CORS: Allow localhost origins
- Access: Private (presigned URLs only)

---

## 7. Event Bus

### Decision: EventBridge with Single Bus

**Selected**: EventBridge event bus `centli-event-bus`

**Rationale**:
- Standard AWS event bus service
- Single bus with detail-type routing (simple, sufficient)
- Native Lambda integration
- Event pattern matching
- Managed service

**Alternatives Considered**:
- **Multiple event buses**: Unnecessary complexity for 3 Action Groups
- **SNS/SQS**: More complex, less flexible routing
- **Direct Lambda invocation**: Tight coupling, no event history

**Trade-offs**:
- **Pros**: Simple, flexible, managed
- **Cons**: Slight latency vs direct invocation
- **Mitigation**: Acceptable latency for demo

**Routing Strategy**:
- Route by `detail-type` field
- Event patterns for each Action Group
- Single bus for all events

**Event Schema**:
```json
{
  "source": "centli.agentcore",
  "detail-type": "TransferRequest | PurchaseRequest | ...",
  "detail": {
    "action_type": "string",
    "action_data": {},
    "user_id": "string",
    "session_id": "string",
    "request_id": "string",
    "timestamp": "ISO 8601",
    "metadata": {}
  }
}
```

---

## 8. Logging and Monitoring

### Decision: CloudWatch Logs + Basic Metrics

**Selected**: CloudWatch Logs with basic CloudWatch metrics

**Rationale**:
- Standard AWS logging service
- Native Lambda integration
- Log aggregation and search
- Basic metrics included (invocations, errors, duration)
- Sufficient for demo monitoring

**Alternatives Considered**:
- **X-Ray tracing**: Adds complexity, not needed for demo
- **Custom metrics**: Not needed for demo
- **Third-party tools (Datadog, New Relic)**: Overkill, adds cost

**Trade-offs**:
- **Pros**: Simple, integrated, sufficient
- **Cons**: Basic features vs specialized tools
- **Mitigation**: Manual monitoring during demo

**Configuration**:
- Log retention: 7 days
- Log level: INFO (ERROR, WARN, INFO)
- Structured logging: JSON format
- Request ID tracking: Enabled

---

## 9. Infrastructure as Code

### Decision: AWS SAM (Serverless Application Model)

**Selected**: AWS SAM for infrastructure deployment

**Rationale**:
- Serverless-focused (Lambda, API Gateway, DynamoDB)
- Simpler than CloudFormation for serverless
- Built-in local testing (sam local)
- Single command deployment
- Already used in existing WiZi demo

**Alternatives Considered**:
- **CloudFormation**: More verbose, less serverless-focused
- **Terraform**: Not AWS-native, adds complexity
- **CDK**: More code, steeper learning curve

**Trade-offs**:
- **Pros**: Simple, serverless-focused, familiar
- **Cons**: Less flexible than CloudFormation/CDK
- **Mitigation**: Sufficient for hackathon needs

**Configuration**:
- Template: `template.yaml`
- Config: `samconfig.toml`
- Build: `sam build`
- Deploy: `sam deploy`

---

## 10. Development Tools

### 10.1 Package Management

**Decision**: Poetry

**Selected**: Poetry for Python dependency management

**Rationale**:
- Already used in existing WiZi demo
- Better dependency resolution than pip
- Lock file for reproducible builds
- Virtual environment management

**Configuration**:
- Python version: 3.11
- Dependencies: boto3, aws-lambda-powertools, pydantic

### 10.2 Code Quality

**Decision**: Minimal tooling (hackathon constraint)

**Selected**:
- PEP 8 style guide (manual adherence)
- Type hints (manual)
- No automated linting (black, flake8, mypy)
- No automated testing (pytest)

**Rationale**:
- Focus on functionality over tooling
- Manual code review sufficient for demo
- Can be added post-hackathon

---

## 11. Tech Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| AI Orchestration | AWS Bedrock AgentCore | Claude 3.7 Sonnet | Full agentic capabilities, managed |
| Voice Processing | AWS Bedrock Nova Sonic | Latest | Native integration, Mexican Spanish |
| Image Processing | AWS Bedrock Nova Canvas | Latest | Native integration, sufficient features |
| Runtime | Python | 3.11 | Modern, stable, performant |
| WebSocket API | API Gateway WebSocket | Latest | Managed, scalable, integrated |
| Session Storage | DynamoDB | On-demand | Fast, scalable, TTL support |
| Conversation Memory | Bedrock Managed Memory | Latest | Native AgentCore integration |
| Image Storage | S3 | Latest | Standard object storage |
| Event Bus | EventBridge | Latest | Flexible routing, managed |
| Logging | CloudWatch Logs | Latest | Standard AWS logging |
| Infrastructure | AWS SAM | Latest | Serverless-focused, simple |
| Package Manager | Poetry | Latest | Better than pip, lock files |

---

## 12. Decision Principles

**Guiding Principles**:
1. **AWS-Native First**: Prefer AWS services over third-party
2. **Managed Services**: Minimize infrastructure management
3. **Simplicity**: Choose simpler over more powerful when sufficient
4. **Integration**: Prefer integrated services (Bedrock ecosystem)
5. **Hackathon-Appropriate**: Balance features vs implementation time

**Trade-off Philosophy**:
- Demo quality, not production quality
- Functionality over perfection
- Speed over optimization
- Pragmatic over ideal

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Tech Stack Decisions**: 11 major decisions with rationale and alternatives

