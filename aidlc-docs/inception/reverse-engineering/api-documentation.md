# API Documentation

## WebSocket API

### Base URL
- **Development**: `wss://{api-id}.execute-api.{region}.amazonaws.com/dev/`
- **QA**: `wss://{api-id}.execute-api.{region}.amazonaws.com/qa/`
- **Production**: `wss://{api-id}.execute-api.{region}.amazonaws.com/prod/`

### Connection Lifecycle

#### Connect
- **Route**: `$connect`
- **Trigger**: Cliente inicia conexión WebSocket
- **Handler**: Lambda Connect
- **Purpose**: Establecer conexión WebSocket
- **Request**: WebSocket handshake
- **Response**: 
  ```json
  {
    "statusCode": 200,
    "body": "Connection Established: {connection_id}"
  }
  ```
- **Side Effects**: Connection ID generado por API Gateway

#### Disconnect
- **Route**: `$disconnect`
- **Trigger**: Cliente cierra conexión o timeout
- **Handler**: Lambda Disconnect
- **Purpose**: Cerrar conexión y limpiar recursos
- **Request**: WebSocket close event
- **Response**: 
  ```json
  {
    "statusCode": 200,
    "body": "Connection closed"
  }
  ```

#### Send Message (Inference)
- **Route**: `sendMessage`
- **Trigger**: Cliente envía mensaje
- **Handler**: Lambda Inference
- **Purpose**: Procesar consulta financiera y retornar respuesta AI
- **Request Format**:
  ```json
  {
    "action": "sendMessage",
    "data": {
      "user_id": "string",
      "message": "string",
      "session_id": "string"
    }
  }
  ```
- **Request Parameters**:
  - `user_id` (required): ID del usuario en DynamoDB
  - `message` (required): Consulta o pregunta del usuario
  - `session_id` (required): ID de sesión para historial de conversación
- **Response**: Streaming de texto vía WebSocket
  - Tokens enviados incrementalmente
  - Respuesta completa acumulada en cliente
- **Response Format**: Plain text (streaming)
- **Side Effects**: 
  - Historial de conversación actualizado en DynamoDB
  - Múltiples llamadas a post_to_connection durante streaming

## Internal APIs

### ConfigChat Class

#### `__init__(self)`
- **Purpose**: Inicializar configuración de chat
- **Parameters**: None
- **Returns**: ConfigChat instance
- **Side Effects**: 
  - Inicializa conexión DynamoDB
  - Carga variables de entorno

#### `get_session_data(self, session_id: str)`
- **Purpose**: Recuperar datos de sesión de DynamoDB
- **Parameters**: 
  - `session_id` (str): ID de sesión a recuperar
- **Returns**: `list` - Lista de items (máximo 1) o lista vacía
- **Exceptions**: Captura y loggea excepciones, retorna []

#### `delete_session(self, session_id: str)`
- **Purpose**: Eliminar sesión de DynamoDB
- **Parameters**: 
  - `session_id` (str): ID de sesión a eliminar
- **Returns**: None
- **Exceptions**: Captura y loggea excepciones

#### `retrieve_chat_history(self, session_id: str)`
- **Purpose**: Recuperar historial completo de conversación
- **Parameters**: 
  - `session_id` (str): ID de sesión
- **Returns**: `dict` - `{session_id: str, conversation: list}`
- **Side Effects**: Elimina sesión existente (patrón delete-then-put)

#### `update_chat_history(self, chat_history: dict, question: str, response: str)`
- **Purpose**: Actualizar historial con nueva interacción
- **Parameters**: 
  - `chat_history` (dict): Historial existente
  - `question` (str): Pregunta del usuario
  - `response` (str): Respuesta del agente
- **Returns**: None
- **Side Effects**: Escribe item actualizado en DynamoDB

#### `limit_conversation_history(self, messages: list, max_turns: int = 5)`
- **Purpose**: Limitar historial para control de tokens
- **Parameters**: 
  - `messages` (list): Lista de mensajes
  - `max_turns` (int): Número máximo de turnos a mantener
- **Returns**: `list` - Mensajes limitados

#### `parse_conversation_history(self, chat_history: list, limit_conversation: bool = False, max_turns: int = 5)`
- **Purpose**: Convertir formato DynamoDB a formato Bedrock
- **Parameters**: 
  - `chat_history` (list): Historial en formato DynamoDB
  - `limit_conversation` (bool): Si limitar historial
  - `max_turns` (int): Número máximo de turnos
