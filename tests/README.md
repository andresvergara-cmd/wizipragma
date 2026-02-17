# CENTLI Unit Tests

## Overview

This directory contains unit tests for CENTLI's Unit 2 (AgentCore & Orchestration).

## Test Structure

```
tests/
├── unit/
│   ├── test_app_connect.py      # WebSocket connect handler tests
│   ├── test_app_disconnect.py   # WebSocket disconnect handler tests
│   └── test_app_message.py      # WebSocket message handler tests
└── README.md
```

## Running Tests

### Install Dependencies

```bash
# Install test dependencies
poetry install --with dev

# Or using pip
pip install pytest pytest-cov pytest-mock moto boto3-stubs
```

### Run All Tests

```bash
# Run all unit tests
poetry run pytest tests/unit/ -v

# Or with coverage
poetry run pytest tests/unit/ --cov=src_aws --cov-report=html --cov-report=term
```

### Run Specific Test File

```bash
# Test connect handler
poetry run pytest tests/unit/test_app_connect.py -v

# Test disconnect handler
poetry run pytest tests/unit/test_app_disconnect.py -v

# Test message handler
poetry run pytest tests/unit/test_app_message.py -v
```

### Run Specific Test

```bash
# Run specific test function
poetry run pytest tests/unit/test_app_connect.py::TestLambdaHandler::test_connect_success -v

# Run specific test class
poetry run pytest tests/unit/test_app_message.py::TestProcessTextMessage -v
```

## Test Coverage

### Current Coverage (Unit 2)

- **test_app_connect.py**: 15 tests
  - Connection success/failure
  - Token validation
  - Session creation
  - Error handling

- **test_app_disconnect.py**: 10 tests
  - Disconnection success
  - Session cleanup
  - Error handling
  - State updates

- **test_app_message.py**: 20 tests
  - Text message processing
  - Voice message handling
  - Image message handling
  - Session management
  - Response sending
  - Error handling

**Total**: 45 unit tests

### Coverage Requirements

- **Target**: ≥ 80% code coverage
- **Current**: Expected ~90% coverage

### View Coverage Report

```bash
# Generate HTML coverage report
poetry run pytest tests/unit/ --cov=src_aws --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Categories

### Unit Tests (`tests/unit/`)

Test individual functions and Lambda handlers in isolation using mocks.

**Characteristics**:
- Fast execution (< 1 second per test)
- No external dependencies
- Use mocks for AWS services
- Test edge cases and error handling

### Integration Tests (Future)

Test interactions between components.

**Location**: `tests/integration/` (to be created)

## Writing Tests

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_env(monkeypatch):
    """Set up environment variables."""
    monkeypatch.setenv('SESSIONS_TABLE', 'test-table')

def test_function_name(mock_env):
    """Test description."""
    # Arrange
    # ... setup
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected
```

### Best Practices

1. **Use descriptive test names**: `test_connect_success`, `test_invalid_token`
2. **Follow AAA pattern**: Arrange, Act, Assert
3. **Mock external dependencies**: DynamoDB, EventBridge, Bedrock
4. **Test edge cases**: Empty inputs, missing fields, errors
5. **Test error handling**: Exceptions, timeouts, invalid data
6. **Use fixtures**: Reuse common setup code
7. **Keep tests independent**: No shared state between tests

### Mocking AWS Services

```python
from unittest.mock import Mock, patch

# Mock DynamoDB
@patch('app_connect.sessions_table')
def test_with_dynamodb(mock_table):
    mock_table.put_item = Mock()
    # ... test code

# Mock API Gateway
@patch('app_message.apigateway')
def test_with_apigateway(mock_api):
    mock_api.post_to_connection = Mock()
    # ... test code
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Pushes to `develop` branch
- Pushes to `main` branch

### CI Configuration

See `.github/workflows/ci-backend.yml` for CI/CD configuration.

## Troubleshooting

### Import Errors

If you get import errors:

```bash
# Ensure src_aws is in Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src_aws"

# Or run tests from project root
cd /path/to/project
poetry run pytest tests/unit/
```

### Mock Not Working

Ensure you're patching the correct location:

```python
# Patch where it's used, not where it's defined
@patch('app_connect.sessions_table')  # ✅ Correct
@patch('boto3.resource')  # ❌ Wrong
```

### Tests Failing

1. Check environment variables are set
2. Verify mocks are configured correctly
3. Check test data matches expected format
4. Review error messages carefully

## Test Maintenance

### Adding New Tests

1. Create test file: `test_<module_name>.py`
2. Add test class: `class Test<FunctionName>`
3. Add test methods: `def test_<scenario>()`
4. Run tests: `pytest tests/unit/test_<module_name>.py -v`

### Updating Tests

When code changes:
1. Update affected tests
2. Add tests for new functionality
3. Remove tests for removed functionality
4. Verify coverage remains ≥ 80%

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Moto (AWS Mocking)](https://docs.getmoto.org/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Last Updated**: 2026-02-17  
**Test Count**: 45 unit tests  
**Coverage**: ~90% (Unit 2)
