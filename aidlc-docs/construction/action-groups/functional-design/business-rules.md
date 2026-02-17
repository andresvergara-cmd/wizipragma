# Business Rules - Unit 3: Action Groups

## Overview

This document defines the business rules, validation logic, and constraints for the Action Groups unit.

---

## 1. Core Banking Rules

### 1.1 Account Validation Rules

**R1.1: Account Existence**
- **Rule**: Both source and destination accounts must exist in the system
- **Validation**: Query DynamoDB accounts table before any transaction
- **Error**: `ACCOUNT_NOT_FOUND` if account doesn't exist

**R1.2: Account Status**
- **Rule**: Account must have status = "active" to perform transactions
- **Validation**: Check account.status field
- **Error**: `ACCOUNT_FROZEN` or `ACCOUNT_CLOSED` if not active

**R1.3: Account Type Validation**
- **Rule**: Different account types have different capabilities:
  - Checking: All operations allowed
  - Savings: All operations allowed
  - Credit: Transfers limited to credit_limit
- **Validation**: Check account_type and available balance/credit
- **Error**: `INSUFFICIENT_FUNDS` or `CREDIT_LIMIT_EXCEEDED`

---

### 1.2 Balance Validation Rules

**R2.1: Sufficient Balance (Checking/Savings)**
- **Rule**: balance >= transfer_amount
- **Validation**: Check before debit operation
- **Error**: `INSUFFICIENT_FUNDS`

**R2.2: Credit Limit (Credit Accounts)**
- **Rule**: balance + transfer_amount <= credit_limit
- **Validation**: Check available_credit before operation
- **Error**: `CREDIT_LIMIT_EXCEEDED`

**R2.3: Minimum Balance**
- **Rule**: Checking/Savings accounts cannot go below 0
- **Validation**: Enforce balance >= 0 constraint
- **Error**: `NEGATIVE_BALANCE_NOT_ALLOWED`

---

### 1.3 Transfer Limit Rules

**R3.1: Daily Transfer Limit**
- **Rule**: Sum of daily transfers <= daily_limit (default: 100,000 MXN)
- **Validation**: Check TransferLimit.daily_used + amount <= daily_limit
- **Error**: `DAILY_LIMIT_EXCEEDED`
- **Reset**: Midnight Mexico City timezone

**R3.2: Monthly Transfer Limit**
- **Rule**: Sum of monthly transfers <= monthly_limit (default: 500,000 MXN)
- **Validation**: Check TransferLimit.monthly_used + amount <= monthly_limit
- **Error**: `MONTHLY_LIMIT_EXCEEDED`
- **Reset**: 1st day of each month

**R3.3: Limit Tracking**
- **Rule**: Update daily_used and monthly_used after successful transfer
- **Implementation**: Atomic increment in DynamoDB
- **Rollback**: Decrement if transfer fails after limit update

---

### 1.4 Transfer Security Rules

**R4.1: Minimum Security Permissions**
- **Rule**: User must have valid authentication token
- **Validation**: Verify JWT token in request
- **Error**: `UNAUTHORIZED`

**R4.2: Account Ownership**
- **Rule**: User can only transfer from their own accounts
- **Validation**: Verify account.user_id matches authenticated user_id
- **Error**: `FORBIDDEN`

**R4.3: Beneficiary Validation**
- **Rule**: If transferring to beneficiary, beneficiary must exist and be active
- **Validation**: Query beneficiaries table
- **Error**: `BENEFICIARY_NOT_FOUND` or `BENEFICIARY_INACTIVE`

---

### 1.5 Transaction Recording Rules

**R5.1: Transaction History**
- **Rule**: All transactions must be recorded in transactions table
- **Validation**: Create transaction record before executing transfer
- **Status**: Set to "pending" initially, update to "completed" or "failed"

**R5.2: Transaction Attributes**
- **Rule**: Must include:
  - transaction_type
  - status
  - amount
  - timestamp
  - geolocation (if available)
  - beneficiary_info (for transfers)
- **Validation**: Enforce required fields

**R5.3: Transaction Retention**
- **Rule**: Keep transactions for last 30 days in main table
- **Implementation**: Archive older transactions to S3
- **TTL**: Set DynamoDB TTL to 30 days

---

### 1.6 Optimistic Locking Rules

