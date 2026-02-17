# Unit of Work Story Mapping - CENTLI

## Overview

This document maps all 19 user stories to their respective units of work, maintaining the original organization by stack técnico for parallel development.

**Total Stories**: 19 stories  
**Total Estimated Effort**: 29 hours  
**Target Timeline**: 8 hours (with 3 developers in parallel)  
**Priority Distribution**: 15 Must Have, 2 Should Have, 2 Could Have

---

## Story Distribution by Unit

| Unit | Stories | Estimated Hours | Developer | Priority Breakdown |
|------|---------|----------------|-----------|-------------------|
| Unit 1: Infrastructure | 0 | 1h (setup) | Shared | N/A |
| Unit 2: AgentCore & Orchestration | 6 | 10.5h | Dev 3 | 5 Must, 1 Should |
| Unit 3: Action Groups | 6 | 10h | Dev 2 | 5 Must, 1 Should |
| Unit 4: Frontend | 7 | 8.5h | Dev 1 | 5 Must, 2 Could |
| **Total** | **19** | **30h** | **3 devs** | **15 Must, 2 Should, 2 Could** |

---

## Unit 2: AgentCore & Orchestration (Dev 3)

### Story 3.1: Setup AWS Bedrock AgentCore
**Priority**: Must Have  
**Estimation**: 2 hours  
**Epic**: Bedrock AgentCore Foundation

**Description**: Configure AWS Bedrock AgentCore with Claude 3.7 Sonnet, Managed Memory, and Action Group definitions

**Acceptance Criteria**:
- AgentCore is active and responds to invocations
- Managed Memory maintains context between invocations
- Logs show successful invocations

**Dependencies**: Unit 1 (Infrastructure)

**Agent Assignment**: CENTLI-AgentCore-Agent

---

### Story 3.2: Configure Action Groups
**Priority**: Must Have  
**Estimation**: 2 hours  
**Epic**: Bedrock AgentCore Foundation

**Description**: Register 3 Action Groups (CoreBanking, Marketplace, CRM) with OpenAPI schemas

**Acceptance Criteria**:
- AgentCore can invoke all 3 Action Groups
- OpenAPI schemas are valid
- Logs show successful Action Group invocations

**Dependencies**: Story 3.1, Unit 3 (Action Groups Lambdas)

**Agent Assignment**: CENTLI-AgentCore-Agent

---

### Story 3.3: Integrate Nova Sonic for Voice
**Priority**: Must Have  
**Estimation**: 2 hours  
**Epic**: Bedrock AgentCore Foundation

**Description**: Integrate AWS Bedrock Nova Sonic for speech-to-text and text-to-speech

**Acceptance Criteria**:
- Nova Sonic transcribes audio correctly
- Nova Sonic generates natural Spanish audio
- Latency < 3 seconds for voice processing

**Dependencies**: Story 3.1

**Agent Assignment**: CENTLI-AgentCore-Agent

---

### Story 3.4: Integrate Nova Canvas for Images
**Priority**: Could Have  
**Estimation**: 1.5 hours  
**Epic**: Bedrock AgentCore Foundation

**Description**: Integrate AWS Bedrock Nova Canvas for image analysis

**Acceptance Criteria**:
- Nova Canvas extracts text from images (OCR)
- Nova Canvas identifies objects in images
- Images are stored in S3

**Dependencies**: Story 3.1, Unit 1 (S3 bucket)

**Agent Assignment**: CENTLI-AgentCore-Agent

---

### Story 3.5: Implement Intent Recognition
**Priority**: Must Have  
**Estimation**: 1.5 hours  
**Epic**: Intelligent Processing

**Description**: Implement natural language understanding for banking commands

**Acceptance Criteria**:
- System identifies TRANSFER intent correctly
- System identifies PURCHASE intent correctly
- System extracts entities (amount, beneficiary, product)

**Dependencies**: Story 3.1

**Agent Assignment**: CENTLI-AgentCore-Agent

---

### Story 3.6: Implement Managed Memory
**Priority**: Should Have  
**Estimation**: 1.5 hours  
**Epic**: Intelligent Processing

