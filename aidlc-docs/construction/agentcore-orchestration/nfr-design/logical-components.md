# Logical Components - Unit 2: AgentCore & Orchestration

## Overview

This document defines the logical infrastructure components and their configurations for implementing NFR requirements.

**Context**: AWS-native services, managed where possible, hackathon-appropriate

---

## 1. Compute Components

### 1.1 Lambda Functions

**Component**: AWS Lambda (Python 3.11)

**Functions**:
1. **app_connect** - WebSocket connection handler
2. **app_disconnect** - WebSocket disconnection handler
3. **app_message** - WebSocket message handler

**Configuration**:
```yaml
Runtime: python3.11
Memory: 512 MB (increase to 1024 MB if needed)
Timeout: 30 seconds
Environment Variables:
  - SESSIONS_TABLE: centli-sessions
  - EVENT_BUS_NAME: centli-event-bus
  - AGENTCORE_ID: centli-agent
  - LOG_LEVEL: INFO
```

**Concurrency**:
- Reserved: None (use account default)
- Provisioned: None (cold starts acceptable for demo)

**IAM Role**: `CentliLambdaExecutionRole` (from Unit 1)

---

### 1.2 Bedrock AgentCore

**Component**: AWS Bedrock AgentCore

**Configuration**:
```yaml
Agent Name: centli-agent
Foundation Model: anthropic.claude-3-7-sonnet-20250219-v1:0
Temperature: 0.7
Max Tokens: 2048
Managed Memory: Enabled
Memory Type: DynamoDB
```

**Action Groups**:
- CoreBanking (EventBridge integration)
- Marketplace (EventBridge integration)
- CRM (EventBridge integration)

**Prompts**:
- System prompt: CENTLI brand personality, Mexican Spanish
- User prompt template: Multimodal context injection

---

## 2. API Gateway Components

### 2.1 WebSocket API

**Component**: API Gateway WebSocket API

**Configuration**:
```yaml
Protocol: WSS (WebSocket Secure)
Routes:
  - $connect: app_connect Lambda
  - $disconnect: app_disconnect Lambda
  - $default: app_message Lambda
Authorization: Custom authorizer (JWT validation)
Throttling: 100 requests/minute per IP
```

**Connection Settings**:
- Idle timeout: 10 minutes
- Max message size: 128 KB
- Connection limit: 10 concurrent (demo)

**CORS**:
```yaml
AllowOrigins:
  - http://localhost:3000
  - http://localhost:8080
AllowMethods:
  - GET
  - POST
```

---

## 3. Storage Components

### 3.1 DynamoDB - Sessions Table

**Component**: DynamoDB Table

**Configuration**:
```yaml
Table Name: centli-sessions
Partition Key: session_id (String)
Capacity Mode: On-demand
TTL Attribute: expires_at
Encryption: AWS managed key
```

**Global Secondary Index**:
```yaml
Index Name: user-index
Partition Key: user_id (String)
Projection: ALL
```

**Attributes**:
- session_id (String, PK)
- user_id (String, GSI PK)
- connection_id (String)
- state (String: ACTIVE, DISCONNECTED)
- created_at (Number, timestamp)
- expires_at (Number, timestamp, TTL)
- last_activity (Number, timestamp)
- message_count (Number)
- user_preferences (Map)

---

### 3.2 Bedrock Managed Memory

**Component**: Bedrock Managed Memory (DynamoDB backend)

**Configuration**:
```yaml
Memory Type: DynamoDB
Retention: 24 hours
Max Messages: 100 per session
Auto Cleanup: Enabled
```

**Managed by**: Bedrock (no manual configuration)

---

### 3.3 S3 - Assets Bucket

**Component**: S3 Bucket (from Unit 1)

**Configuration**:
```yaml
Bucket Name: centli-assets-777937796305
Encryption: AES-256 (default)
Versioning: Disabled
Public Access: Blocked
```

**Lifecycle Policy**:
```yaml
Rules:
  - Id: DeleteImagesAfter7Days
    Status: Enabled
    Prefix: images/
    Expiration: 7 days
```

**CORS**:
```yaml
AllowedOrigins:
  - http://localhost:3000
  - http://localhost:8080
AllowedMethods:
  - GET
  - PUT
  - POST
AllowedHeaders:
  - "*"
MaxAge: 3600
```

---

## 4. Event Bus Components

### 4.1 EventBridge Event Bus

**Component**: EventBridge Event Bus (from Unit 1)

**Configuration**:
```yaml
Bus Name: centli-event-bus
Event Archive: Disabled (demo)
```

**Event Rules** (for Unit 2):
```yaml
# No rules in Unit 2 (AgentCore publishes, Action Groups subscribe)
# Rules defined in Unit 3 (Action Groups)
```

**Event Schema**:
```json
{
  "source": "centli.agentcore",
  "detail-type": "TransferRequest | PurchaseRequest | BeneficiaryQuery | ...",
  "detail": {
    "action_type": "string",
    "action_data": {},
    "user_id": "string",
    "session_id": "string",
    "request_id": "string",
    "timestamp": "ISO 8601",
    "metadata": {
      "intent_confidence": "number",
      "conversation_context": "string",
      "user_preferences": {},
      "multimodal_inputs": ["text", "voice", "image"]
    }
  }
}
```

---

## 5. AI/ML Components

### 5.1 Nova Sonic (Voice)

**Component**: AWS Bedrock Nova Sonic

**Configuration**:
```yaml
Model: amazon.nova-sonic-v1:0
Language: es-MX (Mexican Spanish)
Voice: Neutral, professional
Speaking Rate: Normal
Processing Mode: Batch
```

