# Component Definitions - CENTLI

## Overview

CENTLI architecture consists of 6 main components organized for parallel development by 3 developers during an 8-hour hackathon.

**Component Organization**:
- **Dev 1 (Frontend)**: Frontend Multimodal UI
- **Dev 2 (Backend/Mocks)**: Core Banking Mock, Marketplace Mock, CRM Mock
- **Dev 3 (AgentCore/AI)**: AgentCore Orchestrator, Orchestration Service
- **Shared**: Infrastructure Foundation (configuration only)

---

## Component 1: Infrastructure Foundation

**Type**: Configuration (not application component)

**Purpose**: Define and provision all AWS infrastructure resources required for CENTLI

**Responsibilities**:
- Define DynamoDB table schemas (9 tables total)
- Configure AWS SAM template for serverless deployment
- Define IAM roles and policies for all services
- Configure S3 bucket for image storage
- Define EventBridge event bus for component communication
- Set up CloudWatch logging and monitoring

**Technology Stack**:
- AWS SAM (Serverless Application Model)
- CloudFormation
- YAML configuration files

**Deployment Artifacts**:
- `poc_template.yaml` - Main SAM template
- DynamoDB table definitions
- IAM policy documents
- EventBridge rule configurations

**Note**: This is pure infrastructure-as-code with no application logic or methods.

---

## Component 2: AgentCore Orchestrator

**Type**: AI/ML Orchestration Component

**Purpose**: Central intelligence hub that processes multimodal inputs, orchestrates actions, and generates contextual responses

**Responsibilities**:
- Process incoming messages (text, voice, images) from users
- Perform intent recognition and entity extraction
- Manage conversation context via Bedrock Managed Memory
- Invoke appropriate Action Groups based on user intent
- Generate natural language responses
- Handle voice synthesis via Nova Sonic integration
- Process images via Nova Canvas integration
- Validate user authentication and biometric data
- Manage user sessions and security context
- Publish events to EventBridge for Action Group invocation

**Key Capabilities**:
- **Multimodal Processing**: Handle text, voice (Nova Sonic), and images (Nova Canvas)
- **Agentic Intelligence**: AWS Bedrock AgentCore with Claude 3.7 Sonnet
- **Context Management**: Bedrock Managed Memory for conversation history
- **Intent Recognition**: Natural language understanding for banking commands
- **Security**: Authentication validation, biometric verification, session management

**Technology Stack**:
- AWS Bedrock AgentCore
- AWS Bedrock Nova Sonic (voice)
- AWS Bedrock Nova Canvas (images)
- Bedrock Managed Memory (DynamoDB backend)
- Python 3.9+

**Integration Points**:
- **Input**: Receives messages from Orchestration Service
- **Output**: Publishes events to EventBridge for Action Groups
- **Storage**: Reads/writes to Managed Memory (DynamoDB)

**Deployment**:
- Bedrock Agent configuration (not Lambda - managed service)
- Action Group definitions (OpenAPI schemas)
- Managed Memory configuration

---

## Component 3: Orchestration Service

**Type**: Service Layer / API Gateway Handler

**Purpose**: Coordinate communication between WebSocket API Gateway, AgentCore, and frontend clients

**Responsibilities**:
- Handle WebSocket connections (connect, disconnect, message)
- Route incoming messages to AgentCore
- Manage user sessions locally (DynamoDB)
- Synchronize session state with Bedrock Managed Memory
- Stream audio data for voice processing
- Handle image uploads to S3
- Return responses to WebSocket clients
- Manage connection state and reconnection logic
- Handle authentication tokens and user identity

**Key Capabilities**:
- **WebSocket Management**: Real-time bidirectional communication
- **Session Management**: Local session cache + Managed Memory sync
- **Multimodal Routing**: Route text/voice/image to appropriate processors
- **State Synchronization**: Keep local and Bedrock memory in sync

**Technology Stack**:
- AWS Lambda (Python 3.9+)
- API Gateway WebSocket API
- DynamoDB (session storage)
- S3 (image storage)

**Integration Points**:
- **Input**: WebSocket API Gateway (user messages)
- **Output**: AgentCore (for processing), WebSocket clients (responses)
- **Storage**: DynamoDB (sessions), S3 (images)

**Deployment**:
- 3 Lambda functions: Connect, Disconnect, Message handler
- Evolved from existing `app_inference` Lambda

---

## Component 4: Core Banking Mock (Action Group)

**Type**: Business Logic Component / Action Group

**Purpose**: Simulate core banking operations for P2P transfers, account management, and transaction processing

**Responsibilities**:
- Manage user accounts and balances
- Execute P2P transfers between accounts
- Validate account balances before transactions
- Record transaction history
- Provide account and transaction queries
- Validate transaction limits and business rules
- Return structured responses and errors

**Key Capabilities**:
- **Account Management**: CRUD operations for user accounts
- **P2P Transfers**: Execute transfers with atomic balance updates
- **Transaction History**: Query and record all transactions
- **Validation**: Balance checks, limit validation, account existence

**Technology Stack**:
- AWS Lambda (Python 3.9+)
- DynamoDB (Accounts, Transactions tables)
- EventBridge (event subscription)

**Integration Points**:
- **Input**: EventBridge events from AgentCore
- **Output**: EventBridge responses back to AgentCore
- **Storage**: DynamoDB (Accounts, Transactions)

