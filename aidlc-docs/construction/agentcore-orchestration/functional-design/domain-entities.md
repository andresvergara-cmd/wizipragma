# Domain Entities - Unit 2: AgentCore & Orchestration

## Overview

This document defines all domain entities, their attributes, relationships, and data structures for the AgentCore & Orchestration unit.

---

## 1. Session Entity

### 1.1 Purpose
Represents an active WebSocket connection session between a user and the CENTLI system.

### 1.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | String (UUID) | Yes | Unique session identifier |
| `user_id` | String | Yes | User identifier (from auth token) |
| `connection_id` | String | Yes | API Gateway WebSocket connection ID |
| `state` | Enum | Yes | Session state: CONNECTING, ACTIVE, DISCONNECTING, DISCONNECTED |
| `created_at` | Timestamp (ISO 8601) | Yes | Session creation timestamp |
| `expires_at` | Timestamp (ISO 8601) | Yes | Session expiration timestamp (created_at + 4 hours) |
| `last_activity` | Timestamp (ISO 8601) | Yes | Last message/activity timestamp |
| `message_count` | Integer | Yes | Total messages in session |
| `user_preferences` | Object | No | User preferences (language, voice settings, etc.) |

### 1.3 Entity Structure

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_12345",
  "connection_id": "abc123xyz",
  "state": "ACTIVE",
  "created_at": "2026-02-17T10:00:00Z",
  "expires_at": "2026-02-17T14:00:00Z",
  "last_activity": "2026-02-17T10:15:30Z",
  "message_count": 5,
  "user_preferences": {
    "language": "es-MX",
    "voice_gender": "neutral",
    "voice_speed": "normal"
  }
}
```

### 1.4 Storage
- **Primary Store**: DynamoDB table `centli-sessions`
- **Key**: `session_id` (partition key)
- **GSI**: `user_id` (for user session lookup)
- **TTL**: `expires_at` (automatic cleanup after 4 hours)

### 1.5 Relationships
- **One-to-Many**: Session → Messages (one session has many messages)
- **Many-to-One**: Session → User (many sessions belong to one user)

---

## 2. Message Entity

### 2.1 Purpose
Represents a single message exchanged between user and system within a session.

### 2.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `message_id` | String (UUID) | Yes | Unique message identifier |
| `session_id` | String (UUID) | Yes | Parent session identifier |
| `type` | Enum | Yes | Message type: TEXT, VOICE, IMAGE, COMMAND |
| `content` | String/Object | Yes | Message content (text, audio data, image key) |
| `timestamp` | Timestamp (ISO 8601) | Yes | Message timestamp |
| `direction` | Enum | Yes | Message direction: INBOUND (from user), OUTBOUND (to user) |
| `metadata` | Object | No | Additional metadata (intent, confidence, etc.) |

### 2.3 Entity Structure

**Text Message**:
```json
{
  "message_id": "msg_001",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "TEXT",
  "content": "Envíale 50 lucas a mi hermano",
  "timestamp": "2026-02-17T10:15:30Z",
  "direction": "INBOUND",
  "metadata": {
    "intent": "TRANSFER_P2P",
    "confidence": 0.85
  }
}
```

**Voice Message**:
```json
{
  "message_id": "msg_002",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "VOICE",
  "content": {
    "audio_data": "base64_encoded_audio",
    "format": "mp3",
    "duration": 3.5,
    "transcription": "Envíale 50 lucas a mi hermano"
  },
  "timestamp": "2026-02-17T10:15:30Z",
  "direction": "INBOUND",
  "metadata": {
    "intent": "TRANSFER_P2P",
    "confidence": 0.85
  }
}
```

**Image Message**:
```json
{
  "message_id": "msg_003",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "IMAGE",
  "content": {
    "s3_key": "images/user_12345/session_001/1708167330_laptop.jpg",
    "format": "jpeg",
    "size": 2048576,
    "analysis": {
      "objects": ["laptop", "keyboard"],
      "text": ["MacBook Pro", "$1299"],
      "scene": "product_photo"
    }
  },
  "timestamp": "2026-02-17T10:15:30Z",
  "direction": "INBOUND",
  "metadata": {
    "intent": "QUERY_PRODUCTS",
    "confidence": 0.90
  }
}
```

### 2.4 Storage
- **Primary Store**: Bedrock Managed Memory (DynamoDB backend)
- **Local Cache**: Session metadata in `centli-sessions` table
- **TTL**: Managed by Bedrock (configurable retention)

### 2.5 Relationships
- **Many-to-One**: Message → Session (many messages belong to one session)

---

## 3. Intent Entity

### 3.1 Purpose
Represents a recognized user intent extracted from a message by AgentCore.

### 3.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `intent_type` | Enum | Yes | Intent type (TRANSFER_P2P, QUERY_BALANCE, etc.) |
| `confidence` | Float (0-1) | Yes | Confidence score of intent recognition |
| `transfer_data` | Object | No | Transfer-specific data (amount, beneficiary) |
| `purchase_data` | Object | No | Purchase-specific data (product_id, quantity) |
| `query_data` | Object | No | Query-specific data (query_type, filters) |

### 3.3 Entity Structure (Typed Structure)

**Transfer Intent**:
```json
{
  "intent_type": "TRANSFER_P2P",
  "confidence": 0.85,
  "transfer_data": {
    "amount": 50000,
    "currency": "MXN",
    "beneficiary_alias": "mi hermano",
    "beneficiary_id": null,
    "description": "Transferencia P2P"
  }
}
```

**Purchase Intent**:
```json
{
  "intent_type": "PURCHASE_PRODUCT",
  "confidence": 0.90,
  "purchase_data": {
    "product_id": "prod_laptop_001",
    "product_name": "MacBook Pro",
    "quantity": 1,
    "payment_method": "DEBIT"
  }
}
```

**Query Intent**:
```json
{
  "intent_type": "QUERY_BALANCE",
  "confidence": 0.95,
  "query_data": {
    "query_type": "balance",
    "account_type": "checking"
  }
}
```

### 3.4 Intent Types

| Intent Type | Description | Required Data |
|-------------|-------------|---------------|
| `TRANSFER_P2P` | P2P money transfer | amount, beneficiary_alias |
| `QUERY_BALANCE` | Account balance inquiry | account_type (optional) |
| `QUERY_TRANSACTIONS` | Transaction history | date_range (optional) |
| `PURCHASE_PRODUCT` | Product purchase | product_id, quantity |
| `QUERY_PRODUCTS` | Product catalog browsing | category (optional) |
| `QUERY_BENEFICIARY` | Beneficiary lookup | beneficiary_alias |
| `ADD_BENEFICIARY` | Add new beneficiary | name, account_number |
| `GENERAL_QUERY` | General banking questions | query_text |
| `UNKNOWN` | Unrecognized intent | - |

### 3.5 Storage
- **Transient**: Not stored permanently
- **Logged**: Intent and confidence logged for analytics
- **Passed**: Included in ActionEvent for Action Groups

---

## 4. ActionEvent Entity

### 4.1 Purpose
Represents an action event published to EventBridge for Action Group processing.

### 4.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `action_type` | Enum | Yes | Action type (TRANSFER, PURCHASE, QUERY_BENEFICIARY, etc.) |
| `action_data` | Object | Yes | Action-specific data |
| `user_id` | String | Yes | User identifier |
| `session_id` | String (UUID) | Yes | Session identifier |
| `request_id` | String (UUID) | Yes | Unique request identifier |
| `timestamp` | Timestamp (ISO 8601) | Yes | Event timestamp |
| `metadata` | Object | Yes | Event metadata (intent confidence, context, etc.) |

### 4.3 Entity Structure

```json
{
  "action_type": "TRANSFER",
  "action_data": {
    "amount": 50000,
    "currency": "MXN",
    "beneficiary_alias": "mi hermano",
    "description": "Transferencia P2P"
  },
  "user_id": "user_12345",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "request_id": "req_001",
  "timestamp": "2026-02-17T10:15:35Z",
  "metadata": {
    "intent_confidence": 0.85,
    "conversation_context": "User requested P2P transfer to brother",
    "user_preferences": {
      "language": "es-MX"
    },
    "multimodal_inputs": ["voice"]
  }
}
```

### 4.4 Action Types

| Action Type | Target Action Group | Description |
|-------------|---------------------|-------------|
| `TRANSFER` | CoreBanking | Execute P2P transfer |
| `QUERY_BALANCE` | CoreBanking | Get account balance |
| `QUERY_TRANSACTIONS` | CoreBanking | Get transaction history |
| `PURCHASE` | Marketplace | Execute product purchase |
| `QUERY_PRODUCTS` | Marketplace | Browse product catalog |
| `QUERY_BENEFICIARY` | CRM | Lookup beneficiary |
| `ADD_BENEFICIARY` | CRM | Add new beneficiary |

### 4.5 Storage
- **Transient**: Published to EventBridge, not stored
- **Logged**: Event logged for audit trail
- **Tracked**: request_id stored in session for response correlation

---

## 5. VoiceInput Entity

### 5.1 Purpose
Represents voice input data from user for processing by Nova Sonic.

### 5.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio_data` | String (base64) | Yes | Base64-encoded audio data |
| `format` | Enum | Yes | Audio format: WAV, MP3, OGG |
| `duration` | Float | Yes | Audio duration in seconds |
| `language` | String | Yes | Language code (es-MX) |
| `transcription` | String | No | Transcribed text (after Nova Sonic processing) |

