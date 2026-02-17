# Infrastructure Design - Unit 1: Infrastructure Foundation

## Overview

This document defines the complete AWS infrastructure design for CENTLI, providing the foundation resources that all other units depend on.

**Unit**: Infrastructure Foundation  
**Type**: Configuration Unit (Shared Infrastructure)  
**AWS Account**: 777937796305  
**AWS Profile**: 777937796305_Ps-HackatonAgentic-Mexico  
**Region**: us-east-1  
**Stack Name**: centli-hackathon

---

## AWS Services Mapping

### Core Infrastructure Services

| Service | Resource Name | Purpose | Used By |
|---------|--------------|---------|---------|
| EventBridge | centli-event-bus | Event-driven communication between units | Units 2, 3 |
| S3 | centli-assets-777937796305 | Image storage and static assets | Units 2, 4 |
| IAM | CentliLambdaExecutionRole | Lambda execution permissions | Units 2, 3 |
| CloudWatch Logs | /aws/lambda/centli | Centralized logging | Units 2, 3, 4 |
| SAM | centli-hackathon | Infrastructure as Code deployment | All units |

---

## 1. EventBridge Event Bus

### Resource Configuration

```yaml
CentliEventBus:
  Type: AWS::Events::EventBus
  Properties:
    Name: centli-event-bus
    Tags:
      - Key: Project
        Value: CENTLI
      - Key: Environment
        Value: Hackathon
```

### Event Patterns

**ActionRequest Events** (AgentCore → Action Groups):
```json
{
  "source": ["centli.agentcore"],
  "detail-type": ["ActionRequest"]
}
```

**ActionResponse Events** (Action Groups → AgentCore):
```json
{
  "source": ["centli.actiongroup.corebanking", "centli.actiongroup.marketplace", "centli.actiongroup.crm"],
  "detail-type": ["ActionResponse"]
}
```

**PaymentRequest Events** (Marketplace → Core Banking):
```json
{
  "source": ["centli.actiongroup.marketplace"],
  "detail-type": ["PaymentRequest"]
}
```

### Event Archive

**Status**: Disabled for hackathon (simplicity over debugging capability)

**Rationale**: CloudWatch Logs provide sufficient debugging. Event archive adds complexity and storage costs unnecessary for 8-hour hackathon.

---

## 2. S3 Bucket for Assets

### Resource Configuration

```yaml
CentliAssetsBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: centli-assets-777937796305
    CorsConfiguration:
      CorsRules:
        - AllowedOrigins:
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
    PublicAccessBlockConfiguration:
      BlockPublicAcls: true
      BlockPublicPolicy: true
      IgnorePublicAcls: true
      RestrictPublicBuckets: true
    Tags:
      - Key: Project
        Value: CENTLI
      - Key: Environment
        Value: Hackathon
```

### Bucket Policy

```yaml
CentliAssetsBucketPolicy:
  Type: AWS::S3::BucketPolicy
  Properties:
    Bucket: !Ref CentliAssetsBucket
    PolicyDocument:
      Statement:
        - Sid: AllowLambdaAccess
          Effect: Allow
          Principal:
            AWS: !GetAtt CentliLambdaExecutionRole.Arn
          Action:
            - 's3:GetObject'
            - 's3:PutObject'
            - 's3:DeleteObject'
          Resource: !Sub '${CentliAssetsBucket.Arn}/*'
```

### Usage Patterns

**Image Uploads** (Unit 4 Frontend → S3):
- User captures/selects image
- Frontend uploads directly to S3 with presigned URL
- S3 key format: `images/{user_id}/{timestamp}_{filename}`

**Image Processing** (Unit 2 AgentCore → S3):
- AgentCore retrieves image from S3
- Passes to Nova Canvas for analysis
- Stores analysis results in session state

---

## 3. IAM Roles and Policies

### Lambda Execution Role

