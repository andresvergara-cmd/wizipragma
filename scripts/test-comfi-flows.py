#!/usr/bin/env python3
"""
Test de flujos de usuario para Comfi - Simulación de usuario Comfama
Conecta al WebSocket y ejecuta diferentes flujos de prueba
"""
import json
import time
import ssl
import uuid
import websocket

WS_URL = "wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod"

def send_message(ws, message):
    """Envía un mensaje de texto al WebSocket"""
    payload = json.dumps({
        "action": "sendMessage",
        "data": {
            "type": "TEXT",
            "message": message
        }
    })
    ws.send(payload)

def receive_response(ws, timeout=15):
    """Recibe la respuesta completa del WebSocket"""
    ws.settimeout(timeout)
    full_response = ""
    chunks = 0
    try:
        while True:
            try:
                data = ws.recv()
                chunks += 1
                try:
                    parsed = json.loads(data)
                    if 'content' in parsed:
                        full_response += parsed['content']
                    elif 'message' in parsed:
                        full_response += parsed['message']
                except json.JSONDecodeError:
                    full_response += data
            except websocket.WebSocketTimeoutException:
                break
    except Exception as e:
        pass
    return full_response.strip(), chunks

def run_test(ws, test_name, question, expected_keywords=None):
    """Ejecuta un test individual"""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print(f"📤 Pregunta: {question}")
    print(f"{'='*60}")
    
    send_message(ws, question)
    response, chunks = receive_response(ws)
    
    print(f"📥 Respuesta ({len(response)} chars, {chunks} chunks):")
    print(f"   {response[:300]}{'...' if len(response) > 300 else ''}")
    
    # Validaciones
    result = "✅"
    issues = []
    
    if not response:
        result = "❌"
        issues.append("Sin respuesta del agente")
    elif len(response) < 20:
        result = "⚠️"
        issues.append(f"Respuesta muy corta ({len(response)} chars)")
    
    if expected_keywords:
        missing = [kw for kw in expected_keywords if kw.lower() not in response.lower()]
        if missing:
            result = "⚠️" if result == "✅" else result
            issues.append(f"Palabras clave faltantes: {missing}")
    
    # Verificar identidad
    if 'carlos' in response.lower() or 'méxico' in response.lower() or 'mxn' in response.lower():
        result = "❌"
        issues.append("IDENTIDAD INCORRECTA: Menciona Carlos/México/MXN")
    
    print(f"\n   Resultado: {result}")
    if issues:
        for issue in issues:
            print(f"   ⚠️ {issue}")
    
    return {
        "test": test_name,
        "question": question,
        "response": response,
        "response_length": len(response),
        "chunks": chunks,
        "result": result,
        "issues": issues
    }

def main():
    print("🚀 Iniciando pruebas de flujos de usuario Comfi")
    print(f"🔗 Conectando a: {WS_URL}")
    
    ws = websocket.create_connection(
        WS_URL,
        sslopt={"cert_reqs": ssl.CERT_NONE}
    )
    
    # Esperar conexión
    time.sleep(2)
    try:
        init_data = ws.recv()
        print(f"✅ Conectado. Session: {init_data[:100]}")
    except:
        print("✅ Conectado al WebSocket")
    
    results = []
    
    # ========== FLUJO 1: AFILIACIÓN ==========
    results.append(run_test(
        ws, "Afiliación",
        "¿Cómo me afilio a Comfama?",
        ["comfama", "afilia"]
    ))
    time.sleep(3)
    
    # ========== FLUJO 2: TARIFAS ==========
    results.append(run_test(
        ws, "Tarifas",
        "¿Cuál es mi tarifa de afiliación?",
        ["tarifa", "4%"]
    ))
    time.sleep(3)
    
    # ========== FLUJO 3: TIPOS DE CRÉDITO ==========
    results.append(run_test(
        ws, "Tipos de Crédito",
        "¿Qué tipos de créditos ofrece Comfama?",
        ["crédito"]
    ))
    time.sleep(3)
    
    # ========== FLUJO 4: REQUISITOS CRÉDITO ==========
    results.append(run_test(
        ws, "Requisitos Crédito",
        "¿Qué requisitos necesito para solicitar un crédito?",
        ["requisito"]
    ))
    time.sleep(3)
    
    # ========== FLUJO 5: SUBSIDIOS ==========
    results.append(run_test(
        ws, "Subsidios",
        "¿Qué subsidios ofrece Comfama?",
        ["subsidio"]
    ))
    time.sleep(3)
    
    # ========== FLUJO 6: AYUDA GENERAL ==========
    results.append(run_test(
        ws, "Ayuda General",
        "¿Cómo puedo usar Comfi?",
        ["comfi"]
    ))
    time.sleep(3)
    
    # ========== FLUJO 7: PREGUNTA FUERA DE DOMINIO ==========
    results.append(run_test(
        ws, "Fuera de Dominio",
        "¿Cuál es el clima hoy en Medellín?",
        []
    ))
    time.sleep(3)
    
    # ========== FLUJO 8: CONVERSACIÓN CONTINUA ==========
    results.append(run_test(
        ws, "Seguimiento",
        "¿Y cuánto cuesta la afiliación?",
        []
    ))
    time.sleep(3)

    # ========== FLUJO 9: SERVICIOS RECREACIÓN ==========
    results.append(run_test(
        ws, "Recreación",
        "¿Qué servicios de recreación ofrece Comfama?",
        ["comfama"]
    ))
    time.sleep(3)

    # ========== FLUJO 10: EDUCACIÓN ==========
    results.append(run_test(
        ws, "Educación",
        "¿Comfama ofrece programas de educación?",
        ["comfama"]
    ))
    
    ws.close()
    
    # ========== REPORTE ==========
    print("\n\n" + "="*60)
    print("📊 REPORTE DE PRUEBAS - COMFI (Usuario Comfama)")
    print("="*60)
    
    passed = sum(1 for r in results if r["result"] == "✅")
    warnings = sum(1 for r in results if r["result"] == "⚠️")
    failed = sum(1 for r in results if r["result"] == "❌")
    
    print(f"\n📈 Resumen: {passed} ✅ | {warnings} ⚠️ | {failed} ❌ | Total: {len(results)}")
    
    print("\n📋 Detalle por flujo:")
    for r in results:
        print(f"   {r['result']} {r['test']}: {r['response_length']} chars, {r['chunks']} chunks")
        if r['issues']:
            for issue in r['issues']:
                print(f"      ⚠️ {issue}")
    
    # Guardar reporte
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": {
            "total": len(results),
            "passed": passed,
            "warnings": warnings,
            "failed": failed
        },
        "results": results
    }
    
    with open("test-results-comfi.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Reporte guardado en test-results-comfi.json")
    return report

if __name__ == "__main__":
    main()
