# Infrastructure Design Plan - Unit 1: Infrastructure Foundation

## Unit Context

**Unit Name**: Infrastructure Foundation  
**Unit Type**: Configuration Unit (Shared Infrastructure)  
**Purpose**: Provide base AWS infrastructure resources required by all units  
**Duration**: 1 hour setup  
**Stories**: None (infrastructure only)

**Dependencies**: None (this is the foundation)  
**Dependents**: Units 2, 3, 4 (all depend on this infrastructure)

## Infrastructure Design Steps

### Step 1: Base SAM Template Structure
- [ ] Define base SAM template (`template.yaml`)
- [ ] Configure SAM metadata and parameters
- [ ] Set up template structure for nested stacks
- [ ] Define global configurations (runtime, timeout, memory)

### Step 2: EventBridge Event Bus
- [ ] Create EventBridge event bus resource (`centli-event-bus`)
- [ ] Configure event bus policies for cross-unit access
- [ ] Define event archive configuration (optional for debugging)
- [ ] Set up CloudWatch Events integration

### Step 3: S3 Bucket for Assets
- [ ] Create S3 bucket for images and static assets
- [ ] Configure bucket naming with account ID suffix
- [ ] Set up CORS configuration for frontend access
- [ ] Configure lifecycle policies (optional)
- [ ] Set up bucket policies for Lambda access

### Step 4: IAM Roles and Policies
- [ ] Create base Lambda execution role
- [ ] Define policies for EventBridge access
- [ ] Define policies for DynamoDB access
- [ ] Define policies for S3 access
- [ ] Define policies for Bedrock access
- [ ] Define policies for CloudWatch Logs
- [ ] Create cross-unit access policies

### Step 5: CloudWatch Log Groups
- [ ] Create base log group for all Lambdas (`/aws/lambda/centli`)
- [ ] Configure log retention (7 days for hackathon)
- [ ] Set up log group permissions

### Step 6: Nested Stack Configuration
- [ ] Define nested stack structure for Units 2, 3, 4
- [ ] Configure stack parameters for cross-stack references
- [ ] Set up outputs for shared resources (EventBridge ARN, S3 bucket name, IAM role ARNs)

### Step 7: Deployment Configuration
- [ ] Configure SAM deployment settings
- [ ] Define stack name and tags
- [ ] Set up parameter overrides for environments
- [ ] Document deployment commands

## Infrastructure Questions

### Q1: AWS Account Configuration
**Question**: ¿Ya tienes configurada una cuenta AWS con credenciales para el despliegue? ¿Qué región AWS prefieres usar?

[Answer]: Sí, cuenta AWS configurada con profile `777937796305_Ps-HackatonAgentic-Mexico` (Account ID: 777937796305). Región: us-east-1 (tiene todos los servicios Bedrock incluyendo Nova Sonic y Nova Canvas)

**Rationale**: Necesitamos confirmar la región AWS para configurar correctamente los recursos y asegurar que todos los servicios (Bedrock, Nova Sonic, Nova Canvas) estén disponibles.

---

### Q2: S3 Bucket Naming Strategy
**Question**: Para el bucket S3 de assets, ¿prefieres usar un nombre específico o dejamos que SAM genere uno automáticamente con el formato `centli-assets-${AWS::AccountId}`?

[Answer]: Auto-generado con formato `centli-assets-777937796305` (usando Account ID para garantizar unicidad global)

**Rationale**: Los nombres de buckets S3 deben ser únicos globalmente. Usar el Account ID garantiza unicidad.

---

### Q3: EventBridge Event Archive
**Question**: ¿Quieres habilitar el archivo de eventos en EventBridge para debugging durante el hackathon? (Esto permite replay de eventos pero consume storage)

[Answer]: NO - Para hackathon de 8 horas, simplificamos sin archivo de eventos. CloudWatch Logs es suficiente para debugging.

**Rationale**: El archivo de eventos es útil para debugging pero agrega complejidad. Para un hackathon de 8 horas, podría ser opcional.

---

### Q4: IAM Role Strategy
**Question**: ¿Prefieres un rol IAM compartido para todos los Lambdas o roles separados por unidad? (Compartido es más rápido, separado es más seguro)

[Answer]: Rol IAM compartido para todos los Lambdas - Acelera desarrollo para hackathon. Nombre: `CentliLambdaExecutionRole`

**Rationale**: Para un hackathon, un rol compartido acelera el desarrollo. Para producción, roles separados son mejores.

---

### Q5: Log Retention
**Question**: ¿7 días de retención de logs en CloudWatch es suficiente para el hackathon, o prefieres más tiempo?

[Answer]: 7 días de retención es suficiente para hackathon y post-hackathon debugging

**Rationale**: Más retención = más costo. Para un hackathon, 7 días es generoso. Para producción, típicamente 30-90 días.

---

### Q6: CORS Configuration
**Question**: Para el bucket S3, ¿desde qué orígenes necesitas permitir acceso CORS? ¿Solo localhost para desarrollo o también un dominio específico?

[Answer]: Permitir localhost (http://localhost:3000, http://localhost:8080, http://127.0.0.1:*) y wildcard para desarrollo rápido. Para demo, ajustaremos si es necesario.

**Rationale**: CORS es necesario para que el frontend pueda subir imágenes directamente a S3. Necesitamos saber los orígenes permitidos.

---

### Q7: Nested Stack Strategy
**Question**: ¿Prefieres desplegar todo en un solo stack SAM o usar nested stacks separados por unidad? (Single stack es más simple, nested stacks es más modular)

[Answer]: Single stack SAM - Más simple y rápido para hackathon. Nombre del stack: `centli-hackathon`

**Rationale**: Para un hackathon, un single stack es más rápido. Nested stacks son mejores para proyectos grandes pero agregan complejidad.

---

## Infrastructure Design Artifacts to Generate

1. **infrastructure-design.md** - Complete infrastructure design document
   - AWS services mapping
   - Resource naming conventions
   - IAM policies and roles
   - EventBridge configuration
   - S3 bucket configuration
   - CloudWatch configuration

2. **deployment-architecture.md** - Deployment architecture diagram and documentation
   - Infrastructure diagram (Mermaid)
   - Deployment sequence
   - Stack dependencies
   - Resource outputs and cross-references

3. **shared-infrastructure.md** - Shared infrastructure documentation
   - Shared resources catalog
   - Access patterns for Units 2, 3, 4
   - Integration contracts
   - Troubleshooting guide

## Success Criteria

- [x] All infrastructure questions answered
- [x] Infrastructure design artifacts generated
- [x] AWS services clearly mapped
- [x] IAM policies defined
- [x] EventBridge configuration specified
- [x] S3 bucket configuration specified
- [x] Deployment strategy documented
- [ ] User approval obtained

---

**Plan Status**: Infrastructure design artifacts generated, awaiting user approval  
**Next Step**: User review and approval to proceed to Code Generation