**Description**: Configure Bedrock Managed Memory for conversation context persistence

**Acceptance Criteria**:
- System remembers beneficiary "mi hermano" between sessions
- System suggests frequent beneficiaries
- Managed Memory persists in DynamoDB

**Dependencies**: Story 3.1

**Agent Assignment**: CENTLI-AgentCore-Agent

---

## Unit 3: Action Groups (Dev 2)

### Story 2.1: Implement Core Banking Mock - Accounts
**Priority**: Must Have  
**Estimation**: 1.5 hours  
**Epic**: Core Bancario Mock

**Description**: Implement Lambda for account management and balance queries

**Acceptance Criteria**:
- getAccount returns complete account data
- getBalance returns current balance
- updateBalance persists in DynamoDB

**Dependencies**: Unit 1 (DynamoDB tables)

**Agent Assignment**: CENTLI-Backend-Agent

---

### Story 2.2: Implement P2P Transfers
**Priority**: Must Have  
**Estimation**: 2 hours  
**Epic**: Core Bancario Mock

**Description**: Implement P2P transfer logic with atomic balance updates

**Acceptance Criteria**:
- Transfer updates both source and destination balances
- Transaction is recorded in DynamoDB
- Saldo validation works correctly

**Dependencies**: Story 2.1

**Agent Assignment**: CENTLI-Backend-Agent

---

### Story 2.3: Implement CRM Mock - Beneficiaries
**Priority**: Should Have  
**Estimation**: 1.5 hours  
**Epic**: Core Bancario Mock

**Description**: Implement beneficiary management and alias resolution

**Acceptance Criteria**:
- Search by alias "mi hermano" returns Juan López
- System handles ambiguous aliases
- Frequent beneficiaries are ordered correctly

**Dependencies**: Unit 1 (DynamoDB tables)

**Agent Assignment**: CENTLI-Backend-Agent

---

### Story 2.4: Implement Marketplace Mock - Products
**Priority**: Must Have  
**Estimation**: 1.5 hours  
**Epic**: Marketplace Mock

**Description**: Implement product catalog with search and filtering

**Acceptance Criteria**:
- listProducts returns complete catalog
- Search by category works
- Product details include benefits

**Dependencies**: Unit 1 (DynamoDB tables)

**Agent Assignment**: CENTLI-Backend-Agent

---

### Story 2.5: Implement Benefits Engine
**Priority**: Must Have  
**Estimation**: 2 hours  
**Epic**: Marketplace Mock

**Description**: Implement benefits calculation (cashback, MSI, discounts, points)

**Acceptance Criteria**:
- Cashback calculation is correct (5% = 500 pesos on 10,000)
- MSI options are presented when applicable
- System suggests best benefit for user

**Dependencies**: Story 2.4, Story 2.1 (credit line check)

**Agent Assignment**: CENTLI-Backend-Agent

---

### Story 2.6: Implement Purchase Execution
**Priority**: Must Have  
**Estimation**: 1.5 hours  
**Epic**: Marketplace Mock

**Description**: Execute product purchase with automatic benefit application

**Acceptance Criteria**:
- Purchase updates saldo/credit correctly
- Benefits are applied automatically
- Purchase is recorded in DynamoDB
- Integration with Core Banking works

**Dependencies**: Story 2.5, Story 2.1

**Agent Assignment**: CENTLI-Backend-Agent

---

## Unit 4: Frontend (Dev 1)

### Story 1.1: Implement WebSocket Connection
**Priority**: Must Have  
**Estimation**: 1 hour  
**Epic**: User Interface

**Description**: Establish WebSocket connection with auto-reconnect

**Acceptance Criteria**:
- WebSocket connects automatically on page load
- Messages send and receive in real-time
- Auto-reconnect works on disconnect

**Dependencies**: Unit 1 (WebSocket API Gateway)

**Agent Assignment**: CENTLI-Frontend-Agent

---

### Story 1.2: Implement Voice Input UI
**Priority**: Must Have  
**Estimation**: 1.5 hours  
**Epic**: User Interface

