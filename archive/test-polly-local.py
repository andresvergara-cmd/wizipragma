#!/usr/bin/env python3
"""
Test Polly TTS locally to verify it works
"""

import sys
import os

# Add app_message to path
sys.path.insert(0, 'src_aws/app_message')

try:
    from polly_tts import synthesize_speech, get_available_voices
    
    print("✅ polly_tts module imported successfully")
    print()
    
    # Test 1: List available voices
    print("📢 Test 1: Getting available voices for es-MX...")
    voices = get_available_voices('es-MX')
    if voices:
        print(f"✅ Found {len(voices)} voices:")
        for voice in voices:
            print(f"   - {voice['name']} ({voice['gender']})")
    else:
        print("❌ No voices found")
    print()
    
    # Test 2: Synthesize short text
    print("🔊 Test 2: Synthesizing short text...")
    test_text = "Hola, soy Comfi, tu asistente de Comfama."
    
    try:
        result = synthesize_speech(test_text)
        print(f"✅ Synthesis successful!")
        print(f"   - Audio size: {result['size_bytes']} bytes")
        print(f"   - Voice: {result['voice_id']}")
        print(f"   - Sample rate: {result['sample_rate']}")
        print(f"   - Base64 length: {len(result['audio_base64'])} chars")
    except Exception as e:
        print(f"❌ Synthesis failed: {str(e)}")
    
    print()
    print("✅ All tests completed!")
    
except ImportError as e:
    print(f"❌ Failed to import polly_tts: {str(e)}")
    print()
    print("Checking if file exists...")
    if os.path.exists('src_aws/app_message/polly_tts.py'):
        print("✅ File exists: src_aws/app_message/polly_tts.py")
    else:
        print("❌ File NOT found: src_aws/app_message/polly_tts.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
