#!/usr/bin/env python3
"""
Direct Lambda invocation test for voice pipeline.
Bypasses WebSocket to test Transcribe + Agent + Polly directly.
"""
import json
import base64
import subprocess
import time
import boto3

LAMBDA_NAME = "centli-app-message"
REGION = "us-east-1"

def generate_test_audio():
    """Generate test audio using macOS TTS"""
    print("🎤 Generating test audio with macOS TTS...")
    
    # Generate speech
    subprocess.run(
        ['say', '-v', 'Paulina', '-o', '/tmp/test_voice.aiff',
         'Hola, quién eres tú y qué servicios ofreces?'],
        check=True
    )
    
    # Convert to WebM/Opus (same as browser MediaRecorder)
    result = subprocess.run(
        ['ffmpeg', '-y', '-i', '/tmp/test_voice.aiff',
         '-c:a', 'libopus', '-b:a', '48k', '-ar', '48000', '-ac', '1',
         '/tmp/test_voice.webm'],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"❌ ffmpeg error: {result.stderr}")
        return None
    
    with open('/tmp/test_voice.webm', 'rb') as f:
        audio_bytes = f.read()
    
    audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
    print(f"✅ Audio: {len(audio_bytes)} bytes, base64: {len(audio_b64)} chars")
    return audio_b64


def invoke_lambda(audio_b64):
    """Invoke Lambda directly with audio payload"""
    client = boto3.client('lambda', region_name=REGION)
    
    session_id = f"test-voice-{int(time.time())}"
    
    # Simulate API Gateway WebSocket event
    event = {
        "requestContext": {
            "connectionId": "test-voice-conn",
            "domainName": "vvg621xawg.execute-api.us-east-1.amazonaws.com",
            "stage": "prod"
        },
        "body": json.dumps({
            "action": "sendMessage",
            "data": {
                "user_id": "test-voice-user",
                "session_id": session_id,
                "type": "AUDIO",
                "includeAudio": False,
                "audio": audio_b64
            }
        })
    }
    
    print(f"\n📤 Invoking Lambda '{LAMBDA_NAME}'...")
    print(f"   Session: {session_id}")
    print(f"   Payload size: {len(json.dumps(event))} bytes")
    
    start = time.time()
    response = client.invoke(
        FunctionName=LAMBDA_NAME,
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )
    elapsed = time.time() - start
    
    # Parse response
    status = response['StatusCode']
    payload = json.loads(response['Payload'].read())
    
    print(f"\n📨 Response in {elapsed:.1f}s:")
    print(f"   Status: {status}")
    print(f"   Payload: {json.dumps(payload)}")
    
    # Check if there was a function error
    if 'FunctionError' in response:
        print(f"   ❌ Function Error: {response['FunctionError']}")
    
    return status, payload, elapsed


def check_logs(start_time):
    """Check CloudWatch logs for the invocation"""
    logs = boto3.client('logs', region_name=REGION)
    
    print(f"\n📋 Checking CloudWatch logs...")
    time.sleep(2)  # Wait for logs to appear
    
    response = logs.filter_log_events(
        logGroupName=f"/aws/lambda/{LAMBDA_NAME}",
        startTime=int(start_time * 1000),
        filterPattern="TRANSCRIBE_AUDIO"
    )
    
    for event in response.get('events', []):
        msg = event['message'].strip()
        if any(k in msg for k in ['Transcription:', 'Converting', 'Converted', 'ERROR', 'ffmpeg', 'duration']):
            print(f"   {msg}")


def main():
    print("=" * 60)
    print("🧪 VOICE PIPELINE DIRECT TEST")
    print("=" * 60)
    
    # Step 1: Generate audio
    audio_b64 = generate_test_audio()
    if not audio_b64:
        print("❌ Failed to generate audio")
        return
    
    # Step 2: Invoke Lambda
    start_time = time.time()
    try:
        status, payload, elapsed = invoke_lambda(audio_b64)
    except Exception as e:
        print(f"❌ Lambda invocation failed: {e}")
        return
    
    # Step 3: Check logs
    check_logs(start_time)
    
    # Step 4: Check full logs for transcription result
    print(f"\n📋 Full transcription logs:")
    logs = boto3.client('logs', region_name=REGION)
    time.sleep(3)
    
    response = logs.filter_log_events(
        logGroupName=f"/aws/lambda/{LAMBDA_NAME}",
        startTime=int(start_time * 1000),
        filterPattern="Transcri"
    )
    
    for event in response.get('events', []):
        msg = event['message'].strip()
        print(f"   {msg}")
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
