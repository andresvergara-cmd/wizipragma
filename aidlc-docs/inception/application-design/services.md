# Services - CENTLI

## Overview

CENTLI uses a service-oriented architecture with clear separation of concerns. Services coordinate between components and manage cross-cutting concerns like session management, event routing, and state synchronization.

---

## Service 1: Orchestration Service

**Type**: API Gateway Handler / Message Router

**Purpose**: Coordinate all communication between WebSocket clients, AgentCore, and backend systems

**Responsibilities**:
- Manage WebSocket lifecycle (connect, disconnect, message)
- Route messages to AgentCore for processing
- Handle multimodal input routing (text, voice, images)
- Manage local session state with DynamoDB
- Synchronize session state with Bedrock Managed Memory
- Stream responses back to WebSocket clients
- Handle connection errors and reconnection
- Manage authentication and authorization

**Service Interactions**:
```
WebSocket Client
    ↕
Orchestration Service
    ↓ (invoke)
AgentCore
    ↓ (publish events)
EventBridge
    ↓ (trigger)
Action Groups
```

**Implementation**:
- 3 Lambda functions (Connect, Disconnect, Message)
- DynamoDB table for session storage
- S3 bucket for image uploads
- API Gateway WebSocket API

**Key Patterns**:
- **Request-Response**: Synchronous communication with clients
- **Event-Driven**: Asynchronous communication via AgentCore/EventBridge
- **Cache-Aside**: Local session cache with Managed Memory sync
- **Circuit Breaker**: Handle AgentCore failures gracefully

---

## Service 2: Event Routing Service

**Type**: Event Bus / Message Broker

**Purpose**: Decouple AgentCore from Action Groups using event-driven architecture

**Responsibilities**:
- Route action events from AgentCore to appropriate Action Groups
- Route response events from Action Groups back to AgentCore
- Handle event filtering and transformation
- Provide event replay capability for debugging
- Monitor event flow and detect failures
- Support multiple event patterns (point-to-point, pub-sub)

**Service Interactions**:
```
AgentCore
    ↓ (publish action event)
EventBridge
    ├─→ Core Banking Mock (subscribe to banking events)
    ├─→ Marketplace Mock (subscribe to marketplace events)
    └─→ CRM Mock (subscribe to CRM events)
    
Action Groups
    ↓ (publish response event)
EventBridge
    ↓ (route back)
AgentCore
```

**Implementation**:
- AWS EventBridge as event bus
- Event rules for routing to Action Groups
- Dead letter queues for failed events
- CloudWatch Logs for event monitoring

**Event Patterns**:

### Action Events (AgentCore → Action Groups)
```json
{
  "source": "centli.agentcore",
  "detail-type": "ActionRequest",
  "detail": {
    "action_type": "TRANSFER | PURCHASE | QUERY_BENEFICIARY | ...",
    "action_data": { },
    "user_id": "string",
    "session_id": "string",
    "request_id": "string"
  }
}
```

### Response Events (Action Groups → AgentCore)
```json
{
  "source": "centli.actiongroup.{name}",
  "detail-type": "ActionResponse",
  "detail": {
    "request_id": "string",
    "success": true/false,
    "result": { },
    "error": "string (if failed)"
  }
}
```

**Key Patterns**:
- **Event-Driven Architecture**: Loose coupling between components
- **Publish-Subscribe**: Multiple subscribers per event type
- **Event Sourcing**: All events logged for audit trail
- **Saga Pattern**: Coordinate multi-step transactions across Action Groups

---

## Service 3: Session Management Service

**Type**: State Management / Context Synchronization

**Purpose**: Manage user session state across local storage and Bedrock Managed Memory

**Responsibilities**:
- Create and initialize user sessions
- Store session state locally in DynamoDB for fast access
- Synchronize session state with Bedrock Managed Memory
- Handle session expiration and cleanup
- Resolve session conflicts between local and Bedrock
- Provide session recovery after disconnection
- Track session metrics and analytics

**Service Interactions**:
```
Orchestration Service
    ↕ (read/write)
Local Session Storage (DynamoDB)
    ↕ (sync)
Bedrock Managed Memory
```

