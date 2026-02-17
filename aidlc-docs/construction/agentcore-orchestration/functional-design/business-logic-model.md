# Business Logic Model - Unit 2: AgentCore & Orchestration

## Overview

This document defines the business logic workflows for the AgentCore & Orchestration unit, focusing on message processing, intent recognition, multimodal handling, and event orchestration.

---

## 1. Message Processing Workflow

### 1.1 WebSocket Message Reception

```
User (Browser) 
  → WebSocket Connection 
  → API Gateway WebSocket API 
  → Lambda (app_message) 
  → Orchestration Service
```

**Process Steps**:
1. User sends message via WebSocket (text, voice, or image)
2. API Gateway receives message and invokes `app_message` Lambda
3. Lambda extracts connection_id, user_id, message payload
4. Orchestration Service validates session and authentication
5. Message is routed to appropriate processor based on type

**Business Rules**:
- All messages must have valid session_id and connection_id
- Authentication token must be validated (JWT signature + expiration + user exists + biometric verification)
- Session must be active (not expired, not disconnected)
- Message type must be one of: TEXT, VOICE, IMAGE, COMMAND

---

### 1.2 Message Type Routing

**Text Messages**:
```
Text Message → AgentCore (direct processing) → Intent Recognition
```

**Voice Messages**:
```
Voice Message → Nova Sonic (transcription) → Text → AgentCore → Intent Recognition
```
- Processing Mode: Batch (wait for complete utterance, then transcribe)
- Validation: Check format, size, duration (min/max length)

**Image Messages**:
```
Image Upload → S3 Storage → Nova Canvas (analysis) → Context → AgentCore → Intent Recognition
```
- Validation: Format, size, dimensions, basic content check
- Supported formats: JPEG, PNG (max 5MB)

**Multimodal Messages** (Voice + Image):
```
Voice + Image → Parallel Processing → Merge Results → AgentCore → Intent Recognition
```
- Both voice and image processed simultaneously
- Results merged before sending to AgentCore
- AgentCore receives enriched context from both modalities

---

## 2. Intent Recognition Logic

### 2.1 Intent Processing Flow

```
User Utterance 
  → AgentCore (Claude 3.7 Sonnet) 
  → Intent Classification 
  → Entity Extraction 
  → Confidence Scoring 
  → Decision
```

**Intent Types**:
- `TRANSFER_P2P`: P2P money transfer
- `QUERY_BALANCE`: Account balance inquiry
- `QUERY_TRANSACTIONS`: Transaction history
- `PURCHASE_PRODUCT`: Product purchase
- `QUERY_PRODUCTS`: Product catalog browsing
- `QUERY_BENEFICIARY`: Beneficiary lookup
- `ADD_BENEFICIARY`: Add new beneficiary
- `GENERAL_QUERY`: General banking questions
- `UNKNOWN`: Unrecognized intent

### 2.2 Confidence-Based Decision Logic

**High Confidence (≥ 70%)**:
- Execute intent immediately
- Proceed to Action Event generation

**Low Confidence (< 70%)**:
- Ask user for clarification
- Present clarifying question via WebSocket
- Wait for user response
- Re-process with additional context

**Ambiguous Intent**:
- Multiple intents with similar confidence
- Present options to user for selection
- User selects correct intent
- Proceed with selected intent

### 2.3 Context-Aware Disambiguation

AgentCore uses conversation context to improve intent recognition:
- Previous messages in session (from Managed Memory)
- User preferences (from session metadata)
- Recent transactions (from conversation history)
- Current conversation state (e.g., in middle of transfer flow)

**Example**:
```
User: "Envíale 50 lucas a mi hermano"
Context: Previous message identified "hermano" as "Juan Pérez"
Result: High confidence TRANSFER_P2P with beneficiary=Juan Pérez
```

---

## 3. Session Lifecycle Management

### 3.1 Session States

```
CONNECTING → ACTIVE → DISCONNECTING → DISCONNECTED
```

