"""
Unit tests for WebSocket Message Handler (Unit 2)
Tests message processing, AgentCore integration, and response handling.
"""
import json
import pytest
from unittest.mock import Mock, patch, MagicMock, call
from datetime import datetime
import sys
import os

# Set environment variables BEFORE importing the module
os.environ['SESSIONS_TABLE'] = 'test-sessions-table'
os.environ['EVENT_BUS_NAME'] = 'test-event-bus'
os.environ['WEBSOCKET_API_ENDPOINT'] = 'https://test.execute-api.us-east-1.amazonaws.com/prod'
os.environ['BEDROCK_AGENT_ID'] = 'test-agent-id'
os.environ['BEDROCK_AGENT_ALIAS_ID'] = 'test-alias-id'
os.environ['AGENTCORE_ID'] = 'test-agentcore-id'
os.environ['ASSETS_BUCKET'] = 'test-assets-bucket'
os.environ['LOG_LEVEL'] = 'INFO'

# Add src_aws to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src_aws/app_message'))

from app_message import (
    lambda_handler,
    get_session_by_connection,
    update_session_activity,
    process_text_message,
    process_voice_message,
    process_image_message,
    send_message,
    send_error
)


@pytest.fixture
def mock_env(monkeypatch):
    """Set up environment variables for tests."""
    monkeypatch.setenv('SESSIONS_TABLE', 'test-sessions-table')
    monkeypatch.setenv('EVENT_BUS_NAME', 'test-event-bus')
    monkeypatch.setenv('AGENTCORE_ID', '')  # Empty for testing
    monkeypatch.setenv('ASSETS_BUCKET', 'test-assets-bucket')
    monkeypatch.setenv('LOG_LEVEL', 'INFO')


@pytest.fixture
def mock_dynamodb_table():
    """Mock DynamoDB table."""
    with patch('app_message.sessions_table') as mock_table:
        yield mock_table


@pytest.fixture
def mock_apigateway():
    """Mock API Gateway Management API."""
    with patch('app_message.apigateway') as mock_api:
        yield mock_api


@pytest.fixture
def text_message_event():
    """Valid text message event."""
    return {
        'requestContext': {
            'connectionId': 'test-connection-123',
            'domainName': 'test.execute-api.us-east-1.amazonaws.com',
            'stage': 'prod',
            'eventType': 'MESSAGE',
            'routeKey': '$default'
        },
        'body': json.dumps({
            'type': 'TEXT',
            'content': '¿Cuál es mi saldo?',
            'metadata': {
                'timestamp': '2026-02-17T10:00:00Z',
                'message_id': 'msg-001'
            }
        })
    }


@pytest.fixture
def voice_message_event():
    """Valid voice message event."""
    return {
        'requestContext': {
            'connectionId': 'test-connection-456',
            'domainName': 'test.execute-api.us-east-1.amazonaws.com',
            'stage': 'prod'
        },
        'body': json.dumps({
            'type': 'VOICE',
            'content': 'base64_encoded_audio_data',
            'metadata': {'timestamp': '2026-02-17T10:00:00Z'}
        })
    }


@pytest.fixture
def image_message_event():
    """Valid image message event."""
    return {
        'requestContext': {
            'connectionId': 'test-connection-789',
            'domainName': 'test.execute-api.us-east-1.amazonaws.com',
            'stage': 'prod'
        },
        'body': json.dumps({
            'type': 'IMAGE',
            'content': 'base64_encoded_image_data',
            'metadata': {'timestamp': '2026-02-17T10:00:00Z'}
        })
    }


@pytest.fixture
def mock_session():
    """Mock session data."""
    return {
        'session_id': 'session_123_user-001',
        'user_id': 'user-001',
        'connection_id': 'test-connection-123',
        'state': 'ACTIVE',
        'created_at': 1708185600,
        'last_activity': 1708185600,
        'message_count': 5
    }


