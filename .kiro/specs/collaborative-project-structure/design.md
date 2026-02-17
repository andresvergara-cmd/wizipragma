# Documento de Diseño: Estructura de Proyecto Colaborativo

## Resumen

Este diseño establece una arquitectura modular para el repositorio wizipragma que permite a tres desarrolladores trabajar de forma independiente en componentes de Agente IA, Frontend y Backend, mientras mantiene puntos de integración claros y contratos de API bien definidos.

## Arquitectura

### Arquitectura General del Sistema

```mermaid
graph TB
    subgraph "Frontend (Developer 2)"
        FE[React/Vue Application]
        FE_Types[TypeScript Types]
    end
    
    subgraph "Backend (Developer 3)"
        API[REST API]
        BL[Business Logic]
        DB[(Database)]
    end
    
    subgraph "AI Agent (Developer 1)"
        AC[AgentCore]
        AL[Agent Logic]
    end
    
    subgraph "Shared"
        Contracts[API Contracts]
        Types[Shared Types]
        Schemas[Data Schemas]
    end
    
    FE -->|HTTP/REST| API
    FE -->|WebSocket| API
    AC -->|HTTP/REST| API
    API --> BL
    BL --> DB
    
    FE_Types -.->|imports| Types
    AC -.->|imports| Types
    API -.->|implements| Contracts
    FE -.->|consumes| Contracts
    AC -.->|consumes| Contracts
```

### Principios de Diseño

1. **Separación de Responsabilidades**: Cada componente tiene un propósito claro y límites bien definidos
2. **Contratos Primero**: Las interfaces se definen antes de la implementación
3. **Desarrollo Independiente**: Los desarrolladores pueden trabajar sin bloqueos
4. **Integración Continua**: Los componentes se integran frecuentemente a través de contratos estables

## Componentes e Interfaces

### Estructura de Directorios

```
wizipragma/
├── .github/
│   └── workflows/
│       ├── ci-agent.yml
│       ├── ci-backend.yml
│       ├── ci-frontend.yml
│       └── integration-tests.yml
├── shared/
│   ├── types/
│   │   ├── user.ts
│   │   ├── agent.ts
│   │   ├── request.ts
│   │   └── response.ts
│   ├── contracts/
│   │   └── api-spec.yaml (OpenAPI)
│   └── schemas/
│       └── validation-schemas.json
├── agent/
│   ├── src/
│   │   ├── core/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── .env.example
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   └── middleware/
│   │   ├── services/
│   │   ├── models/
│   │   └── utils/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt (Python) o package.json (Node)
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── utils/
│   ├── tests/
│   ├── .env.example
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── integration-tests/
│   ├── frontend-backend/
│   ├── agent-backend/
│   └── e2e/
├── docker/
│   ├── agent.Dockerfile
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── architecture/
│   │   └── ADR/
│   ├── api/
│   └── setup/
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

### Interfaces de Componentes

#### 1. Tipos Compartidos (shared/types/)

**user.ts**
```typescript
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'developer' | 'user';
  createdAt: Date;
  updatedAt: Date;
}

export interface UserCreateRequest {
  email: string;
  name: string;
  password: string;
  role?: 'developer' | 'user';
}

export interface UserUpdateRequest {
  name?: string;
  email?: string;
}
```

**agent.ts**
```typescript
export interface AgentRequest {
  id: string;
  userId: string;
  action: string;
  parameters: Record<string, any>;
  timestamp: Date;
}

export interface AgentResponse {
  requestId: string;
  status: 'success' | 'error' | 'pending';
  result?: any;
  error?: ErrorDetail;
  timestamp: Date;
}

export interface AgentConfig {
  apiKey: string;
  baseUrl: string;
  timeout: number;
  retryAttempts: number;
}
```

**response.ts**
```typescript
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ErrorDetail;
  metadata?: ResponseMetadata;
}

export interface ErrorDetail {
  code: string;
  message: string;
  details?: Record<string, any>;
  correlationId: string;
}

export interface ResponseMetadata {
  timestamp: Date;
  version: string;
  correlationId: string;
}
```

#### 2. Contrato de API (shared/contracts/api-spec.yaml)

```yaml
openapi: 3.0.0
info:
  title: Wizipragma API
  version: 1.0.0
  description: API para comunicación entre componentes

