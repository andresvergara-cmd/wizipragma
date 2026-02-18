"""
Module: Audio Processing with Amazon Transcribe
Handles audio transcription using Amazon Transcribe Streaming
"""

import boto3
import base64
import uuid
import time
from io import BytesIO
from loguru import logger

# Initialize clients
transcribe = boto3.client('transcribe')
s3 = boto3.client('s3')

# Configuration
S3_BUCKET = 'poc-wizi-mex-audio-temp'  # Temporary bucket for audio files
REGION = 'us-east-1'


def process_audio_message(audio_base64: str) -> str:
    """
    Process audio message: transcribe and return text using Amazon Transcribe
    
    Args:
        audio_base64: Base64 encoded audio from frontend (WebM format)
        
    Returns:
        str: Transcribed text ready for agent processing
    """
    try:
        logger.info("Processing audio message with Amazon Transcribe")
        
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_base64)
        logger.info(f"Audio decoded: {len(audio_bytes)} bytes")
        
        # Generate unique job name
        job_name = f"audio-transcribe-{uuid.uuid4().hex[:8]}-{int(time.time())}"
        s3_key = f"audio-input/{job_name}.webm"
        
        # Upload audio to S3
        logger.info(f"Uploading audio to S3: s3://{S3_BUCKET}/{s3_key}")
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=audio_bytes,
            ContentType='audio/webm'
        )
        
        # Start transcription job
        logger.info(f"Starting transcription job: {job_name}")
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{S3_BUCKET}/{s3_key}'},
            MediaFormat='webm',
            LanguageCode='es-MX',  # Spanish (Mexico)
            Settings={
                'ShowSpeakerLabels': False,
                'MaxSpeakerLabels': 1
            }
        )
        
        # Wait for transcription to complete (max 30 seconds)
        max_wait = 30
        wait_time = 0
        while wait_time < max_wait:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            
            logger.info(f"Transcription status: {job_status}")
            
            if job_status == 'COMPLETED':
                # Get transcription result
                transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                logger.info(f"Transcription completed: {transcript_uri}")
                
                # Download and parse transcript
                import requests
                response = requests.get(transcript_uri)
                transcript_data = response.json()
                
                transcribed_text = transcript_data['results']['transcripts'][0]['transcript']
                logger.info(f"Transcribed text: '{transcribed_text}'")
                
                # Cleanup
                cleanup_transcription(job_name, s3_key)
                
                if not transcribed_text or transcribed_text.strip() == '':
                    return "Lo siento, no pude entender el audio. ¿Podrías repetirlo?"
                
                return transcribed_text.strip()
                
            elif job_status == 'FAILED':
                logger.error("Transcription job failed")
                cleanup_transcription(job_name, s3_key)
                return "Lo siento, hubo un error procesando tu mensaje de voz. ¿Podrías escribirlo?"
            
            # Wait before checking again
            time.sleep(1)
            wait_time += 1
        
        # Timeout
        logger.warning(f"Transcription timeout after {max_wait} seconds")
        cleanup_transcription(job_name, s3_key)
        return "Lo siento, el procesamiento de audio tomó demasiado tiempo. ¿Podrías escribirlo?"
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        return "Lo siento, hubo un error procesando tu mensaje de voz. ¿Podrías escribirlo?"


def cleanup_transcription(job_name: str, s3_key: str):
    """
    Cleanup transcription job and S3 file
    
    Args:
        job_name: Transcription job name
        s3_key: S3 object key
    """
    try:
        # Delete transcription job
        transcribe.delete_transcription_job(TranscriptionJobName=job_name)
        logger.info(f"Deleted transcription job: {job_name}")
    except Exception as e:
        logger.warning(f"Could not delete transcription job: {str(e)}")
    
    try:
        # Delete S3 object
        s3.delete_object(Bucket=S3_BUCKET, Key=s3_key)
        logger.info(f"Deleted S3 object: {s3_key}")
    except Exception as e:
        logger.warning(f"Could not delete S3 object: {str(e)}")
