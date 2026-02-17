# Business Overview

## Business Context Diagram

```
+------------------------------------------------------------------+
|                         USUARIO FINAL                            |
|                    (Cliente Bancario WiZi)                       |
+------------------------------------------------------------------+
                              |
                              | WebSocket
                              v
+------------------------------------------------------------------+
|                    BANKIA FINANCIAL COACH                        |
|                  (Sistema de Asesoría Financiera)                |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |  Análisis de Perfil Financiero                            |  |
|  |  Recomendaciones Personalizadas                           |  |
|  |  Optimización de Beneficios                               |  |
|  |  Gestión de Conversaciones                                |  |
|  +------------------------------------------------------------+  |
|                                                                  |
+------------------------------------------------------------------+
         |                    |                    |
         | Bedrock            | DynamoDB           | API Gateway
         v                    v                    v
+----------------+  +--------------------+  +------------------+
| AWS Bedrock    |  | Datos Usuarios     |  | WebSocket API    |
| Claude 3.7     |  | Transacciones      |  | Real-time        |
| Sonnet         |  | Retailers          |  | Communication    |
|                |  | Historial Chat     |  |                  |
+----------------+  +--------------------+  +------------------+
```

## Business Description

**Business Description**: 
BankIA Financial Coach es un sistema de asesoría financiera conversacional potenciado por Inteligencia Artificial Generativa (GenAI) diseñado para el banco WiZi en México. El sistema actúa como un coach financiero personal llamado "WiZi" que proporciona recomendaciones financieras personalizadas, análisis de patrones de gasto, optimización de beneficios de retailers, y asesoramiento en bienestar financiero basado en el perfil completo del usuario.

**Business Transactions**:

1. **Establecer Sesión de Usuario**
   - Descripción: Crear una conexión WebSocket para iniciar una sesión de chat con el usuario
   - Actores: Usuario final, Sistema
   - Resultado: Conexión activa establecida con ID de sesión

2. **Consulta Financiera Conversacional**
   - Descripción: Usuario envía pregunta o solicitud de asesoría financiera y recibe respuesta personalizada en tiempo real
   - Actores: Usuario final, WiZi (AI Assistant), AWS Bedrock
   - Resultado: Respuesta streaming con recomendaciones personalizadas basadas en perfil, transacciones y beneficios disponibles

3. **Análisis de Perfil Financiero**
   - Descripción: Sistema analiza perfil completo del usuario incluyendo información personal, financiera, transacciones históricas y metas
   - Actores: Sistema, DynamoDB
   - Resultado: Contexto completo del usuario formateado para análisis AI

4. **Optimización de Beneficios de Retailers**
   - Descripción: Sistema identifica retailers relevantes según patrones de gasto del usuario y recomienda mejores beneficios
   - Actores: Sistema, DynamoDB (Retailers, Transactions)
   - Resultado: Recomendaciones de retailers con cashback y beneficios optimizados

5. **Gestión de Historial Conversacional**
   - Descripción: Sistema mantiene y recupera historial de conversaciones para contexto continuo
   - Actores: Sistema, DynamoDB (Chat History)
   - Resultado: Conversaciones persistentes con memoria de interacciones previas

6. **Cerrar Sesión de Usuario**
   - Descripción: Finalizar conexión WebSocket cuando usuario termina sesión
   - Actores: Usuario final, Sistema
   - Resultado: Conexión cerrada y recursos liberados

**Business Dictionary**:

- **WiZi**: Nombre del asistente financiero AI y del banco cliente (WiZi Mex)
- **Coach Financiero**: Rol del sistema como asesor personal de finanzas
- **Perfil Financiero**: Conjunto completo de datos del usuario incluyendo información personal, ingresos, crédito, hábitos, metas
- **Contexto de Usuario**: Información consolidada del usuario formateada para análisis AI
- **Transacción**: Registro de gasto del usuario con fecha, monto, categoría/industria
- **Retailer**: Comercio o establecimiento que ofrece beneficios (cashback, descuentos) a usuarios
- **Beneficio**: Ventaja financiera (cashback, descuento, promoción) ofrecida por retailer
- **Sesión**: Conexión WebSocket activa con historial de conversación asociado
- **Streaming**: Transmisión en tiempo real de respuesta AI token por token
- **Industria/Categoría**: Clasificación de transacciones y retailers (Groceries, Electronics, etc.)
- **Score Crediticio**: Puntaje de crédito del usuario (credit score)
- **Línea de Crédito**: Límite y disponibilidad de crédito del usuario

## Component Level Business Descriptions

### Lambda Connect (app_connect)
- **Purpose**: Establecer conexión WebSocket inicial cuando usuario inicia sesión de chat
- **Responsibilities**: 
  - Aceptar solicitud de conexión WebSocket
  - Generar y retornar connection ID
  - Confirmar establecimiento de conexión

### Lambda Disconnect (app_disconnect)
- **Purpose**: Cerrar conexión WebSocket cuando usuario finaliza sesión
- **Responsibilities**:
  - Procesar evento de desconexión
  - Liberar recursos de conexión
  - Confirmar cierre exitoso

### Lambda Inference (app_inference)
- **Purpose**: Procesar consultas financieras del usuario y generar respuestas personalizadas usando AI
- **Responsibilities**:
  - Recibir mensaje del usuario vía WebSocket
  - Recuperar contexto completo del usuario (perfil, transacciones, retailers)
  - Recuperar historial de conversación
  - Invocar AWS Bedrock con contexto y prompt del sistema
  - Transmitir respuesta streaming en tiempo real
  - Actualizar historial de conversación
  - Gestionar sesiones de chat

### DynamoDB Tables
- **chat-history**: Almacenar historial de conversaciones por sesión
- **user-profile**: Almacenar perfiles completos de usuarios con información personal y financiera
- **transactions**: Almacenar transacciones históricas de usuarios
- **retailers**: Almacenar catálogo de retailers con beneficios disponibles

### API Gateway WebSocket
- **Purpose**: Proporcionar comunicación bidireccional en tiempo real entre usuario y sistema
- **Responsibilities**:
  - Gestionar conexiones WebSocket
  - Enrutar mensajes a Lambda functions apropiadas
  - Transmitir respuestas streaming a clientes conectados
