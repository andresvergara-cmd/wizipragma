# Infrastructure Design - Unit 3: Action Groups

## Document Information
- **Unit**: Unit 3 (Action Groups - Backend Services)
- **Stage**: Infrastructure Design
- **Created**: 2026-02-17
- **Context**: AWS serverless infrastructure for Action Groups

---

## 1. Infrastructure Overview

Unit 3 deploys 9 Lambda functions, 6 DynamoDB tables, and 9 EventBridge rules to implement Core Banking, Marketplace, and CRM Action Groups.

### 1.1 Resource Summary

| Resource Type | Count | Purpose |
|---------------|-------|---------|
| Lambda Functions | 9 | Business logic execution |
| DynamoDB Tables | 6 | Data persistence |
| EventBridge Rules | 9 | Event routing |
| IAM Roles | 9 | Lambda execution permissions |
| CloudWatch Log Groups | 9 | Centralized logging |

**Total AWS Resources**: 42

---

## 2. DynamoDB Tables

### 2.1 Core Banking Tables

**centli-accounts**
```yaml
Type: AWS::DynamoDB::Table
Properties:
  TableName: centli-accounts
  BillingMode: PAY_PER_REQUEST
  AttributeDefinitions:
    - AttributeName: user_id
      AttributeType: S
    - AttributeName: account_id
      AttributeType: S
  KeySchema:
    - AttributeName: user_id
      KeyType: HASH
    - AttributeName: account_id
      KeyType: RANGE
  SSESpecification:
    SSEEnabled: true
  Tags:
    - Key: ActionGroup
      Value: CoreBanking
```

**Access Patterns**:
- Get account: `user_id` + `account_id`
- List accounts: Query by `user_id`

**Attributes**:
- `user_id` (PK): User identifier
- `account_id` (SK): Account identifier
- `account_type`: checking, savings, credit
- `balance`: Current balance (Decimal)
- `currency`: MXN
- `status`: active, inactive, blocked
- `created_at`: ISO timestamp
- `updated_at`: ISO timestamp
- `version`: Optimistic locking version

---

**centli-transactions**
```yaml
Type: AWS::DynamoDB::Table
Properties:
  TableName: centli-transactions
  BillingMode: PAY_PER_REQUEST
  AttributeDefinitions:
    - AttributeName: account_id
      AttributeType: S
    - AttributeName: timestamp_txn_id
      AttributeType: S
    - AttributeName: user_id
      AttributeType: S
  KeySchema:
    - AttributeName: account_id
      KeyType: HASH
    - AttributeName: timestamp_txn_id
      KeyType: RANGE
  GlobalSecondaryIndexes:
    - IndexName: user-index
      KeySchema:
        - AttributeName: user_id
          KeyType: HASH
        - AttributeName: timestamp_txn_id
          KeyType: RANGE
      Projection:
        ProjectionType: ALL
  SSESpecification:
    SSEEnabled: true
```

**Access Patterns**:
- Get transaction: `account_id` + `timestamp_txn_id`
- List by account: Query by `account_id`
- List by user: Query GSI by `user_id`

**Attributes**:
- `account_id` (PK): Account identifier
- `timestamp_txn_id` (SK): `{timestamp}#{transaction_id}`
- `user_id` (GSI PK): User identifier
- `transaction_id`: Unique transaction ID
- `type`: transfer, payment, deposit, withdrawal
- `amount`: Transaction amount
- `currency`: MXN
- `from_account`: Source account
- `to_account`: Destination account
- `status`: completed, pending, failed
- `description`: Transaction description
- `created_at`: ISO timestamp

---

### 2.2 Marketplace Tables