**CONNECTING**:
- WebSocket connection established
- Authentication in progress
- Session record created in DynamoDB

**ACTIVE**:
- User authenticated
- Session active and ready for messages
- Heartbeat monitoring active

**DISCONNECTING**:
- User initiated disconnect OR timeout detected
- Cleanup in progress
- Final state sync to Managed Memory

**DISCONNECTED**:
- Session closed
- Resources released
- Session record marked for TTL deletion

### 3.2 Session Creation (Connect Flow)

```
User Connects 
  → API Gateway (WebSocket $connect) 
  → Lambda (app_connect) 
  → Validate Auth Token 
  → Create Session (Local DynamoDB) 
  → Sync to Managed Memory 
  → Return Success
```

**Process Steps**:
1. Extract auth token from connection request
2. Validate JWT token (signature + expiration)
3. Verify user exists in DynamoDB
4. Verify biometric data (if required)
5. Create session record in local DynamoDB
6. Sync session to Bedrock Managed Memory (simultaneous write)
7. Return connection_id to client

**Session Attributes**:
- session_id (UUID)
- user_id (from token)
- connection_id (from API Gateway)
- state (ACTIVE)
- created_at (timestamp)
- expires_at (created_at + 15 minutes)
- last_activity (timestamp)
- message_count (0)
- user_preferences (from user profile)

### 3.3 Session Maintenance (Active Flow)

**Heartbeat Monitoring**:
- Client sends heartbeat every 60 seconds
- Server updates `last_activity` timestamp
- Session timeout = 15 minutes of inactivity

**Session Timeout Logic**:
```
IF (current_time - last_activity) > 15 minutes THEN
  State = DISCONNECTING
  Send timeout notification to client
  Trigger disconnect flow
END IF
```

**State Synchronization Strategy**:
- Write to local DynamoDB AND Managed Memory simultaneously (strong consistency)
- Higher latency acceptable for session state updates
- Ensures both stores always have consistent state

### 3.4 Session Termination (Disconnect Flow)

```
User Disconnects OR Timeout 
  → API Gateway (WebSocket $disconnect) 
  → Lambda (app_disconnect) 
  → Update Session State 
  → Sync Final State to Managed Memory 
  → Cleanup Resources
```

**Process Steps**:
1. Mark session state as DISCONNECTING
2. Sync final conversation state to Managed Memory
3. Mark session as DISCONNECTED
4. Set TTL for session record deletion (24 hours)
5. Release any held resources
6. Log disconnect event

---

## 4. Voice Processing Pipeline

### 4.1 Voice Input Processing

```
Audio Stream (from client) 
  → Validation (format, size, duration) 
  → Nova Sonic (transcription) 
  → Text Output 
  → AgentCore
```

**Processing Mode**: Batch
- Wait for complete audio utterance
- Transcribe entire audio at once
- Better accuracy than streaming for short utterances

**Validation Rules**:
- Format: WAV, MP3, OGG (standard audio formats)
- Size: Max 10MB per audio file
- Duration: Min 0.5 seconds, Max 60 seconds
- Language: Spanish (Mexican)

**Nova Sonic Configuration**:
- Model: Nova Sonic (AWS Bedrock)
- Language: es-MX (Mexican Spanish)
- Output: Plain text transcription

### 4.2 Voice Output Generation

```
AgentCore Response (text) 
  → Nova Sonic (synthesis) 
  → Audio Stream 
  → WebSocket (to client)
```

**Voice Characteristics**:
- Gender: Customizable (default: neutral)
- Accent: Mexican Spanish (es-MX)
- Speaking Rate: Normal (configurable)
- Tone: Professional, friendly (CENTLI brand personality)

**Nova Sonic Synthesis Configuration**:
- Model: Nova Sonic (AWS Bedrock)
- Voice: Mexican Spanish voice
- Format: MP3 (for web compatibility)
- Quality: Standard (balance between quality and latency)

