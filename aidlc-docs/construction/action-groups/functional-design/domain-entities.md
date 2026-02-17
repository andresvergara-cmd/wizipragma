# Domain Entities - Unit 3: Action Groups

## Overview

This document defines the domain entities for the Action Groups unit, including attributes, data types, relationships, and cardinalities.

---

## 1. Core Banking Entities

### 1.1 Account

**Purpose**: Represents a user's bank account (checking, savings, or credit)

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| account_id | String (UUID) | Yes | Primary key, unique account identifier |
| user_id | String | Yes | Foreign key to user |
| account_type | Enum | Yes | "checking", "savings", "credit" |
| account_number | String | Yes | Display account number (masked) |
| balance | Decimal | Yes | Current account balance (MXN) |
| credit_limit | Decimal | No | Credit limit (only for credit accounts) |
| available_credit | Decimal | No | Available credit (credit_limit - balance) |
| status | Enum | Yes | "active", "frozen", "closed" |
| currency | String | Yes | "MXN" (default) |
| opening_date | Timestamp | Yes | Account opening date |
| version | Integer | Yes | Optimistic locking version number |
| created_at | Timestamp | Yes | Record creation timestamp |
| updated_at | Timestamp | Yes | Last update timestamp |

**Indexes**:
- Primary: `account_id`
- GSI: `user_id` (for querying all accounts by user)

**Business Rules**:
- Checking/Savings: balance >= 0
- Credit: balance <= credit_limit
- Version increments on every balance update

---

### 1.2 Transaction

**Purpose**: Records all financial transactions (transfers, payments, purchases)

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| transaction_id | String (UUID) | Yes | Primary key, unique transaction identifier |
| user_id | String | Yes | User who initiated transaction |
| account_id | String | Yes | Source account for transaction |
| transaction_type | Enum | Yes | "debit", "credit", "transfer", "purchase", "cashback" |
| amount | Decimal | Yes | Transaction amount (MXN) |
| status | Enum | Yes | "pending", "completed", "failed", "reversed" |
| description | String | No | Transaction description |
| beneficiary_id | String | No | Beneficiary ID (for transfers) |
| beneficiary_account_id | String | No | Destination account (for transfers) |
| beneficiary_name | String | No | Beneficiary display name |
| merchant_name | String | No | Merchant name (for purchases) |
| purchase_id | String | No | Related purchase ID (for marketplace) |
| geolocation | Object | No | {latitude, longitude, city, country} |
| device_info | Object | No | {device_type, os, app_version} |
| timestamp | Timestamp | Yes | Transaction timestamp |
| created_at | Timestamp | Yes | Record creation timestamp |

**Indexes**:
- Primary: `transaction_id`
- GSI1: `user_id` + `timestamp` (for transaction history queries)
- GSI2: `account_id` + `timestamp` (for account-specific history)

**Business Rules**:
- Transactions older than 30 days are archived
- Status transitions: pending → completed/failed
- Failed transactions can be retried (new transaction_id)

---

### 1.3 TransferLimit

**Purpose**: Tracks daily and monthly transfer limits per user

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | String | Yes | Primary key, user identifier |
| daily_limit | Decimal | Yes | Maximum daily transfer amount (MXN) |
| monthly_limit | Decimal | Yes | Maximum monthly transfer amount (MXN) |
| daily_used | Decimal | Yes | Amount used today (MXN) |
| monthly_used | Decimal | Yes | Amount used this month (MXN) |
| last_reset_date | Date | Yes | Last daily reset date |
| last_monthly_reset | Date | Yes | Last monthly reset date |
| updated_at | Timestamp | Yes | Last update timestamp |

**Indexes**:
- Primary: `user_id`

**Business Rules**:
- Daily limit resets at midnight (Mexico City timezone)
- Monthly limit resets on 1st of each month
- Default limits: daily=100,000 MXN, monthly=500,000 MXN

---

## 2. Marketplace Entities

### 2.1 Product

**Purpose**: Represents a product available for purchase

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| product_id | String (UUID) | Yes | Primary key, unique product identifier |
| name | String | Yes | Product name |
| description | String | Yes | Product description |
| price | Decimal | Yes | Product price (MXN) |
| category | String | Yes | Product category |
| brand | String | No | Product brand |
| image_url | String | Yes | Product image URL |
| characteristics | Object | No | {color, size, weight, etc.} |
| stock | Integer | Yes | Available stock quantity |
| status | Enum | Yes | "active", "inactive", "out_of_stock" |
| created_at | Timestamp | Yes | Record creation timestamp |
| updated_at | Timestamp | Yes | Last update timestamp |

