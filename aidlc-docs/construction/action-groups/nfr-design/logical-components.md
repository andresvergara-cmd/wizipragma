# Logical Components - Unit 3: Action Groups

## Document Information
- **Unit**: Unit 3 (Action Groups - Backend Services)
- **Stage**: NFR Design
- **Created**: 2026-02-17
- **Context**: Logical architecture for Action Groups

---

## 1. Component Overview

Unit 3 consists of 3 Action Groups, each with multiple Lambda functions and DynamoDB tables.

```
Action Groups (Unit 3)
├── Core Banking Action Group
│   ├── Balance Lambda
│   ├── Transfer Lambda
│   ├── Transactions Lambda
│   ├── Accounts Table
│   └── Transactions Table
├── Marketplace Action Group
│   ├── Catalog Lambda
│   ├── Benefits Lambda
│   ├── Purchase Lambda
│   ├── Products Table
│   ├── Purchases Table
│   └── Retailers Table
└── CRM Action Group
    ├── Resolve Alias Lambda
    ├── Get Beneficiaries Lambda
    ├── Add Beneficiary Lambda
    └── Beneficiaries Table
```

---

## 2. Core Banking Action Group

### 2.1 Components

**Lambda Functions**:
1. **centli-core-banking-balance**
   - Purpose: Query account balance
   - Trigger: EventBridge event (BALANCE_QUERY)
   - Output: EventBridge event (BALANCE_RESPONSE)

2. **centli-core-banking-transfer**
   - Purpose: Execute money transfer
   - Trigger: EventBridge event (TRANSFER_REQUEST)
   - Output: EventBridge event (TRANSFER_COMPLETED / TRANSFER_FAILED)

3. **centli-core-banking-transactions**
   - Purpose: Query transaction history
   - Trigger: EventBridge event (TRANSACTIONS_QUERY)
   - Output: EventBridge event (TRANSACTIONS_RESPONSE)

**DynamoDB Tables**:
1. **centli-accounts**
   - Purpose: Store user bank accounts
   - Access Pattern: Get/Update account by user_id + account_id

2. **centli-transactions**
   - Purpose: Store transaction history
   - Access Pattern: Query by account_id, Query by user_id (GSI)

### 2.2 Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│         Core Banking Action Group                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │   Balance    │      │   Transfer   │               │
│  │   Lambda     │      │   Lambda     │               │
│  └──────┬───────┘      └──────┬───────┘               │
│         │                     │                        │
│         │                     │                        │
│         ▼                     ▼                        │
│  ┌─────────────────────────────────┐                  │
│  │      centli-accounts            │                  │
│  │  PK: user_id  SK: account_id    │                  │
│  └─────────────────────────────────┘                  │
│                                                         │
│  ┌──────────────┐                                      │
│  │ Transactions │                                      │
│  │   Lambda     │                                      │
│  └──────┬───────┘                                      │
│         │                                              │
│         ▼                                              │
│  ┌─────────────────────────────────┐                  │
│  │    centli-transactions          │                  │
│  │  PK: account_id  SK: timestamp  │                  │
│  │  GSI: user_id                   │                  │
│  └─────────────────────────────────┘                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Responsibilities

- Manage user bank accounts
- Execute transfers with validation
- Track transaction history
- Enforce business rules (balance checks, limits)
- Publish events for audit and integration

---

## 3. Marketplace Action Group

### 3.1 Components

**Lambda Functions**:
1. **centli-marketplace-catalog**
   - Purpose: Query product catalog
   - Trigger: EventBridge event (CATALOG_QUERY)
   - Output: EventBridge event (CATALOG_RESPONSE)

2. **centli-marketplace-benefits**
   - Purpose: Calculate product benefits
   - Trigger: EventBridge event (BENEFITS_QUERY)
   - Output: EventBridge event (BENEFITS_RESPONSE)

3. **centli-marketplace-purchase**
   - Purpose: Execute product purchase
   - Trigger: EventBridge event (PURCHASE_REQUEST)
   - Output: EventBridge event (PURCHASE_COMPLETED / PURCHASE_FAILED)

**DynamoDB Tables**:
1. **centli-products**
   - Purpose: Store product catalog
   - Access Pattern: Get product by product_id, Query by retailer_id

2. **centli-purchases**
   - Purpose: Store purchase history
   - Access Pattern: Query by user_id