servers:
  - url: http://localhost:3000/api/v1
    description: Desarrollo local
  - url: https://api.wizipragma.com/api/v1
    description: Producción

paths:
  /users:
    get:
      summary: Obtener lista de usuarios
      tags: [Users]
      responses:
        '200':
          description: Lista de usuarios
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
    
    post:
      summary: Crear nuevo usuario
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreateRequest'
      responses:
        '201':
          description: Usuario creado
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiResponse'

  /agent/execute:
    post:
      summary: Ejecutar acción del agente
      tags: [Agent]
      security:
        - ApiKeyAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AgentRequest'
      responses:
        '200':
          description: Acción ejecutada
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentResponse'
        '401':
          description: No autorizado
        '500':
          description: Error del servidor

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        name:
          type: string
        role:
          type: string
          enum: [admin, developer, user]
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
    
    UserCreateRequest:
      type: object
      required:
        - email
        - name
        - password
      properties:
        email:
          type: string
          format: email
        name:
          type: string
        password:
          type: string
          minLength: 8
        role:
          type: string
          enum: [developer, user]
    
    AgentRequest:
      type: object
      required:
        - action
        - parameters
      properties:
        id:
          type: string
        userId:
          type: string
        action:
          type: string
        parameters:
          type: object
        timestamp:
          type: string
          format: date-time
    
    AgentResponse:
      type: object
      properties:
        requestId:
          type: string
        status:
          type: string
          enum: [success, error, pending]
        result:
          type: object
        error:
          $ref: '#/components/schemas/ErrorDetail'
        timestamp:
          type: string
          format: date-time
    
    ErrorDetail:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object
        correlationId:
          type: string
    
    ApiResponse:
      type: object
      properties:
        success:
          type: boolean
        data:
          type: object
        error:
          $ref: '#/components/schemas/ErrorDetail'
        metadata:
          type: object

  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

### Comunicación entre Componentes

#### Frontend → Backend

**Protocolo**: HTTP/HTTPS REST + WebSocket para tiempo real

**Cliente HTTP (frontend/src/services/api-client.ts)**
```typescript
import axios, { AxiosInstance } from 'axios';
import { ApiResponse } from '../../../shared/types/response';

class ApiClient {
  private client: AxiosInstance;
  
  constructor() {
    this.client = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3000/api/v1',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    this.setupInterceptors();
  }
  
  private setupInterceptors() {
    // Request interceptor para agregar auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
    
    // Response interceptor para manejo de errores
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        // Manejo centralizado de errores
        console.error('API Error:', error.response?.data);
        return Promise.reject(error);
      }
    );
  }
  
  async get<T>(url: string): Promise<ApiResponse<T>> {
    const response = await this.client.get(url);
    return response.data;
  }
  
  async post<T>(url: string, data: any): Promise<ApiResponse<T>> {
    const response = await this.client.post(url, data);
    return response.data;
  }
  
  async put<T>(url: string, data: any): Promise<ApiResponse<T>> {
    const response = await this.client.put(url, data);
    return response.data;
  }
  
  async delete<T>(url: string): Promise<ApiResponse<T>> {
    const response = await this.client.delete(url);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

#### AI Agent → Backend

**Protocolo**: HTTP/HTTPS REST con autenticación por API Key

**Cliente del Agente (agent/src/services/backend-client.ts)**
```typescript
import axios, { AxiosInstance } from 'axios';
import { AgentRequest, AgentResponse } from '../../../shared/types/agent';
import { ApiResponse } from '../../../shared/types/response';

class BackendClient {
  private client: AxiosInstance;
  private apiKey: string;
  private maxRetries: number = 3;
  