**centli-products**
```yaml
Type: AWS::DynamoDB::Table
Properties:
  TableName: centli-products
  BillingMode: PAY_PER_REQUEST
  AttributeDefinitions:
    - AttributeName: product_id
      AttributeType: S
    - AttributeName: retailer_id
      AttributeType: S
  KeySchema:
    - AttributeName: product_id
      KeyType: HASH
    - AttributeName: retailer_id
      KeyType: RANGE
  GlobalSecondaryIndexes:
    - IndexName: retailer-index
      KeySchema:
        - AttributeName: retailer_id
          KeyType: HASH
      Projection:
        ProjectionType: ALL
  SSESpecification:
    SSEEnabled: true
```

**Access Patterns**:
- Get product: `product_id` + `retailer_id`
- List by retailer: Query GSI by `retailer_id`

**Attributes**:
- `product_id` (PK): Product identifier
- `retailer_id` (SK): Retailer identifier
- `name`: Product name
- `description`: Product description
- `price`: Product price
- `currency`: MXN
- `category`: electronics, clothing, food, etc.
- `stock`: Available inventory
- `image_url`: S3 URL for product image
- `benefits`: Array of benefit options (MSI, cashback, points)

---

**centli-purchases**
```yaml
Type: AWS::DynamoDB::Table
Properties:
  TableName: centli-purchases
  BillingMode: PAY_PER_REQUEST
  AttributeDefinitions:
    - AttributeName: user_id
      AttributeType: S
    - AttributeName: timestamp_purchase_id
      AttributeType: S
  KeySchema:
    - AttributeName: user_id
      KeyType: HASH
    - AttributeName: timestamp_purchase_id
      KeyType: RANGE
  SSESpecification:
    SSEEnabled: true
```

**Access Patterns**:
- Get purchase: `user_id` + `timestamp_purchase_id`
- List by user: Query by `user_id`

**Attributes**:
- `user_id` (PK): User identifier
- `timestamp_purchase_id` (SK): `{timestamp}#{purchase_id}`
- `purchase_id`: Unique purchase ID
- `product_id`: Product purchased
- `retailer_id`: Retailer
- `quantity`: Quantity purchased
- `total_amount`: Total amount paid
- `benefit_applied`: MSI, cashback, points
- `status`: completed, pending, failed, cancelled
- `transaction_id`: Related transaction ID
- `created_at`: ISO timestamp

---

**centli-retailers**
```yaml
Type: AWS::DynamoDB::Table
Properties:
  TableName: centli-retailers
  BillingMode: PAY_PER_REQUEST
  AttributeDefinitions:
    - AttributeName: retailer_id
      AttributeType: S
  KeySchema:
    - AttributeName: retailer_id
      KeyType: HASH
  SSESpecification:
    SSEEnabled: true
```

**Access Patterns**:
- Get retailer: `retailer_id`

**Attributes**:
- `retailer_id` (PK): Retailer identifier
- `name`: Retailer name
- `category`: electronics, clothing, food, etc.
- `benefits_offered`: Array of benefits (MSI, cashback, points)
- `logo_url`: S3 URL for retailer logo

---

### 2.3 CRM Tables

**centli-beneficiaries**
```yaml
Type: AWS::DynamoDB::Table
Properties:
  TableName: centli-beneficiaries
  BillingMode: PAY_PER_REQUEST
  AttributeDefinitions:
    - AttributeName: user_id
      AttributeType: S
    - AttributeName: beneficiary_id
      AttributeType: S
    - AttributeName: alias_lower
      AttributeType: S
  KeySchema:
    - AttributeName: user_id
      KeyType: HASH
    - AttributeName: beneficiary_id
      KeyType: RANGE
  GlobalSecondaryIndexes:
    - IndexName: alias-index
      KeySchema:
        - AttributeName: alias_lower
          KeyType: HASH
        - AttributeName: user_id
          KeyType: RANGE
      Projection:
        ProjectionType: ALL
  SSESpecification:
    SSEEnabled: true
```

**Access Patterns**:
- Get beneficiary: `user_id` + `beneficiary_id`
- List by user: Query by `user_id`
- Resolve alias: Query GSI by `alias_lower` + `user_id`

