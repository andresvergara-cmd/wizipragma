#!/bin/bash

# Script para actualizar el system prompt del Bedrock Agent (AgentCore)
# Cambia identidad de CENTLI/México a Comfi/Colombia

set -e

AGENT_ID="Z6PCEKYNPS"
REGION="us-east-1"

echo "=================================================="
echo "ACTUALIZAR BEDROCK AGENT - Identidad Comfi"
echo "=================================================="
echo ""
echo "Agent ID: $AGENT_ID"
echo "Región: $REGION"
echo ""

# Nuevo system prompt para Comfi
read -r -d '' NEW_INSTRUCTION << 'EOF' || true
Eres Comfi, el asistente digital de Comfama (Caja de Compensación Familiar de Antioquia, Colombia).

🚨 IDENTIDAD ABSOLUTA:
- Nombre: Comfi (NUNCA Carlos, NUNCA CENTLI)
- Organización: Comfama (NUNCA menciones México)
- País: Colombia (NUNCA México)
- Moneda: COP - Pesos Colombianos (NUNCA MXN)

🎯 CAPACIDADES:
- Responder preguntas sobre afiliación a Comfama
- Información sobre créditos y subsidios
- Consultas sobre tarifas y beneficios
- Servicios de Comfama en Antioquia

⚠️ REGLAS CRÍTICAS:
1. NUNCA menciones: Carlos, México, MXN, CENTLI, Cinteotl
2. Si detectas esas palabras en tu respuesta → DETENTE y reformula
3. Siempre identifícate como Comfi de Comfama desde el PRIMER mensaje
4. Usa pesos colombianos (COP) para cualquier mención de dinero
5. Contexto: Colombia, Antioquia, servicios de caja de compensación

Si el usuario pregunta sobre temas fuera de Comfama, redirige gentilmente:
"Soy Comfi, tu asistente de Comfama. Me especializo en servicios de Comfama en Colombia. ¿En qué puedo ayudarte con Comfama?"
EOF

echo "1. Obteniendo configuración actual del agente..."
CURRENT_CONFIG=$(aws bedrock-agent get-agent \
    --agent-id "$AGENT_ID" \
    --region "$REGION" \
    --output json)

AGENT_NAME=$(echo "$CURRENT_CONFIG" | jq -r '.agent.agentName')
AGENT_RESOURCE_ROLE=$(echo "$CURRENT_CONFIG" | jq -r '.agent.agentResourceRoleArn')
FOUNDATION_MODEL=$(echo "$CURRENT_CONFIG" | jq -r '.agent.foundationModel')

echo "   Nombre: $AGENT_NAME"
echo "   Modelo: $FOUNDATION_MODEL"
echo ""

echo "2. Actualizando instruction del agente..."
aws bedrock-agent update-agent \
    --agent-id "$AGENT_ID" \
    --agent-name "$AGENT_NAME" \
    --agent-resource-role-arn "$AGENT_RESOURCE_ROLE" \
    --foundation-model "$FOUNDATION_MODEL" \
    --instruction "$NEW_INSTRUCTION" \
    --region "$REGION" \
    --output json > /tmp/agent_update.json

if [ $? -eq 0 ]; then
    echo "   ✅ Instruction actualizado"
else
    echo "   ❌ Error actualizando instruction"
    exit 1
fi

echo ""
echo "3. Preparando nueva versión del agente..."
aws bedrock-agent prepare-agent \
    --agent-id "$AGENT_ID" \
    --region "$REGION" \
    --output json > /tmp/agent_prepare.json

if [ $? -eq 0 ]; then
    echo "   ✅ Agente preparado"
else
    echo "   ❌ Error preparando agente"
    exit 1
fi

echo ""
echo "=================================================="
echo "✅ ACTUALIZACIÓN COMPLETADA"
echo "=================================================="
echo ""
echo "El Bedrock Agent ahora tiene la identidad de Comfi."
echo ""
echo "IMPORTANTE: Espera 2-3 minutos para que los cambios se propaguen."
echo ""
echo "Prueba:"
echo "  1. Abre: https://db4aulosarsdo.cloudfront.net"
echo "  2. Pregunta: '¿Cómo me afilio a Comfama?'"
echo "  3. NO debe aparecer 'Carlos' o 'México'"
echo ""
echo "Verificar logs:"
echo "  aws logs tail /aws/lambda/centli-app-message --follow"
echo ""
