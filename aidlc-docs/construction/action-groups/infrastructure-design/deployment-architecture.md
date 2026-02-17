# Deployment Architecture - Unit 3: Action Groups

## Document Information
- **Unit**: Unit 3 (Action Groups - Backend Services)
- **Stage**: Infrastructure Design
- **Created**: 2026-02-17
- **Context**: AWS deployment architecture for Action Groups

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud                               │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    Unit 2: AgentCore                      │ │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐           │ │
│  │  │ Connect  │    │Disconnect│    │ Message  │           │ │
│  │  │ Lambda   │    │ Lambda   │    │ Lambda   │           │ │
│  │  └──────────┘    └──────────┘    └────┬─────┘           │ │
│  └────────────────────────────────────────┼──────────────────┘ │
│                                           │                    │
│                                           ▼                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              EventBridge Event Bus                        │ │
│  │              (centli-event-bus)                           │ │
│  └───┬───────────────────┬───────────────────┬───────────────┘ │
│      │                   │                   │                 │
│      ▼                   ▼                   ▼                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │Core Banking │    │ Marketplace │    │     CRM     │       │
│  │Action Group │    │Action Group │    │Action Group │       │
│  │             │    │             │    │             │       │
│  │ 3 Lambdas   │    │ 3 Lambdas   │    │ 3 Lambdas   │       │
│  │ 2 Tables    │    │ 3 Tables    │    │ 1 Table     │       │
│  └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Banking Action Group Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              Core Banking Action Group                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EventBridge Event Bus                                          │
│         │                                                       │
│         ├──────────────┬──────────────┬──────────────┐         │
│         │              │              │              │         │
│         ▼              ▼              ▼              │         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐        │         │
│  │ Balance  │   │ Transfer │   │Transaction│        │         │
│  │ Lambda   │   │ Lambda   │   │  Lambda  │        │         │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘        │         │
│       │              │              │               │         │
│       │              │              │               │         │
│       ▼              ▼              ▼               │         │
│  ┌─────────────────────────────────────────┐       │         │
│  │         DynamoDB Tables                 │       │         │
│  │  ┌──────────────┐  ┌──────────────┐    │       │         │
│  │  │   Accounts   │  │ Transactions │    │       │         │
│  │  │              │  │              │    │       │         │
│  │  │ PK: user_id  │  │PK: account_id│    │       │         │
│  │  │ SK: acct_id  │  │SK: timestamp │    │       │         │
│  │  │              │  │GSI: user_id  │    │       │         │
│  │  └──────────────┘  └──────────────┘    │       │         │
│  └─────────────────────────────────────────┘       │         │
│                                                     │         │
│  ┌─────────────────────────────────────────┐       │         │
│  │         CloudWatch Logs                 │       │         │
│  │  /aws/lambda/centli-core-banking-*      │       │         │
│  └─────────────────────────────────────────┘       │         │
│                                                     │         │
│                                                     ▼         │
│                              EventBridge Event Bus            │
│                              (response events)                │
│                                                               │
└─────────────────────────────────────────────────────────────────┘
```

### 2.1 Balance Query Flow

```
1. AgentCore publishes BALANCE_QUERY event
   ↓
2. EventBridge routes to Balance Lambda
   ↓
3. Balance Lambda queries centli-accounts table
   ↓
4. Balance Lambda publishes BALANCE_RESPONSE event
   ↓
5. EventBridge routes back to AgentCore
```

### 2.2 Transfer Flow

```
1. AgentCore publishes TRANSFER_REQUEST event
   ↓
2. EventBridge routes to Transfer Lambda
   ↓
3. Transfer Lambda:
   a. Reads from_account (strong consistency)
   b. Validates sufficient funds
   c. Updates from_account balance (optimistic locking)
   d. Updates to_account balance (optimistic locking)
   e. Creates transaction records
   ↓
4. Transfer Lambda publishes TRANSFER_COMPLETED event
   ↓
