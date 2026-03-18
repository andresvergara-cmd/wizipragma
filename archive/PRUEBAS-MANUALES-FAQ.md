# 🧪 Guía de Pruebas Manuales - Sistema FAQ Comfi

**URL:** http://localhost:3001/  
**Estado:** Servidor corriendo ✅

---

## ✅ CHECKLIST DE PRUEBAS

### 1. Welcome Screen (Pantalla Inicial)

**Abrir:** http://localhost:3001/

**Verificar:**
- [ ] Logo de Comfi visible
- [ ] Mensaje "¡Hola! Soy Comfi"
- [ ] Subtítulo "Tu asistente de Comfama"
- [ ] 5 Quick Actions FAQ visibles:
  - [ ] "¿Cómo me afilio?"
  - [ ] "¿Cuál es mi tarifa?"
  - [ ] "Tipos de créditos"
  - [ ] "Requisitos crédito"
  - [ ] "Subsidios disponibles"

### 2. Quick Actions FAQ

**Acción:** Click en "¿Cómo me afilio?"

**Verificar:**
- [ ] Pregunta se envía al chat
- [ ] Aparece en el chat como mensaje del usuario
- [ ] Bot responde (puede ser texto normal por ahora)

### 3. Preguntas Manuales

**Escribir en el chat:**

**Prueba 1:** "¿Cómo me afilio a Comfama?"
- [ ] Mensaje se envía
- [ ] Bot responde

**Prueba 2:** "¿Cuál es mi tarifa?"
- [ ] Mensaje se envía
- [ ] Bot responde

**Prueba 3:** "¿Qué tipos de créditos ofrecen?"
- [ ] Mensaje se envía
- [ ] Bot responde