  constructor(config: { apiKey: string; baseUrl: string; timeout?: number }) {
    this.apiKey = config.apiKey;
    this.client = axios.create({
      baseURL: config.baseUrl,
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
      },
    });
  }
  
  async executeAction(request: AgentRequest): Promise<AgentResponse> {
    let lastError: Error | null = null;
    
    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        const response = await this.client.post<ApiResponse<AgentResponse>>(
          '/agent/execute',
          request
        );
        
        if (response.data.success && response.data.data) {
          return response.data.data;
        }
        
        throw new Error(response.data.error?.message || 'Unknown error');
      } catch (error) {
        lastError = error as Error;
        
        // Esperar antes de reintentar (exponential backoff)
        if (attempt < this.maxRetries - 1) {
          await this.delay(Math.pow(2, attempt) * 1000);
        }
      }
    }
    
    throw lastError;
  }
  
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export default BackendClient;
```

### Configuración de Entorno

#### Variables de Entorno por Componente

**agent/.env.example**
```env
# Backend API Configuration
BACKEND_API_URL=http://localhost:3000/api/v1
BACKEND_API_KEY=your-api-key-here
BACKEND_TIMEOUT=30000

# Agent Configuration
AGENT_LOG_LEVEL=info
AGENT_MAX_RETRIES=3

# Development
NODE_ENV=development
```

**backend/.env.example**
```env
# Server Configuration
PORT=3000
NODE_ENV=development

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/wizipragma
DATABASE_POOL_SIZE=10

# Authentication
JWT_SECRET=your-jwt-secret-here
JWT_EXPIRATION=24h
API_KEY_SALT=your-api-key-salt

# CORS
CORS_ORIGIN=http://localhost:3001

# Logging
LOG_LEVEL=info
```

**frontend/.env.example**
```env
# API Configuration
REACT_APP_API_URL=http://localhost:3000/api/v1
REACT_APP_WS_URL=ws://localhost:3000

# Environment
NODE_ENV=development
PORT=3001

# Feature Flags
REACT_APP_ENABLE_AGENT_FEATURES=true
```

### Workflow de Git

#### Estrategia de Branching

```mermaid
gitGraph
    commit id: "Initial"
    branch develop
    checkout develop
    
    branch agent/feature-1
    commit id: "Agent: Add core logic"
    commit id: "Agent: Add tests"
    checkout develop
    merge agent/feature-1
    
    branch backend/api-endpoints
    commit id: "Backend: Add user API"
    commit id: "Backend: Add agent API"
    checkout develop
    merge backend/api-endpoints
    
    branch frontend/user-interface
    commit id: "Frontend: Add components"
    commit id: "Frontend: Connect API"
    checkout develop
    merge frontend/user-interface
    
    checkout main
    merge develop tag: "v1.0.0"
```

#### Convenciones de Nombres de Ramas

- **Feature branches**: `{component}/{feature-name}`
  - Ejemplos: `agent/authentication`, `backend/user-api`, `frontend/dashboard`
- **Bugfix branches**: `{component}/fix/{bug-description}`
  - Ejemplos: `agent/fix/retry-logic`, `backend/fix/validation-error`
- **Hotfix branches**: `hotfix/{issue-description}`
  - Para correcciones urgentes en producción

#### Proceso de Pull Request

1. Crear feature branch desde `develop`
2. Implementar cambios con commits descriptivos
3. Ejecutar tests locales
4. Push a GitHub y crear Pull Request
5. Revisión de código por al menos un desarrollador
6. CI/CD ejecuta tests automáticos
7. Merge a `develop` después de aprobación
8. Eliminar feature branch

## Modelos de Datos

### Modelo de Usuario

```typescript
interface User {
  id: string;              // UUID
  email: string;           // Único, validado
  name: string;            // Nombre completo
  role: UserRole;          // Rol del usuario
  passwordHash: string;    // Hash bcrypt (solo backend)
  createdAt: Date;
  updatedAt: Date;
  lastLoginAt?: Date;
}

