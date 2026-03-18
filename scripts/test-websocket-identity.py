#!/usr/bin/env python3
"""
Test WebSocket connection and verify agent identity
"""
import asyncio
import websockets
import json
import ssl
from datetime import datetime

# Configuración
WEBSOCKET_URL = "wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod"
USER_ID = "test-user-comfi"

async def test_identity():
    """Test agent identity response"""
    
    # Disable SSL verification for testing
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    print("=" * 60)
    print("TEST: Identidad del Agente")
    print("=" * 60)
    print(f"\nWebSocket: {WEBSOCKET_URL}")
    print(f"User ID: {USER_ID}")
    print(f"Timestamp: {datetime.now().isoformat()}\n")
    
    try:
        async with websockets.connect(WEBSOCKET_URL, ssl=ssl_context) as ws:
            print("✅ Conectado al WebSocket\n")
            
            # Test 1: Pregunta sobre afiliación
            print("TEST 1: ¿Cómo me afilio a Comfama?")
            print("-" * 60)
            
            message = {
                "action": "sendMessage",
                "userId": USER_ID,
                "type": "TEXT",
                "content": "¿Cómo me afilio a Comfama?"
            }
            
            await ws.send(json.dumps(message))
            print("📤 Mensaje enviado\n")
            
            print("📥 Respuesta del agente:")
            print("-" * 60)
            
            response_text = ""
            forbidden_words = ["carlos", "méxico", "mexico", "mxn", "centli"]
            violations = []
            
            try:
                while True:
                    response = await asyncio.wait_for(ws.recv(), timeout=10.0)
                    data = json.loads(response)
                    
                    if data.get("type") == "TEXT":
                        chunk = data.get("content", "")
                        response_text += chunk
                        print(chunk, end="", flush=True)
                        
                        # Check for forbidden words
                        chunk_lower = chunk.lower()
                        for word in forbidden_words:
                            if word in chunk_lower:
                                violations.append(word)
                    
                    elif data.get("type") == "ERROR":
                        print(f"\n❌ Error: {data.get('content')}")
                        break
                        
            except asyncio.TimeoutError:
                print("\n\n⏱️  Timeout - respuesta completa")
            
            print("\n" + "=" * 60)
            print("RESULTADO DEL TEST")
            print("=" * 60)
            
            if violations:
                print(f"\n❌ FALLO: Se detectaron palabras prohibidas:")
                for word in set(violations):
                    print(f"   - {word}")
                print(f"\nRespuesta completa:\n{response_text}")
            else:
                print("\n✅ ÉXITO: No se detectaron palabras prohibidas")
                print(f"\nLongitud de respuesta: {len(response_text)} caracteres")
                
                # Check for correct identity
                correct_words = ["comfi", "comfama", "colombia"]
                found_correct = [w for w in correct_words if w in response_text.lower()]
                
                if found_correct:
                    print(f"✅ Identidad correcta detectada: {', '.join(found_correct)}")
                else:
                    print("⚠️  Advertencia: No se detectó identidad de Comfi/Comfama")
            
            print("\n" + "=" * 60)
            
    except Exception as e:
        print(f"\n❌ Error de conexión: {str(e)}")
        print("\nPosibles causas:")
        print("1. El WebSocket no está activo")
        print("2. La Lambda no tiene permisos")
        print("3. El Bedrock Agent no está configurado")
        print("\nVerificar logs:")
        print("  aws logs tail /aws/lambda/centli-app-message --follow")

if __name__ == "__main__":
    asyncio.run(test_identity())
