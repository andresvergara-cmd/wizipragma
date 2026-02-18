"""
Module: Nova Sonic Client with Bidirectional Streaming
Handles audio transcription and synthesis using Amazon Bedrock Nova Sonic
"""

import os
import asyncio
import base64
import json
import uuid
import boto3
from io import BytesIO
from loguru import logger

# Audio configuration
INPUT_SAMPLE_RATE = 16000  # Frontend sends 16kHz
OUTPUT_SAMPLE_RATE = 24000  # Nova Sonic outputs 24kHz
CHANNELS = 1
SAMPLE_SIZE_BITS = 16

# AWS Configuration
REGION_NAME = os.environ.get('REGION_NAME', 'us-east-1')
MODEL_ID = 'amazon.nova-sonic-v1:0'


class NovaSonicClient:
    """
    Simplified Nova Sonic client for transcription (STT)
    Uses bidirectional streaming API in a synchronous wrapper
    """
    
    def __init__(self):
        self.bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=REGION_NAME
        )
        self.model_id = MODEL_ID
        self.prompt_name = str(uuid.uuid4())
        self.content_name = str(uuid.uuid4())
        self.audio_content_name = str(uuid.uuid4())
    
    def transcribe_audio(self, audio_base64: str) -> str:
        """
        Transcribe audio to text using Nova Sonic
        
        Args:
            audio_base64: Base64 encoded audio (WebM format from browser)
            
        Returns:
            str: Transcribed text in Spanish
        """
        try:
            logger.info(f"Starting Nova Sonic transcription (audio length: {len(audio_base64)} chars)")
            
            # Decode base64 to bytes
            audio_bytes = base64.b64decode(audio_base64)
            logger.info(f"Audio decoded to {len(audio_bytes)} bytes")
            
            # Convert WebM to PCM if needed
            pcm_audio = self._convert_to_pcm(audio_bytes)
            logger.info(f"Audio converted to PCM: {len(pcm_audio)} bytes")
            
            # Run async transcription in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                transcription = loop.run_until_complete(
                    self._transcribe_async(pcm_audio)
                )
                return transcription
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"Error in Nova Sonic transcription: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
    
    def _convert_to_pcm(self, audio_bytes: bytes) -> bytes:
        """
        Convert WebM audio to PCM format required by Nova Sonic
        
        Args:
            audio_bytes: Raw audio bytes (WebM format)
            
        Returns:
            bytes: PCM audio bytes
        """
        try:
            from pydub import AudioSegment
            
            # Load audio from bytes
            audio = AudioSegment.from_file(
                BytesIO(audio_bytes),
                format="webm"
            )
            
            # Convert to PCM format required by Nova Sonic
            # 16kHz, 16-bit, mono
            audio = audio.set_frame_rate(INPUT_SAMPLE_RATE)
            audio = audio.set_sample_width(2)  # 16-bit = 2 bytes
            audio = audio.set_channels(CHANNELS)
            
            # Export as raw PCM
            pcm_bytes = audio.raw_data
            
            return pcm_bytes
            
        except ImportError:
            logger.warning("pydub not available, using audio as-is (may fail)")
            return audio_bytes
        except Exception as e:
            logger.error(f"Error converting audio to PCM: {str(e)}")
            # Return original bytes as fallback
            return audio_bytes
    
    async def _transcribe_async(self, pcm_audio: bytes) -> str:
        """
        Async transcription using Nova Sonic bidirectional streaming
        
        Args:
            pcm_audio: PCM audio bytes
            
        Returns:
            str: Transcribed text
        """
        transcription_text = ""
        
        try:
            # Start bidirectional stream
            response = self.bedrock_runtime.invoke_model_with_response_stream(
                modelId=self.model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps({
                    "schemaVersion": "messages-v1",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "audio": {
                                        "format": "pcm",
                                        "source": {
                                            "bytes": base64.b64encode(pcm_audio).decode('utf-8')
                                        }
                                    }
                                },
                                {
                                    "text": "Transcribe este audio a texto en español."
                                }
                            ]
                        }
                    ],
                    "inferenceConfig": {
                        "maxTokens": 1000,
                        "temperature": 0.3
                    }
                })
            )
            
            # Process streaming response
            stream = response.get('body')
            if stream:
                for event in stream:
                    chunk = event.get('chunk')
                    if chunk:
                        chunk_data = json.loads(chunk.get('bytes').decode())
                        
                        # Extract text from chunk
                        if 'delta' in chunk_data:
                            delta = chunk_data['delta']
                            if 'text' in delta:
                                transcription_text += delta['text']
                        
                        # Check for complete message
                        if 'message' in chunk_data:
                            message = chunk_data['message']
                            if 'content' in message:
                                for content in message['content']:
                                    if 'text' in content:
                                        transcription_text = content['text']
            
            logger.info(f"Transcription completed: {transcription_text[:100]}...")
            return transcription_text.strip()
            
        except Exception as e:
            logger.error(f"Error in async transcription: {str(e)}")
            raise


def transcribe_audio_with_nova_sonic(audio_base64: str) -> str:
    """
    Main function to transcribe audio using Nova Sonic
    
    Args:
        audio_base64: Base64 encoded audio from frontend
        
    Returns:
        str: Transcribed text in Spanish
    """
    client = NovaSonicClient()
    return client.transcribe_audio(audio_base64)