enum UserRole {
  ADMIN = 'admin',
  DEVELOPER = 'developer',
  USER = 'user'
}
```

### Modelo de Solicitud del Agente

```typescript
interface AgentRequest {
  id: string;              // UUID generado por el agente
  userId: string;          // Usuario que inicia la solicitud
  action: string;          // Acción a ejecutar
  parameters: Record<string, any>;  // Parámetros de la acción
  timestamp: Date;         // Momento de la solicitud
  correlationId?: string;  // Para rastreo distribuido
}
```

### Modelo de Respuesta de API

```typescript
interface ApiResponse<T> {
  success: boolean;        // Indica si la operación fue exitosa
  data?: T;               // Datos de respuesta (si success = true)
  error?: ErrorDetail;    // Detalles del error (si success = false)
  metadata?: {
    timestamp: Date;
    version: string;
    correlationId: string;
  };
}
```



## Propiedades de Corrección

*Una propiedad es una característica o comportamiento que debe mantenerse verdadero en todas las ejecuciones válidas de un sistema - esencialmente, una declaración formal sobre lo que el sistema debe hacer. Las propiedades sirven como puente entre las especificaciones legibles por humanos y las garantías de corrección verificables por máquinas.*

### Propiedad 1: Aislamiento de Componentes

*Para cualquier* archivo de código en un componente (agent, frontend, backend), las declaraciones de importación no deben referenciar directamente archivos internos de otros componentes, solo pueden importar desde el directorio shared.

**Valida: Requisitos 1.2**

### Propiedad 2: Comunicación HTTP entre Componentes

*Para cualquier* solicitud de comunicación entre componentes (Frontend→Backend o Agent→Backend), el protocolo de transporte debe ser HTTP/HTTPS con payloads en formato JSON.

**Valida: Requisitos 3.1, 4.2**

### Propiedad 3: Autenticación de Solicitudes del Agente

*Para cualquier* solicitud del AI Agent al Backend sin credenciales válidas (API key o JWT), el Backend debe rechazar la solicitud con código HTTP 401. Para cualquier solicitud con credenciales válidas, debe ser procesada.

**Valida: Requisitos 3.3**

### Propiedad 4: Lógica de Reintentos del Agente

*Para cualquier* fallo de comunicación del AI Agent con el Backend (timeout, error 5xx), el Agent debe reintentar la solicitud al menos 3 veces con backoff exponencial antes de fallar definitivamente.

**Valida: Requisitos 3.4**

### Propiedad 5: Enrutamiento de Operaciones del Agente

*Para cualquier* operación del AI Agent iniciada desde el Frontend, la solicitud debe ser enrutada a través del Backend API, nunca directamente del Frontend al Agent.

**Valida: Requisitos 4.4**

### Propiedad 6: Definiciones de Tipos para Respuestas de API

*Para cualquier* endpoint de API consumido por el Frontend, debe existir una definición de tipo TypeScript correspondiente en el directorio shared/types.

**Valida: Requisitos 4.5**

### Propiedad 7: No Duplicación de Tipos Compartidos

*Para cualquier* modelo de datos (User, Agent, Request, Response, Error) usado por múltiples componentes, debe existir exactamente una definición en shared/types, no duplicados en componentes individuales.

**Valida: Requisitos 5.2**

### Propiedad 8: Configuración mediante Variables de Entorno

*Para cualquier* valor de configuración específico del entorno (URLs, puertos, credenciales, feature flags), debe ser leído desde variables de entorno, no hardcodeado en el código fuente.

**Valida: Requisitos 6.2, 12.1**

### Propiedad 9: Convención de Nombres de Branches

*Para cualquier* feature branch creado en el repositorio, el nombre debe seguir el patrón `{component}/{feature-name}` donde component es uno de: agent, backend, frontend.

**Valida: Requisitos 7.3**

### Propiedad 10: Cobertura de Tests Unitarios

*Para cualquier* componente (agent, frontend, backend), la cobertura de código de los tests unitarios debe ser mayor o igual al 80%.

**Valida: Requisitos 8.1**

### Propiedad 11: Independencia de Tests de Componentes

*Para cualquier* suite de tests de un componente, debe poder ejecutarse exitosamente sin requerir que otros componentes estén en ejecución o disponibles.

**Valida: Requisitos 8.4**

### Propiedad 12: Versionado de Endpoints de API

*Para cualquier* endpoint expuesto por el Backend, la ruta debe incluir un prefijo de versión en el formato `/api/v{N}/` donde N es un número entero positivo.

**Valida: Requisitos 10.1**

### Propiedad 13: Compatibilidad hacia Atrás de API

*Para cualquier* versión mayor de API (v1, v2, etc.), el Backend debe mantener soporte funcional para la versión mayor anterior durante al menos un ciclo de release.

**Valida: Requisitos 10.3**

### Propiedad 14: Formato Consistente de Errores

*Para cualquier* respuesta de error de cualquier endpoint de API, debe seguir el formato estándar: `{ success: false, error: { code, message, details, correlationId }, metadata }` con código de estado HTTP apropiado según convenciones REST, timestamp, nombre del componente, y correlationId para trazabilidad.

**Valida: Requisitos 11.1, 11.2, 11.3, 11.4**

### Propiedad 15: No Secretos en el Repositorio

*Para cualquier* commit en el repositorio, no debe contener credenciales sensibles (API keys, passwords, tokens, certificados privados) en texto plano.

**Valida: Requisitos 12.4**

### Propiedad 16: Documentación de Funciones Públicas

*Para cualquier* función o clase pública exportada en cualquier componente, debe tener comentarios de documentación (JSDoc para TypeScript/JavaScript, docstrings para Python) que describan su propósito, parámetros y valor de retorno.

**Valida: Requisitos 14.2**

### Propiedad 17: Sincronización de Documentación de API

*Para cualquier* endpoint implementado en el Backend, debe existir una entrada correspondiente en el archivo OpenAPI specification (shared/contracts/api-spec.yaml) con schemas de request y response.

**Valida: Requisitos 14.3**

### Propiedad 18: Puertos Únicos para Componentes

*Para cualquier* configuración de desarrollo local donde múltiples componentes se ejecutan simultáneamente, cada componente debe usar un puerto único sin conflictos (ej: Frontend=3001, Backend=3000, Agent=3002).

**Valida: Requisitos 15.4**

## Manejo de Errores

### Estrategia General

El sistema implementa un enfoque de manejo de errores en capas:

1. **Capa de Validación**: Validación de entrada en el punto de entrada
2. **Capa de Lógica de Negocio**: Errores de dominio y reglas de negocio
3. **Capa de Integración**: Errores de comunicación entre componentes
4. **Capa de Infraestructura**: Errores de base de datos, red, sistema de archivos

### Tipos de Errores

```typescript
// shared/types/errors.ts

