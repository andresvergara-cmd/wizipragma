"""
WebSocket Connect Handler - Unit 2: AgentCore & Orchestration
Handles WebSocket connection establishment and session creation.
"""
import json
import os
import time
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError

# Environment variables
SESSIONS_TABLE = os.environ['SESSIONS_TABLE']
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# AWS clients
dynamodb = boto3.resource('dynamodb')
sessions_table = dynamodb.Table(SESSIONS_TABLE)


def lambda_handler(event, context):
    """
    Handle WebSocket $connect route.
    
    Args:
        event: API Gateway WebSocket event
        context: Lambda context
        
    Returns:
        Response with statusCode 200 (success) or 401/403 (auth failure)
    """
    connection_id = event['requestContext']['connectionId']
    
    try:
        # Extract auth token from query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        token = query_params.get('token')
        
        if not token:
            print(f"ERROR: No auth token provided for connection {connection_id}")
            return {'statusCode': 401, 'body': 'Unauthorized'}
        
        # Validate token and extract user_id (simplified for hackathon)
        user_id = validate_token(token)
        if not user_id:
            print(f"ERROR: Invalid token for connection {connection_id}")
            return {'statusCode': 403, 'body': 'Forbidden'}
        
        # Create session
        session_id = f"session_{int(time.time())}_{user_id}"
        created_at = int(datetime.utcnow().timestamp())
        expires_at = int((datetime.utcnow() + timedelta(hours=4)).timestamp())
        
        session_item = {
            'session_id': session_id,
            'user_id': user_id,
            'connection_id': connection_id,
            'state': 'ACTIVE',
            'created_at': created_at,
            'expires_at': expires_at,
            'last_activity': created_at,
            'message_count': 0,
            'user_preferences': {
                'language': 'es-MX',
                'voice_gender': 'neutral',
                'voice_speed': 'normal'
            }
        }
        
        sessions_table.put_item(Item=session_item)
        
        print(f"INFO: Session created - session_id={session_id}, user_id={user_id}, connection_id={connection_id}")
        
        return {'statusCode': 200, 'body': 'Connected'}
        
    except Exception as e:
        print(f"ERROR: Failed to create session for connection {connection_id}: {str(e)}")
        return {'statusCode': 500, 'body': 'Internal Server Error'}


def validate_token(token: str) -> str:
    """
    Validate JWT token and extract user_id.
    
    Args:
        token: JWT token string
        
    Returns:
        user_id if valid, None otherwise
        
    Note: Simplified validation for hackathon demo.
    Production should use proper JWT validation with signature verification.
    """
    try:
        # Simplified: Extract user_id from token payload
        # In production, use PyJWT library for proper validation
        import base64
        
        # Split token (header.payload.signature)
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decode payload (base64)
        payload = parts[1]
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        decoded = base64.b64decode(payload)
        payload_data = json.loads(decoded)
        
        # Extract user_id
        user_id = payload_data.get('user_id')
        
        # Check expiration
        exp = payload_data.get('exp')
        if exp and exp < time.time():
            print(f"WARN: Token expired for user {user_id}")
            return None
        
        return user_id
        
    except Exception as e:
        print(f"ERROR: Token validation failed: {str(e)}")
        return None
