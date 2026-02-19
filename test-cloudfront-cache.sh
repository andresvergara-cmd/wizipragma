#!/bin/bash

echo "=================================="
echo "TEST DE CACHE DE CLOUDFRONT"
echo "=================================="
echo ""

# Test 1: Verificar CloudFront
echo "[1/3] Verificando CloudFront..."
CF_HASH=$(curl -s "https://d210pgg1e91kn6.cloudfront.net/?t=$(date +%s)" | grep -o 'assets/index-[^"]*\.js')
echo "CloudFront sirve: $CF_HASH"
echo ""

# Test 2: Verificar S3
echo "[2/3] Verificando S3..."
S3_HASH=$(aws s3 cp s3://poc-wizi-mex-front/index.html - --profile pragma-power-user 2>/dev/null | grep -o 'assets/index-[^"]*\.js')
if [ -z "$S3_HASH" ]; then
    echo "ERROR: No se pudo leer S3. Verifica tu sesion AWS."
    echo "Ejecuta: aws sso login --profile pragma-power-user"
    exit 1
fi
echo "S3 tiene: $S3_HASH"
echo ""

# Test 3: Comparar
echo "[3/3] Comparando versiones..."
if [ "$S3_HASH" == "$CF_HASH" ]; then
    echo "✅ CORRECTO: CloudFront sirve la version correcta"
    echo ""
    echo "Las imagenes deberian mostrarse ahora."
    echo "URL: https://d210pgg1e91kn6.cloudfront.net/marketplace"
    echo ""
    echo "Si aun ves imagenes rotas:"
    echo "  1. Cierra TODAS las pestañas"
    echo "  2. Abre ventana de incognito"
    echo "  3. Refresca con Ctrl+Shift+R"
else
    echo "❌ ERROR: CloudFront sirve version antigua"
    echo ""
    echo "S3:         $S3_HASH"
    echo "CloudFront: $CF_HASH"
    echo ""
    echo "Acciones:"
    echo "  1. Espera 2-5 minutos mas"
    echo "  2. Ejecuta este script nuevamente"
    echo "  3. CloudFront tarda en propagarse"
fi

echo ""
echo "=================================="