export enum ErrorCode {
  // Errores de validación (400)
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  INVALID_INPUT = 'INVALID_INPUT',
  MISSING_REQUIRED_FIELD = 'MISSING_REQUIRED_FIELD',
  
  // Errores de autenticación (401)
  UNAUTHORIZED = 'UNAUTHORIZED',
  INVALID_TOKEN = 'INVALID_TOKEN',
  EXPIRED_TOKEN = 'EXPIRED_TOKEN',
  
  // Errores de autorización (403)
  FORBIDDEN = 'FORBIDDEN',
  INSUFFICIENT_PERMISSIONS = 'INSUFFICIENT_PERMISSIONS',
  
  // Errores de recursos (404)
  NOT_FOUND = 'NOT_FOUND',
  RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND',
  
  // Errores de conflicto (409)
  CONFLICT = 'CONFLICT',
  DUPLICATE_RESOURCE = 'DUPLICATE_RESOURCE',
  
  // Errores del servidor (500)
  INTERNAL_ERROR = 'INTERNAL_ERROR',
  DATABASE_ERROR = 'DATABASE_ERROR',
  EXTERNAL_SERVICE_ERROR = 'EXTERNAL_SERVICE_ERROR',
  
  // Errores de servicio no disponible (503)
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  BACKEND_UNAVAILABLE = 'BACKEND_UNAVAILABLE',
}

export class AppError extends Error {
  constructor(
    public code: ErrorCode,
    public message: string,
    public statusCode: number,
    public details?: Record<string, any>,
    public correlationId?: string
  ) {
    super(message);
    this.name = 'AppError';
  }
  