**Indexes**:
- Primary: `product_id`
- GSI: `category` + `status` (for catalog queries)

**Business Rules**:
- Stock must be >= 0
- Status automatically set to "out_of_stock" when stock = 0

---

### 2.2 Benefit

**Purpose**: Represents a benefit (cashback, MSI, discount) applicable to products

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| benefit_id | String (UUID) | Yes | Primary key, unique benefit identifier |
| product_id | String | Yes | Foreign key to product |
| benefit_type | Enum | Yes | "cashback", "msi", "discount" |
| benefit_value | Decimal | Yes | Benefit value (% for cashback/discount, months for MSI) |
| description | String | Yes | Benefit description |
| eligible_account_types | List | Yes | ["checking", "savings", "credit"] |
| min_purchase_amount | Decimal | No | Minimum purchase amount (0 = no minimum) |
| max_usage_per_user | Integer | No | Max times user can use benefit (null = unlimited) |
| start_date | Timestamp | Yes | Benefit start date |
| end_date | Timestamp | Yes | Benefit expiration date |
| status | Enum | Yes | "active", "expired", "exhausted" |
| stackable | Boolean | Yes | Can be combined with other benefits |
| created_at | Timestamp | Yes | Record creation timestamp |
| updated_at | Timestamp | Yes | Last update timestamp |

**Indexes**:
- Primary: `benefit_id`
- GSI: `product_id` + `status` (for benefit queries by product)

**Business Rules**:
- Cashback: Applied immediately after purchase completion
- MSI: Requires credit account
- Multiple benefits can be stacked if stackable=true
- Status automatically set to "expired" when end_date < now

---

### 2.3 Purchase

**Purpose**: Records a product purchase transaction

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| purchase_id | String (UUID) | Yes | Primary key, unique purchase identifier |
| user_id | String | Yes | User who made purchase |
| product_id | String | Yes | Product purchased |
| quantity | Integer | Yes | Quantity purchased |
| unit_price | Decimal | Yes | Price per unit at time of purchase |
| subtotal | Decimal | Yes | quantity * unit_price |
| applied_benefits | List | Yes | List of benefit_ids applied |
| total_discount | Decimal | Yes | Total discount amount (MXN) |
| total_amount | Decimal | Yes | Final amount after benefits |
| payment_account_id | String | Yes | Account used for payment |
| payment_transaction_id | String | No | Related payment transaction ID |
| status | Enum | Yes | "pending_payment", "completed", "failed", "cancelled" |
| timestamp | Timestamp | Yes | Purchase timestamp |
| created_at | Timestamp | Yes | Record creation timestamp |
| updated_at | Timestamp | Yes | Last update timestamp |

**Indexes**:
- Primary: `purchase_id`
- GSI: `user_id` + `timestamp` (for purchase history)

**Business Rules**:
- Status transitions: pending_payment → completed/failed
- If payment fails, restore product stock
- Cashback applied only when status = "completed"

---

### 2.4 BenefitUsage

**Purpose**: Tracks benefit usage per user for usage limits

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| usage_id | String (UUID) | Yes | Primary key |
| user_id | String | Yes | User who used benefit |
| benefit_id | String | Yes | Benefit used |
| purchase_id | String | Yes | Related purchase |
| usage_count | Integer | Yes | Number of times used |
| last_used_at | Timestamp | Yes | Last usage timestamp |

**Indexes**:
- Primary: `usage_id`
- GSI: `user_id` + `benefit_id` (for usage limit checks)

---

## 3. CRM Entities

### 3.1 Beneficiary

**Purpose**: Represents a saved beneficiary for transfers

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| beneficiary_id | String (UUID) | Yes | Primary key, unique beneficiary identifier |
| user_id | String | Yes | User who owns this beneficiary |
| beneficiary_name | String | Yes | Beneficiary full name |
| beneficiary_account_id | String | Yes | Beneficiary's account ID |
| relationship | Enum | Yes | "family", "friend", "vendor" |
| bank_name | String | Yes | Beneficiary's bank name |
| account_type | Enum | Yes | "checking", "savings", "credit" |
| phone | String | No | Beneficiary phone number |
| email | String | No | Beneficiary email |
| alias | String | No | User-defined alias (unique per user) |
| frequency | Integer | Yes | Number of times used (default: 0) |
| last_used_at | Timestamp | No | Last transfer timestamp |
| status | Enum | Yes | "active", "inactive", "deleted" |
| created_at | Timestamp | Yes | Record creation timestamp |
| updated_at | Timestamp | Yes | Last update timestamp |

