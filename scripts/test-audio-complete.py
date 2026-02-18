#!/usr/bin/env python3
"""
Test completo del flujo de audio en CENTLI
Simula grabación de audio, envío, transcripción y respuesta del agente
"""

import json
import base64
import asyncio
import websockets
import time
import ssl
from datetime import datetime

# Configuración
WEBSOCKET_URL = "wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"
USER_ID = "simple-user"

# Audio de prueba simulado (WebM header + datos mínimos)
# Este es un audio WebM válido pero vacío para pruebas
SAMPLE_AUDIO_BASE64 = """
GkXfo59ChoEBQveBAULygQRC84EIQoKEd2VibUKHgQRChYECGFOAZwH/////////FUmpZpkq17GDD0JATYCGQ2hyb21lV0GGQ2hyb21lFlSua7+uvdeBAXPFh1WVdW5khoVWX1ZQOIOBASPAgQEj44OEbWF0cm9za2EAQoeBAkKFgQIYU4BnAfv///////+BAAAAAAADEUmpZpkq17GDD0JATYCGQ2hyb21lV0GGQ2hyb21lFlSua7+uvdeBAXPFhldvcmtlciBDb250ZXh0hoVWX1ZQOIOBASPAgQEj44OEbWF0cm9za2EAQoeBAkKFgQIYU4BnAfv///////+BAAAAAAADEUmpZpkq17GDD0JATYCGQ2hyb21lV0GGQ2hyb21lFlSua7+uvdeBAXPFhldvcmtlciBDb250ZXh0hoVWX1ZQOIOBASPAgQEj44OEbWF0cm9za2EA
""".strip().replace('\n', '')

