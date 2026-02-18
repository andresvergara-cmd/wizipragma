#!/usr/bin/env python3
"""
Test WebSocket with the fixed Lambda
"""

import asyncio
import websockets
import json
from datetime import datetime

WEBSOCKET_URL = "wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"

async def test_chat():
    print("=" * 80)
    print("TESTING FIXED LAMBDA")
    print("=" * 80)
    
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✅ Connected to WebSocket")
        
        # Test message
        message = {
            "action": "sendMessage",
            "data": {
                "user_id": "simple-user",
                "session_id": f"test-session-{int(datetime.now().timestamp())}",
                "message": "¿Cuál es mi saldo?",
                "type": "TEXT"
            }
        }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📤 Sending: {message['data']['message']}")
        await websocket.send(json.dumps(message))
        
        # Collect responses
        responses = []
        chunk_count = 0
        
        try:
            while True:
                response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                chunk_count += 1
                responses.append(response)
                
                # Show first few characters of each chunk
                preview = response[:50] if len(response) > 50 else response
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 📨 Chunk {chunk_count}: {preview}...")
                
        except asyncio.TimeoutError:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ⏱️  No more chunks (timeout)")
        
        print("\n" + "=" * 80)
        print("RESULTS")
        print("=" * 80)
        print(f"Total chunks received: {chunk_count}")
        print(f"\nFull response:")
        print("-" * 80)
        for i, resp in enumerate(responses, 1):
            print(f"Chunk {i}: {resp}")
        print("-" * 80)
        
        # Check if streaming is working correctly
        if chunk_count > 1:
            # Check if chunks are different (not accumulated)
            unique_chunks = len(set(responses))
            if unique_chunks == chunk_count:
                print("\n✅ STREAMING WORKS CORRECTLY: Each chunk is unique (not accumulated)")
            else:
                print("\n⚠️  STREAMING ISSUE: Some chunks are duplicated (might be accumulated)")
        else:
            print("\n⚠️  Only 1 chunk received - streaming might not be working")
        
        # Check if response mentions balance
        full_response = responses[-1] if responses else ""
        if "saldo" in full_response.lower() and ("25" in full_response or "100" in full_response):
            print("✅ USER DATA LOADED: Response includes balance information")
        elif "no tengo información" in full_response.lower():
            print("❌ USER DATA NOT LOADED: Agent says it doesn't have information")
        else:
            print("⚠️  UNCLEAR: Check response manually")

if __name__ == "__main__":
    asyncio.run(test_chat())
