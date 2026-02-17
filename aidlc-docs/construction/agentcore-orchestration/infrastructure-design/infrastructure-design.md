# Infrastructure Design - Unit 2: AgentCore & Orchestration

## Overview

This document specifies the AWS infrastructure resources for Unit 2, building upon the logical components defined in NFR Design.

**Base Infrastructure**: Leverages Unit 1 (EventBridge bus, S3 bucket, IAM role, CloudWatch log group)

---

## 1. SAM Template Resources

### 1.1 WebSocket API

```yaml
CentliWebSocketAPI:
  Type: AWS::ApiGatewayV2::Api
  Properties:
    Name: centli-websocket-api
    ProtocolType: WEBSOCKET
    RouteSelectionExpression: $request.body.action
    Tags:
      Project: CENTLI
      Environment: Hackathon

CentliWebSocketStage:
  Type: AWS::ApiGatewayV2::Stage
  Properties:
    ApiId: !Ref CentliWebSocketAPI
    StageName: prod
    AutoDeploy: true
    DefaultRouteSettings:
      ThrottlingBurstLimit: 100
      ThrottlingRateLimit: 50
```

### 1.2 Lambda Functions

```yaml
ConnectFunction:
  Type: AWS::Serverless::Function
  Properties:
    FunctionName: centli-app-connect
    CodeUri: src_aws/app_connect/
    Handler: app_connect.lambda_handler
    Runtime: python3.11
    MemorySize: 512
    Timeout: 30
    Role: !ImportValue CentliLambdaExecutionRoleArn
    Environment:
      Variables:
        SESSIONS_TABLE: !Ref SessionsTable
        LOG_LEVEL: INFO

DisconnectFunction:
  Type: AWS::Serverless::Function
  Properties:
    FunctionName: centli-app-disconnect
    CodeUri: src_aws/app_disconnect/
    Handler: app_disconnect.lambda_handler
    Runtime: python3.11
    MemorySize: 512
    Timeout: 30
    Role: !ImportValue CentliLambdaExecutionRoleArn
    Environment:
      Variables:
        SESSIONS_TABLE: !Ref SessionsTable
        LOG_LEVEL: INFO

MessageFunction:
  Type: AWS::Serverless::Function
  Properties:
    FunctionName: centli-app-message
    CodeUri: src_aws/app_message/
    Handler: app_message.lambda_handler
    Runtime: python3.11
    MemorySize: 512
    Timeout: 30
    Role: !ImportValue CentliLambdaExecutionRoleArn
    Environment:
      Variables:
        SESSIONS_TABLE: !Ref SessionsTable
        EVENT_BUS_NAME: !ImportValue CentliEventBusName
        AGENTCORE_ID: !Ref AgentCoreAgent
        ASSETS_BUCKET: !ImportValue CentliAssetsBucketName
        LOG_LEVEL: INFO
```

### 1.3 WebSocket Routes

```yaml
ConnectRoute:
  Type: AWS::ApiGatewayV2::Route
  Properties:
    ApiId: !Ref CentliWebSocketAPI
    RouteKey: $connect
    AuthorizationType: NONE
    Target: !Sub integrations/${ConnectIntegration}

DisconnectRoute:
  Type: AWS::ApiGatewayV2::Route
  Properties:
    ApiId: !Ref CentliWebSocketAPI
    RouteKey: $disconnect
    Target: !Sub integrations/${DisconnectIntegration}

DefaultRoute:
  Type: AWS::ApiGatewayV2::Route
  Properties:
    ApiId: !Ref CentliWebSocketAPI
    RouteKey: $default
    Target: !Sub integrations/${MessageIntegration}

ConnectIntegration:
  Type: AWS::ApiGatewayV2::Integration
  Properties:
    ApiId: !Ref CentliWebSocketAPI
    IntegrationType: AWS_PROXY
    IntegrationUri: !Sub arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${ConnectFunction.Arn}/invocations

DisconnectIntegration:
  Type: AWS::ApiGatewayV2::Integration
  Properties:
    ApiId: !Ref CentliWebSocketAPI
    IntegrationType: AWS_PROXY
    IntegrationUri: !Sub arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${DisconnectFunction.Arn}/invocations

MessageIntegration:
  Type: AWS::ApiGatewayV2::Integration
  Properties:
    ApiId: !Ref CentliWebSocketAPI
    IntegrationType: AWS_PROXY
    IntegrationUri: !Sub arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${MessageFunction.Arn}/invocations
```

