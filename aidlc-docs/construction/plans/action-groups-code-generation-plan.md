# Code Generation Plan - Unit 3: Action Groups

## Document Information
- **Unit**: Unit 3 (Action Groups - Backend Services)
- **Stage**: Code Generation
- **Created**: 2026-02-17
- **Context**: Implementation plan for 9 Lambda functions + SAM template updates

---

## Plan Overview

This plan generates code for Unit 3 (Action Groups) following AIDLC framework:
- 9 Lambda functions (Python 3.11)
- Shared utility modules
- SAM template updates
- Data seeding scripts
- Test events

**Estimated Time**: 2-3 hours for AI generation + review

---

## Part 1: Code Generation Planning

### Planning Steps

- [x] Review all design artifacts (Functional, NFR, Infrastructure)
- [x] Identify code components to generate
- [x] Define file structure
- [x] Create generation plan with checkboxes
- [x] Get user approval for plan

---

## Part 2: Code Generation Execution

### Step 1: Shared Utilities (Foundation)

**Purpose**: Common functionality used by all Lambdas

- [x] Create `src_aws/utils/__init__.py`
- [x] Create `src_aws/utils/logger.py` - Structured logging with PII masking
- [x] Create `src_aws/utils/dynamodb_helper.py` - DynamoDB operations with retry
- [x] Create `src_aws/utils/eventbridge_helper.py` - EventBridge publish helper
- [x] Create `src_aws/utils/validation.py` - Input validation utilities
- [x] Create `src_aws/utils/errors.py` - Custom exception classes

**Files**: 6 utility modules ✅ COMPLETE

---

### Step 2: Core Banking Action Group

**Purpose**: Banking operations (balance, transfer, transactions)

#### 2.1 Balance Lambda
- [x] Create `src_aws/core_banking_balance/` directory
- [x] Create `src_aws/core_banking_balance/balance.py` - Lambda handler
- [x] Create `src_aws/core_banking_balance/requirements.txt` - Dependencies

#### 2.2 Transfer Lambda
- [x] Create `src_aws/core_banking_transfer/` directory
- [x] Create `src_aws/core_banking_transfer/transfer.py` - Lambda handler
- [x] Create `src_aws/core_banking_transfer/requirements.txt` - Dependencies

#### 2.3 Transactions Lambda
- [x] Create `src_aws/core_banking_transactions/` directory
- [x] Create `src_aws/core_banking_transactions/transactions.py` - Lambda handler
- [x] Create `src_aws/core_banking_transactions/requirements.txt` - Dependencies

**Files**: 9 files (3 Lambdas × 3 files each) ✅ COMPLETE

---

### Step 3: Marketplace Action Group

**Purpose**: Product catalog, benefits, and purchases

#### 3.1 Catalog Lambda
- [x] Create `src_aws/marketplace_catalog/` directory
- [x] Create `src_aws/marketplace_catalog/catalog.py` - Lambda handler
- [x] Create `src_aws/marketplace_catalog/requirements.txt` - Dependencies

#### 3.2 Benefits Lambda
- [x] Create `src_aws/marketplace_benefits/` directory
- [x] Create `src_aws/marketplace_benefits/benefits.py` - Lambda handler
- [x] Create `src_aws/marketplace_benefits/requirements.txt` - Dependencies

#### 3.3 Purchase Lambda
- [x] Create `src_aws/marketplace_purchase/` directory
- [x] Create `src_aws/marketplace_purchase/purchase.py` - Lambda handler
- [x] Create `src_aws/marketplace_purchase/requirements.txt` - Dependencies

**Files**: 9 files (3 Lambdas × 3 files each) ✅ COMPLETE

---

### Step 4: CRM Action Group

**Purpose**: Beneficiary management and alias resolution

#### 4.1 Resolve Alias Lambda
- [x] Create `src_aws/crm_resolve_alias/` directory
- [x] Create `src_aws/crm_resolve_alias/resolve_alias.py` - Lambda handler
- [x] Create `src_aws/crm_resolve_alias/requirements.txt` - Dependencies

**Functionality**:
- Parse ALIAS_RESOLUTION_REQUEST event
- Normalize alias (lowercase, trim)
- Query centli-beneficiaries GSI by alias_lower
- Fuzzy matching if no exact match
- Publish ALIAS_RESOLUTION_RESPONSE event
- Handle errors with retry

#### 4.2 Get Beneficiaries Lambda
- [x] Create `src_aws/crm_get_beneficiaries/` directory
- [x] Create `src_aws/crm_get_beneficiaries/get_beneficiaries.py` - Lambda handler
- [x] Create `src_aws/crm_get_beneficiaries/requirements.txt` - Dependencies

**Functionality**:
- Parse BENEFICIARIES_QUERY event
- Query centli-beneficiaries table by user_id
- Publish BENEFICIARIES_RESPONSE event
- Handle errors with retry

#### 4.3 Add Beneficiary Lambda
- [x] Create `src_aws/crm_add_beneficiary/` directory
- [x] Create `src_aws/crm_add_beneficiary/add_beneficiary.py` - Lambda handler
- [x] Create `src_aws/crm_add_beneficiary/requirements.txt` - Dependencies

**Functionality**:
- Parse ADD_BENEFICIARY_REQUEST event
- Validate alias uniqueness
- Create beneficiary record
- Publish BENEFICIARY_ADDED event
- Handle errors with retry

**Files**: 9 files (3 Lambdas × 3 files each) ✅ COMPLETE

---

### Step 5: SAM Template Updates

**Purpose**: Add Unit 3 resources to template.yaml

