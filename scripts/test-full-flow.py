#!/usr/bin/env python3
"""
Test completo del flujo frontend → backend
Simula exactamente lo que hace el frontend React
"""
import asyncio
import websockets
import json
import ssl
import time

WS_URL = "wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod"

async def test():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    print("=" * 60)
    print("TEST COMPLETO: Flujo Frontend → Backend")
    print("=" * 60)

    # PASO 1: Conectar
    print("\n[1] Conectando al WebSocket...")
    try:
        ws = await websockets.connect(WS_URL, ssl=ssl_ctx)
        print("    ✅ Conectado")
    except Exception as e:
        print(f"    ❌ Error de conexión: {e}")
        return

    # PASO 2: Enviar mensaje exactamente como el frontend
    session_id = f"session-{int(time.time())}-test123"
    payload = {
        "action": "sendMessage",
        "data": {
            "user_id": "simple-user",
            "session_id": session_id,
            "type": "TEXT",
            "message": "Hola, ¿cómo me afilio a Comfama?"
        }
    }

    print(f"\n[2] Enviando mensaje (formato frontend):")
    print(f"    Payload: {json.dumps(payload, indent=2)}")
    await ws.send(json.dumps(payload))
    print("    ✅ Enviado")

    # PASO 3: Recibir respuesta
    print(f"\n[3] Esperando respuesta...")
    full_response = ""
    chunk_count = 0

    try:
        while True:
            msg = await asyncio.wait_for(ws.recv(), timeout=15.0)
            chunk_count += 1

            # Intentar parsear como JSON
            try:
                data = json.loads(msg)
                print(f"    Chunk {chunk_count} (JSON): {json.dumps(data)[:200]}")
                content = data.get("content", data.get("message", ""))
                full_response += content
            except json.JSONDecodeError:
                # Texto plano (streaming)
                print(f"    Chunk {chunk_count} (text): {msg[:100]}")
                full_response += msg

    except asyncio.TimeoutError:
        pass

    await ws.close()

    # RESULTADO
    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)
    print(f"\nChunks recibidos: {chunk_count}")
    print(f"Longitud respuesta: {len(full_response)} chars")
    print(f"\nRespuesta completa:")
    print("-" * 40)
    print(full_response if full_response else "(vacía)")
    print("-" * 40)

    # Verificar identidad
    lower = full_response.lower()
    forbidden = ["carlos", "méxico", "mexico", "mxn", "centli"]
    found_bad = [w for w in forbidden if w in lower]
    found_good = [w for w in ["comfi", "comfama", "colombia"] if w in lower]

    if found_bad:
        print(f"\n❌ PALABRAS PROHIBIDAS: {found_bad}")
    else:
        print(f"\n✅ Sin palabras prohibidas")

    if found_good:
        print(f"✅ Identidad correcta: {found_good}")
    
    if not full_response:
        print("\n⚠️  RESPUESTA VACÍA - Revisando posibles causas:")
        print("   1. Lambda no procesó el mensaje")
        print("   2. Bedrock Agent no respondió")
        print("   3. Error en el formato del mensaje")
        print("\n   Revisar logs:")
        print("   aws logs tail /aws/lambda/centli-app-message --since 2m")
        print("   aws logs tail /aws/lambda/centli-app-connect --since 2m")

asyncio.run(test())
