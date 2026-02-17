# Business Logic Model - Unit 3: Action Groups

## Overview

This document defines the business workflows and processes for the Action Groups unit, which provides mock banking, marketplace, and CRM services via EventBridge-triggered Lambda functions.

---

## 1. Core Banking Workflows

### 1.1 Account Balance Query

**Trigger**: EventBridge event from AgentCore  
**Event Type**: `action.core-banking.balance-query`

```
Flow:
1. Receive balance query event with user_id
2. Query DynamoDB for user accounts (checking, savings, credit)
3. Retrieve current balances with strong consistency
4. Format response with account details
5. Publish response event to EventBridge
```

**Response Event**: `action.core-banking.balance-response`

---

### 1.2 P2P Transfer Execution

**Trigger**: EventBridge event from AgentCore  
**Event Type**: `action.core-banking.transfer-request`

```
Flow:
1. Receive transfer request event
   - source_account_id
   - destination_account_id (or beneficiary_alias)
   - amount
   - description

2. Validation Phase:
   a. Validate source account exists and is active
   b. Validate destination account exists and is active
   c. Validate source account has sufficient balance
   d. Validate transfer limits (daily/monthly)
   e. Validate minimum security permissions

3. Alias Resolution (if needed):
   - If destination is alias, resolve via CRM Action Group
   - Publish alias resolution request
   - Wait for CRM response with account_id

4. Balance Update Phase (with optimistic locking):
   a. Read source account with version number
   b. Read destination account with version number
   c. Attempt atomic update:
      - Debit source account (balance - amount, version + 1)
      - Credit destination account (balance + amount, version + 1)
   d. If version conflict detected:
      - Retry operation (max 3 retries)
      - If all retries fail, publish error event

5. Transaction Recording:
   - Create transaction record in DynamoDB
   - Include: type, status, amount, timestamp, geolocation, beneficiary info
   - Set status to "completed"

6. Response:
   - Publish success event to EventBridge
   - Include transaction_id and new balances
```

**Response Event**: `action.core-banking.transfer-response`  
**Error Event**: `action.core-banking.transfer-error`

**Retry Strategy**:
- Optimistic locking conflicts: Retry up to 3 times
- Technical failures: Let AgentCore handle retry

---

### 1.3 Transaction History Query

**Trigger**: EventBridge event from AgentCore  
**Event Type**: `action.core-banking.transaction-history`

```
Flow:
1. Receive transaction history request
   - user_id
   - account_id (optional)
   - date_range (default: last 30 days)

2. Query DynamoDB transactions table
   - Filter by user_id and date range
   - Use strong consistency
   - Sort by timestamp descending

3. Format response with transaction list

4. Publish response event to EventBridge
```

**Response Event**: `action.core-banking.transaction-history-response`

---

## 2. Marketplace Workflows

### 2.1 Product Catalog Query

**Trigger**: EventBridge event from AgentCore  
**Event Type**: `action.marketplace.product-catalog`

```
Flow:
1. Receive catalog query event
   - category (optional)
   - search_term (optional)
   - limit (default: 10)

2. Query DynamoDB products table
   - Filter by category/search if provided
   - Include: product_id, name, price, image, stock, characteristics

3. For each product, query benefits:
   - Query benefits table with product_id
   - Include active benefits only (not expired)

4. Format response with products and benefits

5. Publish response event to EventBridge
```

**Response Event**: `action.marketplace.product-catalog-response`

---

### 2.2 Benefit Eligibility Check

**Trigger**: EventBridge event from AgentCore  
**Event Type**: `action.marketplace.benefit-eligibility`

```
Flow:
1. Receive eligibility check event
   - user_id
   - product_id
   - account_type (checking/savings/credit)

2. Query benefits table for product_id
   - Filter by active status
   - Filter by expiration date

3. For each benefit, check eligibility:
   - Cashback: Available for all account types
   - MSI (Meses Sin Intereses): Requires credit account
   - Discounts: Check usage limits per user

4. Calculate benefit values:
   - Multiple benefits can be applied (stackable)
   - Calculate total savings

5. Format response with eligible benefits

6. Publish response event to EventBridge
```

