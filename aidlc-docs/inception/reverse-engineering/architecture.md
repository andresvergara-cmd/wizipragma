# System Architecture

## System Overview

BankIA Financial Coach es una aplicación serverless construida en AWS que proporciona asesoría financiera conversacional en tiempo real. La arquitectura utiliza un patrón event-driven con comunicación WebSocket para streaming de respuestas AI, Lambda functions para procesamiento, DynamoDB para persistencia, y AWS Bedrock para capacidades de GenAI.

El sistema está diseñado para escalar automáticamente, procesar consultas en tiempo real, y proporcionar respuestas personalizadas basadas en análisis completo del perfil financiero del usuario.

## Architecture Diagram

```
                                    USUARIO
                                      |
                                      | wss://
                                      v
                        +---------------------------+
                        |   API Gateway WebSocket   |
                        |   Routes: $connect,       |
                        |   $disconnect, sendMessage|
                        +---------------------------+
                          |           |           |
              $connect    |           |           |  sendMessage
                          v           v           v
                    +----------+ +----------+ +----------------+
                    | Lambda   | | Lambda   | | Lambda         |
                    | Connect  | |Disconnect| | Inference      |
                    +----------+ +----------+ +----------------+
                                                    |
                                    +---------------+---------------+
                                    |               |               |
                                    v               v               v
                            +------------+  +------------+  +------------+
                            | DynamoDB   |  | DynamoDB   |  | DynamoDB   |
                            | Users      |  |Transactions|  | Retailers  |
                            +------------+  +------------+  +------------+
                                    |
                                    v
                            +------------+
                            | DynamoDB   |
                            | ChatHistory|
                            +------------+
                                    |
                                    v
                            +------------------+
                            | AWS Bedrock      |
                            | Claude 3.7 Sonnet|
                            | (Converse Stream)|
                            +------------------+
                                    |
                                    | Streaming Response
                                    v
                            [API Gateway Management]
                                    |
                                    v
                                  USUARIO
```

## Component Descriptions

### API Gateway WebSocket
- **Purpose**: Punto de entrada para comunicación bidireccional en tiempo real
- **Responsibilities**: 
  - Gestionar ciclo de vida de conexiones WebSocket
  - Enrutar eventos a Lambda functions
  - Transmitir respuestas streaming a clientes
- **Dependencies**: Lambda Connect, Lambda Disconnect, Lambda Inference
- **Type**: Infrastructure/Gateway
- **Configuration**: 
  - Protocol: WEBSOCKET
  - Routes: $connect, $disconnect, sendMessage
  - Stage: dev/qa/prod

### Lambda Connect Function
- **Purpose**: Establecer conexión WebSocket
- **Responsibilities**: 
  - Procesar evento $connect
  - Retornar connection ID
  - Confirmar establecimiento exitoso
- **Dependencies**: API Gateway WebSocket
- **Type**: Application/Handler
- **Runtime**: Python 3.10
- **Memory**: 512 MB
- **Timeout**: 60 seconds
- **Handler**: app_connect.lambda_handler

### Lambda Disconnect Function
- **Purpose**: Cerrar conexión WebSocket
- **Responsibilities**: 
  - Procesar evento $disconnect
  - Limpiar recursos de conexión
  - Confirmar cierre exitoso
- **Dependencies**: API Gateway WebSocket
- **Type**: Application/Handler
- **Runtime**: Python 3.10
- **Memory**: 512 MB
- **Timeout**: 60 seconds
- **Handler**: app_disconnect.lambda_handler

### Lambda Inference Function
- **Purpose**: Procesar consultas y generar respuestas AI personalizadas
- **Responsibilities**: 
  - Recibir y parsear mensaje del usuario
  - Recuperar contexto completo del usuario
  - Gestionar historial de conversación
  - Invocar AWS Bedrock con streaming
  - Transmitir respuesta en tiempo real
  - Actualizar historial de chat
- **Dependencies**: 
  - API Gateway WebSocket (recibir/enviar)
  - DynamoDB Tables (todos)
  - AWS Bedrock
  - Lambda Layer (langchain, loguru)
- **Type**: Application/Core Business Logic
- **Runtime**: Python 3.10
- **Memory**: 1024 MB
- **Timeout**: 600 seconds (10 min)
- **Handler**: app.lambda_handler
- **Layers**: pragma-bankia-layer-dev (langchain-aws, loguru)

### DynamoDB Table: chat-history
- **Purpose**: Persistir historial de conversaciones
- **Responsibilities**: 
  - Almacenar conversaciones por session_id
  - Recuperar historial para contexto continuo
  - Eliminar sesiones al actualizar
- **Dependencies**: Lambda Inference
- **Type**: Data Store/NoSQL
- **Primary Key**: session_id (String)
- **Schema**: 
  - session_id: String
  - conversation: List[{user_question: String, agent_response: String}]

### DynamoDB Table: user-profile
- **Purpose**: Almacenar perfiles completos de usuarios
- **Responsibilities**: 
  - Mantener información personal y financiera
  - Proporcionar contexto de usuario para análisis
