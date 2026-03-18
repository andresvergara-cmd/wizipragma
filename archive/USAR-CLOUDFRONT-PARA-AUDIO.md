# 🎤 Usar CloudFront para Probar Audio

**Problema**: El micrófono requiere HTTPS, S3 website solo tiene HTTP

**Solución**: Usar CloudFront (tiene HTTPS) para probar el audio

---

## 🌐 URL a Usar

```
https://d210pgg1e91kn6.cloudfront.net
```

---

## ⚠️ Situación Actual

### CloudFront (HTTPS) ✅
- ✅ Tiene HTTPS (micrófono funciona)
- ❌ Imágenes antiguas (cache persistente)
- ✅ WebSocket funciona
- ✅ Chat funciona
- ✅ Audio funciona

### S3 Website (HTTP) ❌
- ❌ Solo HTTP (micrófono NO funciona)
- ✅ Imágenes correctas
- ✅ WebSocket funciona
- ✅ Chat funciona
- ❌ Audio NO funciona (requiere HTTPS)

---

## 🎯 Recomendación

**Para probar AUDIO**: Usa CloudFront (HTTPS)
```
https://d210pgg1e91kn6.cloudfront.net
```

**Nota**: Las imágenes se verán rotas, pero el micrófono funcionará.

---

## 🔧 Alternativa: Localhost con HTTPS

Si quieres probar con imágenes correctas Y audio:

### 1. Generar certificado local
```bash
cd frontend
npm install -g mkcert
mkcert -install
mkcert localhost
```

### 2. Configurar Vite para HTTPS
```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'

export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key: fs.readFileSync('./localhost-key.pem'),
      cert: fs.readFileSync('./localhost.pem'),
    },
    port: 3000
  }
})
```

### 3. Actualizar .env.development
```bash
VITE_WS_URL=wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
```

### 4. Ejecutar
```bash
npm run dev
```

### 5. Abrir
```
https://localhost:3000
```

---

## ✅ Conclusión

**Para demo/presentación HOY**: 
- Usa CloudFront (HTTPS) para probar audio
- Las imágenes estarán rotas pero el micrófono funcionará
- El agente procesará el audio correctamente

**Para desarrollo local**:
- Usa localhost con HTTPS
- Todo funcionará correctamente
