#!/bin/bash

# Script para desplegar el nuevo diseño Comfama a AWS S3 y CloudFront
# Bucket: poc-wizi-mex-front
# CloudFront Distribution: E29CTPS84NA5BZ
# Fecha: Marzo 12, 2026

echo "🎨 Desplegando nuevo diseño Comfama a producción..."
echo ""

# Navegar a la carpeta del frontend
cd "frontend" || exit

# Construir el proyecto
echo "📦 Construyendo el proyecto..."
npm run build

# Verificar que el build fue exitoso
if [ $? -ne 0 ]; then
    echo "❌ Error en el build. Abortando despliegue."
    exit 1
fi

echo "✅ Build completado exitosamente"
echo ""

# Mostrar archivos generados
echo "📁 Archivos generados en dist/:"
ls -lh dist/

echo ""
echo "🔑 Verificando credenciales de AWS..."

# Verificar credenciales de AWS
aws sts get-caller-identity > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ No se encontraron credenciales de AWS válidas"
    echo ""
    echo "Por favor, configura tus credenciales de AWS:"
    echo "1. Ve a: https://pragmaaws.awsapps.com/start/#/?tab=accounts"
    echo "2. Selecciona la cuenta: pra_hackaton_agentic_mexico (777937796305)"
    echo "3. Copia las credenciales temporales"
    echo "4. Ejecuta: aws configure"
    echo ""
    echo "O sube los archivos manualmente desde la consola de AWS:"
    echo "https://s3.console.aws.amazon.com/s3/buckets/poc-wizi-mex-front"
    exit 1
fi

echo "✅ Credenciales de AWS válidas"
echo ""

# Sincronizar con S3 (elimina archivos viejos)
echo "☁️  Subiendo archivos a S3..."
echo "Bucket: s3://poc-wizi-mex-front/"
echo ""

aws s3 sync dist/ s3://poc-wizi-mex-front/ --delete \
  --cache-control "public, max-age=300" \
  --region us-east-1

# Verificar si el sync fue exitoso
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Archivos subidos exitosamente a S3"
    echo ""
    
    # Crear invalidación de CloudFront
    echo "🔄 Creando invalidación de CloudFront..."
    echo "Distribution ID: E29CTPS84NA5BZ"
    echo ""
    
    INVALIDATION_OUTPUT=$(aws cloudfront create-invalidation \
      --distribution-id E29CTPS84NA5BZ \
      --paths "/*" 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "✅ Invalidación de CloudFront creada exitosamente"
        echo ""
        echo "🎉 ¡Despliegue completado!"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🌐 URL de Producción:"
        echo "   https://d210pgg1e91kn6.cloudfront.net/"
        echo ""
        echo "⏳ Tiempo estimado de propagación:"
        echo "   - S3: Inmediato"
        echo "   - CloudFront: 5-15 minutos"
        echo ""
        echo "🎨 Nuevo diseño Comfama incluye:"
        echo "   ✓ Logo rosa de Comfama"
        echo "   ✓ Hero banner con festival"
        echo "   ✓ Sección de búsqueda"
        echo "   ✓ Beneficios por categorías"
        echo "   ✓ Carrusel de ubicaciones"
        echo "   ✓ FAQ y centro de ayuda"
        echo "   ✓ Sección de aniversario"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
    else
        echo "⚠️  Error al crear la invalidación de CloudFront"
        echo ""
        echo "Puedes crearla manualmente:"
        echo "1. Ve a: https://console.aws.amazon.com/cloudfront/v3/home"
        echo "2. Selecciona la distribución: E29CTPS84NA5BZ"
        echo "3. Ve a la pestaña 'Invalidations'"
        echo "4. Crea una nueva invalidación con el path: /*"
        echo ""
    fi
else
    echo ""
    echo "❌ Error al subir archivos a S3"
    echo ""
    echo "Posibles causas:"
    echo "1. No tienes permisos de S3:PutObject en el bucket"
    echo "2. Las credenciales expiraron"
    echo "3. El bucket no existe o no tienes acceso"
    echo ""
    echo "Solución alternativa - Subir manualmente:"
    echo "1. Ve a: https://s3.console.aws.amazon.com/s3/buckets/poc-wizi-mex-front"
    echo "2. Elimina todos los archivos actuales"
    echo "3. Sube todos los archivos de la carpeta: frontend/dist/"
    echo "4. Crea una invalidación de CloudFront manualmente"
    echo ""
fi
