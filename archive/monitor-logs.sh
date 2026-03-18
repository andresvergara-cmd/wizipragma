#!/bin/bash

# Script para monitorear logs de Lambda en tiempo real
# Muestra los logs de centli-app-message con colores

set -e

LAMBDA_FUNCTION="centli-app-message"
REGION="us-east-1"

echo "📊 Monitoreando logs de Lambda: $LAMBDA_FUNCTION"
echo "=================================================="
echo ""
echo "Presiona Ctrl+C para detener"
echo ""

# Obtener el log group
LOG_GROUP="/aws/lambda/$LAMBDA_FUNCTION"

# Tail logs en tiempo real
aws logs tail "$LOG_GROUP" \
  --region "$REGION" \
  --follow \
  --format short \
  --since 1m
