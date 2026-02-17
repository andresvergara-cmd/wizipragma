# Business Rules - Unit 2: AgentCore & Orchestration

## Overview

This document defines all business rules, validation logic, and constraints for the AgentCore & Orchestration unit.

---

## 1. Authentication and Authorization Rules

### Rule 1.1: Token Validation
**Rule**: All WebSocket connections MUST provide a valid JWT token

**Validation Steps**:
1. Token signature MUST be valid (signed with correct secret)
2. Token MUST NOT be expired (`exp` claim > current time)
3. Token MUST contain required claims: `user_id`, `email`, `exp`, `iat`

**Violation Action**: Reject connection with 401 Unauthorized

---

### Rule 1.2: User Existence Validation
**Rule**: User referenced in token MUST exist in system

**Validation Steps**:
1. Extract `user_id` from token
2. Query DynamoDB `centli-user-profiles` table
3. User record MUST exist

**Violation Action**: Reject connection with 403 Forbidden

---

### Rule 1.3: Biometric Verification (Sensitive Operations)
**Rule**: Sensitive operations REQUIRE biometric verification

**Sensitive Operations**:
- P2P transfers > $1000 MXN
- Beneficiary modifications
- Account settings changes

**Validation Steps**:
1. Check token claim `biometric_verified` = true
2. Verify biometric timestamp < 5 minutes old

**Violation Action**: Request biometric re-authentication

---

## 2. Session Management Rules

### Rule 2.1: Session Timeout
**Rule**: Sessions MUST timeout after 15 minutes of inactivity

**Implementation**:
- Track `last_activity` timestamp on every message
- Background process checks for inactive sessions every 60 seconds
- If `(current_time - last_activity) > 15 minutes`, trigger disconnect

**User Notification**: "Tu sesión ha expirado por inactividad. Por favor reconecta."

---

### Rule 2.2: Session Expiration
**Rule**: Sessions MUST have absolute expiration time

**Implementation**:
- Set `expires_at` = `created_at` + 4 hours (absolute maximum)
- Even with activity, session cannot exceed 4 hours
- Force disconnect at expiration

**User Notification**: "Tu sesión ha alcanzado el tiempo máximo. Por favor reconecta."

---

### Rule 2.3: Concurrent Session Limit
**Rule**: Users MAY have multiple concurrent sessions (no limit for hackathon)

**Rationale**: Allow users to connect from multiple devices simultaneously

**Future Enhancement**: Add configurable limit (e.g., max 3 concurrent sessions)

---

### Rule 2.4: Session State Consistency
**Rule**: Session state MUST be consistent between local DynamoDB and Managed Memory

**Implementation**:
- Write to both stores simultaneously (strong consistency)
- If either write fails, rollback both
- Retry failed writes up to 3 times

**Violation Action**: Log error, mark session as inconsistent, force disconnect

---

## 3. Intent Recognition Rules

### Rule 3.1: Confidence Threshold
**Rule**: Intents with confidence < 70% MUST request clarification

**Implementation**:
```
IF intent_confidence < 0.70 THEN
  Ask clarifying question
  Wait for user response
  Re-process with additional context
ELSE
  Execute intent
END IF
```

**Clarifying Question Examples**:
- "¿Quieres hacer una transferencia o consultar tu saldo?"
- "¿Te refieres a comprar un producto o ver el catálogo?"

---

### Rule 3.2: Ambiguous Intent Handling
**Rule**: When multiple intents have similar confidence (within 10%), present options

**Implementation**:
```
IF (intent1_confidence - intent2_confidence) < 0.10 THEN
  Present both options to user
  User selects correct intent
ELSE
  Use highest confidence intent
END IF
```

**Example**:
```
User: "Quiero ver mi cuenta"
Intents: QUERY_BALANCE (65%), QUERY_TRANSACTIONS (62%)
Response: "¿Quieres ver tu saldo o tus transacciones?"
```

---

### Rule 3.3: Unknown Intent Fallback
**Rule**: Unknown intents MUST trigger general help response

**Implementation**:
```
IF intent_type = UNKNOWN THEN
  Provide general help message
  Suggest common actions
END IF
```

**Help Message**:
"No entendí tu solicitud. Puedo ayudarte con:
- Transferencias P2P
- Consulta de saldo
- Compra de productos
- Gestión de beneficiarios"