```yaml
CentliLambdaExecutionRole:
  Type: AWS::IAM::Role
  Properties:
    RoleName: CentliLambdaExecutionRole
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
          Action: 'sts:AssumeRole'
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    Policies:
      - PolicyName: CentliEventBridgePolicy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - 'events:PutEvents'
              Resource: !GetAtt CentliEventBus.Arn
      
      - PolicyName: CentliDynamoDBPolicy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - 'dynamodb:GetItem'
                - 'dynamodb:PutItem'
                - 'dynamodb:UpdateItem'
                - 'dynamodb:DeleteItem'
                - 'dynamodb:Query'
                - 'dynamodb:Scan'
              Resource:
                - !Sub 'arn:aws:dynamodb:${AWS::Region}:${AWS::AccountId}:table/centli-*'
      
      - PolicyName: CentliS3Policy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - 's3:GetObject'
                - 's3:PutObject'
                - 's3:DeleteObject'
              Resource: !Sub '${CentliAssetsBucket.Arn}/*'
      
      - PolicyName: CentliBedrockPolicy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - 'bedrock:InvokeModel'
                - 'bedrock:InvokeAgent'
                - 'bedrock:Retrieve'
              Resource:
                - !Sub 'arn:aws:bedrock:${AWS::Region}::foundation-model/*'
                - !Sub 'arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:agent/*'
                - !Sub 'arn:aws:bedrock:${AWS::Region}:${AWS::AccountId}:knowledge-base/*'
      
      - PolicyName: CentliAPIGatewayPolicy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - 'execute-api:ManageConnections'
              Resource: !Sub 'arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:*/@connections/*'
    Tags:
      - Key: Project
        Value: CENTLI
      - Key: Environment
        Value: Hackathon
```

### Permission Breakdown

| Permission | Service | Actions | Used By |
|------------|---------|---------|---------|
| EventBridge | events | PutEvents | Units 2, 3 (publish events) |
| DynamoDB | dynamodb | GetItem, PutItem, UpdateItem, DeleteItem, Query, Scan | Units 2, 3 (data operations) |
| S3 | s3 | GetObject, PutObject, DeleteObject | Units 2, 4 (image storage) |
| Bedrock | bedrock | InvokeModel, InvokeAgent, Retrieve | Unit 2 (AI operations) |
| API Gateway | execute-api | ManageConnections | Unit 2 (WebSocket messages) |

---

## 4. CloudWatch Log Groups

### Resource Configuration

```yaml
CentliLogGroup:
  Type: AWS::Logs::LogGroup
  Properties:
    LogGroupName: /aws/lambda/centli
    RetentionInDays: 7
    Tags:
      - Key: Project
        Value: CENTLI
      - Key: Environment
        Value: Hackathon
```

### Log Retention Strategy

**Retention Period**: 7 days  
**Rationale**: Sufficient for hackathon and post-hackathon debugging. Balances debugging needs with cost.

**Log Levels**:
- ERROR: Always logged
- WARN: Logged for important warnings
- INFO: Logged for key operations (transfers, purchases)
- DEBUG: Optional, enable for troubleshooting

### Log Structure

All Lambda functions will log to `/aws/lambda/centli` with structured JSON format:

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

## 5. SAM Template Structure

### Base Template Configuration

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Description: >
  CENTLI - Multimodal Banking Assistant Hackathon
  Complete infrastructure for AgentCore, Action Groups, and Frontend

Globals:
  Function:
    Runtime: python3.9
    Timeout: 30
    MemorySize: 512
    Environment:
      Variables:
        EVENT_BUS_NAME: centli-event-bus
        ASSETS_BUCKET_NAME: centli-assets-777937796305
        LOG_LEVEL: INFO
        AWS_ACCOUNT_ID: '777937796305'
        AWS_REGION: us-east-1
    Tags:
      Project: CENTLI
      Environment: Hackathon

