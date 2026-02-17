# Dependencies

## Internal Dependencies Diagram

```
                    +------------------+
                    |  API Gateway WS  |
                    +------------------+
                      |      |      |
          $connect    |      |      |  sendMessage
                      v      v      v
              +--------+  +--------+  +------------------+
              | Lambda |  | Lambda |  | Lambda Inference |
              |Connect |  |Disconn |  +------------------+
              +--------+  +--------+           |
                                               |
                                    +----------+----------+
                                    |                     |
                                    v                     v
                            +-------------+      +----------------+
                            |  config.py  |      | data_config.py |
                            +-------------+      +----------------+
                                    |                     |
                                    v                     v
                          +------------------+   +-------------+
                          | bedrock_config.py|   | DynamoDB    |
                          +------------------+   | (4 tables)  |
                                    |            +-------------+
                                    v
                            +-------------+
                            | AWS Bedrock |
                            +-------------+
```

## Internal Package Dependencies

### Lambda Connect → (No Internal Dependencies)
- **Type**: Standalone
- **Reason**: Simple handler, solo retorna connection ID

### Lambda Disconnect → (No Internal Dependencies)
- **Type**: Standalone
- **Reason**: Simple handler, solo confirma cierre

### Lambda Inference → config.py
- **Type**: Compile/Runtime
- **Reason**: Usa instancia `config` para orquestar chat con Bedrock
- **Import**: `from config import config`

### Lambda Inference → data_config.py
- **Type**: Compile/Runtime
- **Reason**: Usa `get_user_context()` para recuperar contexto completo del usuario
- **Import**: `from data_config import get_user_context`

### config.py → bedrock_config.py
- **Type**: Compile/Runtime
- **Reason**: Usa `stream_chat()` para invocar Bedrock con streaming
- **Import**: `from bedrock_config import stream_chat`

### bedrock_config.py → (No Internal Dependencies)
- **Type**: Standalone
- **Reason**: Módulo de servicio puro, solo interactúa con AWS

### data_config.py → (No Internal Dependencies)
- **Type**: Standalone
- **Reason**: Módulo de servicio puro, solo interactúa con DynamoDB

## External Dependencies

### boto3 (AWS SDK)
- **Version**: ^1.34.149
- **Purpose**: Interactuar con todos los servicios AWS
- **License**: Apache License 2.0
- **Used By**: Todos los módulos de app_inference
- **Services Used**:
  - bedrock-runtime (Bedrock AI)
  - bedrock-agent-runtime (Bedrock Agents)
  - dynamodb (resource y client)
  - apigatewaymanagementapi (WebSocket management)
- **Criticality**: CRITICAL - sin esto no hay integración AWS

### langchain-aws
- **Version**: ^0.2.0
- **Purpose**: Framework LangChain con integraciones AWS
- **License**: MIT
- **Used By**: Lambda Inference (via Layer)
- **Usage**: Facilitar integración con Bedrock y otros servicios AWS
- **Criticality**: HIGH - simplifica desarrollo con LLMs

### loguru
- **Version**: ^0.7.2
- **Purpose**: Logging avanzado y estructurado
- **License**: MIT
- **Used By**: Todos los módulos de app_inference
- **Usage**: 
  - `logger.info()` para información
  - `logger.warning()` para warnings
  - `logger.exception()` para errores
- **Criticality**: MEDIUM - importante para debugging

### requests
- **Version**: ^2.32.3
- **Purpose**: HTTP client library
- **License**: Apache License 2.0
- **Used By**: No usado en código actual
- **Usage**: Posibles integraciones futuras
- **Criticality**: LOW - no crítico actualmente

### python-dotenv
- **Version**: ^1.0.1
- **Purpose**: Cargar variables de entorno desde .env
- **License**: BSD-3-Clause
- **Used By**: Desarrollo local
- **Usage**: Cargar configuración en desarrollo
- **Criticality**: LOW - solo desarrollo

### pandas
- **Version**: 2.1.1
- **Purpose**: Análisis y manipulación de datos
- **License**: BSD-3-Clause
- **Used By**: Notebooks de desarrollo
- **Usage**: Análisis de datos en notebooks
- **Criticality**: LOW - solo desarrollo

### streamlit
- **Version**: ^1.47.0
- **Purpose**: Framework para aplicaciones web
- **License**: Apache License 2.0
- **Used By**: Posible frontend demo
- **Usage**: Interfaz de usuario interactiva
- **Criticality**: LOW - no parte del core

### tqdm
- **Version**: ^4.66.4
- **Purpose**: Progress bars
- **License**: MIT/MPL-2.0
- **Used By**: Scripts de desarrollo
- **Usage**: Visualización de progreso
- **Criticality**: LOW - solo desarrollo

### ipykernel
- **Version**: ^6.29.5
- **Purpose**: Jupyter kernel
- **License**: BSD-3-Clause
- **Used By**: Notebooks
- **Usage**: Soporte para Jupyter notebooks
- **Criticality**: LOW - solo desarrollo

## AWS Service Dependencies

### AWS Lambda
- **Dependency Type**: Runtime Platform
- **Used By**: Todas las Lambda functions
- **Purpose**: Compute serverless
- **Criticality**: CRITICAL