  toJSON(): ErrorDetail {
    return {
      code: this.code,
      message: this.message,
      details: this.details,
      correlationId: this.correlationId || generateCorrelationId(),
    };
  }
}
```

### Manejo de Errores por Componente

#### Backend

```typescript
// backend/src/middleware/error-handler.ts

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  const correlationId = req.headers['x-correlation-id'] as string || generateCorrelationId();
  
  // Log del error
  logger.error({
    message: error.message,
    stack: error.stack,
    correlationId,
    component: 'backend',
    path: req.path,
    method: req.method,
  });
  
  // Convertir a AppError si no lo es
  let appError: AppError;
  if (error instanceof AppError) {
    appError = error;
  } else {
    appError = new AppError(
      ErrorCode.INTERNAL_ERROR,
      'An unexpected error occurred',
      500,
      { originalError: error.message },
      correlationId
    );
  }
  
  // Enviar respuesta
  res.status(appError.statusCode).json({
    success: false,
    error: appError.toJSON(),
    metadata: {
      timestamp: new Date(),
      version: 'v1',
      correlationId,
    },
  });
}
```

#### Frontend

```typescript
// frontend/src/utils/error-handler.ts

export class ApiErrorHandler {
  static handle(error: any): void {
    if (error.response) {
      // Error de respuesta del servidor
      const apiError = error.response.data.error;
      
      switch (error.response.status) {
        case 401:
          // Redirigir a login
          window.location.href = '/login';
          break;
        case 403:
          // Mostrar mensaje de permisos insuficientes
          toast.error('No tienes permisos para realizar esta acción');
          break;
        case 404:
          toast.error('Recurso no encontrado');
          break;
        case 500:
          toast.error('Error del servidor. Por favor, intenta más tarde.');
          break;
        default:
          toast.error(apiError?.message || 'Error desconocido');
      }
      
      // Log para debugging
      console.error('API Error:', {
        correlationId: apiError?.correlationId,
        code: apiError?.code,
        message: apiError?.message,
      });
    } else if (error.request) {
      // Error de red
      toast.error('Error de conexión. Verifica tu conexión a internet.');
    } else {
      // Error de configuración
      toast.error('Error inesperado');
      console.error('Error:', error.message);
    }
  }
}
```

#### AI Agent

```typescript
// agent/src/utils/error-handler.ts

export class AgentErrorHandler {
  static async handleBackendError(error: any, request: AgentRequest): Promise<AgentResponse> {
    const correlationId = generateCorrelationId();
    
    logger.error({
      message: 'Backend communication error',
      error: error.message,
      request,
      correlationId,
      component: 'agent',
    });
    
    // Determinar si es retryable
    const isRetryable = this.isRetryableError(error);
    
    return {
      requestId: request.id,
      status: 'error',
      error: {
        code: isRetryable ? ErrorCode.SERVICE_UNAVAILABLE : ErrorCode.EXTERNAL_SERVICE_ERROR,
        message: 'Failed to communicate with backend',
        details: {
          originalError: error.message,
          retryable: isRetryable,
        },
        correlationId,
      },
      timestamp: new Date(),
    };
  }
  
  private static isRetryableError(error: any): boolean {
    // Errores de red o timeouts son retryables
    if (error.code === 'ECONNREFUSED' || error.code === 'ETIMEDOUT') {
      return true;
    }
    
    // Errores 5xx son retryables
    if (error.response && error.response.status >= 500) {
      return true;
    }
    
    return false;
  }
}
```

### Logging

Cada componente implementa logging estructurado:

```typescript
// shared/utils/logger.ts

import winston from 'winston';

