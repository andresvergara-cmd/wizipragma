# Unit of Work Dependencies - CENTLI

## Dependency Matrix

| From Unit | To Unit | Dependency Type | Communication | Required For | Can Start Without |
|-----------|---------|-----------------|---------------|--------------|-------------------|
| Unit 2 (AgentCore) | Unit 1 (Infrastructure) | Hard | N/A | EventBridge bus, S3 bucket | No |
| Unit 3 (Action Groups) | Unit 1 (Infrastructure) | Hard | N/A | EventBridge bus, DynamoDB tables | No |
| Unit 4 (Frontend) | Unit 1 (Infrastructure) | Hard | N/A | S3 bucket, WebSocket API | No |
| Unit 2 (AgentCore) | Unit 3 (Action Groups) | Soft | EventBridge (async) | Action execution | Yes (with mocks) |
| Unit 4 (Frontend) | Unit 2 (AgentCore) | Soft | WebSocket (sync) | Message processing | Yes (with mocks) |
| Unit 3 (Marketplace) | Unit 3 (Core Banking) | Soft | EventBridge (async) | Payment processing | Yes (with mocks) |

**Legend**:
- **Hard Dependency**: Must be deployed first, blocking dependency
- **Soft Dependency**: Can start with mocks/stubs, integration later

---

## Dependency Graph

```
[Unit 1: Infrastructure]
        |
        | (provides EventBridge, S3, IAM)
        |
        +-- Hard --> [Unit 2: AgentCore & Orchestration]
        |                   |
        |                   | EventBridge (async)
        |                   v
        +-- Hard --> [Unit 3: Action Groups]
        |                   |
        |                   | (internal: Marketplace → Core Banking)
        |                   |
        +-- Hard --> [Unit 4: Frontend]
                            |
                            | WebSocket (sync)
                            v
                     [Unit 2: AgentCore]
```

---

## Critical Path Analysis

**No Critical Path**: All units can start in parallel (Q9: Opción D)

**Rationale**:
- Unit 1 (Infrastructure) deploys quickly (~1 hour)
- Units 2, 3, 4 can start with local mocks/stubs
- Integration happens at checkpoints (hours 2, 4, 6)

**Parallel Development Strategy**:
1. **Hour 1**: All devs deploy Unit 1 together, then start their units with mocks
2. **Hour 2**: Checkpoint 1 - Verify infrastructure, basic connectivity
3. **Hour 4**: Checkpoint 2 - First integration (AgentCore + Action Groups)
4. **Hour 6**: Checkpoint 3 - Full integration (all units)
5. **Hours 7-8**: Testing and demo prep

---

## Integration Checkpoints

### Checkpoint 1: Hour 2 - Infrastructure Validation

**Goal**: Verify base infrastructure is deployed and accessible

**Validation**:
- [ ] EventBridge bus created and accessible
- [ ] S3 bucket created with proper permissions
- [ ] DynamoDB tables created (sessions, accounts, transactions, etc.)
- [ ] IAM roles configured correctly
- [ ] WebSocket API Gateway deployed
- [ ] CloudWatch log groups created

**Success Criteria**: All infrastructure resources accessible via AWS Console/CLI

**Rollback**: If infrastructure fails, all devs pause and fix together

---

### Checkpoint 2: Hour 4 - First Integration

**Goal**: Verify AgentCore can communicate with Action Groups via EventBridge

**Validation**:
- [ ] AgentCore can publish events to EventBridge
- [ ] Action Groups receive events from EventBridge
- [ ] Action Groups can publish response events
- [ ] AgentCore receives response events
- [ ] Basic P2P transfer flow works end-to-end (mock data)

**Test Scenario**: 
```
AgentCore publishes TRANSFER event
→ EventBridge routes to Core Banking
→ Core Banking executes mock transfer
→ Core Banking publishes response event
→ AgentCore receives response
```

**Success Criteria**: Event flow working, logs show successful routing

**Rollback**: If integration fails, identify bottleneck (EventBridge rules, IAM permissions, Lambda triggers)

---

### Checkpoint 3: Hour 6 - Full Integration

**Goal**: Verify all units working together end-to-end

