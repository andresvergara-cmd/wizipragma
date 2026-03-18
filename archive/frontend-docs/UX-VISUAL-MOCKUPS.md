# 🎨 Mockups Visuales - Chat Comfi

## 📱 Estados de la Interfaz

---

## 1️⃣ Pantalla de Bienvenida (Optimizada)

```
┌─────────────────────────────────────────┐
│  Comfi                            ✕     │ ← Header morado
│  ● En línea                             │
├─────────────────────────────────────────┤
│                                         │
│           🌽 (Avatar Comfi)             │ ← Logo animado
│                                         │
│        ¡Hola! Soy Comfi                 │ ← Título (1.5rem)
│   Tu asistente de Comfama.              │
│   ¿En qué puedo ayudarte hoy?           │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ ⚡ Preguntas frecuentes          │   │ ← FAQ Section
│  │                                  │   │   (Visible sin scroll)
│  │  ┌──────────┐  ┌──────────┐    │   │
│  │  │ 🏦 ¿Cómo │  │ 💰 ¿Cuáles│   │   │
│  │  │ me       │  │ son las   │   │   │
│  │  │ afilio?  │  │ tarifas?  │   │   │
│  │  └──────────┘  └──────────┘    │   │
│  │  ┌──────────┐  ┌──────────┐    │   │
│  │  │ 💳 Tipos │  │ 📋 Requi- │   │   │
│  │  │ de       │  │ sitos     │   │   │
│  │  │ crédito  │  │ crédito   │   │   │
│  │  └──────────┘  └──────────┘    │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌──────────┐  ┌──────────┐           │ ← Quick Actions
│  │ 💰 Ver   │  │ 💸 Hacer │           │   (Visible sin scroll)
│  │ mi saldo │  │ transf.  │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ 🛒 Ver   │  │ 📊 Mis   │           │
│  │ productos│  │ transac. │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ 🎁 Ofertas│ │ ❓ Ayuda │           │
│  └──────────┘  └──────────┘           │
│                                         │
├─────────────────────────────────────────┤
│ 📷 🎤  [Escribe tu mensaje...]    ➤   │ ← Input
└─────────────────────────────────────────┘
    Puedes escribir, hablar o enviar imágenes
```

**Mejoras Aplicadas**:
- ✅ Altura aumentada (680px)
- ✅ FAQ visible sin scroll
- ✅ Espaciado optimizado
- ✅ Todo el contenido importante visible

---

## 2️⃣ Estado: Procesando Mensaje

```
┌─────────────────────────────────────────┐
│  Comfi                            ✕     │
│  ● En línea                             │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ ¿Cuál es mi saldo actual?       │   │ ← Mensaje usuario
│  └─────────────────────────────────┘ 👤│   (Avatar azul)
│                                         │
│  🌽 ┌─────────────────────────────┐    │ ← Indicador nuevo
│     │ ⟳ Comfi está pensando...    │    │   (Spinner + texto)
│     └─────────────────────────────┘    │   (Fondo morado claro)
│                                         │
│                                         │
│                                         │
│                                         │
│                                         │
│                                         │
├─────────────────────────────────────────┤
│ 📷 🎤  [Escribe tu mensaje...]    ➤   │
└─────────────────────────────────────────┘
```

**Características**:
- ✅ Spinner animado (rotación continua)
- ✅ Texto "Comfi está pensando..."
- ✅ Fondo morado claro con borde
- ✅ Avatar Comfi animado
- ✅ Se muestra inmediatamente después de enviar

**CSS**:
```css
.processing-spinner {
  animation: spin 0.8s linear infinite;
}

.processing-text {
  animation: processingPulse 1.5s ease-in-out infinite;
}
```

---

## 3️⃣ Estado: Escribiendo (Streaming)