### 5.3 Entity Structure

```json
{
  "audio_data": "base64_encoded_audio_data_here",
  "format": "mp3",
  "duration": 3.5,
  "language": "es-MX",
  "transcription": "Envíale 50 lucas a mi hermano"
}
```

### 5.4 Validation Rules
- Format: WAV, MP3, OGG only
- Size: Max 10MB
- Duration: 0.5s - 60s
- Language: es-MX (Mexican Spanish)

### 5.5 Storage
- **Transient**: Not stored permanently
- **Processed**: Transcription stored in Message entity
- **Logged**: Audio metadata logged (not audio data)

---

## 6. ImageInput Entity

### 6.1 Purpose
Represents image input data from user for processing by Nova Canvas.

### 6.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `image_data` | String (base64) | Yes | Base64-encoded image data (for upload) |
| `format` | Enum | Yes | Image format: JPEG, PNG |
| `s3_key` | String | Yes | S3 object key (after upload) |
| `size` | Integer | Yes | Image size in bytes |
| `dimensions` | Object | Yes | Image dimensions (width, height) |
| `analysis_results` | Object | No | Nova Canvas analysis results |

### 6.3 Entity Structure

```json
{
  "image_data": "base64_encoded_image_data_here",
  "format": "jpeg",
  "s3_key": "images/user_12345/session_001/1708167330_laptop.jpg",
  "size": 2048576,
  "dimensions": {
    "width": 1920,
    "height": 1080
  },
  "analysis_results": {
    "objects": ["laptop", "keyboard", "mouse"],
    "text": ["MacBook Pro", "$1299", "16GB RAM"],
    "scene": "product_photo",
    "confidence": 0.92
  }
}
```

