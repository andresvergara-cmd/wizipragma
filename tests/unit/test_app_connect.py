"""
Unit tests for WebSocket Connect Handler (Unit 2)
Tests session creation, authentication, and error handling.
"""
import json
import time
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Set environment variables BEFORE importing the module
os.environ['SESSIONS_TABLE'] = 'test-sessions-table'
os.environ['LOG_LEVEL'] = 'INFO'

# Add src_aws to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src_aws/app_connect'))

from app_connect import lambda_handler, validate_token


@pytest.fixture
def mock_env(monkeypatch):
    """Set up environment variables for tests."""
    monkeypatch.setenv('SESSIONS_TABLE', 'test-sessions-table')
    monkeypatch.setenv('LOG_LEVEL', 'INFO')


@pytest.fixture
def mock_dynamodb_table():
    """Mock DynamoDB table."""
    with patch('app_connect.sessions_table') as mock_table:
        yield mock_table


@pytest.fixture
def valid_connect_event():
    """Valid WebSocket connect event."""
    return {
        'requestContext': {
            'connectionId': 'test-connection-123',
            'eventType': 'CONNECT',
            'routeKey': '$connect'
        },
        'queryStringParameters': {
            'token': create_test_token('user-001')
        }
    }


@pytest.fixture
def connect_event_no_token():
    """Connect event without token."""
    return {
        'requestContext': {
            'connectionId': 'test-connection-456',
            'eventType': 'CONNECT',
            'routeKey': '$connect'
        },
        'queryStringParameters': None
    }


def create_test_token(user_id: str) -> str:
    """Create a test JWT token."""
    import base64
    import time
    
    # Create payload
    payload = {
        'user_id': user_id,
        'exp': int(time.time()) + 3600  # Expires in 1 hour
    }
    
    # Encode payload (simplified JWT)
    payload_json = json.dumps(payload)
    payload_b64 = base64.b64encode(payload_json.encode()).decode()
    
    # Create fake JWT (header.payload.signature)
    return f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.{payload_b64}.fake_signature"


