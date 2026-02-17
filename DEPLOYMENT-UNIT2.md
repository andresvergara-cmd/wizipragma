# Unit 2 Deployment Guide - AgentCore & Orchestration

## Quick Start

### 1. Deploy Infrastructure
```bash
./commands/deploy-unit2.sh
```

This will:
- Build Lambda functions with SAM
- Deploy CloudFormation stack
- Display WebSocket URL and outputs

### 2. Configure Bedrock AgentCore
```bash
./scripts/configure-bedrock.sh
```

Follow the manual steps to:
- Create Bedrock Agent via AWS Console
- Enable Managed Memory
- Create Agent Alias
- Note Agent ID

### 3. Update Lambda Environment
```bash
# Replace <AGENT_ID> with your actual Agent ID
aws lambda update-function-configuration \
    --profile 777937796305_Ps-HackatonAgentic-Mexico \
    --region us-east-1 \
    --function-name centli-app-message \
    --environment Variables='{
        "AGENTCORE_ID":"<AGENT_ID>",
        "SESSIONS_TABLE":"centli-sessions",
        "EVENT_BUS_NAME":"centli-event-bus",
        "ASSETS_BUCKET":"centli-assets-777937796305",
        "LOG_LEVEL":"INFO",
        "AWS_ACCOUNT_ID":"777937796305"
    }'
```

### 4. Test WebSocket Connection
```bash
# Install wscat
npm install -g wscat

# Get WebSocket URL
WEBSOCKET_URL=$(aws cloudformation describe-stacks \
    --profile 777937796305_Ps-HackatonAgentic-Mexico \
    --region us-east-1 \
    --stack-name centli-hackathon \
    --query "Stacks[0].Outputs[?OutputKey=='WebSocketURL'].OutputValue" \
    --output text)

# Connect
wscat -c "$WEBSOCKET_URL?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdC11c2VyIiwiZXhwIjoxNzQwMDAwMDAwfQ.test"

# Send test message
{"type":"TEXT","content":"Hola, ¿cuál es mi saldo?"}
```

## What Was Deployed

### Lambda Functions
- **centli-app-connect**: WebSocket connection handler with JWT validation
- **centli-app-disconnect**: WebSocket disconnection handler
- **centli-app-message**: Message processing and AgentCore integration

### Infrastructure
- **WebSocket API**: Real-time communication endpoint
- **DynamoDB Table**: Session storage (centli-sessions)
- **IAM Permissions**: Lambda execution role with Bedrock access
- **CloudWatch Logs**: Centralized logging

### Outputs
- WebSocketURL: WebSocket endpoint for frontend
- SessionsTableName: DynamoDB table name
- Function ARNs: Lambda function identifiers

## Architecture

```
Frontend (Unit 4)
    ↓ WebSocket
WebSocket API Gateway
    ↓
Lambda Functions (Unit 2)
    ├─ Connect → DynamoDB Sessions
    ├─ Disconnect → DynamoDB Sessions
    └─ Message → Bedrock AgentCore → EventBridge (Unit 3)
```

## Next Steps

After Unit 2 deployment:
1. **Unit 3**: Deploy Action Groups (Core Banking, Marketplace, CRM)
2. **Unit 4**: Deploy Frontend Multimodal UI
3. **Integration Testing**: Test end-to-end flow
4. **Demo Preparation**: Prepare demo scenarios

## Troubleshooting

### WebSocket Connection Fails
- Check JWT token format and expiration
- Verify WebSocket URL is correct
- Check Lambda logs in CloudWatch

### Message Processing Fails
- Verify AGENTCORE_ID is set correctly
- Check Bedrock Agent is created and active
- Review Lambda logs for errors

### DynamoDB Errors
- Verify sessions table exists
- Check IAM permissions for Lambda role
- Review table capacity settings

## Resources

- **Code Summary**: `aidlc-docs/construction/agentcore-orchestration/code/code-summary.md`
- **Infrastructure Design**: `aidlc-docs/construction/agentcore-orchestration/infrastructure-design/`
- **Deployment Architecture**: `aidlc-docs/construction/agentcore-orchestration/infrastructure-design/deployment-architecture.md`

---

**Status**: Ready for deployment  
**Estimated Time**: 10-15 minutes (excluding Bedrock manual setup)  
**AWS Profile**: 777937796305_Ps-HackatonAgentic-Mexico  
**Region**: us-east-1
