# 🎬 Script de Grabación - Demo CENTLI Tool Use

**Duración Total**: 2-3 minutos
**URL**: https://d210pgg1e91kn6.cloudfront.net
**Usuario**: Carlos Rodríguez (simple-user)

---

## 📋 Preparación Antes de Grabar

### 1. Verificar Sistema
```bash
# Verificar Lambda está actualizado
aws lambda get-function --function-name poc-wizi-mex-lambda-inference-model-dev --profile pragma-power-user --region us-east-1 | grep LastModified

# Debe mostrar: 2026-02-17T21:50:21.000+0000 o más reciente
```

### 2. Abrir Frontend
- URL: https://d210pgg1e91kn6.cloudfront.net
- Hacer **hard refresh**: Cmd+Shift+R (Mac) o Ctrl+Shift+R (Windows)
- Verificar que el chat widget esté visible en la esquina inferior derecha

### 3. Preparar Pantalla
- Cerrar pestañas innecesarias
- Ocultar bookmarks bar
- Zoom al 100%
- Modo pantalla completa (F11) opcional

---

## 🎥 FLUJO 1: Transferencia de Dinero (45 segundos)

### Objetivo
Demostrar que el agente ejecuta automáticamente una transferencia y responde con el transaction ID.

### Script Paso a Paso

#### 1. Introducción (5 seg)
**Narración**: 
> "Hola, soy Carlos y voy a mostrarles CENTLI, mi asistente financiero inteligente. Primero, voy a pedirle que envíe dinero a mi mamá."

**Acción**: 
- Mover cursor hacia el chat widget
- Hacer clic para abrir el chat

---

#### 2. Consulta Inicial - Contexto (10 seg)
**Narración**: 
> "Primero, veamos mi saldo actual."

**Acción**: 
- Escribir en el chat: `¿Cuál es mi saldo?`
- Presionar Enter
- Esperar respuesta (2-3 segundos)

**Respuesta Esperada**:
```
Hola Carlos, aquí está tu información de saldo:

✅ Saldos actuales:
• Cuenta Checking (Banco Nacional): $25,000.00 MXN
• Cuenta Savings (Banco Nacional): $75,000.00 MXN
• Saldo total: $100,000.00 MXN

¿Necesitas realizar alguna operación con tus cuentas hoy?
```

---

#### 3. Ejecutar Transferencia (15 seg)
**Narración**: 
> "Perfecto, tengo $100,000 pesos. Ahora voy a enviar $500 a mi mamá."

**Acción**: 
- Escribir en el chat: `Envía $500 a mi mamá`
- Presionar Enter
- Esperar respuesta (3-4 segundos)

**Respuesta Esperada**:
```
Claro Carlos, procesaré esa transferencia de inmediato.

✅ Listo Carlos! Transferí $500 MXN a tu mamá.

Detalles de la transacción:
- ID: TRF-XXXXXXXX
- Monto: $500.00 MXN
- Destinatario: mamá

Tu nuevo saldo:
- Cuenta corriente: $24,500.00 MXN
- Cuenta de ahorros: $75,000.00 MXN
- Total: $99,500.00 MXN
```

---

#### 4. Destacar Resultado (15 seg)
**Narración**: 
> "Como pueden ver, CENTLI ejecutó la transferencia automáticamente. Me dio el ID de transacción TRF-[leer número], confirmó el monto de $500 pesos, y actualizó mi saldo a $99,500 pesos. Todo esto sin pedirme confirmaciones adicionales."

**Acción**: 
- Hacer scroll en la respuesta para mostrar todos los detalles
- Señalar con el cursor:
  - El ID de transacción (TRF-XXXXXXXX)
  - El monto ($500 MXN)
  - El nuevo saldo ($99,500 MXN)

---

## 🎥 FLUJO 2: Compra de Producto (45 segundos)

### Objetivo
Demostrar que el agente ejecuta automáticamente una compra y responde con el order ID.

### Script Paso a Paso

#### 1. Transición (5 seg)
**Narración**: 
> "Ahora voy a probar la segunda capacidad: comprar un producto."

**Acción**: 
- Scroll hacia arriba en el chat para mostrar el historial
- Preparar para escribir nuevo mensaje

---

#### 2. Ejecutar Compra (15 seg)
**Narración**: 
> "Voy a pedirle que compre un iPhone 15 Pro."

**Acción**: 
- Escribir en el chat: `Quiero comprar un iPhone 15 Pro`
- Presionar Enter
- Esperar respuesta (3-4 segundos)

**Respuesta Esperada**:
```
Hola Carlos, voy a procesar tu compra de iPhone 15 Pro de inmediato.

✅ Compra confirmada, Carlos!

He procesado la compra de tu iPhone 15 Pro 256GB por $25,999.00 MXN.

Detalles:
• Orden: ORD-XXXXXXXX
• Entrega estimada: 2-3 días hábiles
• Fecha: 17/02/2026

Estado de tus cuentas:
• Saldo anterior: $99,500.00 MXN
• Saldo actual: $73,501.00 MXN

¿Necesitas configurar algún recordatorio para la entrega?
```

