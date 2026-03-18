#!/bin/bash

echo "=========================================="
echo "MONITOREANDO CLOUDFRONT"
echo "=========================================="
echo ""
echo "Hora inicio: $(date)"
echo ""

while true; do
    # Verificar estado de distribución
    STATUS=$(aws cloudfront get-distribution --id E29CTPS84NA5BZ --profile pragma-power-user --query 'Distribution.Status' --output text 2>/dev/null)
    
    echo "[$(date +%H:%M:%S)] Estado CloudFront: $STATUS"
    
    if [ "$STATUS" == "Deployed" ]; then
        echo ""
        echo "✅ CloudFront está DEPLOYED"
        echo ""
        
        # Verificar si sirve la versión correcta
        echo "Verificando versión..."
        ./test-images-complete.sh
        
        break
    fi
    
    echo "  ⏳ Esperando 3 minutos..."
    sleep 180
done

echo ""
echo "=========================================="
echo "MONITOREO COMPLETADO"
echo "=========================================="
