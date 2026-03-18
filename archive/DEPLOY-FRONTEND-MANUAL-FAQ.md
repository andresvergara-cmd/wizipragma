# 📦 Deploy Manual Frontend - Comfi con Sistema FAQ

**Fecha:** 2024-03-12  
**Build:** ✅ Completado en `frontend/dist/`  
**Método:** Deploy manual vía Consola AWS

---

## ✅ BUILD COMPLETADO

```
✓ 64 modules transformed.
dist/index.html                   0.83 kB
dist/assets/index-QXORHo-_.css   48.88 kB
dist/assets/index-DS-hAYwI.js   233.00 kB
✓ built in 744ms
```

**Archivos listos en:** `frontend/dist/`

---

## 🚀 PASOS PARA DEPLOY MANUAL

### Paso 1: Acceder a S3

1. Ir a AWS Console: https://console.aws.amazon.com/s3/
2. Buscar bucket: `poc-wizi-mex-front`
3. Click en el bucket

### Paso 2: Limpiar Archivos Antiguos (Opcional pero Recomendado)

1. Seleccionar todos los archivos en el bucket
2. Click en "Delete"
3. Confirmar eliminación

**Nota:** Esto asegura que no queden archivos antiguos de CENTLI

### Paso 3: Subir Nuevos Archivos

1. Click en "Upload"
2. Click en "Add files" o "Add folder"
3. Seleccionar TODO el contenido de `frontend/dist/`:
   - `index.html`
   - Carpeta `assets/` (con todos sus archivos)
4. Click en "Upload"
5. Esperar a que complete

### Paso 4: Verificar Archivos Subidos

Deberías ver:
```
poc-wizi-mex-front/
├── index.html
└── assets/
    ├── index-QXORHo-_.css
    └── index-DS-hAYwI.js
```

### Paso 5: Invalidar CloudFront

1. Ir a CloudFront: https://console.aws.amazon.com/cloudfront/
2. Buscar distribución: `E29CTPS84NA5BZ`
3. Click en la distribución
4. Ir a pestaña "Invalidations"
5. Click en "Create invalidation"
6. En "Object paths" escribir: `/*`
7. Click en "Create invalidation"
8. Esperar 2-5 minutos

---

## 🧪 VERIFICAR DEPLOY

### 1. Abrir URL

```
https://d210pgg1e91kn6.cloudfront.net/
```

### 2. Verificar Cambios

**Debe mostrar:**
- ✅ Logo/nombre "Comfi" (no CENTLI)
- ✅ Mensaje "¡Hola! Soy Comfi"
- ✅ Subtítulo "Tu asistente de Comfama"
- ✅ 5 Quick Actions FAQ:
  - "¿Cómo me afilio?"
  - "¿Cuál es mi tarifa?"
  - "Tipos de créditos"
  - "Requisitos crédito"
  - "Subsidios disponibles"

### 3. Probar Funcionalidad

1. **Click en Quick Action FAQ**
   - Debe enviar la pregunta al chat
   - Debe aparecer como mensaje del usuario

2. **Escribir pregunta manualmente**
   - Ejemplo: "¿Cómo me afilio a Comfama?"
   - Debe enviar correctamente

3. **Verificar WebSocket**
   - Indicador debe mostrar "En línea" (verde)
   - Si muestra "Desconectado" (rojo), hay problema de conexión

---

## 📊 CAMBIOS INCLUIDOS EN ESTE DEPLOY

### Frontend Actualizado

**Renombrado CENTLI → Comfi:**
- ✅ Nombre del asistente
- ✅ Mensajes de bienvenida
- ✅ Quick actions