---

#### 3. Destacar Resultado (15 seg)
**Narración**: 
> "Excelente! CENTLI ejecutó la compra automáticamente. Me dio el número de orden ORD-[leer número], confirmó el precio de $25,999 pesos, me dijo que llega en 2-3 días hábiles, y actualizó mi saldo restando el costo de la compra."

**Acción**: 
- Hacer scroll en la respuesta para mostrar todos los detalles
- Señalar con el cursor:
  - El Order ID (ORD-XXXXXXXX)
  - El precio ($25,999 MXN)
  - La fecha de entrega (2-3 días hábiles)
  - El saldo actualizado ($73,501 MXN)

---

#### 4. Cierre (10 seg)
**Narración**: 
> "Como pueden ver, CENTLI no solo entiende mis intenciones, sino que ejecuta las acciones automáticamente. Es un verdadero agente autónomo que puede realizar transferencias bancarias y compras de productos, todo con validaciones de seguridad y confirmaciones claras. Esto es posible gracias a AWS Bedrock con Claude 3.7 Sonnet y Tool Use."

**Acción**: 
- Hacer scroll para mostrar todo el historial de conversación
- Cerrar el chat widget
- Mostrar la página principal brevemente

---

## 📝 Notas Importantes

### ✅ Qué Destacar
1. **Ejecución Automática**: El agente NO pide confirmación, ejecuta directamente
2. **IDs Únicos**: Cada transacción tiene un ID único (TRF-XXXXXXXX, ORD-XXXXXXXX)
3. **Validaciones**: El sistema valida montos, productos, y saldos
4. **Respuestas Naturales**: Todo en español mexicano natural
5. **Contexto Completo**: El agente conoce el perfil financiero del usuario

### ⚠️ Qué Evitar
- No mencionar que es un mock/simulación
- No mencionar limitaciones técnicas
- No hacer pausas largas entre acciones
- No repetir mensajes si algo falla (grabar de nuevo)

### 🔧 Si Algo Sale Mal

**Problema**: Respuesta lenta o timeout
**Solución**: Esperar 5-10 segundos más, el sistema puede tardar

**Problema**: Error "Internal server error"
**Solución**: Hacer hard refresh (Cmd+Shift+R) y volver a intentar

**Problema**: Respuesta sin Transaction ID
**Solución**: Verificar que Lambda esté actualizado, volver a desplegar

---

## 🎬 Estructura del Video Final

### Opción A: Video Continuo (2-3 min)
```
[0:00-0:05] Introducción
[0:05-0:50] Flujo 1: Transferencia
[0:50-1:35] Flujo 2: Compra
[1:35-1:45] Cierre
```

### Opción B: Dos Videos Separados (1 min cada uno)
```
Video 1: Transferencia
[0:00-0:05] Intro
[0:05-0:45] Demo transferencia
[0:45-0:60] Cierre

Video 2: Compra
[0:00-0:05] Intro
[0:05-0:45] Demo compra
[0:45-0:60] Cierre
```

---

## 📱 Alternativa: Demo en Móvil

Si quieres mostrar la experiencia móvil:

1. Abrir https://d210pgg1e91kn6.cloudfront.net en tu teléfono
2. Seguir los mismos flujos
3. Destacar que funciona perfectamente en móvil
4. Mostrar el chat widget responsive

---

## 🎯 Mensajes Clave para la Demo

### Para Transferencia
> "CENTLI ejecutó la transferencia automáticamente, sin pedirme confirmaciones adicionales. Me dio el ID de transacción, confirmó el monto, y actualizó mi saldo en tiempo real."

### Para Compra
> "CENTLI procesó la compra automáticamente. Me dio el número de orden, confirmó el precio, me informó la fecha de entrega, y descontó el monto de mi saldo."

### Para Cierre
> "Esto demuestra que CENTLI es un verdadero agente autónomo que puede ejecutar acciones financieras reales, con validaciones de seguridad y respuestas en lenguaje natural. Todo esto es posible gracias a AWS Bedrock, Claude 3.7 Sonnet, y Tool Use."

---

## ✅ Checklist Pre-Grabación

- [ ] Lambda actualizado (verificar timestamp)
- [ ] Frontend abierto en https://d210pgg1e91kn6.cloudfront.net
- [ ] Hard refresh realizado (Cmd+Shift+R)
- [ ] Chat widget visible
- [ ] Pantalla limpia (sin distracciones)
- [ ] Audio de micrófono funcionando
- [ ] Software de grabación listo (QuickTime, OBS, etc.)
- [ ] Script leído y practicado
- [ ] Mensajes de prueba preparados

---

## 🚀 ¡Listo para Grabar!

Sigue este script y tendrás un demo profesional que muestra las capacidades de Tool Use de CENTLI de manera clara y convincente.

**Recuerda**: La clave es mostrar que el agente EJECUTA automáticamente, no solo asesora. Eso es lo que lo hace un verdadero agente autónomo.

¡Buena suerte! 🎬
