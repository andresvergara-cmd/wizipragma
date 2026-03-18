#!/bin/bash

# Script para desplegar la corrección de Lambda
# Corrige el error de MaxSpeakerLabels en Transcribe

set -e

echo "🚀 Desplegando Corrección de Lambda"
echo "===================================="
echo ""

# Verificar credenciales
echo "🔐 Verificando credenciales de AWS..."
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ Error: Credenciales de AWS no configuradas"
    echo ""
    echo "Por favor ejecuta primero:"
    echo "  ./configure-aws-credentials.sh"
    exit 1
fi

echo "✅ Credenciales válidas"
echo ""

# Configuración
LAMBDA_FUNCTION="centli-app-message"
REGION="us-east-1"

# Paso 1: Empaquetar Lambda
echo "📦 Paso 1: Empaquetando Lambda..."

# Ir al directorio de la Lambda
cd src_aws/app_message

# Limpiar zips anteriores
rm -f app_message.zip

# Crear nuevo zip (desde dentro del directorio para estructura correcta)
zip -r app_message.zip . \
  -x "*.pyc" \
  -x "__pycache__/*" \
  -x "*.git*" \
  -x "*.zip" > /dev/null

ZIP_SIZE=$(du -h app_message.zip | cut -f1)
echo "✅ Package creado: $ZIP_SIZE"
echo ""

# Paso 2: Desplegar Lambda
echo "🔄 Paso 2: Desplegando a AWS Lambda..."
aws lambda update-function-code \
  --function-name $LAMBDA_FUNCTION \
  --zip-file fileb://app_message.zip \
  --region $REGION \
  --query '{FunctionName: FunctionName, LastModified: LastModified, CodeSize: CodeSize}' \
  --output json

echo ""
echo "✅ Lambda actualizada"
echo ""

# Paso 3: Esperar a que esté lista
echo "⏳ Paso 3: Esperando a que Lambda esté lista..."
aws lambda wait function-updated \
  --function-name $LAMBDA_FUNCTION \
  --region $REGION

echo "✅ Lambda lista"
echo ""

# Limpiar y volver
rm -f app_message.zip
cd ../..

# Resumen
echo "===================================="
echo "✅ Deployment Completado"
echo "===================================="
echo ""
echo "Lambda: $LAMBDA_FUNCTION"
echo "Región: $REGION"
echo ""
echo "🧪 Próximos pasos:"
echo "1. Abrir: https://db4aulosarsdo.cloudfront.net"
echo "2. Click en 🎤"
echo "3. Hablar: 'Hola Comfi'"
echo "4. Click en ⏹️"
echo ""
echo "📊 Monitorear logs:"
echo "  ./monitor-logs.sh"
echo ""
