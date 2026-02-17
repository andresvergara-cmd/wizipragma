# Units of Work - CENTLI

## Overview

CENTLI is decomposed into 4 units of work for parallel development during an 8-hour hackathon. Each unit represents a logical grouping of components and stories that can be developed independently with well-defined integration contracts.

**Decomposition Strategy**:
- 4 units (grouped from 6 components)
- Parallel development (no critical path)
- Infrastructure distributed by responsibility
- Integration checkpoints at hours 2, 4, 6

**Code Organization**: By type (src/lambdas/, src/frontend/, src/infrastructure/)

**Deployment**: SAM template base + nested templates per unit

---

## Unit 1: Infrastructure Foundation

**Type**: Configuration Unit (Shared Infrastructure)

**Purpose**: Provide base AWS infrastructure resources required by all units

**Responsibilities**:
- Define base SAM template structure
- Configure EventBridge event bus (centli-event-bus)
- Define IAM roles for cross-unit access
- Set up CloudWatch log groups
- Configure S3 bucket for images and static assets
- Define base networking (if needed)

**Technology Stack**:
- AWS SAM (Serverless Application Model)
- CloudFormation
- YAML configuration

**Deployment Artifacts**:
- `infrastructure/base-template.yaml` - Base SAM template
- `infrastructure/eventbridge-config.yaml` - EventBridge rules (nested)
- `infrastructure/iam-policies.yaml` - IAM roles and policies (nested)

**Integration Points**:
- Provides EventBridge bus for all units
- Provides S3 bucket for Frontend and AgentCore units
- Provides IAM roles for Lambda execution

**Stories Assigned**: None (infrastructure only)

**Estimated Effort**: 1 hour (setup during hour 1)

**Developer Assignment**: Shared (all developers contribute their infrastructure needs)

**Infrastructure Components**:
```yaml
Resources:
  # EventBridge Event Bus
  CentliEventBus:
    Type: AWS::Events::EventBus
    Properties:
      Name: centli-event-bus
  
  # S3 Bucket for images and static assets
  CentliAssetsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: centli-assets-${AWS::AccountId}
  
  # CloudWatch Log Group
  CentliLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/lambda/centli
      RetentionInDays: 7
  
  # Base IAM Role for Lambdas
  CentliLambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument: ...
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

---

## Unit 2: AgentCore & Orchestration

**Type**: AI/ML Orchestration Unit

**Purpose**: Provide intelligent orchestration, multimodal processing, and WebSocket communication

**Responsibilities**:
- Configure AWS Bedrock AgentCore with Claude 3.7 Sonnet
- Set up Bedrock Managed Memory (DynamoDB backend)
- Integrate Nova Sonic for voice processing
- Integrate Nova Canvas for image processing
- Implement Orchestration Service (3 Lambdas: Connect, Disconnect, Message)
- Manage WebSocket API Gateway
- Handle session management (local DynamoDB + Managed Memory sync)
- Publish action events to EventBridge
- Process response events from Action Groups

**Technology Stack**:
- AWS Bedrock AgentCore
- AWS Bedrock Nova Sonic (voice)
- AWS Bedrock Nova Canvas (images)
- AWS Lambda (Python 3.9+)
- API Gateway WebSocket API
- DynamoDB (sessions table)
- EventBridge (event publishing)

**Deployment Artifacts**:
- `infrastructure/agentcore-template.yaml` - Nested SAM template
- `lambdas/app_connect/` - WebSocket connect handler
- `lambdas/app_disconnect/` - WebSocket disconnect handler
- `lambdas/app_message/` - WebSocket message handler
- `agentcore/agent-config.json` - Bedrock Agent configuration
- `agentcore/action-groups/` - OpenAPI schemas for Action Groups

**DynamoDB Tables**:
```yaml
CentliSessionsTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: centli-sessions
    AttributeDefinitions:
      - AttributeName: session_id
        AttributeType: S
      - AttributeName: user_id
        AttributeType: S
    KeySchema:
      - AttributeName: session_id
        KeyType: HASH
    GlobalSecondaryIndexes:
      - IndexName: user-index
        KeySchema:
          - AttributeName: user_id
            KeyType: HASH
    TimeToLiveSpecification:
      AttributeName: expires_at
      Enabled: true
