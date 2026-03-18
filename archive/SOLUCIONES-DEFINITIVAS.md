# 🎯 Soluciones Definitivas para CloudFront Cache

**Fecha**: 2026-02-19
**Problema**: CloudFront cache muy agresivo (24 horas) causa problemas en deploys

---

## 📊 Comparación de Soluciones

| Solución | Tiempo | Complejidad | HTTPS | Recomendada |
|----------|--------|-------------|-------|-------------|
| 1. Modificar CloudFront actual | 15-20 min | Baja | ✅ | ⭐⭐⭐⭐⭐ |
| 2. Nueva distribución CloudFront | 15-20 min | Media | ✅ | ⭐⭐⭐⭐ |
| 3. Versionado de URLs | Inmediato | Baja | ✅ | ⭐⭐⭐ |
| 4. Mantener S3 Website | Inmediato | Ninguna | ❌ | ⭐⭐ |

---

## ✅ SOLUCIÓN 1: Modificar CloudFront Actual (RECOMENDADA)

### Ventajas:
- ✅ Mantiene la misma URL
- ✅ HTTPS habilitado
- ✅ Soluciona el problema de raíz
- ✅ Futuros deploys serán rápidos (5 min)

### Desventajas:
- ⏳ Tarda 15-20 minutos en aplicarse
- ⚠️ Requiere esperar a que se propague

### Cómo Aplicar:

```bash
chmod +x fix-cloudfront-cache.sh
./fix-cloudfront-cache.sh
```

### Qué Hace:
1. Obtiene configuración actual de CloudFront
2. Modifica los valores de cache:
   - `DefaultTTL`: 86400 (24h) → 300 (5 min)
   - `MaxTTL`: 31536000 (1 año) → 3600 (1 hora)
3. Aplica los cambios
4. Crea nueva invalidación

### Resultado:
- HTML: Cache de 5 minutos (en lugar de 24 horas)
- Assets (JS/CSS): Siguen con cache largo (tienen hash en nombre)
- Futuros deploys se propagarán en ~5 minutos

---

## ✅ SOLUCIÓN 2: Nueva Distribución CloudFront

### Ventajas:
- ✅ Configuración optimizada desde cero
- ✅ HTTPS habilitado
- ✅ Separación de cache por tipo de archivo
- ✅ No afecta distribución actual

### Desventajas:
- ⏳ Tarda 15-20 minutos en estar lista
- 🔄 Requiere cambiar URL en configuración
- 💰 Costo adicional (mínimo)

### Cómo Aplicar:

```bash
chmod +x create-new-cloudfront.sh
./create-new-cloudfront.sh
```

### Qué Hace:
1. Crea nueva distribución apuntando a S3 Website
2. Configura cache optimizado:
   - HTML: 5 minutos
   - Assets: 24 horas
3. Habilita compresión y HTTPS
4. Configura error pages para SPA

### Resultado:
Nueva URL de CloudFront con configuración optimizada.

---

## ✅ SOLUCIÓN 3: Versionado de URLs

### Ventajas:
- ✅ Funciona inmediatamente
- ✅ No requiere cambios en CloudFront
- ✅ HTTPS habilitado
- ✅ Muy simple de implementar

### Desventajas:
- 🔄 Requiere actualizar URL en cada deploy
- 📝 Necesita documentación para el equipo

### Cómo Aplicar:

#### Opción A: Parámetro de Query
Agregar timestamp a la URL:
```
https://d210pgg1e91kn6.cloudfront.net/?v=20260219-1453
```

