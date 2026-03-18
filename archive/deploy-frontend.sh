#!/bin/bash

# Script para desplegar el frontend a AWS S3 y CloudFront
# Bucket: poc-wizi-mex-front
# CloudFront Distribution: E29CTPS84NA5BZ

echo "🚀 Desplegando frontend a producción..."

# Navegar a la carpeta del frontend
cd "frontend" || exit

# Construir el proyecto
echo "📦 Construyendo el proyecto..."
npm run build

# Sincronizar con S3 (elimina archivos viejos)
echo "☁️  Subiendo archivos a S3..."
aws s3 sync dist/ s3://poc-wizi-mex-front/ --delete \
  --cache-control "public, max-age=300" \
  --region us-east-1

# Verificar si el sync fue exitoso
if [ $? -eq 0 ]; then
    echo "✅ Archivos subidos exitosamente a S3"
    
    # Crear invalidación de CloudFront
    echo "🔄 Creando invalidación de CloudFront..."
    aws cloudfront create-invalidation \
      --distribution-id E29CTPS84NA5BZ \
      --paths "/*"
    
    if [ $? -eq 0 ]; then
        echo "✅ Invalidación de CloudFront creada exitosamente"
        echo ""
        echo "🎉 Despliegue completado!"
        echo "🌐 URL: https://d210pgg1e91kn6.cloudfront.net/"
        echo ""
        echo "⏳ Nota: La invalidación de CloudFront puede tardar 5-15 minutos"
    else
        echo "⚠️  Error al crear la invalidación de CloudFront"
        echo "Puedes crearla manualmente desde la consola de AWS"
    fi
else
    echo "❌ Error al subir archivos a S3"
    echo "Verifica tus credenciales de AWS y permisos"
fi
