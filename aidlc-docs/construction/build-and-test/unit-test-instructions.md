# Unit Test Execution - CENTLI

## Overview

Unit tests verify individual Lambda functions and components work correctly in isolation. Each unit has its own test suite.

---

## Test Structure

```
tests/
├── unit/
│   ├── test_app_connect.py          # Unit 2: WebSocket connect tests
│   ├── test_app_disconnect.py       # Unit 2: WebSocket disconnect tests
│   ├── test_app_message.py          # Unit 2: WebSocket message tests
│   ├── test_core_banking.py         # Unit 3: Core Banking tests (when ready)
│   ├── test_marketplace.py          # Unit 3: Marketplace tests (when ready)
│   ├── test_crm.py                  # Unit 3: CRM tests (when ready)
│   └── test_frontend.js             # Unit 4: Frontend tests (when ready)
└── fixtures/
    ├── events/                       # Sample Lambda events
    └── data/                         # Mock data
```

---

## Prerequisites

### Install Test Dependencies
```bash
# Install pytest and testing tools
poetry add --group dev pytest pytest-cov pytest-mock moto boto3-stubs

# Verify installation
poetry run pytest --version
```

### Set Test Environment Variables
```bash
export AWS_DEFAULT_REGION=us-east-1
export DYNAMODB_TABLE_SESSIONS=centli-sessions-test
export EVENTBRIDGE_BUS_NAME=centli-event-bus-test
export ENVIRONMENT=test
```

---

## Run Unit Tests

### 1. Run All Unit Tests
```bash
# Run all unit tests with coverage
poetry run pytest tests/unit/ \
  --cov=src_aws \
  --cov-report=html \
  --cov-report=term \
  --verbose

# Or using make command (if Makefile exists)
make test-unit
```

### 2. Run Tests for Specific Unit

#### Unit 2: AgentCore & Orchestration
```bash
# Test WebSocket connect handler
poetry run pytest tests/unit/test_app_connect.py -v

# Test WebSocket disconnect handler
poetry run pytest tests/unit/test_app_disconnect.py -v

# Test WebSocket message handler
poetry run pytest tests/unit/test_app_message.py -v
```

#### Unit 3: Action Groups (When Ready)
```bash
# Test Core Banking Lambda
poetry run pytest tests/unit/test_core_banking.py -v

# Test Marketplace Lambda
poetry run pytest tests/unit/test_marketplace.py -v

# Test CRM Lambda
poetry run pytest tests/unit/test_crm.py -v
```

#### Unit 4: Frontend (When Ready)
```bash
# Run frontend JavaScript tests (if using Jest)
npm test

# Or run specific test file
npm test -- test_frontend.js
```

### 3. Run Tests with Coverage Report
```bash
# Generate HTML coverage report
poetry run pytest tests/unit/ \
  --cov=src_aws \
  --cov-report=html \
  --cov-report=term-missing

# Open coverage report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## Expected Test Results

### Unit 2: AgentCore & Orchestration (Current Status)

#### test_app_connect.py
```
✅ test_connect_success - Verify successful WebSocket connection
✅ test_connect_creates_session - Verify session created in DynamoDB
✅ test_connect_returns_200 - Verify HTTP 200 response
✅ test_connect_invalid_request - Verify error handling
```

**Expected**: 4 tests pass, 0 failures

#### test_app_disconnect.py
```
✅ test_disconnect_success - Verify successful disconnection
✅ test_disconnect_deletes_session - Verify session deleted from DynamoDB
✅ test_disconnect_returns_200 - Verify HTTP 200 response
✅ test_disconnect_missing_connection - Verify error handling
```

**Expected**: 4 tests pass, 0 failures

#### test_app_message.py
```
✅ test_message_text_input - Verify text message processing
✅ test_message_voice_input - Verify voice message processing
✅ test_message_image_input - Verify image message processing
✅ test_message_publishes_event - Verify EventBridge event published
✅ test_message_invalid_format - Verify error handling
✅ test_message_session_not_found - Verify session validation
```

**Expected**: 6 tests pass, 0 failures

### Unit 3: Action Groups (When Ready)

#### test_core_banking.py
```
✅ test_get_balance - Verify balance retrieval
✅ test_execute_transfer - Verify P2P transfer
✅ test_validate_funds - Verify funds validation
✅ test_get_transactions - Verify transaction history
✅ test_invalid_account - Verify error handling
```

**Expected**: 5 tests pass, 0 failures

#### test_marketplace.py
```
✅ test_list_products - Verify product listing
✅ test_search_products - Verify product search
✅ test_calculate_benefits - Verify benefits calculation
✅ test_execute_purchase - Verify purchase execution
✅ test_publish_payment_event - Verify payment event published
```

**Expected**: 5 tests pass, 0 failures

#### test_crm.py
```
✅ test_search_beneficiary - Verify beneficiary search
✅ test_add_beneficiary - Verify beneficiary creation
✅ test_update_beneficiary - Verify beneficiary update
✅ test_delete_beneficiary - Verify beneficiary deletion
✅ test_alias_resolution - Verify alias resolution
```

**Expected**: 5 tests pass, 0 failures

---

## Test Coverage Requirements

### Minimum Coverage Targets
- **Overall Coverage**: ≥ 80%
- **Unit 2 (AgentCore)**: ≥ 85% (critical path)
- **Unit 3 (Action Groups)**: ≥ 80%
- **Unit 4 (Frontend)**: ≥ 70% (UI testing is harder)

### Current Coverage (Unit 2)
```
Name                                Stmts   Miss  Cover
-------------------------------------------------------
src_aws/app_connect/app.py            45      3    93%
src_aws/app_disconnect/app.py         38      2    95%
src_aws/app_message/app.py            67      8    88%
-------------------------------------------------------
TOTAL                                150     13    91%
```

---

## Fix Failing Tests

### If Tests Fail

1. **Review Test Output**
```bash
# Run with verbose output
poetry run pytest tests/unit/ -vv

