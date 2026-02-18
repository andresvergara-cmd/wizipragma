# 📦 Entregables para Demo - CENTLI Tool Use

## 🎯 Objetivo
Grabar un video demo de 2-3 minutos mostrando las capacidades de Tool Use de CENTLI:
1. **Transferencia de dinero** - Ejecuta automáticamente con transaction ID
2. **Compra de producto** - Ejecuta automáticamente con order ID

---

## 📁 Archivos Entregados

### 1. Script de Grabación Principal
**Archivo**: `DEMO-SCRIPT-GRABACION.md`

**Contenido**:
- ✅ Preparación antes de grabar
- ✅ Flujo 1: Transferencia de dinero (paso a paso)
- ✅ Flujo 2: Compra de producto (paso a paso)
- ✅ Narración completa con timings
- ✅ Respuestas esperadas del sistema
- ✅ Qué destacar en cada paso
- ✅ Checklist pre-grabación

**Uso**: Lee este documento antes de grabar para conocer el flujo completo

---

### 2. Tips y Técnicas de Grabación
**Archivo**: `DEMO-TIPS-GRABACION.md`

**Contenido**:
- ✅ Configuración de software de grabación
- ✅ Configuración de pantalla y audio
- ✅ Técnicas de narración profesional
- ✅ Troubleshooting durante grabación
- ✅ Script de narración detallado
- ✅ Checklist de calidad
- ✅ Edición post-grabación
- ✅ Tips de publicación

**Uso**: Consulta este documento para mejorar la calidad de tu grabación

---

### 3. Checklist Automatizado
**Archivo**: `PRE-DEMO-CHECKLIST.sh`

**Contenido**:
- ✅ Verifica Lambda actualizado
- ✅ Verifica logs recientes
- ✅ Verifica frontend accesible
- ✅ Verifica WebSocket endpoint
- ✅ Verifica tablas DynamoDB
- ✅ Verifica usuario de prueba
- ✅ Ejecuta prueba rápida automática
- ✅ Muestra checklist final

**Uso**: 
```bash
./PRE-DEMO-CHECKLIST.sh
```

---

### 4. Demo Interactivo en Navegador
**Archivo**: `demo-tool-use-browser.html`

**Contenido**:
- ✅ Interfaz visual para probar Tool Use
- ✅ Botones para cada flujo
- ✅ Visualización de mensajes en tiempo real
- ✅ Indicador de conexión
- ✅ Diseño profesional

**Uso**: Abre en navegador para probar antes de grabar
```bash
open demo-tool-use-browser.html
```

---

### 5. Tests Automatizados
**Archivos**: 
- `test-tool-use-complete.py` - Suite completa
- `test-transfer-only.py` - Solo transferencia

**Contenido**:
- ✅ Test de transferencia
- ✅ Test de compra
- ✅ Test de consulta (sin tool use)
- ✅ Validación de Transaction IDs
- ✅ Validación de Order IDs
- ✅ Reporte de resultados

**Uso**:
```bash
python3 test-tool-use-complete.py
python3 test-transfer-only.py
```

---

### 6. Script de Deployment
**Archivo**: `deploy-tool-use-fix.sh`

**Contenido**:
- ✅ Empaqueta código Lambda
- ✅ Despliega a AWS
- ✅ Espera actualización
- ✅ Muestra instrucciones de prueba

**Uso**:
```bash
./deploy-tool-use-fix.sh
```

---

### 7. Documentación Técnica
**Archivos**:
- `TOOL-USE-WORKING.md` - Documentación completa del sistema
- `SESSION-COMPLETE.md` - Resumen de la sesión
- `TOOL-USE-STATUS.md` - Estado anterior (debugging)

**Contenido**:
- ✅ Arquitectura de Tool Use
- ✅ Flujo completo de ejecución
- ✅ Código clave explicado
- ✅ Herramientas disponibles
- ✅ Logs de éxito
- ✅ Próximos pasos

**Uso**: Referencia técnica para entender el sistema

---

## 🎬 Flujo de Trabajo para Grabar

### Paso 1: Preparación (5 minutos)
```bash
# 1. Ejecutar checklist automatizado
./PRE-DEMO-CHECKLIST.sh

# 2. Si hay problemas, re-desplegar
./deploy-tool-use-fix.sh

# 3. Esperar 30 segundos después del deployment
```

### Paso 2: Verificación Manual (2 minutos)
```bash
# 1. Abrir frontend
open https://d210pgg1e91kn6.cloudfront.net

# 2. Hard refresh
# Mac: Cmd+Shift+R
# Windows: Ctrl+Shift+R

# 3. Verificar chat widget visible

# 4. Probar un mensaje rápido
# "Hola" → Debe responder
```

### Paso 3: Lectura del Script (5 minutos)
```bash
# Leer y practicar:
# - DEMO-SCRIPT-GRABACION.md
# - Sección de narración
# - Timings de cada paso
```

### Paso 4: Configuración de Grabación (3 minutos)
```bash
# 1. Abrir software de grabación
# 2. Configurar resolución: 1920x1080
# 3. Configurar frame rate: 30 fps
# 4. Probar audio
# 5. Limpiar pantalla
```

### Paso 5: Grabación (3 minutos)
```bash
# Seguir script en DEMO-SCRIPT-GRABACION.md
# - Flujo 1: Transferencia (45 seg)
# - Flujo 2: Compra (45 seg)
# - Cierre (10 seg)
```