- **Returns**: `list` - Mensajes en formato Bedrock
- **Format**: `[{role: "user"|"assistant", content: [{text: str}]}]`

#### `chat_with_bedrock(self, user_query: str, user_context: str, connection_id: str, session_id: str, limit_chat_history: bool = False, max_turns: int = 5)`
- **Purpose**: Orquestar flujo completo de chat con Bedrock
- **Parameters**: 
  - `user_query` (str): Pregunta del usuario
  - `user_context` (str): Contexto completo del usuario
  - `connection_id` (str): ID de conexión WebSocket
  - `session_id` (str): ID de sesión
  - `limit_chat_history` (bool): Si limitar historial
  - `max_turns` (int): Número máximo de turnos
- **Returns**: `str` - Respuesta completa de Bedrock
- **Side Effects**: 
  - Recupera y actualiza historial
  - Envía streaming a WebSocket
- **Exceptions**: Propaga excepciones después de logging

### Bedrock Config Module

#### `get_system_prompt(user_context: str)`
- **Purpose**: Generar system prompt personalizado para Bedrock
- **Parameters**: 
  - `user_context` (str): Contexto completo del usuario
- **Returns**: `str` - System prompt con instrucciones y contexto
- **Prompt Sections**:
  - Rol y objetivo (WiZi financial coach)
  - Contexto completo del usuario
  - Instrucciones principales
  - Estilo, tono y formato
  - Conversión de moneda y datos
  - Límites y seguridad
  - Dimensiones de análisis sugeridas

#### `chat(model_id, user_context, user_message)`
- **Purpose**: Llamada no-streaming a Bedrock
- **Parameters**: 
  - `model_id` (str): ID del modelo Bedrock
  - `user_context` (str): Contexto del usuario
  - `user_message` (str): Mensaje del usuario
- **Returns**: `str` - Respuesta completa de Bedrock
- **API**: bedrock_client.converse()
- **Config**: maxTokens=4000, topP=0.8, temperature=0.6, top_k=60

#### `transmit_response(connection_id, response_chat)`
- **Purpose**: Enviar respuesta a conexión WebSocket
- **Parameters**: 
  - `connection_id` (str): ID de conexión
  - `response_chat` (str): Texto a enviar
- **Returns**: None
- **API**: apigatewaymanagementapi.post_to_connection()

#### `stream_chat(model_id: str, user_context: str, user_message: str, user_hist_conversation: list, connection_id: str)`
- **Purpose**: Llamada streaming a Bedrock con transmisión en tiempo real
- **Parameters**: 
  - `model_id` (str): ID del modelo Bedrock
  - `user_context` (str): Contexto del usuario
  - `user_message` (str): Mensaje del usuario
  - `user_hist_conversation` (list): Historial formateado
  - `connection_id` (str): ID de conexión WebSocket
- **Returns**: `str` - Respuesta completa acumulada
- **API**: bedrock_client.converse_stream()
- **Side Effects**: Transmite cada token vía WebSocket
- **Error Handling**: Retorna mensaje de fallback en caso de error

### Data Config Module

#### `get_user_data(table, primary_key, primary_value: str)`
- **Purpose**: Query DynamoDB por primary key
- **Parameters**: 
  - `table`: Objeto Table de boto3
  - `primary_key` (str): Nombre de la primary key
  - `primary_value` (str): Valor a buscar
- **Returns**: `list` - Item encontrado o lista vacía
- **Limit**: 1 item

#### `scan_table(table)`
- **Purpose**: Scan completo de tabla DynamoDB con paginación
- **Parameters**: 
  - `table`: Objeto Table de boto3
- **Returns**: `list` - Todos los items de la tabla
- **Pagination**: Maneja LastEvaluatedKey automáticamente

#### `format_user_context(user: dict)`
- **Purpose**: Formatear perfil de usuario en texto estructurado
- **Parameters**: 
  - `user` (dict): Datos del usuario de DynamoDB
- **Returns**: `str` - Contexto formateado en secciones
- **Sections**: 
  - Perfil del usuario
  - Información financiera
  - Fechas importantes
  - Hábitos y preferencias
  - Metas financieras

#### `summarize_transactions(transactions, user_id: str, last_transactions: int = 10)`
- **Purpose**: Analizar transacciones y generar resumen
- **Parameters**: 
  - `transactions` (list): Todas las transacciones
  - `user_id` (str): ID del usuario a filtrar
  - `last_transactions` (int): Número de transacciones recientes a mostrar
