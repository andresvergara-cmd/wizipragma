# 🚀 Instrucciones de Deploy - Backend Comfi FAQ

**Fecha:** 2024-03-12  
**Objetivo:** Desplegar backend actualizado con sistema FAQ

---

## 📋 CAMBIOS EN EL BACKEND

### Archivos Modificados

1. **src_aws/app_inference/action_tools.py**
   - ✅ Base de datos FAQ (5 FAQs)
   - ✅ Función `answer_faq()`
   - ✅ Tool `answer_faq` en `get_available_tools()`
   - ✅ Handler en `execute_tool()`
   - ✅ Moneda actualizada a COP

2. **src_aws/app_inference/bedrock_config.py**
   - ✅ System prompt: CENTLI → Comfi
   - ✅ Contexto: México → Comfama (Colombia)
   - ✅ Capacidades FAQ agregadas
   - ✅ Ejemplos de uso FAQ
   - ✅ Moneda actualizada a COP

---

## 🔧 OPCIONES DE DEPLOY

### Opción 1: Deploy Manual con AWS CLI

#### Paso 1: Empaquetar Lambda

```bash
# Ir al directorio del backend
cd src_aws

# Crear directorio de empaquetado
mkdir -p package

# Instalar dependencias
pip install -r requirements.txt -t package/

# Copiar código de la aplicación
cp -r app_inference package/
cp -r app_connect package/
cp -r app_disconnect package/
cp -r app_message package/

# Crear ZIP
cd package
zip -r ../lambda-comfi-faq.zip .
cd ..

# Agregar archivos adicionales si es necesario
zip -g lambda-comfi-faq.zip *.py
```

#### Paso 2: Actualizar Lambda Functions

```bash
# Actualizar función de inference (la que tiene bedrock_config.py)
aws lambda update-function-code \
    --function-name <NOMBRE_FUNCION_INFERENCE> \
    --zip-file fileb://lambda-comfi-faq.zip

# Esperar a que se actualice
aws lambda wait function-updated \
    --function-name <NOMBRE_FUNCION_INFERENCE>
```

**Nota:** Reemplaza `<NOMBRE_FUNCION_INFERENCE>` con el nombre real de tu función Lambda.

---

### Opción 2: Deploy con SAM/CDK (Si usas IaC)

Si tu proyecto usa SAM o CDK:

```bash
# Con SAM
sam build
sam deploy

# Con CDK
cdk deploy
```

---

### Opción 3: Deploy Manual desde Consola AWS

1. **Ir a AWS Lambda Console**
   - https://console.aws.amazon.com/lambda/

2. **Buscar tu función Lambda** (la que maneja inference)

3. **Subir código:**
   - Click en "Upload from" → ".zip file"
   - Seleccionar `lambda-comfi-faq.zip`
   - Click "Save"

4. **Esperar deployment**
   - Verificar que el estado sea "Active"

---

## 🧪 VERIFICAR DEPLOY

### 1. Verificar Variables de Entorno

Asegúrate de que tu Lambda tenga estas variables:

```
REGION_NAME=us-east-1
API_ENDPOINT=<tu-websocket-endpoint>
```

### 2. Probar Tool Answer FAQ

Puedes probar directamente en Lambda:

```python
# Test event
{
  "tool_name": "answer_faq",
  "tool_input": {
    "question": "¿Cómo me afilio a Comfama?"
  }
}
```

**Respuesta esperada:**
```json
{
  "success": true,
  "faq_id": "faq-afiliacion-001",
  "question": "¿Cómo me afilio a Comfama?",
  "shortAnswer": "Tu empleador te afilia automáticamente...",
  "confidence": 0.83
}
```

### 3. Probar desde Frontend

1. Abrir: https://d210pgg1e91kn6.cloudfront.net/
2. Abrir chat
3. Escribir: "¿Cómo me afilio a Comfama?"
4. Verificar que:
   - WebSocket conecta
   - Bot responde
   - (Idealmente) FAQCard se renderiza

---

## 📊 CHECKLIST DE DEPLOY

### Pre-Deploy
- [ ] Build frontend completado
- [ ] Frontend desplegado a S3
- [ ] CloudFront invalidado
- [ ] Código backend actualizado localmente

### Deploy Backend
- [ ] Lambda empaquetado
- [ ] Dependencias incluidas
- [ ] Código subido a Lambda
- [ ] Variables de entorno verificadas

### Post-Deploy
- [ ] Lambda en estado "Active"
- [ ] Test de answer_faq exitoso
- [ ] WebSocket conecta desde frontend
- [ ] Chat responde correctamente

### Verificación FAQ
- [ ] Pregunta FAQ enviada
- [ ] Backend usa tool answer_faq
- [ ] Respuesta FAQ recibida
- [ ] FAQCard renderizado (si backend responde correctamente)

---

## 🐛 TROUBLESHOOTING

### Error: "Module not found"
**Solución:** Verificar que todas las dependencias estén en el ZIP

```bash
# Verificar contenido del ZIP
unzip -l lambda-comfi-faq.zip | grep -E "(loguru|boto3)"
```

### Error: "Tool not found"
**Solución:** Verificar que `answer_faq` esté en `get_available_tools()`

```python
# En action_tools.py
def get_available_tools():
    return [
        # ... otros tools
        {
            "toolSpec": {
                "name": "answer_faq",
                # ...
            }
        }
    ]
```

### WebSocket no conecta
**Solución:** Verificar URL en `.env.production`

```bash
# frontend/.env.production
VITE_WEBSOCKET_URL=wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
```

### FAQCard no se renderiza
**Posibles causas:**
1. Backend no está usando el tool
2. Respuesta no tiene el formato esperado
3. `parseFAQFromMessage()` no detecta el FAQ

**Solución:** Verificar logs de Lambda y consola del navegador

---

## 📝 NOMBRES DE FUNCIONES LAMBDA

Basado en tu proyecto, las funciones Lambda probablemente son:

- **app_connect**: Maneja conexiones WebSocket
- **app_disconnect**: Maneja desconexiones
- **app_message**: Maneja mensajes (incluye inference)

**La función que necesitas actualizar es:** `app_message` o la que contenga `bedrock_config.py`

---

## 🚀 COMANDO RÁPIDO DE DEPLOY

Si conoces el nombre de tu función Lambda:

```bash
# Build
cd frontend && npm run build && cd ..

# Deploy Frontend
./deploy-comfi-faq.sh

# Deploy Backend (ajusta el nombre de la función)
cd src_aws
zip -r lambda.zip app_inference/ app_message/ requirements.txt
aws lambda update-function-code \
    --function-name <TU_FUNCION_LAMBDA> \
    --zip-file fileb://lambda.zip
```

---

## ✅ VERIFICACIÓN FINAL

Una vez desplegado todo:

1. **Abrir:** https://d210pgg1e91kn6.cloudfront.net/
2. **Verificar:**
   - Logo dice "Comfi"
   - Welcome screen muestra 5 quick actions FAQ
   - Chat conecta (indicador "En línea")
3. **Probar:**
   - Click en quick action FAQ
   - Escribir: "¿Cómo me afilio a Comfama?"
   - Verificar respuesta

**Éxito:** Si ves FAQCard renderizado con la respuesta estructurada

---

**Última actualización:** 2024-03-12  
**Estado:** Listo para Deploy Backend