- **Dependencies**: Lambda Inference
- **Type**: Data Store/NoSQL
- **Primary Key**: userId (String)
- **Schema**: 
  - userId, firstName, lastName, email
  - personalInfo: {location, occupation, birthDate, maritalStatus, children}
  - financialInfo: {incomeAnnual, creditScore, hasMortgage}
  - creditLine: {limit, available, isApproved}
  - importantDates: {anniversary, creditCardDueDate, mortgageDueDate, childrenBirthdays}
  - habits: {preferredPaymentMethod, savingsRate, investmentStyle, spendingFrequency, shoppingHabits}
  - preferences: {communicationChannel, language, notificationFrequency, timezone}
  - goals: {shortTerm, mediumTerm, longTerm, targetSavings}

### DynamoDB Table: transactions
- **Purpose**: Almacenar transacciones históricas de usuarios
- **Responsibilities**: 
  - Registrar gastos por usuario
  - Proporcionar datos para análisis de patrones
  - Identificar categorías de gasto
- **Dependencies**: Lambda Inference
- **Type**: Data Store/NoSQL
- **Primary Key**: transactionId (String)
- **Schema**: 
  - transactionId, userId, date, amount, industry

### DynamoDB Table: retailers
- **Purpose**: Catálogo de retailers con beneficios
- **Responsibilities**: 
  - Almacenar información de retailers
  - Mantener beneficios disponibles por industria
  - Proporcionar datos para recomendaciones
- **Dependencies**: Lambda Inference
- **Type**: Data Store/NoSQL
- **Primary Key**: retailerId (String)
- **Schema**: 
  - retailerId, name, industry
  - benefits: List[{description: String}]

### AWS Bedrock
- **Purpose**: Proporcionar capacidades de GenAI para respuestas conversacionales
- **Responsibilities**: 
  - Procesar prompts con contexto de usuario
  - Generar respuestas personalizadas
  - Streaming de tokens en tiempo real
- **Dependencies**: Lambda Inference
- **Type**: External Service/AI/ML
- **Model**: us.anthropic.claude-3-7-sonnet-20250219-v1:0
- **API**: converse_stream
- **Configuration**:
  - maxTokens: 4000
  - topP: 0.8
  - temperature: 0.6
  - top_k: 60

## Data Flow

### Consulta Financiera (Happy Path)

```
Usuario -> WebSocket -> API Gateway -> Lambda Inference
                                            |
                                            v
                                    [Parse Request]
                                    user_id, message, session_id
                                            |
                                            v
                                    [Get User Context]
                                            |
                        +-------------------+-------------------+
                        |                   |                   |
                        v                   v                   v
                DynamoDB Users    DynamoDB Transactions  DynamoDB Retailers
                        |                   |                   |
                        +-------------------+-------------------+
                                            |
                                            v
                                [Format Complete Context]
                                            |
                                            v
                                [Retrieve Chat History]
                                            |
                                            v
                                    DynamoDB ChatHistory
                                            |
                                            v
                                [Invoke Bedrock Stream]
                                            |
                                            v
                                    AWS Bedrock Claude
                                            |
                                            v
                                [Stream Tokens to User]
                                            |
                                            v
                            API Gateway Management (post_to_connection)
                                            |
                                            v
                                        Usuario
                                            |
                                            v
                                [Update Chat History]
                                            |
                                            v
                                    DynamoDB ChatHistory
```

## Integration Points

### External APIs
- **AWS Bedrock API**: Servicio de GenAI para procesamiento de lenguaje natural y generación de respuestas
  - Endpoint: bedrock-runtime
  - Method: converse_stream
  - Purpose: Generar respuestas conversacionales personalizadas

- **API Gateway Management API**: Control de conexiones WebSocket
  - Endpoint: execute-api.{region}.amazonaws.com/{stage}
  - Method: post_to_connection
  - Purpose: Enviar mensajes a conexiones WebSocket activas

### Databases
- **DynamoDB**: Base de datos NoSQL serverless para todos los datos
  - Tables: chat-history, user-profile, transactions, retailers
  - Access Pattern: Query por primary key, Scan para análisis completo
  - Purpose: Persistencia de datos de usuarios, transacciones, retailers e historial

### Third-party Services
- **AWS Lambda**: Compute serverless para toda la lógica de negocio
- **AWS API Gateway**: Gateway para WebSocket y gestión de conexiones
- **AWS Bedrock**: Servicio de AI/ML para GenAI
- **AWS CloudFormation/SAM**: Infrastructure as Code para deployment

## Infrastructure Components

### SAM Template (poc_template.yaml)
- **Purpose**: Definir toda la infraestructura como código
- **Resources**: 
  - 4 DynamoDB Tables
  - 3 Lambda Functions
  - 1 WebSocket API
  - Routes, Integrations, Permissions
- **Parameters**: Stage, ProjectName, ModelId, LayerSelected
- **Outputs**: ConnectionsURL, WebSocketURL

### Deployment Model
- **Type**: AWS SAM (Serverless Application Model)
- **Stages**: dev, qa, prod
- **Deployment**: CloudFormation stack deployment
- **Build System**: Poetry para dependencias Python
- **Commands**: deploy.sh script para automatización

### Networking
- **VPC**: No configurado (Lambda en VPC pública de AWS)
- **Security**: 
  - IAM Roles para Lambda functions
  - Policies para Bedrock, DynamoDB, API Gateway
  - WebSocket sin autenticación (NONE) - consideración de seguridad
- **Endpoints**: 
  - WebSocket: wss://{api-id}.execute-api.{region}.amazonaws.com/{stage}/
  - Management: https://{api-id}.execute-api.{region}.amazonaws.com/{stage}