**R6.1: Version Number**
- **Rule**: Every account has a version number that increments on update
- **Implementation**: Account.version field
- **Initial**: version = 1 on account creation

**R6.2: Concurrent Update Detection**
- **Rule**: Update only succeeds if version matches expected value
- **Validation**: DynamoDB ConditionExpression: `version = :expected_version`
- **Error**: `VERSION_CONFLICT` if version mismatch

**R6.3: Retry Strategy**
- **Rule**: Retry up to 3 times on version conflict
- **Implementation**: Exponential backoff (100ms, 200ms, 400ms)
- **Error**: `CONCURRENT_UPDATE_FAILED` if all retries fail

---

## 2. Marketplace Rules

### 2.1 Product Validation Rules

**R7.1: Product Availability**
- **Rule**: Product must exist and have status = "active"
- **Validation**: Query products table
- **Error**: `PRODUCT_NOT_FOUND` or `PRODUCT_INACTIVE`

**R7.2: Stock Validation**
- **Rule**: product.stock >= purchase_quantity
- **Validation**: Check before recording purchase
- **Error**: `INSUFFICIENT_STOCK`

**R7.3: Stock Decrement**
- **Rule**: Decrement stock atomically when purchase is recorded
- **Implementation**: DynamoDB atomic counter
- **Rollback**: Increment stock if payment fails

---

### 2.2 Benefit Eligibility Rules

**R8.1: Benefit Status**
- **Rule**: Benefit must have status = "active"
- **Validation**: Check benefit.status and expiration date
- **Error**: `BENEFIT_EXPIRED` or `BENEFIT_EXHAUSTED`

**R8.2: Account Type Eligibility**
- **Rule**: User's account type must be in benefit.eligible_account_types
- **Validation**: Check account_type against eligible list
- **Error**: `BENEFIT_NOT_ELIGIBLE`
- **Example**: MSI requires credit account

**R8.3: Minimum Purchase Amount**
- **Rule**: If benefit has min_purchase_amount, purchase must meet minimum
- **Validation**: purchase_amount >= benefit.min_purchase_amount
- **Error**: `MINIMUM_PURCHASE_NOT_MET`
- **Note**: Default min_purchase_amount = 0 (no minimum)

**R8.4: Usage Limit**
- **Rule**: If benefit has max_usage_per_user, check usage count
- **Validation**: Query BenefitUsage table for user + benefit
- **Error**: `BENEFIT_USAGE_LIMIT_EXCEEDED`

---

### 2.3 Benefit Application Rules

**R9.1: Multiple Benefits**
- **Rule**: User can apply multiple benefits if all are stackable
- **Validation**: Check benefit.stackable = true for all selected benefits
- **Error**: `BENEFITS_NOT_STACKABLE`

**R9.2: Benefit Calculation Order**
- **Rule**: Apply benefits in this order:
  1. Discounts (reduce price)
  2. MSI (split payment)
  3. Cashback (credit after purchase)
- **Implementation**: Calculate total_discount and final amount

**R9.3: Cashback Application**
- **Rule**: Cashback is credited immediately after purchase completion
- **Timing**: When purchase.status = "completed"
- **Implementation**: Create credit transaction to user's account
- **Amount**: (purchase_amount * cashback_percentage) / 100

**R9.4: MSI Application**
- **Rule**: MSI (Meses Sin Intereses) splits payment into monthly installments
- **Validation**: Requires credit account
- **Implementation**: Record MSI terms in purchase record
- **Note**: Actual installment charging is out of scope for hackathon

---

### 2.4 Purchase Validation Rules

**R10.1: Payment Account Validation**
- **Rule**: Payment account must exist and be enabled (status = "active")
- **Validation**: Query accounts table
- **Error**: `PAYMENT_ACCOUNT_INVALID`

**R10.2: Payment Account Balance**
- **Rule**: Account must have sufficient balance/credit for purchase
- **Validation**: Delegated to Core Banking payment processing
- **Error**: `INSUFFICIENT_FUNDS` (from Core Banking)

**R10.3: Purchase Status Transitions**
- **Rule**: Valid status transitions:
  - pending_payment → completed (payment succeeds)
  - pending_payment → failed (payment fails)
  - completed → cancelled (manual cancellation)
