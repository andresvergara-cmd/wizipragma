"""Module: Inference process"""

# ───────────────────────────────────────────── IMPORTS ─────────────────────────────────────────────
import json
from loguru import logger
from data_config import get_user_context
from config import config
from audio_processor import process_audio_message


# ──────────────────────────────────────────── METHODS ──────────────────────────────────────────────
def lambda_handler(event, context):
    """Main Driver Inference Process"""
    connection_id = event['requestContext']['connectionId']
    payload = json.loads(event['body'])
    logger.info(f'The data received: {payload}')

    data = payload.get('data')
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    message_type = data.get('type', 'TEXT')
    
    # Process based on message type
    if message_type == 'AUDIO':
        logger.info('Processing AUDIO message')
        audio_base64 = data.get('audio')
        
        if not audio_base64:
            logger.error('No audio data provided')
            user_msg = "Error: No se recibió audio"
        else:
            # Transcribe audio to text
            user_msg = process_audio_message(audio_base64)
            logger.info(f'Audio transcribed to: {user_msg}')
    else:
        # TEXT or IMAGE message
        user_msg = data.get('message')

    # Get user context from dynamodb
    user_context = get_user_context(config.table_names, user_id)

    # Generate and transmit agent response
    agent_response = config.chat_with_bedrock(
        user_query=user_msg, 
        user_context=user_context,
        connection_id=connection_id,
        session_id=session_id,
        limit_chat_history=True,
        max_turns=4
    )
    logger.info(f'Agent response len: {len(agent_response)}')

    return {'statusCode': 200}