### Paso 6: Revisión (2 minutos)
```bash
# 1. Ver video completo
# 2. Verificar audio claro
# 3. Verificar Transaction IDs visibles
# 4. Verificar sin errores
```

### Paso 7: Edición (Opcional, 10 minutos)
```bash
# 1. Cortar inicio/final
# 2. Cortar pausas largas
# 3. Agregar título
# 4. Exportar
```

---

## 📝 Mensajes Exactos para Probar

### Flujo 1: Transferencia
```
1. ¿Cuál es mi saldo?
2. Envía $500 a mi mamá
```

**Respuesta Esperada**:
- Transaction ID: `TRF-XXXXXXXX`
- Monto: `$500.00 MXN`
- Nuevo saldo: `$99,500.00 MXN`

### Flujo 2: Compra
```
3. Quiero comprar un iPhone 15 Pro
```

**Respuesta Esperada**:
- Order ID: `ORD-XXXXXXXX`
- Producto: `iPhone 15 Pro 256GB`
- Precio: `$25,999.00 MXN`
- Entrega: `2-3 días hábiles`
- Nuevo saldo: `$73,501.00 MXN`

---

## 🎯 Puntos Clave a Destacar

### Durante Transferencia
1. ✅ "CENTLI ejecutó la transferencia **automáticamente**"
2. ✅ "Sin pedir confirmaciones adicionales"
3. ✅ "Me dio el ID de transacción: TRF-XXXXXXXX"
4. ✅ "Actualizó mi saldo en tiempo real"

### Durante Compra
1. ✅ "CENTLI procesó la compra **automáticamente**"
2. ✅ "Me dio el número de orden: ORD-XXXXXXXX"
3. ✅ "Confirmó el precio y fecha de entrega"
4. ✅ "Descontó el monto de mi saldo"

### En el Cierre
1. ✅ "Es un **verdadero agente autónomo**"
2. ✅ "No solo asesora, **ejecuta acciones**"
3. ✅ "Con validaciones de seguridad"
4. ✅ "Gracias a AWS Bedrock y Tool Use"

---

## 🔧 Troubleshooting Rápido

### Problema: Lambda no responde
```bash
# Solución:
./deploy-tool-use-fix.sh
# Esperar 30 segundos
# Intentar de nuevo
```

### Problema: Frontend no carga
```bash
# Solución:
# 1. Verificar URL correcta
# 2. Hard refresh (Cmd+Shift+R)
# 3. Limpiar cache del navegador
# 4. Intentar en modo incógnito
```

### Problema: Respuesta sin Transaction ID
```bash
# Solución:
# 1. Verificar Lambda actualizado:
aws lambda get-function --function-name poc-wizi-mex-lambda-inference-model-dev --profile pragma-power-user | grep LastModified

# 2. Si es antiguo, re-desplegar:
./deploy-tool-use-fix.sh
```

### Problema: Error "Internal server error"
```bash
# Solución:
# 1. Ver logs:
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev --follow --profile pragma-power-user

# 2. Buscar errores
# 3. Re-desplegar si es necesario
```

---

## 📊 Checklist Final Pre-Grabación

```
[ ] PRE-DEMO-CHECKLIST.sh ejecutado exitosamente
[ ] Lambda actualizado (timestamp reciente)
[ ] Frontend accesible y con hard refresh
[ ] Chat widget visible
[ ] Prueba rápida exitosa (test-transfer-only.py)
[ ] Script de demo leído y practicado
[ ] Software de grabación configurado
[ ] Audio de micrófono probado
[ ] Pantalla limpia (sin notificaciones)
[ ] Escritorio ordenado
[ ] Zoom del navegador al 100%
[ ] Mensajes de prueba preparados
[ ] Listo para grabar! 🎬
```

---

## 🚀 Comandos Rápidos

### Verificar Sistema
```bash
./PRE-DEMO-CHECKLIST.sh
```

### Re-desplegar Lambda
```bash
./deploy-tool-use-fix.sh
```

### Probar Transferencia
```bash
python3 test-transfer-only.py
```

### Probar Todo
```bash
python3 test-tool-use-complete.py
```

### Ver Logs en Tiempo Real
```bash
aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev --follow --profile pragma-power-user
```

### Abrir Frontend
```bash
open https://d210pgg1e91kn6.cloudfront.net
```

### Abrir Demo Interactivo
```bash
open demo-tool-use-browser.html
```

---

## 📹 Información del Sistema

**Frontend URL**: https://d210pgg1e91kn6.cloudfront.net
**WebSocket URL**: wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
**Lambda**: poc-wizi-mex-lambda-inference-model-dev
**Usuario**: simple-user (Carlos Rodríguez)
**AWS Profile**: pragma-power-user
**Región**: us-east-1

---

## 🎉 ¡Todo Listo!

Tienes todo lo necesario para grabar un demo profesional:
- ✅ Scripts detallados
- ✅ Checklist automatizado
- ✅ Tests de validación
- ✅ Troubleshooting completo
- ✅ Sistema funcionando al 100%

**Siguiente paso**: Ejecuta `./PRE-DEMO-CHECKLIST.sh` y sigue el script en `DEMO-SCRIPT-GRABACION.md`

¡Buena suerte con la grabación! 🎬🚀