**Indexes**:
- Primary: `beneficiary_id`
- GSI1: `user_id` + `frequency` (for recommendations)
- GSI2: `user_id` + `alias` (for alias resolution)

**Business Rules**:
- Alias must be unique per user (not globally unique)
- One alias per beneficiary
- Frequency increments on each successful transfer
- Soft delete: status = "deleted" (not hard delete)

---

### 3.2 UserProfile

**Purpose**: Extended user profile for CRM features

**Attributes**:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | String | Yes | Primary key, user identifier |
| full_name | String | Yes | User full name |
| email | String | Yes | User email |
| phone | String | Yes | User phone number |
| preferred_language | String | Yes | "es-MX" (default) |
| notification_preferences | Object | Yes | {email: true, sms: true, push: true} |
| created_at | Timestamp | Yes | Record creation timestamp |
| updated_at | Timestamp | Yes | Last update timestamp |

**Indexes**:
- Primary: `user_id`

---

## 4. Entity Relationships

### 4.1 Relationship Diagram

```
User (1) ──────< (N) Account
                      │
                      │ (1)
                      │
                      ▼
                     (N) Transaction
                      │
                      │ (0..1)
                      │
                      ▼
                     (0..1) Beneficiary

User (1) ──────< (N) Beneficiary

User (1) ──────< (N) Purchase
                      │
                      │ (1)
                      │
                      ▼
                     (1) Product
                      │
                      │ (1)
                      │
                      ▼
                     (N) Benefit

User (1) ────── (1) UserProfile

User (1) ────── (1) TransferLimit
```

### 4.2 Cardinalities

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| User → Account | 1:N | One user has multiple accounts (checking, savings, credit) |
| Account → Transaction | 1:N | One account has many transactions |
| Transaction → Beneficiary | N:1 | Many transactions can reference same beneficiary |
| User → Beneficiary | 1:N | One user has multiple saved beneficiaries |
| User → Purchase | 1:N | One user makes multiple purchases |
| Purchase → Product | N:1 | Many purchases can be for same product |
| Product → Benefit | 1:N | One product can have multiple benefits |
| User → UserProfile | 1:1 | One user has one profile |
| User → TransferLimit | 1:1 | One user has one set of limits |

---

## 5. Data Types and Constraints

### 5.1 Common Data Types

| Type | Format | Example |
|------|--------|---------|
| String (UUID) | UUID v4 | "550e8400-e29b-41d4-a716-446655440000" |
| String | UTF-8 text | "Juan Pérez" |
| Decimal | Decimal(10,2) | 1234.56 |
| Integer | 32-bit signed | 42 |
| Timestamp | ISO 8601 | "2026-02-17T14:30:00Z" |
| Date | YYYY-MM-DD | "2026-02-17" |
| Enum | String | "active" |
| Object | JSON | {"key": "value"} |
| List | JSON Array | ["item1", "item2"] |

### 5.2 Enum Values

**account_type**: "checking", "savings", "credit"  
**account_status**: "active", "frozen", "closed"  
**transaction_type**: "debit", "credit", "transfer", "purchase", "cashback"  
**transaction_status**: "pending", "completed", "failed", "reversed"  
**product_status**: "active", "inactive", "out_of_stock"  
**benefit_type**: "cashback", "msi", "discount"  
**benefit_status**: "active", "expired", "exhausted"  
**purchase_status**: "pending_payment", "completed", "failed", "cancelled"  
**relationship**: "family", "friend", "vendor"  
**beneficiary_status**: "active", "inactive", "deleted"

---

## Success Criteria

- [x] All entities defined with complete attributes
- [x] Data types specified for all attributes
- [x] Relationships and cardinalities documented
- [x] Indexes defined for query patterns
- [x] Business rules documented per entity
- [x] Enum values specified

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17  
**Next Step**: Generate Business Rules document