**Attributes**:
- `user_id` (PK): User identifier
- `beneficiary_id` (SK): Beneficiary identifier
- `name`: Beneficiary full name
- `alias`: User-defined alias (e.g., "mi hermano")
- `alias_lower` (GSI PK): Lowercase alias for matching
- `account_id`: Beneficiary account ID
- `relationship`: brother, sister, friend, etc.
- `created_at`: ISO timestamp

---

## 3. Lambda Functions

### 3.1 Core Banking Lambdas

**centli-core-banking-balance**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-core-banking-balance
  CodeUri: src_aws/core_banking_balance/
  Handler: balance.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      ACCOUNTS_TABLE: centli-accounts
      EVENT_BUS_NAME: centli-event-bus
  Events:
    BalanceQuery:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - BALANCE_QUERY
```

**Responsibilities**:
- Query account balance
- Validate user access
- Publish BALANCE_RESPONSE event

---

**centli-core-banking-transfer**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-core-banking-transfer
  CodeUri: src_aws/core_banking_transfer/
  Handler: transfer.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      ACCOUNTS_TABLE: centli-accounts
      TRANSACTIONS_TABLE: centli-transactions
      EVENT_BUS_NAME: centli-event-bus
  Events:
    TransferRequest:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - TRANSFER_REQUEST
```

**Responsibilities**:
- Execute money transfer
- Validate sufficient funds
- Update account balances with optimistic locking
- Create transaction records
- Publish TRANSFER_COMPLETED or TRANSFER_FAILED event

---

**centli-core-banking-transactions**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-core-banking-transactions
  CodeUri: src_aws/core_banking_transactions/
  Handler: transactions.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      TRANSACTIONS_TABLE: centli-transactions
      EVENT_BUS_NAME: centli-event-bus
  Events:
    TransactionsQuery:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - TRANSACTIONS_QUERY
```

**Responsibilities**:
- Query transaction history
- Support pagination
- Publish TRANSACTIONS_RESPONSE event

---

### 3.2 Marketplace Lambdas

**centli-marketplace-catalog**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-marketplace-catalog
  CodeUri: src_aws/marketplace_catalog/
  Handler: catalog.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      PRODUCTS_TABLE: centli-products
      RETAILERS_TABLE: centli-retailers
      EVENT_BUS_NAME: centli-event-bus
  Events:
    CatalogQuery:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - CATALOG_QUERY
```

**Responsibilities**:
- Query product catalog
- Filter by category, retailer
- Publish CATALOG_RESPONSE event

---

**centli-marketplace-benefits**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-marketplace-benefits
  CodeUri: src_aws/marketplace_benefits/
  Handler: benefits.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      PRODUCTS_TABLE: centli-products
      EVENT_BUS_NAME: centli-event-bus
  Events:
    BenefitsQuery:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - BENEFITS_QUERY
```

**Responsibilities**:
- Calculate product benefits (MSI, cashback, points)
- Compare benefit options
- Publish BENEFITS_RESPONSE event

---

**centli-marketplace-purchase**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-marketplace-purchase
  CodeUri: src_aws/marketplace_purchase/
  Handler: purchase.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      PRODUCTS_TABLE: centli-products
      PURCHASES_TABLE: centli-purchases
      EVENT_BUS_NAME: centli-event-bus
  Events:
    PurchaseRequest:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - PURCHASE_REQUEST
    PaymentCompleted:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - PAYMENT_COMPLETED
    PaymentFailed:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - PAYMENT_FAILED
```

**Responsibilities**:
- Reserve product inventory
- Publish PAYMENT_REQUEST event
- Handle PAYMENT_COMPLETED (confirm purchase)
- Handle PAYMENT_FAILED (release inventory, compensation)
- Publish PURCHASE_CONFIRMED or PURCHASE_FAILED event

---