```
┌─────────────────────────────────────────┐
│  Comfi                            ✕     │
│  ● En línea                             │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ ¿Cuál es mi saldo actual?       │   │
│  └─────────────────────────────────┘ 👤│
│                                         │
│  🌽 ┌─────────────────────────────┐    │ ← Streaming
│     │ Tu saldo actual es de       │    │   (Texto apareciendo)
│     │ $1,234,567 COP. Tienes      │    │   (Cursor parpadeante)
│     │ disponible para gastar|     │    │
│     └─────────────────────────────┘    │
│                                         │
│                                         │
│                                         │
│                                         │
├─────────────────────────────────────────┤
│ 📷 🎤  [Escribe tu mensaje...]    ➤   │
└─────────────────────────────────────────┘
```

**Características**:
- ✅ Texto aparece gradualmente
- ✅ Cursor parpadeante (|)
- ✅ Avatar Comfi con animación "hablando"
- ✅ Fondo con gradiente sutil

---

## 4️⃣ Conversación Completa

```
┌─────────────────────────────────────────┐
│  Comfi                            ✕     │
│  ● En línea                             │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Hola, ¿cómo estás?              │   │
│  └─────────────────────────────────┘ 👤│ ← Avatar usuario
│                                         │   (Azul #4a90e2)
│  🌽 ┌─────────────────────────────┐    │
│     │ ¡Hola! Estoy muy bien,      │    │
│     │ gracias por preguntar.      │    │
│     │ ¿En qué puedo ayudarte?     │    │
│     └─────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Quiero hacer una transferencia  │   │
│  └─────────────────────────────────┘ 👤│
│                                         │
│  🌽 ┌─────────────────────────────┐    │ ← Avatar Comfi
│     │ Perfecto, te ayudo con eso. │    │   (Morado #ad37e0)
│     │ ¿A quién deseas transferir? │    │
│     └─────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ A Juan Pérez                    │   │
│  └─────────────────────────────────┘ 👤│
│                                         │
│  🌽 ┌─────────────────────────────┐    │
│     │ ⟳ Comfi está pensando...    │    │ ← Procesando
│     └─────────────────────────────┘    │
│                                         │
├─────────────────────────────────────────┤
│ 📷 🎤  [Escribe tu mensaje...]    ➤   │
└─────────────────────────────────────────┘
```

**Diferenciación Visual**:
- **Usuario**: Burbuja derecha, avatar azul 👤
- **Bot**: Burbuja izquierda, avatar morado 🌽
- **Procesando**: Spinner + texto morado
- **Streaming**: Cursor parpadeante

---

## 5️⃣ Hover States - Quick Actions

### **Estado Normal**
```
┌──────────────┐
│  💰 Ver mi   │  ← Borde gris #e8e8e8
│     saldo    │     Fondo blanco
└──────────────┘
```

### **Estado Hover**
```
┌──────────────┐
│  💰 Ver mi   │  ← Borde morado #ad37e0
│     saldo    │     Fondo gradiente morado
└──────────────┘     Elevación -4px
     ↑ Sombra        Escala 1.0
```

**Animación**:
```css
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
transform: translateY(-4px);
box-shadow: 0 8px 16px rgba(173, 55, 224, 0.15);
```

---

## 6️⃣ Hover States - FAQ Quick Actions

### **Estado Normal**
```
┌──────────────┐
│  🏦 ¿Cómo me │  ← Borde gris #e8e8e8
│     afilio?  │     Fondo blanco
└──────────────┘     Texto negro
```

### **Estado Hover**
```
┌──────────────┐
│  🏦 ¿Cómo me │  ← Borde morado #ad37e0
│     afilio?  │     Fondo gradiente morado
└──────────────┘     Texto blanco
     ↑ Sombra        Icono escala 1.15
```

**Animación**:
```css
.quick-action-item:hover {
  background: linear-gradient(135deg, #ad37e0 0%, #8b2bb3 100%);
  color: white;
  transform: translateY(-3px);
}

.quick-action-item:hover .quick-faq-icon {
  transform: scale(1.15);
}
```

