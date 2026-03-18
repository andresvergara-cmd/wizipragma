# Deploy Urgente - System Prompt Ultra Simplificado

## Problema Detectado
El validador funciona, pero el texto se transmite en streaming ANTES de que pueda limpiarlo. El usuario ve "Hola Carlos" antes de que el validador actúe.

## Solución Implementada
System prompt ultra simplificado y directo que enfatiza:
- 🚨 NO mencionar Carlos/México NUNCA
- 🎯 Usar tools INMEDIATAMENTE sin texto previo
- Instrucciones al inicio del prompt (lo primero que lee el modelo)

## Cambios en bedrock_config.py

```python
🚨 REGLA ABSOLUTA - LEE ESTO PRIMERO:
Tu nombre es COMFI. Trabajas para COMFAMA en COLOMBIA. Usas PESOS COLOMBIANOS (COP).
NUNCA menciones: Carlos, México, MXN, CENTLI.
Si estás a punto de decir cualquiera de esas palabras → DETENTE INMEDIATAMENTE.

🎯 REGLA DE TOOLS - ÚSALOS INMEDIATAMENTE:
Si la pregunta es sobre Comfama → USA answer_faq SIN GENERAR TEXTO PREVIO
NO escribas "Hola", NO escribas "Entiendo", NO escribas nada → USA EL TOOL DIRECTAMENTE
```

## Deploy

### Paso 1: Obtener Credenciales
En la consola de AWS, haz clic en tu usuario → "Command line or programmatic access" → Copia Opción 1:

```bash
export AWS_ACCESS_KEY_ID="ASIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."
```

### Paso 2: Verificar
```bash
aws sts get-caller-identity
```

### Paso 3: Deploy
```bash
cd src_aws/app_inference
./deploy.sh
```

O manualmente:
```bash
aws lambda update-function-code \
  --function-name centli-app-message \
  --zip-file fileb://lambda_function.zip
```

## Prueba
1. Abre https://db4aulosarsdo.cloudfront.net
2. Pregunta: "¿Cómo me afilio a Comfama?"
3. NO debe aparecer "Carlos" o "México" en NINGÚN momento del streaming

## Si Aún Aparece Carlos

Significa que el modelo tiene el prompt anterior en caché. Soluciones:

1. **Esperar 5-10 minutos** para que expire el caché
2. **Limpiar historial de conversación** en DynamoDB
3. **Usar una nueva sesión** (abrir en ventana incógnita)
4. **Aumentar temperatura** a 0.7 para más variabilidad

## Monitoreo
```bash
aws logs tail /aws/lambda/centli-app-message --follow
```

Buscar:
- `Validating response identity...`
- `IDENTITY VIOLATION DETECTED`
- Cualquier mención de "carlos" o "méxico"
