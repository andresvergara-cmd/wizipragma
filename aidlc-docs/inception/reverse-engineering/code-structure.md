# Code Structure

## Build System
- **Type**: Poetry (Python package manager)
- **Configuration**: pyproject.toml
- **Python Version**: >=3.9, <3.9.7 || >3.9.7, <3.11
- **Build Backend**: poetry.core.masonry.api
- **Deployment**: AWS SAM (Serverless Application Model)
- **Infrastructure**: CloudFormation via SAM template

## Project Structure

```
workspace-root/
├── src_aws/                          # Application code
│   ├── app_connect/                  # WebSocket connect handler
│   │   └── app_connect.py
│   ├── app_disconnect/               # WebSocket disconnect handler
│   │   └── app_disconnect.py
│   └── app_inference/                # Core inference logic
│       ├── app.py                    # Main Lambda handler
│       ├── bedrock_config.py         # Bedrock AI integration
│       ├── config.py                 # Chat configuration & history
│       └── data_config.py            # Data retrieval & formatting
├── data/                             # Sample/seed data
│   ├── users_mx.json
│   ├── transactions_mx.json
│   └── stores_mx.json
├── commands/                         # Deployment scripts
│   └── deploy.sh
├── notebooks/                        # Development/testing notebooks
│   └── test.ipynb
├── gen2/                             # (Empty - future use)
├── poc_template.yaml                 # SAM infrastructure template
├── pyproject.toml                    # Poetry dependencies
├── poetry.lock                       # Locked dependencies
└── index.html                        # (Likely frontend/demo)
```

## Module Hierarchy

```
app_inference (Core Module)
├── app.py (Entry Point)
│   ├── Imports: config, data_config
│   └── Handler: lambda_handler(event, context)
│       ├── Parse WebSocket event
│       ├── Call: get_user_context()
│       └── Call: config.chat_with_bedrock()
│
├── config.py (Chat Management)
│   ├── Class: ConfigChat
│   │   ├── __init__(): Initialize tables and model
│   │   ├── get_session_data(): Query chat history
│   │   ├── delete_session(): Remove session
│   │   ├── retrieve_chat_history(): Get conversation
│   │   ├── update_chat_history(): Save interaction
│   │   ├── limit_conversation_history(): Truncate history
│   │   ├── parse_conversation_history(): Format for Bedrock
│   │   └── chat_with_bedrock(): Main orchestration
│   └── Imports: bedrock_config.stream_chat
│
├── bedrock_config.py (AI Integration)
│   ├── get_system_prompt(): Generate system prompt
│   ├── chat(): Non-streaming Bedrock call
│   ├── transmit_response(): Send to WebSocket
│   └── stream_chat(): Streaming Bedrock call
│
└── data_config.py (Data Layer)
    ├── get_user_data(): Query DynamoDB by key
    ├── scan_table(): Full table scan
    ├── format_user_context(): Format user profile
    ├── summarize_transactions(): Analyze spending
    ├── format_retailer_context_pairs(): Format retailers
    └── get_user_context(): Orchestrate all data
```

## Existing Files Inventory

### Application Code (Candidates for Modification)

#### WebSocket Handlers
- `src_aws/app_connect/app_connect.py` - Establece conexión WebSocket, retorna connection ID
- `src_aws/app_disconnect/app_disconnect.py` - Cierra conexión WebSocket, limpia recursos

#### Core Inference Module
- `src_aws/app_inference/app.py` - Handler principal Lambda, orquesta flujo de inferencia
- `src_aws/app_inference/config.py` - Gestión de configuración, historial de chat, orquestación Bedrock
- `src_aws/app_inference/bedrock_config.py` - Integración AWS Bedrock, streaming, system prompts
- `src_aws/app_inference/data_config.py` - Capa de datos, formateo de contexto, análisis transacciones

### Infrastructure
- `poc_template.yaml` - Template SAM/CloudFormation con toda la infraestructura AWS
- `commands/deploy.sh` - Script de deployment automatizado

### Configuration
- `pyproject.toml` - Dependencias Poetry y configuración del proyecto
- `poetry.lock` - Versiones locked de dependencias

### Data/Testing
- `data/users_mx.json` - Datos de ejemplo de usuarios
- `data/transactions_mx.json` - Datos de ejemplo de transacciones
- `data/stores_mx.json` - Datos de ejemplo de retailers
- `notebooks/test.ipynb` - Notebook para testing/desarrollo
- `index.html` - Posible frontend o demo page

### Empty/Future
- `gen2/` - Directorio vacío para uso futuro

## Design Patterns

