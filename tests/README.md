# Comfi - Unit Tests

## Structure

```
tests/
├── unit/
│   ├── test_app_connect.py      # WebSocket $connect handler (13 tests)
│   ├── test_app_disconnect.py   # WebSocket $disconnect handler (10 tests)
│   └── test_app_message.py      # WebSocket message handler (12 tests)
└── README.md
```

## Running Tests

```bash
# Install dependencies
pip install pytest

# Set Python path
export PYTHONPATH="${PWD}/src_aws/app_message:${PWD}/src_aws/app_connect:${PWD}/src_aws/app_disconnect"

# Run all tests
python -m pytest tests/unit/ -v -p no:anyio

# Run specific file
python -m pytest tests/unit/test_app_connect.py -v -p no:anyio
```

## Test Coverage

- `test_app_connect.py`: Connection, token validation, session creation, demo mode, error handling
- `test_app_disconnect.py`: Disconnection, session state update, error handling, graceful degradation
- `test_app_message.py`: Session lookup, activity tracking, text processing (echo mode), send/error helpers

Total: 35 unit tests

## Notes

- Tests use mocks for AWS services (DynamoDB, API Gateway, Bedrock)
- `AGENTCORE_ID` is set to empty string for echo mode testing
- Use `-p no:anyio` flag to avoid anyio plugin conflicts on Python 3.13