**Response Event**: `action.marketplace.benefit-eligibility-response`

---

### 2.3 Purchase Execution

**Trigger**: EventBridge event from AgentCore  
**Event Type**: `action.marketplace.purchase-request`

```
Flow:
1. Receive purchase request event
   - user_id
   - product_id
   - quantity
   - selected_benefits (list of benefit_ids)
   - payment_account_id

2. Validation Phase:
   a. Validate product exists and has stock
   b. Validate quantity <= available stock
   c. Validate payment account is enabled
   d. Calculate total amount with benefits applied

3. Record Purchase:
   - Create purchase record in DynamoDB
   - Set status to "pending_payment"
   - Decrement product stock

4. Payment Processing (Asynchronous):
   - Publish payment request event to EventBridge
   - Event type: `action.core-banking.payment-request`
   - Include: purchase_id, user_id, amount, account_id

5. Wait for Payment Response:
   - Subscribe to payment response events
   - If payment succeeds:
     * Update purchase status to "completed"
     * Apply cashback immediately (credit to account)
   - If payment fails:
     * Update purchase status to "failed"
     * Restore product stock (compensation logic)

6. Response:
   - Publish purchase response event
   - Include purchase_id and status
```

**Response Event**: `action.marketplace.purchase-response`  
**Error Event**: `action.marketplace.purchase-error`

**Integration**: Marketplace → Core Banking (payment event)

---

## 3. CRM Workflows

### 3.1 Beneficiary Management

**Trigger**: EventBridge event from AgentCore  
**Event Type**: `action.crm.beneficiary-add`

```
Flow:
1. Receive add beneficiary request
   - user_id
   - beneficiary_name
   - beneficiary_account_id
   - relationship (family/friend/vendor)
   - bank_info (bank_name, account_type)
   - contact_info (phone, email)
   - alias (optional)

2. Validation:
   a. Validate beneficiary account exists
   b. Validate alias is unique per user
   c. Validate alias format (length, characters)

3. Create Beneficiary Record:
   - Store in DynamoDB beneficiaries table
   - Initialize frequency counter to 0
   - Set created_at timestamp

4. Response:
   - Publish success event with beneficiary_id
```

**Response Event**: `action.crm.beneficiary-add-response`

---

### 3.2 Alias Resolution

**Trigger**: EventBridge event from AgentCore or Core Banking  
**Event Type**: `action.crm.alias-resolve`

```
Flow:
1. Receive alias resolution request
   - user_id
   - alias_text (e.g., "mi hermano", "Juan")

2. Semantic Matching:
   - Query beneficiaries table for user_id
   - Perform semantic matching on alias and name fields
   - Consider relationship context

3. Disambiguation:
   - If single match found:
     * Return beneficiary_id and account_id
   - If multiple matches found:
     * Return all matches with confidence scores
     * Publish disambiguation request to AgentCore
     * Wait for user clarification
   - If no matches found:
     * Return error with suggestions

4. Frequency Tracking:
   - Increment frequency counter for selected beneficiary
   - Update last_used timestamp

5. Response:
   - Publish resolution response event
```

**Response Event**: `action.crm.alias-resolve-response`

---

### 3.3 Proactive Beneficiary Recommendations

**Trigger**: EventBridge event from AgentCore  
**Event Type**: `action.crm.beneficiary-recommend`

```
Flow:
1. Receive recommendation request
   - user_id
   - context (optional: recent conversation)

2. Query Beneficiaries:
   - Get all beneficiaries for user_id
   - Sort by frequency (descending)
   - Consider recency (last_used timestamp)

3. Generate Recommendations:
   - Return top 5 most frequent beneficiaries
   - Include: name, alias, relationship, last_used

4. Response:
   - Publish recommendations event
```