3. **centli-retailers**
   - Purpose: Store retailer information
   - Access Pattern: Get retailer by retailer_id

### 3.2 Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│         Marketplace Action Group                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │   Catalog    │      │   Benefits   │               │
│  │   Lambda     │      │   Lambda     │               │
│  └──────┬───────┘      └──────┬───────┘               │
│         │                     │                        │
│         ▼                     ▼                        │
│  ┌─────────────────────────────────┐                  │
│  │      centli-products            │                  │
│  │  PK: product_id  SK: retailer   │                  │
│  └─────────────────────────────────┘                  │
│                                                         │
│  ┌──────────────┐                                      │
│  │   Purchase   │                                      │
│  │   Lambda     │                                      │
│  └──────┬───────┘                                      │
│         │                                              │
│         ├──────────────┐                               │
│         ▼              ▼                               │
│  ┌──────────┐   ┌──────────┐                          │
│  │ Purchases│   │Retailers │                          │
│  │  Table   │   │  Table   │                          │
│  └──────────┘   └──────────┘                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Responsibilities

- Provide product catalog with pricing
- Calculate benefits (MSI, cashback, points)
- Execute purchases with inventory management
- Integrate with Core Banking for payments
- Track purchase history

---

## 4. CRM Action Group

### 4.1 Components

**Lambda Functions**:
1. **centli-crm-resolve-alias**
   - Purpose: Resolve beneficiary alias to account
   - Trigger: EventBridge event (ALIAS_RESOLUTION_REQUEST)
   - Output: EventBridge event (ALIAS_RESOLUTION_RESPONSE)

2. **centli-crm-get-beneficiaries**
   - Purpose: List user beneficiaries
   - Trigger: EventBridge event (BENEFICIARIES_QUERY)
   - Output: EventBridge event (BENEFICIARIES_RESPONSE)

3. **centli-crm-add-beneficiary**
   - Purpose: Add new beneficiary
   - Trigger: EventBridge event (ADD_BENEFICIARY_REQUEST)
   - Output: EventBridge event (BENEFICIARY_ADDED)

**DynamoDB Tables**:
1. **centli-beneficiaries**
   - Purpose: Store user beneficiaries and aliases
   - Access Pattern: Get by user_id + beneficiary_id, Query by alias (GSI)

### 4.2 Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│         CRM Action Group                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │ Resolve Alias│      │     Get      │               │
│  │   Lambda     │      │Beneficiaries │               │
│  └──────┬───────┘      │   Lambda     │               │
│         │              └──────┬───────┘               │
│         │                     │                        │
│         ▼                     ▼                        │
│  ┌─────────────────────────────────┐                  │
│  │    centli-beneficiaries         │                  │
│  │  PK: user_id  SK: beneficiary   │                  │
│  │  GSI: alias                     │                  │
│  └─────────────────────────────────┘                  │
│                     ▲                                  │
│                     │                                  │
│  ┌──────────────────┘                                 │
│  │  Add Beneficiary                                   │
│  │     Lambda                                         │
│  └──────────────┘                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.3 Responsibilities

- Manage user beneficiaries
- Resolve natural language aliases ("mi hermano" → Juan López)
- Support semantic matching for aliases
- Validate beneficiary data
- Track beneficiary relationships

---

## 5. Cross-Cutting Components

### 5.1 Shared Utilities

**Component**: Python utility module (shared across all Lambdas)

**Modules**:
```python
# utils/
├── logger.py          # Structured logging with PII masking
├── dynamodb.py        # DynamoDB helper functions
├── eventbridge.py     # EventBridge publish helper
├── retry.py           # Retry logic with backoff
├── idempotency.py     # Idempotency checking
└── validation.py      # Input validation
```

**Usage**:
```python
from utils.logger import StructuredLogger
from utils.dynamodb import retry_with_backoff
from utils.eventbridge import publish_event

logger = StructuredLogger('core-banking-balance', correlation_id)
logger.info('Processing balance query')
```

### 5.2 EventBridge Event Bus

**Component**: centli-event-bus (from Unit 1)

**Purpose**: Central event routing for all Action Groups