**Description**: Implement voice recording button with visual feedback

**Acceptance Criteria**:
- Voice button captures audio correctly
- Visual indicator shows recording state
- Audio transmits to backend via WebSocket

**Dependencies**: Story 1.1

**Agent Assignment**: CENTLI-Frontend-Agent

---

### Story 1.3: Implement Voice Output UI
**Priority**: Must Have  
**Estimation**: 1 hour  
**Epic**: User Interface

**Description**: Implement audio playback for voice responses

**Acceptance Criteria**:
- Audio plays automatically when received
- Visual indicator shows CENTLI is speaking
- Playback controls work (pause, resume)

**Dependencies**: Story 1.1

**Agent Assignment**: CENTLI-Frontend-Agent

---

### Story 1.4: Implement Chat Interface
**Priority**: Must Have  
**Estimation**: 1.5 hours  
**Epic**: User Interface

**Description**: Implement chat UI with message history and auto-scroll

**Acceptance Criteria**:
- User and CENTLI messages are visually distinct
- Auto-scroll to latest message works
- Timestamps are displayed
- UI is responsive on mobile

**Dependencies**: Story 1.1

**Agent Assignment**: CENTLI-Frontend-Agent

---

### Story 1.5: Implement Transaction Confirmation UI
**Priority**: Must Have  
**Estimation**: 1 hour  
**Epic**: User Interface

**Description**: Implement confirmation modal for transactions

**Acceptance Criteria**:
- Modal shows all transaction details
- Confirm/Cancel buttons work
- Success/Error feedback is clear
- Receipt is generated

**Dependencies**: Story 1.4

**Agent Assignment**: CENTLI-Frontend-Agent

---

### Story 1.6: Implement Product Catalog UI
**Priority**: Must Have  
**Estimation**: 1.5 hours  
**Epic**: User Interface

**Description**: Implement product grid with benefits badges

**Acceptance Criteria**:
- Product grid displays correctly
- Images load properly
- Benefits badges are clear
- Detail view shows all information
- Benefits comparison is easy to understand

**Dependencies**: Story 1.4

**Agent Assignment**: CENTLI-Frontend-Agent

---

### Story 1.7: Implement Image Upload UI
**Priority**: Could Have  
**Estimation**: 1 hour  
**Epic**: User Interface

**Description**: Implement image upload with preview

**Acceptance Criteria**:
- File picker opens correctly
- Image preview works
- Upload progresses and completes
- Image arrives at backend

**Dependencies**: Story 1.1

**Agent Assignment**: CENTLI-Frontend-Agent

---

## Story Execution Timeline

### Hour 1: Foundation Stories
- **Dev 1**: Story 1.1 (WebSocket Connection) - 1h
- **Dev 2**: Story 2.1 (Core Banking Accounts) - 1.5h
- **Dev 3**: Story 3.1 (AgentCore Setup) - 2h

### Hour 2: Core Features + Checkpoint 1
- **Dev 1**: Story 1.2 (Voice Input) - 1.5h
- **Dev 2**: Story 2.2 (P2P Transfers) - 2h
- **Dev 3**: Story 3.2 (Action Groups) - 2h
- **Checkpoint**: Infrastructure validation

### Hour 3-4: Feature Development
- **Dev 1**: Story 1.3 (Voice Output) - 1h, Story 1.4 (Chat) - 1.5h
- **Dev 2**: Story 2.4 (Marketplace Products) - 1.5h, Story 2.5 (Benefits) - 2h
- **Dev 3**: Story 3.3 (Nova Sonic) - 2h
- **Checkpoint (Hour 4)**: First integration test

### Hour 5-6: Integration Features
- **Dev 1**: Story 1.5 (Transaction Confirmation) - 1h, Story 1.6 (Product Catalog) - 1.5h
- **Dev 2**: Story 2.6 (Purchase Execution) - 1.5h
- **Dev 3**: Story 3.5 (Intent Recognition) - 1.5h, Story 3.6 (Managed Memory) - 1.5h
- **Checkpoint (Hour 6)**: Full integration test

