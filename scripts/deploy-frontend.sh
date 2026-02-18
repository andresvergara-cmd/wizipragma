#!/bin/bash
# Deploy CENTLI Frontend to S3 + CloudFront

BUCKET="centli-frontend-prod"
DISTRIBUTION_ID="E29CTPS84NA5BZ"
PROFILE="pragma-power-user"

echo "🚀 Desplegando CENTLI Frontend..."
echo ""

# Build
echo "📦 Building frontend..."
cd frontend
npm run build

if [ $? -ne 0 ]; then
  echo "❌ Build failed"
  exit 1
fi

echo "✅ Build completed"
echo ""

# Deploy to S3
echo "📤 Uploading to S3..."
aws s3 sync dist/ s3://$BUCKET/ \
  --profile $PROFILE \
  --delete \
  --exclude "test-*.html" \
  --exclude "diagnose*.html"

if [ $? -ne 0 ]; then
  echo "❌ S3 upload failed"
  exit 1
fi

echo "✅ Uploaded to S3"
echo ""

# Invalidate CloudFront cache
echo "🔄 Invalidating CloudFront cache..."
INVALIDATION_ID=$(aws cloudfront create-invalidation \
  --distribution-id $DISTRIBUTION_ID \
  --paths "/*" \
  --profile $PROFILE \
  --query 'Invalidation.Id' \
  --output text)

if [ $? -ne 0 ]; then
  echo "❌ CloudFront invalidation failed"
  exit 1
fi

echo "✅ CloudFront cache invalidated (ID: $INVALIDATION_ID)"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "✅ DESPLIEGUE COMPLETADO"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🌐 URLs:"
echo "  HTTP:  http://$BUCKET.s3-website-us-east-1.amazonaws.com"
echo "  HTTPS: https://d210pgg1e91kn6.cloudfront.net"
echo ""
echo "⏳ Espera 1-2 minutos para que la invalidación se propague"
echo ""