**Event Types**:
- Core Banking: BALANCE_QUERY, TRANSFER_REQUEST, TRANSACTIONS_QUERY
- Marketplace: CATALOG_QUERY, BENEFITS_QUERY, PURCHASE_REQUEST
- CRM: ALIAS_RESOLUTION_REQUEST, BENEFICIARIES_QUERY, ADD_BENEFICIARY_REQUEST

### 5.3 CloudWatch Logs

**Component**: Centralized logging

**Log Groups**:
- /aws/lambda/centli-core-banking-balance
- /aws/lambda/centli-core-banking-transfer
- /aws/lambda/centli-core-banking-transactions
- /aws/lambda/centli-marketplace-catalog
- /aws/lambda/centli-marketplace-benefits
- /aws/lambda/centli-marketplace-purchase
- /aws/lambda/centli-crm-resolve-alias
- /aws/lambda/centli-crm-get-beneficiaries
- /aws/lambda/centli-crm-add-beneficiary

---

## 6. Integration Points

### 6.1 Unit 2 Integration (AgentCore)

**Flow**:
```
AgentCore (Unit 2)
    ↓ (publishes event)
EventBridge
    ↓ (routes to)
Action Group Lambda (Unit 3)
    ↓ (processes)
DynamoDB
    ↓ (publishes result)
EventBridge
    ↓ (routes back to)
AgentCore (Unit 2)
```

**Event Contract**:
```json
{
  "version": "1.0",
  "event_type": "TRANSFER_REQUEST",
  "correlation_id": "uuid",
  "timestamp": "ISO8601",
  "source": "agentcore",
  "user_id": "string",
  "data": {
    "from_account": "string",
    "to_account": "string",
    "amount": number
  }
}
```

### 6.2 Cross-Action Group Integration

**Example: Purchase Flow**

```
1. AgentCore → PURCHASE_REQUEST → Marketplace
2. Marketplace → INVENTORY_RESERVED → (internal)
3. Marketplace → PAYMENT_REQUEST → Core Banking
4. Core Banking → PAYMENT_COMPLETED → Marketplace
5. Marketplace → PURCHASE_CONFIRMED → AgentCore
```

**Compensation Flow** (on failure):
```
1. Core Banking → PAYMENT_FAILED → Marketplace
2. Marketplace → COMPENSATION_REQUIRED → (internal)
3. Marketplace → INVENTORY_RELEASED → (internal)
4. Marketplace → PURCHASE_FAILED → AgentCore
```

---

## 7. Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Unit 2: AgentCore                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   EventBridge Event Bus                     │
└──────┬──────────────────┬──────────────────┬────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Core Banking │   │ Marketplace  │   │     CRM      │
│ Action Group │   │ Action Group │   │ Action Group │
├──────────────┤   ├──────────────┤   ├──────────────┤
│ 3 Lambdas    │   │ 3 Lambdas    │   │ 3 Lambdas    │
│ 2 Tables     │   │ 3 Tables     │   │ 1 Table      │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┴──────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   EventBridge Event Bus                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Unit 2: AgentCore                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Component Summary

| Component | Type | Count | Purpose |
|-----------|------|-------|---------|
| Lambda Functions | Compute | 9 | Business logic execution |
| DynamoDB Tables | Storage | 6 | Data persistence |
| EventBridge Rules | Integration | 9 | Event routing |
| IAM Roles | Security | 9 | Lambda execution permissions |
| CloudWatch Log Groups | Observability | 9 | Centralized logging |
| Utility Modules | Shared Code | 6 | Common functionality |

**Total Components**: 48 logical components

---

## 9. Deployment Units

Each Action Group is independently deployable:

**Core Banking Deployment Unit**:
- 3 Lambda functions
- 2 DynamoDB tables
- 3 EventBridge rules
- 3 IAM roles

**Marketplace Deployment Unit**:
- 3 Lambda functions
- 3 DynamoDB tables
- 3 EventBridge rules
- 3 IAM roles

**CRM Deployment Unit**:
- 3 Lambda functions
- 1 DynamoDB table
- 3 EventBridge rules
- 3 IAM roles

---

## 10. Next Steps

1. ✅ Logical Components complete
2. ⏳ Generate Infrastructure Design (SAM template)
3. ⏳ Generate Code Generation Plan
4. ⏳ Implement Action Groups

---

**Document Status**: Complete  
**Approved By**: [Pending approval]  
**Next Stage**: Infrastructure Design
