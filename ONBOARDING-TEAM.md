# 🚀 CENTLI - Onboarding Rápido para el Equipo

**Tiempo estimado**: 5 minutos  
**Objetivo**: Que el equipo pueda probar el proyecto inmediatamente

---

## ⚡ Quick Start (3 pasos)

### 1️⃣ Sincronizar Código (30 segundos)
```bash
git checkout feature/hackaton
git pull origin feature/hackaton
```

### 2️⃣ Probar en Producción (2 minutos)
Abrir en el navegador:
```
http://centli-frontend-prod.s3-website-us-east-1.amazonaws.com/test.html
```
- Verificar "✅ Conectado"
- Escribir "Hola" y enviar
- Ver respuesta en el log

### 3️⃣ Probar App Completa (2 minutos)
```
http://centli-frontend-prod.s3-website-us-east-1.amazonaws.com
```
- Explorar marketplace
- Click en botón flotante 💬
- Enviar mensaje en el chat

---

## ✅ ¿Qué está listo?

| Componente | Estado | URL |
|------------|--------|-----|
| Frontend | ✅ | http://centli-frontend-prod.s3-website-us-east-1.amazonaws.com |
| Test Tool | ✅ | .../test.html |
| WebSocket | ✅ | wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod |
| Chat | ✅ | Multimodal (texto, voz, imagen) |
| Marketplace | ✅ | 8 productos con filtros |

---

## 📱 Funcionalidades Principales

### 1. Marketplace Bancario
- 8 productos financieros
- Filtros por categoría, beneficios, precio
- Búsqueda en tiempo real
- Diseño profesional

### 2. Chat Multimodal (DIFERENCIADOR)
- 📝 Texto: Input con envío en tiempo real
- 🎤 Voz: Grabación con animación
- 📷 Imagen: Upload con preview
- ⚡ 6 Quick Actions predefinidas

### 3. Integración Backend
- WebSocket en tiempo real
- Streaming de respuestas
- Reconexión automática
- Manejo de errores

---

## 🧪 Checklist de Pruebas (5 min)

### Básico (2 min)
- [ ] Frontend carga
- [ ] Chat se conecta
- [ ] Enviar mensaje funciona

### Completo (5 min)
- [ ] Marketplace muestra productos
- [ ] Filtros funcionan
- [ ] Chat multimodal (texto, voz, imagen)
- [ ] Quick actions funcionan
- [ ] Responsive design

---

## 🐛 Troubleshooting Rápido

### Problema: Chat no conecta
**Solución**: Usar `/test.html` primero

### Problema: No se pueden enviar mensajes
**Solución**: Verificar estado "Conectado" (verde)

### Problema: Errores en consola
**Solución**: Abrir F12 y buscar mensajes con ❌

---

## 📁 Archivos Clave

### Documentación
- `TEAM-STATUS.md` - Estado completo
- `MENSAJE-PARA-EQUIPO.md` - Mensaje del equipo
- `CHAT-FIX-REPORT.md` - Correcciones recientes

### Código
- `frontend/src/components/Chat/ChatWidget.jsx` - Chat UI
- `frontend/src/context/WebSocketContext.jsx` - WebSocket
- `frontend/src/pages/Marketplace.jsx` - Marketplace

### Testing
- `test-websocket.html` - Test standalone
- `check-deployment.sh` - Verificación

---

## 💻 Desarrollo Local (Opcional)

```bash
cd frontend
npm install
npm run dev
```
Abrir: http://localhost:5173

---

## 🎯 Roles del Equipo

| Desarrollador | Rol | Tareas |
|---------------|-----|--------|
| Dev 1 (AI) | Full Stack | ✅ Frontend + Backend + Docs |
| Dev 2 | Frontend | ⏳ Pruebas + UX/UI |
| Dev 3 | Backend | ⏳ Pruebas + Integration |

---

## 📊 Métricas

- **Páginas**: 4 (Home, Marketplace, ProductDetail, Transactions)
- **Componentes**: 8 principales
- **Build**: 248KB (73KB gzipped)
- **Tiempo de carga**: < 2s

---

## 🚀 Próximos Pasos

1. ⏳ Probar todo el equipo
2. ⏳ Identificar mejoras
3. ⏳ Mejorar UX/UI
4. ⏳ Preparar demo
5. ⏳ ¡Ganar el hackathon!

---

## 📞 Ayuda Rápida

**URLs**:
- Frontend: http://centli-frontend-prod.s3-website-us-east-1.amazonaws.com
- Test: .../test.html
- GitHub: https://github.com/andresvergara-cmd/wizipragma.git

**Documentos**:
- `TEAM-STATUS.md` - Info completa
- `README.md` - Información general

**Scripts**:
- `check-deployment.sh` - Verificar deployment

---

## ✨ Tips

1. **Probar primero** `/test.html` para verificar WebSocket
2. **Usar consola** (F12) para ver logs con emojis
3. **Revisar docs** si hay dudas
4. **Comunicar** problemas al equipo

---

**¡Bienvenidos al equipo CENTLI!** 🌽

**Última actualización**: 2026-02-17 19:35 UTC  
**Commit**: 9c0b388  
**Estado**: ✅ Listo para pruebas del equipo

