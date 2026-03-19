"""
Amazon Transcribe Streaming STT (Speech-to-Text) Module
Uses the amazon-transcribe streaming SDK for real-time transcription (~1-3s).
Replaces the batch job approach which took 5-60+ seconds.
"""

import os
import base64
import asyncio
import subprocess
import logging
import time

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# AWS Configuration
REGION_NAME = os.environ.get('AWS_REGION', 'us-east-1')
ASSETS_BUCKET = os.environ.get('ASSETS_BUCKET', 'centli-assets-777937796305')

# Audio settings for Transcribe Streaming
SAMPLE_RATE = 16000  # 16kHz
CHUNK_SIZE = 16000 * 2  # 1 second of 16-bit PCM audio (16000 samples * 2 bytes)


def convert_webm_to_wav(audio_bytes: bytes) -> bytes:
    """Convert WebM/Opus audio to WAV (16kHz, mono, 16-bit PCM) using ffmpeg."""
    print("🔄 Converting WebM to WAV using ffmpeg...")
    
    input_path = '/tmp/input_audio.webm'
    output_path = '/tmp/output_audio.wav'
    
    with open(input_path, 'wb') as f:
        f.write(audio_bytes)
    
    # Find ffmpeg
    ffmpeg_bin = None
    for path in ['/opt/bin/ffmpeg', '/opt/ffmpeg', '/usr/bin/ffmpeg', '/var/task/ffmpeg']:
        if os.path.exists(path):
            ffmpeg_bin = path
            break
    
    if not ffmpeg_bin:
        try:
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
            if result.returncode == 0:
                ffmpeg_bin = result.stdout.strip()
        except:
            pass
    
    if not ffmpeg_bin:
        for root, dirs, files in os.walk('/opt'):
            for f in files:
                if f == 'ffmpeg':
                    ffmpeg_bin = os.path.join(root, f)
                    break
            if ffmpeg_bin:
                break
        if not ffmpeg_bin:
            raise Exception("ffmpeg not found in Lambda Layer")
    
    cmd = [
        ffmpeg_bin, '-y',
        '-i', input_path,
        '-ar', str(SAMPLE_RATE),
        '-ac', '1',
        '-sample_fmt', 's16',
        '-af', 'volume=1.5,highpass=f=80,lowpass=f=8000',
        '-f', 'wav',
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        raise Exception(f"ffmpeg conversion failed: {result.stderr}")
    
    with open(output_path, 'rb') as f:
        wav_bytes = f.read()
    
    duration_seconds = (len(wav_bytes) - 44) / 32000.0
    print(f"✅ Converted to WAV: {len(wav_bytes)} bytes, duration: {duration_seconds:.1f}s")
    
    try:
        os.remove(input_path)
        os.remove(output_path)
    except:
        pass
    
    return wav_bytes


def extract_pcm_from_wav(wav_bytes: bytes) -> bytes:
    """Extract raw PCM data from WAV file (skip 44-byte header)."""
    if wav_bytes[:4] == b'RIFF':
        return wav_bytes[44:]
    return wav_bytes


async def _transcribe_streaming(pcm_audio: bytes) -> str:
    """
    Transcribe audio using Amazon Transcribe Streaming API.
    Sends PCM audio in chunks and receives real-time transcription.
    
    Args:
        pcm_audio: Raw PCM audio bytes (16kHz, mono, 16-bit)
    Returns:
        str: Transcribed text
    """
    from amazon_transcribe.client import TranscribeStreamingClient
    from amazon_transcribe.handlers import TranscriptResultStreamHandler
    from amazon_transcribe.model import TranscriptEvent

    transcript_text = ""

    class MyHandler(TranscriptResultStreamHandler):
        async def handle_transcript_event(self, transcript_event: TranscriptEvent):
            nonlocal transcript_text
            results = transcript_event.transcript.results
            for result in results:
                if not result.is_partial:
                    for alt in result.alternatives:
                        transcript_text += alt.transcript + " "

    client = TranscribeStreamingClient(region=REGION_NAME)

    stream = await client.start_stream_transcription(
        language_code="es-US",
        media_sample_rate_hz=SAMPLE_RATE,
        media_encoding="pcm",
    )

    handler = MyHandler(stream.output_stream)

    # Send audio in chunks (simulate real-time rate to avoid signing issues)
    async def send_audio():
        chunk_size = CHUNK_SIZE  # 1 second of audio
        offset = 0
        while offset < len(pcm_audio):
            end = min(offset + chunk_size, len(pcm_audio))
            chunk = pcm_audio[offset:end]
            await stream.input_stream.send_audio_event(audio_chunk=chunk)
            offset = end
        # Signal end of audio
        await stream.input_stream.end_stream()

    # Run send and receive concurrently
    await asyncio.gather(send_audio(), handler.handle_events())

    return transcript_text.strip()


def transcribe_audio(audio_base64: str, session_id: str) -> str:
    """
    Transcribe audio to text using Amazon Transcribe Streaming.
    
    Args:
        audio_base64: Base64 encoded audio (WebM or WAV from browser)
        session_id: Session ID for logging
        
    Returns:
        str: Transcribed text in Spanish
    """
    print("\n" + "=" * 60)
    print("🎙️ TRANSCRIBE_AUDIO (STREAMING) STARTED")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        print(f"📊 Input base64 length: {len(audio_base64)} chars")
        
        # Decode base64
        audio_bytes = base64.b64decode(audio_base64)
        print(f"✅ Decoded to {len(audio_bytes)} bytes")
        
        # Convert to WAV if needed
        is_wav = audio_bytes[:4] == b'RIFF'
        if is_wav:
            wav_bytes = audio_bytes
        else:
            wav_bytes = convert_webm_to_wav(audio_bytes)
        
        # Extract PCM from WAV
        pcm_audio = extract_pcm_from_wav(wav_bytes)
        duration_s = len(pcm_audio) / (SAMPLE_RATE * 2)
        print(f"📊 PCM audio: {len(pcm_audio)} bytes, ~{duration_s:.1f}s")
        
        # Run streaming transcription
        print("🚀 Starting Transcribe Streaming...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            transcription = loop.run_until_complete(_transcribe_streaming(pcm_audio))
        finally:
            loop.close()
        
        elapsed = time.time() - start_time
        print(f"📝 Transcription: '{transcription}'")
        print(f"⏱️ Total STT time: {elapsed:.1f}s")
        print("=" * 60)
        
        return transcription
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ STREAMING STT FAILED after {elapsed:.1f}s: {str(e)}")
        import traceback
        print(f"TRACEBACK:\n{traceback.format_exc()}")
        
        # Fallback to batch transcription if streaming fails
        print("⚠️ Falling back to batch transcription...")
        return _transcribe_batch_fallback(audio_base64, session_id)


def _transcribe_batch_fallback(audio_base64: str, session_id: str) -> str:
    """
    Fallback: batch transcription if streaming fails.
    Uses the original S3 + StartTranscriptionJob approach.
    """
    import json
    import boto3
    
    transcribe = boto3.client('transcribe', region_name=REGION_NAME)
    s3_client = boto3.client('s3', region_name=REGION_NAME)
    
    audio_bytes = base64.b64decode(audio_base64)
    is_wav = audio_bytes[:4] == b'RIFF'
    
    if not is_wav:
        wav_bytes = convert_webm_to_wav(audio_bytes)
    else:
        wav_bytes = audio_bytes
    
    timestamp = int(time.time())
    audio_key = f"transcribe-temp/{session_id}/{timestamp}.wav"
    s3_uri = f"s3://{ASSETS_BUCKET}/{audio_key}"
    
    s3_client.put_object(Bucket=ASSETS_BUCKET, Key=audio_key, Body=wav_bytes, ContentType='audio/wav')
    
    job_name = f"transcribe-{session_id}-{timestamp}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_uri},
        MediaFormat='wav',
        MediaSampleRateHertz=SAMPLE_RATE,
        LanguageCode='es-US'
    )
    
    max_attempts = 60
    poll_interval = 0.5
    for attempt in range(max_attempts):
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = status['TranscriptionJob']['TranscriptionJobStatus']
        
        if job_status == 'COMPLETED':
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            import urllib.request
            with urllib.request.urlopen(transcript_uri) as response:
                transcript_data = json.loads(response.read().decode('utf-8'))
            transcription = transcript_data['results']['transcripts'][0]['transcript']
            
            try:
                s3_client.delete_object(Bucket=ASSETS_BUCKET, Key=audio_key)
                transcribe.delete_transcription_job(TranscriptionJobName=job_name)
            except:
                pass
            
            return transcription.strip()
        elif job_status == 'FAILED':
            try:
                s3_client.delete_object(Bucket=ASSETS_BUCKET, Key=audio_key)
                transcribe.delete_transcription_job(TranscriptionJobName=job_name)
            except:
                pass
            raise Exception(f"Batch transcription failed: {status['TranscriptionJob'].get('FailureReason')}")
        
        time.sleep(poll_interval)
        poll_interval = min(poll_interval * 1.1, 1.5)
    
    raise Exception("Batch transcription timeout")