### 6.4 Validation Rules
- Format: JPEG, PNG only
- Size: Max 5MB
- Dimensions: Max 4096x4096 pixels
- Content: Basic content check (not empty, valid image)

### 6.5 Storage
- **S3**: Images stored in `centli-assets-{account-id}` bucket
- **Key Pattern**: `images/{user_id}/{session_id}/{timestamp}_{filename}`
- **Lifecycle**: Delete after 7 days
- **Analysis**: Results stored in Message entity

---

## 7. AgentResponse Entity

### 7.1 Purpose
Represents a response generated by AgentCore to be sent back to the user.

### 7.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `response_text` | String | Yes | Text response content |
| `response_audio` | String (base64) | No | Audio response (if voice output requested) |
| `response_type` | Enum | Yes | Response type: TEXT, VOICE, ERROR, CONFIRMATION |
| `metadata` | Object | No | Response metadata |
| `data` | Object | No | Additional data (transaction details, products, etc.) |

### 7.3 Entity Structure

**Text Response**:
```json
{
  "response_text": "Transferencia completada. Enviaste $50,000 MXN a Juan Pérez.",
  "response_audio": null,
  "response_type": "CONFIRMATION",
  "metadata": {
    "timestamp": "2026-02-17T10:15:40Z",
    "in_reply_to": "msg_001"
  },
  "data": {
    "transaction_details": {
      "transaction_id": "txn_001",
      "amount": 50000,
      "beneficiary": "Juan Pérez",
      "status": "completed"
    }
  }
}
```

**Voice Response**:
```json
{
  "response_text": "Transferencia completada. Enviaste 50 mil pesos a Juan Pérez.",
  "response_audio": "base64_encoded_audio_response",
  "response_type": "VOICE",
  "metadata": {
    "timestamp": "2026-02-17T10:15:40Z",
    "in_reply_to": "msg_001",
    "voice_config": {
      "language": "es-MX",
      "gender": "neutral",
      "speed": "normal"
    }
  },
  "data": {
    "transaction_details": {
      "transaction_id": "txn_001",
      "amount": 50000,
      "beneficiary": "Juan Pérez",
      "status": "completed"
    }
  }
}
```

**Error Response**:
```json
{
  "response_text": "No tienes saldo suficiente para esta operación.",
  "response_audio": null,
  "response_type": "ERROR",
  "metadata": {
    "timestamp": "2026-02-17T10:15:40Z",
    "in_reply_to": "msg_001",
    "error_code": "INSUFFICIENT_FUNDS"
  },
  "data": null
}
```

