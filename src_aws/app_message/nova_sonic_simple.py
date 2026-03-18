"""
Simplified Nova Sonic Client for Lambda
Handles STT (Speech-to-Text) and TTS (Text-to-Speech)
"""

import os
import base64
import json
import boto3
import logging
from io import BytesIO

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# AWS Configuration
REGION_NAME = 'us-east-1'
MODEL_ID = 'amazon.nova-sonic-v1:0'

# Audio configuration
INPUT_SAMPLE_RATE = 16000  # Frontend sends 16kHz
OUTPUT_SAMPLE_RATE = 24000  # Nova Sonic outputs 24kHz

# Initialize Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name=REGION_NAME)


def transcribe_audio(audio_base64: str) -> str:
    """
    Transcribe audio to text using Nova Sonic STT
    
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
        
        # Convert WebM to PCM
        pcm_audio = convert_to_pcm(audio_bytes)
        logger.info(f"Audio converted to PCM: {len(pcm_audio)} bytes")
        
        # Invoke Nova Sonic for transcription with streaming
        response = bedrock_runtime.invoke_model_with_response_stream(
            modelId=MODEL_ID,
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
        
        # Parse streaming response
        transcription = ""
        stream = response.get('body')
        
        if stream:
            for event in stream:
                chunk = event.get('chunk')
                if chunk:
                    chunk_data = json.loads(chunk.get('bytes').decode())
                    
                    # Extract text from chunk
                    if 'contentBlockDelta' in chunk_data:
                        delta = chunk_data['contentBlockDelta']
                        if 'delta' in delta:
                            delta_content = delta['delta']
                            if 'text' in delta_content:
                                transcription += delta_content['text']
        
        logger.info(f"Transcription completed: {transcription[:100]}...")
        return transcription.strip()
        
    except Exception as e:
        logger.error(f"Error in Nova Sonic transcription: {str(e)}")
        raise Exception(f"Transcription failed: {str(e)}")


def synthesize_speech(text: str) -> dict:
    """
    Synthesize text to speech using Nova Sonic TTS with streaming
    
    Args:
        text: Text to synthesize in Spanish
        
    Returns:
        dict: {
            'audio_chunks': list of base64 audio chunks,
            'total_size': total size in bytes
        }
    """
    try:
        logger.info(f"Starting Nova Sonic TTS (text length: {len(text)} chars)")
        
        # Invoke Nova Sonic for TTS with streaming
        response = bedrock_runtime.invoke_model_with_response_stream(
            modelId=MODEL_ID,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "schemaVersion": "messages-v1",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": f"Convierte este texto a audio en español colombiano con voz femenina amigable: {text}"
                            }
                        ]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 4096,
                    "temperature": 0.5
                },
                "audioConfig": {
                    "format": "pcm",
                    "sampleRate": OUTPUT_SAMPLE_RATE
                }
            })
        )
        
        # Collect audio chunks
        audio_chunks = []
        total_size = 0
        stream = response.get('body')
        
        if stream:
            for event in stream:
                chunk = event.get('chunk')
                if chunk:
                    chunk_data = json.loads(chunk.get('bytes').decode())
                    
                    # Extract audio from chunk
                    if 'contentBlockDelta' in chunk_data:
                        delta = chunk_data['contentBlockDelta']
                        if 'delta' in delta:
                            delta_content = delta['delta']
                            if 'audio' in delta_content:
                                audio_data = delta_content['audio']
                                if 'bytes' in audio_data:
                                    audio_chunk = audio_data['bytes']
                                    audio_chunks.append(audio_chunk)
                                    total_size += len(base64.b64decode(audio_chunk))
        
        logger.info(f"TTS completed: {len(audio_chunks)} chunks, {total_size} bytes total")
        
        return {
            'audio_chunks': audio_chunks,
            'total_size': total_size,
            'sample_rate': OUTPUT_SAMPLE_RATE,
            'format': 'pcm'
        }
        
    except Exception as e:
        logger.error(f"Error in Nova Sonic TTS: {str(e)}")
        raise Exception(f"TTS failed: {str(e)}")


def convert_to_pcm(audio_bytes: bytes) -> bytes:
    """
    Convert WebM audio to PCM format required by Nova Sonic
    
    Args:
        audio_bytes: Raw audio bytes (WebM format)
        
    Returns:
        bytes: PCM audio bytes (16kHz, 16-bit, mono)
    """
    try:
        from pydub import AudioSegment
        
        # Set ffmpeg path from Lambda Layer
        AudioSegment.converter = "/opt/bin/ffmpeg"
        AudioSegment.ffprobe = "/opt/bin/ffprobe"
        
        # Load audio from bytes
        audio = AudioSegment.from_file(
            BytesIO(audio_bytes),
            format="webm"
        )
        
        # Convert to PCM format required by Nova Sonic
        # 16kHz, 16-bit, mono
        audio = audio.set_frame_rate(INPUT_SAMPLE_RATE)
        audio = audio.set_sample_width(2)  # 16-bit = 2 bytes
        audio = audio.set_channels(1)  # mono
        
        # Export as raw PCM
        pcm_bytes = audio.raw_data
        
        return pcm_bytes
        
    except ImportError as e:
        logger.error(f"pydub not available: {str(e)}")
        raise Exception("Audio conversion failed: pydub not available")
    except Exception as e:
        logger.error(f"Error converting audio to PCM: {str(e)}")
        raise Exception(f"Audio conversion failed: {str(e)}")
