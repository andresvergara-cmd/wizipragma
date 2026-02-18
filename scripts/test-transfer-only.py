#!/usr/bin/env python3
"""Test transfer only"""

import asyncio
import websockets
import json
import ssl
from datetime import datetime

WS_URL = "wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"
USER_ID = "simple-user"

async def test():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    async with websockets.connect(WS_URL, ssl=ssl_context) as websocket:
        msg = {
            "action": "sendMessage",
            "data": {
                "user_id": USER_ID,
                "session_id": f"test-{datetime.now().timestamp()}",
                "type": "TEXT",
                "message": "Envía $500 a mi mamá"
            }
        }
        print(f"USER: Envía $500 a mi mamá")
        await websocket.send(json.dumps(msg))
        
        response_text = ""
        timeout_count = 0
        
        while timeout_count < 40:  # 40 seconds max
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                chunk = response
                response_text += chunk
                print(chunk, end='', flush=True)
                timeout_count = 0
            except asyncio.TimeoutError:
                timeout_count += 1
                if timeout_count >= 3:
                    break
        
        print("\n\n" + "="*60)
        if "TRF-" in response_text:
            print("✅ SUCCESS - Transaction ID found!")
        else:
            print("❌ FAILED - No transaction ID")
        print("="*60)

asyncio.run(test())
