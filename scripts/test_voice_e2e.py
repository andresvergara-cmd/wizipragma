#!/usr/bin/env python3
"""
End-to-end voice test: sends audio via WebSocket to Lambda,
waits for transcription + agent response + audio response.
"""
import asyncio
import json
import base64
import time
import websockets

WS_URL = "wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod"
AUDIO_B64_FILE = "/tmp/test_audio_b64.txt"

async def test_voice():
    print("=" * 60)
    print("🎤 VOICE E2E TEST")
    print("=" * 60)
    
    # Load audio
    with open(AUDIO_B64_FILE, 'r') as f:
        audio_b64 = f.read().strip()
    print(f"📊 Audio base64 length: {len(audio_b64)} chars")
    
    # Connect
    print(f"\n🔌 Connecting to {WS_URL}...")
    async with websockets.connect(WS_URL) as ws:
        print("✅ Connected")
        
        # Build payload (same as frontend)
        session_id = f"session-test-voice-{int(time.time())}"
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
        print(f"📤 Sending AUDIO payload ({len(payload_json)} bytes)...")
        await ws.send(payload_json)
        print("✅ Sent")
        
        # Wait for responses (timeout 90s)
        print("\n⏳ Waiting for responses...")
        start = time.time()
        responses = []
        
        try:
            while time.time() - start < 90:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    elapsed = time.time() - start
                    
                    try:
                        data = json.loads(msg)
                        msg_type = data.get('msg_type', data.get('type', 'unknown'))
                        print(f"\n📨 [{elapsed:.1f}s] JSON message (msg_type={msg_type}):")
                        
                        if msg_type == 'transcription':
                            print(f"   🎤 Transcription: '{data.get('text', '')}'")
                        elif msg_type == 'agent_response':
                            content = data.get('message', '')[:200]
                            print(f"   🤖 Agent response: '{content}...'")
                        elif msg_type == 'audio_response':
                            audio_len = len(data.get('audio', ''))
                            print(f"   🔊 Audio response: {audio_len} chars base64")
                        elif msg_type == 'audio_chunk':
                            idx = data.get('chunk_index', 0)
                            total = data.get('total_chunks', 0)
                            print(f"   🔊 Audio chunk {idx+1}/{total}")
                        elif data.get('type') == 'ERROR':
                            print(f"   ❌ Error: {data.get('content', '')}")
                        else:
                            print(f"   📋 {json.dumps(data)[:200]}")
                        
                        responses.append(data)
                        
                        # If we got agent_response, we're done with text
                        # Keep waiting for audio chunks
                        if msg_type == 'agent_response':
                            # Wait a bit more for audio
                            continue
                            
                    except json.JSONDecodeError:
                        # Plain text chunk (streaming)
                        print(f"\n📨 [{elapsed:.1f}s] Plain text: '{msg[:100]}...'")
                        if 'Internal server error' in msg:
                            print("   ⚠️ API GW timeout (Lambda still running)")
                        responses.append(msg)
                        
                except asyncio.TimeoutError:
                    # No message in 5s
                    if responses:
                        # We have responses, check if we're done
                        last = responses[-1]
                        if isinstance(last, dict):
                            lt = last.get('msg_type', '')
                            if lt in ('agent_response', 'audio_response') or (lt == 'audio_chunk' and last.get('chunk_index', 0) == last.get('total_chunks', 1) - 1):
                                print(f"\n✅ All responses received in {time.time()-start:.1f}s")
                                break
                    elapsed = time.time() - start
                    print(f"   ⏳ Waiting... ({elapsed:.0f}s)")
                    
        except websockets.exceptions.ConnectionClosed as e:
            print(f"\n🔌 Connection closed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total responses: {len(responses)}")
    
    got_transcription = any(isinstance(r, dict) and r.get('msg_type') == 'transcription' for r in responses)
    got_agent = any(isinstance(r, dict) and r.get('msg_type') == 'agent_response' for r in responses)
    got_audio = any(isinstance(r, dict) and r.get('msg_type') in ('audio_response', 'audio_chunk') for r in responses)
    got_error = any(isinstance(r, dict) and r.get('type') == 'ERROR' for r in responses)
    
    print(f"  Transcription: {'✅' if got_transcription else '❌'}")
    print(f"  Agent response: {'✅' if got_agent else '❌'}")
    print(f"  Audio response: {'✅' if got_audio else '❌'}")
    print(f"  Errors: {'❌ YES' if got_error else '✅ None'}")
    
    if got_transcription:
        for r in responses:
            if isinstance(r, dict) and r.get('msg_type') == 'transcription':
                print(f"\n  Transcribed text: '{r.get('text', '')}'")
    
    if got_agent:
        for r in responses:
            if isinstance(r, dict) and r.get('msg_type') == 'agent_response':
                print(f"\n  Agent said: '{r.get('message', '')[:300]}'")
    
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(test_voice())