---

## 7️⃣ Botón de Enviar - Estados

### **Normal**
```
  ➤   ← Círculo morado
      Sombra suave
```

### **Hover**
```
  ➤   ← Círculo morado
      Rotación 15deg
      Sombra intensa
      Escala 1.1
```

### **Active (Click)**
```
  ➤   ← Círculo morado
      Escala 0.95
      Efecto de onda
```

### **Disabled**
```
  ➤   ← Círculo gris
      Opacidad 0.5
      Sin hover
```

**Animación de Onda**:
```css
.send-btn::before {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transition: width 0.6s, height 0.6s;
}

.send-btn:hover::before {
  width: 100px;
  height: 100px;
}
```

---

## 8️⃣ Avatares - Comparación

### **Antes**
```
Bot:  🌽  ← Avatar Comfi (OK)
User: 👤  ← Emoji simple (Mejorable)
```

### **Después**
```
Bot:  🌽  ← Avatar Comfi
          Gradiente morado
          Sombra rgba(173, 55, 224, 0.3)
          
User: 👤  ← Avatar estilizado
          Gradiente azul #4a90e2
          Sombra rgba(74, 144, 226, 0.3)
          Hover: scale(1.1)
```

**CSS Avatar Usuario**:
```css
.message-avatar.user-avatar {
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.message-avatar.user-avatar::before {
  content: '👤';
  font-size: 1.25rem;
}
```

---

## 9️⃣ Animaciones de Entrada

### **Mensaje Nuevo**
```
Frame 1 (0ms):
  opacity: 0
  transform: translateY(20px) scale(0.95)

Frame 2 (200ms):
  opacity: 0.5
  transform: translateY(10px) scale(0.975)

Frame 3 (400ms):
  opacity: 1
  transform: translateY(0) scale(1)
```

### **Chat Widget Apertura**
```
Frame 1 (0ms):
  transform: scale(0) translateY(50px)
  opacity: 0
  border-radius: 50%

Frame 2 (360ms):
  transform: scale(1.05) translateY(-10px)
  opacity: 0.9
  border-radius: 20px

Frame 3 (600ms):
  transform: scale(1) translateY(0)
  opacity: 1
  border-radius: 20px
```

**Efecto WOW**: El chat "explota" desde el botón flotante con efecto elástico.

---

## 🔟 Responsive - Mobile

```
┌─────────────────────┐
│ Comfi           ✕   │ ← Header
│ ● En línea          │
├─────────────────────┤
│                     │
│      🌽             │
│                     │
│  ¡Hola! Soy Comfi   │
│  Tu asistente de    │
│  Comfama.           │
│                     │
│ ┌─────────────────┐ │
│ │ ⚡ Preguntas    │ │
│ │ frecuentes      │ │
│ │                 │ │
│ │ ┌─────────────┐ │ │
│ │ │ 🏦 ¿Cómo me │ │ │
│ │ │ afilio?     │ │ │
│ │ └─────────────┘ │ │
│ │ ┌─────────────┐ │ │
│ │ │ 💰 ¿Cuáles  │ │ │
│ │ │ son tarifas?│ │ │
│ │ └─────────────┘ │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │ ← 1 columna
│ │ 💰 Ver mi saldo │ │
│ └─────────────────┘ │
│ ┌─────────────────┐ │
│ │ 💸 Hacer transf.│ │
│ └─────────────────┘ │
│                     │
├─────────────────────┤
│ 📷🎤 [Mensaje...] ➤│
└─────────────────────┘
```

**Cambios Mobile**:
- Grid de 2 columnas → 1 columna
- Altura 100vh (pantalla completa)
- Border-radius solo arriba
- Burbujas max-width 85%

---

## 1️⃣1️⃣ Paleta de Colores Visual

