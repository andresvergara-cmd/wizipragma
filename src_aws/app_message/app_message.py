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
    print("=" * 80)
    print("🚀 LAMBDA HANDLER STARTED")
    print("=" * 80)
    
    connection_id = event['requestContext']['connectionId']
    domain_name = event['requestContext']['domainName']
    stage = event['requestContext']['stage']
    
    print(f"📡 Connection ID: {connection_id}")
    print(f"🌐 Domain: {domain_name}")
    print(f"🎭 Stage: {stage}")
    
    # Initialize API Gateway Management API client with endpoint
    global apigateway
    apigateway = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url=f"https://{domain_name}/{stage}"
    )
    print(f"✅ API Gateway client initialized")
    
    try:
        # Parse message
        print("📦 Parsing message body...")
        body = json.loads(event.get('body', '{}'))
        print(f"📦 Body parsed: {json.dumps(body, indent=2)}")
        
        # Support both formats: direct and nested in 'data'
        if 'data' in body:
            # Frontend format: {action: "sendMessage", data: {message, type, ...}}
            data = body.get('data', {})
            message_type = data.get('type', 'TEXT')
            content = data.get('message', data.get('audio', ''))
            include_audio = data.get('includeAudio', False)  # Check if user wants audio response
            print(f"📋 Format: Frontend nested")
        else:
            # Direct format: {type: "TEXT", content: "..."}
            message_type = body.get('type', 'TEXT')
            content = body.get('content', '')
            include_audio = body.get('includeAudio', False)
            print(f"📋 Format: Direct")
        
        print(f"📝 Message type: {message_type}")
        print(f"📏 Content length: {len(content)} chars")
        print(f"🔊 Include audio: {include_audio}")
        
        # Get session
        print(f"🔍 Getting session for connection: {connection_id}")
        session = get_session_by_connection(connection_id)
        if not session:
            print(f"❌ Session not found for connection: {connection_id}")
            send_error(connection_id, "Session not found")
            return {'statusCode': 200}
        
        session_id = session['session_id']
        user_id = session['user_id']
        print(f"✅ Session found: {session_id}")
        print(f"👤 User ID: {user_id}")
        
        # Update last activity
        print(f"⏰ Updating session activity...")
        update_session_activity(session_id)
        print(f"✅ Session activity updated")
        
        # Process message based on type
        print(f"🎯 Processing message type: {message_type}")
        if message_type == 'TEXT':
            print(f"📝 Calling process_text_message...")
            response = process_text_message(content, session_id, user_id, connection_id, include_audio)
        elif message_type == 'VOICE' or message_type == 'AUDIO':
            print(f"🎤 Calling process_voice_message...")
            response = process_voice_message(content, session_id, user_id, connection_id)
        elif message_type == 'IMAGE':
            print(f"🖼️ Calling process_image_message...")
            response = process_image_message(content, session_id, user_id, connection_id)
        else:
            print(f"❌ Unknown message type: {message_type}")
            response = {"error": "Unknown message type"}
        
        print(f"✅ Message processed successfully")
        print(f"📤 Response: {json.dumps(response, indent=2)[:500]}")
        
        # Send response only if not already streamed (TEXT messages are streamed)
        if message_type != 'TEXT':
            print(f"📨 Sending response to client...")
            send_message(connection_id, response)
            print(f"✅ Response sent")
        
        print("=" * 80)
        print("✅ LAMBDA HANDLER COMPLETED SUCCESSFULLY")
        print("=" * 80)
        return {'statusCode': 200}
        
    except Exception as e:
        print("=" * 80)
        print(f"❌ ERROR IN LAMBDA HANDLER")
        print("=" * 80)
        print(f"ERROR: Message processing failed for connection {connection_id}: {str(e)}")
        import traceback
        print(f"TRACEBACK:\n{traceback.format_exc()}")
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


