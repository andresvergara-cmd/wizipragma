# Infrastructure Code Summary - Unit 1: Infrastructure Foundation

## Overview

This document summarizes all code generated for Unit 1 (Infrastructure Foundation), including SAM templates, configuration files, deployment scripts, and documentation.

**Generated**: 2026-02-17  
**Unit**: Infrastructure Foundation  
**Purpose**: Base AWS infrastructure for CENTLI multimodal banking assistant

---

## Files Generated

### 1. SAM Template (`template.yaml`)

**Location**: Workspace root  
**Type**: AWS SAM CloudFormation template  
**Lines**: ~300 lines  
**Purpose**: Define all AWS infrastructure resources

**Resources Defined**:
- `CentliEventBus` - EventBridge Event Bus for event-driven communication
- `CentliAssetsBucket` - S3 bucket for images and static assets
- `CentliAssetsBucketPolicy` - S3 bucket policy for Lambda access
- `CentliLambdaExecutionRole` - IAM role with 5 inline policies
- `CentliLogGroup` - CloudWatch Log Group for centralized logging

**Outputs Defined**:
- `EventBusArn` - EventBridge bus ARN (exported)
- `EventBusName` - EventBridge bus name (exported)
- `AssetsBucketName` - S3 bucket name (exported)
- `AssetsBucketArn` - S3 bucket ARN (exported)
- `LambdaExecutionRoleArn` - IAM role ARN (exported)
- `LogGroupName` - CloudWatch log group name (exported)
- `StackName` - CloudFormation stack name
- `Region` - AWS region
- `AccountId` - AWS account ID

**Key Features**:
- Globals section for Lambda defaults (Python 3.9, 512 MB, 30s timeout)
- Parameters for Environment and LogLevel
- Comprehensive tagging (Project, Environment, Unit)
- Placeholder sections for Units 2, 3, 4

---

### 2. SAM Configuration (`samconfig.toml`)

**Location**: Workspace root  
**Type**: TOML configuration file  
**Lines**: ~30 lines  
**Purpose**: SAM CLI deployment configuration

**Configuration Sections**:
- `[default.global.parameters]` - Stack name
- `[default.build.parameters]` - Build settings (cached, parallel)
- `[default.validate.parameters]` - Validation settings (lint)
- `[default.deploy.parameters]` - Deployment settings
  - Stack name: `centli-hackathon`
  - Region: `us-east-1`
  - Profile: `777937796305_Ps-HackatonAgentic-Mexico`
  - Capabilities: `CAPABILITY_NAMED_IAM`
  - Parameter overrides: `Environment=hackathon LogLevel=INFO`
  - Tags: `Project=CENTLI Environment=Hackathon`

**Benefits**:
- No need to specify parameters on every `sam deploy`
- Consistent deployment configuration
- Easy to modify for different environments

---

### 3. Deployment Script (`commands/deploy-infrastructure.sh`)

**Location**: `commands/deploy-infrastructure.sh`  
**Type**: Bash shell script  
**Lines**: ~100 lines  
**Purpose**: Automated infrastructure deployment

**Script Steps**:
1. Validate AWS credentials
2. Validate SAM template
3. Build SAM application
4. Deploy to AWS
5. Verify stack status
6. Retrieve and display stack outputs

**Features**:
- Color-coded output (green for success, yellow for info, red for errors)
- Error handling with `set -e`
- Detailed progress messages
- Automatic stack output display
- Next steps guidance

**Usage**:
```bash
./commands/deploy-infrastructure.sh
```

**Expected Output**:
```
=========================================
CENTLI Infrastructure Deployment
=========================================

Step 1: Validating AWS credentials...
✓ AWS Account: 777937796305
✓ AWS Region: us-east-1

Step 2: Validating SAM template...
✓ SAM template is valid

Step 3: Building SAM application...
✓ SAM build completed

Step 4: Deploying to AWS...
Stack Name: centli-hackathon
This may take a few minutes...
✓ Deployment completed

Step 5: Verifying stack status...
✓ Stack Status: CREATE_COMPLETE

Step 6: Retrieving stack outputs...
[Stack outputs table]

=========================================
Deployment Successful!
=========================================
```

---

### 4. Cleanup Script (`commands/cleanup-infrastructure.sh`)

