#!/bin/bash

# Script para corregir el prompt de identidad de Comfi
# Fecha: 2026-03-13

set -e

echo "🔧 Corrigiendo prompt de identidad de Comfi..."
echo ""

# Variables
LAMBDA_NAME="centli-app-message"
REGION="us-east-1"

# 1. Empaquetar código actualizado
echo "📦 Empaquetando código actualizado..."
cd src_aws/app_inference
zip -r ../../lambda-inference-update.zip . -x "*.pyc" -x "__pycache__/*" -x "*.git*"
cd ../..

# 2. Actualizar Lambda
echo "🚀 Actualizando Lambda ${LAMBDA_NAME}..."
aws lambda update-function-code \
    --function-name ${LAMBDA_NAME} \
    --zip-file fileb://lambda-inference-update.zip \
    --region ${REGION}

echo ""
echo "⏳ Esperando a que la función se actualice..."
aws lambda wait function-updated \
    --function-name ${LAMBDA_NAME} \
    --region ${REGION}

# 3. Limpiar
echo "🧹 Limpiando archivos temporales..."
rm lambda-inference-update.zip

echo ""
echo "✅ Deploy completado exitosamente"
echo ""
echo "Cambios aplicados:"
echo "  • System prompt actualizado con instrucciones claras sobre identidad"
echo "  • Agregadas preguntas FAQ sobre identidad de Comfi"
echo "  • Instrucciones para responder directamente preguntas sobre 'quién eres'"
echo ""
echo "Prueba preguntando: '¿Quién eres?'"
