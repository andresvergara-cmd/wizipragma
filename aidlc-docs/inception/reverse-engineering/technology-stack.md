# Technology Stack

## Programming Languages

### Python
- **Version**: 3.9-3.10 (excluding 3.9.7, max 3.11)
- **Usage**: Toda la lógica de aplicación backend
- **Components**: 
  - Lambda Functions (3)
  - Business logic modules (4)
  - Notebooks de desarrollo
- **Justification**: Lenguaje estándar para AWS Lambda, excelente ecosistema para AI/ML

## Frameworks & Libraries

### AWS SDK (boto3)
- **Version**: ^1.34.149
- **Purpose**: SDK oficial de AWS para Python
- **Usage**: 
  - Interacción con Bedrock (bedrock-runtime, bedrock-agent-runtime)
  - Operaciones DynamoDB (resource y client)
  - API Gateway Management (apigatewaymanagementapi)
- **Criticality**: Core - toda la integración AWS depende de esto

### LangChain AWS
- **Version**: ^0.2.0
- **Purpose**: Framework para aplicaciones LLM con integración AWS
- **Usage**: Facilitar integración con AWS Bedrock y otros servicios
- **Location**: Lambda Layer (pragma-bankia-layer-dev)
- **Criticality**: High - simplifica integración con Bedrock

### Loguru
- **Version**: ^0.7.2
- **Purpose**: Logging avanzado y estructurado
- **Usage**: Logging en todos los módulos de aplicación
- **Location**: Lambda Layer y pyproject.toml
- **Criticality**: Medium - importante para debugging y monitoring

### Requests
- **Version**: ^2.32.3
- **Purpose**: HTTP client library
- **Usage**: Posibles integraciones HTTP o testing
- **Criticality**: Low - no usado en código principal actual

### Python-dotenv
- **Version**: ^1.0.1
- **Purpose**: Gestión de variables de entorno
- **Usage**: Cargar configuración desde .env en desarrollo
- **Criticality**: Low - solo desarrollo local

### Pandas
- **Version**: 2.1.1
- **Purpose**: Análisis y manipulación de datos
- **Usage**: Notebooks de desarrollo, análisis de datos
- **Criticality**: Low - solo desarrollo/testing

### Streamlit
- **Version**: ^1.47.0
- **Purpose**: Framework para aplicaciones web interactivas
- **Usage**: Posible frontend demo o interfaz de testing
- **Criticality**: Low - no parte del core backend

### tqdm
- **Version**: ^4.66.4
- **Purpose**: Progress bars para iteraciones
- **Usage**: Scripts de desarrollo, notebooks
- **Criticality**: Low - solo desarrollo

### ipykernel
- **Version**: ^6.29.5
- **Purpose**: Jupyter kernel para notebooks
- **Usage**: Soporte para notebooks de desarrollo
- **Criticality**: Low - solo desarrollo

## Infrastructure Services

### AWS Lambda
- **Purpose**: Compute serverless para toda la lógica de aplicación
- **Usage**: 
  - 3 Lambda Functions (Connect, Disconnect, Inference)
  - Runtime: Python 3.10
  - Memory: 512 MB (connect/disconnect), 1024 MB (inference)
  - Timeout: 60s (connect/disconnect), 600s (inference)
- **Criticality**: Core - toda la aplicación corre en Lambda

### AWS API Gateway
- **Type**: WebSocket API
- **Purpose**: Gateway para comunicación bidireccional en tiempo real
- **Usage**: 
  - Gestión de conexiones WebSocket
  - Routing de eventos ($connect, $disconnect, sendMessage)
  - Transmisión de respuestas streaming
- **Criticality**: Core - punto de entrada de la aplicación

### AWS DynamoDB
- **Purpose**: Base de datos NoSQL serverless
- **Usage**: 
  - 4 Tables: chat-history, user-profile, transactions, retailers
  - Access patterns: Query por primary key, Scan completo
  - Consistency: Eventually consistent
- **Criticality**: Core - toda la persistencia de datos

### AWS Bedrock
- **Model**: Claude 3.7 Sonnet (us.anthropic.claude-3-7-sonnet-20250219-v1:0)
- **Purpose**: Servicio de GenAI para respuestas conversacionales
- **API**: converse_stream (streaming), converse (non-streaming)
- **Configuration**:
  - maxTokens: 4000
  - topP: 0.8
  - temperature: 0.6
  - top_k: 60
- **Criticality**: Core - cerebro de la aplicación

### AWS Lambda Layers
- **Layer Name**: pragma-bankia-layer-dev
- **Version**: 1
- **Purpose**: Compartir dependencias pesadas entre Lambda functions
- **Contents**: langchain-aws, loguru
- **Criticality**: High - reduce tamaño de deployment packages

