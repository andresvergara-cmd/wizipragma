"""
WebSocket Message Handler - Unit 2: AgentCore & Orchestration
Handles incoming WebSocket messages and orchestrates processing.
"""
import json
import os
import time
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

# Environment variables
SESSIONS_TABLE = os.environ['SESSIONS_TABLE']
EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']
AGENTCORE_ID = os.environ.get('AGENTCORE_ID', '')
ASSETS_BUCKET = os.environ['ASSETS_BUCKET']
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# AWS clients
dynamodb = boto3.resource('dynamodb')
sessions_table = dynamodb.Table(SESSIONS_TABLE)
eventbridge = boto3.client('events')
bedrock_agent = boto3.client('bedrock-agent-runtime')
apigateway = boto3.client('apigatewaymanagementapi')


def lambda_handler(event, context):
    """
    Handle WebSocket $default route (messages).
    
    Args:
        event: API Gateway WebSocket event with message
        context: Lambda context
        
    Returns:
        Response with statusCode 200
    """
    connection_id = event['requestContext']['connectionId']
    domain_name = event['requestContext']['domainName']
    stage = event['requestContext']['stage']
    
    # Initialize API Gateway Management API client with endpoint
    global apigateway
    apigateway = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url=f"https://{domain_name}/{stage}"
    )
    
    try:
        # Parse message
        body = json.loads(event.get('body', '{}'))
        message_type = body.get('type', 'TEXT')
        content = body.get('content', '')
        
        # Get session
        session = get_session_by_connection(connection_id)
        if not session:
            send_error(connection_id, "Session not found")
            return {'statusCode': 200}
        
        session_id = session['session_id']
        user_id = session['user_id']
        
        # Update last activity
        update_session_activity(session_id)
        
        # Process message based on type
        if message_type == 'TEXT':
            response = process_text_message(content, session_id, user_id, connection_id)
        elif message_type == 'VOICE':
            response = process_voice_message(content, session_id, user_id, connection_id)
        elif message_type == 'IMAGE':
            response = process_image_message(content, session_id, user_id, connection_id)
        else:
            response = {"error": "Unknown message type"}
        
        # Send response
        send_message(connection_id, response)
        
        return {'statusCode': 200}
        
    except Exception as e:
        print(f"ERROR: Message processing failed for connection {connection_id}: {str(e)}")
        send_error(connection_id, "Processing failed")
        return {'statusCode': 200}


def get_session_by_connection(connection_id: str) -> dict:
    """Get session by connection_id."""
    try:
        response = sessions_table.scan(
            FilterExpression='connection_id = :conn_id AND #state = :state',
            ExpressionAttributeNames={'#state': 'state'},
            ExpressionAttributeValues={
                ':conn_id': connection_id,
                ':state': 'ACTIVE'
            }
        )
        return response['Items'][0] if response.get('Items') else None
    except Exception as e:
        print(f"ERROR: Failed to get session: {str(e)}")
        return None


def update_session_activity(session_id: str):
    """Update session last_activity timestamp."""
    try:
        sessions_table.update_item(
            Key={'session_id': session_id},
            UpdateExpression='SET last_activity = :timestamp, message_count = message_count + :inc',
            ExpressionAttributeValues={
                ':timestamp': int(datetime.utcnow().timestamp()),
                ':inc': 1
            }
        )
    except Exception as e:
        print(f"ERROR: Failed to update session activity: {str(e)}")


def process_text_message(content: str, session_id: str, user_id: str, connection_id: str) -> dict:
    """
    Process text message through AgentCore.
    
    Args:
        content: Text message content
        session_id: Session ID
        user_id: User ID
        connection_id: WebSocket connection ID
        
    Returns:
        Response dict with text or error
    """
    try:
        # Invoke AgentCore (simplified for hackathon)
        if not AGENTCORE_ID:
            # Fallback: Echo response for testing
            return {
                "type": "TEXT",
                "content": f"Echo: {content}",
                "metadata": {"timestamp": datetime.utcnow().isoformat()}
            }
        
        # Invoke Bedrock Agent
        response = bedrock_agent.invoke_agent(
            agentId=AGENTCORE_ID,
            agentAliasId='TSTALIASID',  # Test alias
            sessionId=session_id,
            inputText=content
        )
        
        # Extract response text
        response_text = extract_agent_response(response)
        
        return {
            "type": "TEXT",
            "content": response_text,
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
        
    except Exception as e:
        print(f"ERROR: Text processing failed: {str(e)}")
        return {"error": f"Processing failed: {str(e)}"}


def process_voice_message(audio_data: str, session_id: str, user_id: str, connection_id: str) -> dict:
    """
    Process voice message (base64 audio).
    
    Note: Simplified for hackathon. Full implementation would:
    1. Decode base64 audio
    2. Invoke Nova Sonic for transcription
    3. Process text through AgentCore
    4. Invoke Nova Sonic for synthesis
    5. Return audio response
    """
    try:
        # Placeholder: Return text response
        return {
            "type": "TEXT",
            "content": "Voice processing not yet implemented. Please use text.",
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
    except Exception as e:
        print(f"ERROR: Voice processing failed: {str(e)}")
        return {"error": f"Voice processing failed: {str(e)}"}


def process_image_message(image_data: str, session_id: str, user_id: str, connection_id: str) -> dict:
    """
    Process image message (base64 image).
    
    Note: Simplified for hackathon. Full implementation would:
    1. Decode base64 image
    2. Upload to S3
    3. Invoke Nova Canvas for analysis
    4. Process results through AgentCore
    5. Return response
    """
    try:
        # Placeholder: Return text response
        return {
            "type": "TEXT",
            "content": "Image processing not yet implemented. Please use text.",
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
    except Exception as e:
        print(f"ERROR: Image processing failed: {str(e)}")
        return {"error": f"Image processing failed: {str(e)}"}


def extract_agent_response(response) -> str:
    """Extract text from Bedrock Agent response."""
    try:
        # Parse streaming response
        event_stream = response['completion']
        response_text = ""
        
        for event in event_stream:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    response_text += chunk['bytes'].decode('utf-8')
        
        return response_text or "No response from agent"
        
    except Exception as e:
        print(f"ERROR: Failed to extract agent response: {str(e)}")
        return "Error processing response"


def send_message(connection_id: str, message: dict):
    """Send message to WebSocket connection."""
    try:
        apigateway.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(message).encode('utf-8')
        )
    except Exception as e:
        print(f"ERROR: Failed to send message to {connection_id}: {str(e)}")


def send_error(connection_id: str, error_message: str):
    """Send error message to WebSocket connection."""
    try:
        error_response = {
            "type": "ERROR",
            "content": error_message,
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
        send_message(connection_id, error_response)
    except Exception as e:
        print(f"ERROR: Failed to send error to {connection_id}: {str(e)}")
