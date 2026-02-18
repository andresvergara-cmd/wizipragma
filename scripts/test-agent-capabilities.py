#!/usr/bin/env python3
"""
Test de capacidades del agente CENTLI
Prueba transferencias y compras
"""

import json
import asyncio
import websockets
import ssl

WEBSOCKET_URL = "wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"
USER_ID = "simple-user"

async def test_agent():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    async with websockets.connect(WEBSOCKET_URL, ssl=ssl_context) as ws:
        session_id = f"test-{int(asyncio.get_event_loop().time())}"
        
        # Test 1: Transferencia
        print("\n" + "="*60)
        print("TEST 1: Solicitar transferencia a mamá")
        print("="*60)
        
        payload = {
            "action": "sendMessage",
            "data": {
                "user_id": USER_ID,
                "session_id": session_id,
                "type": "TEXT",
                "message": "Quiero hacer una transferencia de $500 MXN a mi mamá"
            }
        }
        
        await ws.send(json.dumps(payload))
        print("📤 Mensaje enviado")
        
        # Recibir respuesta
        response_text = ""
        timeout = 10
        start = asyncio.get_event_loop().time()
        
        while asyncio.get_event_loop().time() - start < timeout:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                try:
                    data = json.loads(msg)
                    if data.get('msg_type') == 'stream_chunk':
                        response_text += data.get('message', '')
                    elif data.get('msg_type') == 'stream_end':
                        final = data.get('message', '')
                        if final:
                            response_text = final
                        break
                except:
                    response_text += msg
            except asyncio.TimeoutError:
                if response_text:
                    break
        
        print(f"\n📨 Respuesta del agente:")
        print(response_text)
        
        # Test 2: Compra de producto
        await asyncio.sleep(2)
        
        print("\n" + "="*60)
        print("TEST 2: Comprar un producto")
        print("="*60)
        
        payload = {
            "action": "sendMessage",
            "data": {
                "user_id": USER_ID,
                "session_id": session_id,
                "type": "TEXT",
                "message": "Quiero comprar un iPhone 15 Pro"
            }
        }
        
        await ws.send(json.dumps(payload))
        print("📤 Mensaje enviado")
        
        # Recibir respuesta
        response_text = ""
        start = asyncio.get_event_loop().time()
        
        while asyncio.get_event_loop().time() - start < timeout:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                try:
                    data = json.loads(msg)
                    if data.get('msg_type') == 'stream_chunk':
                        response_text += data.get('message', '')
                    elif data.get('msg_type') == 'stream_end':
                        final = data.get('message', '')
                        if final:
                            response_text = final
                        break
                except:
                    response_text += msg
            except asyncio.TimeoutError:
                if response_text:
                    break
        
        print(f"\n📨 Respuesta del agente:")
        print(response_text)
        
        print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(test_agent())