**Validation**:
- [ ] Frontend can connect to WebSocket API
- [ ] Frontend can send messages to Orchestration Service
- [ ] Orchestration Service routes to AgentCore
- [ ] AgentCore processes intent and invokes Action Groups
- [ ] Action Groups execute business logic
- [ ] Responses flow back to Frontend
- [ ] Voice input/output working (Nova Sonic)
- [ ] Product purchase flow working (Marketplace + Core Banking)

**Test Scenarios**:
1. **P2P Transfer**: User says "Envíale 50 lucas a mi hermano" → Transfer executes → Confirmation displayed
2. **Product Purchase**: User selects laptop → Benefits calculated → Purchase executes → Confirmation displayed

**Success Criteria**: Both priority flows working end-to-end

**Rollback**: If full integration fails, identify failing unit and simplify

---

## Data Flow Dependencies

### Flow 1: User Message → AgentCore → Action Group → Response

```
[Frontend]
    | 1. WebSocket message
    v
[Orchestration Service]
    | 2. Invoke AgentCore
    v
[AgentCore]
    | 3. Publish action event
    v
[EventBridge]
    | 4. Route to Action Group
    v
[Action Group Lambda]
    | 5. Execute business logic
    | 6. Query/Update DynamoDB
    v
[DynamoDB]
    | 7. Return data
    v
[Action Group Lambda]
    | 8. Publish response event
    v
[EventBridge]
    | 9. Route to AgentCore
    v
[AgentCore]
    | 10. Generate response
    v
[Orchestration Service]
    | 11. Send via WebSocket
    v
[Frontend]
```

**Dependencies**:
- Step 1-2: Frontend → Orchestration Service (Unit 4 → Unit 2)
- Step 3-4: AgentCore → EventBridge (Unit 2 → Unit 1)
- Step 4-5: EventBridge → Action Group (Unit 1 → Unit 3)
- Step 8-9: Action Group → EventBridge (Unit 3 → Unit 1)
- Step 9-10: EventBridge → AgentCore (Unit 1 → Unit 2)
- Step 11: Orchestration Service → Frontend (Unit 2 → Unit 4)

---

### Flow 2: Cross-Unit Communication (Marketplace → Core Banking)

```
[Marketplace Lambda]
    | 1. Publish payment event
    v
[EventBridge]
    | 2. Route to Core Banking
    v
[Core Banking Lambda]
    | 3. Process payment
    | 4. Update account balance
    v
[DynamoDB: Accounts]
    | 5. Return result
    v
[Core Banking Lambda]
    | 6. Publish payment response
    v
[EventBridge]
    | 7. Route to Marketplace
    v
[Marketplace Lambda]
    | 8. Complete purchase
    v
[DynamoDB: Purchases]
```

**Dependencies**:
- Internal to Unit 3 (Action Groups)
- Both Lambdas must be deployed
- EventBridge rules must route payment events correctly

---

## Deployment Dependencies

### Deployment Order (Recommended)

**Phase 1: Infrastructure** (Hour 1)
1. Deploy Unit 1 (Infrastructure Foundation)
   - Base SAM template
   - EventBridge bus
   - S3 bucket
   - IAM roles

**Phase 2: Backend Services** (Hours 1-2, parallel)
2. Deploy Unit 2 (AgentCore & Orchestration)
   - Orchestration Service Lambdas
   - AgentCore configuration
   - Managed Memory setup
3. Deploy Unit 3 (Action Groups)
   - Core Banking Lambda
   - Marketplace Lambda
   - CRM Lambda
   - DynamoDB tables

**Phase 3: Frontend** (Hours 1-2, parallel)
4. Deploy Unit 4 (Frontend)
   - Upload static files to S3
   - Configure WebSocket endpoint

**Note**: Units 2, 3, 4 can deploy in parallel after Unit 1 completes

---

### Nested Template Structure

```yaml
# base-template.yaml (Unit 1)
Resources:
  EventBridge:
    Type: AWS::Events::EventBus
  
  S3Bucket:
    Type: AWS::S3::Bucket
  
  AgentCoreStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: ./agentcore-template.yaml
      Parameters:
        EventBusName: !Ref EventBridge
        AssetsBucket: !Ref S3Bucket
  
  ActionGroupsStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: ./action-groups-template.yaml
      Parameters:
        EventBusName: !Ref EventBridge
```

