# 🪣 Crear Nuevo Bucket S3 para Comfi

**Objetivo:** Crear infraestructura nueva para Comfi sin afectar el proyecto anterior  
**Fecha:** 2024-03-12

---

## 🎯 ESTRATEGIA

**Mantener separados:**
- ✅ Bucket anterior: `poc-wizi-mex-front` (CENTLI - sin tocar)
- ✅ Bucket nuevo: `comfi-frontend` (Comfi con FAQ)

**Ventajas:**
- No afecta desarrollo anterior
- Puedes comparar ambas versiones
- Rollback fácil si es necesario
- Testing independiente

---

## 📋 PASO 1: Crear Bucket S3

### Opción A: Desde Consola AWS (Recomendado)

1. **Ir a S3 Console**
   - https://console.aws.amazon.com/s3/

2. **Crear Bucket**
   - Click en "Create bucket"

3. **Configuración del Bucket**
   ```
   Bucket name: comfi-frontend
   AWS Region: us-east-1 (o la misma que usas)
   
   Object Ownership:
   ✓ ACLs disabled (recommended)
   
   Block Public Access settings:
   ☐ Block all public access (DESMARCAR)
   ✓ Confirmar que entiendes los riesgos
   
   Bucket Versioning:
   ○ Disable (por ahora)
   
   Tags (opcional):
   Key: Project, Value: Comfi
   Key: Environment, Value: Production
   
   Default encryption:
   ✓ Server-side encryption with Amazon S3 managed keys (SSE-S3)
   ```

4. **Click "Create bucket"**

### Opción B: Con AWS CLI (Si tienes permisos)

```bash
# Crear bucket
aws s3 mb s3://comfi-frontend --region us-east-1

# Configurar para hosting estático
aws s3 website s3://comfi-frontend \
    --index-document index.html \
    --error-document index.html

# Configurar política pública
cat > bucket-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::comfi-frontend/*"
        }
    ]
}
EOF

aws s3api put-bucket-policy \
    --bucket comfi-frontend \
    --policy file://bucket-policy.json
```

---

## 📋 PASO 2: Configurar Bucket para Hosting

### Desde Consola AWS

1. **Ir al bucket recién creado**
   - Click en `comfi-frontend`

2. **Habilitar Static Website Hosting**
   - Ir a pestaña "Properties"
   - Scroll hasta "Static website hosting"
   - Click "Edit"
   - Seleccionar "Enable"
   - Index document: `index.html`
   - Error document: `index.html`
   - Click "Save changes"