- **Returns**: `tuple` - (summary_text: str, unique_categories: set)
- **Analysis**: 
  - Resumen mensual por categoría
  - Últimas N transacciones
  - Categorías únicas para matching de retailers

#### `format_retailer_context_pairs(retailers: list, retailers_in_tx: list)`
- **Purpose**: Formatear retailers relevantes según categorías de transacciones
- **Parameters**: 
  - `retailers` (list): Todos los retailers
  - `retailers_in_tx` (list): Categorías de transacciones del usuario
- **Returns**: `str` - Retailers formateados agrupados por industria
- **Filtering**: Solo retailers en categorías del usuario

#### `get_user_context(table_names, user_id: str, last_txn: int = 10)`
- **Purpose**: Orquestar recuperación de contexto completo del usuario
- **Parameters**: 
  - `table_names` (dict): Nombres de tablas DynamoDB
  - `user_id` (str): ID del usuario
  - `last_txn` (int): Número de transacciones recientes
- **Returns**: `str` - Contexto completo combinado
- **Data Sources**: 
  - Perfil de usuario
  - Transacciones con resumen
  - Retailers relevantes

## Data Models

### User Profile Model
- **Table**: user-profile
- **Primary Key**: userId (String)
- **Fields**:
  - `userId`: String - Identificador único
  - `firstName`: String - Nombre
  - `lastName`: String - Apellido
  - `email`: String - Correo electrónico
  - `personalInfo`: Object
    - `location`: String
    - `occupation`: String
    - `birthDate`: String (ISO date)
    - `maritalStatus`: String
    - `children`: Number
  - `financialInfo`: Object
    - `incomeAnnual`: Number (Decimal)
    - `creditScore`: Number
    - `hasMortgage`: Boolean
  - `creditLine`: Object
    - `limit`: Number (Decimal)
    - `available`: Number (Decimal)
    - `isApproved`: Boolean
  - `importantDates`: Object
    - `anniversary`: String (ISO date)
    - `creditCardDueDate`: String
    - `mortgageDueDate`: String
    - `childrenBirthdays`: Array[String]
  - `habits`: Object
    - `preferredPaymentMethod`: String
    - `savingsRate`: Number (Decimal)
    - `investmentStyle`: String
    - `spendingFrequency`: String
    - `shoppingHabits`: Array[String]
  - `preferences`: Object
    - `communicationChannel`: String
    - `language`: String
    - `notificationFrequency`: String
    - `timezone`: String
  - `goals`: Object
    - `shortTerm`: Array[String]
    - `mediumTerm`: Array[String]
    - `longTerm`: Array[String]
    - `targetSavings`: Number (Decimal)

### Transaction Model
- **Table**: transactions
- **Primary Key**: transactionId (String)
- **Fields**:
  - `transactionId`: String - Identificador único
  - `userId`: String - ID del usuario
  - `date`: String (ISO timestamp)
  - `amount`: Number (Decimal) - Monto en USD
  - `industry`: String - Categoría (Groceries, Electronics, etc.)

### Retailer Model
- **Table**: retailers
- **Primary Key**: retailerId (String)
- **Fields**:
  - `retailerId`: String - Identificador único
  - `name`: String - Nombre del retailer
  - `industry`: String - Categoría/industria
  - `benefits`: Array[Object]
    - `description`: String - Descripción del beneficio

### Chat History Model
- **Table**: chat-history
- **Primary Key**: session_id (String)
- **Fields**:
  - `session_id`: String - Identificador de sesión
  - `conversation`: Array[Object]
    - `user_question`: String - Pregunta del usuario
    - `agent_response`: String - Respuesta del agente

## Validation Rules

### WebSocket Message Validation
- `action` field must be "sendMessage"
- `data.user_id` must exist in user-profile table
- `data.message` must be non-empty string
- `data.session_id` must be valid string

### User Context Validation
- User must exist in user-profile table
- Transactions filtered by userId
- Retailers filtered by transaction categories
- All numeric fields converted from Decimal to float/int for formatting

### Bedrock Request Validation
- `model_id` must be valid Bedrock model identifier
- `maxTokens` must be <= 4000
- `temperature` must be between 0 and 1
- `topP` must be between 0 and 1
- `top_k` must be positive integer