**Response Event**: `action.crm.beneficiary-recommend-response`

---

## 4. Cross-Action Group Workflows

### 4.1 Marketplace Payment Flow

```
Sequence:
1. Marketplace: Receive purchase request
2. Marketplace: Validate and record purchase
3. Marketplace → EventBridge: Publish payment request
4. Core Banking: Receive payment request
5. Core Banking: Validate account and balance
6. Core Banking: Execute payment (debit account)
7. Core Banking → EventBridge: Publish payment response
8. Marketplace: Receive payment response
9. Marketplace: Update purchase status
10. Marketplace: Apply cashback if applicable
11. Marketplace → EventBridge: Publish purchase response
```

**Events**:
- `action.core-banking.payment-request`
- `action.core-banking.payment-response`
- `action.marketplace.purchase-response`

---

### 4.2 Transfer with Alias Resolution

```
Sequence:
1. Core Banking: Receive transfer request with alias
2. Core Banking → EventBridge: Publish alias resolution request
3. CRM: Receive alias resolution request
4. CRM: Perform semantic matching
5. CRM → EventBridge: Publish resolution response
6. Core Banking: Receive resolution response
7. Core Banking: Execute transfer with resolved account_id
8. Core Banking → EventBridge: Publish transfer response
```

**Events**:
- `action.crm.alias-resolve`
- `action.crm.alias-resolve-response`
- `action.core-banking.transfer-response`

---

## 5. Event-Driven Communication Patterns

### 5.1 Lambda Architecture

**Strategy**: Multiple Lambdas per Action Group
- Core Banking: 3 Lambdas (balance, transfer, transaction-history)
- Marketplace: 3 Lambdas (catalog, eligibility, purchase)
- CRM: 3 Lambdas (beneficiary-add, alias-resolve, recommend)

**Event Filtering**: EventBridge level
- Each Lambda subscribes to specific event patterns
- Filter by `detail-type` field in event

---

### 5.2 Error Handling

**Strategy**: Retry with fallback to AgentCore

```
Flow:
1. Action Group Lambda receives event
2. If operation fails:
   a. Retry operation (max 3 retries with exponential backoff)
   b. If all retries fail:
      - Publish error event to EventBridge
      - Include error category (validation/business/technical)
      - Include error details and original request
3. AgentCore receives error event
4. AgentCore decides next action (inform user, retry, compensate)
```

**Error Categories**:
- `validation_error`: Invalid input data
- `business_error`: Business rule violation
- `technical_error`: System/infrastructure failure

---

### 5.3 Idempotency

**Strategy**: Request ID tracking

```
Implementation:
1. Each event includes unique request_id
2. Lambda checks DynamoDB for existing request_id
3. If found, return cached response (no re-execution)
4. If not found, execute operation and cache response
5. TTL on cached responses: 24 hours
```

---

## 6. Data Consistency Strategy

### 6.1 DynamoDB Consistency

**Read Consistency**: Strong consistency for all reads
- Ensures latest data is always retrieved
- Critical for balance checks and transfer validation

**Write Consistency**: Optimistic locking with version numbers
- Prevents race conditions on concurrent updates
- Automatic retry on version conflicts

---

### 6.2 Cross-Action Group Consistency

**Strategy**: Eventual consistency via EventBridge
- Action Groups communicate via events
- No distributed transactions
- Compensation logic for failed operations

**Example**: Purchase payment failure
1. Marketplace records purchase (status: pending)
2. Core Banking payment fails
3. Core Banking publishes payment-failed event
4. Marketplace receives event and compensates:
   - Update purchase status to "failed"
   - Restore product stock
   - Notify user via AgentCore

---

## Success Criteria

- [x] All workflows documented with step-by-step flows
- [x] Event types and schemas defined
- [x] Integration points specified
- [x] Error handling strategies defined
- [x] Data consistency patterns documented
- [x] Cross-Action Group communication patterns defined

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17  
**Next Step**: Generate Domain Entities document
