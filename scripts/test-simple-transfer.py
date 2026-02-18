import json
import asyncio
import websockets
import ssl

async def test():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    async with websockets.connect("wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev", ssl=ssl_context) as ws:
        payload = {
            "action": "sendMessage",
            "data": {
                "user_id": "simple-user",
                "session_id": f"test-{int(asyncio.get_event_loop().time())}",
                "type": "TEXT",
                "message": "Envía $500 a mi mamá"
            }
        }
        
        await ws.send(json.dumps(payload))
        print("Mensaje enviado, esperando respuesta...")
        
        timeout = 15
        start = asyncio.get_event_loop().time()
        
        while asyncio.get_event_loop().time() - start < timeout:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                print(f"Recibido: {msg[:200]}")
            except asyncio.TimeoutError:
                break

asyncio.run(test())