### Hour 7-8: Testing & Optional Features
- **All Devs**: Integration testing, bug fixes, demo rehearsal
- **Optional**: Story 2.3 (CRM), Story 3.4 (Nova Canvas), Story 1.7 (Image Upload)

---

## Priority-Based Execution

### Must Have Stories (15 stories - 23.5 hours)

**Critical for Demo**:
1. Story 3.1: AgentCore Setup (2h)
2. Story 3.2: Action Groups Config (2h)
3. Story 3.3: Nova Sonic Voice (2h)
4. Story 3.5: Intent Recognition (1.5h)
5. Story 2.1: Core Banking Accounts (1.5h)
6. Story 2.2: P2P Transfers (2h)
7. Story 2.4: Marketplace Products (1.5h)
8. Story 2.5: Benefits Engine (2h)
9. Story 2.6: Purchase Execution (1.5h)
10. Story 1.1: WebSocket Connection (1h)
11. Story 1.2: Voice Input (1.5h)
12. Story 1.3: Voice Output (1h)
13. Story 1.4: Chat Interface (1.5h)
14. Story 1.5: Transaction Confirmation (1h)
15. Story 1.6: Product Catalog (1.5h)

**Total**: 23.5 hours → ~8 hours with 3 devs in parallel

---

### Should Have Stories (2 stories - 3 hours)

**Important but not critical**:
1. Story 3.6: Managed Memory (1.5h) - Enhances UX with context
2. Story 2.3: CRM Beneficiaries (1.5h) - Enables alias resolution

**Execution**: If time permits after Must Have stories

---

### Could Have Stories (2 stories - 2.5 hours)

**Nice to have**:
1. Story 3.4: Nova Canvas Images (1.5h) - Image processing
2. Story 1.7: Image Upload UI (1h) - Image upload interface

**Execution**: Only if ahead of schedule

---

## Story Dependencies Graph

```
Unit 1: Infrastructure (1h)
    |
    +-- Unit 2: AgentCore
    |       |
    |       +-- Story 3.1 (AgentCore Setup) [2h]
    |               |
    |               +-- Story 3.2 (Action Groups) [2h]
    |               +-- Story 3.3 (Nova Sonic) [2h]
    |               +-- Story 3.4 (Nova Canvas) [1.5h] (optional)
    |               +-- Story 3.5 (Intent Recognition) [1.5h]
    |               +-- Story 3.6 (Managed Memory) [1.5h]
    |
    +-- Unit 3: Action Groups
    |       |
    |       +-- Story 2.1 (Core Banking) [1.5h]
    |       |       |
    |       |       +-- Story 2.2 (P2P Transfers) [2h]
    |       |
    |       +-- Story 2.3 (CRM) [1.5h]
    |       |
    |       +-- Story 2.4 (Marketplace) [1.5h]
    |               |
    |               +-- Story 2.5 (Benefits) [2h]
    |                       |
    |                       +-- Story 2.6 (Purchase) [1.5h]
    |
    +-- Unit 4: Frontend
            |
            +-- Story 1.1 (WebSocket) [1h]
                    |
                    +-- Story 1.2 (Voice Input) [1.5h]
                    +-- Story 1.3 (Voice Output) [1h]
                    +-- Story 1.4 (Chat) [1.5h]
                    |       |
                    |       +-- Story 1.5 (Transaction Confirmation) [1h]
                    |       +-- Story 1.6 (Product Catalog) [1.5h]
                    |
                    +-- Story 1.7 (Image Upload) [1h] (optional)
```

---

## Story-to-Component Mapping