- **Validation**: Enforce state machine
- **Error**: `INVALID_STATUS_TRANSITION`

---

### 2.5 Payment Processing Rules

**R11.1: Asynchronous Payment**
- **Rule**: Marketplace publishes payment request, Core Banking processes asynchronously
- **Implementation**: EventBridge event-driven architecture
- **Timeout**: Wait up to 30 seconds for payment response

**R11.2: Payment Failure Compensation**
- **Rule**: If payment fails, restore product stock
- **Implementation**: Increment product.stock by purchase_quantity
- **Status**: Update purchase.status to "failed"

**R11.3: Payment Success Actions**
- **Rule**: When payment succeeds:
  1. Update purchase.status to "completed"
  2. Record payment_transaction_id
  3. Apply cashback if applicable
- **Implementation**: Sequential operations with error handling

---

## 3. CRM Rules

### 3.1 Beneficiary Management Rules

**R12.1: Beneficiary Account Validation**
- **Rule**: Beneficiary account must exist in the system
- **Validation**: Query accounts table with beneficiary_account_id
- **Error**: `BENEFICIARY_ACCOUNT_NOT_FOUND`

**R12.2: Alias Uniqueness**
- **Rule**: Alias must be unique per user (not globally unique)
- **Validation**: Query beneficiaries table with user_id + alias
- **Error**: `ALIAS_ALREADY_EXISTS`
- **Note**: One alias per beneficiary

**R12.3: Alias Format**
- **Rule**: Alias must meet format requirements:
  - Length: 1-50 characters
  - Characters: Letters, numbers, spaces, hyphens
  - No reserved words: "yo", "mi cuenta", "banco"
- **Validation**: Regex pattern matching
- **Error**: `INVALID_ALIAS_FORMAT`

**R12.4: Beneficiary Status**
- **Rule**: Only active beneficiaries can be used for transfers
- **Validation**: Check beneficiary.status = "active"
- **Error**: `BENEFICIARY_INACTIVE`

---

### 3.2 Alias Resolution Rules

**R13.1: Semantic Matching**
- **Rule**: Perform semantic matching on alias and name fields
- **Implementation**: 
  - Exact match on alias field (highest priority)
  - Fuzzy match on beneficiary_name field
  - Consider relationship context
- **Confidence**: Return confidence score (0-100)

**R13.2: Single Match**
- **Rule**: If single match found with confidence >= 80, return immediately
- **Response**: beneficiary_id and account_id
- **Action**: Increment frequency counter

**R13.3: Multiple Matches**
- **Rule**: If multiple matches found, request user clarification
- **Response**: List of matches with confidence scores
- **Action**: Publish disambiguation request to AgentCore
- **Wait**: For user selection before proceeding

**R13.4: No Matches**
- **Rule**: If no matches found, return error with suggestions
- **Response**: List of similar beneficiaries (fuzzy match)
- **Error**: `ALIAS_NOT_FOUND`

---

### 3.3 Frequency Tracking Rules

**R14.1: Frequency Increment**
- **Rule**: Increment beneficiary.frequency on successful transfer
- **Implementation**: Atomic counter in DynamoDB
- **Timing**: After transfer status = "completed"

**R14.2: Last Used Timestamp**
- **Rule**: Update beneficiary.last_used_at on successful transfer
- **Implementation**: Set to current timestamp
- **Purpose**: For recency-based recommendations

**R14.3: Frequency Decay**
- **Rule**: No decay implemented (frequency is cumulative)
- **Note**: Could be enhanced in future to weight recent transfers more

---

### 3.4 Proactive Recommendation Rules

**R15.1: Recommendation Criteria**
- **Rule**: Recommend top 5 beneficiaries based on:
  - Primary: frequency (descending)
  - Secondary: last_used_at (most recent)
- **Validation**: Only include active beneficiaries
- **Response**: List of 5 beneficiaries with metadata

**R15.2: Recommendation Trigger**
- **Rule**: Recommendations triggered by:
  - User asks "¿A quién puedo transferir?"
  - AgentCore detects transfer intent without beneficiary
- **Implementation**: AgentCore publishes recommendation request

**R15.3: Empty Recommendations**
- **Rule**: If user has no beneficiaries, suggest adding one
- **Response**: Prompt to add beneficiary with instructions

---