3. **Configurar Bucket Policy**
   - Ir a pestaña "Permissions"
   - Scroll hasta "Bucket policy"
   - Click "Edit"
   - Pegar esta política:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::comfi-frontend/*"
        }
    ]
}
```

   - Click "Save changes"

4. **Configurar CORS (Opcional pero recomendado)**
   - En pestaña "Permissions"
   - Scroll hasta "Cross-origin resource sharing (CORS)"
   - Click "Edit"
   - Pegar:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

   - Click "Save changes"

---

## 📋 PASO 3: Subir Archivos del Build

1. **Ir al bucket `comfi-frontend`**

2. **Click en "Upload"**

3. **Subir archivos**
   - Click "Add files" o "Add folder"
   - Seleccionar TODO el contenido de `frontend/dist/`:
     - `index.html`
     - Carpeta `assets/` completa
   - Click "Upload"

4. **Verificar archivos subidos**
   ```
   comfi-frontend/
   ├── index.html
   └── assets/
       ├── index-QXORHo-_.css
       └── index-DS-hAYwI.js
   ```

5. **Probar URL del bucket**
   - Ir a "Properties" → "Static website hosting"
   - Copiar "Bucket website endpoint"
   - Ejemplo: `http://comfi-frontend.s3-website-us-east-1.amazonaws.com`
   - Abrir en navegador para verificar

---

## 📋 PASO 4: Crear Distribución CloudFront

### Desde Consola AWS

1. **Ir a CloudFront Console**
   - https://console.aws.amazon.com/cloudfront/

2. **Crear Distribución**
   - Click "Create distribution"

3. **Configuración Origin**
   ```
   Origin domain: comfi-frontend.s3.us-east-1.amazonaws.com
   (Seleccionar de la lista desplegable)
   
   Origin path: (dejar vacío)
   
   Name: comfi-frontend-origin
   
   Origin access:
   ○ Public (si configuraste bucket policy)
   ○ Origin access control settings (OAC) (más seguro)
   
   Si eliges OAC:
   - Click "Create control setting"
   - Name: comfi-oac
   - Click "Create"
   ```

4. **Configuración Default Cache Behavior**
   ```
   Viewer protocol policy:
   ○ Redirect HTTP to HTTPS
   
   Allowed HTTP methods:
   ○ GET, HEAD
   
   Cache policy:
   ○ CachingOptimized (recomendado)
   
   Origin request policy:
   ○ CORS-S3Origin (si usas CORS)
   ```

5. **Configuración Settings**
   ```
   Price class:
   ○ Use all edge locations (best performance)
   
   Alternate domain name (CNAME) - opcional:
   comfi.tudominio.com (si tienes dominio)
   
   Custom SSL certificate:
   (Solo si agregaste CNAME)
   
   Default root object:
   index.html
   
   Standard logging:
   ○ Off (o On si quieres logs)
   
   IPv6:
   ✓ On
   ```

6. **Click "Create distribution"**

7. **Esperar deployment**
   - Estado cambiará de "Deploying" a "Enabled"
   - Puede tomar 5-15 minutos

8. **Copiar URL de CloudFront**
   - Ejemplo: `https://d1a2b3c4d5e6f7.cloudfront.net`

---

## 📋 PASO 5: Configurar Error Pages (Importante para SPA)

1. **Ir a tu distribución CloudFront**

2. **Ir a pestaña "Error pages"**

3. **Crear custom error response**
   - Click "Create custom error response"
   - HTTP error code: `403`
   - Customize error response: `Yes`
   - Response page path: `/index.html`
   - HTTP response code: `200`
   - Click "Create"

4. **Repetir para error 404**
   - HTTP error code: `404`
   - Response page path: `/index.html`
   - HTTP response code: `200`
   - Click "Create"

---

## 🧪 PASO 6: Verificar Deploy

1. **Abrir URL de CloudFront**
   - Ejemplo: `https://d1a2b3c4d5e6f7.cloudfront.net`

2. **Verificar que carga Comfi**
   - ✅ Logo/nombre "Comfi"
   - ✅ Mensaje "¡Hola! Soy Comfi"
   - ✅ 5 Quick Actions FAQ

3. **Probar navegación**
   - Click en diferentes secciones
   - Verificar que no hay errores 404

---

## 📝 ACTUALIZAR CONFIGURACIÓN FRONTEND

Una vez que tengas la URL de CloudFront, actualiza:

### frontend/.env.production

```env
# WebSocket URL (mantener la misma)
VITE_WEBSOCKET_URL=wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev

# Nueva URL de CloudFront (opcional, para referencia)
VITE_APP_URL=https://d1a2b3c4d5e6f7.cloudfront.net
```

**Nota:** No necesitas rebuild si solo cambias la URL de CloudFront, ya que el frontend se conecta al WebSocket directamente.

---

## 🔄 SCRIPT DE DEPLOY ACTUALIZADO

Crea un nuevo script para el bucket de Comfi:

```bash
#!/bin/bash
# deploy-comfi-nuevo.sh

S3_BUCKET="comfi-frontend"
CLOUDFRONT_DIST="<TU_NUEVA_DISTRIBUCION_ID>"
BUILD_DIR="frontend/dist"

echo "🚀 Deploy Comfi a nuevo bucket"

# Subir a S3
aws s3 sync $BUILD_DIR s3://$S3_BUCKET/ --delete

# Invalidar CloudFront
aws cloudfront create-invalidation \
    --distribution-id $CLOUDFRONT_DIST \
    --paths "/*"

echo "✅ Deploy completado!"
echo "URL: https://<tu-cloudfront-url>.cloudfront.net"
```

---

## 📊 COMPARACIÓN DE AMBIENTES

### Ambiente Anterior (CENTLI)
- **Bucket:** poc-wizi-mex-front
- **CloudFront:** E29CTPS84NA5BZ
- **URL:** https://d210pgg1e91kn6.cloudfront.net/
- **Estado:** Intacto, sin cambios

### Ambiente Nuevo (Comfi)
- **Bucket:** comfi-frontend
- **CloudFront:** <nuevo-id>
- **URL:** https://<nueva-url>.cloudfront.net/
- **Estado:** Con sistema FAQ

---

## 💰 COSTOS ESTIMADOS

**S3:**
- Almacenamiento: ~$0.023 por GB/mes
- Tu build (~0.3 MB): ~$0.001/mes
- Transferencia: Gratis a CloudFront

**CloudFront:**
- Primeros 1 TB/mes: $0.085 por GB
- Requests: $0.0075 por 10,000 requests
- Estimado para testing: <$1/mes

**Total estimado:** <$2/mes para ambiente de testing

---

## ✅ CHECKLIST

### Creación de Infraestructura
- [ ] Bucket S3 creado: `comfi-frontend`
- [ ] Static website hosting habilitado
- [ ] Bucket policy configurada
- [ ] CORS configurado (opcional)
- [ ] Archivos subidos desde `frontend/dist/`
- [ ] Distribución CloudFront creada
- [ ] Error pages configuradas (403, 404)
- [ ] URL de CloudFront funcionando

### Verificación
- [ ] URL abre correctamente
- [ ] Nombre "Comfi" visible
- [ ] 5 Quick Actions FAQ visibles
- [ ] Chat funciona
- [ ] No hay errores 404 en navegación

### Documentación
- [ ] URL de CloudFront documentada
- [ ] Distribution ID documentado
- [ ] Script de deploy actualizado

---

## 🎯 SIGUIENTE PASO

Una vez completada la infraestructura nueva:

1. **Verificar frontend funciona** en nueva URL
2. **Deploy backend** (puede usar el mismo Lambda)
3. **Probar integración completa**
4. **Comparar** con versión anterior si es necesario

---

**Última actualización:** 2024-03-12  
**Estado:** Listo para crear infraestructura nueva
