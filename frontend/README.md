# CENTLI Frontend - React Application

Frontend profesional para CENTLI, tu coach financiero multimodal con IA.

## 🎨 Características

- ✅ **React 18** con Vite para desarrollo rápido
- ✅ **Diseño Profesional** inspirado en marketplaces modernos
- ✅ **Identidad CENTLI** con colores morado/violeta (#ad37e0)
- ✅ **Interfaz Conversacional** integrada con WebSocket
- ✅ **Catálogo de Productos** con datos mock
- ✅ **Sistema de Beneficios** (Cashback, MSI, Descuentos)
- ✅ **Responsive Design** mobile-first
- ✅ **Animaciones Suaves** con Framer Motion
- ✅ **Routing** con React Router
- ✅ **Context API** para estado global

## 📁 Estructura del Proyecto

```
frontend/
├── public/              # Archivos estáticos
├── src/
│   ├── components/      # Componentes reutilizables
│   │   ├── Layout/      # Layout principal
│   │   ├── Chat/        # Interfaz conversacional
│   │   ├── Product/     # Componentes de productos
│   │   ├── Common/      # Componentes comunes
│   │   └── ...
│   ├── pages/           # Páginas de la aplicación
│   │   ├── Home.jsx
│   │   ├── Marketplace.jsx
│   │   ├── ProductDetail.jsx
│   │   └── Transactions.jsx
│   ├── context/         # Context providers
│   │   ├── WebSocketContext.jsx
│   │   └── ChatContext.jsx
│   ├── hooks/           # Custom hooks
│   ├── data/            # Datos mock
│   │   └── mockProducts.js
│   ├── utils/           # Utilidades
│   ├── App.jsx          # Componente principal
│   ├── main.jsx         # Entry point
│   └── index.css        # Estilos globales
├── index.html
├── vite.config.js
└── package.json
```

## 🚀 Instalación

### Prerrequisitos
- Node.js 18+ 
- npm o yarn

### Pasos

1. **Navegar al directorio frontend**:
```bash
cd frontend
```

2. **Instalar dependencias**:
```bash
npm install
```

3. **Configurar variables de entorno** (crear `.env`):
```env
VITE_WEBSOCKET_URL=wss://your-websocket-endpoint.execute-api.us-east-1.amazonaws.com/prod
VITE_API_URL=https://your-api-endpoint.execute-api.us-east-1.amazonaws.com/prod
```

4. **Iniciar servidor de desarrollo**:
```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`

## 🛠️ Scripts Disponibles

- `npm run dev` - Inicia servidor de desarrollo
- `npm run build` - Construye para producción
- `npm run preview` - Preview de build de producción
- `npm run lint` - Ejecuta linter

## 🎨 Identidad Visual CENTLI

### Colores Principales
- **Primary**: `#ad37e0` (Morado CENTLI)
- **Primary Dark**: `#8b2bb3`
- **Primary Light**: `#c77dff`
- **Secondary**: `#6b46c1`
- **Accent**: `#e0aaff`

### Tipografía
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800

### Iconografía
- **Mascota**: Cintéotl (Dios Azteca del Maíz - CENTLI significa "maíz" en náhuatl)
- **Logo**: SVG personalizado con diseño inspirado en iconografía azteca
- **Estilo**: Lucide React Icons

## 📦 Componentes Principales

### Layout
- **Header**: Navegación principal con logo CENTLI
- **Sidebar**: Menú lateral con categorías
- **ChatWidget**: Interfaz conversacional flotante
- **Footer**: Información y enlaces

### Marketplace
- **ProductGrid**: Grid responsive de productos
- **ProductCard**: Tarjeta de producto con beneficios
- **FilterBar**: Filtros y búsqueda
- **BenefitBadge**: Badges de beneficios (Cashback, MSI, etc.)

### Chat
- **ChatWindow**: Ventana de chat con mensajes
- **MessageBubble**: Burbujas de mensajes (usuario/bot)
- **VoiceInput**: Botón de entrada de voz
- **ImageUpload**: Upload de imágenes

### Product
- **ProductDetail**: Vista detallada de producto
- **BenefitComparison**: Comparador de beneficios
- **PurchaseModal**: Modal de confirmación de compra

## 🔌 Integración WebSocket

### Formato de Mensajes

**Envío (Frontend → Backend)**:
```json
{
  "action": "sendMessage",
  "data": {
    "user_id": "user-001",
    "session_id": "session-123",
    "message": "¿Cuál es mi saldo?",
    "type": "TEXT"
  }
}
```

**Recepción (Backend → Frontend)**:
```json
{
  "msg_type": "agent_response",
  "message": "Tu saldo actual es $50,000 MXN",
  "is_response": true,
  "data": {
    "type": "TEXT",
    "content": "..."
  }
}
```

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px
- **Large Desktop**: > 1400px

## 🎯 Funcionalidades Implementadas

### ✅ Fase 1 - Base (Completado)
- [x] Estructura de proyecto React
- [x] Sistema de diseño CENTLI
- [x] Routing con React Router
- [x] Context API para estado global
- [x] Datos mock de productos

### ✅ Fase 2 - Componentes (Completado)
- [x] Layout completo (Header, Nav, Footer)
- [x] Página Home con hero section
- [x] Marketplace con grid de productos
- [x] ProductCard con beneficios
- [x] Filtros y búsqueda
- [x] ProductDetail con tabs
- [x] Transactions con historial

### ✅ Fase 3 - Chat (Completado)
- [x] ChatWidget flotante
- [x] Integración WebSocket
- [x] Mensajes de texto
- [x] Context providers (WebSocket, Chat)
- [x] Typing indicator
- [x] Connection status

### ⏳ Fase 4 - Multimodal (Pendiente)
- [ ] Voice input/output
- [ ] Image upload
- [ ] Transaction confirmation modal
- [ ] Product recommendations from chat

## 🚢 Deployment

### Build para Producción
```bash
npm run build
```

### Deploy a S3
```bash
aws s3 sync dist/ s3://centli-frontend-bucket/ --delete
aws s3 website s3://centli-frontend-bucket/ --index-document index.html
```

### Deploy a CloudFront (Opcional)
```bash
# Crear distribución CloudFront apuntando al bucket S3
# Configurar invalidación de caché
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

## 📝 Próximos Pasos

1. **Completar componentes de Layout**
2. **Implementar páginas principales**
3. **Integrar WebSocket real**
4. **Agregar voice input/output**
5. **Implementar flujo de transacciones**
6. **Testing e2e**
7. **Optimización de performance**
8. **Deploy a producción**

## 🤝 Contribución

Este proyecto es parte del hackathon CENTLI. Para contribuir:

1. Crear branch desde `feature/hackaton`
2. Implementar cambios
3. Commit y push
4. Crear PR para revisión

## 📄 Licencia

Proyecto privado - Pragma S.A.

---

**Creado con ❤️ por el equipo CENTLI**  
**Hackathon 2026 - Pragma**
