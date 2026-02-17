# Guía de Despliegue a AWS

## Prerequisitos

1. AWS CLI configurado con perfil `wizipragma`
2. Credenciales con permisos de deploy
3. Código testeado y aprobado en develop

## Ambientes

- **Development**: Para pruebas locales
- **Staging**: Para pruebas pre-producción en AWS
- **Production**: Ambiente productivo

## Despliegue por Componente

### Backend (Python/FastAPI)

#### Opción 1: Lambda + API Gateway (Serverless)

```bash
cd backend

# Instalar SAM CLI
pip install aws-sam-cli

# Crear template.yaml (si no existe)
sam init

# Build
sam build

# Deploy a staging
sam deploy \
  --stack-name wizipragma-backend-staging \
  --profile wizipragma \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM

# Deploy a production
sam deploy \
  --stack-name wizipragma-backend-prod \
  --profile wizipragma \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM
```

#### Opción 2: ECS/Fargate (Containerizado)

```bash
cd backend

# Build Docker image
docker build -t wizipragma-backend .

# Tag para ECR
docker tag wizipragma-backend:latest \
  777937796305.dkr.ecr.us-east-1.amazonaws.com/wizipragma-backend:latest

# Login a ECR
aws ecr get-login-password --region us-east-1 --profile wizipragma | \
  docker login --username AWS --password-stdin \
  777937796305.dkr.ecr.us-east-1.amazonaws.com

# Push
docker push 777937796305.dkr.ecr.us-east-1.amazonaws.com/wizipragma-backend:latest

# Deploy a ECS (usando AWS Console o CLI)
```

### Frontend (React)

```bash
cd frontend

# Build para producción
npm run build

# Deploy a S3
aws s3 sync build/ s3://wizipragma-frontend-prod \
  --profile wizipragma \
  --delete

# Invalidar cache de CloudFront (si aplica)
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*" \
  --profile wizipragma
```

### Agent (TypeScript)

```bash
cd agent

# Build
npm run build

# Crear ZIP para Lambda
cd dist
zip -r ../agent.zip .
cd ..

# Deploy a Lambda
aws lambda update-function-code \
  --function-name wizipragma-agent-prod \
  --zip-file fileb://agent.zip \
  --profile wizipragma \
  --region us-east-1

# Actualizar variables de entorno
aws lambda update-function-configuration \
  --function-name wizipragma-agent-prod \
  --environment Variables="{
    BACKEND_API_URL=https://api.wizipragma.com/api/v1,
    NODE_ENV=production
  }" \
  --profile wizipragma
```

## CI/CD con GitHub Actions

### Setup de Secrets en GitHub

1. Ve a: Settings → Secrets and variables → Actions
2. Agrega:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` = us-east-1
   - `AWS_ACCOUNT_ID` = 777937796305

### Workflow Automático

El proyecto ya tiene workflows en `.github/workflows/` que se ejecutan automáticamente:

- **Push a develop**: Deploy a staging
- **Push a main**: Deploy a production
- **Pull Request**: Run tests

## Verificación Post-Deploy

### Backend
```bash
# Health check
curl https://api.wizipragma.com/health

# Test endpoint
curl https://api.wizipragma.com/api/v1/users
```

### Frontend
```bash
# Verificar que carga
curl https://wizipragma.com

# Verificar assets
curl https://wizipragma.com/static/js/main.js
```

### Agent
```bash
# Invocar Lambda directamente
aws lambda invoke \
  --function-name wizipragma-agent-prod \
  --payload '{"action":"test"}' \
  --profile wizipragma \
  response.json

cat response.json
```

## Rollback

### Backend (Lambda)
```bash
# Listar versiones
aws lambda list-versions-by-function \
  --function-name wizipragma-backend-prod \
  --profile wizipragma

# Rollback a versión anterior
aws lambda update-alias \
  --function-name wizipragma-backend-prod \
  --name prod \
  --function-version PREVIOUS_VERSION \
  --profile wizipragma
```

### Frontend (S3)
```bash
# Restaurar versión anterior (si versionado está habilitado)
aws s3api list-object-versions \
  --bucket wizipragma-frontend-prod \
  --profile wizipragma

# Copiar versión anterior
aws s3 cp s3://wizipragma-frontend-prod/index.html \
  s3://wizipragma-frontend-prod/index.html \
  --version-id VERSION_ID \
  --profile wizipragma
```

## Monitoreo

### CloudWatch Logs
```bash
# Ver logs del backend
aws logs tail /aws/lambda/wizipragma-backend-prod \
  --follow \
  --profile wizipragma

# Ver logs del agent
aws logs tail /aws/lambda/wizipragma-agent-prod \
  --follow \
  --profile wizipragma
```

### CloudWatch Metrics
- Lambda invocations
- API Gateway requests
- Error rates
- Response times

Dashboard: https://console.aws.amazon.com/cloudwatch/

## Troubleshooting

### Error: "Access Denied"
- Verificar credenciales AWS
- Verificar permisos IAM
- Verificar que estás usando el perfil correcto

### Error: "Function not found"
- Verificar que la función Lambda existe
- Verificar la región correcta
- Verificar el nombre de la función

### Frontend no carga
- Verificar que el bucket S3 es público
- Verificar CloudFront distribution
- Verificar DNS en Route 53

## Costos Estimados

- **Lambda**: $0.20 por millón de requests
- **API Gateway**: $3.50 por millón de requests
- **S3**: $0.023 por GB/mes
- **CloudFront**: $0.085 por GB transferido

**Total estimado**: $20-100/mes dependiendo del tráfico