def process_text_message(content: str, session_id: str, user_id: str, connection_id: str, include_audio: bool = False) -> dict:
    """
    Process text message through AgentCore with streaming.
    
    Args:
        content: Text message content
        session_id: Session ID
        user_id: User ID
        connection_id: WebSocket connection ID
        include_audio: Whether to include audio response (TTS)
        
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
        
        # Get agent alias ID from environment
        agent_alias_id = os.environ.get('AGENTCORE_ALIAS_ID', 'TSTALIASID')
        
        # Invoke Bedrock Agent
        response = bedrock_agent.invoke_agent(
            agentId=AGENTCORE_ID,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=content
        )
        
        # Stream response to client (audio is sent automatically if include_audio=True)
        response_text, audio_data = stream_agent_response(response, connection_id, include_audio)
        
        result = {
            "type": "TEXT",
            "content": response_text,
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
        
        if audio_data:
            result["audio"] = audio_data
            result["audio_format"] = "mp3"
        
        return result
        
    except Exception as e:
        print(f"ERROR: Text processing failed: {str(e)}")
        return {"error": f"Processing failed: {str(e)}"}


def process_voice_message(audio_data: str, session_id: str, user_id: str, connection_id: str) -> dict:
    """
    Process voice message using Transcribe STT + Polly TTS
    
    Flow:
    1. Decode base64 audio (WebM from browser)
    2. Amazon Transcribe STT: audio → text
    3. Bedrock Agent: text → response text
    4. Amazon Polly TTS: response text → audio chunks
    5. Stream audio chunks to client
    """
    print("\n" + "=" * 80)
    print("🎤 PROCESS_VOICE_MESSAGE STARTED")
    print("=" * 80)
    
    try:
        print(f"📊 Audio data length: {len(audio_data)} chars")
        print(f"🆔 Session ID: {session_id}")
        print(f"👤 User ID: {user_id}")
        print(f"📡 Connection ID: {connection_id}")
        
        # Step 1: Transcribe audio to text using Amazon Transcribe
        print("\n" + "-" * 80)
        print("STEP 1: TRANSCRIBE STT (Audio → Text)")
        print("-" * 80)
        
        try:
            print("📥 Importing transcribe_stt module...")
            from transcribe_stt import transcribe_audio
            print("✅ Module imported successfully")
            
            print("🎯 Calling transcribe_audio()...")
            transcribed_text = transcribe_audio(audio_data, session_id)
            print(f"✅ Transcription completed")
            print(f"📝 Transcribed text: '{transcribed_text}'")
            
            # Send transcription to client
            print("📤 Sending transcription to client...")
            transcription_message = {
                "msg_type": "transcription",
                "text": transcribed_text
            }
            apigateway.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps(transcription_message).encode('utf-8')
            )
            print("✅ Transcription sent to client")
            
        except Exception as stt_error:
            print("\n" + "!" * 80)
            print("❌ STT ERROR")
            print("!" * 80)
            print(f"ERROR: STT failed: {str(stt_error)}")
            import traceback
            print(f"TRACEBACK:\n{traceback.format_exc()}")
            print("!" * 80)
            
            return {
                "type": "TEXT",
                "content": "Lo siento, no pude entender el audio. Por favor intenta de nuevo.",
                "metadata": {"timestamp": datetime.utcnow().isoformat()}
            }
        
        # Step 2: Process transcribed text through Bedrock Agent
        print("\n" + "-" * 80)
        print("STEP 2: BEDROCK AGENT (Text → Response)")
        print("-" * 80)
        
        if not AGENTCORE_ID:
            print("⚠️ AGENTCORE_ID not set, using echo response")
            return {
                "type": "TEXT",
                "content": f"Escuché: {transcribed_text}",
                "metadata": {"timestamp": datetime.utcnow().isoformat()}
            }
        
        agent_alias_id = os.environ.get('AGENTCORE_ALIAS_ID', 'TSTALIASID')
        print(f"🤖 Agent ID: {AGENTCORE_ID}")
        print(f"🏷️ Agent Alias ID: {agent_alias_id}")
        
        print("📤 Invoking Bedrock Agent...")
        response = bedrock_agent.invoke_agent(
            agentId=AGENTCORE_ID,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=transcribed_text
        )
        print("✅ Bedrock Agent invoked")
        
        # Extract response text (no streaming for voice)
        print("📥 Extracting agent response...")
        response_text = extract_agent_response(response)
        print(f"✅ Response extracted")
        print(f"📝 Response text (first 200 chars): '{response_text[:200]}...'")
        
        # Step 3: Synthesize response to audio using Amazon Polly
        print("\n" + "-" * 80)
        print("STEP 3: POLLY TTS (Text → Audio)")
        print("-" * 80)
        
        try:
            print("📥 Importing polly_tts module...")
            from polly_tts import synthesize_speech
            print("✅ Module imported successfully")
            
            print("🎯 Calling synthesize_speech()...")
            audio_result = synthesize_speech(response_text)
            print(f"✅ Speech synthesized")
            print(f"📊 Audio size: {audio_result['size_bytes']} bytes")
            print(f"📊 Base64 length: {len(audio_result['audio_base64'])} chars")
            
            # Split audio into chunks if too large (100KB limit per WebSocket message)
            audio_base64 = audio_result['audio_base64']
            MAX_CHUNK_SIZE = 100 * 1024  # 100KB
            
            if len(audio_base64) > MAX_CHUNK_SIZE:
                print(f"⚠️ Audio too large ({len(audio_base64)} bytes), splitting into chunks")
                
                # Calculate number of chunks
                total_chunks = (len(audio_base64) + MAX_CHUNK_SIZE - 1) // MAX_CHUNK_SIZE
                print(f"📦 Total chunks: {total_chunks}")
                
                # Send chunks
                for i in range(total_chunks):
                    start = i * MAX_CHUNK_SIZE
                    end = min(start + MAX_CHUNK_SIZE, len(audio_base64))
                    chunk = audio_base64[start:end]
                    
                    print(f"📤 Sending chunk {i+1}/{total_chunks} ({len(chunk)} bytes)...")
                    
                    audio_chunk_message = {
                        "msg_type": "audio_chunk",
                        "chunk_index": i,
                        "total_chunks": total_chunks,
                        "audio_chunk": chunk,
                        "audio_format": "mp3",
                        "sample_rate": audio_result['sample_rate']
                    }
                    
                    apigateway.post_to_connection(
                        ConnectionId=connection_id,
                        Data=json.dumps(audio_chunk_message).encode('utf-8')
                    )
                    print(f"✅ Chunk {i+1}/{total_chunks} sent")
            else:
                # Send complete audio in one message
                print(f"📤 Sending complete audio ({len(audio_base64)} bytes)...")
                audio_message = {
                    "msg_type": "audio_response",
                    "audio": audio_base64,
                    "audio_format": "mp3",
                    "sample_rate": audio_result['sample_rate']
                }
                apigateway.post_to_connection(
                    ConnectionId=connection_id,
                    Data=json.dumps(audio_message).encode('utf-8')
                )
                print(f"✅ Audio sent successfully")
            
        except Exception as tts_error:
            print("\n" + "!" * 80)
            print("⚠️ TTS WARNING (non-fatal)")
            print("!" * 80)
            print(f"WARNING: TTS failed: {str(tts_error)}")
            import traceback
            print(f"TRACEBACK:\n{traceback.format_exc()}")
            print("!" * 80)
            print("ℹ️ Continuing with text-only response")
        
        print("\n" + "=" * 80)
        print("✅ PROCESS_VOICE_MESSAGE COMPLETED")
        print("=" * 80 + "\n")
        
        return {
            "type": "TEXT",
            "content": response_text,
            "metadata": {"timestamp": datetime.utcnow().isoformat()}
        }
        
    except Exception as e:
        print("\n" + "!" * 80)
        print("❌ CRITICAL ERROR IN PROCESS_VOICE_MESSAGE")
        print("!" * 80)
        print(f"ERROR: Voice processing failed: {str(e)}")
        import traceback
        print(f"TRACEBACK:\n{traceback.format_exc()}")
        print("!" * 80 + "\n")
        
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


def stream_agent_response(response, connection_id: str, include_audio: bool = False) -> tuple:
    """
    Stream Bedrock Agent response to WebSocket client in real-time.
    
    Args:
        response: Bedrock Agent response with event stream
        connection_id: WebSocket connection ID
        include_audio: Whether to generate and send audio after streaming
        
    Returns:
        Tuple of (response_text, audio_base64 or None)
    """
    try:
        event_stream = response['completion']
        response_text = ""
        chunk_count = 0
        
        print(f"INFO: Starting to stream response to connection {connection_id}, include_audio={include_audio}")
        
        for event in event_stream:
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    # Decode chunk
                    chunk_text = chunk['bytes'].decode('utf-8')
                    response_text += chunk_text
                    chunk_count += 1
                    
                    print(f"INFO: Sending chunk #{chunk_count}, length={len(chunk_text)}, preview={chunk_text[:50]}")
                    
                    # Send chunk immediately to client (plain text)
                    try:
                        apigateway.post_to_connection(
                            ConnectionId=connection_id,
                            Data=chunk_text.encode('utf-8')
                        )
                        print(f"INFO: Chunk #{chunk_count} sent successfully")
                    except Exception as send_error:
                        print(f"ERROR: Failed to send chunk #{chunk_count}: {str(send_error)}")
        
        print(f"INFO: Streaming complete. Total chunks: {chunk_count}, total length: {len(response_text)}")
        
        # Generate audio if requested
        audio_base64 = None
        if include_audio and response_text:
            try:
                print(f"INFO: Generating audio for response (length: {len(response_text)} chars)")
                from polly_tts import synthesize_speech
                audio_result = synthesize_speech(response_text)
                audio_base64 = audio_result['audio_base64']
                audio_size = audio_result['size_bytes']
                print(f"INFO: Audio generated successfully: {audio_size} bytes, base64 length: {len(audio_base64)}")
                
                # Check if audio is too large for WebSocket (128KB limit)
                # Base64 is ~33% larger than binary, so 128KB binary = ~170KB base64
                # To be safe, use 100KB base64 limit
                MAX_WEBSOCKET_SIZE = 100 * 1024  # 100KB
                
                if len(audio_base64) > MAX_WEBSOCKET_SIZE:
                    print(f"WARNING: Audio too large ({len(audio_base64)} bytes), splitting into chunks")
                    
                    # Split audio into chunks
                    chunk_size = MAX_WEBSOCKET_SIZE
                    total_chunks = (len(audio_base64) + chunk_size - 1) // chunk_size
                    
                    for i in range(total_chunks):
                        start = i * chunk_size
                        end = min(start + chunk_size, len(audio_base64))
                        chunk = audio_base64[start:end]
                        
                        audio_chunk_message = {
                            "msg_type": "audio_chunk",
                            "chunk_index": i,
                            "total_chunks": total_chunks,
                            "audio_chunk": chunk,
                            "audio_format": "mp3",
                            "sample_rate": audio_result.get('sample_rate', '24000')
                        }
                        
                        try:
                            apigateway.post_to_connection(
                                ConnectionId=connection_id,
                                Data=json.dumps(audio_chunk_message).encode('utf-8')
                            )
                            print(f"INFO: Audio chunk {i+1}/{total_chunks} sent successfully")
                        except Exception as chunk_error:
                            print(f"ERROR: Failed to send audio chunk {i+1}: {str(chunk_error)}")
                else:
                    # Send complete audio in one message
                    audio_message = {
                        "msg_type": "audio_response",
                        "audio": audio_base64,
                        "audio_format": "mp3",
                        "sample_rate": audio_result.get('sample_rate', '24000')
                    }
                    apigateway.post_to_connection(
                        ConnectionId=connection_id,
                        Data=json.dumps(audio_message).encode('utf-8')
                    )
                    print(f"INFO: Audio sent to client successfully")
                
            except Exception as audio_error:
                print(f"WARNING: Audio generation failed: {str(audio_error)}")
                import traceback
                print(f"WARNING: Audio error traceback: {traceback.format_exc()}")
        
        return response_text or "No response from agent", audio_base64
        
    except Exception as e:
        print(f"ERROR: Failed to stream agent response: {str(e)}")
        import traceback
        print(f"ERROR: Traceback: {traceback.format_exc()}")
        return "Error processing response", None


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