**Transcription**:
- Input: Audio file (WAV, MP3, OGG)
- Output: Plain text (Spanish)
- Latency: ~1-2 seconds

**Synthesis**:
- Input: Text (Spanish)
- Output: Audio file (MP3)
- Latency: ~500ms-1s

---

### 5.2 Nova Canvas (Images)

**Component**: AWS Bedrock Nova Canvas

**Configuration**:
```yaml
Model: amazon.nova-canvas-v1:0
Analysis Types:
  - Object detection
  - Text extraction (OCR)
  - Scene understanding
Confidence Threshold: 0.7
Max Objects: 10
```

**Input**:
- Image formats: JPEG, PNG
- Max size: 5 MB
- Max dimensions: 4096x4096

**Output**:
```json
{
  "objects": ["laptop", "keyboard"],
  "text": ["MacBook Pro", "$1299"],
  "scene": "product_photo",
  "confidence": 0.92
}
```

---

## 6. Monitoring Components

### 6.1 CloudWatch Logs

**Component**: CloudWatch Log Groups

**Configuration**:
```yaml
Log Groups:
  - /aws/lambda/centli-app-connect
  - /aws/lambda/centli-app-disconnect
  - /aws/lambda/centli-app-message
Retention: 7 days
Encryption: AWS managed key
```

**Log Format**: JSON structured logging

---

### 6.2 CloudWatch Metrics

**Component**: CloudWatch Metrics

**Metrics Tracked**:
- Lambda: Invocations, Errors, Duration, Throttles
- DynamoDB: Read/Write Capacity, Throttles
- API Gateway: Requests, Errors, Latency, Connection Count

**Dashboard**: Manual (no automated dashboard for hackathon)

---

## 7. Security Components

### 7.1 IAM Execution Role

**Component**: IAM Role (from Unit 1)

**Role Name**: `CentliLambdaExecutionRole`

**Policies**:
1. **AWS Managed**: `AWSLambdaBasicExecutionRole`
2. **Inline - Bedrock**:
```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeAgent",
    "bedrock:InvokeModel"
  ],
  "Resource": "*"
}
```
3. **Inline - DynamoDB**:
```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:UpdateItem",
    "dynamodb:Query"
  ],
  "Resource": [
    "arn:aws:dynamodb:*:*:table/centli-sessions",
    "arn:aws:dynamodb:*:*:table/centli-sessions/index/*"
  ]
}
```
4. **Inline - EventBridge**:
```json
{
  "Effect": "Allow",
  "Action": "events:PutEvents",
  "Resource": "arn:aws:events:*:*:event-bus/centli-event-bus"
}
```
5. **Inline - S3**:
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::centli-assets-*/*"
}
```
6. **Inline - API Gateway**:
```json
{
  "Effect": "Allow",
  "Action": "execute-api:ManageConnections",
  "Resource": "arn:aws:execute-api:*:*:*/@connections/*"
}
```

---

## 8. Component Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                        User (Browser)                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ WSS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              API Gateway WebSocket API                       │
└──────┬──────────────────┬──────────────────┬────────────────┘
       │                  │                  │
       │ $connect         │ $default         │ $disconnect
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│app_connect  │    │app_message  │    │app_disconnect│
│  Lambda     │    │  Lambda     │    │  Lambda     │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    DynamoDB (Sessions)                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Bedrock AgentCore                           │
│                  (Claude 3.7 Sonnet)                         │
└──────┬──────────────────┬──────────────────┬────────────────┘
       │                  │                  │
       │ Voice            │ Image            │ Events
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│Nova Sonic   │    │Nova Canvas  │    │EventBridge  │
└─────────────┘    └──────┬──────┘    │  Event Bus  │
                          │            └─────────────┘
                          ▼
                   ┌─────────────┐
                   │S3 (Images)  │
                   └─────────────┘
```

---

## 9. Resource Sizing

| Component | Size/Capacity | Rationale |
|-----------|---------------|-----------|
| Lambda Memory | 512 MB | Sufficient for Python + Boto3 |
| Lambda Timeout | 30 seconds | Accommodate AgentCore + Action Group calls |
| DynamoDB | On-demand | Auto-scales, pay per request |
| S3 | Unlimited | Standard object storage |
| API Gateway Connections | 10 concurrent | Demo scale |
| EventBridge | Unlimited | Managed service |

---

## 10. Component Summary

| Component | Type | Purpose | Configuration |
|-----------|------|---------|---------------|
| Lambda Functions | Compute | WebSocket handlers | Python 3.11, 512MB, 30s timeout |
| Bedrock AgentCore | AI/ML | Intent recognition, orchestration | Claude 3.7 Sonnet, Managed Memory |
| Nova Sonic | AI/ML | Voice transcription/synthesis | es-MX, batch mode |
| Nova Canvas | AI/ML | Image analysis | Object detection, OCR |
| WebSocket API | API Gateway | Real-time communication | WSS, JWT auth, 10min timeout |
| Sessions Table | DynamoDB | Session storage | On-demand, TTL enabled |
| Managed Memory | Bedrock | Conversation history | DynamoDB backend, 24h retention |
| Assets Bucket | S3 | Image storage | AES-256, 7-day lifecycle |
| Event Bus | EventBridge | Event routing | Single bus, detail-type routing |
| Log Groups | CloudWatch | Logging | 7-day retention, JSON format |
| Execution Role | IAM | Permissions | Least privilege, inline policies |

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Logical Components**: 11 component types with configurations for hackathon implementation