**Benefits**:
- Modular deployment
- Each unit can be updated independently
- Clear dependency management via parameters

---

## Runtime Dependencies

### Service-to-Service Communication

| Service | Depends On | Protocol | Timeout | Retry |
|---------|-----------|----------|---------|-------|
| Orchestration Service | AgentCore | Bedrock API | 30s | 3x |
| AgentCore | EventBridge | PutEvents API | 5s | 3x |
| Action Groups | DynamoDB | SDK | 5s | Built-in |
| Action Groups | EventBridge | PutEvents API | 5s | 3x |
| Frontend | WebSocket API | WSS | 30s | Auto-reconnect |

### External Service Dependencies

| Unit | External Service | Purpose | Fallback |
|------|-----------------|---------|----------|
| Unit 2 | AWS Bedrock AgentCore | AI orchestration | Bedrock Converse |
| Unit 2 | AWS Bedrock Nova Sonic | Voice processing | Text-only mode |
| Unit 2 | AWS Bedrock Nova Canvas | Image processing | Skip images |
| All | AWS CloudWatch | Logging | Local logs |
| All | AWS IAM | Authorization | Pre-configured roles |

---

## Failure Scenarios & Mitigation

### Scenario 1: Unit 1 (Infrastructure) Fails

**Impact**: All units blocked (hard dependency)

**Mitigation**:
- All devs pause and fix together
- Verify AWS credentials and permissions
- Check CloudFormation stack events for errors
- Simplify template if needed (remove optional resources)

**Rollback**: Delete stack and redeploy

---

### Scenario 2: Unit 2 (AgentCore) Fails

**Impact**: No AI orchestration, system non-functional

**Mitigation**:
- Fallback to Bedrock Converse (simpler, no Action Groups)
- Manual routing in Orchestration Service
- Simplify intent recognition

**Rollback**: Use text-only mode, skip voice/images

---

### Scenario 3: Unit 3 (Action Groups) Fails

**Impact**: No business logic, transactions don't work

**Mitigation**:
- Use in-memory mocks (no DynamoDB)
- Hardcoded responses for demo
- Focus on one Action Group (Core Banking for P2P)

**Rollback**: Simplify to single Action Group

---

### Scenario 4: Unit 4 (Frontend) Fails

**Impact**: No user interface

**Mitigation**:
- Use Postman/curl for testing backend
- Simple HTML form (no fancy UI)
- Focus on backend demo

**Rollback**: Command-line demo

---

## Testing Dependencies

### Unit Tests (Per Unit)

- **Unit 2**: Test Orchestration Service Lambdas independently
- **Unit 3**: Test Action Group Lambdas with mock DynamoDB
- **Unit 4**: Test Frontend modules with mock WebSocket

**No Dependencies**: Each unit tests independently

---

### Integration Tests (Cross-Unit)

**Test 1: AgentCore → Action Groups**
- Dependencies: Unit 1, Unit 2, Unit 3
- Validates: EventBridge routing, Action Group invocation

**Test 2: Frontend → Backend**
- Dependencies: Unit 1, Unit 2, Unit 4
- Validates: WebSocket communication, message routing

**Test 3: End-to-End P2P Transfer**
- Dependencies: All units
- Validates: Complete flow from user input to transaction

**Test 4: End-to-End Product Purchase**
- Dependencies: All units
- Validates: Marketplace + Core Banking integration

---

## Dependency Resolution Strategy

**Strategy**: Parallel development with contract-based mocks (Q4: Opción B)

**Implementation**:
1. **Define contracts first** (integration-contracts in unit-of-work.md)
2. **Each unit implements mocks** for dependencies
3. **Integration at checkpoints** replaces mocks with real implementations
4. **Continuous testing** validates contracts

**Example**:
- Unit 2 (AgentCore) starts with mock Action Group responses
- Unit 3 (Action Groups) starts with mock EventBridge events
- At Checkpoint 2 (Hour 4), replace mocks with real EventBridge integration

---

**Document Status**: Complete  
**Created**: 2026-02-16  
**Dependencies**: 4 units with clear dependency matrix and integration strategy  
**Strategy**: Parallel development with contract-based mocks and 3 integration checkpoints
