#!/bin/bash

# Script para redesplegar frontend con WebSocket correcto
# Usa el WebSocket de la cuenta actual (777937796305)

set -e

BUCKET="comfi-frontend-pragma"
DISTRIBUTION_ID="E2UWNXJTS2NM3V"

echo "=================================================="
echo "REDEPLOY FRONTEND - WebSocket Correcto"
echo "=================================================="
echo ""

echo "Cuenta actual:"
aws sts get-caller-identity --output json | jq '{Account, Arn}'
echo ""

echo "Nuevo WebSocket:"
echo "  wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod"
echo ""

echo "1. Verificando .env.production..."
if grep -q "vvg621xawg" frontend/.env.production; then
    echo "   ✅ .env.production actualizado correctamente"
else
    echo "   ❌ ERROR: .env.production no tiene el WebSocket correcto"
    exit 1
fi

echo ""
echo "2. Instalando dependencias..."
cd frontend
npm install --silent

echo ""
echo "3. Construyendo frontend..."
npm run build

if [ ! -d "dist" ]; then
    echo "   ❌ ERROR: No se generó la carpeta dist/"
    exit 1
fi

echo "   ✅ Build completado"

echo ""
echo "4. Verificando que el build tiene el WebSocket correcto..."
if grep -r "vvg621xawg" dist/ > /dev/null; then
    echo "   ✅ WebSocket correcto en el build"
else
    echo "   ❌ ERROR: El build no contiene el WebSocket correcto"
    exit 1
fi

echo ""
echo "5. Desplegando a S3..."
aws s3 sync dist/ s3://$BUCKET/ --delete --quiet

if [ $? -eq 0 ]; then
    echo "   ✅ Archivos subidos a S3"
else
    echo "   ❌ ERROR subiendo a S3"
    exit 1
fi

echo ""
echo "6. Invalidando caché de CloudFront..."
INVALIDATION_ID=$(aws cloudfront create-invalidation \
    --distribution-id $DISTRIBUTION_ID \
    --paths "/*" \
    --output json | jq -r '.Invalidation.Id')

if [ -n "$INVALIDATION_ID" ]; then
    echo "   ✅ Invalidación creada: $INVALIDATION_ID"
else
    echo "   ❌ ERROR creando invalidación"
    exit 1
fi

echo ""
echo "=================================================="
echo "✅ DEPLOY COMPLETADO"
echo "=================================================="
echo ""
echo "URL: https://db4aulosarsdo.cloudfront.net"
echo "WebSocket: wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod"
echo ""
echo "IMPORTANTE:"
echo "1. Espera 2-3 minutos para que CloudFront se actualice"
echo "2. Abre en ventana incógnita para evitar caché del navegador"
echo "3. Verifica en DevTools → Network que conecta al WebSocket correcto"
echo ""
echo "Verificar invalidación:"
echo "  aws cloudfront get-invalidation --distribution-id $DISTRIBUTION_ID --id $INVALIDATION_ID"
echo ""
