"""
Unit tests for WebSocket Disconnect Handler (Unit 2)
Tests session cleanup and disconnection handling.
"""
import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Add src_aws to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src_aws/app_disconnect'))

from app_disconnect import lambda_handler


@pytest.fixture
def mock_env(monkeypatch):
    """Set up environment variables for tests."""
    monkeypatch.setenv('SESSIONS_TABLE', 'test-sessions-table')
    monkeypatch.setenv('LOG_LEVEL', 'INFO')


@pytest.fixture
def mock_dynamodb_table():
    """Mock DynamoDB table."""
    with patch('app_disconnect.sessions_table') as mock_table:
        yield mock_table


@pytest.fixture
def disconnect_event():
    """Valid WebSocket disconnect event."""
    return {
        'requestContext': {
            'connectionId': 'test-connection-123',
            'eventType': 'DISCONNECT',
            'routeKey': '$disconnect'
        }
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
    
    def test_disconnect_success(self, mock_env, mock_dynamodb_table, disconnect_event, mock_session):
        """Test successful WebSocket disconnection."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_dynamodb_table.update_item = Mock()
        
        # Act
        response = lambda_handler(disconnect_event, None)
        
        # Assert
        assert response['statusCode'] == 200
        assert response['body'] == 'Disconnected'
        
        # Verify scan was called to find session
        mock_dynamodb_table.scan.assert_called_once()
        scan_args = mock_dynamodb_table.scan.call_args[1]
        assert scan_args['FilterExpression'] == 'connection_id = :conn_id'
        assert scan_args['ExpressionAttributeValues'][':conn_id'] == 'test-connection-123'
        
        # Verify update was called to mark session as disconnected
        mock_dynamodb_table.update_item.assert_called_once()
        update_args = mock_dynamodb_table.update_item.call_args[1]
        assert update_args['Key']['session_id'] == 'session_123_user-001'
        assert ':state' in update_args['ExpressionAttributeValues']
        assert update_args['ExpressionAttributeValues'][':state'] == 'DISCONNECTED'
    
    def test_disconnect_session_not_found(self, mock_env, mock_dynamodb_table, disconnect_event):
        """Test disconnection when session doesn't exist."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': []}
        
        # Act
        response = lambda_handler(disconnect_event, None)
        
        # Assert
        assert response['statusCode'] == 200
        assert response['body'] == 'Disconnected'
        mock_dynamodb_table.update_item.assert_not_called()
    
    def test_disconnect_dynamodb_scan_error(self, mock_env, mock_dynamodb_table, disconnect_event):
        """Test disconnection when DynamoDB scan fails."""
        # Arrange
        mock_dynamodb_table.scan.side_effect = Exception("DynamoDB scan error")
        
        # Act
        response = lambda_handler(disconnect_event, None)
        
        # Assert
        # Should return 200 anyway to avoid connection errors
        assert response['statusCode'] == 200
        assert response['body'] == 'Disconnected'
    
    def test_disconnect_dynamodb_update_error(self, mock_env, mock_dynamodb_table, disconnect_event, mock_session):
        """Test disconnection when DynamoDB update fails."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_dynamodb_table.update_item.side_effect = Exception("DynamoDB update error")
        
        # Act
        response = lambda_handler(disconnect_event, None)
        
        # Assert
        # Should return 200 anyway to avoid connection errors
        assert response['statusCode'] == 200
        assert response['body'] == 'Disconnected'
    
    def test_disconnect_updates_last_activity(self, mock_env, mock_dynamodb_table, disconnect_event, mock_session):
        """Test that last_activity timestamp is updated on disconnect."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_dynamodb_table.update_item = Mock()
        
        # Act
        lambda_handler(disconnect_event, None)
        
        # Assert
        update_args = mock_dynamodb_table.update_item.call_args[1]
        assert ':timestamp' in update_args['ExpressionAttributeValues']
        
        # Verify timestamp is recent (within last 5 seconds)
        timestamp = update_args['ExpressionAttributeValues'][':timestamp']
        current_time = int(datetime.utcnow().timestamp())
        assert abs(current_time - timestamp) < 5
    
    def test_disconnect_multiple_sessions_same_connection(self, mock_env, mock_dynamodb_table, disconnect_event):
        """Test disconnection when multiple sessions found (edge case)."""
        # Arrange
        sessions = [
            {'session_id': 'session_1', 'connection_id': 'test-connection-123'},
            {'session_id': 'session_2', 'connection_id': 'test-connection-123'}
        ]
        mock_dynamodb_table.scan.return_value = {'Items': sessions}
        mock_dynamodb_table.update_item = Mock()
        
        # Act
        response = lambda_handler(disconnect_event, None)
        
        # Assert
        assert response['statusCode'] == 200
        # Should update first session found
        mock_dynamodb_table.update_item.assert_called_once()
        update_args = mock_dynamodb_table.update_item.call_args[1]
        assert update_args['Key']['session_id'] == 'session_1'


class TestSessionStateUpdate:
    """Test session state update details."""
    
    def test_state_changed_to_disconnected(self, mock_env, mock_dynamodb_table, disconnect_event, mock_session):
        """Test that session state is changed to DISCONNECTED."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_dynamodb_table.update_item = Mock()
        
        # Act
        lambda_handler(disconnect_event, None)
        
        # Assert
        update_args = mock_dynamodb_table.update_item.call_args[1]
        assert update_args['UpdateExpression'] == 'SET #state = :state, last_activity = :timestamp'
        assert update_args['ExpressionAttributeNames']['#state'] == 'state'
        assert update_args['ExpressionAttributeValues'][':state'] == 'DISCONNECTED'
    
    def test_session_not_deleted(self, mock_env, mock_dynamodb_table, disconnect_event, mock_session):
        """Test that session is not deleted, only marked as disconnected."""
        # Arrange
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        mock_dynamodb_table.update_item = Mock()
        mock_dynamodb_table.delete_item = Mock()
        
        # Act
        lambda_handler(disconnect_event, None)
        
        # Assert
        mock_dynamodb_table.update_item.assert_called_once()
        mock_dynamodb_table.delete_item.assert_not_called()


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_graceful_degradation(self, mock_env, mock_dynamodb_table, disconnect_event):
        """Test that errors don't cause connection issues."""
        # Arrange
        mock_dynamodb_table.scan.side_effect = Exception("Critical error")
        
        # Act
        response = lambda_handler(disconnect_event, None)
        
        # Assert
        # Should always return 200 to avoid WebSocket errors
        assert response['statusCode'] == 200
    
    def test_missing_connection_id(self, mock_env, mock_dynamodb_table):
        """Test handling of event without connection_id."""
        # Arrange
        event = {'requestContext': {}}  # Missing connectionId
        
        # Act & Assert
        with pytest.raises(KeyError):
            lambda_handler(event, None)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
