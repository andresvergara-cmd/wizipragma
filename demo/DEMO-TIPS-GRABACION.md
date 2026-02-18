# 🎥 Tips de Grabación - Demo CENTLI

## 🎬 Configuración de Grabación

### Software Recomendado

**Mac**:
- QuickTime Player (gratis, incluido)
- OBS Studio (gratis, más opciones)
- ScreenFlow (pago, profesional)

**Windows**:
- OBS Studio (gratis)
- Camtasia (pago)
- Xbox Game Bar (gratis, incluido en Windows 10/11)

**Linux**:
- OBS Studio (gratis)
- SimpleScreenRecorder (gratis)

### Configuración de Pantalla

**Resolución Recomendada**: 1920x1080 (Full HD)
**Frame Rate**: 30 fps mínimo, 60 fps ideal
**Zoom del Navegador**: 100% (importante para claridad)

### Configuración de Audio

- Usar micrófono externo si es posible
- Grabar en ambiente silencioso
- Hacer prueba de audio antes de grabar
- Volumen: Hablar claro y a volumen normal

---

## 📱 Opciones de Presentación

### Opción 1: Solo Navegador (Recomendado)
**Ventajas**:
- Enfoque total en la aplicación
- Sin distracciones
- Más profesional

**Cómo**:
- Presionar F11 para pantalla completa
- Grabar solo la ventana del navegador
- Zoom 100% o 110% para mejor visibilidad

### Opción 2: Pantalla Completa con Narración
**Ventajas**:
- Muestra contexto completo
- Más natural

**Cómo**:
- Grabar pantalla completa
- Mantener escritorio limpio
- Ocultar barra de tareas/dock si es posible

### Opción 3: Picture-in-Picture
**Ventajas**:
- Conexión personal con audiencia
- Más engagement

**Cómo**:
- Usar OBS o software similar
- Cámara en esquina inferior derecha
- Tamaño: 20-25% de la pantalla

---

## 🎯 Técnicas de Narración

### Tono de Voz
- **Entusiasta pero profesional**
- **Claro y pausado** (no apresurarse)
- **Confiado** (conoces el producto)

### Estructura de Frases
✅ **Bueno**: "Voy a pedirle que envíe $500 a mi mamá"
❌ **Malo**: "Ehh... ahora voy a... bueno, voy a intentar enviar dinero"

✅ **Bueno**: "Como pueden ver, CENTLI ejecutó la transferencia automáticamente"
❌ **Malo**: "Parece que funcionó... creo que sí... sí, funcionó"

### Pausas Estratégicas
- **Después de escribir**: Pausa 1 segundo antes de presionar Enter
- **Durante respuesta**: Dejar que se vea el streaming (no hablar encima)
- **Después de respuesta**: Pausa 2 segundos para que se lea completa

---

## 🎨 Mejoras Visuales

### Cursor
- Usar cursor grande (Configuración > Accesibilidad > Cursor)
- Mover cursor de forma deliberada (no errático)
- Señalar elementos importantes

### Highlights (Opcional)
Si usas software de edición:
- Resaltar Transaction ID con círculo/flecha
- Resaltar saldo actualizado
- Zoom in en detalles importantes

### Transiciones
- Fade in al inicio (1 segundo)
- Fade out al final (1 segundo)
- Sin transiciones entre flujos (mantener continuidad)

---

## 🔧 Troubleshooting Durante Grabación

### Problema: Chat no responde
**Solución Inmediata**:
1. Pausar grabación
2. Hard refresh (Cmd+Shift+R)
3. Esperar 5 segundos
4. Reanudar grabación
5. Decir: "Voy a refrescar la página" (natural)

### Problema: Respuesta con error
**Solución Inmediata**:
1. Pausar grabación
2. Verificar Lambda logs
3. Re-desplegar si es necesario
4. Reanudar grabación desde el inicio del flujo

