#!/bin/bash

# Pre-Demo Checklist - CENTLI Tool Use
# Ejecuta este script antes de grabar para verificar que todo esté listo

echo "🎬 CENTLI Pre-Demo Checklist"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
LAMBDA_NAME="poc-wizi-mex-lambda-inference-model-dev"
AWS_PROFILE="pragma-power-user"
REGION="us-east-1"
FRONTEND_URL="https://d210pgg1e91kn6.cloudfront.net"
WS_URL="wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"

# Check 1: Lambda Updated
echo "1️⃣  Verificando Lambda actualizado..."
LAST_MODIFIED=$(aws lambda get-function \
    --function-name $LAMBDA_NAME \
    --profile $AWS_PROFILE \
    --region $REGION \
    --query 'Configuration.LastModified' \
    --output text 2>/dev/null)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Lambda encontrado${NC}"
    echo "   Última modificación: $LAST_MODIFIED"
    
    # Check if it's recent (within last hour)
    LAST_MODIFIED_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${LAST_MODIFIED:0:19}" "+%s" 2>/dev/null)
    NOW_EPOCH=$(date "+%s")
    DIFF=$((NOW_EPOCH - LAST_MODIFIED_EPOCH))
    
    if [ $DIFF -lt 3600 ]; then
        echo -e "${GREEN}   ✅ Lambda actualizado recientemente (hace $((DIFF/60)) minutos)${NC}"
    else
        echo -e "${YELLOW}   ⚠️  Lambda no actualizado recientemente (hace $((DIFF/3600)) horas)${NC}"
        echo "   Considera re-desplegar: ./deploy-tool-use-fix.sh"
    fi
else
    echo -e "${RED}❌ Error verificando Lambda${NC}"
fi
echo ""

# Check 2: Lambda Logs
echo "2️⃣  Verificando logs recientes de Lambda..."
RECENT_LOGS=$(aws logs tail /aws/lambda/$LAMBDA_NAME \
    --since 5m \
    --profile $AWS_PROFILE \
    --region $REGION 2>/dev/null | grep -c "Tool use")

if [ $RECENT_LOGS -gt 0 ]; then
    echo -e "${GREEN}✅ Lambda procesando Tool Use correctamente${NC}"
    echo "   Eventos de Tool Use en últimos 5 min: $RECENT_LOGS"
else
    echo -e "${YELLOW}⚠️  No hay actividad reciente de Tool Use${NC}"
    echo "   Esto es normal si no has probado recientemente"
fi
echo ""

# Check 3: Frontend Accessible
echo "3️⃣  Verificando acceso al frontend..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $FRONTEND_URL)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Frontend accesible${NC}"
    echo "   URL: $FRONTEND_URL"
else
    echo -e "${RED}❌ Frontend no accesible (HTTP $HTTP_CODE)${NC}"
fi
echo ""

# Check 4: WebSocket Endpoint
echo "4️⃣  Verificando WebSocket endpoint..."
WS_CHECK=$(aws apigatewayv2 get-apis \
    --profile $AWS_PROFILE \
    --region $REGION \
    --query "Items[?Name=='poc-wizi-mex-websocket-api-dev'].ApiEndpoint" \
    --output text 2>/dev/null)

if [ ! -z "$WS_CHECK" ]; then
    echo -e "${GREEN}✅ WebSocket API encontrado${NC}"
    echo "   Endpoint: $WS_CHECK"
else
    echo -e "${YELLOW}⚠️  No se pudo verificar WebSocket API${NC}"
fi
echo ""

# Check 5: DynamoDB Tables
echo "5️⃣  Verificando tablas DynamoDB..."
TABLES=("poc-wizi-mex-user-profile-dev" "poc-wizi-mex-transactions-dev" "poc-wizi-mex-retailers-dev")
ALL_TABLES_OK=true

for TABLE in "${TABLES[@]}"; do
    TABLE_STATUS=$(aws dynamodb describe-table \
        --table-name $TABLE \
        --profile $AWS_PROFILE \
        --region $REGION \
        --query 'Table.TableStatus' \
        --output text 2>/dev/null)
    
    if [ "$TABLE_STATUS" = "ACTIVE" ]; then
        echo -e "${GREEN}   ✅ $TABLE: ACTIVE${NC}"
    else
        echo -e "${RED}   ❌ $TABLE: $TABLE_STATUS${NC}"
        ALL_TABLES_OK=false
    fi
done
echo ""

# Check 6: Test User Data
echo "6️⃣  Verificando datos del usuario de prueba..."
USER_DATA=$(aws dynamodb get-item \
    --table-name poc-wizi-mex-user-profile-dev \
    --key '{"user_id": {"S": "simple-user"}}' \
    --profile $AWS_PROFILE \
    --region $REGION \
    --query 'Item.name.S' \
    --output text 2>/dev/null)

if [ "$USER_DATA" = "Carlos Rodríguez" ]; then
    echo -e "${GREEN}✅ Usuario de prueba encontrado: $USER_DATA${NC}"
else
    echo -e "${RED}❌ Usuario de prueba no encontrado${NC}"
fi
echo ""

# Summary
echo "================================"
echo "📋 RESUMEN"
echo "================================"
echo ""

# Quick Test
echo "7️⃣  Ejecutando prueba rápida..."
echo ""
echo "Probando transferencia..."
python3 test-transfer-only.py > /tmp/test-output.txt 2>&1 &
TEST_PID=$!

# Wait for test with timeout
TIMEOUT=15
ELAPSED=0
while kill -0 $TEST_PID 2>/dev/null && [ $ELAPSED -lt $TIMEOUT ]; do
    sleep 1
    ELAPSED=$((ELAPSED + 1))
    echo -n "."
done
echo ""

if grep -q "SUCCESS" /tmp/test-output.txt 2>/dev/null; then
    echo -e "${GREEN}✅ Prueba de transferencia: EXITOSA${NC}"
    grep "TRF-" /tmp/test-output.txt | head -1
else
    echo -e "${RED}❌ Prueba de transferencia: FALLIDA${NC}"
    echo "Ver detalles en: /tmp/test-output.txt"
fi
echo ""

# Final Checklist
echo "================================"
echo "✅ CHECKLIST FINAL"
echo "================================"
echo ""
echo "Antes de grabar, verifica:"
echo ""
echo "[ ] Lambda actualizado y funcionando"
echo "[ ] Frontend accesible en $FRONTEND_URL"
echo "[ ] Hard refresh realizado (Cmd+Shift+R)"
echo "[ ] Chat widget visible"
echo "[ ] Prueba rápida exitosa"
echo "[ ] Micrófono funcionando"
echo "[ ] Software de grabación listo"
echo "[ ] Pantalla limpia (sin notificaciones)"
echo "[ ] Script de demo leído"
echo ""
echo "================================"
echo ""

# Instructions
echo "📝 PRÓXIMOS PASOS:"
echo ""
echo "1. Abre el frontend:"
echo "   $FRONTEND_URL"
echo ""
echo "2. Haz hard refresh:"
echo "   Mac: Cmd+Shift+R"
echo "   Windows: Ctrl+Shift+R"
echo ""
echo "3. Verifica que el chat widget esté visible"
echo ""
echo "4. Sigue el script en: DEMO-SCRIPT-GRABACION.md"
echo ""
echo "5. Mensajes de prueba:"
echo "   - ¿Cuál es mi saldo?"
echo "   - Envía \$500 a mi mamá"
echo "   - Quiero comprar un iPhone 15 Pro"
echo ""
echo "================================"
echo ""
echo "🎬 ¡Listo para grabar!"
echo ""

# Cleanup
rm -f /tmp/test-output.txt
