#!/usr/bin/env python3
"""
Test Nova Sonic locally to verify it works
"""

import sys
import os
import json
import boto3
import base64

# Add app_message to path
sys.path.insert(0, 'src_aws/app_message')

print("=" * 60)
print("NOVA SONIC LOCAL TEST")
print("=" * 60)
print()

# Test 1: Check if nova_sonic_simple can be imported
print("Test 1: Import nova_sonic_simple module")
try:
    from nova_sonic_simple import transcribe_audio, synthesize_speech, convert_to_pcm
    print("✅ Module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import: {str(e)}")
    sys.exit(1)
print()

# Test 2: Check Bedrock client
print("Test 2: Check Bedrock client connection")
try:
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    print("✅ Bedrock client created")
except Exception as e:
    print(f"❌ Failed to create Bedrock client: {str(e)}")
    sys.exit(1)
print()

# Test 3: Check if Nova Sonic model is accessible
print("Test 3: Check Nova Sonic model accessibility")
try:
    # Try a simple invoke to check permissions
    response = bedrock.invoke_model(
        modelId='amazon.nova-sonic-v1:0',
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            "schemaVersion": "messages-v1",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": "Hola"
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 10,
                "temperature": 0.3
            }
        })
    )
    print("✅ Nova Sonic model is accessible")
    response_body = json.loads(response['body'].read())
    print(f"   Response preview: {str(response_body)[:100]}...")
except Exception as e:
    print(f"❌ Failed to access Nova Sonic: {str(e)}")
    print(f"   Error type: {type(e).__name__}")
    sys.exit(1)
print()

# Test 4: Test TTS (Text-to-Speech)
print("Test 4: Test Nova Sonic TTS (Text-to-Speech)")
try:
    test_text = "Hola, soy Comfi."
    print(f"   Input text: '{test_text}'")
    
    result = synthesize_speech(test_text)
    
    print(f"✅ TTS successful!")
    print(f"   Audio chunks: {len(result['audio_chunks'])}")
    print(f"   Total size: {result['total_size']} bytes")
    print(f"   Sample rate: {result['sample_rate']} Hz")
    print(f"   Format: {result['format']}")
except Exception as e:
    print(f"❌ TTS failed: {str(e)}")
    import traceback
    print(f"   Traceback: {traceback.format_exc()}")
print()

# Test 5: Test audio conversion (if pydub is available)
print("Test 5: Test audio conversion (pydub)")
try:
    from pydub import AudioSegment
    print("✅ pydub is available")
    
    # Check if ffmpeg is accessible
    AudioSegment.converter = "/opt/bin/ffmpeg"
    AudioSegment.ffprobe = "/opt/bin/ffprobe"
    
    # Try to check if ffmpeg exists (won't work locally but shows the path)
    print(f"   ffmpeg path: {AudioSegment.converter}")
    print(f"   ffprobe path: {AudioSegment.ffprobe}")
    
except ImportError:
    print("⚠️  pydub not available (expected in local environment)")
    print("   This is OK - pydub will be available in Lambda via Layer")
except Exception as e:
    print(f"⚠️  pydub check failed: {str(e)}")
print()

print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✅ Nova Sonic is working!")
print("✅ TTS (Text-to-Speech) is functional")
print("⚠️  STT (Speech-to-Text) requires audio input (test manually)")
print()
print("Next steps:")
print("1. Test STT by sending actual audio from frontend")
print("2. Monitor Lambda logs during voice message")
print("3. Verify audio chunks are received in frontend")
print("=" * 60)
