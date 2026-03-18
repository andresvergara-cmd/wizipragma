#!/bin/bash

# Script de deploy para Lambda centli-app-message
# Incluye validador de identidad y system prompt reforzado

set -e  # Exit on error

echo "=================================================="
echo "DEPLOY: centli-app-message Lambda Function"
echo "=================================================="
echo ""

# Verificar credenciales AWS
echo "1. Verificando credenciales AWS..."
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ ERROR: Credenciales AWS expiradas o no configuradas"
    echo ""
    echo "Por favor ejecuta:"
    echo "  aws sso login --profile pra_pragma_awsconnect_lab"
    echo "o"
    echo "  aws sso login"
    echo ""
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
USER_ARN=$(aws sts get-caller-identity --query Arn --output text)
echo "✅ Credenciales válidas"
echo "   Account: $ACCOUNT_ID"
echo "   User: $USER_ARN"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "bedrock_config.py" ]; then
    echo "❌ ERROR: Debes ejecutar este script desde src_aws/app_inference/"
    exit 1
fi

# Verificar que existe el zip
if [ ! -f "lambda_function.zip" ]; then
    echo "❌ ERROR: No se encontró lambda_function.zip"
    echo "   Ejecuta primero: zip -r lambda_function.zip . -x '*.git*' '*.pytest_cache*' 'tests/*' '*.md' 'frontend/*' 'aidlc-docs/*' '.kiro/*' '.vscode/*' '*.zip'"
    exit 1
fi

echo "2. Verificando archivos en el zip..."
unzip -l lambda_function.zip | grep -E "(bedrock_config|identity_validator|action_tools)" || true
echo ""

# Deploy a Lambda
echo "3. Desplegando a Lambda..."
aws lambda update-function-code \
    --function-name centli-app-message \
    --zip-file fileb://lambda_function.zip \
    --output json > /tmp/lambda_deploy.json

echo "✅ Deploy iniciado"
echo ""

# Esperar a que termine
echo "4. Esperando a que termine el deploy..."
sleep 5

# Verificar estado
STATUS=$(aws lambda get-function \
    --function-name centli-app-message \
    --query 'Configuration.LastUpdateStatus' \
    --output text)

echo "   Estado: $STATUS"
echo ""

if [ "$STATUS" = "Successful" ]; then
    echo "=================================================="
    echo "✅ DEPLOY EXITOSO"
    echo "=================================================="
    echo ""
    echo "Cambios desplegados:"
    echo "  ✅ System prompt reforzado (bedrock_config.py)"
    echo "  ✅ Validador de identidad (identity_validator.py)"
    echo "  ✅ FAQs de Comfama (action_tools.py)"
    echo ""
    echo "Próximos pasos:"
    echo "  1. Probar en: https://db4aulosarsdo.cloudfront.net"
    echo "  2. Preguntar: '¿Cómo me afilio a Comfama?'"
    echo "  3. Verificar que NO mencione Carlos o México"
    echo "  4. Monitorear logs en CloudWatch"
    echo ""
    echo "Logs:"
    echo "  aws logs tail /aws/lambda/centli-app-message --follow"
    echo ""
elif [ "$STATUS" = "InProgress" ]; then
    echo "⏳ Deploy aún en progreso..."
    echo "   Espera 10-15 segundos y verifica con:"
    echo "   aws lambda get-function --function-name centli-app-message --query 'Configuration.LastUpdateStatus'"
else
    echo "❌ Deploy falló con estado: $STATUS"
    echo ""
    echo "Revisa los detalles en /tmp/lambda_deploy.json"
    cat /tmp/lambda_deploy.json
    exit 1
fi