**Deployment**:
- Lambda function with EventBridge trigger
- Registered as Bedrock Action Group

---

## Component 5: Marketplace Mock (Action Group)

**Type**: Business Logic Component / Action Group

**Purpose**: Simulate marketplace operations including product catalog, benefits calculation, and purchase execution

**Responsibilities**:
- Manage product catalog (list, search, details)
- Calculate available benefits (cashback, MSI, discounts, points)
- Execute product purchases
- Apply benefits automatically during purchase
- Integrate with Core Banking for payment processing
- Record purchase history
- Return structured responses and errors

**Key Capabilities**:
- **Product Catalog**: Browse and search products by category
- **Benefits Engine**: Calculate optimal benefits for user/product combinations
- **Purchase Execution**: Process purchases with benefit application
- **Payment Integration**: Coordinate with Core Banking for fund transfers

**Technology Stack**:
- AWS Lambda (Python 3.9+)
- DynamoDB (Products, Purchases tables)
- EventBridge (event subscription and publishing)

**Integration Points**:
- **Input**: EventBridge events from AgentCore
- **Output**: EventBridge responses to AgentCore, events to Core Banking
- **Storage**: DynamoDB (Products, Purchases)

**Deployment**:
- Lambda function with EventBridge trigger
- Registered as Bedrock Action Group

---

## Component 6: CRM Mock (Action Group)

**Type**: Business Logic Component / Action Group

**Purpose**: Manage beneficiary relationships and resolve natural language aliases to account information

**Responsibilities**:
- Store and manage user beneficiaries
- Resolve natural language aliases ("mi hermano", "mi mamá") to beneficiary data
- Handle ambiguous alias resolution (multiple matches)
- Track beneficiary usage frequency
- Provide beneficiary suggestions based on history
- Return structured responses and errors

**Key Capabilities**:
- **Beneficiary Management**: CRUD operations for beneficiaries
- **Alias Resolution**: Fuzzy matching and natural language processing
- **Ambiguity Handling**: Return multiple options when alias is ambiguous
- **Frequency Tracking**: Track and suggest frequent beneficiaries

**Technology Stack**:
- AWS Lambda (Python 3.9+)
- DynamoDB (Beneficiaries table)
- EventBridge (event subscription)

**Integration Points**:
- **Input**: EventBridge events from AgentCore
- **Output**: EventBridge responses back to AgentCore
- **Storage**: DynamoDB (Beneficiaries)

**Deployment**:
- Lambda function with EventBridge trigger
- Registered as Bedrock Action Group

---

## Component 7: Frontend Multimodal UI

**Type**: User Interface Component

**Purpose**: Provide multimodal user interface for voice, text, and image interactions with CENTLI

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

**Key Capabilities**:
- **Voice Input**: Browser MediaRecorder API for audio capture
- **Voice Output**: Browser Audio API for playback
- **Chat Interface**: Real-time message display with auto-scroll
- **Image Upload**: File picker and camera integration
- **Transaction UI**: Confirmation modals with transaction details
- **Product Catalog**: Grid/list view with benefits badges

**Technology Stack**:
- HTML5 / CSS3 / JavaScript (ES6+)
- WebSocket API (native browser)
- MediaRecorder API (voice input)
- Audio API (voice output)
- Responsive design (mobile-first)

**Integration Points**:
- **Input**: User interactions (voice, text, images, clicks)
- **Output**: WebSocket messages to Orchestration Service
- **Storage**: Local storage for session persistence

**Deployment**:
- Static files hosted on S3 + CloudFront
- Or served via API Gateway HTTP endpoint

---

## Component Interaction Summary

```
User (Browser)
    |
    | WebSocket
    v
Orchestration Service (Lambda)
    |
    | Invokes
    v
AgentCore (Bedrock)
    |
    | Publishes Events
    v
EventBridge (Event Bus)
    |
    +-- Triggers --> Core Banking Mock (Lambda)
    |
    +-- Triggers --> Marketplace Mock (Lambda)
    |
    +-- Triggers --> CRM Mock (Lambda)
```

**Event Flow**:
1. User sends message via WebSocket
2. Orchestration Service receives and routes to AgentCore
3. AgentCore processes intent and publishes event to EventBridge
4. EventBridge routes event to appropriate Action Group Lambda
5. Action Group processes request and publishes response event
6. AgentCore receives response and generates user-facing message
7. Orchestration Service sends response back via WebSocket
8. Frontend displays response to user

---

## Component Ownership (3 Developers)

**Dev 1 - Frontend Specialist**:
- Component 7: Frontend Multimodal UI
- Estimated: 8.5 hours (7 user stories)

**Dev 2 - Backend/Mocks Specialist**:
- Component 4: Core Banking Mock
- Component 5: Marketplace Mock
- Component 6: CRM Mock
- Estimated: 10 hours (6 user stories)

**Dev 3 - AgentCore/AI Specialist**:
- Component 2: AgentCore Orchestrator
- Component 3: Orchestration Service
- Estimated: 10.5 hours (6 user stories)

**Shared**:
- Component 1: Infrastructure Foundation (configuration - all devs contribute)

---

**Document Status**: Complete  
**Created**: 2026-02-16  
**Components**: 7 components (6 application + 1 infrastructure configuration)
