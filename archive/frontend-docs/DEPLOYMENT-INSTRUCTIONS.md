# Instrucciones de Despliegue - Mejoras UX Chat

## 🚀 Despliegue a Producción

### Pre-requisitos
- Node.js 18+ instalado
- npm o yarn
- Acceso al repositorio
- Variables de entorno configuradas

---

## 📋 Checklist Pre-Despliegue

### 1. Verificar Build Local
```bash
cd frontend
npm install
npm run build
```

**Resultado esperado**:
```
✓ 65 modules transformed
✓ built in ~2s
dist/index.html
dist/assets/index-*.css
dist/assets/index-*.js
```

### 2. Ejecutar Tests
```bash
npm run test
```

**Resultado esperado**:
```
✓ 12 tests passing
✓ All suites passed
```

### 3. Verificar Linting
```bash
npm run lint
```

**Resultado esperado**:
```
✓ No linting errors
```

### 4. Probar Localmente
```bash
npm run dev
```

Abrir: http://localhost:5173

**Verificar**:
- ✅ Chat se abre correctamente
- ✅ Indicador de procesamiento aparece
- ✅ Avatar de usuario visible
- ✅ FAQ visible sin scroll
- ✅ Animaciones fluidas
- ✅ WebSocket conecta

---

## 🔧 Configuración de Variables

### `.env.production`
```env
VITE_WEBSOCKET_URL=wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
VITE_API_URL=https://api.comfama.com
```

---

## 📦 Proceso de Despliegue

### Opción 1: Despliegue Manual

```bash
# 1. Build de producción
npm run build

# 2. Verificar archivos generados
ls -la dist/

# 3. Subir a servidor
scp -r dist/* user@server:/var/www/html/

# 4. Verificar en producción
curl https://tu-dominio.com
```

### Opción 2: CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy Frontend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm run test
      
      - name: Build
        run: |
          cd frontend
          npm run build
      
      - name: Deploy to S3
        run: |
          aws s3 sync frontend/dist/ s3://your-bucket/
```

### Opción 3: Vercel/Netlify

```bash
# Vercel
vercel --prod

# Netlify
netlify deploy --prod
```

---

## ✅ Verificación Post-Despliegue

### 1. Funcionalidad Básica
- [ ] Chat se abre al hacer clic en botón flotante
- [ ] Pantalla de bienvenida visible
- [ ] FAQ visible sin scroll
- [ ] Botones de acción rápida funcionan

### 2. Indicador de Procesamiento
- [ ] Aparece al enviar mensaje
- [ ] Muestra "Comfi está escribiendo..."
- [ ] Desaparece al iniciar streaming
- [ ] Animación de puntos funciona

### 3. Avatar de Usuario
- [ ] Visible en mensajes del usuario
- [ ] Posicionado a la derecha
- [ ] Gradiente azul correcto
- [ ] Efecto de brillo funciona

### 4. Animaciones
- [ ] Mensajes aparecen con animación
- [ ] Streaming tiene gradiente animado
- [ ] Cursor parpadea durante streaming
- [ ] Transiciones suaves

### 5. WebSocket
- [ ] Conexión exitosa
- [ ] Estado "En línea" visible
- [ ] Mensajes se envían correctamente
- [ ] Respuestas se reciben

### 6. Responsive
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

---

## 🐛 Troubleshooting

### Problema: Build falla
```bash
# Limpiar cache
rm -rf node_modules dist
npm install
npm run build
```

### Problema: WebSocket no conecta
```bash
# Verificar URL en .env.production
echo $VITE_WEBSOCKET_URL

# Probar conexión
wscat -c wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
```

### Problema: Animaciones no funcionan
```bash
# Verificar que CSS se cargó
curl https://tu-dominio.com/assets/index-*.css | grep "messageSlideIn"
```

### Problema: Avatar no aparece
```bash
# Verificar en DevTools Console
# Buscar errores de CSS o componentes
```

---

## 📊 Monitoreo Post-Despliegue

### Métricas a Observar

1. **Performance**
   - Tiempo de carga: <3s
   - First Contentful Paint: <1.5s
   - Time to Interactive: <3.5s

2. **Errores**
   - JavaScript errors: 0
   - CSS errors: 0
   - WebSocket errors: <1%

3. **Uso**
   - Tasa de apertura del chat
   - Mensajes enviados
   - Tiempo de respuesta promedio

### Herramientas

```bash
# Lighthouse
lighthouse https://tu-dominio.com --view

# WebPageTest
# https://www.webpagetest.org/

# Chrome DevTools
# Performance tab
# Network tab
```

---

## 🔄 Rollback

### Si algo sale mal:

```bash
# Opción 1: Revertir commit
git revert HEAD
git push

# Opción 2: Deploy versión anterior
git checkout <commit-anterior>
npm run build
# Deploy...

# Opción 3: Restaurar backup
aws s3 sync s3://backup-bucket/ s3://production-bucket/
```

---

## 📝 Notas Importantes

1. **No hay breaking changes**: Las mejoras son aditivas
2. **Backward compatible**: Funciona con backend actual
3. **Progressive enhancement**: Funciona sin JavaScript (HTML básico)
4. **Graceful degradation**: Fallbacks para navegadores antiguos

---

## 🎉 Despliegue Exitoso

Una vez completado:

1. ✅ Notificar al equipo
2. ✅ Actualizar documentación
3. ✅ Monitorear métricas
4. ✅ Recopilar feedback de usuarios
5. ✅ Planear siguientes mejoras

---

## 📞 Contacto

Para problemas durante el despliegue:
- Revisar logs en servidor
- Consultar documentación en `/frontend/`
- Contactar al equipo de DevOps
