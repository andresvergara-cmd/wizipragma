# Deployment Architecture - Unit 2: AgentCore & Orchestration

## Overview

This document defines the deployment sequence, resource dependencies, and integration points for Unit 2.

---

## 1. Deployment Sequence

### Phase 1: Pre-Deployment Verification
```bash
# Verify Unit 1 is deployed
aws cloudformation describe-stacks --stack-name centli-infrastructure-foundation

# Verify exports are available
aws cloudformation list-exports | grep Centli
```

### Phase 2: Deploy Unit 2 SAM Template
```bash
# Build Lambda functions
sam build --template template-unit2.yaml

# Deploy to AWS
sam deploy \
  --template-file .aws-sam/build/template.yaml \
  --stack-name centli-agentcore-orchestration \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    Environment=Hackathon \
    LogLevel=INFO \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

### Phase 3: Configure Bedrock AgentCore (Manual)
```bash
# Create Bedrock Agent
aws bedrock-agent create-agent \
  --agent-name centli-agent \
  --foundation-model anthropic.claude-3-7-sonnet-20250219-v1:0 \
  --instruction "You are CENTLI, a friendly Mexican banking assistant..." \
  --agent-resource-role-arn <CentliLambdaExecutionRoleArn> \
  --idle-session-ttl-in-seconds 900

# Enable Managed Memory
aws bedrock-agent update-agent \
  --agent-id <agent-id> \
  --memory-configuration '{"enabledMemoryTypes":["SESSION_SUMMARY"],"storageDays":1}'

# Create Action Groups (3 groups: CoreBanking, Marketplace, CRM)
# (Detailed commands in deployment script)
```

### Phase 4: Update Lambda Environment Variables
```bash
# Get AgentCore ID
AGENT_ID=$(aws bedrock-agent list-agents --query 'agentSummaries[?agentName==`centli-agent`].agentId' --output text)

# Update Message Function
aws lambda update-function-configuration \
  --function-name centli-app-message \
  --environment Variables={AGENTCORE_ID=$AGENT_ID,...}
```

### Phase 5: Verification
```bash
# Test WebSocket connection
wscat -c wss://<api-id>.execute-api.us-east-1.amazonaws.com/prod

# Send test message
{"action":"message","data":"Hola"}

# Verify logs
aws logs tail /aws/lambda/centli-app-message --follow
```

---

## 2. Resource Dependencies

### 2.1 Dependency Graph

```
┌─────────────────────────────────────────────────────────────┐
│                    Unit 1 (Foundation)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ EventBridge  │  │  S3 Bucket   │  │   IAM Role   │      │
│  │     Bus      │  │   (Assets)   │  │  (Execution) │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │                  │                  │
┌─────────┼──────────────────┼──────────────────┼─────────────┐
│         │     Unit 2 (AgentCore & Orchestration)             │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Lambda      │  │  Lambda      │  │  Lambda      │      │
│  │  (Connect)   │  │ (Disconnect) │  │  (Message)   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                            ▼                                 │
│                   ┌──────────────┐                           │
│                   │  DynamoDB    │                           │
│                   │  (Sessions)  │                           │
│                   └──────────────┘                           │
│                            │                                 │
│                            ▼                                 │
│                   ┌──────────────┐                           │
│                   │   Bedrock    │                           │
│                   │  AgentCore   │                           │
│                   └──────┬───────┘                           │
│                          │                                   │
│                          ├──> Nova Sonic (Voice)             │
│                          ├──> Nova Canvas (Images)           │
│                          └──> EventBridge (Events)           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Import/Export Dependencies

**Unit 2 Imports from Unit 1**:
- `CentliEventBusName` → Used by Message Function
- `CentliAssetsBucketName` → Used by Message Function
- `CentliLambdaExecutionRoleArn` → Used by all Lambda functions
- `CentliLogGroupName` → Used for logging

**Unit 2 Exports**:
- `CentliWebSocketURL` → Used by Unit 4 (Frontend)
- `CentliSessionsTableName` → Reference for other units
- `CentliConnectFunctionArn` → Reference
- `CentliMessageFunctionArn` → Reference

---

## 3. Integration Points

### 3.1 Frontend → Unit 2 (WebSocket)

**Connection Flow**:
```
Frontend (Browser)
  ↓ WSS connection
API Gateway WebSocket
  ↓ $connect
ConnectFunction
  ↓ Create session
DynamoDB (Sessions)
  ↓ Return connection_id
Frontend (connected)
```

**Message Flow**:
```
Frontend
  ↓ Send message (JSON)
API Gateway
  ↓ $default route
MessageFunction
  ↓ Process message
AgentCore
  ↓ Recognize intent
EventBridge
  ↓ Publish action event
[Action Groups in Unit 3]
```

### 3.2 Unit 2 → Unit 3 (EventBridge)