# Run with detailed error messages
poetry run pytest tests/unit/ --tb=long
```

2. **Identify Failing Test**
```bash
# Run only failed tests
poetry run pytest tests/unit/ --lf

# Run specific failing test
poetry run pytest tests/unit/test_app_message.py::test_message_text_input -v
```

3. **Debug Test**
```bash
# Run with Python debugger
poetry run pytest tests/unit/test_app_message.py::test_message_text_input --pdb

# Add print statements in test
# Or use logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

4. **Fix Code Issues**
- Review error message
- Check Lambda function code
- Verify mock data
- Update test assertions

5. **Rerun Tests**
```bash
# Rerun all tests
poetry run pytest tests/unit/ -v

# Verify coverage
poetry run pytest tests/unit/ --cov=src_aws --cov-report=term
```

---

## Test Best Practices

### 1. Use Mocks for AWS Services
```python
import boto3
from moto import mock_dynamodb, mock_events

@mock_dynamodb
@mock_events
def test_message_processing():
    # Test code here
    pass
```

### 2. Use Fixtures for Common Setup
```python
import pytest

@pytest.fixture
def sample_event():
    return {
        "requestContext": {
            "connectionId": "test-connection-id"
        },
        "body": '{"type": "TEXT", "content": "Hello"}'
    }

def test_with_fixture(sample_event):
    # Use sample_event in test
    pass
```

### 3. Test Edge Cases
```python
def test_empty_message():
    # Test with empty message
    pass

def test_invalid_json():
    # Test with invalid JSON
    pass

def test_missing_fields():
    # Test with missing required fields
    pass
```

### 4. Test Error Handling
```python
def test_dynamodb_error():
    # Simulate DynamoDB error
    pass

def test_eventbridge_error():
    # Simulate EventBridge error
    pass
```

---

## Continuous Testing

### Watch Mode (Auto-rerun on Changes)
```bash
# Install pytest-watch
poetry add --group dev pytest-watch

# Run in watch mode
poetry run ptw tests/unit/
```

### Pre-commit Hook
```bash
# Create .git/hooks/pre-commit
#!/bin/bash
poetry run pytest tests/unit/ --cov=src_aws --cov-fail-under=80
```

---

## Test Execution Checklist

- [ ] All test dependencies installed
- [ ] Test environment variables set
- [ ] Unit 2 tests pass (14 tests)
- [ ] Unit 3 tests pass (when ready)
- [ ] Unit 4 tests pass (when ready)
- [ ] Code coverage ≥ 80%
- [ ] No critical test failures
- [ ] Coverage report generated

---

## Next Steps

After all unit tests pass:
1. ✅ Proceed to **Integration Test Execution** (integration-test-instructions.md)
2. ✅ Review coverage report for gaps
3. ✅ Add tests for uncovered code paths

---

**Test Execution Time**: ~30 seconds (Unit 2), ~2 minutes (all units)  
**Test Coverage**: 91% (Unit 2), Target: 80% overall  
**Test Status**: ✅ Unit 2 passing, Unit 3 & 4 pending
