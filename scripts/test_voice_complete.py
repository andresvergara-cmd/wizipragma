#!/usr/bin/env python3
"""
Complete voice pipeline test:
1. Generate test audio with macOS TTS
2. Connect to WebSocket (creates session)
3. Send audio message
4. Wait for transcription + agent response + audio response
5. Check CloudWatch logs for details
"""
import asyncio
import json
import base64
import time
import subprocess
import ssl
import sys

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

import websockets

WS_URL = "wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod"


def generate_test_audio_webm(text="Hola, buenos días. Me gustaría saber cuáles son los servicios que ofrece Comfama."):
    """Generate test audio as WebM/Opus (same as browser MediaRecorder)"""
    print(f"🎤 Generating WebM/Opus audio: '{text}'")
    
    subprocess.run(
        ['say', '-v', 'Paulina', '-o', '/tmp/test_voice.aiff', text],
        check=True
    )
    
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
    print(f"✅ WebM audio: {len(audio_bytes)} bytes, base64: {len(audio_b64)} chars")
    return audio_b64


def generate_test_audio_wav(text="Hola, buenos días. Me gustaría saber cuáles son los servicios que ofrece Comfama."):
    """Generate test audio as WAV 16kHz mono (skip Lambda conversion)"""
    print(f"🎤 Generating WAV audio: '{text}'")
    
    subprocess.run(
        ['say', '-v', 'Paulina', '-o', '/tmp/test_voice.aiff', text],
        check=True
    )
    
    result = subprocess.run(
        ['ffmpeg', '-y', '-i', '/tmp/test_voice.aiff',
         '-ar', '16000', '-ac', '1', '-sample_fmt', 's16',
         '-f', 'wav', '/tmp/test_voice.wav'],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"❌ ffmpeg error: {result.stderr}")
        return None
    
    with open('/tmp/test_voice.wav', 'rb') as f:
        audio_bytes = f.read()
    
    audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
    print(f"✅ WAV audio: {len(audio_bytes)} bytes, base64: {len(audio_b64)} chars")
    return audio_b64


async def test_voice_pipeline(audio_b64, label=""):
    """Send audio via WebSocket and wait for responses"""
    print(f"\n{'='*60}")
    print(f"🔌 TEST: {label}")
    print(f"{'='*60}")
    print(f"Connecting to {WS_URL}...")
    
    async with websockets.connect(WS_URL, ssl=SSL_CONTEXT) as ws:
        print("✅ Connected")
        await asyncio.sleep(1)  # Wait for $connect to create session
        
        session_id = f"session-test-{int(time.time())}"
        payload = {
            "action": "sendMessage",
            "data": {
                "user_id": "test-voice-user",
                "session_id": session_id,
                "type": "AUDIO",
                "includeAudio": False,
                "audio": audio_b64
            }
        }
        
        payload_json = json.dumps(payload)
        print(f"📤 Sending AUDIO ({len(payload_json)} bytes)...")
        await ws.send(payload_json)
        print("✅ Sent")
        
        print("⏳ Waiting for responses...")
        start = time.time()
        responses = []
        got_final = False
        
        try:
            while time.time() - start < 90:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=10.0)
                    elapsed = time.time() - start
                    
                    try:
                        data = json.loads(msg)
                        msg_type = data.get('msg_type', data.get('type', 'unknown'))
                        
                        if msg_type == 'transcription':
                            text = data.get('text', '')
                            print(f"  [{elapsed:.1f}s] 🎤 TRANSCRIPTION: '{text}'")
                            responses.append(('transcription', text))
                            
                        elif msg_type == 'agent_response':
                            content = data.get('message', '')
                            print(f"  [{elapsed:.1f}s] 🤖 AGENT: {content[:300]}")
                            responses.append(('agent_response', content))
                            got_final = True
                            
                        elif msg_type == 'audio_response':
                            audio_len = len(data.get('audio', ''))
                            print(f"  [{elapsed:.1f}s] 🔊 AUDIO: {audio_len} chars")
                            responses.append(('audio_response', audio_len))
                            got_final = True
                            
                        elif msg_type == 'audio_chunk':
                            idx = data.get('chunk_index', 0)
                            total = data.get('total_chunks', 0)
                            print(f"  [{elapsed:.1f}s] 🔊 CHUNK {idx+1}/{total}")
                            responses.append(('audio_chunk', f"{idx+1}/{total}"))
                            if idx == total - 1:
                                got_final = True
                            
                        elif data.get('type') == 'ERROR':
                            print(f"  [{elapsed:.1f}s] ❌ ERROR: {data.get('content', '')}")
                            responses.append(('error', data.get('content', '')))
                            got_final = True
                            
                        else:
                            content = data.get('message', json.dumps(data)[:200])
                            print(f"  [{elapsed:.1f}s] 📋 {msg_type}: {str(content)[:200]}")
                            responses.append(('other', str(content)[:100]))
                        
                    except json.JSONDecodeError:
                        if 'Internal server error' in msg:
                            print(f"  [{elapsed:.1f}s] ⚠️ API GW timeout (Lambda continues)")
                        elif 'Endpoint request timed out' in msg:
                            print(f"  [{elapsed:.1f}s] ⚠️ API GW endpoint timeout (Lambda continues)")
                        else:
                            print(f"  [{elapsed:.1f}s] 📝 TEXT: '{msg[:100]}'")
                        responses.append(('text', msg[:100]))
                        
                except asyncio.TimeoutError:
                    elapsed = time.time() - start
                    if got_final:
                        # Wait 3 more seconds for any trailing messages
                        try:
                            msg = await asyncio.wait_for(ws.recv(), timeout=3.0)
                            # Process it
                            try:
                                data = json.loads(msg)
                                msg_type = data.get('msg_type', '')
                                if msg_type == 'audio_response':
                                    print(f"  [{time.time()-start:.1f}s] 🔊 AUDIO (late): {len(data.get('audio',''))} chars")
                                    responses.append(('audio_response', len(data.get('audio', ''))))
                            except:
                                pass
                        except asyncio.TimeoutError:
                            pass
                        break
                    print(f"  ⏳ Waiting... ({elapsed:.0f}s)")
                    
        except websockets.exceptions.ConnectionClosed as e:
            print(f"  🔌 Connection closed: {e}")
    
    return responses


