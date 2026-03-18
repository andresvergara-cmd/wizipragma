#!/bin/bash

# Script para configurar credenciales de AWS de forma segura
# Las credenciales se almacenan en ~/.aws/credentials

echo "🔐 Configuración de Credenciales de AWS"
echo "========================================"
echo ""
echo "Por favor, ingresa las credenciales de AWS:"
echo ""

# Solicitar credenciales
read -p "AWS Access Key ID: " AWS_ACCESS_KEY_ID
read -p "AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY
read -p "AWS Session Token: " AWS_SESSION_TOKEN

# Configurar región por defecto
AWS_REGION="us-east-1"

echo ""
echo "📝 Configurando credenciales..."

# Crear directorio .aws si no existe
mkdir -p ~/.aws

# Escribir credenciales
cat > ~/.aws/credentials <<EOF
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
aws_session_token = $AWS_SESSION_TOKEN
EOF

# Escribir configuración
cat > ~/.aws/config <<EOF
[default]
region = $AWS_REGION
output = json
EOF

echo "✅ Credenciales configuradas"
echo ""
echo "🧪 Verificando credenciales..."

# Verificar credenciales
if aws sts get-caller-identity > /dev/null 2>&1; then
    echo "✅ Credenciales válidas"
    echo ""
    aws sts get-caller-identity
else
    echo "❌ Error: Credenciales inválidas"
    exit 1
fi

echo ""
echo "✅ Configuración completa"
echo ""
echo "Ahora puedes ejecutar:"
echo "  ./deploy-lambda-fix.sh"
