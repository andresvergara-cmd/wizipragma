#!/bin/bash

echo "=========================================="
echo "SOLUCIÓN DEFINITIVA - CloudFront Cache"
echo "=========================================="
echo ""

# Paso 1: Obtener configuración actual
echo "[1/3] Obteniendo configuración actual de CloudFront..."
aws cloudfront get-distribution-config \
  --id E29CTPS84NA5BZ \
  --profile pragma-power-user \
  --output json > cloudfront-config.json

if [ $? -ne 0 ]; then
    echo "❌ Error obteniendo configuración"
    exit 1
fi

ETAG=$(jq -r '.ETag' cloudfront-config.json)
echo "✅ ETag: $ETAG"
echo ""

# Paso 2: Modificar configuración
echo "[2/3] Modificando configuración de cache..."
jq '.DistributionConfig.DefaultCacheBehavior.MinTTL = 0 |
    .DistributionConfig.DefaultCacheBehavior.DefaultTTL = 300 |
    .DistributionConfig.DefaultCacheBehavior.MaxTTL = 3600' \
    cloudfront-config.json | jq '.DistributionConfig' > cloudfront-config-new.json

echo "Nuevos valores:"
echo "  MinTTL: 0"
echo "  DefaultTTL: 300 (5 minutos)"
echo "  MaxTTL: 3600 (1 hora)"
echo ""

# Paso 3: Aplicar cambios
echo "[3/3] Aplicando cambios a CloudFront..."
aws cloudfront update-distribution \
  --id E29CTPS84NA5BZ \
  --distribution-config file://cloudfront-config-new.json \
  --if-match "$ETAG" \
  --profile pragma-power-user \
  --output json > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Configuración actualizada exitosamente"
    echo ""
    echo "Cambios aplicados:"
    echo "  • Cache reducido de 24 horas a 5 minutos"
    echo "  • Futuros deploys se propagarán en ~5 minutos"
    echo "  • Invalidaciones serán más efectivas"
    echo ""
    echo "⚠️  NOTA: Los cambios tardan 15-20 minutos en propagarse"
    echo ""
    
    # Limpiar archivos temporales
    rm cloudfront-config.json cloudfront-config-new.json
    
    # Crear nueva invalidación
    echo "Creando nueva invalidación..."
    aws cloudfront create-invalidation \
      --distribution-id E29CTPS84NA5BZ \
      --paths "/*" \
      --profile pragma-power-user \
      --query 'Invalidation.Id' \
      --output text
    
    echo ""
    echo "✅ SOLUCIÓN APLICADA"
else
    echo "❌ Error aplicando cambios"
    rm cloudfront-config.json cloudfront-config-new.json
    exit 1
fi

echo ""
echo "=========================================="
