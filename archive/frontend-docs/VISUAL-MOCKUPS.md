# 🎨 Mockups Visuales - Chat Widget Comfi

## 📱 Vista General del Chat

### Antes vs Después

```
┌─────────────────────────────────────────────────────────────────────┐
│                          ANTES (Problemas)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ❌ Sin indicador inmediato de procesamiento                       │
│  ❌ Botones FAQ requieren scroll                                   │
│  ❌ Usuario sin avatar                                             │
│  ❌ Feedback visual limitado                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                          DESPUÉS (Solución)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ✅ Indicador inmediato: "Enviando..." → "Pensando..."            │
│  ✅ Layout compacto: Todo visible sin scroll                       │
│  ✅ Avatar de usuario con iniciales y color                        │
│  ✅ Microinteracciones y feedback mejorado                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎬 Flujo de Interacción Completo

### 1. Pantalla de Bienvenida (Compacta)

```
╔═════════════════════════════════════════════════════════════╗
║  🦸 Comfi                                    ● En línea  [×] ║
╠═════════════════════════════════════════════════════════════╣
║                                                             ║
║                      🦸 [Avatar 60px]                       ║
║                                                             ║
║                   ¡Hola! Soy Comfi 👋                      ║
║                  ¿En qué puedo ayudarte?                   ║
║                                                             ║
║  ⚡ Preguntas frecuentes                                    ║
║  ┌─────────────────────────────────────────────────────┐   ║
║  │ 🏦  ¿Cómo me afilio a Comfama?                      │   ║
║  ├─────────────────────────────────────────────────────┤   ║
║  │ 💳  ¿Qué tipos de crédito ofrecen?                  │   ║
║  ├─────────────────────────────────────────────────────┤   ║
║  │ 🎁  ¿Qué subsidios están disponibles?               │   ║
║  └─────────────────────────────────────────────────────┘   ║
║                                                             ║
║  ┌──────────────────────┬──────────────────────┐           ║
║  │  💰                  │  💸                  │           ║
║  │  Ver mi saldo        │  Hacer transferencia │           ║
║  ├──────────────────────┼──────────────────────┤           ║
║  │  🛒                  │  📊                  │           ║
║  │  Ver productos       │  Mis transacciones   │           ║
║  └──────────────────────┴──────────────────────┘           ║
║                                                             ║
║              [ Ver más opciones ↓ ]                        ║
║                                                             ║
╠═════════════════════════════════════════════════════════════╣
║  📷  🎤  [ Escribe tu mensaje... ]              [➤]        ║
╚═════════════════════════════════════════════════════════════╝
```

**Dimensiones**:
- Logo: 60px (reducido de 80px)
- FAQs: 3 items × 45px = 135px
- Acciones: 2 filas × 80px = 160px
- Espaciado: ~55px
- **Total: ~490px** ✅ (cabe sin scroll)

---

### 2. Usuario Envía Mensaje

```
╔═════════════════════════════════════════════════════════════╗
║  🦸 Comfi                                    ● En línea  [×] ║
╠═════════════════════════════════════════════════════════════╣
║                                                             ║
║                                                             ║
║                                    ┌──────────────────┐    ║
║                                 👤 │ ¿Cuál es mi      │    ║
║                                    │ saldo actual?    │    ║
║                                    └──────────────────┘    ║
║                                                             ║
║  🦸  ⚡ • • •                                               ║
║  ┌────────────────────────────────┐                        ║
║  │ Enviando...                    │  ← Estado 1 (0-300ms)  ║
║  └────────────────────────────────┘                        ║
║                                                             ║
╠═════════════════════════════════════════════════════════════╣
║  📷  🎤  [ Escribe tu mensaje... ]              [➤]        ║
╚═════════════════════════════════════════════════════════════╝
```

**Estado 1: "Enviando..."**
- Aparece inmediatamente (0ms)
- Dots animados saltando
- Avatar con animación pulse
- Duración: 300ms

---

### 3. Procesando Respuesta

```
╔═════════════════════════════════════════════════════════════╗
║  🦸 Comfi                                    ● En línea  [×] ║
╠═════════════════════════════════════════════════════════════╣
║                                                             ║
║                                                             ║
║                                    ┌──────────────────┐    ║
║                                 👤 │ ¿Cuál es mi      │    ║
║                                    │ saldo actual?    │    ║
║                                    └──────────────────┘    ║
║                                                             ║
║  🦸  🧠 • • •                                               ║
║  ┌────────────────────────────────┐                        ║
║  │ Comfi está pensando...         │  ← Estado 2 (300ms+)   ║
║  └────────────────────────────────┘                        ║
║                                                             ║
╠═════════════════════════════════════════════════════════════╣
║  📷  🎤  [ Escribe tu mensaje... ]              [➤]        ║
╚═════════════════════════════════════════════════════════════╝
```

**Estado 2: "Comfi está pensando..."**
- Aparece después de 300ms
- Cerebro 🧠 con animación pulse
- Dots animados
- Avatar con animación thinking
- Duración: Hasta que llega stream_start

---

### 4. Streaming de Respuesta

```
╔═════════════════════════════════════════════════════════════╗
║  🦸 Comfi                                    ● En línea  [×] ║
╠═════════════════════════════════════════════════════════════╣
║                                                             ║
║                                                             ║
║                                    ┌──────────────────┐    ║
║                                 👤 │ ¿Cuál es mi      │    ║
║                                    │ saldo actual?    │    ║
║                                    └──────────────────┘    ║
║                                                             ║
║  🦸                                                          ║
║  ┌────────────────────────────────┐                        ║
║  │ Tu saldo actual es             │  ← Estado 3 (streaming)║
║  │ $15,234.50 MXN|                │                        ║
║  └────────────────────────────────┘                        ║
║                                                             ║
╠═════════════════════════════════════════════════════════════╣
║  📷  🎤  [ Escribe tu mensaje... ]              [➤]        ║
╚═════════════════════════════════════════════════════════════╝
```

**Estado 3: Streaming**
- Texto aparece progresivamente
- Cursor parpadeante |
- Avatar con animación speaking
- Gradiente sutil en el fondo

---

### 5. Respuesta Completa

```
╔═════════════════════════════════════════════════════════════╗
║  🦸 Comfi                                    ● En línea  [×] ║
╠═════════════════════════════════════════════════════════════╣
║                                                             ║
║                                                             ║
║                                    ┌──────────────────┐    ║
║                                 👤 │ ¿Cuál es mi      │    ║
║                                    │ saldo actual?    │    ║
║                                    └──────────────────┘    ║
║                                                             ║
║  🦸                                                          ║
║  ┌────────────────────────────────┐                        ║
║  │ Tu saldo actual es             │                        ║
║  │ $15,234.50 MXN                 │                        ║
║  │                                │                        ║
║  │ [💰 Ver detalle] [💸 Transferir]│  ← Acciones rápidas   ║
║  └────────────────────────────────┘                        ║
║                                                             ║
╠═════════════════════════════════════════════════════════════╣
║  📷  🎤  [ Escribe tu mensaje... ]              [➤]        ║
╚═════════════════════════════════════════════════════════════╝
```

**Estado 4: Completo**
- Mensaje completo visible
- Botones de acción contextual
- Avatar estático
- Listo para siguiente interacción

---

## 👤 Avatares

### Avatar de Comfi (Bot)

```
┌─────────────┐
│             │
│   🦸        │  ← Imagen del superhéroe Comfi
│             │     Tamaño: 28px en mensajes
│             │     Animaciones: wave, thinking, speaking
└─────────────┘
```

### Avatar de Usuario (Nuevo)

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│     JD      │     MA      │     CR      │     LP      │
│   (Azul)    │   (Verde)   │   (Coral)   │  (Naranja)  │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**Características**:
- Iniciales del usuario (máx 2 letras)
- Color generado del nombre (6 colores)
- Gradiente sutil
- Sombra suave
- Animación pop al aparecer

---

## 🎨 Paleta de Colores

```
┌──────────────────────────────────────────────────────────┐
│  PRIMARIOS                                               │
├──────────────────────────────────────────────────────────┤
│  ███ #ad37e0  Comfi Primary (Morado)                    │
│  ███ #8b2bb3  Comfi Primary Dark                        │
│  ░░░ rgba(173, 55, 224, 0.1)  Comfi Light               │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  ESTADOS                                                 │
├──────────────────────────────────────────────────────────┤
│  ███ #4caf50  Success (Verde)                           │
│  ███ #ff9800  Warning (Naranja)                         │
│  ███ #f44336  Error (Rojo)                              │
│  ███ #2196f3  Info (Azul)                               │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  AVATARES DE USUARIO                                     │
├──────────────────────────────────────────────────────────┤
│  ███ #4a90e2  Azul                                      │
│  ███ #50c878  Verde Esmeralda                           │
│  ███ #ff6b6b  Rojo Coral                                │
│  ███ #ffa500  Naranja                                   │
│  ███ #9b59b6  Púrpura                                   │
│  ███ #3498db  Azul Cielo                                │
└──────────────────────────────────────────────────────────┘
```

---

## 📐 Espaciado y Dimensiones

```
┌─────────────────────────────────────────────────────────┐
│  COMPONENTE              │  ANTES    │  DESPUÉS         │
├─────────────────────────────────────────────────────────┤
│  Logo bienvenida         │  80px     │  60px  ✅        │
│  FAQs mostrados          │  6 items  │  3 items  ✅     │
│  Acciones rápidas        │  6 (3×2)  │  4 (2×2)  ✅     │
│  Avatar mensaje          │  36px     │  36px            │
│  Padding mensaje         │  0.875rem │  0.875rem        │
│  Gap entre mensajes      │  1rem     │  1rem            │
│  Altura total bienvenida │  ~650px   │  ~490px  ✅      │
└─────────────────────────────────────────────────────────┘
```

---

## 🎭 Animaciones

### 1. Envío de Mensaje

```
[Botón Enviar]
    ↓