### 3.3 CRM Lambdas

**centli-crm-resolve-alias**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-crm-resolve-alias
  CodeUri: src_aws/crm_resolve_alias/
  Handler: resolve_alias.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      BENEFICIARIES_TABLE: centli-beneficiaries
      EVENT_BUS_NAME: centli-event-bus
  Events:
    AliasResolution:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - ALIAS_RESOLUTION_REQUEST
```

**Responsibilities**:
- Resolve alias to beneficiary
- Semantic matching (lowercase, fuzzy)
- Publish ALIAS_RESOLUTION_RESPONSE event

---

**centli-crm-get-beneficiaries**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-crm-get-beneficiaries
  CodeUri: src_aws/crm_get_beneficiaries/
  Handler: get_beneficiaries.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      BENEFICIARIES_TABLE: centli-beneficiaries
      EVENT_BUS_NAME: centli-event-bus
  Events:
    BeneficiariesQuery:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - BENEFICIARIES_QUERY
```

**Responsibilities**:
- List user beneficiaries
- Publish BENEFICIARIES_RESPONSE event

---

**centli-crm-add-beneficiary**
```yaml
Type: AWS::Serverless::Function
Properties:
  FunctionName: centli-crm-add-beneficiary
  CodeUri: src_aws/crm_add_beneficiary/
  Handler: add_beneficiary.lambda_handler
  Runtime: python3.11
  Timeout: 10
  MemorySize: 512
  Environment:
    Variables:
      BENEFICIARIES_TABLE: centli-beneficiaries
      EVENT_BUS_NAME: centli-event-bus
  Events:
    AddBeneficiary:
      Type: EventBridgeRule
      Properties:
        EventBusName: centli-event-bus
        Pattern:
          detail-type:
            - ADD_BENEFICIARY_REQUEST
```

**Responsibilities**:
- Add new beneficiary
- Validate alias uniqueness
- Publish BENEFICIARY_ADDED event

---

## 4. EventBridge Integration

### 4.1 Event Patterns

All Lambdas are triggered by EventBridge events with specific `detail-type` patterns.

**Event Flow Example - Transfer**:
```
1. AgentCore → TRANSFER_REQUEST → Core Banking Transfer Lambda
2. Transfer Lambda → TRANSFER_COMPLETED → AgentCore
```

**Event Flow Example - Purchase**:
```
1. AgentCore → PURCHASE_REQUEST → Marketplace Purchase Lambda
2. Purchase Lambda → PAYMENT_REQUEST → Core Banking Transfer Lambda
3. Transfer Lambda → PAYMENT_COMPLETED → Marketplace Purchase Lambda
4. Purchase Lambda → PURCHASE_CONFIRMED → AgentCore
```

### 4.2 Event Schema

All events follow consistent schema:
```json
{
  "version": "1.0",
  "event_type": "TRANSFER_REQUEST",
  "correlation_id": "uuid",
  "timestamp": "ISO8601",
  "source": "agentcore",
  "user_id": "string",
  "data": {
    // Event-specific payload
  }
}
```

---

## 5. IAM Permissions

### 5.1 Lambda Execution Roles

Each Lambda has dedicated IAM role with least privilege permissions.

**Core Banking Balance Role**:
- DynamoDB: GetItem, Query on `centli-accounts`
- EventBridge: PutEvents on `centli-event-bus`
- CloudWatch Logs: CreateLogGroup, CreateLogStream, PutLogEvents

**Core Banking Transfer Role**:
- DynamoDB: GetItem, UpdateItem, PutItem on `centli-accounts`, `centli-transactions`
- EventBridge: PutEvents on `centli-event-bus`
- CloudWatch Logs: CreateLogGroup, CreateLogStream, PutLogEvents

**Marketplace Purchase Role**:
- DynamoDB: GetItem, UpdateItem, PutItem on `centli-products`, `centli-purchases`
- EventBridge: PutEvents on `centli-event-bus`
- CloudWatch Logs: CreateLogGroup, CreateLogStream, PutLogEvents

