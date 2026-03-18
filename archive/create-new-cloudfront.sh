#!/bin/bash

echo "=========================================="
echo "CREAR NUEVA DISTRIBUCIÓN CLOUDFRONT"
echo "=========================================="
echo ""

# Crear configuración para nueva distribución
cat > new-cloudfront-config.json <<'EOF'
{
  "CallerReference": "centli-frontend-2026-02-19",
  "Comment": "CENTLI Frontend - Optimized Cache",
  "Enabled": true,
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "S3-poc-wizi-mex-front",
        "DomainName": "poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com",
        "CustomOriginConfig": {
          "HTTPPort": 80,
          "HTTPSPort": 443,
          "OriginProtocolPolicy": "http-only",
          "OriginSslProtocols": {
            "Quantity": 1,
            "Items": ["TLSv1.2"]
          }
        }
      }
    ]
  },
  "DefaultRootObject": "index.html",
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-poc-wizi-mex-front",
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": {
      "Quantity": 2,
      "Items": ["GET", "HEAD"],
      "CachedMethods": {
        "Quantity": 2,
        "Items": ["GET", "HEAD"]
      }
    },
    "Compress": true,
    "MinTTL": 0,
    "DefaultTTL": 300,
    "MaxTTL": 3600,
    "ForwardedValues": {
      "QueryString": false,
      "Cookies": {
        "Forward": "none"
      }
    },
    "TrustedSigners": {
      "Enabled": false,
      "Quantity": 0
    }
  },
  "CacheBehaviors": {
    "Quantity": 1,
    "Items": [
      {
        "PathPattern": "/assets/*",
        "TargetOriginId": "S3-poc-wizi-mex-front",
        "ViewerProtocolPolicy": "redirect-to-https",
        "AllowedMethods": {
          "Quantity": 2,
          "Items": ["GET", "HEAD"],
          "CachedMethods": {
            "Quantity": 2,
            "Items": ["GET", "HEAD"]
          }
        },
        "Compress": true,
        "MinTTL": 0,
        "DefaultTTL": 86400,
        "MaxTTL": 31536000,
        "ForwardedValues": {
          "QueryString": false,
          "Cookies": {
            "Forward": "none"
          }
        },
        "TrustedSigners": {
          "Enabled": false,
          "Quantity": 0
        }
      }
    ]
  },
  "CustomErrorResponses": {
    "Quantity": 1,
    "Items": [
      {
        "ErrorCode": 404,
        "ResponsePagePath": "/index.html",
        "ResponseCode": "200",
        "ErrorCachingMinTTL": 300
      }
    ]
  },
  "PriceClass": "PriceClass_100"
}
EOF

echo "Creando nueva distribución de CloudFront..."
echo ""
echo "Configuración:"
echo "  • Origin: S3 Website Endpoint"
echo "  • HTML: Cache 5 minutos"
echo "  • Assets: Cache 24 horas"
echo "  • HTTPS: Habilitado"
echo "  • Compresión: Habilitada"
echo ""

RESULT=$(aws cloudfront create-distribution \
  --distribution-config file://new-cloudfront-config.json \
  --profile pragma-power-user \
  --output json)

if [ $? -eq 0 ]; then
    DIST_ID=$(echo "$RESULT" | jq -r '.Distribution.Id')
    DOMAIN=$(echo "$RESULT" | jq -r '.Distribution.DomainName')
    
    echo "✅ Distribución creada exitosamente"
    echo ""
    echo "ID: $DIST_ID"
    echo "URL: https://$DOMAIN"
    echo ""
    echo "⚠️  IMPORTANTE:"
    echo "  • La distribución tarda 15-20 minutos en estar lista"
    echo "  • Estado: Deploying → Deployed"
    echo "  • Usa esta URL en lugar de la anterior"
    echo ""
    echo "Verificar estado:"
    echo "  aws cloudfront get-distribution --id $DIST_ID --profile pragma-power-user --query 'Distribution.Status'"
    echo ""
    
    rm new-cloudfront-config.json
else
    echo "❌ Error creando distribución"
    rm new-cloudfront-config.json
    exit 1
fi

echo "=========================================="