## 4. Cross-Unit Rules

### 4.1 Event-Driven Communication Rules

**R16.1: Event Schema Validation**
- **Rule**: All events must conform to defined schemas
- **Validation**: JSON schema validation at Lambda entry point
- **Error**: `INVALID_EVENT_SCHEMA`

**R16.2: Request ID Uniqueness**
- **Rule**: Each event must have unique request_id
- **Implementation**: UUID v4 generated by publisher
- **Purpose**: Idempotency and duplicate detection

**R16.3: Event Filtering**
- **Rule**: EventBridge filters events by detail-type
- **Implementation**: Event pattern matching in EventBridge rules
- **Benefit**: Reduces Lambda invocations and costs

---

### 4.2 Idempotency Rules

**R17.1: Duplicate Detection**
- **Rule**: Check for duplicate request_id before processing
- **Implementation**: Query DynamoDB idempotency table
- **Action**: If found, return cached response (no re-execution)

**R17.2: Response Caching**
- **Rule**: Cache response for each request_id
- **TTL**: 24 hours
- **Storage**: DynamoDB idempotency table

**R17.3: Idempotent Operations**
- **Rule**: All operations must be idempotent (safe to retry)
- **Implementation**: Use conditional writes and version checks
- **Benefit**: Safe automatic retries on failures

---

### 4.3 Error Handling Rules

**R18.1: Error Categories**
- **Rule**: Categorize all errors into:
  - `validation_error`: Invalid input data
  - `business_error`: Business rule violation
  - `technical_error`: System/infrastructure failure
- **Purpose**: Different retry strategies per category

**R18.2: Retry Strategy**
- **Rule**: Retry based on error category:
  - validation_error: No retry (fix input)
  - business_error: No retry (business rule prevents)
  - technical_error: Retry up to 3 times
- **Implementation**: Exponential backoff

**R18.3: Error Propagation**
- **Rule**: If all retries fail, publish error event to EventBridge
- **Event**: Include error category, details, and original request
- **Recipient**: AgentCore handles error and informs user

---

### 4.4 Data Consistency Rules

**R19.1: Strong Consistency Reads**
- **Rule**: All DynamoDB reads use strong consistency
- **Implementation**: ConsistentRead=true in all queries
- **Purpose**: Ensure latest data for balance checks and validations

**R19.2: Optimistic Locking Writes**
- **Rule**: All balance updates use optimistic locking
- **Implementation**: Version number in ConditionExpression
- **Purpose**: Prevent race conditions on concurrent updates

**R19.3: Eventual Consistency Across Units**
- **Rule**: Cross-unit communication is eventually consistent
- **Implementation**: EventBridge pub/sub
- **Compensation**: Implement compensation logic for failures

---

## 5. Validation Rules Summary

### 5.1 Input Validation

| Field | Validation | Error Code |
|-------|------------|------------|
| account_id | UUID format, exists | INVALID_ACCOUNT_ID |
| amount | Decimal > 0, max 2 decimals | INVALID_AMOUNT |
| user_id | String, not empty | INVALID_USER_ID |
| product_id | UUID format, exists | INVALID_PRODUCT_ID |
| quantity | Integer > 0 | INVALID_QUANTITY |
| alias | 1-50 chars, valid format | INVALID_ALIAS_FORMAT |
| email | Valid email format | INVALID_EMAIL |
| phone | Valid phone format | INVALID_PHONE |

### 5.2 Business Validation

| Rule | Validation | Error Code |
|------|------------|------------|
| Sufficient balance | balance >= amount | INSUFFICIENT_FUNDS |
| Daily limit | daily_used + amount <= daily_limit | DAILY_LIMIT_EXCEEDED |
| Stock available | stock >= quantity | INSUFFICIENT_STOCK |
| Benefit active | status = active, not expired | BENEFIT_EXPIRED |
| Account active | status = active | ACCOUNT_FROZEN |
| Alias unique | No duplicate for user | ALIAS_ALREADY_EXISTS |

---

## Success Criteria

- [x] All business rules documented with validation logic
- [x] Error codes defined for each rule violation
- [x] Retry strategies specified
- [x] Data consistency rules defined
- [x] Cross-unit rules documented
- [x] Validation rules summarized

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17  
**Next Step**: Present for user approval