```
┌─────────────────────────────────────────┐
│ PRIMARIOS                               │
├─────────────────────────────────────────┤
│ ████ #ad37e0  Morado Comfama (Principal)│
│ ████ #8b2bb3  Morado Oscuro (Hover)     │
│ ████ #4a90e2  Azul Usuario (Avatar)     │
│ ████ #357abd  Azul Oscuro (Hover)       │
├─────────────────────────────────────────┤
│ NEUTROS                                 │
├─────────────────────────────────────────┤
│ ████ #f5f5f7  Gris Fondo               │
│ ████ #e8e8e8  Gris Borde               │
│ ████ #666666  Gris Texto               │
│ ████ #1a1a1a  Negro Texto              │
├─────────────────────────────────────────┤
│ ESTADOS                                 │
├─────────────────────────────────────────┤
│ ████ #f44336  Rojo Error               │
│ ████ #4caf50  Verde Éxito              │
└─────────────────────────────────────────┘
```

---

## 1️⃣2️⃣ Tipografía

```
┌─────────────────────────────────────────┐
│ JERARQUÍA TIPOGRÁFICA                   │
├─────────────────────────────────────────┤
│                                         │
│ H2 - Título Welcome                     │
│ 1.5rem (24px) / Bold / #1a1a1a         │
│ ¡Hola! Soy Comfi                        │
│                                         │
│ Body - Descripción                      │
│ 0.95rem (15px) / Regular / #666         │
│ Tu asistente de Comfama                 │
│                                         │
│ Button - Quick Actions                  │
│ 0.8rem (13px) / SemiBold / #333         │
│ Ver mi saldo                            │
│                                         │
│ Message - Burbujas                      │
│ 0.95rem (15px) / Regular / #1a1a1a      │
│ Tu saldo actual es...                   │
│                                         │
│ Small - Hints                           │
│ 0.75rem (12px) / Regular / #999         │
│ Puedes escribir, hablar o enviar...    │
│                                         │
└─────────────────────────────────────────┘
```

---

## 1️⃣3️⃣ Espaciado Sistema

```
┌─────────────────────────────────────────┐
│ SISTEMA DE ESPACIADO (8px base)         │
├─────────────────────────────────────────┤
│                                         │
│ 0.25rem (4px)   - Gap mínimo           │
│ 0.5rem  (8px)   - Gap pequeño          │
│ 0.75rem (12px)  - Gap medio            │
│ 1rem    (16px)  - Gap estándar         │
│ 1.25rem (20px)  - Gap grande           │
│ 1.5rem  (24px)  - Padding secciones    │
│ 2rem    (32px)  - Separación mayor     │
│                                         │
└─────────────────────────────────────────┘
```

---

## 1️⃣4️⃣ Sombras (Elevación)

```
┌─────────────────────────────────────────┐
│ NIVELES DE ELEVACIÓN                    │
├─────────────────────────────────────────┤
│                                         │
│ Nivel 1 - Burbujas                      │
│ 0 2px 8px rgba(0, 0, 0, 0.06)          │
│ ┌─────────────┐                        │
│ │   Mensaje   │                        │
│ └─────────────┘                        │
│                                         │
│ Nivel 2 - Avatares                      │
│ 0 4px 12px rgba(173, 55, 224, 0.3)     │
│   🌽                                    │
│                                         │
│ Nivel 3 - Hover Quick Actions           │
│ 0 8px 16px rgba(173, 55, 224, 0.15)    │
│ ┌─────────────┐                        │
│ │ Ver mi saldo│ ← Elevado              │
│ └─────────────┘                        │
│                                         │
│ Nivel 4 - Chat Container                │
│ 0 20px 60px rgba(0, 0, 0, 0.3)         │
│                                         │
└─────────────────────────────────────────┘
```

---

## 1️⃣5️⃣ Border Radius

