# Instrucciones para Despliegue Manual del Nuevo Diseño Comfama

## ✅ Estado Actual
- ✅ Build completado exitosamente
- ✅ Archivos listos en: `frontend/dist/`
- ⚠️ Permisos de S3 CLI no disponibles
- 📋 Solución: Subir manualmente desde la consola

---

## 📦 Paso 1: Preparar los archivos

Los archivos ya están construidos en:
```
frontend/dist/
├── assets/
│   ├── index-4BWRE57x.css (42.81 kB)
│   └── index-DJs9Egh0.js (223.18 kB)
└── index.html (0.83 kB)
```

---

## ☁️ Paso 2: Subir a S3

### 2.1 Acceder al bucket
1. Ve a: https://s3.console.aws.amazon.com/s3/buckets/poc-wizi-mex-front
2. Inicia sesión con tu cuenta de AWS si es necesario

### 2.2 Limpiar archivos antiguos
1. Selecciona TODOS los archivos actuales en el bucket
2. Haz clic en "Delete" (Eliminar)
3. Confirma la eliminación

### 2.3 Subir nuevos archivos
1. Haz clic en "Upload" (Cargar)
2. Arrastra TODA la carpeta `frontend/dist/` a la ventana de carga
   - O haz clic en "Add files" y "Add folder"
3. Asegúrate de que se suban:
   - `index.html`
   - Carpeta `assets/` con todos sus archivos
4. Haz clic en "Upload" (Cargar) para iniciar la subida
5. Espera a que termine (debería ser rápido, son solo ~270 KB)

---

## 🔄 Paso 3: Invalidar CloudFront

### 3.1 Acceder a CloudFront
1. Ve a: https://console.aws.amazon.com/cloudfront/v3/home
2. Busca la distribución: `E29CTPS84NA5BZ`
3. Haz clic en el ID de la distribución

### 3.2 Crear invalidación
1. Ve a la pestaña "Invalidations" (Invalidaciones)
2. Haz clic en "Create invalidation" (Crear invalidación)
3. En "Object paths" escribe: `/*`
4. Haz clic en "Create invalidation" (Crear invalidación)

### 3.3 Esperar propagación
- La invalidación puede tardar 5-15 minutos
- Puedes ver el progreso en la misma página

---

## 🎉 Paso 4: Verificar el despliegue

### 4.1 Probar la URL
Después de 5-15 minutos, abre:
```
https://d210pgg1e91kn6.cloudfront.net/
```

### 4.2 Verificar el nuevo diseño
Deberías ver:
- ✅ Logo rosa de Comfama en el header
- ✅ Hero banner con "Festival de Animación Comfama"
- ✅ Sección de búsqueda con 4 tarjetas
- ✅ Beneficios por categorías (Niños, Jóvenes, Adultos, etc.)
- ✅ Carrusel de ubicaciones/sedes
- ✅ Sección de FAQ
- ✅ Sección de aniversario "70 años de Comfama"

### 4.3 Si ves el diseño antiguo
- Espera unos minutos más (la invalidación puede tardar)
- Prueba en modo incógnito o borra la caché del navegador
- Verifica que la invalidación de CloudFront esté completa

---

## 🆘 Solución de Problemas

### Problema: Los archivos no se suben
- Verifica que tienes permisos de escritura en S3 desde la consola
- Intenta refrescar la página de S3 y volver a intentar

### Problema: CloudFront sigue mostrando el diseño antiguo
- Verifica que la invalidación esté en estado "Completed"
- Espera 15 minutos completos
- Prueba con: `https://d210pgg1e91kn6.cloudfront.net/?v=2`

### Problema: Errores 404 o página en blanco
- Verifica que `index.html` esté en la raíz del bucket
- Verifica que la carpeta `assets/` esté correctamente subida
- Revisa la configuración de CloudFront (debe apuntar a `index.html`)

---

## 📝 Notas Importantes

1. **Credenciales temporales**: Las credenciales de AWS que configuramos expiran después de unas horas
2. **Permisos**: Tu rol actual no tiene permisos de S3 desde CLI, pero sí desde la consola
3. **Cache**: CloudFront tiene cache de 5 minutos (configurado en el despliegue)
4. **Backup**: Los archivos antiguos fueron eliminados, pero puedes reconstruirlos desde el código

---

## ✨ Características del Nuevo Diseño

### Header
- Logo rosa de Comfama
- Navegación: Afiliaciones, Créditos, Subsidios, Servicios de empleo, Tienda Comfama
- Zona transaccional (botón rosa)
- Botones de Ayuda y Buscador

### Contenido Principal
- Hero banner con festival de animación
- Sección de búsqueda con 4 servicios principales
- Beneficios por categorías (5 tarjetas con imágenes circulares)
- Carrusel de ubicaciones/sedes
- FAQ con panel de ayuda
- Sección de aniversario con imagen de fondo

### Funcionalidad
- Chat widget flotante (mantiene funcionalidad original)
- Navegación entre páginas (Marketplace, Transacciones)
- Diseño responsive
- Colores de marca Comfama (#e6007e - rosa)

---

## 🔗 Enlaces Útiles

- **S3 Bucket**: https://s3.console.aws.amazon.com/s3/buckets/poc-wizi-mex-front
- **CloudFront**: https://console.aws.amazon.com/cloudfront/v3/home
- **URL Producción**: https://d210pgg1e91kn6.cloudfront.net/
- **WebSocket Backend**: wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev

---

¡Listo! Una vez completados estos pasos, el nuevo diseño Comfama estará en producción. 🚀