**Location**: `commands/cleanup-infrastructure.sh`  
**Type**: Bash shell script  
**Lines**: ~120 lines  
**Purpose**: Complete infrastructure teardown

**Script Steps**:
1. Validate AWS credentials
2. Check if stack exists
3. Empty S3 bucket (required before deletion)
4. Delete CloudFormation stack
5. Wait for stack deletion
6. Verify deletion

**Features**:
- Confirmation prompt before deletion
- S3 bucket cleanup (empties before deletion)
- Wait for complete deletion
- Verification of successful cleanup
- Error handling

**Usage**:
```bash
./commands/cleanup-infrastructure.sh
```

**Safety Features**:
- Requires explicit "yes" confirmation
- Shows stack name and region before deletion
- Validates credentials before proceeding

---

## IAM Permissions Breakdown

### CentliLambdaExecutionRole

**Managed Policies**:
- `AWSLambdaBasicExecutionRole` - CloudWatch Logs write access

**Inline Policies**:

#### 1. CentliEventBridgePolicy
- **Actions**: `events:PutEvents`
- **Resources**: `centli-event-bus` ARN
- **Purpose**: Publish events to EventBridge

#### 2. CentliDynamoDBPolicy
- **Actions**: GetItem, PutItem, UpdateItem, DeleteItem, Query, Scan, BatchGetItem, BatchWriteItem
- **Resources**: `centli-*` tables and indexes
- **Purpose**: Full DynamoDB access for all CENTLI tables

#### 3. CentliS3Policy
- **Actions**: GetObject, PutObject, DeleteObject, ListBucket
- **Resources**: `centli-assets-*` bucket and objects
- **Purpose**: Read/write access to assets bucket

#### 4. CentliBedrockPolicy
- **Actions**: InvokeModel, InvokeAgent, Retrieve, InvokeModelWithResponseStream
- **Resources**: Foundation models, agents, agent aliases, knowledge bases
- **Purpose**: Full Bedrock access for AI operations

#### 5. CentliAPIGatewayPolicy
- **Actions**: ManageConnections, Invoke
- **Resources**: API Gateway connections
- **Purpose**: WebSocket connection management

---

## EventBridge Configuration

### Event Bus
- **Name**: `centli-event-bus`
- **Purpose**: Event-driven communication between AgentCore and Action Groups
- **Event Archive**: Disabled (for hackathon simplicity)

### Event Patterns (to be configured in Units 2, 3)

**ActionRequest** (AgentCore → Action Groups):
- Source: `centli.agentcore`
- DetailType: `ActionRequest`

**ActionResponse** (Action Groups → AgentCore):
- Source: `centli.actiongroup.{corebanking|marketplace|crm}`
- DetailType: `ActionResponse`

**PaymentRequest** (Marketplace → Core Banking):
- Source: `centli.actiongroup.marketplace`
- DetailType: `PaymentRequest`

---

## S3 Bucket Configuration

### Bucket Details
- **Name**: `centli-assets-777937796305`
- **Purpose**: Store user-uploaded images and static assets
- **Public Access**: Blocked (all 4 settings enabled)

### CORS Configuration
```yaml
AllowedOrigins:
  - 'http://localhost:3000'
  - 'http://localhost:8080'
  - 'http://127.0.0.1:*'
AllowedMethods:
  - GET
  - PUT
  - POST
  - DELETE
AllowedHeaders:
  - '*'
MaxAge: 3600
```

### Bucket Policy
- Allows Lambda execution role to GetObject, PutObject, DeleteObject
- No public access

### Key Structure (to be used by Units 2, 4)
- Images: `images/{user_id}/{timestamp}_{filename}`
- Static assets: `static/{asset_type}/{filename}`

---

## CloudWatch Logs Configuration

### Log Group
- **Name**: `/aws/lambda/centli`
- **Retention**: 7 days
- **Purpose**: Centralized logging for all Lambda functions

### Log Format (recommended)
```json
{
  "timestamp": "2026-02-17T00:00:00Z",
  "level": "INFO",
  "unit": "agentcore",
  "function": "message_handler",
  "message": "Processing user message",
  "context": {
    "user_id": "user_carlos",
    "session_id": "sess_123",
    "request_id": "req_456"
  }
}
```