### 7.4 Response Types

| Response Type | Description | Use Case |
|---------------|-------------|----------|
| `TEXT` | Plain text response | General responses, queries |
| `VOICE` | Voice response (text + audio) | Voice interactions |
| `ERROR` | Error message | Operation failures |
| `CONFIRMATION` | Confirmation message | Successful operations |

### 7.5 Storage
- **Transient**: Sent via WebSocket, not stored permanently
- **Cached**: Stored in session if WebSocket disconnected (5 min TTL)
- **Logged**: Response metadata logged for analytics

---

## 8. ActionResponse Entity

### 8.1 Purpose
Represents a response from an Action Group Lambda back to AgentCore via EventBridge.

### 8.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `request_id` | String (UUID) | Yes | Original request identifier (for correlation) |
| `success` | Boolean | Yes | Operation success status |
| `result` | Object | No | Result data (if successful) |
| `error` | String | No | Error message (if failed) |
| `timestamp` | Timestamp (ISO 8601) | Yes | Response timestamp |

### 8.3 Entity Structure

**Success Response**:
```json
{
  "request_id": "req_001",
  "success": true,
  "result": {
    "data": {
      "transaction_id": "txn_001",
      "amount": 50000,
      "beneficiary": "Juan Pérez",
      "status": "completed"
    },
    "message": "Transferencia completada exitosamente"
  },
  "error": null,
  "timestamp": "2026-02-17T10:15:38Z"
}
```

**Error Response**:
```json
{
  "request_id": "req_001",
  "success": false,
  "result": null,
  "error": "INSUFFICIENT_FUNDS",
  "timestamp": "2026-02-17T10:15:38Z"
}
```

### 8.4 Storage
- **Transient**: Received from EventBridge, not stored
- **Processed**: Used to generate AgentResponse
- **Logged**: Response logged for audit trail

---

## 9. UserProfile Entity

### 9.1 Purpose
Represents a user's profile information for authentication and preferences.

### 9.2 Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | String | Yes | Unique user identifier |
| `email` | String | Yes | User email address |
| `name` | String | Yes | User full name |
| `phone` | String | No | User phone number |
| `language` | String | Yes | Preferred language (es-MX) |
| `voice_preferences` | Object | No | Voice settings (gender, speed) |
| `biometric_verified` | Boolean | Yes | Biometric verification status |
| `created_at` | Timestamp (ISO 8601) | Yes | Profile creation timestamp |
| `updated_at` | Timestamp (ISO 8601) | Yes | Last update timestamp |

### 9.3 Entity Structure

```json
{
  "user_id": "user_12345",
  "email": "juan.perez@example.com",
  "name": "Juan Pérez",
  "phone": "+52 55 1234 5678",
  "language": "es-MX",
  "voice_preferences": {
    "gender": "neutral",
    "speed": "normal"
  },
  "biometric_verified": true,
  "created_at": "2026-01-15T08:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

### 9.4 Storage
- **Primary Store**: DynamoDB table `centli-user-profiles`
- **Key**: `user_id` (partition key)
- **GSI**: `email` (for email lookup)

### 9.5 Relationships
- **One-to-Many**: User → Sessions (one user has many sessions)

---

## 10. Entity Relationships Diagram

```
UserProfile (1) ──────< (N) Session
                            │
                            │
                            └──────< (N) Message
                                        │
                                        ├──> (1) Intent
                                        │
                                        ├──> (0..1) VoiceInput
                                        │
                                        └──> (0..1) ImageInput

Intent ──────> (1) ActionEvent ──────> (1) ActionResponse ──────> (1) AgentResponse
```

**Relationship Descriptions**:
- User has many Sessions (1:N)
- Session has many Messages (1:N)
- Message has one Intent (1:1)
- Message may have VoiceInput (1:0..1)
- Message may have ImageInput (1:0..1)
- Intent generates ActionEvent (1:1)
- ActionEvent receives ActionResponse (1:1)
- ActionResponse generates AgentResponse (1:1)

---

## 11. Data Flow Summary

```
User Input (Text/Voice/Image)
  ↓
Message Entity (created)
  ↓
VoiceInput/ImageInput Entity (if applicable)
  ↓
Intent Entity (extracted by AgentCore)
  ↓
ActionEvent Entity (published to EventBridge)
  ↓
ActionResponse Entity (received from Action Group)
  ↓
AgentResponse Entity (generated by AgentCore)
  ↓
User Output (via WebSocket)
```

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Domain Entities**: 10 entities with attributes, structures, and relationships defined

