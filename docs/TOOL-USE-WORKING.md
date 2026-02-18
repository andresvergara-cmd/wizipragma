# ✅ Tool Use - FUNCIONANDO

**Fecha**: 2026-02-17 21:51 UTC
**Status**: 🎉 COMPLETADO Y FUNCIONANDO

## Problema Resuelto

### Problema Original
Los parámetros de las herramientas llegaban vacíos `{}` causando errores:
```
Error: transfer_money() missing 2 required positional arguments: 'amount' and 'recipient_name'
```

### Causa Raíz
1. **Parsing de Input**: El input de las herramientas llega como JSON string en chunks que deben acumularse
2. **Formato de Respuesta**: Al enviar el tool use de vuelta a Bedrock, el `input` debe ser un objeto JSON, no un string

### Solución Implementada
1. Acumular correctamente los chunks de input en `contentBlockDelta`
2. Convertir el string JSON acumulado a objeto antes de enviarlo de vuelta a Bedrock
3. Mantener el input como string durante la acumulación, convertir a objeto solo al ejecutar y al responder

## Pruebas Exitosas

### Test 1: Transferencia de Dinero ✅
**Input**: "Envía $500 a mi mamá"

**Output**:
```
✅ Listo Carlos! Transferí $500 MXN a tu mamá.

Detalles de la transacción:
- ID: TRF-589591BC
- Monto: $500.00 MXN
- Destinatario: mamá

Tu nuevo saldo:
- Cuenta corriente: $24,500.00 MXN
- Cuenta de ahorros: $75,000.00 MXN
- Total: $99,500.00 MXN
```

**Validación**:
- ✅ Tool `transfer_money` ejecutado correctamente
- ✅ Parámetros capturados: `amount=500`, `recipient_name="mamá"`
- ✅ Transaction ID generado: `TRF-589591BC`
- ✅ Respuesta natural y completa
- ✅ Saldos actualizados mostrados

### Test 2: Compra de Producto ✅
**Input**: "Quiero comprar un iPhone 15 Pro"

**Output**:
```
✅ Compra confirmada, Carlos!

He procesado la compra de tu iPhone 15 Pro 256GB por $25,999.00 MXN.

Detalles:
• Orden: ORD-EB5B8D9C
• Entrega estimada: 2-3 días hábiles
• Fecha: 17/02/2026

Estado de tus cuentas:
• Saldo anterior: $100,000.00 MXN
• Saldo actual: $74,001.00 MXN
```

**Validación**:
- ✅ Tool `purchase_product` ejecutado correctamente
- ✅ Parámetros capturados: `product_name="iPhone 15 Pro"`
- ✅ Order ID generado: `ORD-EB5B8D9C`
- ✅ Precio correcto del catálogo: $25,999 MXN
- ✅ Cálculo de saldo correcto
- ✅ Respuesta natural y completa

### Test 3: Consulta de Saldo (Sin Tool Use) ✅
**Input**: "¿Cuál es mi saldo?"

**Output**:
```
Hola Carlos, aquí está tu información de saldo:

✅ Saldos actuales:
• Cuenta Checking (Banco Nacional): $25,000.00 MXN
• Cuenta Savings (Banco Nacional): $75,000.00 MXN
• Saldo total: $100,000.00 MXN

¿Necesitas realizar alguna operación con tus cuentas hoy?
```

**Validación**:
- ✅ No usa herramientas (correcto)
- ✅ Responde con conocimiento interno
- ✅ Datos precisos del usuario

## Arquitectura de Tool Use

### Flujo Completo

```
1. Usuario envía mensaje
   ↓
2. Lambda recibe via WebSocket
   ↓
3. Bedrock ConverseStream con toolConfig
   ↓
4. Modelo decide usar herramienta
   ↓
5. contentBlockStart: {toolUseId, name}
   ↓
6. contentBlockDelta: {input: "{"amo"}
   ↓
7. contentBlockDelta: {input: "unt": 500}
   ↓
8. contentBlockDelta: {input: ", "recipient"}
   ↓
9. contentBlockStop: Acumular input completo
   ↓
10. messageStop: Ejecutar herramienta
    ↓
11. Convertir input string → JSON object
    ↓
12. Ejecutar función Python
    ↓
13. Obtener resultado
    ↓
14. Enviar resultado a Bedrock (input como objeto)
    ↓
15. Bedrock genera respuesta final
    ↓
16. Stream respuesta al usuario
```

### Código Clave

**Acumulación de Input**:
```python
elif 'contentBlockDelta' in chunk:
    delta = chunk['contentBlockDelta']['delta']
    if 'toolUse' in delta:
        if current_tool and 'input' in delta['toolUse']:
            current_tool['input'] += delta['toolUse']['input']  # Acumular string
```

**Conversión y Ejecución**:
```python
# Parse input string to dict
tool_input = json.loads(tool_input_str) if isinstance(tool_input_str, str) else tool_input_str

# Execute the tool
result = execute_tool(tool_name, tool_input)
```

**Formato para Bedrock**:
```python
# Convert input to JSON object for Bedrock
tool_input_obj = json.loads(tool_input_str)

tool_use_content.append({
    "toolUse": {
        "toolUseId": tool_block.get('toolUseId'),
        "name": tool_block.get('name'),
        "input": tool_input_obj  # Must be JSON object, not string
    }
})
```

## Herramientas Disponibles

### 1. transfer_money
**Descripción**: Ejecuta una transferencia de dinero