Parameters:
  Environment:
    Type: String
    Default: hackathon
    Description: Environment name
  
  LogLevel:
    Type: String
    Default: INFO
    AllowedValues:
      - DEBUG
      - INFO
      - WARN
      - ERROR
    Description: CloudWatch log level

Resources:
  # Infrastructure Foundation (Unit 1)
  # - EventBridge Event Bus
  # - S3 Assets Bucket
  # - IAM Roles
  # - CloudWatch Log Groups
  
  # AgentCore & Orchestration (Unit 2)
  # - WebSocket API Gateway
  # - Connect/Disconnect/Message Lambdas
  # - Sessions DynamoDB Table
  # - Bedrock Agent Configuration
  
  # Action Groups (Unit 3)
  # - Core Banking Lambda
  # - Marketplace Lambda
  # - CRM Lambda
  # - 6 DynamoDB Tables
  # - EventBridge Rules
  
  # Frontend (Unit 4)
  # - S3 Static Website (optional)
  # - CloudFront Distribution (optional)

Outputs:
  EventBusArn:
    Description: EventBridge Event Bus ARN
    Value: !GetAtt CentliEventBus.Arn
    Export:
      Name: !Sub '${AWS::StackName}-EventBusArn'
  
  AssetsBucketName:
    Description: S3 Assets Bucket Name
    Value: !Ref CentliAssetsBucket
    Export:
      Name: !Sub '${AWS::StackName}-AssetsBucketName'
  
  LambdaExecutionRoleArn:
    Description: Lambda Execution Role ARN
    Value: !GetAtt CentliLambdaExecutionRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-LambdaExecutionRoleArn'
  
  LogGroupName:
    Description: CloudWatch Log Group Name
    Value: !Ref CentliLogGroup
    Export:
      Name: !Sub '${AWS::StackName}-LogGroupName'
```

### Stack Strategy

**Approach**: Single SAM stack for all units  
**Rationale**: Simpler and faster for hackathon. All resources in one template.

**Stack Name**: `centli-hackathon`  
**Deployment Command**:
```bash
sam build && sam deploy \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides Environment=hackathon LogLevel=INFO
```

---

## 6. Resource Naming Conventions

### Naming Pattern

All resources follow the pattern: `centli-{resource-type}-{identifier}`

| Resource Type | Naming Pattern | Example |
|--------------|----------------|---------|
| EventBridge Bus | centli-event-bus | centli-event-bus |
| S3 Bucket | centli-assets-{account-id} | centli-assets-777937796305 |
| IAM Role | Centli{Purpose}Role | CentliLambdaExecutionRole |
| Lambda Function | centli-{unit}-{function} | centli-agentcore-message |
| DynamoDB Table | centli-{entity} | centli-sessions, centli-accounts |
| CloudWatch Log Group | /aws/lambda/centli | /aws/lambda/centli |
| API Gateway | centli-websocket-api | centli-websocket-api |

### Tagging Strategy

All resources tagged with:
- **Project**: CENTLI
- **Environment**: Hackathon
- **Unit**: {unit-name} (for unit-specific resources)

---

## 7. Cross-Unit Integration

### Shared Resources Access

| Resource | Unit 2 (AgentCore) | Unit 3 (Action Groups) | Unit 4 (Frontend) |
|----------|-------------------|----------------------|------------------|
| EventBridge | Publish/Subscribe | Publish/Subscribe | - |
| S3 Bucket | Read/Write | - | Write (uploads) |
| IAM Role | Use | Use | - |
| CloudWatch Logs | Write | Write | - |

### Resource Outputs

Stack outputs enable cross-unit references:
- `EventBusArn`: Used by Units 2, 3 for event publishing
- `AssetsBucketName`: Used by Units 2, 4 for image operations
- `LambdaExecutionRoleArn`: Used by Units 2, 3 for Lambda functions
- `LogGroupName`: Used by all units for logging configuration

---

## 8. Security Considerations

### IAM Least Privilege

**Current Approach**: Shared role with broad permissions for hackathon speed  
**Production Recommendation**: Separate roles per unit with minimal permissions

### S3 Bucket Security

- Public access blocked
- CORS restricted to localhost origins
- Bucket policy limits access to Lambda role only
- No public read/write access

### EventBridge Security

- Event bus accessible only within AWS account
- No cross-account access configured
- Event patterns restrict source/detail-type

### API Gateway Security

- WebSocket connections require authentication token
- Connection IDs are ephemeral and non-guessable
- Rate limiting can be added if needed

---

## 9. Cost Estimation (Hackathon)

| Service | Usage | Estimated Cost |
|---------|-------|---------------|
| EventBridge | ~1000 events | $0.00 (free tier) |
| S3 | ~100 MB storage, ~1000 requests | $0.00 (free tier) |
| CloudWatch Logs | ~1 GB logs, 7 days retention | $0.50 |
| Lambda | ~10,000 invocations, 512 MB | $0.00 (free tier) |
| Bedrock | ~100 AgentCore invocations | $5.00 |
| Bedrock Nova Sonic | ~50 voice requests | $2.00 |
| Bedrock Nova Canvas | ~20 image requests | $1.00 |
| API Gateway WebSocket | ~100 connections, ~1000 messages | $0.00 (free tier) |
| DynamoDB | ~1000 read/write units | $0.00 (free tier) |
| **Total Estimated Cost** | | **~$8.50** |

**Note**: Most services stay within free tier for hackathon usage. Bedrock is the primary cost driver.

---

## 10. Deployment Sequence

### Step 1: Validate AWS Configuration
```bash
aws sts get-caller-identity --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Step 2: Build SAM Application
```bash
sam build
```