**Event Publishing**:
```python
# In MessageFunction
eventbridge.put_events(
    Entries=[{
        'Source': 'centli.agentcore',
        'DetailType': 'TransferRequest',
        'Detail': json.dumps({
            'action_type': 'TRANSFER',
            'action_data': {...},
            'user_id': user_id,
            'session_id': session_id,
            'request_id': request_id
        }),
        'EventBusName': 'centli-event-bus'
    }]
)
```

**Event Subscription** (in Unit 3):
```yaml
# Action Group Lambda subscribes to events
CoreBankingFunction:
  Type: AWS::Serverless::Function
  Events:
    TransferEvent:
      Type: EventBridgeRule
      Properties:
        EventBusName: !ImportValue CentliEventBusName
        Pattern:
          source: [centli.agentcore]
          detail-type: [TransferRequest, BalanceQuery, TransactionQuery]
```

### 3.3 Unit 3 → Unit 2 (EventBridge Response)

**Response Flow**:
```
Action Group (Unit 3)
  ↓ Process action
  ↓ Publish response event
EventBridge
  ↓ Route to AgentCore
AgentCore
  ↓ Generate user response
MessageFunction
  ↓ Send via WebSocket
Frontend
```

---

## 4. Event Flows

### 4.1 Voice Message Flow

```
User speaks
  ↓
Frontend captures audio
  ↓ WebSocket (base64 audio)
MessageFunction
  ↓ Extract audio
Nova Sonic (transcription)
  ↓ Text output
AgentCore (intent recognition)
  ↓ Intent + entities
EventBridge (action event)
  ↓
Action Group (Unit 3)
  ↓ Process action
EventBridge (response event)
  ↓
AgentCore (generate response)
  ↓ Response text
Nova Sonic (synthesis)
  ↓ Audio output
MessageFunction
  ↓ WebSocket (base64 audio)
Frontend plays audio
```

### 4.2 Image Message Flow

```
User uploads image
  ↓
Frontend sends image
  ↓ WebSocket (base64 image)
MessageFunction
  ↓ Upload to S3
S3 (store image)
  ↓ S3 key
Nova Canvas (analysis)
  ↓ Analysis results
AgentCore (context enrichment)
  ↓ Intent + image context
EventBridge (action event)
  ↓
[Continue as normal flow]
```

### 4.3 Multimodal Flow (Voice + Image)

```
User speaks + shows image
  ↓
Frontend sends both
  ↓ WebSocket (audio + image)
MessageFunction
  ├─> Nova Sonic (parallel)
  └─> S3 + Nova Canvas (parallel)
  ↓ Merge results
AgentCore (multimodal context)
  ↓ Intent with rich context
[Continue as normal flow]
```

---

## 5. Monitoring and Observability

### 5.1 CloudWatch Dashboards

**Key Metrics**:
- WebSocket connections (active, new, closed)
- Lambda invocations (count, errors, duration)
- DynamoDB operations (reads, writes, throttles)
- AgentCore invocations (count, latency)
- EventBridge events (published, delivered, failed)

**Dashboard Widgets**:
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/Lambda", "Invocations", {"stat": "Sum"}],
          [".", "Errors", {"stat": "Sum"}],
          [".", "Duration", {"stat": "Average"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Lambda Metrics"
      }
    }
  ]
}
```

### 5.2 Log Aggregation

**Log Groups**:
- `/aws/lambda/centli-app-connect`
- `/aws/lambda/centli-app-disconnect`
- `/aws/lambda/centli-app-message`

**Log Insights Queries**:
```sql
-- Find errors
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20

-- Track request flow
fields @timestamp, request_id, user_id, operation
| filter request_id = "<request-id>"
| sort @timestamp asc
```

---

## 6. Rollback Strategy

### 6.1 Rollback Triggers
- Lambda function errors > 10% of invocations
- WebSocket connection failures > 20%
- DynamoDB throttling detected
- AgentCore failures > 30%

### 6.2 Rollback Steps
```bash
# 1. Identify previous stack version
aws cloudformation describe-stack-events \
  --stack-name centli-agentcore-orchestration

# 2. Rollback to previous version
aws cloudformation rollback-stack \
  --stack-name centli-agentcore-orchestration

# 3. Verify rollback
aws cloudformation describe-stacks \
  --stack-name centli-agentcore-orchestration \
  --query 'Stacks[0].StackStatus'

# 4. Test functionality
wscat -c wss://<api-id>.execute-api.us-east-1.amazonaws.com/prod
```

---

## 7. Deployment Checklist

- [ ] Unit 1 deployed and verified
- [ ] SAM template validated (`sam validate`)
- [ ] Lambda code built (`sam build`)
- [ ] Stack deployed (`sam deploy`)
- [ ] Bedrock AgentCore created
- [ ] Action Groups configured
- [ ] Lambda environment variables updated
- [ ] WebSocket connection tested
- [ ] Voice processing tested
- [ ] Image processing tested
- [ ] EventBridge events verified
- [ ] CloudWatch logs verified
- [ ] Cost monitoring enabled

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Deployment Architecture**: 7 sections covering deployment sequence, dependencies, integration points, event flows, monitoring, rollback, and checklist

