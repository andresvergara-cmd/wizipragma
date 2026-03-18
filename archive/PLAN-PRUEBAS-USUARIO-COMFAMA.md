# Plan de Pruebas - Usuario Comfama

## Objetivo
Validar la experiencia de usuario de Comfi desde la perspectiva de un usuario real de Comfama, identificar problemas y proponer mejoras.

## URL de Prueba
https://db4aulosarsdo.cloudfront.net

## Flujos de Prueba

### 1. Flujo de Bienvenida
**Objetivo**: Validar la primera impresión del usuario

**Pasos**:
1. Abrir la aplicación
2. Observar la pantalla de bienvenida
3. Revisar las 6 preguntas frecuentes
4. Verificar que todas sean visibles sin scroll

**Criterios de éxito**:
- ✅ Avatar de Comfi visible y atractivo
- ✅ Mensaje de bienvenida claro
- ✅ 6 preguntas frecuentes visibles sin scroll
- ✅ Diseño limpio y profesional

**Documentar**:
- Primera impresión
- Claridad del mensaje
- Facilidad de navegación
- Sugerencias de mejora

### 2. Flujo de Afiliación
**Objetivo**: Validar respuestas sobre afiliación a Comfama

**Pasos**:
1. Hacer clic en "¿Cómo me afilio?"
2. Leer la respuesta
3. Verificar que la información sea precisa
4. Probar preguntas relacionadas:
   - "¿Qué documentos necesito para afiliarme?"
   - "¿Cuánto tiempo tarda la afiliación?"
   - "¿Mi familia también se afilia?"

**Criterios de éxito**:
- ✅ Respuesta clara y precisa
- ✅ Tarjeta FAQ bien formateada
- ✅ Información útil y accionable
- ✅ Sin texto plano intermedio

**Documentar**:
- Precisión de la información
- Claridad de la respuesta
- Utilidad para el usuario
- Sugerencias de mejora

### 3. Flujo de Tarifas
**Objetivo**: Validar respuestas sobre tarifas de afiliación

**Pasos**:
1. Hacer clic en "¿Cuál es mi tarifa?"
2. Leer la respuesta
3. Verificar que muestre la tarifa correcta (4%)
4. Probar preguntas relacionadas:
   - "¿Quién paga la tarifa?"
   - "¿La tarifa cambia según el salario?"
   - "¿Hay descuentos en la tarifa?"

**Criterios de éxito**:
- ✅ Tarifa correcta (4%)
- ✅ Explicación clara de quién paga
- ✅ Ejemplos útiles
- ✅ Respuesta diferente a la de afiliación

**Documentar**:
- Precisión de la información
- Claridad de ejemplos
- Diferenciación con otras FAQs
- Sugerencias de mejora

### 4. Flujo de Créditos
**Objetivo**: Validar información sobre créditos

**Pasos**:
1. Hacer clic en "Tipos de créditos"
2. Leer la respuesta
3. Verificar que liste los tipos de crédito
4. Hacer clic en "Requisitos crédito"
5. Verificar que muestre requisitos claros
6. Probar preguntas relacionadas:
   - "¿Cuánto puedo pedir prestado?"
   - "¿Cuál es la tasa de interés?"
   - "¿Cuánto tiempo tengo para pagar?"

**Criterios de éxito**:
- ✅ Lista completa de tipos de crédito
- ✅ Requisitos claros y específicos
- ✅ Información útil para tomar decisiones
- ✅ Respuestas diferenciadas

**Documentar**:
- Completitud de la información
- Claridad de requisitos
- Utilidad para el usuario
- Sugerencias de mejora

### 5. Flujo de Subsidios
**Objetivo**: Validar información sobre subsidios

**Pasos**:
1. Hacer clic en "Subsidios disponibles"
2. Leer la respuesta
3. Verificar que liste los subsidios
4. Probar preguntas relacionadas:
   - "¿Cómo solicito un subsidio?"
   - "¿Cuánto es el subsidio de vivienda?"
   - "¿Quién puede solicitar subsidios?"

**Criterios de éxito**:
- ✅ Lista completa de subsidios
- ✅ Montos claros
- ✅ Proceso de solicitud explicado
- ✅ Información actualizada

**Documentar**:
- Completitud de la información
- Claridad de montos
- Facilidad de entender el proceso
- Sugerencias de mejora

### 6. Flujo de Ayuda General
**Objetivo**: Validar respuestas a preguntas generales

