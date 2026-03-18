#!/bin/bash

echo "=========================================="
echo "TEST DE AUDIO - CENTLI AGENT"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Este script te ayudará a probar el flujo de audio del agente CENTLI"
echo ""

# Menu
echo "Selecciona el tipo de test:"
echo ""
echo "1. Ver logs en tiempo real (todos)"
echo "2. Ver logs de AUDIO solamente"
echo "3. Ver logs de ejecución de TOOLS"
echo "4. Ver logs de ERRORES"
echo "5. Ver logs de TRANSCRIPCIÓN"
echo "6. Abrir frontend para pruebas"
echo "7. Test completo (logs + frontend)"
echo ""
read -p "Opción (1-7): " option

case $option in
    1)
        echo ""
        echo "${GREEN}📊 Mostrando todos los logs en tiempo real...${NC}"
        echo "Presiona Ctrl+C para salir"
        echo ""
        aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
          --follow \
          --profile pragma-power-user
        ;;
    
    2)
        echo ""
        echo "${GREEN}🎤 Mostrando logs de AUDIO...${NC}"
        echo "Presiona Ctrl+C para salir"
        echo ""
        aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
          --follow \
          --profile pragma-power-user \
          --filter-pattern "AUDIO"
        ;;
    
    3)
        echo ""
        echo "${GREEN}🔧 Mostrando logs de ejecución de TOOLS...${NC}"
        echo "Presiona Ctrl+C para salir"
        echo ""
        aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
          --follow \
          --profile pragma-power-user \
          --filter-pattern "Executing tool"
        ;;
    
    4)
        echo ""
        echo "${RED}❌ Mostrando ERRORES...${NC}"
        echo "Presiona Ctrl+C para salir"
        echo ""
        aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
          --follow \
          --profile pragma-power-user \
          --filter-pattern "ERROR"
        ;;
    
    5)
        echo ""
        echo "${GREEN}📝 Mostrando logs de TRANSCRIPCIÓN...${NC}"
        echo "Presiona Ctrl+C para salir"
        echo ""
        aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
          --follow \
          --profile pragma-power-user \
          --filter-pattern "transcribed"
        ;;
    
    6)
        echo ""
        echo "${GREEN}🌐 Abriendo frontend...${NC}"
        echo ""
        echo "URL: http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com"
        echo ""
        echo "Instrucciones:"
        echo "  1. Presiona el botón de micrófono 🎤"
        echo "  2. Di una de estas frases:"
        echo "     • '¿Cuál es mi saldo?'"
        echo "     • 'Envía 500 pesos a mi mamá'"
        echo "     • 'Quiero comprar un iPhone 15 Pro'"
        echo "     • 'Muéstrame mis últimas transacciones'"
        echo "  3. Observa la respuesta del agente"
        echo ""
        
        # Try to open in browser
        if command -v open &> /dev/null; then
            open "http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com"
        else
            echo "Abre manualmente: http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com"
        fi
        ;;
    
    7)
        echo ""
        echo "${GREEN}🚀 Test completo...${NC}"
        echo ""
        echo "1. Abriendo frontend..."
        
        # Open frontend
        if command -v open &> /dev/null; then
            open "http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com"
        fi
        
        echo ""
        echo "2. Esperando 3 segundos..."
        sleep 3
        
        echo ""
        echo "3. Iniciando logs en tiempo real..."
        echo ""
        echo "${YELLOW}Instrucciones:${NC}"
        echo "  • Usa el micrófono en el frontend"
        echo "  • Observa los logs aquí"
        echo "  • Presiona Ctrl+C para salir"
        echo ""
        
        aws logs tail /aws/lambda/poc-wizi-mex-lambda-inference-model-dev \
          --follow \
          --profile pragma-power-user
        ;;
    
    *)
        echo ""
        echo "${RED}Opción inválida${NC}"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