### 1.4 Lambda Permissions

```yaml
ConnectPermission:
  Type: AWS::Lambda::Permission
  Properties:
    FunctionName: !Ref ConnectFunction
    Action: lambda:InvokeFunction
    Principal: apigateway.amazonaws.com
    SourceArn: !Sub arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${CentliWebSocketAPI}/*

DisconnectPermission:
  Type: AWS::Lambda::Permission
  Properties:
    FunctionName: !Ref DisconnectFunction
    Action: lambda:InvokeFunction
    Principal: apigateway.amazonaws.com
    SourceArn: !Sub arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${CentliWebSocketAPI}/*

MessagePermission:
  Type: AWS::Lambda::Permission
  Properties:
    FunctionName: !Ref MessageFunction
    Action: lambda:InvokeFunction
    Principal: apigateway.amazonaws.com
    SourceArn: !Sub arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${CentliWebSocketAPI}/*
```

### 1.5 DynamoDB Sessions Table

```yaml
SessionsTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: centli-sessions
    BillingMode: PAY_PER_REQUEST
    AttributeDefinitions:
      - AttributeName: session_id
        AttributeType: S
      - AttributeName: user_id
        AttributeType: S
    KeySchema:
      - AttributeName: session_id
        KeyType: HASH
    GlobalSecondaryIndexes:
      - IndexName: user-index
        KeySchema:
          - AttributeName: user_id
            KeyType: HASH
        Projection:
          ProjectionType: ALL
    TimeToLiveSpecification:
      AttributeName: expires_at
      Enabled: true
    SSESpecification:
      SSEEnabled: true
    Tags:
      - Key: Project
        Value: CENTLI
      - Key: Environment
        Value: Hackathon
```

### 1.6 Bedrock AgentCore (Manual Configuration)

**Note**: Bedrock AgentCore cannot be created via SAM/CloudFormation. Must be configured manually via AWS Console or AWS CLI.

**Configuration Steps** (documented for manual execution):
1. Create Bedrock Agent via Console
2. Configure foundation model: Claude 3.7 Sonnet
3. Enable Managed Memory (DynamoDB backend)
4. Create 3 Action Groups (CoreBanking, Marketplace, CRM)
5. Configure Action Groups with EventBridge integration
6. Test agent with sample prompts

**Agent Configuration**:
```json
{
  "agentName": "centli-agent",
  "foundationModel": "anthropic.claude-3-7-sonnet-20250219-v1:0",
  "instruction": "You are CENTLI, a friendly Mexican banking assistant...",
  "idleSessionTTLInSeconds": 900,
  "agentResourceRoleArn": "<CentliLambdaExecutionRoleArn>"
}
```

### 1.7 Outputs

```yaml
Outputs:
  WebSocketURL:
    Description: WebSocket API URL
    Value: !Sub wss://${CentliWebSocketAPI}.execute-api.${AWS::Region}.amazonaws.com/prod
    Export:
      Name: CentliWebSocketURL
  
  SessionsTableName:
    Description: Sessions DynamoDB table name
    Value: !Ref SessionsTable
    Export:
      Name: CentliSessionsTableName
  
  ConnectFunctionArn:
    Description: Connect Lambda function ARN
    Value: !GetAtt ConnectFunction.Arn
    Export:
      Name: CentliConnectFunctionArn
  
  MessageFunctionArn:
    Description: Message Lambda function ARN
    Value: !GetAtt MessageFunction.Arn
    Export:
      Name: CentliMessageFunctionArn
```

---