```

**Integration Points**:
- **Input**: WebSocket API Gateway (user messages)
- **Output**: EventBridge (action events to Action Groups)
- **Input**: EventBridge (response events from Action Groups)
- **Output**: WebSocket API Gateway (responses to users)
- **Storage**: S3 (image uploads), DynamoDB (sessions)

**Stories Assigned** (Dev 3 - AgentCore/AI):
- Story 3.1: Setup AWS Bedrock AgentCore (2h)
- Story 3.2: Configure Action Groups (2h)
- Story 3.3: Integrate Nova Sonic for Voice (2h)
- Story 3.4: Integrate Nova Canvas for Images (1.5h)
- Story 3.5: Implement Intent Recognition (1.5h)
- Story 3.6: Implement Managed Memory (1.5h)

**Total Estimated Effort**: 10.5 hours

**Developer Assignment**: Dev 3 (AgentCore/AI Specialist)

**Key Methods** (from component-methods.md):
- AgentCore: process_message, recognize_intent, validate_authentication, manage_session, process_voice_input, generate_voice_output, process_image_input, publish_action_event
- Orchestration Service: handle_connect, handle_disconnect, handle_message, route_to_agentcore, manage_local_session, sync_with_managed_memory, handle_voice_stream, handle_image_upload, send_response

---

## Unit 3: Action Groups (Backend Services)

**Type**: Business Logic Unit (Grouped)

**Purpose**: Provide mock banking, marketplace, and CRM services via EventBridge-triggered Lambdas

**Responsibilities**:
- Implement Core Banking Mock (accounts, transfers, transactions)
- Implement Marketplace Mock (products, benefits, purchases)
- Implement CRM Mock (beneficiaries, alias resolution)
- Subscribe to EventBridge action events
- Publish response events back to EventBridge
- Manage DynamoDB tables for business data
- Handle cross-Action Group communication (e.g., Marketplace → Core Banking for payment)

**Technology Stack**:
- AWS Lambda (Python 3.9+)
- DynamoDB (6 tables: Accounts, Transactions, Beneficiaries, Products, Purchases, UserProfiles)
- EventBridge (event subscription and publishing)

**Deployment Artifacts**:
- `infrastructure/action-groups-template.yaml` - Nested SAM template
- `lambdas/core_banking/` - Core Banking Lambda
- `lambdas/marketplace/` - Marketplace Lambda
- `lambdas/crm/` - CRM Lambda

**DynamoDB Tables**:
```yaml
# Core Banking Tables
CentliAccountsTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: centli-accounts
    AttributeDefinitions:
      - AttributeName: user_id
        AttributeType: S
    KeySchema:
      - AttributeName: user_id
        KeyType: HASH

CentliTransactionsTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: centli-transactions
    AttributeDefinitions:
      - AttributeName: transaction_id
        AttributeType: S
      - AttributeName: user_id
        AttributeType: S
      - AttributeName: timestamp
        AttributeType: S
    KeySchema:
      - AttributeName: transaction_id
        KeyType: HASH
    GlobalSecondaryIndexes:
      - IndexName: user-timestamp-index
        KeySchema:
          - AttributeName: user_id
            KeyType: HASH
          - AttributeName: timestamp
            KeyType: RANGE

# Marketplace Tables
CentliProductsTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: centli-products
    AttributeDefinitions:
      - AttributeName: product_id
        AttributeType: S
      - AttributeName: category
        AttributeType: S
    KeySchema:
      - AttributeName: product_id
        KeyType: HASH
    GlobalSecondaryIndexes:
      - IndexName: category-index
        KeySchema:
          - AttributeName: category
            KeyType: HASH

CentliPurchasesTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: centli-purchases
    AttributeDefinitions:
      - AttributeName: purchase_id
        AttributeType: S
      - AttributeName: user_id
        AttributeType: S
    KeySchema:
      - AttributeName: purchase_id
        KeyType: HASH
    GlobalSecondaryIndexes:
      - IndexName: user-index
        KeySchema:
          - AttributeName: user_id
            KeyType: HASH