[Scale 1 → 0.85 → 1]  (300ms)
    +
[Partícula ✨ flotando]
    ↓
[Indicador "Enviando..."]
```

### 2. Transición de Estados

```
"Enviando..."
    ↓ (fade out 200ms)
"Comfi está pensando..."
    ↓ (fade in 200ms)
[Streaming]
    ↓ (fade out 200ms)
[Mensaje completo]
```

### 3. Avatar de Usuario

```
[Aparición]
    ↓
Scale: 0 → 1.1 → 1  (400ms)
Opacity: 0 → 1
Easing: cubic-bezier(0.34, 1.56, 0.64, 1)
```

---

## 📱 Responsive

### Desktop (> 768px)

```
┌─────────────────────────┐
│  Chat Widget            │
│  420px × 680px          │
│                         │
│  - Logo: 60px           │
│  - FAQs: 3 items        │
│  - Acciones: 2×2        │
│  - Sin scroll ✅        │
└─────────────────────────┘
```

### Mobile (< 768px)

```
┌─────────────────────────┐
│  Chat Widget            │
│  100vw × 100vh          │
│                         │
│  - Logo: 60px           │
│  - FAQs: 3 items (1 col)│
│  - Acciones: 2×2        │
│  - Sin scroll ✅        │
└─────────────────────────┘
```

---

## ✨ Microinteracciones

### Hover en Botones de Acción

```
[Estado Normal]
    ↓ (hover)
[Border: #e8e8e8 → #ad37e0]
[Transform: translateY(0) → translateY(-2px)]
[Shadow: 0 2px 8px → 0 6px 12px]
[Background: white → gradient]
```

### Click en Botón Enviar

```
[Click]
    ↓
[Scale: 1 → 0.85]  (150ms)
    ↓
[Partícula ✨]
    ↓
[Scale: 0.85 → 1]  (150ms)
```

### Mensaje Entrante

```
[Nuevo mensaje]
    ↓
[Slide in from bottom]
[Opacity: 0 → 1]
[Scale: 0.95 → 1]
[Duration: 400ms]
```

---

**Documento creado por**: Kiro - Diseñador UX/UI
**Versión**: 1.0