---

## Deployment Commands

### Initial Deployment
```bash
# Option 1: Using deployment script (recommended)
./commands/deploy-infrastructure.sh

# Option 2: Using SAM CLI directly
sam build
sam deploy
```

### Update Deployment
```bash
# Rebuild and redeploy
sam build && sam deploy
```

### Validate Template
```bash
sam validate --profile 777937796305_Ps-HackatonAgentic-Mexico --region us-east-1
```

### Get Stack Outputs
```bash
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Stacks[0].Outputs' \
  --output table
```

### Delete Stack
```bash
# Option 1: Using cleanup script (recommended)
./commands/cleanup-infrastructure.sh

# Option 2: Using AWS CLI directly
aws cloudformation delete-stack \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

---

## Verification Steps

### After Deployment

1. **Verify Stack Status**:
```bash
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Stacks[0].StackStatus'
```
Expected: `CREATE_COMPLETE` or `UPDATE_COMPLETE`

2. **Verify EventBridge Bus**:
```bash
aws events describe-event-bus \
  --name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

3. **Verify S3 Bucket**:
```bash
aws s3 ls s3://centli-assets-777937796305 \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

4. **Verify IAM Role**:
```bash
aws iam get-role \
  --role-name CentliLambdaExecutionRole \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

5. **Verify CloudWatch Log Group**:
```bash
aws logs describe-log-groups \
  --log-group-name-prefix /aws/lambda/centli \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

---

## Troubleshooting

### Issue: SAM Validation Fails

**Symptoms**: `sam validate` returns errors

**Solutions**:
1. Check YAML syntax (indentation, colons, quotes)
2. Verify resource names are unique
3. Check CloudFormation resource types are correct
4. Review error message for specific issue

### Issue: Deployment Fails

**Symptoms**: `sam deploy` fails with error

**Common Causes**:
- IAM permissions insufficient
- Resource name conflicts
- Region doesn't support service
- S3 bucket name already taken

**Solutions**:
1. Check CloudFormation events in AWS Console
2. Review error message for specific resource
3. Verify IAM permissions for CloudFormation
4. Check if resources already exist

### Issue: Stack Deletion Fails

**Symptoms**: Stack deletion hangs or fails

**Common Causes**:
- S3 bucket not empty
- Resources have dependencies
- Manual resources created outside CloudFormation

**Solutions**:
1. Empty S3 bucket manually
2. Delete dependent resources first
3. Check CloudFormation events for specific error
4. Use cleanup script which handles S3 bucket

---

## Cost Estimation

### Unit 1 Resources (Monthly)

| Resource | Usage | Cost |
|----------|-------|------|
| EventBridge | ~10,000 events/month | $0.00 (free tier) |
| S3 | ~1 GB storage, ~10,000 requests | $0.03 |
| CloudWatch Logs | ~1 GB logs, 7 days retention | $0.50 |
| IAM | Roles and policies | $0.00 (free) |

**Total Unit 1 Cost**: ~$0.53/month

**Note**: Most costs come from Units 2, 3 (Lambda, DynamoDB, Bedrock)

---

## Next Steps

After Unit 1 deployment:

1. **Verify all outputs** - Ensure EventBusArn, AssetsBucketName, LambdaExecutionRoleArn are available
2. **Proceed to Unit 2** - AgentCore & Orchestration (WebSocket API, Lambdas, Bedrock)
3. **Proceed to Unit 3** - Action Groups (Core Banking, Marketplace, CRM Lambdas)
4. **Proceed to Unit 4** - Frontend (Static website, WebSocket client)

---

## Summary

Unit 1 code generation created:
- ✅ Complete SAM template with 5 resources
- ✅ SAM configuration file for consistent deployments
- ✅ Automated deployment script with validation
- ✅ Automated cleanup script with safety checks
- ✅ 9 stack outputs for cross-unit integration
- ✅ Comprehensive IAM permissions (5 inline policies)
- ✅ EventBridge event bus for event-driven architecture
- ✅ S3 bucket with CORS for frontend uploads
- ✅ CloudWatch Logs for centralized logging

**Infrastructure foundation is ready for Units 2, 3, 4 to build upon.**