#### Opción B: Modificar Vite Config
```javascript
// frontend/vite.config.js
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name]-[hash]-${Date.now()}.js`,
        chunkFileNames: `assets/[name]-[hash]-${Date.now()}.js`,
        assetFileNames: `assets/[name]-[hash]-${Date.now()}.[ext]`
      }
    }
  }
})
```

### Resultado:
Cada build genera archivos con nombres únicos que CloudFront no tiene cacheados.

---

## ✅ SOLUCIÓN 4: Mantener S3 Website (Temporal)

### Ventajas:
- ✅ Funciona ahora
- ✅ Sin problemas de cache
- ✅ Cero configuración adicional

### Desventajas:
- ❌ Sin HTTPS
- ❌ Sin CDN (más lento globalmente)
- ❌ No es solución de producción

### URL:
```
http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com
```

---

## 🎯 Recomendación Final

### Para AHORA (Próximas horas):
**Usar S3 Website** mientras se aplica solución definitiva:
```
http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com
```

### Para PRODUCCIÓN (Solución definitiva):
**Aplicar Solución 1** (Modificar CloudFront actual):
```bash
./fix-cloudfront-cache.sh
```

**Razones**:
1. Mantiene la misma URL (no hay que cambiar configuración)
2. Soluciona el problema de raíz
3. Futuros deploys serán rápidos
4. HTTPS habilitado
5. Configuración profesional

---

## 📝 Plan de Implementación

### Paso 1: Inmediato (Ahora)
```bash
# Usar S3 Website para demo/pruebas
echo "URL temporal: http://poc-wizi-mex-front.s3-website-us-east-1.amazonaws.com"
```

### Paso 2: Aplicar Solución Definitiva (15-20 min)
```bash
# Modificar CloudFront
chmod +x fix-cloudfront-cache.sh
./fix-cloudfront-cache.sh
```

### Paso 3: Verificar (Después de 20 min)
```bash
# Verificar que CloudFront funcione
./test-images-complete.sh
```

### Paso 4: Cambiar a CloudFront
```bash
# Cuando test muestre ✅, usar CloudFront
echo "URL producción: https://d210pgg1e91kn6.cloudfront.net"
```

---

## 🔧 Comandos Útiles

### Verificar estado de CloudFront
```bash
aws cloudfront get-distribution \
  --id E29CTPS84NA5BZ \
  --profile pragma-power-user \
  --query 'Distribution.Status'
```

### Verificar configuración de cache
```bash
aws cloudfront get-distribution-config \
  --id E29CTPS84NA5BZ \
  --profile pragma-power-user \
  --query 'DistributionConfig.DefaultCacheBehavior.{MinTTL:MinTTL,DefaultTTL:DefaultTTL,MaxTTL:MaxTTL}'
```

### Crear invalidación manual
```bash
aws cloudfront create-invalidation \
  --distribution-id E29CTPS84NA5BZ \
  --paths "/*" \
  --profile pragma-power-user
```

---

## 💡 Mejores Prácticas para el Futuro

### 1. Cache por Tipo de Archivo
- **HTML**: Cache corto (5 min) - cambia frecuentemente
- **JS/CSS con hash**: Cache largo (1 año) - nombre único por versión
- **Imágenes**: Cache medio (1 día) - cambian ocasionalmente

### 2. Versionado de Assets
Vite ya hace esto automáticamente:
```
index-DMo-c1dr.js  ← Hash único por versión
```

### 3. Headers de Cache
```bash
# HTML: No cache
--cache-control "no-cache, no-store, must-revalidate"

# Assets: Cache largo
--cache-control "public, max-age=31536000, immutable"
```

### 4. Invalidaciones Estratégicas
```bash
# Solo HTML (rápido)
--paths "/index.html"

# Todo (lento)
--paths "/*"
```

---

## ✅ Conclusión

**Solución Recomendada**: Modificar CloudFront actual (Solución 1)

**Tiempo total**: 15-20 minutos

**Resultado**: CloudFront con cache optimizado que permite deploys rápidos sin problemas de cache.

---

**Scripts disponibles**:
- `fix-cloudfront-cache.sh` - Modifica CloudFront actual
- `create-new-cloudfront.sh` - Crea nueva distribución
- `test-images-complete.sh` - Verifica estado

**Documentación**:
- `SOLUCION-INMEDIATA-IMAGENES.md` - Solución temporal (S3)
- `SOLUCIONES-DEFINITIVAS.md` - Este documento
