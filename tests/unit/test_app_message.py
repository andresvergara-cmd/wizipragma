"""
Unit tests for WebSocket Message Handler
Tests message processing, session management, and response handling.
"""
import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Set environment variables BEFORE importing the module
os.environ['SESSIONS_TABLE'] = 'test-sessions-table'
os.environ['EVENT_BUS_NAME'] = 'test-event-bus'
os.environ['WEBSOCKET_API_ENDPOINT'] = 'https://test.execute-api.us-east-1.amazonaws.com/prod'
os.environ['AGENTCORE_ID'] = ''  # Empty = echo mode
os.environ['AGENTCORE_ALIAS_ID'] = 'TSTALIASID'
os.environ['ASSETS_BUCKET'] = 'test-assets-bucket'
os.environ['LOG_LEVEL'] = 'INFO'

# Add src_aws to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src_aws/app_message'))

from app_message import (
    get_session_by_connection,
    update_session_activity,
    process_text_message,
    process_image_message,
    send_message,
    send_error
)


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv('SESSIONS_TABLE', 'test-sessions-table')
    monkeypatch.setenv('EVENT_BUS_NAME', 'test-event-bus')
    monkeypatch.setenv('AGENTCORE_ID', '')
    monkeypatch.setenv('ASSETS_BUCKET', 'test-assets-bucket')


@pytest.fixture
def mock_dynamodb_table():
    with patch('app_message.sessions_table') as mock_table:
        yield mock_table


@pytest.fixture
def mock_apigateway():
    with patch('app_message.apigateway') as mock_api:
        yield mock_api


@pytest.fixture
def mock_session():
    return {
        'session_id': 'session_123_user-001',
        'user_id': 'user-001',
        'connection_id': 'test-connection-123',
        'state': 'ACTIVE',
        'created_at': 1708185600,
        'last_activity': 1708185600,
        'message_count': 5
    }


class TestGetSessionByConnection:
    def test_session_found(self, mock_env, mock_dynamodb_table, mock_session):
        mock_dynamodb_table.scan.return_value = {'Items': [mock_session]}
        session = get_session_by_connection('test-connection-123')
        assert session == mock_session
        mock_dynamodb_table.scan.assert_called_once()

    def test_session_not_found(self, mock_env, mock_dynamodb_table):
        mock_dynamodb_table.scan.return_value = {'Items': []}
        session = get_session_by_connection('nonexistent')
        assert session is None

    def test_dynamodb_error(self, mock_env, mock_dynamodb_table):
        mock_dynamodb_table.scan.side_effect = Exception("DynamoDB error")
        session = get_session_by_connection('test')
        assert session is None


class TestUpdateSessionActivity:
    def test_activity_updated(self, mock_env, mock_dynamodb_table):
        mock_dynamodb_table.update_item = Mock()
        update_session_activity('session_123')
        mock_dynamodb_table.update_item.assert_called_once()
        args = mock_dynamodb_table.update_item.call_args[1]
        assert args['Key']['session_id'] == 'session_123'
        assert ':inc' in args['ExpressionAttributeValues']
        assert args['ExpressionAttributeValues'][':inc'] == 1

    def test_message_count_incremented(self, mock_env, mock_dynamodb_table):
        mock_dynamodb_table.update_item = Mock()
        update_session_activity('session_456')
        args = mock_dynamodb_table.update_item.call_args[1]
        assert 'message_count = message_count + :inc' in args['UpdateExpression']

    def test_dynamodb_error_handled(self, mock_env, mock_dynamodb_table):
        mock_dynamodb_table.update_item.side_effect = Exception("Update failed")
        update_session_activity('session_789')  # Should not raise


class TestProcessTextMessage:
    def test_echo_response_when_no_agentcore(self, mock_env):
        """When AGENTCORE_ID is empty, returns echo response."""
        response = process_text_message('Hola', 'session_123', 'user-001', 'conn-123')
        assert response['type'] == 'TEXT'
        assert 'Echo: Hola' in response['content']
        assert 'metadata' in response

    def test_response_has_timestamp(self, mock_env):
        response = process_text_message('Test', 'session_456', 'user-002', 'conn-456')
        assert 'timestamp' in response['metadata']


class TestProcessImageMessage:
    def test_image_not_implemented(self, mock_env):
        response = process_image_message('image_data', 'session_123', 'user-001', 'conn-123')
        assert response['type'] == 'TEXT'
        assert 'not yet implemented' in response['content'].lower()


class TestSendMessage:
    def test_message_sent(self, mock_env, mock_apigateway):
        message = {'type': 'TEXT', 'content': 'Test'}
        send_message('conn-123', message)
        mock_apigateway.post_to_connection.assert_called_once()
        args = mock_apigateway.post_to_connection.call_args[1]
        assert args['ConnectionId'] == 'conn-123'
        data = json.loads(args['Data'].decode('utf-8'))
        assert data == message

    def test_send_error_handled(self, mock_env, mock_apigateway):
        mock_apigateway.post_to_connection.side_effect = Exception("Send failed")
        send_message('conn-456', {'type': 'TEXT', 'content': 'Test'})  # Should not raise


class TestSendError:
    def test_error_message_sent(self, mock_env, mock_apigateway):
        send_error('conn-789', 'Test error')
        mock_apigateway.post_to_connection.assert_called_once()
        args = mock_apigateway.post_to_connection.call_args[1]
        data = json.loads(args['Data'].decode('utf-8'))
        assert data['type'] == 'ERROR'
        assert data['content'] == 'Test error'
        assert 'timestamp' in data['metadata']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