class TestLambdaHandler:
    """Test lambda_handler function."""
    
    def test_connect_success(self, mock_env, mock_dynamodb_table, valid_connect_event):
        """Test successful WebSocket connection."""
        # Arrange
        mock_dynamodb_table.put_item = Mock()
        
        # Act
        response = lambda_handler(valid_connect_event, None)
        
        # Assert
        assert response['statusCode'] == 200
        assert response['body'] == 'Connected'
        mock_dynamodb_table.put_item.assert_called_once()
        
        # Verify session item structure
        call_args = mock_dynamodb_table.put_item.call_args
        session_item = call_args[1]['Item']
        assert session_item['user_id'] == 'user-001'
        assert session_item['connection_id'] == 'test-connection-123'
        assert session_item['state'] == 'ACTIVE'
        assert 'session_id' in session_item
        assert 'created_at' in session_item
        assert 'expires_at' in session_item
    
    def test_connect_no_token(self, mock_env, mock_dynamodb_table, connect_event_no_token):
        """Test connection without auth token."""
        # Act
        response = lambda_handler(connect_event_no_token, None)
        
        # Assert
        assert response['statusCode'] == 401
        assert response['body'] == 'Unauthorized'
        mock_dynamodb_table.put_item.assert_not_called()
    
    def test_connect_invalid_token(self, mock_env, mock_dynamodb_table):
        """Test connection with invalid token."""
        # Arrange
        event = {
            'requestContext': {'connectionId': 'test-connection-789'},
            'queryStringParameters': {'token': 'invalid.token.here'}
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 403
        assert response['body'] == 'Forbidden'
        mock_dynamodb_table.put_item.assert_not_called()
    
    def test_connect_dynamodb_error(self, mock_env, mock_dynamodb_table, valid_connect_event):
        """Test connection when DynamoDB fails."""
        # Arrange
        mock_dynamodb_table.put_item.side_effect = Exception("DynamoDB error")
        
        # Act
        response = lambda_handler(valid_connect_event, None)
        
        # Assert
        assert response['statusCode'] == 500
        assert response['body'] == 'Internal Server Error'
    
    def test_session_expiration_set(self, mock_env, mock_dynamodb_table, valid_connect_event):
        """Test that session expiration is set correctly (4 hours)."""
        # Act
        lambda_handler(valid_connect_event, None)
        
        # Assert
        call_args = mock_dynamodb_table.put_item.call_args
        session_item = call_args[1]['Item']
        
        created_at = session_item['created_at']
        expires_at = session_item['expires_at']
        
        # Verify expiration is ~4 hours from creation
        expiration_delta = expires_at - created_at
        assert 14300 <= expiration_delta <= 14500  # ~4 hours (14400 seconds) with tolerance


class TestValidateToken:
    """Test validate_token function."""
    
    def test_valid_token(self):
        """Test validation of valid token."""
        # Arrange
        token = create_test_token('user-123')
        
        # Act
        user_id = validate_token(token)
        
        # Assert
        assert user_id == 'user-123'
    
    def test_invalid_format(self):
        """Test validation of malformed token."""
        # Arrange
        token = "not.a.valid.token.format"
        
        # Act
        user_id = validate_token(token)
        
        # Assert
        assert user_id is None
    
    def test_expired_token(self):
        """Test validation of expired token."""
        # Arrange
        import base64
        import time
        
        payload = {
            'user_id': 'user-expired',
            'exp': int(time.time()) - 3600  # Expired 1 hour ago
        }
        payload_json = json.dumps(payload)
        payload_b64 = base64.b64encode(payload_json.encode()).decode()
        token = f"header.{payload_b64}.signature"
        
        # Act
        user_id = validate_token(token)
        
        # Assert
        assert user_id is None
    
    def test_token_without_user_id(self):
        """Test token without user_id field."""
        # Arrange
        import base64
        
        payload = {'exp': int(time.time()) + 3600}  # No user_id
        payload_json = json.dumps(payload)
        payload_b64 = base64.b64encode(payload_json.encode()).decode()
        token = f"header.{payload_b64}.signature"
        
        # Act
        user_id = validate_token(token)
        
        # Assert
        assert user_id is None
    
    def test_token_invalid_base64(self):
        """Test token with invalid base64 encoding."""
        # Arrange
        token = "header.invalid_base64!@#.signature"
        
        # Act
        user_id = validate_token(token)
        
        # Assert
        assert user_id is None


class TestSessionCreation:
    """Test session creation details."""
    
    def test_session_id_format(self, mock_env, mock_dynamodb_table, valid_connect_event):
        """Test session_id format includes timestamp and user_id."""
        # Act
        lambda_handler(valid_connect_event, None)
        
        # Assert
        call_args = mock_dynamodb_table.put_item.call_args
        session_item = call_args[1]['Item']
        session_id = session_item['session_id']
        
        assert session_id.startswith('session_')
        assert 'user-001' in session_id
    
    def test_user_preferences_default(self, mock_env, mock_dynamodb_table, valid_connect_event):
        """Test default user preferences are set."""
        # Act
        lambda_handler(valid_connect_event, None)
        
        # Assert
        call_args = mock_dynamodb_table.put_item.call_args
        session_item = call_args[1]['Item']
        preferences = session_item['user_preferences']
        
        assert preferences['language'] == 'es-MX'
        assert preferences['voice_gender'] == 'neutral'
        assert preferences['voice_speed'] == 'normal'
    
    def test_message_count_initialized(self, mock_env, mock_dynamodb_table, valid_connect_event):
        """Test message_count is initialized to 0."""
        # Act
        lambda_handler(valid_connect_event, None)
        
        # Assert
        call_args = mock_dynamodb_table.put_item.call_args
        session_item = call_args[1]['Item']
        
        assert session_item['message_count'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
