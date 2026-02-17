#!/bin/bash

# CENTLI - Script de Verificación de Deployment
# Verifica que todos los componentes estén desplegados correctamente

echo "🔍 CENTLI - Verificación de Deployment"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# URLs
FRONTEND_URL="http://centli-frontend-prod.s3-website-us-east-1.amazonaws.com"
TEST_URL="http://centli-frontend-prod.s3-website-us-east-1.amazonaws.com/test.html"
WS_URL="wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod"

echo "📦 Verificando S3 Bucket..."
aws s3 ls s3://centli-frontend-prod/ --profile pragma-power-user > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ S3 Bucket accesible${NC}"
    
    # Check files
    echo ""
    echo "📄 Archivos en S3:"
    aws s3 ls s3://centli-frontend-prod/ --recursive --profile pragma-power-user | grep -E '\.(html|js|css)$' | awk '{print "   " $4 " (" $3 " bytes)"}'
else
    echo -e "${RED}❌ No se puede acceder al S3 Bucket${NC}"
fi

echo ""
echo "🌐 URLs de Producción:"
echo "   Frontend: $FRONTEND_URL"
echo "   Test:     $TEST_URL"
echo "   WebSocket: $WS_URL"

echo ""
echo "🧪 Verificando Frontend..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL")
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Frontend accesible (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}❌ Frontend no accesible (HTTP $HTTP_CODE)${NC}"
fi

echo ""
echo "🧪 Verificando Página de Test..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$TEST_URL")
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Página de test accesible (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}❌ Página de test no accesible (HTTP $HTTP_CODE)${NC}"
fi

echo ""
echo "📊 Build Info:"
if [ -f "frontend/dist/index.html" ]; then
    echo -e "${GREEN}✅ Build local existe${NC}"
    echo "   Archivos:"
    ls -lh frontend/dist/assets/*.js 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'
    ls -lh frontend/dist/assets/*.css 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'
else
    echo -e "${YELLOW}⚠️  No hay build local${NC}"
fi

echo ""
echo "🔧 Variables de Entorno:"
if [ -f "frontend/.env.production" ]; then
    echo -e "${GREEN}✅ .env.production existe${NC}"
    echo "   Contenido:"
    grep -v '^#' frontend/.env.production | grep -v '^$' | sed 's/^/   /'
else
    echo -e "${RED}❌ .env.production no existe${NC}"
fi

echo ""
echo "📝 Documentación:"
docs=("CHAT-FIX-REPORT.md" "FRONTEND-STATUS.md" "INTEGRATION-GUIDE.md" "DEPLOYMENT-SUCCESS.md")
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}✅ $doc${NC}"
    else
        echo -e "${RED}❌ $doc${NC}"
    fi
done

echo ""
echo "========================================"
echo "✨ Verificación completada"
echo ""
echo "🚀 Para probar:"
echo "   1. Abrir: $TEST_URL"
echo "   2. Verificar conexión WebSocket"
echo "   3. Enviar mensaje de prueba"
echo ""