class TestLambdaHandler:
    """Test lambda_handler function."""
    
    def test_text_message_success(self, mock_env, mock_dynamodb_table, mock_apigateway, text_message_event, mock_session):
        """Test successful text message processing."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_dynamodb_table.update_item = Mock()
        mock_apigateway.post_to_connection = Mock()
        
        # Act
        response = lambda_handler(text_message_event, None)
        
        # Assert
        assert response['statusCode'] == 200
        mock_dynamodb_table.scan.assert_called_once()
        mock_dynamodb_table.update_item.assert_called_once()
        mock_apigateway.post_to_connection.assert_called_once()
    
    def test_session_not_found(self, mock_env, mock_dynamodb_table, mock_apigateway, text_message_event):
        """Test message when session doesn't exist."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': []}
        mock_apigateway.post_to_connection = Mock()
        
        # Act
        response = lambda_handler(text_message_event, None)
        
        # Assert
        assert response['statusCode'] == 200
        # Should send error message
        mock_apigateway.post_to_connection.assert_called_once()
        call_args = mock_apigateway.post_to_connection.call_args[1]
        data = json.loads(call_args['Data'].decode('utf-8'))
        assert data['type'] == 'ERROR'
    
    def test_invalid_message_format(self, mock_env, mock_dynamodb_table, mock_apigateway, mock_session):
        """Test message with invalid JSON."""
        # Arrange
        event = {
            'requestContext': {
                'connectionId': 'test-connection-123',
                'domainName': 'test.execute-api.us-east-1.amazonaws.com',
                'stage': 'prod'
            },
            'body': 'invalid json'
        }
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_apigateway.post_to_connection = Mock()
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        # Should send error
        mock_apigateway.post_to_connection.assert_called()
    
    def test_unknown_message_type(self, mock_env, mock_dynamodb_table, mock_apigateway, mock_session):
        """Test message with unknown type."""
        # Arrange
        event = {
            'requestContext': {
                'connectionId': 'test-connection-123',
                'domainName': 'test.execute-api.us-east-1.amazonaws.com',
                'stage': 'prod'
            },
            'body': json.dumps({'type': 'UNKNOWN', 'content': 'test'})
        }
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_apigateway.post_to_connection = Mock()
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        mock_apigateway.post_to_connection.assert_called()


class TestGetSessionByConnection:
    """Test get_session_by_connection function."""
    
    def test_session_found(self, mock_env, mock_dynamodb_table, mock_session):
        """Test finding active session by connection_id."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        
        # Act
        session = get_session_by_connection('test-connection-123')
        
        # Assert
        assert session == mock_session
        mock_dynamodb_table.scan.assert_called_once()
        scan_args = mock_dynamodb_table.scan.call_args[1]
        assert ':conn_id' in scan_args['ExpressionAttributeValues']
        assert scan_args['ExpressionAttributeValues'][':state'] == 'ACTIVE'
    
    def test_session_not_found(self, mock_env, mock_dynamodb_table):
        """Test when no session found."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': []}
        
        # Act
        session = get_session_by_connection('nonexistent-connection')
        
        # Assert
        assert session is None
    
    def test_dynamodb_error(self, mock_env, mock_dynamodb_table):
        """Test handling of DynamoDB error."""
        # Arrange
        mock_dynamodb_table.scan.side_effect = Exception("DynamoDB error")
        
        # Act
        session = get_session_by_connection('test-connection')
        
        # Assert
        assert session is None


class TestUpdateSessionActivity:
    """Test update_session_activity function."""
    
    def test_activity_updated(self, mock_env, mock_dynamodb_table):
        """Test session activity timestamp is updated."""
        # Arrange
        mock_dynamodb_table.update_item = Mock()
        
        # Act
        update_session_activity('session_123')
        
        # Assert
        mock_dynamodb_table.update_item.assert_called_once()
        update_args = mock_dynamodb_table.update_item.call_args[1]
        assert update_args['Key']['session_id'] == 'session_123'
        assert ':timestamp' in update_args['ExpressionAttributeValues']
        assert ':inc' in update_args['ExpressionAttributeValues']
        assert update_args['ExpressionAttributeValues'][':inc'] == 1
    
    def test_message_count_incremented(self, mock_env, mock_dynamodb_table):
        """Test message_count is incremented."""
        # Arrange
        mock_dynamodb_table.update_item = Mock()
        
        # Act
        update_session_activity('session_456')
        
        # Assert
        update_args = mock_dynamodb_table.update_item.call_args[1]
        assert 'message_count = message_count + :inc' in update_args['UpdateExpression']
    
    def test_dynamodb_error_handled(self, mock_env, mock_dynamodb_table):
        """Test that DynamoDB errors are handled gracefully."""
        # Arrange
        mock_dynamodb_table.update_item.side_effect = Exception("Update failed")
        
        # Act & Assert - Should not raise exception
        update_session_activity('session_789')


