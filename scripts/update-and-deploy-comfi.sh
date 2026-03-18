#!/bin/bash

# Script completo para actualizar Comfi y desplegar nueva versión

set -e

AGENT_ID="Z6PCEKYNPS"
ALIAS_ID="BRUXPV975I"
REGION="us-east-1"

echo "=================================================="
echo "ACTUALIZAR Y DESPLEGAR Comfi"
echo "=================================================="
echo ""

# 1. Preparar agente (esto crea una nueva versión)
echo "1. Preparando agente (creando nueva versión)..."
PREPARE_OUTPUT=$(aws bedrock-agent prepare-agent \
    --agent-id "$AGENT_ID" \
    --region "$REGION" \
    --output json)

NEW_VERSION=$(echo "$PREPARE_OUTPUT" | jq -r '.agentVersion')
echo "   ✅ Nueva versión creada: $NEW_VERSION"

# 2. Esperar a que la versión esté lista
echo ""
echo "2. Esperando a que la versión esté lista..."
sleep 5

STATUS="CREATING"
ATTEMPTS=0
MAX_ATTEMPTS=30

while [ "$STATUS" != "PREPARED" ] && [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    ATTEMPTS=$((ATTEMPTS + 1))
    
    VERSION_INFO=$(aws bedrock-agent get-agent-version \
        --agent-id "$AGENT_ID" \
        --agent-version "$NEW_VERSION" \
        --region "$REGION" \
        --output json 2>/dev/null || echo '{"agentVersion":{"agentStatus":"CREATING"}}')
    
    STATUS=$(echo "$VERSION_INFO" | jq -r '.agentVersion.agentStatus')
    
    echo "   Intento $ATTEMPTS/$MAX_ATTEMPTS - Status: $STATUS"
    
    if [ "$STATUS" = "PREPARED" ]; then
        break
    fi
    
    sleep 2
done

if [ "$STATUS" != "PREPARED" ]; then
    echo "   ❌ Timeout esperando a que la versión esté lista"
    exit 1
fi

echo "   ✅ Versión lista"

# 3. Actualizar alias para apuntar a la nueva versión
echo ""
echo "3. Actualizando alias '$ALIAS_ID' a versión $NEW_VERSION..."
aws bedrock-agent update-agent-alias \
    --agent-id "$AGENT_ID" \
    --agent-alias-id "$ALIAS_ID" \
    --agent-alias-name "prod" \
    --routing-configuration "agentVersion=$NEW_VERSION" \
    --region "$REGION" \
    --output json > /dev/null

echo "   ✅ Alias actualizado"

echo ""
echo "=================================================="
echo "✅ ACTUALIZACIÓN COMPLETADA"
echo "=================================================="
echo ""
echo "Cambios aplicados:"
echo "  ✅ Nueva versión: $NEW_VERSION"
echo "  ✅ Alias 'prod' actualizado"
echo "  ✅ Identidad: Comfi de Comfama"
echo "  ✅ Contexto: Caja de Compensación Familiar"
echo ""
echo "Prueba AHORA:"
echo "  1. Abre: https://db4aulosarsdo.cloudfront.net"
echo "  2. Recarga la página (Ctrl+R o Cmd+R)"
echo "  3. Pregunta: '¿Qué es Comfama?'"
echo "  4. Debe responder como Comfi de Comfama"
echo ""