**Pasos**:
1. Hacer clic en "Ayuda"
2. Leer la respuesta
3. Probar preguntas variadas:
   - "¿Dónde están las oficinas de Comfama?"
   - "¿Cuál es el horario de atención?"
   - "¿Cómo contacto a Comfama?"
   - "¿Qué servicios ofrece Comfama?"

**Criterios de éxito**:
- ✅ Respuestas útiles y relevantes
- ✅ Información de contacto clara
- ✅ Horarios y ubicaciones precisas
- ✅ Tono amigable y profesional

**Documentar**:
- Utilidad de las respuestas
- Precisión de la información
- Tono y estilo de comunicación
- Sugerencias de mejora

### 7. Flujo de Conversación Continua
**Objetivo**: Validar la capacidad del agente de mantener contexto

**Pasos**:
1. Hacer una pregunta inicial
2. Hacer preguntas de seguimiento sin repetir contexto
3. Verificar que el agente mantenga el contexto
4. Ejemplo:
   - "¿Cómo me afilio?"
   - "¿Y cuánto cuesta?"
   - "¿Qué beneficios obtengo?"

**Criterios de éxito**:
- ✅ Mantiene contexto de la conversación
- ✅ Respuestas coherentes
- ✅ No requiere repetir información
- ✅ Transiciones naturales

**Documentar**:
- Capacidad de mantener contexto
- Coherencia de respuestas
- Naturalidad de la conversación
- Sugerencias de mejora

### 8. Flujo de Errores y Edge Cases
**Objetivo**: Validar manejo de errores y casos límite

**Pasos**:
1. Hacer preguntas fuera del dominio:
   - "¿Cuál es el clima hoy?"
   - "¿Quién es el presidente?"
2. Hacer preguntas ambiguas:
   - "¿Cuánto cuesta?"
   - "¿Dónde está?"
3. Enviar mensajes vacíos
4. Enviar mensajes muy largos

**Criterios de éxito**:
- ✅ Manejo elegante de preguntas fuera del dominio
- ✅ Solicita clarificación cuando es necesario
- ✅ No se rompe con inputs inválidos
- ✅ Mensajes de error claros

**Documentar**:
- Manejo de errores
- Mensajes de error
- Robustez del sistema
- Sugerencias de mejora

## Criterios de Evaluación

### Usabilidad (1-5)
- Facilidad de uso
- Claridad de la interfaz
- Navegación intuitiva
- Accesibilidad

### Contenido (1-5)
- Precisión de la información
- Completitud de las respuestas
- Utilidad para el usuario
- Actualización de datos

### Experiencia (1-5)
- Primera impresión
- Fluidez de la conversación
- Tiempo de respuesta
- Satisfacción general

### Diseño (1-5)
- Estética visual
- Consistencia de marca
- Legibilidad
- Responsive design

## Formato de Reporte

Para cada flujo, documentar:

```markdown
## [Nombre del Flujo]

### Resultado
✅ Exitoso / ⚠️ Con problemas / ❌ Fallido

### Observaciones
- [Observación 1]
- [Observación 2]
- [Observación 3]

### Problemas Identificados
1. [Problema 1]
   - Severidad: Alta/Media/Baja
   - Impacto: [Descripción]
   
2. [Problema 2]
   - Severidad: Alta/Media/Baja
   - Impacto: [Descripción]

### Sugerencias de Mejora
1. [Sugerencia 1]
   - Prioridad: Alta/Media/Baja
   - Esfuerzo: Alto/Medio/Bajo
   - Beneficio esperado: [Descripción]

2. [Sugerencia 2]
   - Prioridad: Alta/Media/Baja
   - Esfuerzo: Alto/Medio/Bajo
   - Beneficio esperado: [Descripción]

### Capturas de Pantalla
[Adjuntar capturas relevantes]

### Calificación
- Usabilidad: [1-5]
- Contenido: [1-5]
- Experiencia: [1-5]
- Diseño: [1-5]
```

## Entregables

1. **Reporte de Pruebas**: Documento con todos los flujos probados
2. **Lista de Problemas**: Priorizada por severidad e impacto
3. **Propuestas de Mejora**: Priorizadas por beneficio y esfuerzo
4. **Capturas de Pantalla**: Evidencia visual de problemas y éxitos
5. **Recomendaciones**: Acciones específicas para mejorar la experiencia

## Próximos Pasos

Después de completar las pruebas:
1. Revisar el reporte con el equipo
2. Priorizar las mejoras
3. Implementar cambios críticos
4. Realizar pruebas de regresión
5. Iterar basándose en feedback