**CRM Resolve Alias Role**:
- DynamoDB: Query on `centli-beneficiaries` (including GSI)
- EventBridge: PutEvents on `centli-event-bus`
- CloudWatch Logs: CreateLogGroup, CreateLogStream, PutLogEvents

---

## 6. Monitoring and Logging

### 6.1 CloudWatch Log Groups

Each Lambda has dedicated log group:
- `/aws/lambda/centli-core-banking-balance`
- `/aws/lambda/centli-core-banking-transfer`
- `/aws/lambda/centli-core-banking-transactions`
- `/aws/lambda/centli-marketplace-catalog`
- `/aws/lambda/centli-marketplace-benefits`
- `/aws/lambda/centli-marketplace-purchase`
- `/aws/lambda/centli-crm-resolve-alias`
- `/aws/lambda/centli-crm-get-beneficiaries`
- `/aws/lambda/centli-crm-add-beneficiary`

**Retention**: 7 days (hackathon context)

### 6.2 CloudWatch Metrics

**Lambda Metrics**:
- Invocations
- Duration (p50, p95, p99)
- Errors
- Throttles
- Concurrent Executions

**DynamoDB Metrics**:
- ConsumedReadCapacityUnits
- ConsumedWriteCapacityUnits
- UserErrors
- SystemErrors

---

## 7. Cost Estimation

### 7.1 Lambda Costs

**Assumptions**:
- 8-hour hackathon
- 100 invocations per Lambda
- 500ms average duration
- 512MB memory

**Calculation**:
- 9 Lambdas × 100 invocations = 900 invocations
- 900 × 0.5s × 512MB = 450 GB-seconds
- Cost: $0.00 (within free tier: 400,000 GB-seconds/month)

### 7.2 DynamoDB Costs

**Assumptions**:
- 1,000 writes
- 5,000 reads
- On-demand pricing

**Calculation**:
- Writes: 1,000 × $1.25/million = $0.00125
- Reads: 5,000 × $0.25/million = $0.00125
- Total: $0.0025

### 7.3 EventBridge Costs

**Assumptions**:
- 2,000 events

**Calculation**:
- 2,000 × $1.00/million = $0.002

### 7.4 Total Unit 3 Cost

**Total**: ~$0.005 (less than 1 cent)

Most services stay within AWS free tier for hackathon usage.

---

## 8. Deployment Strategy

### 8.1 SAM Deployment

```bash
# Build
sam build

# Deploy
sam deploy --profile 777937796305_Ps-HackatonAgentic-Mexico

# Verify
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### 8.2 Data Seeding

After deployment, seed initial data:

```bash
# Seed accounts
python scripts/seed_accounts.py

# Seed products
python scripts/seed_products.py

# Seed beneficiaries
python scripts/seed_beneficiaries.py
```

---

## 9. Testing Strategy

### 9.1 Unit Testing

Test each Lambda independently:
```bash
# Test balance Lambda
sam local invoke CoreBankingBalanceFunction \
  --event events/balance_query.json
```

### 9.2 Integration Testing

Test event flows:
```bash
# Publish test event to EventBridge
aws events put-events \
  --entries file://events/transfer_request.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### 9.3 End-to-End Testing

Test via WebSocket (Unit 2):
```bash
wscat -c "$WEBSOCKET_URL"
> {"type":"TEXT","content":"Transfiere 100 pesos a mi hermano"}
```

---

## 10. Next Steps

1. ✅ Infrastructure Design complete
2. ⏳ Update template.yaml with Unit 3 resources
3. ⏳ Generate Code Generation Plan
4. ⏳ Implement Lambda functions
5. ⏳ Deploy and test

---

**Document Status**: Complete  
**Approved By**: [Pending approval]  
**Next Stage**: Code Generation
