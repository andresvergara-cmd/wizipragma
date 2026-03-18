#!/bin/bash

# Deploy Script para Comfi con Sistema FAQ
# Fecha: 2024-03-12
# Incluye: Renombrado CENTLI → Comfi + Sistema FAQ completo

set -e

echo "🚀 Deploy Comfi con Sistema FAQ"
echo "================================"
echo ""

# Variables
S3_BUCKET="poc-wizi-mex-front"
CLOUDFRONT_DIST="E29CTPS84NA5BZ"
BUILD_DIR="frontend/dist"

# Verificar que el build existe
if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ Error: No se encontró el directorio $BUILD_DIR"
    echo "   Ejecuta primero: cd frontend && npm run build"
    exit 1
fi

echo "✅ Build encontrado en $BUILD_DIR"
echo ""

# Mostrar archivos a subir
echo "📦 Archivos a subir:"
ls -lh $BUILD_DIR
echo ""

# Confirmar deploy
read -p "¿Deseas continuar con el deploy a S3? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deploy cancelado"
    exit 1
fi

echo ""
echo "📤 Subiendo archivos a S3..."
echo ""

# Subir archivos a S3
aws s3 sync $BUILD_DIR s3://$S3_BUCKET/ \
    --delete \
    --cache-control "public, max-age=31536000" \
    --exclude "*.html" \
    --exclude "*.json"

# Subir HTML sin cache
aws s3 sync $BUILD_DIR s3://$S3_BUCKET/ \
    --cache-control "no-cache, no-store, must-revalidate" \
    --exclude "*" \
    --include "*.html" \
    --include "*.json"

echo ""
echo "✅ Archivos subidos a S3"
echo ""

# Invalidar CloudFront
echo "🔄 Invalidando caché de CloudFront..."
INVALIDATION_ID=$(aws cloudfront create-invalidation \
    --distribution-id $CLOUDFRONT_DIST \
    --paths "/*" \
    --query 'Invalidation.Id' \
    --output text)

echo "✅ Invalidación creada: $INVALIDATION_ID"
echo ""

# Esperar invalidación (opcional)
read -p "¿Deseas esperar a que complete la invalidación? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⏳ Esperando invalidación..."
    aws cloudfront wait invalidation-completed \
        --distribution-id $CLOUDFRONT_DIST \
        --id $INVALIDATION_ID
    echo "✅ Invalidación completada"
fi

echo ""
echo "🎉 Deploy completado exitosamente!"
echo ""
echo "📊 Resumen del Deploy:"
echo "   • Frontend: Comfi con Sistema FAQ"
echo "   • S3 Bucket: $S3_BUCKET"
echo "   • CloudFront: $CLOUDFRONT_DIST"
echo "   • URL: https://d210pgg1e91kn6.cloudfront.net/"
echo ""
echo "🔍 Cambios incluidos:"
echo "   ✅ Renombrado CENTLI → Comfi"
echo "   ✅ Contexto Comfama (Colombia)"
echo "   ✅ Moneda COP"
echo "   ✅ 4 componentes FAQ React"
echo "   ✅ 5 Quick Actions FAQ"
echo "   ✅ Integración ChatWidget"
echo ""
echo "⚠️  Nota: Para ver FAQCards funcionando necesitas:"
echo "   1. Deploy del backend actualizado a Lambda"
echo "   2. Backend con tool answer_faq"
echo "   3. WebSocket conectado"
echo ""
echo "📝 Siguiente paso: Deploy del backend"
echo "   Ver: INSTRUCCIONES-DEPLOY-BACKEND.md"
echo ""