- [x] Add Core Banking DynamoDB tables (accounts, transactions)
- [x] Add Marketplace DynamoDB tables (products, purchases, retailers)
- [x] Add CRM DynamoDB table (beneficiaries)
- [x] Add Core Banking Lambda functions (3)
- [x] Add Marketplace Lambda functions (3)
- [x] Add CRM Lambda functions (3)
- [x] Add EventBridge rules for all Lambdas (9)
- [x] Add IAM permissions for all Lambdas
- [x] Add CloudWatch Log Groups
- [x] Add Outputs (table names, function ARNs)

**Files**: 1 file (template.yaml updates) ✅ COMPLETE

---

### Step 6: Data Seeding Scripts

**Purpose**: Seed initial data for demo

- [x] Create `scripts/seed_accounts.py` - Seed user accounts
- [x] Create `scripts/seed_products.py` - Seed product catalog
- [x] Create `scripts/seed_beneficiaries.py` - Seed beneficiaries
- [x] Create `scripts/seed_all.py` - Run all seed scripts

**Files**: 4 scripts ✅ COMPLETE

---

### Step 7: Test Events

**Purpose**: EventBridge test events for local testing

- [x] Create `events/balance_query.json`
- [x] Create `events/transfer_request.json`
- [x] Create `events/transactions_query.json`
- [x] Create `events/catalog_query.json`
- [x] Create `events/benefits_query.json`
- [x] Create `events/purchase_request.json`
- [x] Create `events/alias_resolution_request.json`
- [x] Create `events/beneficiaries_query.json`
- [x] Create `events/add_beneficiary_request.json`

**Files**: 9 test event files ✅ COMPLETE

---

### Step 8: Documentation

**Purpose**: Code summaries and deployment guides

- [x] Create `aidlc-docs/construction/action-groups/code/code-summary.md`
- [x] Create `aidlc-docs/construction/action-groups/code/deployment-guide.md`
- [ ] Update `README.md` with Unit 3 information

**Files**: 3 documentation files

---

## Code Generation Summary

### Total Files to Generate: 50

| Category | Files | Status |
|----------|-------|--------|
| Shared Utilities | 6 | ✅ Complete |
| Core Banking Lambdas | 9 | ✅ Complete |
| Marketplace Lambdas | 9 | ✅ Complete |
| CRM Lambdas | 9 | ✅ Complete |
| SAM Template | 1 | ⏳ Pending |
| Seed Scripts | 4 | ✅ Complete |
| Test Events | 9 | ✅ Complete |
| Documentation | 3 | 🔄 2/3 Complete |

**Progress**: 44/50 files (88% complete)

---

## Code Quality Standards

### Python Code Standards:
- PEP 8 compliant
- Type hints where appropriate
- Docstrings for all functions
- Error handling with try/except
- Structured logging with correlation_id
- PII masking in logs
- Input validation
- Idempotency checks

### Lambda Handler Pattern:
```python
def lambda_handler(event, context):
    """
    Lambda handler for [ACTION]
    
    Args:
        event: EventBridge event
        context: Lambda context
        
    Returns:
        dict: Response with statusCode and body
    """
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('lambda-name', correlation_id)
    
    try:
        # Parse event
        # Validate input
        # Execute business logic
        # Publish result event
        # Return success
    except Exception as e:
        logger.error('Error processing event', error=str(e))
        # Publish error event
        # Return error
```

---

## Testing Strategy

### Unit Testing (Optional for hackathon):
- Test each Lambda handler independently
- Mock DynamoDB and EventBridge
- Test error scenarios

### Integration Testing:
```bash
# Test via SAM local
sam local invoke CoreBankingBalanceFunction \
  --event events/balance_query.json

# Test via EventBridge
aws events put-events \
  --entries file://events/transfer_request.json
```

### End-to-End Testing:
```bash
# Test via WebSocket
wscat -c "$WEBSOCKET_URL"
> {"type":"TEXT","content":"¿Cuál es mi saldo?"}
```

---

## Deployment Steps

### 1. Build
```bash
sam build
```

### 2. Deploy
```bash
sam deploy --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### 3. Seed Data
```bash
python scripts/seed_all.py
```

### 4. Test
```bash
# Test balance query
aws events put-events \
  --entries file://events/balance_query.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

## Success Criteria

- [ ] All 50 files generated
- [ ] SAM template validates successfully
- [ ] SAM build completes without errors
- [ ] Deployment succeeds
- [ ] All DynamoDB tables created
- [ ] All Lambda functions deployed
- [ ] All EventBridge rules created
- [ ] Data seeding completes
- [ ] End-to-end test passes (balance query)
- [ ] End-to-end test passes (transfer)
- [ ] End-to-end test passes (purchase with compensation)

---

## Risk Mitigation

### Risk 1: Code generation errors
**Mitigation**: Generate in small batches, validate syntax

### Risk 2: SAM template errors
**Mitigation**: Validate template after each section

### Risk 3: Deployment failures
**Mitigation**: Deploy incrementally, check CloudFormation events

### Risk 4: Integration issues
**Mitigation**: Test each Lambda independently first

---

## Next Steps After Code Generation

1. Review generated code
2. Fix any syntax errors
3. Validate SAM template
4. Deploy to AWS
5. Seed data
6. Run integration tests
7. Fix any issues
8. Prepare demo scenarios

---

## Approval Required

**Question**: Ready to proceed with code generation?

**Options**:
A) **Continue to Next Stage**: Proceed with generating all 50 files
B) **Request Changes**: Modify the plan before generation

**Please respond with your choice.**

---

**Plan Status**: Awaiting user approval  
**Total Files**: 50 files to generate  
**Estimated Time**: 2-3 hours for generation + review  
**Next Step**: Execute code generation plan