### Pattern: Lambda Handler Pattern
- **Location**: Todos los archivos app_*.py
- **Purpose**: Punto de entrada estándar para AWS Lambda
- **Implementation**: 
  - Función `lambda_handler(event, context)`
  - Parse event para extraer datos
  - Ejecutar lógica de negocio
  - Retornar response con statusCode y body

### Pattern: Configuration Singleton
- **Location**: config.py (instancia `config` al final del módulo)
- **Purpose**: Compartir configuración y recursos AWS entre invocaciones
- **Implementation**: 
  - Clase ConfigChat con inicialización de recursos
  - Instancia global `config = ConfigChat()`
  - Reutilización de conexiones boto3

### Pattern: Service Layer
- **Location**: bedrock_config.py, data_config.py
- **Purpose**: Separar lógica de negocio de integración con servicios
- **Implementation**: 
  - Funciones especializadas por servicio (Bedrock, DynamoDB)
  - Abstracción de APIs de AWS
  - Formateo de datos específico por servicio

### Pattern: Context Builder
- **Location**: data_config.py (get_user_context, format_* functions)
- **Purpose**: Construir contexto completo del usuario desde múltiples fuentes
- **Implementation**: 
  - Recuperar datos de múltiples tablas
  - Formatear cada sección (perfil, transacciones, retailers)
  - Combinar en contexto unificado para AI

### Pattern: Streaming Response
- **Location**: bedrock_config.py (stream_chat, transmit_response)
- **Purpose**: Enviar respuesta AI en tiempo real token por token
- **Implementation**: 
  - Bedrock converse_stream API
  - Iterar sobre chunks de respuesta
  - Transmitir cada chunk vía WebSocket

### Pattern: Conversation History Management
- **Location**: config.py (retrieve, update, parse, limit methods)
- **Purpose**: Mantener contexto conversacional entre interacciones
- **Implementation**: 
  - Recuperar historial de DynamoDB
  - Formatear para Bedrock (role: user/assistant)
  - Limitar a N turnos para control de tokens
  - Actualizar con nueva interacción
  - Patrón delete-then-put para actualización

## Critical Dependencies

### boto3
- **Version**: ^1.34.149
- **Usage**: SDK de AWS para Python
- **Purpose**: Interactuar con todos los servicios AWS (Bedrock, DynamoDB, API Gateway)
- **Clients Used**: 
  - bedrock-runtime (Bedrock AI)
  - bedrock-agent-runtime (Agents)
  - dynamodb (resource y client)
  - apigatewaymanagementapi (WebSocket management)

### langchain-aws
- **Version**: ^0.2.0
- **Usage**: Integración LangChain con AWS
- **Purpose**: Facilitar integración con Bedrock y otros servicios AWS
- **Location**: Lambda Layer (pragma-bankia-layer-dev)

### loguru
- **Version**: ^0.7.2
- **Usage**: Logging avanzado
- **Purpose**: Logging estructurado y debugging
- **Location**: Lambda Layer y pyproject.toml

### requests
- **Version**: ^2.32.3
- **Usage**: HTTP client
- **Purpose**: Llamadas HTTP (posiblemente para testing o integraciones futuras)

### python-dotenv
- **Version**: ^1.0.1
- **Usage**: Gestión de variables de entorno
- **Purpose**: Cargar configuración desde archivos .env en desarrollo

### pandas
- **Version**: 2.1.1
- **Usage**: Análisis de datos
- **Purpose**: Procesamiento de datos en notebooks o análisis avanzado

### streamlit
- **Version**: ^1.47.0
- **Usage**: Framework de aplicaciones web
- **Purpose**: Posible frontend o demo interactiva

### tqdm
- **Version**: ^4.66.4
- **Usage**: Progress bars
- **Purpose**: Visualización de progreso en scripts o notebooks

### ipykernel
- **Version**: ^6.29.5
- **Usage**: Jupyter kernel
- **Purpose**: Soporte para notebooks de desarrollo/testing

## Code Organization Principles

1. **Separation of Concerns**: 
   - Handlers separados por tipo de evento (connect, disconnect, inference)
   - Módulos especializados por responsabilidad (config, bedrock, data)

2. **Serverless Best Practices**:
   - Inicialización de recursos fuera del handler
   - Reutilización de conexiones boto3
   - Lambda Layers para dependencias pesadas

3. **Data Formatting**:
   - Funciones dedicadas para formatear cada tipo de dato
   - Contexto estructurado en secciones legibles
   - Separación de recuperación y formateo

4. **Error Handling**:
   - Try-except en operaciones críticas
   - Logging de errores con loguru
   - Retorno de valores por defecto en caso de error

5. **Configuration Management**:
   - Variables de entorno para configuración
   - Hardcoded table names (consideración de mejora)
   - Parámetros SAM para deployment