**Parámetros**:
- `amount` (number, required): Monto en MXN
- `recipient_name` (string, required): Nombre del destinatario
- `concept` (string, optional): Concepto de la transferencia

**Validaciones**:
- Monto > 0
- Monto ≤ $50,000 MXN (límite diario)

**Respuesta**:
```json
{
  "success": true,
  "transaction_id": "TRF-XXXXXXXX",
  "amount": 500,
  "currency": "MXN",
  "recipient": "mamá",
  "timestamp": "2026-02-17 21:49:29",
  "status": "completed"
}
```

### 2. purchase_product
**Descripción**: Ejecuta la compra de un producto

**Parámetros**:
- `product_name` (string, required): Nombre del producto
- `quantity` (integer, optional): Cantidad (default: 1)

**Catálogo**:
- iPhone 15 Pro: $25,999 MXN
- iPhone 15: $21,999 MXN
- MacBook Air M3: $35,999 MXN
- AirPods Pro 2: $5,499 MXN
- iPad Air: $15,999 MXN
- Apple Watch Series 9: $12,999 MXN

**Validaciones**:
- Producto existe en catálogo
- Total ≤ $100,000 MXN (límite de compra)

**Respuesta**:
```json
{
  "success": true,
  "order_id": "ORD-XXXXXXXX",
  "product": "iPhone 15 Pro 256GB",
  "quantity": 1,
  "unit_price": 25999,
  "total": 25999,
  "currency": "MXN",
  "timestamp": "2026-02-17 21:49:37",
  "status": "confirmed",
  "delivery": "2-3 días hábiles"
}
```

## Comportamiento del Agente

### Cuándo Usa Herramientas
- ✅ "Envía dinero", "transferir", "pagar" → `transfer_money`
- ✅ "Comprar", "quiero un producto" → `purchase_product`
- ✅ Ejecuta automáticamente sin pedir confirmación adicional

### Cuándo NO Usa Herramientas
- ❌ Consultas de saldo → Usa contexto interno
- ❌ Análisis financiero → Usa conocimiento del modelo
- ❌ Recomendaciones → Usa razonamiento interno

## Archivos Modificados

### Backend
1. `src_aws/app_inference/bedrock_config.py`
   - Acumulación correcta de input en streaming
   - Conversión de string a objeto para Bedrock
   - Manejo de tool results

2. `src_aws/app_inference/action_tools.py`
   - Implementación de `transfer_money()`
   - Implementación de `purchase_product()`
   - Tool definitions para Bedrock
   - Función `execute_tool()`

### Scripts de Prueba
1. `test-tool-use-complete.py` - Suite completa de tests
2. `test-transfer-only.py` - Test específico de transferencia
3. `deploy-tool-use-fix.sh` - Script de deployment

### Documentación
1. `TOOL-USE-STATUS.md` - Estado anterior (debugging)
2. `TOOL-USE-WORKING.md` - Este documento (funcionando)

## Logs de Éxito

```
2026-02-17 21:49:29.507 | INFO | Tool use stop, accumulated input: {"amount": 500, "recipient_name": "mamá"}
2026-02-17 21:49:29.507 | INFO | Tool use requested: 1 tools
2026-02-17 21:49:29.508 | INFO | Executing tool: transfer_money
2026-02-17 21:49:29.508 | INFO | Executing transfer: $500 MXN to mamá
2026-02-17 21:49:29.508 | INFO | Transfer completed: TRF-9EFEF051
2026-02-17 21:49:29.508 | INFO | Getting final response with tool results
```

## Próximos Pasos

### Completado ✅
- [x] Implementar Tool Use
- [x] Debuggear parsing de parámetros
- [x] Probar transferencias
- [x] Probar compras
- [x] Validar respuestas naturales

### Pendiente
- [ ] Implementar Nova Sonic para audio (transcripción)
- [ ] Crear video demo mostrando ambos flujos
- [ ] Agregar más productos al catálogo
- [ ] Implementar validaciones de seguridad reales
- [ ] Integrar con APIs bancarias reales

## Demo Script

### Escena 1: Transferencia (30 seg)
```
Usuario: "Envía $500 a mi mamá"
CENTLI: [Ejecuta transfer_money]
        "✅ Listo Carlos! Transferí $500 MXN a tu mamá.
         ID: TRF-XXXXXXXX
         Tu nuevo saldo: $99,500 MXN"
```

### Escena 2: Compra (30 seg)
```
Usuario: "Quiero comprar un iPhone 15 Pro"
CENTLI: [Ejecuta purchase_product]
        "✅ Compra confirmada! iPhone 15 Pro por $25,999 MXN
         Orden: ORD-XXXXXXXX
         Entrega: 2-3 días hábiles"
```

### Escena 3: Consulta (15 seg)
```
Usuario: "¿Cuál es mi saldo?"
CENTLI: [Sin herramientas]
        "Saldo total: $100,000 MXN
         Checking: $25,000 MXN
         Savings: $75,000 MXN"
```

## Conclusión

🎉 **Tool Use está 100% funcional y listo para demo!**

El agente CENTLI ahora puede:
- ✅ Ejecutar transferencias automáticamente
- ✅ Procesar compras automáticamente
- ✅ Generar IDs de transacción únicos
- ✅ Responder con lenguaje natural mexicano
- ✅ Mostrar detalles completos de cada operación
- ✅ Decidir inteligentemente cuándo usar herramientas

**Estado**: LISTO PARA DEMO 🚀