**Implementation**:
- DynamoDB table: `centli-sessions`
- Bedrock Managed Memory (DynamoDB backend)
- Lambda functions for sync operations
- TTL for automatic session cleanup

**Session Data Structure**:
```json
{
  "session_id": "string (PK)",
  "user_id": "string (GSI)",
  "connection_id": "string",
  "created_at": "ISO timestamp",
  "last_activity": "ISO timestamp",
  "expires_at": "ISO timestamp (TTL)",
  "state": {
    "conversation_history": [],
    "current_intent": "string",
    "pending_actions": [],
    "user_context": {}
  },
  "sync_status": {
    "last_sync": "ISO timestamp",
    "sync_version": "int",
    "conflicts": []
  }
}
```

**Synchronization Strategy**:
- **Write-Through**: Updates written to both local and Bedrock
- **Read-Through**: Read from local, fallback to Bedrock if missing
- **Periodic Sync**: Background sync every 30 seconds
- **Conflict Resolution**: Last-write-wins with conflict logging

**Key Patterns**:
- **Cache-Aside**: Local cache with remote backing store
- **Write-Through Cache**: Synchronous writes to both stores
- **Eventual Consistency**: Accept temporary inconsistencies
- **Optimistic Locking**: Version-based conflict detection

---

## Service 4: Authentication & Authorization Service

**Type**: Security / Identity Management

**Purpose**: Validate user identity and authorize operations

**Responsibilities**:
- Validate authentication tokens
- Verify biometric data (voice prints)
- Authorize operations based on user permissions
- Manage authentication levels (BASIC, BIOMETRIC, MFA)
- Track authentication attempts and failures
- Handle session security and token refresh

**Service Interactions**:
```
Orchestration Service
    ↓ (validate)
Auth Service
    ↓ (verify)
User Profile (DynamoDB)
    
AgentCore
    ↓ (validate before action)
Auth Service
```

**Implementation**:
- Lambda function for auth validation
- DynamoDB table: `centli-user-profiles`
- Integration with AgentCore for biometric validation
- JWT tokens for session authentication

**Authentication Levels**:
- **BASIC**: Username/password or token
- **BIOMETRIC**: Voice print validation (simulated for hackathon)
- **MFA**: Multi-factor authentication (optional)

**Authorization Rules**:
- **Low-risk operations**: BASIC auth (query balance, view products)
- **Medium-risk operations**: BIOMETRIC auth (small transfers < 1000 MXN)
- **High-risk operations**: BIOMETRIC + confirmation (large transfers, purchases)

**Key Patterns**:
- **Token-Based Authentication**: JWT tokens for stateless auth
- **Role-Based Access Control**: User roles determine permissions
- **Defense in Depth**: Multiple validation layers
- **Fail-Secure**: Deny by default, explicit allow

---

## Service 5: Multimodal Processing Service

**Type**: Input/Output Transformation

**Purpose**: Handle multimodal input/output transformations (voice, images)

**Responsibilities**:
- Stream audio data to Nova Sonic for transcription
- Generate audio responses via Nova Sonic
- Upload images to S3 for Nova Canvas processing
- Transform multimodal data to/from AgentCore format
- Handle format conversions and compression
- Manage streaming protocols for real-time processing

**Service Interactions**:
```
Orchestration Service
    ↓ (audio/image data)
Multimodal Service
    ├─→ Nova Sonic (voice processing)
    ├─→ Nova Canvas (image processing)
    └─→ S3 (image storage)
    ↓ (processed data)
AgentCore
```

**Implementation**:
- Integrated within Orchestration Service Lambda
- S3 bucket for image storage
- Direct integration with Bedrock Nova Sonic/Canvas

**Processing Flows**:

### Voice Input Flow
```
User speaks → Browser captures audio → WebSocket stream →
Orchestration Service → Nova Sonic → Text →
AgentCore → Intent recognition
```

### Voice Output Flow
```
AgentCore generates text → Nova Sonic → Audio stream →
Orchestration Service → WebSocket stream → Browser plays audio
```

### Image Input Flow
```
User uploads image → WebSocket/HTTP → Orchestration Service →
S3 upload → Nova Canvas analysis → Extracted data →
AgentCore → Context enrichment
```