5. EventBridge routes back to AgentCore
```

---

## 3. Marketplace Action Group Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              Marketplace Action Group                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EventBridge Event Bus                                          │
│         │                                                       │
│         ├──────────────┬──────────────┬──────────────┐         │
│         │              │              │              │         │
│         ▼              ▼              ▼              │         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐        │         │
│  │ Catalog  │   │ Benefits │   │ Purchase │        │         │
│  │ Lambda   │   │ Lambda   │   │ Lambda   │        │         │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘        │         │
│       │              │              │               │         │
│       │              │              │               │         │
│       ▼              ▼              ▼               │         │
│  ┌─────────────────────────────────────────┐       │         │
│  │         DynamoDB Tables                 │       │         │
│  │  ┌──────────┐ ┌──────────┐ ┌─────────┐ │       │         │
│  │  │ Products │ │Purchases │ │Retailers│ │       │         │
│  │  │          │ │          │ │         │ │       │         │
│  │  │PK: prod  │ │PK: user  │ │PK: ret  │ │       │         │
│  │  │SK: ret   │ │SK: time  │ │         │ │       │         │
│  │  └──────────┘ └──────────┘ └─────────┘ │       │         │
│  └─────────────────────────────────────────┘       │         │
│                                                     │         │
│                                                     ▼         │
│                              EventBridge Event Bus            │
│                              (PAYMENT_REQUEST to Core Banking)│
│                                                               │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 Purchase Flow (Success Path)

```
1. AgentCore publishes PURCHASE_REQUEST event
   ↓
2. EventBridge routes to Purchase Lambda
   ↓
3. Purchase Lambda:
   a. Validates product availability
   b. Reserves inventory (update stock)
   c. Publishes PAYMENT_REQUEST event
   ↓
4. EventBridge routes to Core Banking Transfer Lambda
   ↓
5. Transfer Lambda processes payment
   ↓
6. Transfer Lambda publishes PAYMENT_COMPLETED event
   ↓
7. EventBridge routes back to Purchase Lambda
   ↓
8. Purchase Lambda:
   a. Creates purchase record
   b. Publishes PURCHASE_CONFIRMED event
   ↓
9. EventBridge routes back to AgentCore
```

### 3.2 Purchase Flow (Failure Path with Compensation)

```
1-4. Same as success path
   ↓
5. Transfer Lambda detects insufficient funds
   ↓
6. Transfer Lambda publishes PAYMENT_FAILED event
   ↓
7. EventBridge routes back to Purchase Lambda
   ↓
8. Purchase Lambda (compensation):
   a. Releases reserved inventory
   b. Publishes PURCHASE_FAILED event
   ↓
9. EventBridge routes back to AgentCore
```

---

## 4. CRM Action Group Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              CRM Action Group                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EventBridge Event Bus                                          │
│         │                                                       │
│         ├──────────────┬──────────────┬──────────────┐         │
│         │              │              │              │         │
│         ▼              ▼              ▼              │         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐        │         │
│  │ Resolve  │   │   Get    │   │   Add    │        │         │
│  │  Alias   │   │Benefic.  │   │Benefic.  │        │         │
│  │ Lambda   │   │ Lambda   │   │ Lambda   │        │         │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘        │         │
│       │              │              │               │         │
│       │              │              │               │         │
│       ▼              ▼              ▼               │         │
│  ┌─────────────────────────────────────────┐       │         │
│  │         DynamoDB Table                  │       │         │
│  │  ┌──────────────────────────────┐       │       │         │
│  │  │      Beneficiaries           │       │       │         │
│  │  │                              │       │       │         │
│  │  │  PK: user_id                 │       │       │         │
│  │  │  SK: beneficiary_id          │       │       │         │
│  │  │  GSI: alias_lower + user_id  │       │       │         │
│  │  └──────────────────────────────┘       │       │         │
│  └─────────────────────────────────────────┘       │         │
│                                                     │         │
│                                                     ▼         │
│                              EventBridge Event Bus            │
│                              (response events)                │
│                                                               │
└─────────────────────────────────────────────────────────────────┘
```

### 4.1 Alias Resolution Flow

```
1. AgentCore publishes ALIAS_RESOLUTION_REQUEST event
   Data: {"alias": "mi hermano", "user_id": "user-123"}
   ↓
2. EventBridge routes to Resolve Alias Lambda
   ↓
3. Resolve Alias Lambda:
   a. Normalizes alias (lowercase, trim)
   b. Queries GSI by alias_lower + user_id
   c. Performs fuzzy matching if exact match fails
   d. Returns beneficiary account_id
   ↓
4. Resolve Alias Lambda publishes ALIAS_RESOLUTION_RESPONSE event
   Data: {"beneficiary_id": "ben-456", "account_id": "acc-789"}
   ↓
5. EventBridge routes back to AgentCore
```

---

## 5. Cross-Action Group Integration

### 5.1 Transfer with Alias Resolution

```
User: "Transfiere 100 pesos a mi hermano"

1. AgentCore → ALIAS_RESOLUTION_REQUEST → CRM
2. CRM → ALIAS_RESOLUTION_RESPONSE → AgentCore
3. AgentCore → TRANSFER_REQUEST → Core Banking
4. Core Banking → TRANSFER_COMPLETED → AgentCore
```

