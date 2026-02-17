#!/usr/bin/env python3
"""
Test WebSocket Connection for CENTLI
Tests text and audio message sending
"""

import asyncio
import websockets
import json
import time
import base64
import ssl

WS_URL = "wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"

async def test_connection():
    print("🔌 Conectando a WebSocket...")
    print(f"URL: {WS_URL}")
    
    # Create SSL context that doesn't verify certificates (for testing)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        async with websockets.connect(WS_URL, ssl=ssl_context) as websocket:
            print("✅ WebSocket conectado exitosamente")
            
            # Generate session ID
            session_id = f"session-{int(time.time())}-test"
            print(f"🆔 Session ID: {session_id}")
            
            # Test 1: Send text message
            print("\n📝 TEST 1: Enviando mensaje de texto...")
            text_payload = {
                "action": "sendMessage",
                "data": {
                    "user_id": "test-user-001",
                    "session_id": session_id,
                    "message": "Hola, ¿cuál es mi saldo?",
                    "type": "TEXT"
                }
            }
            
            await websocket.send(json.dumps(text_payload))
            print("📤 Mensaje de texto enviado")
            
            # Wait for response
            print("⏳ Esperando respuesta...")
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                print(f"📨 Respuesta recibida: {response}")
                
                # Parse response
                try:
                    data = json.loads(response)
                    print(f"📦 Tipo de mensaje: {data.get('msg_type', 'unknown')}")
                    if 'message' in data:
                        print(f"💬 Contenido: {data['message']}")
                except json.JSONDecodeError:
                    print("⚠️ Respuesta no es JSON válido")
                    
            except asyncio.TimeoutError:
                print("❌ Timeout esperando respuesta (10s)")
            
            # Test 2: Send audio message (simulated)
            print("\n🎤 TEST 2: Enviando mensaje de audio simulado...")
            
            # Create a small dummy audio data (base64)
            dummy_audio = base64.b64encode(b"dummy audio data").decode('utf-8')
            
            audio_payload = {
                "action": "sendMessage",
                "data": {
                    "user_id": "test-user-001",
                    "session_id": session_id,
                    "message": dummy_audio,
                    "type": "VOICE"
                }
            }
            
            await websocket.send(json.dumps(audio_payload))
            print("📤 Mensaje de audio enviado")
            
            # Wait for response
            print("⏳ Esperando respuesta...")
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                print(f"📨 Respuesta recibida: {response}")
                
                # Parse response
                try:
                    data = json.loads(response)
                    print(f"📦 Tipo de mensaje: {data.get('msg_type', 'unknown')}")
                    if 'message' in data:
                        print(f"💬 Contenido: {data['message']}")
                except json.JSONDecodeError:
                    print("⚠️ Respuesta no es JSON válido")
                    
            except asyncio.TimeoutError:
                print("❌ Timeout esperando respuesta (10s)")
            
            print("\n✅ Tests completados")
            
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ Error de WebSocket: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 CENTLI - Test de WebSocket")
    print("=" * 50)
    asyncio.run(test_connection())