# CRM Tables
CentliBeneficiariesTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: centli-beneficiaries
    AttributeDefinitions:
      - AttributeName: beneficiary_id
        AttributeType: S
      - AttributeName: user_id
        AttributeType: S
    KeySchema:
      - AttributeName: beneficiary_id
        KeyType: HASH
    GlobalSecondaryIndexes:
      - IndexName: user-index
        KeySchema:
          - AttributeName: user_id
            KeyType: HASH

CentliUserProfilesTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: centli-user-profiles
    AttributeDefinitions:
      - AttributeName: user_id
        AttributeType: S
    KeySchema:
      - AttributeName: user_id
        KeyType: HASH
```

**Integration Points**:
- **Input**: EventBridge (action events from AgentCore)
- **Output**: EventBridge (response events to AgentCore)
- **Cross-Unit**: Marketplace → Core Banking (payment events via EventBridge)
- **Storage**: DynamoDB (6 tables for business data)

**Stories Assigned** (Dev 2 - Backend/Mocks):
- Story 2.1: Implement Core Banking Mock - Accounts (1.5h)
- Story 2.2: Implement P2P Transfers (2h)
- Story 2.3: Implement CRM Mock - Beneficiaries (1.5h)
- Story 2.4: Implement Marketplace Mock - Products (1.5h)
- Story 2.5: Implement Benefits Engine (2h)
- Story 2.6: Implement Purchase Execution (1.5h)

**Total Estimated Effort**: 10 hours

**Developer Assignment**: Dev 2 (Backend/Mocks Specialist)

**Key Methods** (from component-methods.md):
- Core Banking: get_balance, get_account, validate_funds, execute_transfer, get_transactions, validate_account_exists, handle_action_event
- Marketplace: list_products, get_product, search_products, calculate_benefits, execute_purchase, get_purchase_history, handle_action_event, publish_payment_event
- CRM: search_beneficiary, get_beneficiary, add_beneficiary, update_beneficiary, delete_beneficiary, get_frequent_beneficiaries, increment_usage_frequency, handle_action_event

---

## Unit 4: Frontend Multimodal UI

**Type**: User Interface Unit

**Purpose**: Provide multimodal user interface for voice, text, and image interactions

**Responsibilities**:
- Establish and maintain WebSocket connection
- Capture and stream voice input (microphone)
- Play voice output (audio responses)
- Display chat interface with message history
- Handle image uploads (camera or file picker)
- Show transaction confirmation dialogs
- Display product catalog with benefits
- Provide visual feedback for all operations
- Handle connection errors and reconnection

**Technology Stack**:
- HTML5 / CSS3 / JavaScript (ES6+)
- WebSocket API (native browser)
- MediaRecorder API (voice input)
- Audio API (voice output)
- Responsive design (mobile-first)

**Deployment Artifacts**:
- `frontend/index.html` - Main HTML file
- `frontend/css/styles.css` - Styles
- `frontend/js/websocket-manager.js` - WebSocket connection
- `frontend/js/voice-manager.js` - Voice input/output
- `frontend/js/chat-manager.js` - Chat interface
- `frontend/js/image-manager.js` - Image upload
- `frontend/js/transaction-manager.js` - Transaction confirmation
- `frontend/js/product-catalog-manager.js` - Product catalog

**Deployment Strategy**:
- Static files hosted on S3 (from Unit 1)
- Optional: CloudFront distribution for CDN
- Or: Served via API Gateway HTTP endpoint

**Integration Points**:
- **Output**: WebSocket API Gateway (messages to Orchestration Service)
- **Input**: WebSocket API Gateway (responses from Orchestration Service)
- **Storage**: S3 (image uploads), Local Storage (session persistence)

**Stories Assigned** (Dev 1 - Frontend):
- Story 1.1: Implement WebSocket Connection (1h)
- Story 1.2: Implement Voice Input UI (1.5h)
- Story 1.3: Implement Voice Output UI (1h)
- Story 1.4: Implement Chat Interface (1.5h)
- Story 1.5: Implement Transaction Confirmation UI (1h)
- Story 1.6: Implement Product Catalog UI (1.5h)
- Story 1.7: Implement Image Upload UI (1h)

**Total Estimated Effort**: 8.5 hours

**Developer Assignment**: Dev 1 (Frontend Specialist)

**Key Methods** (from component-methods.md):
- WebSocketManager: connect, disconnect, send_message, on_message
- VoiceManager: start_recording, stop_recording, play_audio
- ChatManager: add_message, clear_chat, auto_scroll
- ImageManager: upload_image
- TransactionManager: show_confirmation, show_receipt
- ProductCatalogManager: display_products, show_product_details, show_benefits_comparison

---

## Unit Summary

| Unit | Components | Stories | Effort | Developer | Critical |
|------|-----------|---------|--------|-----------|----------|
| Unit 1: Infrastructure | EventBridge, S3, IAM, CloudWatch | 0 | 1h | Shared | No |
| Unit 2: AgentCore & Orchestration | AgentCore, Orchestration Service, Nova Sonic/Canvas | 6 | 10.5h | Dev 3 | No |
| Unit 3: Action Groups | Core Banking, Marketplace, CRM | 6 | 10h | Dev 2 | No |
| Unit 4: Frontend | Multimodal UI | 7 | 8.5h | Dev 1 | No |
| **Total** | **7 components** | **19 stories** | **30h** | **3 devs** | **Parallel** |

**Parallel Execution**: With 3 developers working simultaneously, estimated completion time is ~10 hours (with buffer for integration)

**Target Timeline**: 8 hours (aggressive but achievable with Must Have focus)

---

## Development Sequence

### Hour 1: Setup & Infrastructure
- **All Devs**: Deploy Unit 1 (Infrastructure Foundation)
- **Dev 1**: Start Story 1.1 (WebSocket Connection)
- **Dev 2**: Start Story 2.1 (Core Banking Accounts)
- **Dev 3**: Start Story 3.1 (AgentCore Setup)

### Hour 2: Core Development + Checkpoint 1
- **Dev 1**: Stories 1.2, 1.3 (Voice Input/Output)
- **Dev 2**: Story 2.2 (P2P Transfers)
- **Dev 3**: Stories 3.2, 3.3 (Action Groups, Nova Sonic)
- **Checkpoint**: Verify infrastructure deployed, basic connectivity working

### Hours 3-4: Feature Development + Checkpoint 2
- **Dev 1**: Stories 1.4, 1.5 (Chat, Transaction Confirmation)
- **Dev 2**: Stories 2.4, 2.5 (Marketplace, Benefits)
- **Dev 3**: Story 3.5 (Intent Recognition)
- **Checkpoint (Hour 4)**: First integration test (AgentCore + Action Groups)

### Hours 5-6: Integration + Checkpoint 3
- **Dev 1**: Story 1.6 (Product Catalog)
- **Dev 2**: Story 2.6 (Purchase Execution)
- **Dev 3**: Story 3.6 (Managed Memory)
- **Checkpoint (Hour 6)**: Full integration test (all units working together)

### Hours 7-8: Testing & Demo Prep
- **All Devs**: Integration testing, bug fixes, demo rehearsal
- **Optional**: Stories 2.3 (CRM), 3.4 (Nova Canvas), 1.7 (Image Upload) if time permits

---

## Integration Contracts

### Contract 1: AgentCore → Action Groups (via EventBridge)

**Event Schema**:
```json
{
  "source": "centli.agentcore",
  "detail-type": "ActionRequest",
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
    "request_id": "string",
    "timestamp": "ISO 8601"
  }
}
```

**Response Schema**:
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

### Contract 2: Frontend → Orchestration Service (via WebSocket)

**Message Schema**:
```json
{
  "type": "TEXT | VOICE | IMAGE | COMMAND",
  "content": "string | base64",
  "metadata": {
    "timestamp": "ISO 8601",
    "message_id": "string",
    "user_id": "string",
    "session_id": "string"
  }
}
```

**Response Schema**:
```json
{
  "type": "TEXT | VOICE | ERROR | CONFIRMATION",
  "content": "string | base64",
  "metadata": {
    "timestamp": "ISO 8601",
    "message_id": "string",
    "in_reply_to": "string"
  },
  "data": {
    "transaction_details": {} (optional),
    "products": [] (optional),
    "benefits": [] (optional)
  }
}
```

### Contract 3: Marketplace → Core Banking (via EventBridge)

**Payment Event Schema**:
```json
{
  "source": "centli.actiongroup.marketplace",
  "detail-type": "PaymentRequest",
  "detail": {
    "user_id": "string",
    "amount": "number",
    "purchase_id": "string",
    "payment_method": "DEBIT | CREDIT",
    "request_id": "string",
    "timestamp": "ISO 8601"
  }
}
```

---

## Rollback Strategy

**If Unit Fails**:
1. **Simplify the unit**: Reduce scope, use simpler mocks
2. **Adjust demo**: Focus on working units
3. **Fallback options**:
   - Unit 2 (AgentCore): Fallback to Bedrock Converse (simpler)
   - Unit 3 (Action Groups): Use in-memory mocks (no DynamoDB)
   - Unit 4 (Frontend): Text-only interface (skip voice/images)

**Priority**: Must Have stories (15) take precedence over Should/Could Have (4)

---

## Code Organization

```
centli/
├── infrastructure/
│   ├── base-template.yaml           # Unit 1: Base SAM template
│   ├── agentcore-template.yaml      # Unit 2: Nested template
│   ├── action-groups-template.yaml  # Unit 3: Nested template
│   ├── eventbridge-config.yaml      # Unit 1: EventBridge rules
│   └── iam-policies.yaml            # Unit 1: IAM roles
├── lambdas/
│   ├── app_connect/                 # Unit 2: WebSocket connect
│   ├── app_disconnect/              # Unit 2: WebSocket disconnect
│   ├── app_message/                 # Unit 2: WebSocket message
│   ├── core_banking/                # Unit 3: Core Banking Lambda
│   ├── marketplace/                 # Unit 3: Marketplace Lambda
│   └── crm/                         # Unit 3: CRM Lambda
├── agentcore/
│   ├── agent-config.json            # Unit 2: Bedrock Agent config
│   └── action-groups/               # Unit 2: OpenAPI schemas
├── frontend/
│   ├── index.html                   # Unit 4: Main HTML
│   ├── css/                         # Unit 4: Styles
│   └── js/                          # Unit 4: JavaScript modules
├── tests/
│   ├── unit/                        # Unit tests per unit
│   └── integration/                 # Integration tests
├── data/
│   └── mock-data/                   # Mock data for seeding
├── pyproject.toml                   # Python dependencies
└── README.md                        # Project documentation
```

---

## Agent Assignment (Automated Creation)

**Strategy**: Hybrid - 3 specialized agents + 1 testing agent (Opción E)

### Agent 1: CENTLI-Frontend-Agent
- **Responsibility**: Unit 4 (Frontend Multimodal UI)
- **Context**: Stories Dev 1, component-methods.md (Frontend), services.md
- **Creation**: Automatic during Code Generation of Unit 4
- **Customization**: User can personalize after creation

### Agent 2: CENTLI-Backend-Agent
- **Responsibility**: Unit 3 (Action Groups)
- **Context**: Stories Dev 2, component-methods.md (Action Groups), services.md
- **Creation**: Automatic during Code Generation of Unit 3
- **Customization**: User can personalize after creation

### Agent 3: CENTLI-AgentCore-Agent
- **Responsibility**: Unit 2 (AgentCore & Orchestration)
- **Context**: Stories Dev 3, component-methods.md (AgentCore), services.md
- **Creation**: Automatic during Code Generation of Unit 2
- **Customization**: User can personalize after creation

### Agent 4: CENTLI-Test-Agent
- **Responsibility**: Build and Test phase (all units)
- **Context**: All unit artifacts, test requirements
- **Creation**: Automatic during Build and Test phase
- **Customization**: User can personalize after creation

**Note**: Agents will be created automatically when entering Code Generation phase for each unit. User will have opportunity to customize agents before they execute.

---

**Document Status**: Complete  
**Created**: 2026-02-16  
**Units**: 4 units of work with clear boundaries and dependencies  
**Timeline**: 8-hour hackathon with parallel development