### 5.2 Purchase with Payment

```
User: "Compra una laptop con MSI 6 meses"

1. AgentCore → PURCHASE_REQUEST → Marketplace
2. Marketplace → PAYMENT_REQUEST → Core Banking
3. Core Banking → PAYMENT_COMPLETED → Marketplace
4. Marketplace → PURCHASE_CONFIRMED → AgentCore
```

---

## 6. IAM Architecture

### 6.1 Lambda Execution Roles

Each Lambda has dedicated IAM role:

```
┌─────────────────────────────────────────────────────────────────┐
│                    IAM Roles                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CoreBankingBalanceRole                                         │
│    ├─ DynamoDB: GetItem, Query (centli-accounts)               │
│    ├─ EventBridge: PutEvents (centli-event-bus)                │
│    └─ CloudWatch Logs: CreateLogGroup, PutLogEvents            │
│                                                                 │
│  CoreBankingTransferRole                                        │
│    ├─ DynamoDB: GetItem, UpdateItem, PutItem                   │
│    │   (centli-accounts, centli-transactions)                  │
│    ├─ EventBridge: PutEvents (centli-event-bus)                │
│    └─ CloudWatch Logs: CreateLogGroup, PutLogEvents            │
│                                                                 │
│  MarketplacePurchaseRole                                        │
│    ├─ DynamoDB: GetItem, UpdateItem, PutItem                   │
│    │   (centli-products, centli-purchases)                     │
│    ├─ EventBridge: PutEvents (centli-event-bus)                │
│    └─ CloudWatch Logs: CreateLogGroup, PutLogEvents            │
│                                                                 │
│  CRMResolveAliasRole                                            │
│    ├─ DynamoDB: Query (centli-beneficiaries + GSI)             │
│    ├─ EventBridge: PutEvents (centli-event-bus)                │
│    └─ CloudWatch Logs: CreateLogGroup, PutLogEvents            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Least Privilege Principle

Each role has minimal permissions:
- Read-only Lambdas: GetItem, Query only
- Write Lambdas: GetItem, UpdateItem, PutItem only
- No DeleteItem permissions (data safety)
- No Scan permissions (performance)

---

## 7. Monitoring Architecture

### 7.1 CloudWatch Logs

```
┌─────────────────────────────────────────────────────────────────┐
│                    CloudWatch Logs                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Log Groups (9 total):                                          │
│    /aws/lambda/centli-core-banking-balance                      │
│    /aws/lambda/centli-core-banking-transfer                     │
│    /aws/lambda/centli-core-banking-transactions                 │
│    /aws/lambda/centli-marketplace-catalog                       │
│    /aws/lambda/centli-marketplace-benefits                      │
│    /aws/lambda/centli-marketplace-purchase                      │
│    /aws/lambda/centli-crm-resolve-alias                         │
│    /aws/lambda/centli-crm-get-beneficiaries                     │
│    /aws/lambda/centli-crm-add-beneficiary                       │
│                                                                 │
│  Retention: 7 days                                              │
│  Format: Structured JSON with correlation_id                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 CloudWatch Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│                    CloudWatch Metrics                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Lambda Metrics:                                                │
│    - Invocations (count)                                        │
│    - Duration (ms, p50/p95/p99)                                 │
│    - Errors (count)                                             │
│    - Throttles (count)                                          │
│    - ConcurrentExecutions (count)                               │
│                                                                 │
│  DynamoDB Metrics:                                              │
│    - ConsumedReadCapacityUnits                                  │
│    - ConsumedWriteCapacityUnits                                 │
│    - UserErrors (count)                                         │
│    - SystemErrors (count)                                       │
│                                                                 │
│  EventBridge Metrics:                                           │
│    - Invocations (count)                                        │
│    - FailedInvocations (count)                                  │
│    - TriggeredRules (count)                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Deployment Architecture

### 8.1 SAM Template Structure

```
template.yaml
├── Parameters (Environment, LogLevel)
├── Globals (Runtime, Timeout, Memory, Tags)
├── Resources
│   ├── Unit 1: Infrastructure Foundation
│   │   ├── EventBridge Event Bus
│   │   ├── S3 Assets Bucket
│   │   └── IAM Execution Role
│   ├── Unit 2: AgentCore & Orchestration
│   │   ├── WebSocket API
│   │   ├── Sessions Table
│   │   └── 3 Lambda Functions
│   └── Unit 3: Action Groups
│       ├── 6 DynamoDB Tables
│       ├── 9 Lambda Functions
│       └── 9 EventBridge Rules
└── Outputs (WebSocket URL, Table Names, Function ARNs)
```