```
┌─────────────────────────────────────────┐
│ SISTEMA DE BORDES REDONDEADOS           │
├─────────────────────────────────────────┤
│                                         │
│ 8px  - Elementos pequeños (badges)     │
│ 10px - FAQ items                        │
│ 12px - Quick actions, inputs            │
│ 16px - FAQ container                    │
│ 18px - Burbujas de mensaje              │
│ 20px - Chat container                   │
│ 24px - Input field                      │
│ 50% - Círculos (avatares, botones)     │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎬 Flujo de Interacción Completo

```
1. Usuario abre chat
   ↓
   [Animación WOW de apertura]
   ↓
2. Ve pantalla de bienvenida
   - Logo Comfi animado
   - FAQ visible sin scroll ✅
   - Quick actions visibles ✅
   ↓
3. Usuario hace clic en FAQ o escribe
   ↓
   [Mensaje aparece con animación]
   ↓
4. Sistema muestra "Comfi está pensando..." ✅
   - Spinner animado
   - Texto pulsante
   ↓
5. Respuesta llega (streaming)
   ↓
   [Texto aparece gradualmente]
   - Cursor parpadeante
   - Avatar animado
   ↓
6. Mensaje completo
   ↓
   [Burbuja final con hover effect]
   ↓
7. Usuario puede continuar conversación
```

---

## ✨ Detalles de Microinteracciones

### **1. Hover en Avatar**
```
Normal: scale(1)
Hover:  scale(1.1) + transition 0.3s
```

### **2. Click en Quick Action**
```
Normal:     translateY(0)
Hover:      translateY(-4px)
Active:     translateY(-2px) + scale(0.98)
```

### **3. Botón Enviar**
```
Normal:     rotate(0deg)
Hover:      rotate(15deg) + scale(1.1)
Active:     scale(0.95)
Enviando:   rotate(360deg) [animación]
```

### **4. Indicador de Procesamiento**
```
Spinner:    rotate(360deg) 0.8s infinite
Texto:      opacity pulse 1.5s infinite
```

### **5. Streaming Text**
```
Cursor:     opacity blink 1s step-end infinite
Burbuja:    box-shadow pulse 1.5s infinite
```

---

## 📊 Comparación Antes/Después

### **Pantalla Inicial**

**ANTES**:
```
┌─────────────────┐
│ Comfi       ✕   │
├─────────────────┤
│                 │
│      🌽         │
│                 │
│ ¡Hola! Soy Comfi│
│                 │
│ [Quick Actions] │
│ [Quick Actions] │
│ [Quick Actions] │
│                 │ ← FAQ no visible
│ [Scroll needed] │    (requiere scroll)
│       ↓         │
├─────────────────┤
│ [Input]     ➤  │
└─────────────────┘
```

**DESPUÉS**:
```
┌─────────────────┐
│ Comfi       ✕   │
├─────────────────┤
│      🌽         │
│ ¡Hola! Soy Comfi│
│                 │
│ [FAQ Section]   │ ← Visible ✅
│ [FAQ Items]     │
│                 │
│ [Quick Actions] │ ← Visible ✅
│ [Quick Actions] │
│ [Quick Actions] │
│                 │
├─────────────────┤
│ [Input]     ➤  │
└─────────────────┘
```

### **Procesamiento**

**ANTES**:
```
Usuario: "¿Cuál es mi saldo?"
         [Enviado]
         
         [Silencio... 3-5 segundos] ❌
         [Usuario confundido]
         
Bot:     "Tu saldo es..."
```

**DESPUÉS**:
```
Usuario: "¿Cuál es mi saldo?"
         [Enviado]
         
Bot:     "⟳ Comfi está pensando..." ✅
         [Feedback inmediato]
         
Bot:     "Tu saldo es..."
         [Streaming con cursor]
```

---

**Documento creado por**: Kiro AI - Diseñador UX/UI
**Proyecto**: CENTLI - Asistente Financiero con IA
**Fecha**: 2024