---

### Rule 3.4: Context-Aware Intent Resolution
**Rule**: Use conversation context to improve intent recognition

**Context Sources**:
1. Previous messages in session (last 10 messages)
2. User preferences (from profile)
3. Recent transactions (last 24 hours)
4. Current conversation state (e.g., in transfer flow)

**Example**:
```
Message 1: "Quiero hacer una transferencia"
Message 2: "A mi hermano" (context: transfer in progress)
Result: Resolve "hermano" to beneficiary using CRM
```

---

## 4. Voice Processing Rules

### Rule 4.1: Audio Format Validation
**Rule**: Only accept standard audio formats

**Allowed Formats**: WAV, MP3, OGG

**Validation**:
- Check file extension
- Verify MIME type
- Validate audio header

**Violation Action**: Reject with error "Formato de audio no soportado. Usa WAV, MP3 u OGG."

---

### Rule 4.2: Audio Size Limit
**Rule**: Audio files MUST NOT exceed 10MB

**Rationale**: Prevent abuse, ensure reasonable processing time

**Violation Action**: Reject with error "Audio demasiado grande. Máximo 10MB."

---

### Rule 4.3: Audio Duration Limits
**Rule**: Audio duration MUST be between 0.5 and 60 seconds

**Rationale**:
- Min 0.5s: Avoid empty or too-short audio
- Max 60s: Keep utterances concise, prevent abuse

**Violation Action**: 
- Too short: "Audio demasiado corto. Habla por al menos medio segundo."
- Too long: "Audio demasiado largo. Máximo 60 segundos."

---

### Rule 4.4: Language Detection
**Rule**: Voice input MUST be in Spanish (Mexican)

**Implementation**:
- Nova Sonic configured for es-MX
- If language detection fails, return error

**Violation Action**: "No pude entender el audio. Por favor habla en español."

---

### Rule 4.5: Voice Quality Check
**Rule**: Perform basic quality validation on audio

**Checks**:
- Audio is not silent (has audio data)
- Audio is not corrupted (valid audio stream)
- Audio has reasonable volume level

**Violation Action**: "Audio no válido. Por favor graba de nuevo."

---

## 5. Image Processing Rules

### Rule 5.1: Image Format Validation
**Rule**: Only accept JPEG and PNG formats

**Allowed Formats**: JPEG (.jpg, .jpeg), PNG (.png)

**Validation**:
- Check file extension
- Verify MIME type (image/jpeg, image/png)
- Validate image header

**Violation Action**: Reject with error "Formato de imagen no soportado. Usa JPEG o PNG."

---

### Rule 5.2: Image Size Limit
**Rule**: Images MUST NOT exceed 5MB

**Rationale**: Balance between quality and upload/processing time

**Violation Action**: Reject with error "Imagen demasiado grande. Máximo 5MB."

---

### Rule 5.3: Image Dimension Limits
**Rule**: Images MUST NOT exceed 4096x4096 pixels

**Rationale**: Prevent excessive processing time, reasonable for mobile photos

**Violation Action**: Reject with error "Imagen demasiado grande. Máximo 4096x4096 píxeles."

---

### Rule 5.4: Image Content Validation
**Rule**: Perform basic content check on images

**Checks**:
- Image is not empty (has pixel data)
- Image is not corrupted (valid image data)
- Image has reasonable dimensions (min 100x100)

**Violation Action**: "Imagen no válida. Por favor sube una imagen válida."

---

### Rule 5.5: Image Storage Lifecycle
**Rule**: Uploaded images MUST be deleted after 7 days

**Implementation**:
- S3 lifecycle policy: Delete objects after 7 days
- Temporary storage for demo purposes only

**Rationale**: Reduce storage costs, images only needed for immediate processing

---

## 6. Action Event Rules

### Rule 6.1: Request ID Uniqueness
**Rule**: Every action event MUST have a unique request_id

**Implementation**:
- Generate UUID v4 for each request
- Store request_id in session for response correlation
- Prevent duplicate processing

**Violation Action**: Log error, reject duplicate request

---

### Rule 6.2: Event Schema Validation
**Rule**: All action events MUST conform to schema