---

## 5. Image Processing Pipeline

### 5.1 Image Upload and Storage

```
Image (from client) 
  → Validation (format, size, dimensions) 
  → S3 Upload (presigned URL) 
  → S3 Key 
  → Nova Canvas
```

**Validation Rules**:
- Format: JPEG, PNG only
- Size: Max 5MB
- Dimensions: Max 4096x4096 pixels
- Content: Basic content check (not empty, valid image data)

**S3 Storage**:
- Bucket: `centli-assets-{account-id}`
- Key Pattern: `images/{user_id}/{session_id}/{timestamp}_{filename}`
- Access: Private (presigned URLs for upload/download)
- Lifecycle: Delete after 7 days (temporary storage)

### 5.2 Image Analysis

```
S3 Key 
  → Nova Canvas (image analysis) 
  → Analysis Results 
  → Context Enrichment 
  → AgentCore
```

**Nova Canvas Analysis**:
- Object detection (identify products, items)
- Text extraction (OCR for product labels, prices)
- Scene understanding (context of image)
- Product matching (if applicable)

**Context Enrichment**:
- Combine image analysis with voice/text input
- Example: "¿Cuánto cuesta esto?" + [laptop image] → Product price query for laptop
- Enriched context sent to AgentCore for intent recognition

---

## 6. Action Event Publishing Logic

### 6.1 Intent to Action Event Mapping

```
Intent (from AgentCore) 
  → Action Event Schema 
  → EventBridge Publish 
  → Action Group
```

**Intent → Action Type Mapping**:
- `TRANSFER_P2P` → `TransferRequest` (CoreBanking)
- `QUERY_BALANCE` → `BalanceQuery` (CoreBanking)
- `QUERY_TRANSACTIONS` → `TransactionQuery` (CoreBanking)
- `PURCHASE_PRODUCT` → `PurchaseRequest` (Marketplace)
- `QUERY_PRODUCTS` → `ProductQuery` (Marketplace)
- `QUERY_BENEFICIARY` → `BeneficiaryQuery` (CRM)
- `ADD_BENEFICIARY` → `BeneficiaryCreate` (CRM)

### 6.2 Action Event Schema

**Comprehensive Schema** (includes full conversation context):

```json
{
  "source": "centli.agentcore",
  "detail-type": "TransferRequest | PurchaseRequest | ...",
  "detail": {
    "action_type": "TRANSFER | PURCHASE | QUERY_BENEFICIARY | ...",
    "action_data": {
      "user_id": "string",
      "amount": "number (optional)",
      "beneficiary_alias": "string (optional)",
      "product_id": "string (optional)",
      ...
    },
    "user_id": "string",
    "session_id": "string",
    "request_id": "string (UUID)",
    "timestamp": "ISO 8601",
    "metadata": {
      "intent_confidence": "number (0-1)",
      "conversation_context": "string (summary)",
      "user_preferences": {},
      "multimodal_inputs": ["text", "voice", "image"]
    }
  }
}
```

**EventBridge Routing**:
- Single event bus: `centli-event-bus`
- Routing by `detail-type` field
- Event pattern matching for each Action Group Lambda

### 6.3 Event Publishing Process

**Process Steps**:
1. AgentCore determines action required
2. Extract action data from intent entities
3. Generate unique request_id (UUID)
4. Build comprehensive event payload
5. Publish to EventBridge
6. Store request_id in session for response correlation
7. Set timeout for Action Group response (3 seconds)

---

## 7. Response Handling Logic

### 7.1 Action Group Response Reception

```
Action Group (Lambda) 
  → EventBridge (response event) 
  → AgentCore (via event subscription) 
  → Response Processing 
  → WebSocket (to client)
```

**Response Event Schema**:
```json
{
  "source": "centli.actiongroup.{name}",
  "detail-type": "ActionResponse",
  "detail": {
    "request_id": "string",
    "success": true/false,
    "result": {
      "data": {},
      "message": "string"
    },
    "error": "string (if failed)",
    "timestamp": "ISO 8601"
  }
}
```