### Step 3: Deploy Infrastructure
```bash
sam deploy \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides Environment=hackathon LogLevel=INFO
```

### Step 4: Verify Deployment
```bash
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Stacks[0].StackStatus'
```

### Step 5: Get Stack Outputs
```bash
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Stacks[0].Outputs'
```

---

## 11. Troubleshooting Guide

### Issue: Stack Deployment Fails

**Symptoms**: SAM deploy returns error  
**Possible Causes**:
- IAM permissions insufficient
- Resource name conflicts
- Region doesn't support service

**Solutions**:
1. Check IAM permissions for CloudFormation, Lambda, EventBridge, S3, DynamoDB
2. Verify stack name is unique
3. Confirm us-east-1 region is configured
4. Review CloudFormation events for specific error

### Issue: EventBridge Events Not Delivered

**Symptoms**: Events published but not received  
**Possible Causes**:
- Event pattern mismatch
- Lambda not subscribed to event bus
- IAM permissions missing

**Solutions**:
1. Verify event pattern matches published events
2. Check EventBridge rules are created
3. Confirm Lambda has EventBridge trigger
4. Review CloudWatch Logs for Lambda invocations

### Issue: S3 CORS Errors

**Symptoms**: Frontend can't upload images  
**Possible Causes**:
- CORS configuration incorrect
- Origin not allowed
- Bucket policy restrictive

**Solutions**:
1. Verify CORS configuration includes frontend origin
2. Check browser console for specific CORS error
3. Test with curl to isolate issue
4. Review S3 bucket policy

---

## Summary

Unit 1 provides the complete infrastructure foundation for CENTLI:
- ✅ EventBridge for event-driven communication
- ✅ S3 for image and asset storage
- ✅ IAM roles with appropriate permissions
- ✅ CloudWatch Logs for centralized logging
- ✅ Single SAM stack for simplified deployment
- ✅ Cost-optimized for hackathon (~$8.50 total)
- ✅ Security best practices applied
- ✅ Ready for Units 2, 3, 4 to build upon

**Next Steps**: Proceed to Code Generation to create the actual SAM template and deployment scripts.