### AWS API Gateway
- **Dependency Type**: Gateway Service
- **Used By**: Todas las Lambda functions (trigger)
- **Purpose**: WebSocket API management
- **Criticality**: CRITICAL

### AWS DynamoDB
- **Dependency Type**: Data Store
- **Used By**: Lambda Inference
- **Tables**: 
  - chat-history (session management)
  - user-profile (user data)
  - transactions (transaction history)
  - retailers (retailer catalog)
- **Purpose**: Persistencia de datos
- **Criticality**: CRITICAL

### AWS Bedrock
- **Dependency Type**: AI/ML Service
- **Used By**: Lambda Inference (via bedrock_config.py)
- **Model**: Claude 3.7 Sonnet
- **Purpose**: Generación de respuestas conversacionales
- **Criticality**: CRITICAL - core functionality

### AWS CloudWatch
- **Dependency Type**: Monitoring Service
- **Used By**: Todas las Lambda functions (implicit)
- **Purpose**: Logging y monitoring
- **Criticality**: HIGH

### AWS IAM
- **Dependency Type**: Security Service
- **Used By**: Todas las Lambda functions
- **Purpose**: Autenticación y autorización
- **Criticality**: CRITICAL

### AWS Lambda Layers
- **Dependency Type**: Shared Dependencies
- **Layer**: pragma-bankia-layer-dev:1
- **Used By**: Lambda Inference
- **Contents**: langchain-aws, loguru
- **Purpose**: Compartir dependencias pesadas
- **Criticality**: HIGH

## Build Dependencies

### Poetry
- **Version**: Latest
- **Purpose**: Gestión de dependencias Python
- **Used By**: Build process
- **Criticality**: HIGH

### AWS SAM CLI
- **Purpose**: Build y deployment de aplicaciones serverless
- **Used By**: Deployment process
- **Criticality**: HIGH

## Dependency Management Strategy

### Production Dependencies
- Definidas en `pyproject.toml` bajo `[tool.poetry.dependencies]`
- Locked en `poetry.lock` para reproducibilidad
- Deployed via Lambda deployment packages o Layers

### Development Dependencies
- Incluidas en `pyproject.toml` (pandas, streamlit, ipykernel, tqdm)
- No deployed a producción
- Solo para desarrollo local y testing

### Lambda Layer Strategy
- Dependencias pesadas (langchain-aws, loguru) en Layer
- Reduce tamaño de deployment packages
- Compartidas entre múltiples functions
- Versionadas (actualmente v1)

## Dependency Risks & Considerations

### Risk: Bedrock Model Availability
- **Issue**: Dependencia en modelo específico de Bedrock
- **Impact**: Si modelo no disponible, aplicación falla
- **Mitigation**: Parametrizar model_id, tener fallback models

### Risk: Lambda Layer Version
- **Issue**: Layer hardcoded a versión 1
- **Impact**: Cambios en layer requieren actualizar template
- **Mitigation**: Parametrizar layer version en SAM template

### Risk: Hardcoded Table Names
- **Issue**: Nombres de tablas hardcoded en config.py
- **Impact**: Dificulta multi-environment deployment
- **Mitigation**: Usar variables de entorno para table names

### Risk: No Dependency Scanning
- **Issue**: No se detecta scanning de vulnerabilidades
- **Impact**: Dependencias vulnerables pueden pasar desapercibidas
- **Mitigation**: Agregar Dependabot, Snyk, o similar

### Risk: Boto3 Version Drift
- **Issue**: Lambda runtime incluye boto3, puede diferir de pyproject.toml
- **Impact**: Comportamiento inconsistente entre local y Lambda
- **Mitigation**: Incluir boto3 en deployment package o layer

## Dependency Update Strategy

### Current State
- Poetry lock file mantiene versiones exactas
- Caret (^) versioning permite minor/patch updates
- No CI/CD automatizado para updates

### Recommendations
1. Agregar Dependabot para PRs automáticos de updates
2. Establecer schedule de review de dependencias (mensual)
3. Testing automatizado antes de updates
4. Documentar breaking changes en dependencies

## Transitive Dependencies

### Via boto3
- botocore
- jmespath
- python-dateutil
- urllib3
- s3transfer

### Via langchain-aws
- langchain-core
- langchain-community
- pydantic
- aiohttp
- (otros según versión)

### Via pandas
- numpy
- python-dateutil
- pytz
- tzdata

### Via streamlit
- altair
- click
- pillow
- protobuf
- tornado
- (muchos otros)

## Dependency Size Impact

### Large Dependencies (Impact on Lambda Cold Start)
- **pandas**: ~50 MB - solo desarrollo
- **streamlit**: ~30 MB - solo desarrollo
- **langchain-aws**: ~10-20 MB - en Layer
- **boto3**: ~30 MB - incluido en Lambda runtime

### Optimization
- Dependencias pesadas en Layer (langchain, loguru)
- Dependencias de desarrollo no deployed
- boto3 usar versión de Lambda runtime cuando posible

## License Compliance

### Permissive Licenses (OK for Commercial Use)
- Apache License 2.0: boto3, requests, streamlit
- MIT: langchain-aws, loguru, tqdm
- BSD-3-Clause: pandas, python-dotenv, ipykernel

### No Copyleft Licenses Detected
- Todas las dependencias son compatibles con uso comercial
- No restricciones de distribución