### 7.2 Response Aggregation Strategy

**Smart Aggregation** (AgentCore decides based on intent type):

**Single Action Group** (e.g., balance query):
- Wait for single response
- Process immediately
- Send to user

**Multiple Action Groups - Sequential** (e.g., transfer with beneficiary lookup):
- CRM lookup first → get beneficiary account
- CoreBanking transfer second → execute transfer
- Process in order, each depends on previous

**Multiple Action Groups - Parallel** (e.g., product purchase with benefits):
- Marketplace calculates benefits
- CoreBanking validates balance
- Both execute in parallel
- Wait for both responses
- Aggregate results
- Send combined response to user

### 7.3 Response Timeout Handling

**Timeout**: 3 seconds per Action Group

**Timeout Logic**:
```
IF response not received within 3 seconds THEN
  Log timeout error
  Return error to user: "La operación está tardando más de lo esperado. Por favor intenta de nuevo."
  Mark request as failed
END IF
```

---

## 8. Error Handling and Retry Logic

### 8.1 AgentCore Failure Handling

**Strategy**: Queue for later processing, notify user of delay

**Process**:
1. AgentCore fails to process message
2. Message queued in DynamoDB (retry queue)
3. User notified: "Estamos procesando tu solicitud. Te notificaremos cuando esté lista."
4. Background process retries message processing
5. User notified when complete (via WebSocket if connected, or next session)

### 8.2 WebSocket Disconnect During Processing

**Strategy**: Attempt to reconnect and deliver response

**Process**:
1. Detect WebSocket disconnect
2. Continue processing message
3. Store response in session record
4. Attempt to reconnect (if client reconnects within 5 minutes)
5. Deliver stored response on reconnection
6. If no reconnection, response expires after 5 minutes

### 8.3 Retry Strategies

**Exponential Backoff**:
- Retry 1: Immediate
- Retry 2: 1 second delay
- Retry 3: 2 seconds delay
- Max retries: 3

**Circuit Breaker**:
- If AgentCore fails 5 times in 1 minute, circuit opens
- Fallback to error message for 30 seconds
- Circuit half-opens after 30 seconds (test with single request)
- Circuit closes if test succeeds

---

## 9. Security and Validation

### 9.1 Authentication Validation

**Strict Validation** (3-level check):
1. Validate JWT token signature and expiration
2. Check user exists in DynamoDB (user_profiles table)
3. Verify biometric data (if required for sensitive operations)

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

### 9.2 Input Validation

**Text Messages**:
- Max length: 1000 characters
- No malicious content (basic XSS check)
- Valid UTF-8 encoding

**Voice Messages**:
- Format: WAV, MP3, OGG
- Size: Max 10MB
- Duration: 0.5s - 60s

**Image Messages**:
- Format: JPEG, PNG
- Size: Max 5MB
- Dimensions: Max 4096x4096

### 9.3 PII Protection

**Sensitive Data Handling**:
- Account numbers masked in logs
- Biometric data never logged
- User tokens redacted in error messages
- Conversation history encrypted at rest (DynamoDB encryption)

---

## 10. Performance Considerations

### 10.1 Latency Targets

- **WebSocket Message → AgentCore**: < 500ms
- **AgentCore → Intent Recognition**: < 1s
- **Action Group Response**: < 3s
- **End-to-End (User → Response)**: < 5s

### 10.2 Optimization Strategies

**Lambda Warm-Up**:
- Provisioned concurrency for app_message Lambda
- Reduces cold start latency

**AgentCore Caching**:
- Cache frequent intents and responses
- Reduces AgentCore invocation latency

**DynamoDB Optimization**:
- Use GSI for user_id lookups
- Enable DAX for session reads (if needed)

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Business Logic Workflows**: 10 major workflows defined with detailed process steps