### AWS CloudFormation / SAM
- **Purpose**: Infrastructure as Code
- **Usage**: Definir y desplegar toda la infraestructura
- **Template**: poc_template.yaml
- **Criticality**: Core - gestión de infraestructura

### AWS IAM
- **Purpose**: Gestión de permisos y roles
- **Usage**: 
  - Roles de ejecución para Lambda functions
  - Policies para acceso a Bedrock, DynamoDB, API Gateway
- **Criticality**: Core - seguridad y autorización

## Build Tools

### Poetry
- **Version**: Latest (via pyproject.toml)
- **Purpose**: Gestión de dependencias y packaging Python
- **Usage**: 
  - Definir dependencias del proyecto
  - Lock de versiones (poetry.lock)
  - Build de packages
- **Criticality**: High - gestión de dependencias

### AWS SAM CLI
- **Purpose**: CLI para desarrollo y deployment serverless
- **Usage**: 
  - Build de aplicaciones SAM
  - Deployment a AWS
  - Testing local (opcional)
- **Criticality**: High - deployment de aplicación

### Bash
- **Purpose**: Scripting de deployment
- **Usage**: deploy.sh para automatización
- **Criticality**: Medium - automatización de deployment

## Development Tools

### Jupyter Notebook
- **Purpose**: Desarrollo interactivo y testing
- **Usage**: test.ipynb para experimentación
- **Criticality**: Low - solo desarrollo

### Git (Implied)
- **Purpose**: Control de versiones
- **Usage**: Gestión de código fuente
- **Criticality**: High - colaboración y versionado

## Testing Tools

### (None Detected)
- **Status**: No se detectaron frameworks de testing (pytest, unittest, etc.)
- **Gap**: Falta de tests automatizados
- **Recommendation**: Agregar pytest para unit tests

## Monitoring & Observability

### AWS CloudWatch (Implied)
- **Purpose**: Logging y monitoring
- **Usage**: 
  - Logs de Lambda functions
  - Métricas de API Gateway
  - Métricas de DynamoDB
- **Criticality**: High - debugging y monitoring

### Loguru
- **Purpose**: Structured logging
- **Usage**: Logging en código de aplicación
- **Integration**: Logs van a CloudWatch
- **Criticality**: Medium - debugging

## Security

### AWS IAM
- **Purpose**: Autenticación y autorización
- **Usage**: Roles y policies para servicios AWS
- **Criticality**: Core

### (No Authentication on WebSocket)
- **Status**: WebSocket API sin autenticación (AuthorizationType: NONE)
- **Gap**: Falta de autenticación de usuarios
- **Recommendation**: Agregar Lambda Authorizer o Cognito

## Data Formats

### JSON
- **Usage**: 
  - Formato de datos en DynamoDB
  - Request/response de API
  - Archivos de datos de ejemplo
- **Criticality**: Core

### YAML
- **Usage**: SAM template (CloudFormation)
- **Criticality**: High - definición de infraestructura

### TOML
- **Usage**: pyproject.toml (Poetry configuration)
- **Criticality**: Medium - configuración de build

## Architecture Patterns

### Serverless
- **Pattern**: Event-driven serverless architecture
- **Benefits**: Auto-scaling, pay-per-use, no server management
- **Components**: Lambda, API Gateway, DynamoDB

### Microservices
- **Pattern**: Funciones Lambda independientes por responsabilidad
- **Benefits**: Separación de concerns, deployment independiente
- **Components**: 3 Lambda functions con responsabilidades específicas

### Event-Driven
- **Pattern**: WebSocket events trigger Lambda functions
- **Benefits**: Real-time processing, loose coupling
- **Components**: API Gateway routes → Lambda handlers

### Streaming
- **Pattern**: Token-by-token streaming de respuestas AI
- **Benefits**: Mejor UX, respuestas en tiempo real
- **Components**: Bedrock converse_stream → WebSocket transmission

## Technology Maturity

### Production-Grade
- AWS Lambda, API Gateway, DynamoDB, Bedrock (servicios managed)
- boto3, Python 3.10 (tecnologías maduras)

### Emerging/Modern
- AWS Bedrock (servicio relativamente nuevo, 2023)
- Claude 3.7 Sonnet (modelo reciente, 2025)
- LangChain (framework en evolución rápida)

### Development-Only
- Jupyter, Streamlit, Pandas (no en producción)

## Deployment Architecture

### Stages
- **dev**: Desarrollo
- **qa**: Quality Assurance
- **prod**: Producción

### Deployment Method
- Infrastructure: AWS SAM / CloudFormation
- Code: Lambda deployment packages (CodeUri)
- Dependencies: Lambda Layers

### CI/CD
- **Status**: Script manual (deploy.sh)
- **Gap**: No CI/CD pipeline automatizado detectado
- **Recommendation**: Agregar GitHub Actions, AWS CodePipeline, o similar