def print_summary(responses):
    """Print test results"""
    got_transcription = any(r[0] == 'transcription' for r in responses)
    got_agent = any(r[0] == 'agent_response' for r in responses)
    got_audio = any(r[0] in ('audio_response', 'audio_chunk') for r in responses)
    got_error = any(r[0] == 'error' for r in responses)
    
    print(f"\n  Transcription: {'✅' if got_transcription else '❌'}")
    print(f"  Agent response: {'✅' if got_agent else '❌'}")
    print(f"  Audio response: {'✅' if got_audio else '❌'}")
    print(f"  Errors: {'❌ YES' if got_error else '✅ None'}")
    
    # Check if transcription was meaningful
    for r in responses:
        if r[0] == 'transcription':
            print(f"  Transcribed: '{r[1]}'")
    for r in responses:
        if r[0] == 'agent_response':
            is_error_msg = 'no pude entender' in r[1].lower() or 'intenta de nuevo' in r[1].lower()
            if is_error_msg:
                print(f"  ⚠️ Agent returned error message (STT failed)")
            else:
                print(f"  Agent: '{r[1][:200]}'")
    
    success = got_transcription and got_agent and not got_error
    # Also check if agent response was not an error message
    for r in responses:
        if r[0] == 'agent_response':
            if 'no pude entender' in r[1].lower():
                success = False
    
    return success


def check_cloudwatch_logs(start_time):
    """Try to check CloudWatch logs (may fail if no credentials)"""
    try:
        import boto3
        logs = boto3.client('logs', region_name='us-east-1')
        
        print("\n📋 CloudWatch Logs:")
        time.sleep(3)
        
        response = logs.filter_log_events(
            logGroupName='/aws/lambda/centli-app-message',
            startTime=int(start_time * 1000),
            filterPattern='Transcri'
        )
        
        for event in response.get('events', []):
            msg = event['message'].strip()
            if msg and any(k in msg for k in ['Transcri', 'Convert', 'ffmpeg', 'duration', 'WAV', 'ERROR', 'empty', 'short']):
                print(f"  {msg[:200]}")
                
    except Exception as e:
        print(f"\n⚠️ Could not read CloudWatch logs: {str(e)[:100]}")


async def main():
    print("=" * 60)
    print("🧪 VOICE PIPELINE E2E TEST")
    print("=" * 60)
    
    mode = sys.argv[1] if len(sys.argv) > 1 else 'webm'
    text = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "Hola, buenos días. Me gustaría saber cuáles son los servicios que ofrece Comfama para los afiliados."
    
    start_time = time.time()
    
    if mode == 'wav':
        audio_b64 = generate_test_audio_wav(text)
        label = "WAV 16kHz mono (skip Lambda conversion)"
    else:
        audio_b64 = generate_test_audio_webm(text)
        label = "WebM/Opus (same as browser)"
    
    if not audio_b64:
        print("❌ Failed to generate audio")
        return
    
    responses = await test_voice_pipeline(audio_b64, label)
    
    print(f"\n{'='*60}")
    print("📊 RESULTS")
    print(f"{'='*60}")
    success = print_summary(responses)
    
    check_cloudwatch_logs(start_time)
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 TEST PASSED")
    else:
        print("❌ TEST FAILED")
    print(f"{'='*60}")


if __name__ == '__main__':
    print("Usage: python3 test_voice_complete.py [webm|wav] [custom text]")
    print()
    asyncio.run(main())