**Required Fields**:
- `source`: "centli.agentcore"
- `detail-type`: Valid action type
- `detail.action_type`: Valid action
- `detail.user_id`: Valid user ID
- `detail.session_id`: Valid session ID
- `detail.request_id`: Unique UUID
- `detail.timestamp`: ISO 8601 timestamp

**Violation Action**: Log error, reject malformed event

---

### Rule 6.3: Event Routing by Detail-Type
**Rule**: EventBridge MUST route events by `detail-type` field

**Routing Rules**:
- `TransferRequest` → CoreBanking Lambda
- `BalanceQuery` → CoreBanking Lambda
- `TransactionQuery` → CoreBanking Lambda
- `PurchaseRequest` → Marketplace Lambda
- `ProductQuery` → Marketplace Lambda
- `BeneficiaryQuery` → CRM Lambda
- `BeneficiaryCreate` → CRM Lambda

**Violation Action**: Event not routed, log error

---

### Rule 6.4: Event Metadata Inclusion
**Rule**: Events MUST include comprehensive metadata

**Required Metadata**:
- `intent_confidence`: Confidence score (0-1)
- `conversation_context`: Summary of conversation
- `user_preferences`: User preferences object
- `multimodal_inputs`: Array of input types used

**Rationale**: Provide Action Groups with full context for better decision-making

---

## 7. Response Handling Rules

### Rule 7.1: Response Timeout
**Rule**: Action Group responses MUST arrive within 3 seconds

**Implementation**:
- Set timeout timer when publishing event
- If no response within 3 seconds, trigger timeout handler

**Timeout Action**: Return error to user "La operación está tardando más de lo esperado. Por favor intenta de nuevo."

---

### Rule 7.2: Response Correlation
**Rule**: Responses MUST be correlated to requests via request_id

**Implementation**:
- Store request_id in session when publishing event
- Match response request_id to stored request_id
- Reject responses with unknown request_id

**Violation Action**: Log error, discard orphaned response

---

### Rule 7.3: Response Aggregation Strategy
**Rule**: AgentCore decides aggregation strategy based on intent type

**Single Action Group Intents**:
- QUERY_BALANCE → Wait for CoreBanking only
- QUERY_PRODUCTS → Wait for Marketplace only

**Sequential Multi-Action Intents**:
- TRANSFER_P2P → CRM first (beneficiary), then CoreBanking (transfer)

**Parallel Multi-Action Intents**:
- PURCHASE_PRODUCT → Marketplace (benefits) + CoreBanking (balance) in parallel

**Implementation**: AgentCore orchestrates based on intent type configuration

---

### Rule 7.4: Error Response Handling
**Rule**: Action Group errors MUST be translated to user-friendly messages

**Error Translation**:
- `INSUFFICIENT_FUNDS` → "No tienes saldo suficiente para esta operación."
- `BENEFICIARY_NOT_FOUND` → "No encontré a ese beneficiario. ¿Puedes ser más específico?"
- `PRODUCT_NOT_AVAILABLE` → "Ese producto no está disponible en este momento."
- `INVALID_AMOUNT` → "El monto no es válido. Por favor verifica."

**Rationale**: Technical errors should not be exposed to users

---

## 8. Error Handling and Retry Rules

### Rule 8.1: AgentCore Failure Retry
**Rule**: AgentCore failures MUST be queued for retry

**Implementation**:
1. On AgentCore failure, store message in retry queue (DynamoDB)
2. Notify user: "Estamos procesando tu solicitud. Te notificaremos cuando esté lista."
3. Background process retries every 30 seconds
4. Max retries: 3
5. If all retries fail, notify user of permanent failure

**Permanent Failure Message**: "No pudimos procesar tu solicitud. Por favor intenta de nuevo más tarde."

---

### Rule 8.2: Exponential Backoff
**Rule**: Retries MUST use exponential backoff

**Backoff Schedule**:
- Retry 1: Immediate
- Retry 2: 1 second delay
- Retry 3: 2 seconds delay
- Retry 4: 4 seconds delay (if applicable)

**Rationale**: Avoid overwhelming failing services

---

### Rule 8.3: Circuit Breaker
**Rule**: Implement circuit breaker for AgentCore failures

**Circuit States**:
- **CLOSED**: Normal operation
- **OPEN**: Too many failures, reject requests immediately
- **HALF-OPEN**: Test with single request after cooldown