**Key Patterns**:
- **Streaming**: Real-time audio streaming for low latency
- **Adapter Pattern**: Transform between different data formats
- **Asynchronous Processing**: Non-blocking multimodal operations
- **Fallback Strategy**: Text fallback if voice/image fails

---

## Service Orchestration Patterns

### Pattern 1: Synchronous Request-Response
**Use Case**: User queries balance  
**Flow**:
1. User sends message via WebSocket
2. Orchestration Service routes to AgentCore
3. AgentCore recognizes intent (QUERY_BALANCE)
4. AgentCore publishes event to EventBridge
5. Core Banking Mock receives event, queries balance
6. Core Banking Mock publishes response event
7. AgentCore receives response, generates user message
8. Orchestration Service sends response to user

**Latency**: ~2-3 seconds

---

### Pattern 2: Multi-Step Transaction
**Use Case**: P2P transfer with beneficiary resolution  
**Flow**:
1. User: "Envíale 50 lucas a mi hermano"
2. AgentCore recognizes intent (TRANSFER) + entity (alias="mi hermano")
3. AgentCore publishes event to CRM Mock (resolve alias)
4. CRM Mock returns beneficiary data
5. AgentCore publishes event to Core Banking Mock (validate funds)
6. Core Banking Mock confirms sufficient balance
7. AgentCore requests user confirmation
8. User confirms
9. AgentCore publishes event to Core Banking Mock (execute transfer)
10. Core Banking Mock executes and returns result
11. AgentCore generates confirmation message

**Latency**: ~5-7 seconds (includes user confirmation)

---

### Pattern 3: Cross-Component Coordination
**Use Case**: Product purchase with payment  
**Flow**:
1. User selects product and benefit option
2. AgentCore publishes event to Marketplace Mock (calculate benefits)
3. Marketplace Mock returns benefit details
4. AgentCore requests user confirmation
5. User confirms
6. AgentCore publishes event to Marketplace Mock (execute purchase)
7. Marketplace Mock publishes event to Core Banking Mock (process payment)
8. Core Banking Mock executes payment and returns result
9. Marketplace Mock completes purchase and returns result
10. AgentCore generates confirmation with benefits applied

**Latency**: ~6-8 seconds (includes user confirmation)

---

## Service Monitoring & Observability

### Metrics to Track
- **Orchestration Service**: WebSocket connections, message throughput, latency
- **Event Routing Service**: Event volume, routing latency, failed events
- **Session Management Service**: Active sessions, sync latency, conflicts
- **Auth Service**: Auth attempts, failures, biometric validations
- **Multimodal Service**: Voice transcription latency, image processing time

### Logging Strategy
- **Structured Logging**: JSON format with correlation IDs
- **Log Levels**: DEBUG (dev), INFO (prod), ERROR (always)
- **Correlation**: Track requests across services with request_id
- **PII Masking**: Mask sensitive data in logs

### Alerting
- **High Priority**: Auth failures, event routing failures, AgentCore errors
- **Medium Priority**: High latency, session sync conflicts
- **Low Priority**: Connection drops, retry exhaustion

---

## Service Deployment

### Lambda Configuration
- **Runtime**: Python 3.9+
- **Memory**: 512 MB (Orchestration), 256 MB (Action Groups)
- **Timeout**: 30 seconds (Orchestration), 15 seconds (Action Groups)
- **Concurrency**: Reserved concurrency for critical services
- **Environment Variables**: Service-specific configuration

### EventBridge Configuration
- **Event Bus**: `centli-event-bus`
- **Rules**: One rule per Action Group for event routing
- **Dead Letter Queue**: SQS queue for failed events
- **Archive**: 7-day event archive for debugging

### DynamoDB Configuration
- **Tables**: Sessions, Accounts, Transactions, Beneficiaries, Products, Purchases
- **Capacity**: On-demand (hackathon), Provisioned (production)
- **TTL**: Enabled on sessions table (24-hour expiration)
- **Streams**: Enabled for session sync

---

**Document Status**: Complete  
**Created**: 2026-02-16  
**Services**: 5 core services with orchestration patterns  
**Architecture**: Event-driven, microservices, serverless
