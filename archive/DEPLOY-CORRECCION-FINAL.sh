#!/bin/bash

# Script de Deployment - Corrección Final Bug Mensajes Desaparecen
# Fecha: 13 de marzo de 2026

set -e  # Exit on error

echo "🚀 Iniciando deployment de corrección..."
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Variables
BUCKET="comfi-frontend-pragma"
DISTRIBUTION_ID="E2UWNXJTS2NM3V"
FRONTEND_DIR="frontend"

# Verificar que estamos en el directorio correcto
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ Error: Directorio frontend/ no encontrado${NC}"
    echo "Por favor ejecuta este script desde la raíz del proyecto"
    exit 1
fi

# Verificar credenciales AWS
echo "🔐 Verificando credenciales AWS..."
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Credenciales AWS no válidas${NC}"
    echo "Por favor configura tus credenciales AWS primero"
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✅ Credenciales válidas - Account: $ACCOUNT_ID${NC}"
echo ""

# Build del frontend
ech