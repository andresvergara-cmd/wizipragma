"""
WebSocket Disconnect Handler - Unit 2: AgentCore & Orchestration
Handles WebSocket disconnection and session cleanup.
"""
import os
from datetime import datetime
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
    Handle WebSocket $disconnect route.
    
    Args:
        event: API Gateway WebSocket event
        context: Lambda context
        
    Returns:
        Response with statusCode 200
    """
    connection_id = event['requestContext']['connectionId']
    
    try:
        # Find session by connection_id
        response = sessions_table.scan(
            FilterExpression='connection_id = :conn_id',
            ExpressionAttributeValues={':conn_id': connection_id}
        )
        
        if not response.get('Items'):
            print(f"WARN: No session found for connection {connection_id}")
            return {'statusCode': 200, 'body': 'Disconnected'}
        
        session = response['Items'][0]
        session_id = session['session_id']
        
        # Update session state
        sessions_table.update_item(
            Key={'session_id': session_id},
            UpdateExpression='SET #state = :state, last_activity = :timestamp',
            ExpressionAttributeNames={'#state': 'state'},
            ExpressionAttributeValues={
                ':state': 'DISCONNECTED',
                ':timestamp': int(datetime.utcnow().timestamp())
            }
        )
        
        print(f"INFO: Session disconnected - session_id={session_id}, connection_id={connection_id}")
        
        return {'statusCode': 200, 'body': 'Disconnected'}
        
    except Exception as e:
        print(f"ERROR: Failed to disconnect session for connection {connection_id}: {str(e)}")
        # Return 200 anyway to avoid connection errors
        return {'statusCode': 200, 'body': 'Disconnected'}