### Problema: Respuesta lenta (>10 seg)
**Solución Inmediata**:
1. NO pausar grabación
2. Decir: "El sistema está procesando la solicitud..."
3. Esperar hasta 15 segundos
4. Si no responde, pausar y reiniciar

### Problema: Respuesta sin Transaction ID
**Solución Inmediata**:
1. Pausar grabación
2. Verificar deployment con:
   ```bash
   aws lambda get-function --function-name poc-wizi-mex-lambda-inference-model-dev --profile pragma-power-user | grep LastModified
   ```
3. Si es antiguo, re-desplegar:
   ```bash
   ./deploy-tool-use-fix.sh
   ```
4. Esperar 30 segundos
5. Reanudar grabación

---

## 📝 Script de Narración Detallado

### Introducción (5 seg)
```
"Hola, soy [tu nombre] y voy a mostrarles CENTLI, 
un asistente financiero inteligente construido con 
AWS Bedrock y Claude 3.7 Sonnet."
```

### Flujo 1: Setup (10 seg)
```
"Primero, voy a consultar mi saldo actual para 
establecer el contexto."

[Escribir: ¿Cuál es mi saldo?]
[Esperar respuesta]

"Perfecto, tengo $100,000 pesos mexicanos en total."
```

### Flujo 1: Acción (15 seg)
```
"Ahora voy a pedirle a CENTLI que envíe $500 pesos 
a mi mamá. Observen cómo ejecuta la acción 
automáticamente."

[Escribir: Envía $500 a mi mamá]
[Esperar respuesta]

"Excelente! CENTLI ejecutó la transferencia de 
inmediato, sin pedirme confirmaciones adicionales."
```

### Flujo 1: Análisis (15 seg)
```
"Como pueden ver, me proporcionó:
- El ID de transacción: TRF-[leer número]
- Confirmación del monto: $500 pesos
- El destinatario: mi mamá
- Y actualizó mi saldo a $99,500 pesos

Todo esto en lenguaje natural y en español mexicano."
```

### Flujo 2: Transición (5 seg)
```
"Ahora voy a demostrar la segunda capacidad: 
la compra de productos."
```

### Flujo 2: Acción (15 seg)
```
"Voy a pedirle que compre un iPhone 15 Pro."

[Escribir: Quiero comprar un iPhone 15 Pro]
[Esperar respuesta]

"Perfecto! CENTLI procesó la compra automáticamente."
```

### Flujo 2: Análisis (15 seg)
```
"Me proporcionó:
- El número de orden: ORD-[leer número]
- El producto específico: iPhone 15 Pro 256GB
- El precio: $25,999 pesos
- La fecha de entrega: 2-3 días hábiles
- Y descontó el monto de mi saldo

Mi nuevo saldo es $73,501 pesos."
```

### Cierre (10 seg)
```
"Esto demuestra que CENTLI es un verdadero agente 
autónomo que puede ejecutar acciones financieras 
reales. No solo asesora, sino que ejecuta.

Esto es posible gracias a AWS Bedrock, Claude 3.7 
Sonnet, y la capacidad de Tool Use que permite al 
modelo llamar funciones externas.

Gracias por ver esta demostración."
```

---

## ✅ Checklist de Calidad

### Antes de Grabar
- [ ] Practicar el script 2-3 veces
- [ ] Verificar que Lambda esté actualizado
- [ ] Hacer prueba de audio
- [ ] Cerrar notificaciones (Do Not Disturb)
- [ ] Cerrar aplicaciones innecesarias
- [ ] Limpiar escritorio
- [ ] Verificar batería/conexión eléctrica
- [ ] Verificar conexión a internet estable

### Durante la Grabación
- [ ] Hablar claro y pausado
- [ ] Mover cursor de forma deliberada
- [ ] Esperar respuestas completas
- [ ] No apresurarse entre acciones
- [ ] Mantener tono entusiasta

### Después de Grabar
- [ ] Ver el video completo
- [ ] Verificar que audio sea claro
- [ ] Verificar que Transaction IDs sean visibles
- [ ] Verificar que no haya errores
- [ ] Editar si es necesario (cortar pausas largas)