**Sistema FAQ Implementado:**
- ✅ 4 componentes React (FAQCard, FAQQuickActions, etc.)
- ✅ 5 Quick Actions FAQ en welcome screen
- ✅ Estilos con tema Comfama (rosa #e6007e)
- ✅ Integración completa en ChatWidget
- ✅ Base de datos FAQ frontend (5 FAQs)

**Funcionalidades FAQ:**
- ✅ Click en quick action → envía pregunta
- ✅ Detección de respuestas FAQ
- ✅ Renderizado de FAQCard (cuando backend responda)
- ✅ Thumbs up/down para feedback
- ✅ Preguntas relacionadas
- ✅ Formulario de feedback
- ✅ Escalamiento a asesor

---

## ⚠️ IMPORTANTE: Backend Pendiente

**Para ver FAQCards funcionando completamente**, necesitas:

### 1. Deploy Backend Actualizado

El backend tiene cambios en:
- `src_aws/app_inference/action_tools.py` (FAQ database + tool)
- `src_aws/app_inference/bedrock_config.py` (system prompt)

**Ver instrucciones:** `INSTRUCCIONES-DEPLOY-BACKEND.md`

### 2. Qué Funciona Ahora vs Después del Backend

**AHORA (Solo Frontend):**
- ✅ Welcome screen con quick actions FAQ
- ✅ Click en quick actions funciona
- ✅ Chat envía preguntas
- ✅ Bot responde (texto normal)
- ⏳ FAQCards NO se renderizan (necesita backend)

**DESPUÉS (Frontend + Backend):**
- ✅ Todo lo anterior
- ✅ Backend detecta preguntas FAQ
- ✅ Backend usa tool `answer_faq`
- ✅ Respuesta estructurada FAQ
- ✅ FAQCard se renderiza con diseño elegante
- ✅ Botones de acción funcionan
- ✅ Preguntas relacionadas navegables

---

## 🐛 TROUBLESHOOTING

### No veo los cambios

**Solución 1:** Limpiar caché del navegador
- Chrome: Ctrl+Shift+R (Cmd+Shift+R en Mac)
- Firefox: Ctrl+F5
- Safari: Cmd+Option+R

**Solución 2:** Verificar invalidación de CloudFront
- Debe estar en estado "Completed"
- Esperar 5 minutos adicionales

**Solución 3:** Modo incógnito
- Abrir en ventana privada/incógnito

### Quick Actions FAQ no aparecen

**Verificar:**
1. Consola del navegador (F12)
2. Buscar errores de JavaScript
3. Verificar que `faqData.js` se cargó

**Solución:** Limpiar caché y recargar

### WebSocket no conecta

**Verificar:**
1. URL en `.env.production`:
   ```
   VITE_WEBSOCKET_URL=wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev
   ```
2. Backend Lambda está activo
3. API Gateway está funcionando

---

## 📝 CHECKLIST DE DEPLOY

### Pre-Deploy
- [x] Build completado (`npm run build`)
- [x] Archivos en `frontend/dist/`
- [ ] Acceso a AWS Console S3
- [ ] Acceso a AWS Console CloudFront

### Deploy
- [ ] Archivos antiguos eliminados de S3
- [ ] Nuevos archivos subidos a S3
- [ ] `index.html` presente
- [ ] Carpeta `assets/` presente
- [ ] CloudFront invalidado

### Post-Deploy
- [ ] URL abre correctamente
- [ ] Nombre "Comfi" visible
- [ ] 5 Quick Actions FAQ visibles
- [ ] Chat funciona
- [ ] WebSocket conecta

### Verificación FAQ
- [ ] Click en quick action funciona
- [ ] Pregunta se envía al chat
- [ ] Bot responde
- [ ] (Pendiente backend) FAQCard se renderiza

---

## 🎯 SIGUIENTE PASO

Una vez completado el deploy del frontend:

**Deploy del Backend:**
1. Leer: `INSTRUCCIONES-DEPLOY-BACKEND.md`
2. Empaquetar Lambda con cambios
3. Actualizar función Lambda
4. Probar tool `answer_faq`
5. Verificar integración completa

---

## 📞 RESUMEN

**Frontend Deploy:** Manual vía Consola AWS  
**Bucket S3:** poc-wizi-mex-front  
**CloudFront:** E29CTPS84NA5BZ  
**URL:** https://d210pgg1e91kn6.cloudfront.net/

**Estado Actual:**
- ✅ Build completado
- ⏳ Esperando deploy manual a S3
- ⏳ Esperando invalidación CloudFront
- ⏳ Esperando deploy backend

**Progreso Total:** 85% (Frontend listo, Backend pendiente)

---

**Última actualización:** 2024-03-12  
**Siguiente:** Deploy Backend para completar sistema FAQ
