"""
Amazon Transcribe STT (Speech-to-Text) Module
Converts audio to text using Amazon Transcribe
"""

import os
import base64
import json
import boto3
import logging
from io import BytesIO
import time

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# AWS Configuration
REGION_NAME = 'us-east-1'

# Initialize Transcribe client
transcribe = boto3.client('transcribe', region_name=REGION_NAME)
s3_client = boto3.client('s3', region_name=REGION_NAME)

# S3 bucket for temporary audio files
ASSETS_BUCKET = os.environ.get('ASSETS_BUCKET', 'centli-assets-777937796305')


def transcribe_audio(audio_base64: str, session_id: str) -> str:
    """
    Transcribe audio to text using Amazon Transcribe
    
    Args:
        audio_base64: Base64 encoded audio (WebM format from browser)
        session_id: Session ID for unique file naming
        
    Returns:
        str: Transcribed text in Spanish
    """
    print("\n" + "=" * 80)
    print("🎙️ TRANSCRIBE_AUDIO STARTED")
    print("=" * 80)
    
    try:
        print(f"📊 Input audio length: {len(audio_base64)} chars")
        print(f"🆔 Session ID: {session_id}")
        
        # Decode base64 to bytes
        print("🔓 Decoding base64...")
        audio_bytes = base64.b64decode(audio_base64)
        print(f"✅ Decoded to {len(audio_bytes)} bytes")
        
        # Convert WebM to WAV (Transcribe supports WAV, MP3, MP4, FLAC, OGG, AMR, WebM)
        # WebM is supported directly, so we can use it as-is
        
        # Upload audio to S3 (Transcribe requires S3 input)
        timestamp = int(time.time())
        audio_key = f"transcribe-temp/{session_id}/{timestamp}.webm"
        s3_uri = f"s3://{ASSETS_BUCKET}/{audio_key}"
        
        print(f"📤 Uploading to S3: {s3_uri}")
        s3_client.put_object(
            Bucket=ASSETS_BUCKET,
            Key=audio_key,
            Body=audio_bytes,
            ContentType='audio/webm'
        )
        print(f"✅ Upload completed")
        
        # Start transcription job
        job_name = f"transcribe-{session_id}-{timestamp}"
        print(f"🚀 Starting transcription job: {job_name}")
        
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat='webm',
            LanguageCode='es-ES'  # Spanish (Spain) - es-CO not supported
            # No Settings needed for simple transcription
        )
        print(f"✅ Transcription job started")
        
        # Wait for transcription to complete (optimized polling)
        max_attempts = 40  # 40 attempts max
        attempt = 0
        poll_interval = 0.3  # Start with 300ms
        max_interval = 1.5  # Max 1.5 seconds
        
        print(f"⏳ Polling for completion (optimized intervals)...")
        
        while attempt < max_attempts:
            attempt += 1
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            
            if attempt % 5 == 0:  # Log every 5 attempts
                print(f"⏳ Status: {job_status} (attempt {attempt}/{max_attempts}, interval: {poll_interval:.2f}s)")
            
            if job_status == 'COMPLETED':
                # Get transcription result
                transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                print(f"✅ Transcription completed in {attempt} attempts!")
                print(f"📥 Transcript URI: {transcript_uri}")
                
                # Download transcript
                print(f"📥 Downloading transcript...")
                import urllib.request
                with urllib.request.urlopen(transcript_uri) as response:
                    transcript_data = json.loads(response.read().decode('utf-8'))
                print(f"✅ Transcript downloaded")
                
                # Extract text
                transcription = transcript_data['results']['transcripts'][0]['transcript']
                print(f"📝 Transcription: '{transcription}'")
                
                # Cleanup: Delete S3 file and transcription job
                print(f"🧹 Cleaning up...")
                try:
                    s3_client.delete_object(Bucket=ASSETS_BUCKET, Key=audio_key)
                    print(f"✅ S3 file deleted")
                    transcribe.delete_transcription_job(TranscriptionJobName=job_name)
                    print(f"✅ Transcription job deleted")
                except Exception as cleanup_error:
                    print(f"⚠️ Cleanup warning: {str(cleanup_error)}")
                
                print("=" * 80)
                print("✅ TRANSCRIBE_AUDIO COMPLETED")
                print("=" * 80 + "\n")
                
                return transcription.strip()
                
            elif job_status == 'FAILED':
                error_msg = status['TranscriptionJob'].get('FailureReason', 'Unknown error')
                print(f"❌ Transcription failed: {error_msg}")
                
                # Cleanup
                try:
                    s3_client.delete_object(Bucket=ASSETS_BUCKET, Key=audio_key)
                    transcribe.delete_transcription_job(TranscriptionJobName=job_name)
                except:
                    pass
                
                raise Exception(f"Transcription failed: {error_msg}")
            
            # Wait before next check with exponential backoff
            time.sleep(poll_interval)
            poll_interval = min(poll_interval * 1.15, max_interval)  # Gradual increase
        
        # Timeout
        print(f"❌ Transcription timeout after {attempt} attempts (~{attempt * 0.5:.1f} seconds)")
        
        # Cleanup
        try:
            s3_client.delete_object(Bucket=ASSETS_BUCKET, Key=audio_key)
            transcribe.delete_transcription_job(TranscriptionJobName=job_name)
        except:
            pass
        
        raise Exception(f"Transcription timeout after {attempt} attempts")
        
    except Exception as e:
        print("\n" + "!" * 80)
        print("❌ ERROR IN TRANSCRIBE_AUDIO")
        print("!" * 80)
        print(f"ERROR: {str(e)}")
        import traceback
        print(f"TRACEBACK:\n{traceback.format_exc()}")
        print("!" * 80 + "\n")
        raise Exception(f"Transcription failed: {str(e)}")
