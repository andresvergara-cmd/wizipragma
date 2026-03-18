#!/bin/bash

# Script para agregar permisos de Amazon Transcribe al rol de Lambda

set -e

echo "🔐 Agregando permisos de Amazon Transcribe"
echo "==========================================="
echo ""

ROLE_NAME="CentliLambdaExecutionRole"
POLICY_NAME="CentliTranscribePolicy"
REGION="us-east-1"

# Crear política JSON
cat > /tmp/transcribe-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "transcribe:DeleteTranscriptionJob",
        "transcribe:ListTranscriptionJobs"
      ],
      "Resource": "*"
    }
  ]
}
EOF

echo "📄 Política creada:"
cat /tmp/transcribe-policy.json
echo ""

# Aplicar política al rol
echo "🔧 Aplicando política al rol: $ROLE_NAME"
aws iam put-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name "$POLICY_NAME" \
  --policy-document file:///tmp/transcribe-policy.json \
  --region "$REGION"

echo "✅ Política aplicada exitosamente"
echo ""

# Verificar
echo "🔍 Verificando políticas del rol:"
aws iam list-role-policies \
  --role-name "$ROLE_NAME" \
  --region "$REGION" \
  --output table

echo ""
echo "==========================================="
echo "✅ Permisos de Transcribe agregados"
echo "==========================================="
echo ""
echo "El rol ahora tiene permisos para:"
echo "  - StartTranscriptionJob"
echo "  - GetTranscriptionJob"
echo "  - DeleteTranscriptionJob"
echo "  - ListTranscriptionJobs"
echo ""

# Limpiar
rm -f /tmp/transcribe-policy.json
