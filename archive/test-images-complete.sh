#!/bin/bash

echo "=========================================="
echo "TEST COMPLETO DE IMÁGENES - CENTLI"
echo "=========================================="
echo ""

# Test 1: Verificar S3
echo "[1/4] Verificando S3 (vía AWS CLI)..."
S3_HASH=$(aws s3 cp s3://poc-wizi-mex-front/index.html - --profile pragma-power-user 2>/dev/null | grep -o 'assets/index-[^"]*\.js')
if [ -z "$S3_HASH" ]; then
    echo "❌ ERROR: No se pudo leer S3. Verifica tu sesión AWS."
    echo "Ejecuta: aws sso login --profile pragma-power-user"
    exit 1
fi
echo "✅ S3 tiene: $S3_HASH"
echo ""

# Test 2: Verificar contenido del JS en S3
echo "[2/4] Verificando imágenes en archivo JS..."
IMAGE_COUNT=$(aws s3 cp s3://poc-wizi-mex-front/assets/$S3_HASH - --profile pragma-power-user 2>/dev/null | grep -o 'dummyimage.com' | wc -l | tr -d ' ')
if [ "$IMAGE_COUNT" -ge 8 ]; then
    echo "✅ Encontradas $IMAGE_COUNT referencias a dummyimage.com"
else
    echo "⚠️  Solo se encontraron $IMAGE_COUNT referencias (esperadas: 8+)"
fi
echo ""

# Test 3: Verificar S3 Website Endpoint
echo "[3/4] Verificando S3 Website Endpoint..."
S3_WEB_HASH=$(curl -s "http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com/" | grep -o 'assets/index-[^"]*\.js')
if [ -z "$S3_WEB_HASH" ]; then
    echo "⚠️  No se pudo acceder al website endpoint de S3"
else
    echo "✅ S3 Website sirve: $S3_WEB_HASH"
fi
echo ""

# Test 4: Verificar CloudFront
echo "[4/4] Verificando CloudFront..."
CF_HASH=$(curl -s "https://d210pgg1e91kn6.cloudfront.net/?t=$(date +%s)" | grep -o 'assets/index-[^"]*\.js')
if [ -z "$CF_HASH" ]; then
    echo "❌ ERROR: No se pudo acceder a CloudFront"
else
    echo "CloudFront sirve: $CF_HASH"
fi
echo ""

# Comparación final
echo "=========================================="
echo "RESULTADO FINAL"
echo "=========================================="
echo ""

if [ "$S3_HASH" == "$CF_HASH" ]; then
    echo "✅ ¡ÉXITO! CloudFront sirve la versión correcta"
    echo ""
    echo "Las imágenes deberían mostrarse ahora en:"
    echo "  🌐 https://d210pgg1e91kn6.cloudfront.net/marketplace"
    echo ""
    echo "Si aún ves imágenes rotas:"
    echo "  1. Cierra TODAS las pestañas del navegador"
    echo "  2. Abre ventana de incógnito"
    echo "  3. Refresca con Ctrl+Shift+R (o Cmd+Shift+R en Mac)"
    echo "  4. Limpia cache del navegador"
else
    echo "⏳ CloudFront aún tiene cache antiguo"
    echo ""
    echo "Versiones:"
    echo "  S3:         $S3_HASH ✅"
    echo "  CloudFront: $CF_HASH ❌"
    echo ""
    echo "SOLUCIÓN TEMPORAL - Usa S3 directamente:"
    echo "  🌐 http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com"
    echo ""
    echo "Acciones:"
    echo "  1. Espera 2-5 minutos más"
    echo "  2. Ejecuta este script nuevamente"
    echo "  3. O usa la URL de S3 arriba (funciona inmediatamente)"
fi

echo ""
echo "=========================================="
echo ""
echo "Última invalidación: I37Q8FBNAB0CRWSKIBPFP3VY23"
echo "Hora: $(date)"
echo ""
