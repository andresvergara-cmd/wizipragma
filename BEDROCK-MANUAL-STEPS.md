# Pasos Manuales para Resolver Bedrock Agent

## Problema Actual
Error: `accessDeniedException` al invocar el agente desde Lambda

## Solución: Verificar Acceso al Modelo en Consola

### Paso 1: Solicitar Acceso al Modelo (si es necesario)

1. Ve a AWS Console → Bedrock
2. En el menú lateral, click en "Model access"
3. Busca "Claude 3.5 Sonnet v2" (anthropic.claude-3-5-sonnet-20241022-v2:0)
4. Si dice "Available" o "Access granted" → Ya tienes acceso
5. Si dice "Request access" → Click y solicita acceso (puede tomar unos minutos)

### Paso 2: Verificar el Agente en Consola

1. Ve a AWS Console → Bedrock → Agents
2. Busca el agente "centli-agentcore" (ID: Z6PCEKYNPS)
3. Click en el agente
4. Verifica:
   - Status: PREPARED ✅
   - Foundation model: Claude 3.5 Sonnet v2 ✅
   - Service role: CentliBedrockAgentRole ✅

### Paso 3: Probar el Agente en Consola

1. En la página del agente, busca la sección "Test"
2. En el alias dropdown, selecciona "prod" (BRUXPV975I)
3. En el campo de texto, escribe: "Hola, ¿cuál es mi saldo?"
4. Click "Run"
5. **Si funciona aquí pero no desde Lambda** → Es un problema de permisos de Lambda
6. **Si NO funciona aquí** → Es un problema con el agente o el modelo

### Paso 4: Verificar Permisos del Rol del Agente

1. Ve a IAM → Roles
2. Busca "CentliBedrockAgentRole"
3. Click en el rol
4. En "Permissions", verifica que tenga:
   - Policy: BedrockAgentFullPolicy
   - Actions: bedrock:InvokeModel, bedrock:InvokeModelWithResponseStream
   - Resource: arn:aws:bedrock:*::foundation-model/*

### Paso 5: Verificar Trust Relationship del Rol

1. En el mismo rol "CentliBedrockAgentRole"
2. Click en "Trust relationships"
3. Verifica que el trust policy sea:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Service": "bedrock.amazonaws.com"
    },
    "Action": "sts:AssumeRole"
  }]
}
```

### Paso 6: Verificar Permisos de Lambda

1. Ve a IAM → Roles
2. Busca "CentliLambdaExecutionRole"
3. Verifica que tenga:
   - Policy: BedrockAgentInvokePolicy
   - Actions: bedrock:InvokeAgent, bedrock:Retrieve, bedrock:RetrieveAndGenerate
   - Resource: *

### Paso 7: Si Todo Falla - Usar Bedrock Converse API

Si después de verificar todo lo anterior el problema persiste, podemos cambiar a usar Bedrock Converse API que es más simple:

```python
# En app_message.py, reemplazar la sección de invoke_agent con:

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock_runtime.converse(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    messages=[{
        "role": "user",
        "content": [{"text": content}]
    }],
    system=[{
        "text": "Eres CENTLI, un asistente bancario multimodal..."
    }],
    inferenceConfig={
        "maxTokens": 1000,
        "temperature": 0.7
    }
)

response_text = response['output']['message']['content'][0]['text']
```

## Comandos Útiles

### Verificar estado del agente
```bash
aws bedrock-agent get-agent \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --agent-id Z6PCEKYNPS
```

### Ver logs de Lambda
```bash
aws logs tail /aws/lambda/centli-app-message \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --since 5m \
  --follow
```

### Probar WebSocket
```bash
node test-bedrock-agent.js
```

## Información del Agente

- **Agent ID**: Z6PCEKYNPS
- **Agent Name**: centli-agentcore
- **Alias ID**: BRUXPV975I
- **Alias Name**: prod
- **Model**: anthropic.claude-3-5-sonnet-20241022-v2:0
- **Service Role**: arn:aws:iam::777937796305:role/CentliBedrockAgentRole
- **Lambda Role**: arn:aws:iam::777937796305:role/CentliLambdaExecutionRole

## Próximos Pasos

1. Sigue los pasos 1-6 arriba
2. Si el agente funciona en consola, el problema es de permisos de Lambda
3. Si no funciona en consola, el problema es con el agente o modelo
4. Si todo falla, usa Converse API (Paso 7)

---

**Nota**: El error `accessDeniedException` generalmente significa que:
- El modelo no tiene acceso habilitado en la cuenta
- El rol del agente no tiene permisos para invocar el modelo
- Hay una política de servicio que bloquea el acceso