| Story | Component(s) | Methods Used |
|-------|-------------|--------------|
| 3.1 | AgentCore | agent configuration, managed memory setup |
| 3.2 | AgentCore | action group registration, OpenAPI schemas |
| 3.3 | AgentCore | process_voice_input, generate_voice_output |
| 3.4 | AgentCore | process_image_input |
| 3.5 | AgentCore | recognize_intent |
| 3.6 | AgentCore | manage_session |
| 2.1 | Core Banking Mock | get_balance, get_account, validate_funds |
| 2.2 | Core Banking Mock | execute_transfer, get_transactions |
| 2.3 | CRM Mock | search_beneficiary, add_beneficiary, get_frequent_beneficiaries |
| 2.4 | Marketplace Mock | list_products, get_product, search_products |
| 2.5 | Marketplace Mock | calculate_benefits |
| 2.6 | Marketplace Mock | execute_purchase, publish_payment_event |
| 1.1 | Orchestration Service | handle_connect, handle_disconnect, handle_message |
| 1.2 | Frontend | VoiceManager.start_recording, VoiceManager.stop_recording |
| 1.3 | Frontend | VoiceManager.play_audio |
| 1.4 | Frontend | ChatManager.add_message, ChatManager.auto_scroll |
| 1.5 | Frontend | TransactionManager.show_confirmation, show_receipt |
| 1.6 | Frontend | ProductCatalogManager.display_products, show_benefits_comparison |
| 1.7 | Frontend | ImageManager.upload_image |

---

## Agent-to-Story Assignment

### CENTLI-AgentCore-Agent (Dev 3)
- Story 3.1: Setup AWS Bedrock AgentCore
- Story 3.2: Configure Action Groups
- Story 3.3: Integrate Nova Sonic for Voice
- Story 3.4: Integrate Nova Canvas for Images
- Story 3.5: Implement Intent Recognition
- Story 3.6: Implement Managed Memory

**Total**: 6 stories, 10.5 hours

---

### CENTLI-Backend-Agent (Dev 2)
- Story 2.1: Implement Core Banking Mock - Accounts
- Story 2.2: Implement P2P Transfers
- Story 2.3: Implement CRM Mock - Beneficiaries
- Story 2.4: Implement Marketplace Mock - Products
- Story 2.5: Implement Benefits Engine
- Story 2.6: Implement Purchase Execution

**Total**: 6 stories, 10 hours

---

### CENTLI-Frontend-Agent (Dev 1)
- Story 1.1: Implement WebSocket Connection
- Story 1.2: Implement Voice Input UI
- Story 1.3: Implement Voice Output UI
- Story 1.4: Implement Chat Interface
- Story 1.5: Implement Transaction Confirmation UI
- Story 1.6: Implement Product Catalog UI
- Story 1.7: Implement Image Upload UI

**Total**: 7 stories, 8.5 hours

---

### CENTLI-Test-Agent (All Devs)
- Integration testing across all units
- End-to-end flow validation
- Demo rehearsal

**Execution**: Hours 7-8 (Build and Test phase)

---

## Story Completion Tracking

**Format**: Update checkboxes as stories complete

### Unit 2: AgentCore & Orchestration
- [ ] Story 3.1: Setup AWS Bedrock AgentCore
- [ ] Story 3.2: Configure Action Groups
- [ ] Story 3.3: Integrate Nova Sonic for Voice
- [ ] Story 3.4: Integrate Nova Canvas for Images (optional)
- [ ] Story 3.5: Implement Intent Recognition
- [ ] Story 3.6: Implement Managed Memory

### Unit 3: Action Groups
- [ ] Story 2.1: Implement Core Banking Mock - Accounts
- [ ] Story 2.2: Implement P2P Transfers
- [ ] Story 2.3: Implement CRM Mock - Beneficiaries
- [ ] Story 2.4: Implement Marketplace Mock - Products
- [ ] Story 2.5: Implement Benefits Engine
- [ ] Story 2.6: Implement Purchase Execution

### Unit 4: Frontend
- [ ] Story 1.1: Implement WebSocket Connection
- [ ] Story 1.2: Implement Voice Input UI
- [ ] Story 1.3: Implement Voice Output UI
- [ ] Story 1.4: Implement Chat Interface
- [ ] Story 1.5: Implement Transaction Confirmation UI
- [ ] Story 1.6: Implement Product Catalog UI
- [ ] Story 1.7: Implement Image Upload UI (optional)

---

**Document Status**: Complete  
**Created**: 2026-02-16  
**Stories Mapped**: 19 stories across 4 units  
**Agent Assignment**: 3 specialized agents + 1 testing agent