**Thresholds**:
- Open circuit: 5 failures in 1 minute
- Cooldown period: 30 seconds
- Half-open test: 1 request

**Open Circuit Action**: Return error "El servicio está temporalmente no disponible. Por favor intenta en unos momentos."

---

### Rule 8.4: WebSocket Disconnect Handling
**Rule**: Continue processing if WebSocket disconnects during message processing

**Implementation**:
1. Detect disconnect
2. Continue processing message
3. Store response in session record
4. If client reconnects within 5 minutes, deliver stored response
5. If no reconnection, response expires

**Reconnection Message**: "Tienes una respuesta pendiente: [response]"

---

## 9. Data Validation Rules

### Rule 9.1: Text Message Validation
**Rule**: Text messages MUST meet length and content requirements

**Validation**:
- Min length: 1 character
- Max length: 1000 characters
- Valid UTF-8 encoding
- No malicious content (basic XSS check)

**Violation Action**: Reject with appropriate error message

---

### Rule 9.2: Session ID Validation
**Rule**: All messages MUST reference a valid, active session

**Validation**:
1. session_id MUST exist in DynamoDB
2. Session state MUST be ACTIVE
3. Session MUST NOT be expired

**Violation Action**: Reject with 403 Forbidden, "Sesión inválida o expirada."

---

### Rule 9.3: User ID Validation
**Rule**: user_id in message MUST match session owner

**Validation**:
- Extract user_id from message
- Compare to session.user_id
- MUST match exactly

**Violation Action**: Reject with 403 Forbidden, "Usuario no autorizado."

---

## 10. Performance and Scalability Rules

### Rule 10.1: Lambda Concurrency Limits
**Rule**: Set reserved concurrency for critical Lambdas

**Concurrency Limits**:
- app_message: 100 concurrent executions
- app_connect: 50 concurrent executions
- app_disconnect: 50 concurrent executions

**Rationale**: Prevent Lambda throttling during high load

---

### Rule 10.2: DynamoDB Throughput
**Rule**: Use on-demand capacity mode for DynamoDB tables

**Rationale**: Hackathon demo with unpredictable load patterns

**Tables**:
- centli-sessions: On-demand
- centli-user-profiles: On-demand

---

### Rule 10.3: S3 Upload Rate Limiting
**Rule**: Limit image uploads to 10 per minute per user

**Implementation**:
- Track upload count in session metadata
- Reset counter every minute
- Reject uploads exceeding limit

**Violation Action**: "Has alcanzado el límite de subidas. Por favor espera un momento."

---

### Rule 10.4: AgentCore Rate Limiting
**Rule**: Limit AgentCore invocations to prevent abuse

**Limits**:
- Max 30 messages per minute per user
- Max 100 messages per hour per user

**Implementation**:
- Track message count in session metadata
- Reject messages exceeding limits

**Violation Action**: "Has enviado demasiados mensajes. Por favor espera un momento."

---

## 11. Security Rules

### Rule 11.1: PII Masking in Logs
**Rule**: Personally Identifiable Information MUST be masked in logs

**PII Fields to Mask**:
- Account numbers (show last 4 digits only)
- Email addresses (show first 2 chars + domain)
- Phone numbers (show last 4 digits only)
- Biometric data (never log)

**Example**: 
- Account: `1234567890` → `******7890`
- Email: `user@example.com` → `us***@example.com`

---

### Rule 11.2: Token Redaction
**Rule**: JWT tokens MUST be redacted in error messages and logs

**Implementation**:
- Never log full token
- Log token prefix only (first 10 chars)
- Redact token in error responses

**Example**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` → `eyJhbGciOi***`

---

### Rule 11.3: Conversation History Encryption
**Rule**: Conversation history MUST be encrypted at rest

**Implementation**:
- Enable DynamoDB encryption for sessions table
- Enable S3 encryption for image storage
- Use AWS KMS for key management

**Rationale**: Protect sensitive financial conversations

---

### Rule 11.4: HTTPS Only
**Rule**: All WebSocket connections MUST use WSS (WebSocket Secure)

**Implementation**:
- API Gateway configured for WSS only
- Reject WS (non-secure) connections

**Violation Action**: Connection refused

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Business Rules**: 44 rules across 11 categories with validation logic and violation actions