class AudioTester:
    def __init__(self):
        self.ws = None
        self.session_id = f"test-session-{int(time.time())}"
        self.messages_received = []
        self.test_results = {
            "connection": False,
            "audio_sent": False,
            "transcription_received": False,
            "agent_response": False,
            "streaming_works": False,
            "response_time": 0
        }
        
    async def connect(self):
        """Conectar al WebSocket"""
        print(f"\n{'='*60}")
        print(f"🔌 PRUEBA 1: Conexión WebSocket")
        print(f"{'='*60}")
        print(f"URL: {WEBSOCKET_URL}")
        
        try:
            # Create SSL context that doesn't verify certificates (for testing)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            self.ws = await websockets.connect(WEBSOCKET_URL, ssl=ssl_context)
            self.test_results["connection"] = True
            print("✅ Conexión establecida exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error conectando: {e}")
            return False
    
    async def send_audio_message(self):
        """Enviar mensaje de audio simulado"""
        print(f"\n{'='*60}")
        print(f"🎤 PRUEBA 2: Envío de mensaje de audio")
        print(f"{'='*60}")
        
        payload = {
            "action": "sendMessage",
            "data": {
                "user_id": USER_ID,
                "session_id": self.session_id,
                "type": "AUDIO",
                "audio": SAMPLE_AUDIO_BASE64
            }
        }
        
        print(f"📤 Enviando audio...")
        print(f"   - User ID: {USER_ID}")
        print(f"   - Session ID: {self.session_id}")
        print(f"   - Type: AUDIO")
        print(f"   - Audio length: {len(SAMPLE_AUDIO_BASE64)} chars")
        
        try:
            await self.ws.send(json.dumps(payload))
            self.test_results["audio_sent"] = True
            print("✅ Audio enviado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error enviando audio: {e}")
            return False
    
    async def receive_messages(self, timeout=15):
        """Recibir y procesar mensajes del servidor"""
        print(f"\n{'='*60}")
        print(f"📨 PRUEBA 3: Recepción de respuestas")
        print(f"{'='*60}")
        print(f"⏳ Esperando respuestas (timeout: {timeout}s)...\n")
        
        start_time = time.time()
        stream_chunks = []
        
        try:
            while True:
                # Check timeout
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    print(f"\n⏱️  Timeout alcanzado ({timeout}s)")
                    break
                
                try:
                    # Receive with timeout
                    message = await asyncio.wait_for(
                        self.ws.recv(), 
                        timeout=2.0
                    )
                    
                    self.messages_received.append(message)
                    
                    # Try to parse as JSON
                    try:
                        data = json.loads(message)
                        msg_type = data.get('msg_type', 'unknown')
                        
                        print(f"📬 Mensaje recibido: {msg_type}")
                        
                        if msg_type == 'stream_start':
                            print("   🌊 Inicio de streaming")
                            self.test_results["streaming_works"] = True
                            
                        elif msg_type == 'stream_chunk':
                            chunk = data.get('message', '')
                            stream_chunks.append(chunk)
                            print(f"   📦 Chunk: {chunk[:50]}...")
                            
                        elif msg_type == 'stream_end':
                            final_message = data.get('message', '')
                            if not final_message and stream_chunks:
                                final_message = ''.join(stream_chunks)
                            
                            print(f"   🏁 Fin de streaming")
                            print(f"   📝 Mensaje completo: {final_message[:100]}...")
                            
                            self.test_results["agent_response"] = True
                            self.test_results["response_time"] = time.time() - start_time
                            
                            # Check if it's a real response (not error)
                            if len(final_message) > 20 and "error" not in final_message.lower():
                                self.test_results["transcription_received"] = True
                            
                            break
                            
                        elif msg_type == 'agent_response':
                            response = data.get('message', '')
                            print(f"   🤖 Respuesta del agente: {response[:100]}...")
                            self.test_results["agent_response"] = True
                            self.test_results["response_time"] = time.time() - start_time
                            break
                            
                        elif msg_type == 'error':
                            error_msg = data.get('message', 'Unknown error')
                            print(f"   ❌ Error del servidor: {error_msg}")
                            
                    except json.JSONDecodeError:
                        # Plain text chunk (old streaming format)
                        print(f"   📦 Chunk (texto plano): {message[:50]}...")
                        stream_chunks.append(message)
                        self.test_results["streaming_works"] = True
                        
                except asyncio.TimeoutError:
                    # No more messages
                    if stream_chunks:
                        # Finalize stream
                        final_message = ''.join(stream_chunks)
                        print(f"\n   🏁 Stream finalizado (timeout)")
                        print(f"   📝 Mensaje completo: {final_message[:100]}...")
                        self.test_results["agent_response"] = True
                        self.test_results["response_time"] = time.time() - start_time
                    break
                    
        except Exception as e:
            print(f"\n❌ Error recibiendo mensajes: {e}")
        
        return len(self.messages_received) > 0
    
    async def send_text_message(self, text):
        """Enviar mensaje de texto para comparación"""
        print(f"\n{'='*60}")
        print(f"💬 PRUEBA 4: Mensaje de texto (comparación)")
        print(f"{'='*60}")
        
        payload = {
            "action": "sendMessage",
            "data": {
                "user_id": USER_ID,
                "session_id": self.session_id,
                "type": "TEXT",
                "message": text
            }
        }
        
        print(f"📤 Enviando: '{text}'")
        
        try:
            await self.ws.send(json.dumps(payload))
            print("✅ Mensaje enviado")
            
            # Wait for response
            print("⏳ Esperando respuesta...")
            start_time = time.time()
            
            while time.time() - start_time < 10:
                try:
                    message = await asyncio.wait_for(self.ws.recv(), timeout=2.0)
                    try:
                        data = json.loads(message)
                        if data.get('msg_type') in ['stream_end', 'agent_response']:
                            response = data.get('message', '')
                            print(f"✅ Respuesta recibida: {response[:100]}...")
                            return True
                    except:
                        pass
                except asyncio.TimeoutError:
                    continue
                    
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return False
    
    async def close(self):
        """Cerrar conexión"""
        if self.ws:
            await self.ws.close()
    
    def print_summary(self):
        """Imprimir resumen de resultados"""
        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE PRUEBAS")
        print(f"{'='*60}\n")
        
        tests = [
            ("Conexión WebSocket", self.test_results["connection"]),
            ("Envío de audio", self.test_results["audio_sent"]),
            ("Transcripción procesada", self.test_results["transcription_received"]),
            ("Respuesta del agente", self.test_results["agent_response"]),
            ("Streaming funcional", self.test_results["streaming_works"])
        ]
        
        passed = sum(1 for _, result in tests if result)
        total = len(tests)
        
        for test_name, result in tests:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        if self.test_results["response_time"] > 0:
            print(f"\n⏱️  Tiempo de respuesta: {self.test_results['response_time']:.2f}s")
        
        print(f"\n📈 Resultado: {passed}/{total} pruebas exitosas")
        
        if passed == total:
            print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
            print("✅ El sistema de audio está funcionando correctamente")
        else:
            print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
            print("❌ Revisar logs de Lambda y frontend para más detalles")
        
        print(f"\n{'='*60}\n")
        
        return passed == total

async def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "="*60)
    print("🎯 PRUEBA COMPLETA DEL SISTEMA DE AUDIO - CENTLI")
    print("="*60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Usuario de prueba: {USER_ID}")
    
    tester = AudioTester()
    
    try:
        # Test 1: Connect
        if not await tester.connect():
            print("\n❌ No se pudo conectar. Abortando pruebas.")
            return False
        
        await asyncio.sleep(1)
        
        # Test 2: Send audio
        if not await tester.send_audio_message():
            print("\n❌ No se pudo enviar audio. Abortando pruebas.")
            return False
        
        # Test 3: Receive responses
        await tester.receive_messages(timeout=15)
        
        await asyncio.sleep(2)
        
        # Test 4: Send text for comparison
        await tester.send_text_message("¿Cuál es mi saldo actual?")
        
        await asyncio.sleep(2)
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await tester.close()
    
    # Print summary
    success = tester.print_summary()
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