---

## 🎬 Edición Post-Grabación (Opcional)

### Ediciones Básicas
1. **Cortar inicio/final**: Remover preparación y cierre
2. **Cortar pausas largas**: Si hay esperas >5 segundos
3. **Agregar título**: "CENTLI - Agente Autónomo con Tool Use"
4. **Agregar música de fondo**: Suave, no invasiva (opcional)

### Ediciones Avanzadas
1. **Highlights visuales**: Círculos/flechas en IDs importantes
2. **Zoom in**: En Transaction IDs y Order IDs
3. **Subtítulos**: Para mejor accesibilidad
4. **Lower thirds**: Con tu nombre y título
5. **Call to action**: Al final (GitHub, LinkedIn, etc.)

### Software de Edición
- **Básico**: iMovie (Mac), Windows Video Editor (Windows)
- **Intermedio**: DaVinci Resolve (gratis)
- **Avanzado**: Adobe Premiere Pro, Final Cut Pro

---

## 📊 Métricas de Éxito

### Video Exitoso Si:
- ✅ Duración: 2-3 minutos
- ✅ Audio claro y sin ruido
- ✅ Ambos flujos funcionan correctamente
- ✅ Transaction IDs visibles
- ✅ Narración fluida y profesional
- ✅ Sin errores técnicos visibles

### Señales de Re-Grabar:
- ❌ Audio con ruido o muy bajo
- ❌ Errores técnicos (Internal server error)
- ❌ Respuestas sin Transaction IDs
- ❌ Pausas muy largas (>10 seg)
- ❌ Narración confusa o con muchas pausas
- ❌ Cursor errático o distracciones visuales

---

## 🚀 Publicación del Video

### Plataformas Recomendadas
1. **YouTube**: Mejor para demos técnicos
2. **LinkedIn**: Mejor para audiencia profesional
3. **Twitter/X**: Clips cortos (30-60 seg)
4. **GitHub**: Como parte del README

### Título Sugerido
```
CENTLI - Agente Autónomo con AWS Bedrock y Tool Use | Demo
```

### Descripción Sugerida
```
Demo de CENTLI, un asistente financiero inteligente 
construido con AWS Bedrock y Claude 3.7 Sonnet.

En este video muestro cómo CENTLI puede:
✅ Ejecutar transferencias bancarias automáticamente
✅ Procesar compras de productos
✅ Generar IDs de transacción únicos
✅ Responder en lenguaje natural (español mexicano)

Tecnologías:
- AWS Bedrock
- Claude 3.7 Sonnet
- Tool Use (Function Calling)
- WebSocket API Gateway
- AWS Lambda
- DynamoDB

#AWS #Bedrock #AI #AgenticAI #ToolUse #Claude
```

### Thumbnail Sugerido
- Captura de pantalla del chat con Transaction ID visible
- Texto: "CENTLI - Agente Autónomo"
- Logo de AWS Bedrock
- Colores: Morado/Azul (brand de CENTLI)

---

## 💡 Tips Finales

1. **Practica**: Graba 2-3 veces, usa la mejor toma
2. **Sé natural**: No leas el script palabra por palabra
3. **Muestra confianza**: Conoces el producto, demuéstralo
4. **Destaca lo importante**: Transaction IDs, ejecución automática
5. **Mantén ritmo**: No muy rápido, no muy lento
6. **Sonríe**: Se nota en la voz, incluso sin cámara

---

## 🎯 Objetivo del Video

**Mensaje Principal**: 
> "CENTLI no solo entiende intenciones, EJECUTA acciones. Es un verdadero agente autónomo."

**Diferenciador Clave**:
> "Otros chatbots solo asesoran. CENTLI ejecuta transferencias y compras automáticamente, con validaciones de seguridad y confirmaciones claras."

---

¡Buena suerte con la grabación! 🎬🚀
