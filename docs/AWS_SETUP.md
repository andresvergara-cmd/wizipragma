# Configuración de AWS para Wizipragma

## Cuenta AWS del Proyecto

- **Account ID**: 777937796305
- **Email**: pra_hackaton_agentic_mexico@pragma.com.co
- **Región principal**: us-east-1

## Setup para Desarrolladores

### 1. Instalar AWS CLI

**macOS:**
```bash
brew install awscli
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Windows:**
Descargar desde: https://aws.amazon.com/cli/

### 2. Configurar Credenciales

```bash
aws configure --profile wizipragma
```

Ingresar:
- AWS Access Key ID: [Solicitar al líder del proyecto]
- AWS Secret Access Key: [Solicitar al líder del proyecto]
- Default region: `us-east-1`
- Default output format: `json`

### 3. Verificar Configuración

```bash
aws sts get-caller-identity --profile wizipragma
```

Deberías ver:
```json
{
    "UserId": "...",
    "Account": "777937796305",
    "Arn": "..."
}
```

### 4. Usar el Perfil en el Proyecto

En tu archivo `.env` local:
```bash
AWS_PROFILE=wizipragma
AWS_ACCOUNT_ID=777937796305
AWS_REGION=us-east-1
```

## Servicios AWS a Utilizar

### Backend
- **Lambda**: Para funciones serverless
- **API Gateway**: Para exponer APIs
- **RDS/DynamoDB**: Para base de datos
- **S3**: Para almacenamiento de archivos

### Frontend
- **S3**: Para hosting estático
- **CloudFront**: Para CDN
- **Route 53**: Para DNS (si aplica)

### AI Agent
- **Lambda**: Para ejecutar el agente
- **SQS**: Para colas de mensajes
- **EventBridge**: Para eventos programados

## Despliegue

### Backend (Python/FastAPI)

```bash
# Instalar dependencias de despliegue
pip install aws-sam-cli

# Desplegar
cd backend
sam build
sam deploy --profile wizipragma
```

### Frontend (React)

```bash
# Build
cd frontend
npm run build

# Desplegar a S3
aws s3 sync build/ s3://wizipragma-frontend --profile wizipragma
```

### Agent (TypeScript)

```bash
# Build
cd agent
npm run build

# Desplegar Lambda
aws lambda update-function-code \
  --function-name wizipragma-agent \
  --zip-file fileb://dist/agent.zip \
  --profile wizipragma
```

## Estructura de Recursos AWS

```
wizipragma-dev-*     # Recursos de desarrollo
wizipragma-staging-* # Recursos de staging
wizipragma-prod-*    # Recursos de producción
```

## Permisos y Seguridad

### IAM Roles Necesarios

1. **Developer Role**: Para desarrollo local
   - Permisos: Lambda, S3, DynamoDB, CloudWatch Logs

2. **CI/CD Role**: Para GitHub Actions
   - Permisos: Deploy a Lambda, S3, CloudFormation

3. **Lambda Execution Role**: Para funciones Lambda
   - Permisos: CloudWatch Logs, DynamoDB, S3

### Buenas Prácticas

- ✅ Nunca commitear credenciales en el código
- ✅ Usar variables de entorno
- ✅ Usar IAM roles en lugar de access keys cuando sea posible
- ✅ Rotar credenciales regularmente
- ✅ Usar MFA para acceso a consola AWS

## Costos

Monitorear costos en: https://console.aws.amazon.com/billing/

**Presupuesto estimado:**
- Lambda: ~$5-10/mes (capa gratuita)
- S3: ~$1-5/mes
- RDS/DynamoDB: ~$10-50/mes
- Total estimado: ~$20-70/mes

## Soporte

Para problemas con AWS:
1. Revisar CloudWatch Logs
2. Consultar documentación: https://docs.aws.amazon.com/
3. Contactar al líder del proyecto

## Variables de Entorno por Componente

### Backend
```bash
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=777937796305
DATABASE_URL=postgresql://...
S3_BUCKET=wizipragma-backend-storage
```

### Frontend
```bash
REACT_APP_API_URL=https://api.wizipragma.com
REACT_APP_AWS_REGION=us-east-1
```

### Agent
```bash
AWS_REGION=us-east-1
BACKEND_API_URL=https://api.wizipragma.com/api/v1
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/777937796305/wizipragma-queue
```