## 2. IAM Policy Extensions

### 2.1 Additional Bedrock Permissions

Add to `CentliLambdaExecutionRole` (from Unit 1):

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeAgent",
    "bedrock:InvokeModel",
    "bedrock:GetAgent",
    "bedrock:ListAgents"
  ],
  "Resource": "*"
}
```

### 2.2 API Gateway Management Permissions

Add to `CentliLambdaExecutionRole`:

```json
{
  "Effect": "Allow",
  "Action": [
    "execute-api:ManageConnections",
    "execute-api:Invoke"
  ],
  "Resource": "arn:aws:execute-api:*:*:*/@connections/*"
}
```

---

## 3. Resource Dependencies

```
Unit 1 Resources (Already Deployed)
  ├── EventBridge Bus (centli-event-bus)
  ├── S3 Bucket (centli-assets-*)
  ├── IAM Role (CentliLambdaExecutionRole)
  └── CloudWatch Log Group (/aws/lambda/centli)

Unit 2 Resources (This Unit)
  ├── WebSocket API
  │   ├── $connect Route → ConnectFunction
  │   ├── $disconnect Route → DisconnectFunction
  │   └── $default Route → MessageFunction
  ├── Lambda Functions
  │   ├── ConnectFunction (uses IAM Role from Unit 1)
  │   ├── DisconnectFunction (uses IAM Role from Unit 1)
  │   └── MessageFunction (uses IAM Role from Unit 1)
  ├── DynamoDB Table (centli-sessions)
  └── Bedrock AgentCore (manual configuration)
```

---

## 4. Environment Variables

### 4.1 Connect Function
```
SESSIONS_TABLE=centli-sessions
LOG_LEVEL=INFO
```

### 4.2 Disconnect Function
```
SESSIONS_TABLE=centli-sessions
LOG_LEVEL=INFO
```

### 4.3 Message Function
```
SESSIONS_TABLE=centli-sessions
EVENT_BUS_NAME=centli-event-bus
AGENTCORE_ID=<agent-id-from-bedrock>
ASSETS_BUCKET=centli-assets-777937796305
LOG_LEVEL=INFO
```

---

## 5. Deployment Sequence

1. **Verify Unit 1 deployed** (EventBridge, S3, IAM, CloudWatch)
2. **Deploy Unit 2 SAM template** (WebSocket API, Lambdas, DynamoDB)
3. **Configure Bedrock AgentCore manually** (via Console/CLI)
4. **Update Message Function** with AgentCore ID
5. **Test WebSocket connection** (connect, send message, disconnect)

---

## 6. Resource Naming Conventions

| Resource Type | Naming Pattern | Example |
|---------------|----------------|---------|
| Lambda Function | `centli-app-{function}` | `centli-app-connect` |
| DynamoDB Table | `centli-{purpose}` | `centli-sessions` |
| API Gateway | `centli-{type}-api` | `centli-websocket-api` |
| IAM Role | `Centli{Purpose}Role` | `CentliLambdaExecutionRole` |
| CloudWatch Log | `/aws/lambda/centli-{function}` | `/aws/lambda/centli-app-connect` |

---

## 7. Cost Estimation (Demo Period: 8 hours)

| Service | Usage | Cost |
|---------|-------|------|
| Lambda | ~200 invocations, 512MB, 5s avg | $0.00 (free tier) |
| API Gateway | ~100 connections, ~500 messages | $0.00 (free tier) |
| DynamoDB | ~1000 reads, ~500 writes | $0.00 (free tier) |
| Bedrock AgentCore | ~100 invocations | ~$0.50 |
| Nova Sonic | ~50 voice requests | ~$0.25 |
| Nova Canvas | ~10 image requests | ~$0.10 |
| S3 | ~10 images, 7-day storage | $0.00 (negligible) |
| EventBridge | ~200 events | $0.00 (free tier) |
| **Total Estimated Cost** | | **~$0.85** |

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Infrastructure Resources**: 11 SAM resources + 1 manual Bedrock configuration