export const createLogger = (component: string) => {
  return winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: winston.format.combine(
      winston.format.timestamp(),
      winston.format.errors({ stack: true }),
      winston.format.json()
    ),
    defaultMeta: { component },
    transports: [
      new winston.transports.Console({
        format: winston.format.combine(
          winston.format.colorize(),
          winston.format.simple()
        ),
      }),
      new winston.transports.File({ 
        filename: `logs/${component}-error.log`, 
        level: 'error' 
      }),
      new winston.transports.File({ 
        filename: `logs/${component}-combined.log` 
      }),
    ],
  });
};
```

## Estrategia de Testing

### Enfoque Dual de Testing

El proyecto utiliza un enfoque dual que combina:

1. **Tests Unitarios**: Verifican ejemplos específicos, casos edge y condiciones de error
2. **Tests Basados en Propiedades**: Verifican propiedades universales a través de múltiples entradas generadas

Ambos tipos de tests son complementarios y necesarios para cobertura comprehensiva.

### Configuración por Componente

#### Frontend (Jest + React Testing Library)

```json
// frontend/package.json
{
  "scripts": {
    "test": "jest --coverage",
    "test:watch": "jest --watch",
    "test:ci": "jest --coverage --ci --maxWorkers=2"
  },
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

**Ejemplo de Test Unitario:**
```typescript
// frontend/src/services/__tests__/api-client.test.ts

describe('ApiClient', () => {
  it('should add auth token to requests', async () => {
    localStorage.setItem('authToken', 'test-token');
    
    const mockResponse = { success: true, data: { id: '1' } };
    mock.onGet('/users/1').reply(200, mockResponse);
    
    const response = await apiClient.get('/users/1');
    
    expect(response).toEqual(mockResponse);
    expect(mock.history.get[0].headers.Authorization).toBe('Bearer test-token');
  });
  
  it('should handle 401 errors', async () => {
    mock.onGet('/users/1').reply(401);
    
    await expect(apiClient.get('/users/1')).rejects.toThrow();
  });
});
```

#### Backend (Jest para Node.js o pytest para Python)

**Para Node.js:**
```json
// backend/package.json
{
  "scripts": {
    "test": "jest --coverage --runInBand",
    "test:watch": "jest --watch",
    "test:integration": "jest --testPathPattern=integration"
  }
}
```

**Para Python:**
```ini
# backend/pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=src --cov-report=html --cov-report=term --cov-fail-under=80
```

**Ejemplo de Test Unitario (Python):**
```python
# backend/tests/test_user_service.py

def test_create_user_success():
    user_data = {
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'SecurePass123'
    }
    
    user = user_service.create_user(user_data)
    
    assert user.email == user_data['email']
    assert user.name == user_data['name']
    assert user.password_hash != user_data['password']  # Debe estar hasheado

def test_create_user_duplicate_email():
    user_data = {'email': 'existing@example.com', 'name': 'Test', 'password': 'pass'}
    
    user_service.create_user(user_data)
    
    with pytest.raises(AppError) as exc_info:
        user_service.create_user(user_data)
    
    assert exc_info.value.code == ErrorCode.DUPLICATE_RESOURCE
```

#### AI Agent

```json
// agent/package.json
{
  "scripts": {
    "test": "jest --coverage",
    "test:watch": "jest --watch"
  }
}
```

**Ejemplo de Test Unitario:**
```typescript
// agent/tests/backend-client.test.ts

describe('BackendClient', () => {
  it('should retry on network errors', async () => {
    const client = new BackendClient({
      apiKey: 'test-key',
      baseUrl: 'http://localhost:3000/api/v1',
    });
    
    // Simular 2 fallos y luego éxito
    mock
      .onPost('/agent/execute').replyOnce(500)
      .onPost('/agent/execute').replyOnce(500)
      .onPost('/agent/execute').replyOnce(200, {
        success: true,
        data: { requestId: '123', status: 'success' }
      });
    
    const request: AgentRequest = {
      id: '123',
      userId: 'user-1',
      action: 'test',
      parameters: {},
      timestamp: new Date(),
    };
    
    const response = await client.executeAction(request);
    
    expect(response.status).toBe('success');
    expect(mock.history.post.length).toBe(3); // 2 fallos + 1 éxito
  });
});
```

### Tests de Integración

Los tests de integración verifican la comunicación entre componentes:

```typescript
// integration-tests/frontend-backend/user-flow.test.ts

describe('User Management Integration', () => {
  beforeAll(async () => {
    // Iniciar backend de prueba
    await startTestBackend();
  });
  
  afterAll(async () => {
    await stopTestBackend();
  });
  
  it('should create and retrieve user through API', async () => {
    // Crear usuario desde frontend
    const createResponse = await apiClient.post('/users', {
      email: 'integration@test.com',
      name: 'Integration Test',
      password: 'TestPass123',
    });
    
    expect(createResponse.success).toBe(true);
    const userId = createResponse.data.id;
    
    // Recuperar usuario
    const getResponse = await apiClient.get(`/users/${userId}`);
    
    expect(getResponse.success).toBe(true);
    expect(getResponse.data.email).toBe('integration@test.com');
  });
});
```

```typescript
// integration-tests/agent-backend/agent-communication.test.ts

describe('Agent-Backend Integration', () => {
  it('should authenticate and execute agent action', async () => {
    const client = new BackendClient({
      apiKey: process.env.TEST_API_KEY,
      baseUrl: 'http://localhost:3000/api/v1',
    });
    
    const request: AgentRequest = {
      id: generateId(),
      userId: 'test-user',
      action: 'process_data',
      parameters: { data: 'test' },
      timestamp: new Date(),
    };
    
    const response = await client.executeAction(request);
    
    expect(response.status).toBe('success');
    expect(response.requestId).toBe(request.id);
  });
});
```

### Tests End-to-End

```typescript
// integration-tests/e2e/user-workflow.test.ts

describe('Complete User Workflow', () => {
  it('should complete full user journey', async () => {
    // 1. Usuario se registra (Frontend → Backend)
    const signupResponse = await page.goto('/signup');
    await page.fill('[name="email"]', 'e2e@test.com');
    await page.fill('[name="password"]', 'E2eTest123');
    await page.click('button[type="submit"]');
    
    // 2. Usuario inicia sesión
    await page.goto('/login');
    await page.fill('[name="email"]', 'e2e@test.com');
    await page.fill('[name="password"]', 'E2eTest123');
    await page.click('button[type="submit"]');
    
    // 3. Usuario ejecuta acción del agente (Frontend → Backend → Agent)
    await page.goto('/agent');
    await page.click('[data-testid="execute-agent"]');
    
    // 4. Verificar resultado
    await page.waitForSelector('[data-testid="agent-result"]');
    const result = await page.textContent('[data-testid="agent-result"]');
    expect(result).toContain('success');
  });
});
```

### Configuración de Tests Basados en Propiedades

Para implementar tests basados en propiedades, se utilizará:
- **Frontend/Agent (TypeScript)**: fast-check
- **Backend (Python)**: Hypothesis
- **Backend (Node.js)**: fast-check

**Configuración mínima**: 100 iteraciones por test de propiedad

**Formato de etiquetas**: Cada test de propiedad debe incluir un comentario:
```
Feature: collaborative-project-structure, Property {número}: {texto de la propiedad}
```

**Ejemplo de Test de Propiedad:**
```typescript
// Feature: collaborative-project-structure, Property 14: Formato Consistente de Errores

import fc from 'fast-check';

describe('Property: Error Response Format', () => {
  it('should return consistent error format for all error types', async () => {
    await fc.assert(
      fc.asyncProperty(
        fc.oneof(
          fc.constant(400),
          fc.constant(401),
          fc.constant(403),
          fc.constant(404),
          fc.constant(500)
        ),
        fc.string(),
        async (statusCode, errorMessage) => {
          // Simular error
          const error = new AppError(
            ErrorCode.INTERNAL_ERROR,
            errorMessage,
            statusCode
          );
          
          const response = error.toJSON();
          
          // Verificar formato
          expect(response).toHaveProperty('code');
          expect(response).toHaveProperty('message');
          expect(response).toHaveProperty('correlationId');
          expect(typeof response.correlationId).toBe('string');
          expect(response.correlationId.length).toBeGreaterThan(0);
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

### Ejecución de Tests en CI/CD

```yaml
# .github/workflows/ci-backend.yml

name: Backend CI

on:
  pull_request:
    paths:
      - 'backend/**'
      - 'shared/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        working-directory: ./backend
        run: npm ci
      
      - name: Run unit tests
        working-directory: ./backend
        run: npm test
      
      - name: Run integration tests
        working-directory: ./backend
        run: npm run test:integration
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage/lcov.info
          flags: backend
```

### Balance entre Tests Unitarios y de Propiedades

- **Tests Unitarios**: Enfocarse en ejemplos específicos y casos edge
- **Tests de Propiedades**: Verificar propiedades universales con cobertura amplia de inputs
- Evitar demasiados tests unitarios cuando una propiedad puede cubrir el comportamiento
- Los tests de propiedades manejan la cobertura de múltiples inputs automáticamente
