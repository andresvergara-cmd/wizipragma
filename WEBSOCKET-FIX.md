# 🔧 CENTLI - Corrección de WebSocket

**Fecha**: 2026-02-17  
**Problema**: Interfaz conversacional no funciona

---

## 🔍 Diagnóstico

### Problema Encontrado
El frontend estaba intentando conectarse a un WebSocket API que **NO EXISTE**:
```
❌ wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
```

### Error
```
HTTP 401 - Unauthorized
Invalid API identifier specified
```

---

## ✅ Solución Aplicada

### 1. Identificación del WebSocket Correcto
Encontré el WebSocket API real desplegado:
```
✅ wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
```

**Detalles**:
- API ID: `vp8zwzpjpj`
- Nombre: `poc-wizi-mex-apigateway-ws-dev`
- Stage: `dev` (no `prod`)
- Rutas: `$connect`, `$disconnect`, `sendMessage`

### 2. Actualización de Variables de Entorno

**Antes**:
```env
VITE_WEBSOCKET_URL=wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
```

**Después**:
```env
VITE_WEBSOCKET_URL=wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
```

**Archivos actualizados**:
- `frontend/.env`
- `frontend/.env.production`

### 3. Rebuild y Redeploy
```bash
npm run build --prefix frontend
aws s3 sync frontend/dist/ s3://centli-frontend-prod/ --delete
```

---

## 🧪 Pruebas Realizadas

### Test con Python
```python
✅ WebSocket conectado exitosamente
🆔 Session ID: session-1771355405-test

📝 TEST 1: Enviando mensaje de texto...
📤 Mensaje de texto enviado
📨 Respuesta recibida: {"message": "Internal server error"}

🎤 TEST 2: Enviando mensaje de audio...
📤 Mensaje de audio enviado
📨 Respuesta recibida: {"message": "Internal server error"}
```

### Resultado
- ✅ **Conexión exitosa** al WebSocket
- ⚠️ **Lambda devuelve error interno** (problema del backend, no del frontend)

---

## 📊 Estado Actual

| Componente | Estado | Nota |
|------------|--------|------|
| WebSocket Connection | ✅ Funciona | Se conecta correctamente |
| Frontend | ✅ Desplegado | URL correcta configurada |
| Lambda Backend | ⚠️ Error | Devuelve "Internal server error" |

---

## 🎯 Próximos Pasos

### Inmediato
1. ✅ Frontend actualizado y desplegado
2. ⏳ Verificar logs del Lambda `sendMessage`
3. ⏳ Corregir error interno del Lambda
4. ⏳ Probar nuevamente

### Para Verificar en CloudWatch
```bash
# Ver logs del Lambda
aws logs tail /aws/lambda/poc-wizi-mex-lambda-message-dev --follow --profile pragma-power-user
```

---

## 🔗 URLs Actualizadas

### Frontend
```
http://centli-frontend-prod.s3-website-us-east-1.amazonaws.com
```

### WebSocket (CORRECTO)
```
wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
```

---

## 📝 Notas Técnicas

### Por qué falló antes
1. URL incorrecta en variables de entorno
2. API Gateway `vvg621xawg` no existe
3. Stage era `prod` pero debía ser `dev`

### Cómo se corrigió
1. Listado de APIs con AWS CLI
2. Identificación del API correcto
3. Verificación de stages
4. Actualización de variables
5. Rebuild y redeploy

---

## ✅ Conclusión

**Problema del Frontend**: ✅ RESUELTO
- WebSocket se conecta correctamente
- Frontend desplegado con URL correcta

**Problema del Backend**: ⚠️ PENDIENTE
- Lambda devuelve "Internal server error"
- Necesita revisión de logs en CloudWatch
- Posible problema con Bedrock AgentCore

---

**Última actualización**: 2026-02-17 20:00 UTC  
**Estado**: Frontend funcional, backend con errores internos