### 8.2 Deployment Commands

```bash
# Validate template
sam validate

# Build application
sam build

# Deploy to AWS
sam deploy \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --stack-name centli-hackathon \
  --capabilities CAPABILITY_NAMED_IAM

# Verify deployment
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --query 'Stacks[0].StackStatus'
```

---

## 9. Data Flow Architecture

### 9.1 End-to-End Flow

```
┌─────────────┐
│   User      │
│  (Frontend) │
└──────┬──────┘
       │ WebSocket
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Unit 2: AgentCore                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Message Lambda                                          │   │
│  │    ├─ Receives user message                             │   │
│  │    ├─ Invokes Bedrock AgentCore                         │   │
│  │    └─ Publishes event to EventBridge                    │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              EventBridge Event Bus                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Routes events based on detail-type:                    │   │
│  │    - BALANCE_QUERY → Core Banking Balance               │   │
│  │    - TRANSFER_REQUEST → Core Banking Transfer           │   │
│  │    - PURCHASE_REQUEST → Marketplace Purchase            │   │
│  │    - ALIAS_RESOLUTION_REQUEST → CRM Resolve Alias       │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│Core Banking  │  │ Marketplace  │  │     CRM      │
│Action Group  │  │ Action Group │  │ Action Group │
│              │  │              │  │              │
│ Processes    │  │ Processes    │  │ Processes    │
│ event        │  │ event        │  │ event        │
│              │  │              │  │              │
│ Reads/Writes │  │ Reads/Writes │  │ Reads/Writes │
│ DynamoDB     │  │ DynamoDB     │  │ DynamoDB     │
│              │  │              │  │              │
│ Publishes    │  │ Publishes    │  │ Publishes    │
│ result event │  │ result event │  │ result event │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              EventBridge Event Bus                              │
│  Routes result events back to AgentCore                         │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Unit 2: AgentCore                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Message Lambda                                          │   │
│  │    ├─ Receives result event                             │   │
│  │    ├─ Formats response                                  │   │
│  │    └─ Sends to user via WebSocket                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────────┘
                         │ WebSocket
                         ▼
                   ┌─────────────┐
                   │   User      │
                   │  (Frontend) │
                   └─────────────┘
```

---

## 10. Scalability Architecture

### 10.1 Horizontal Scaling

All components scale horizontally:

**Lambda**: Auto-scales to handle concurrent requests
- No configuration needed
- Scales from 0 to 1000 concurrent executions (account limit)

**DynamoDB**: Auto-scales with on-demand mode
- No capacity planning needed
- Handles spikes automatically

**EventBridge**: Managed service, scales automatically
- Handles millions of events per second

### 10.2 Vertical Scaling

Lambda memory can be adjusted per function:
- Current: 512 MB
- Range: 128 MB to 10,240 MB
- Adjust based on performance testing

---

## 11. Security Architecture

### 11.1 Network Security

**No Public Endpoints**:
- All Lambdas are private (no public URLs)
- Triggered only by EventBridge
- No VPC required (serverless)

**Encryption**:
- DynamoDB: Encryption at rest (AWS managed keys)
- EventBridge: Encryption in transit (TLS 1.2+)
- CloudWatch Logs: Encryption at rest (AWS managed keys)

### 11.2 Access Control

**IAM Roles**:
- Each Lambda has dedicated role
- Least privilege permissions
- No cross-account access

**EventBridge**:
- IAM-based authentication
- No public event publishing

---

## 12. Disaster Recovery

### 12.1 Backup Strategy

**DynamoDB**:
- Point-in-time recovery: Disabled (demo context)
- On-demand backups: Not configured (demo context)
- Data can be re-seeded from scripts

**Lambda**:
- Code stored in S3 by SAM
- Can be redeployed from template

### 12.2 Recovery Strategy

**Full Stack Recovery**:
```bash
# Delete stack
sam delete --stack-name centli-hackathon

# Redeploy
sam build && sam deploy

# Re-seed data
python scripts/seed_all.py
```

**Recovery Time Objective (RTO)**: ~10 minutes  
**Recovery Point Objective (RPO)**: Last deployment

---

## 13. Next Steps

1. ✅ Deployment Architecture complete
2. ⏳ Update template.yaml with Unit 3 resources
3. ⏳ Generate Code Generation Plan
4. ⏳ Implement Lambda functions
5. ⏳ Deploy and test

---

**Document Status**: Complete  
**Approved By**: [Pending approval]  
**Next Stage**: Code Generation