class TestProcessTextMessage:
    """Test process_text_message function."""
    
    def test_echo_response_when_no_agentcore(self, mock_env):
        """Test echo response when AgentCore ID is not set."""
        # Act
        response = process_text_message('Hello', 'session_123', 'user-001', 'conn-123')
        
        # Assert
        assert response['type'] == 'TEXT'
        assert 'Echo: Hello' in response['content']
        assert 'metadata' in response
        assert 'timestamp' in response['metadata']
    
    def test_response_format(self, mock_env):
        """Test response format is correct."""
        # Act
        response = process_text_message('Test message', 'session_456', 'user-002', 'conn-456')
        
        # Assert
        assert 'type' in response
        assert 'content' in response
        assert 'metadata' in response
        assert isinstance(response['metadata']['timestamp'], str)


class TestProcessVoiceMessage:
    """Test process_voice_message function."""
    
    def test_voice_not_implemented(self, mock_env):
        """Test voice processing returns not implemented message."""
        # Act
        response = process_voice_message('audio_data', 'session_123', 'user-001', 'conn-123')
        
        # Assert
        assert response['type'] == 'TEXT'
        assert 'not yet implemented' in response['content'].lower()


class TestProcessImageMessage:
    """Test process_image_message function."""
    
    def test_image_not_implemented(self, mock_env):
        """Test image processing returns not implemented message."""
        # Act
        response = process_image_message('image_data', 'session_123', 'user-001', 'conn-123')
        
        # Assert
        assert response['type'] == 'TEXT'
        assert 'not yet implemented' in response['content'].lower()


class TestSendMessage:
    """Test send_message function."""
    
    def test_message_sent(self, mock_env, mock_apigateway):
        """Test message is sent to WebSocket connection."""
        # Arrange
        message = {'type': 'TEXT', 'content': 'Test'}
        
        # Act
        send_message('conn-123', message)
        
        # Assert
        mock_apigateway.post_to_connection.assert_called_once()
        call_args = mock_apigateway.post_to_connection.call_args[1]
        assert call_args['ConnectionId'] == 'conn-123'
        
        # Verify message is JSON encoded
        data = json.loads(call_args['Data'].decode('utf-8'))
        assert data == message
    
    def test_send_error_handled(self, mock_env, mock_apigateway):
        """Test that send errors are handled gracefully."""
        # Arrange
        mock_apigateway.post_to_connection.side_effect = Exception("Send failed")
        
        # Act & Assert - Should not raise exception
        send_message('conn-456', {'type': 'TEXT', 'content': 'Test'})


class TestSendError:
    """Test send_error function."""
    
    def test_error_message_sent(self, mock_env, mock_apigateway):
        """Test error message is sent with correct format."""
        # Act
        send_error('conn-789', 'Test error')
        
        # Assert
        mock_apigateway.post_to_connection.assert_called_once()
        call_args = mock_apigateway.post_to_connection.call_args[1]
        
        # Verify error message format
        data = json.loads(call_args['Data'].decode('utf-8'))
        assert data['type'] == 'ERROR'
        assert data['content'] == 'Test error'
        assert 'metadata' in data
        assert 'timestamp' in data['metadata']


class TestIntegration:
    """Integration tests for complete message flow."""
    
    def test_complete_text_message_flow(self, mock_env, mock_dynamodb_table, mock_apigateway, text_message_event, mock_session):
        """Test complete flow from message receipt to response."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_dynamodb_table.update_item = Mock()
        mock_apigateway.post_to_connection = Mock()
        
        # Act
        response = lambda_handler(text_message_event, None)
        
        # Assert
        assert response['statusCode'] == 200
        
        # Verify session was found
        assert mock_dynamodb_table.scan.called
        
        # Verify activity was updated
        assert mock_dynamodb_table.update_item.called
        
        # Verify response was sent
        assert mock_apigateway.post_to_connection.called
        call_args = mock_apigateway.post_to_connection.call_args[1]
        response_data = json.loads(call_args['Data'].decode('utf-8'))
        assert response_data['type'] == 'TEXT'
        assert 'content' in response_data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
