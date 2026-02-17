# Integration Test Instructions - CENTLI

## Purpose

Integration tests verify that different units work together correctly. These tests validate:
- Communication between Frontend and AgentCore (WebSocket)
- Communication between AgentCore and Action Groups (EventBridge)
- Communication between Action Groups (EventBridge)
- End-to-end user workflows

---

## Test Scenarios

### Scenario 1: Frontend → AgentCore Integration (WebSocket)

**Description**: Test WebSocket connection and message flow between Frontend and Orchestration Service

**Setup**:
```bash
# Deploy Unit 2 (if not already deployed)
sam deploy --guided --profile 777937796305_Ps-HackatonAgentic-Mexico

# Get WebSocket API endpoint
aws apigatewayv2 get-apis \
  --query 'Items[?Name==`centli-websocket-api`].ApiEndpoint' \
  --output text \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**Test Steps**:

1. **Connect to WebSocket**
```bash
# Using wscat (install: npm install -g wscat)
wscat -c wss://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod

# Expected: Connection established
# Expected: Receive connection confirmation message
```

2. **Send Text Message**
```json
{
  "type": "TEXT",
  "content": "Hola, ¿cuál es mi saldo?",
  "metadata": {
    "timestamp": "2026-02-17T10:00:00Z",
    "message_id": "msg-001",
    "user_id": "user-123",
    "session_id": "session-abc"
  }
}
```

**Expected Results**:
- ✅ Message received by Orchestration Service
- ✅ Session created/updated in DynamoDB
- ✅ Message processed by AgentCore
- ✅ Response sent back via WebSocket
- ✅ Response contains relevant information

**Verification**:
```bash
# Check DynamoDB sessions table
aws dynamodb scan \
  --table-name centli-sessions \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check CloudWatch logs
aws logs tail /aws/lambda/centli-app-message \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**Cleanup**:
```bash
# Disconnect from WebSocket
# Press Ctrl+C in wscat
```

---

### Scenario 2: AgentCore → Action Groups Integration (EventBridge)

**Description**: Test event-driven communication between AgentCore and Action Groups

**Setup**:
```bash
# Ensure Unit 2 is deployed
# Ensure Unit 3 is deployed (when ready)

# Verify EventBridge bus exists
aws events describe-event-bus \
  --name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**Test Steps**:

1. **Publish Test Action Event**
```bash
# Create test event file
cat > test-action-event.json <<EOF
{
  "Source": "centli.agentcore",
  "DetailType": "ActionRequest",
  "Detail": "{\"action_type\":\"GET_BALANCE\",\"action_data\":{\"user_id\":\"user-123\"},\"user_id\":\"user-123\",\"session_id\":\"session-abc\",\"request_id\":\"req-001\",\"timestamp\":\"2026-02-17T10:00:00Z\"}",
  "EventBusName": "centli-event-bus"
}
EOF

# Publish event
aws events put-events \
  --entries file://test-action-event.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

2. **Verify Event Delivery**
```bash
# Check Core Banking Lambda logs (Unit 3)
aws logs tail /aws/lambda/centli-core-banking \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Expected: Event received and processed
```

3. **Verify Response Event**
```bash
# Check for response event in EventBridge
# (Response should be published back to event bus)

# Check AgentCore logs for response handling
aws logs tail /aws/lambda/centli-app-message \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**Expected Results**:
- ✅ Action event published to EventBridge
- ✅ Core Banking Lambda receives event
- ✅ Core Banking Lambda processes request
- ✅ Response event published back to EventBridge
- ✅ AgentCore receives response event
- ✅ Response sent to user via WebSocket

**Cleanup**:
```bash
# Remove test event file
rm test-action-event.json
```

---

### Scenario 3: Marketplace → Core Banking Integration (Cross-Action Group)

**Description**: Test communication between Action Groups (Marketplace triggers payment in Core Banking)

**Setup**:
```bash
# Ensure Unit 3 is fully deployed
# Seed test data in DynamoDB tables
```

**Test Steps**:

1. **Trigger Purchase Flow**
```bash
# Publish purchase event
cat > test-purchase-event.json <<EOF
{
  "Source": "centli.agentcore",
  "DetailType": "ActionRequest",
  "Detail": "{\"action_type\":\"PURCHASE_PRODUCT\",\"action_data\":{\"user_id\":\"user-123\",\"product_id\":\"prod-001\",\"amount\":500},\"user_id\":\"user-123\",\"session_id\":\"session-abc\",\"request_id\":\"req-002\",\"timestamp\":\"2026-02-17T10:05:00Z\"}",
  "EventBusName": "centli-event-bus"
}
EOF

aws events put-events \
  --entries file://test-purchase-event.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

2. **Verify Marketplace Processing**
```bash
# Check Marketplace Lambda logs
aws logs tail /aws/lambda/centli-marketplace \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Expected: Purchase request received
# Expected: Payment event published to EventBridge
```

3. **Verify Core Banking Payment**
```bash
# Check Core Banking Lambda logs
aws logs tail /aws/lambda/centli-core-banking \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Expected: Payment event received
# Expected: Funds deducted from account
# Expected: Transaction recorded
```

4. **Verify Purchase Completion**
```bash
# Check DynamoDB purchases table
aws dynamodb scan \
  --table-name centli-purchases \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Expected: Purchase record created with status "COMPLETED"
```

**Expected Results**:
- ✅ Purchase request received by Marketplace
- ✅ Payment event published to EventBridge
- ✅ Core Banking receives payment event
- ✅ Funds deducted from user account
- ✅ Transaction recorded in transactions table
- ✅ Purchase completed in purchases table
- ✅ Success response sent back to AgentCore

**Cleanup**:
```bash
rm test-purchase-event.json
```

---

### Scenario 4: End-to-End User Workflow (All Units)

**Description**: Complete user journey from Frontend to Action Groups and back

**Setup**:
```bash
# Ensure all units are deployed
# Open frontend in browser
open frontend/index.html
# Or deploy to S3 and access via URL
```

**Test Steps**:

1. **User Connects**
- Open frontend in browser
- Click "Connect" button
- Verify WebSocket connection established
- Verify connection status shows "Connected"

2. **User Sends Text Message**
- Type: "¿Cuál es mi saldo?"
- Click "Send" or press Enter
- Verify message appears in chat
- Verify loading indicator shows

3. **AgentCore Processes**
- Verify AgentCore receives message
- Verify intent recognized as "GET_BALANCE"
- Verify action event published to EventBridge

4. **Action Group Responds**
- Verify Core Banking Lambda receives event
- Verify balance retrieved from DynamoDB
- Verify response event published

5. **User Receives Response**
- Verify response appears in chat
- Verify response contains balance information
- Verify loading indicator disappears

**Expected Results**:
- ✅ User connects successfully
- ✅ Message sent and received
- ✅ AgentCore processes message
- ✅ Action Group executes action
- ✅ Response received by user
- ✅ UI updates correctly
- ✅ Total round-trip time < 3 seconds

**Verification**:
```bash
# Check all Lambda logs
aws logs tail /aws/lambda/centli-app-message --follow &
aws logs tail /aws/lambda/centli-core-banking --follow &

# Monitor EventBridge events
aws events list-rules \
  --event-bus-name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

## Setup Integration Test Environment

### 1. Deploy All Units
```bash
# Deploy Unit 1 (Infrastructure)
sam deploy --template infrastructure/base-template.yaml \
  --stack-name centli-infrastructure \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Deploy Unit 2 (AgentCore)
sam deploy --guided \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Deploy Unit 3 (Action Groups) - when ready
sam deploy --template infrastructure/action-groups-template.yaml \
  --stack-name centli-action-groups \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Deploy Unit 4 (Frontend) - when ready
aws s3 sync frontend/ s3://centli-assets-777937796305/ \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### 2. Seed Test Data
```bash
# Seed users
aws dynamodb put-item \
  --table-name centli-user-profiles \
  --item file://data/users_mx.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Seed transactions
aws dynamodb batch-write-item \
  --request-items file://data/transactions_mx.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Seed products
aws dynamodb batch-write-item \
  --request-items file://data/stores_mx.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### 3. Configure Service Endpoints
```bash
# Get WebSocket API endpoint
export WEBSOCKET_URL=$(aws apigatewayv2 get-apis \
  --query 'Items[?Name==`centli-websocket-api`].ApiEndpoint' \
  --output text \
  --profile 777937796305_Ps-HackatonAgentic-Mexico)

echo "WebSocket URL: $WEBSOCKET_URL"

# Get EventBridge bus ARN
export EVENTBRIDGE_BUS_ARN=$(aws events describe-event-bus \
  --name centli-event-bus \
  --query 'Arn' \
  --output text \
  --profile 777937796305_Ps-HackatonAgentic-Mexico)

echo "EventBridge Bus ARN: $EVENTBRIDGE_BUS_ARN"
```

---

## Run Integration Tests

### Automated Integration Test Suite
```bash
# Run integration tests (when test suite is ready)
poetry run pytest tests/integration/ -v

# Or run specific scenario
poetry run pytest tests/integration/test_websocket_integration.py -v
poetry run pytest tests/integration/test_eventbridge_integration.py -v
poetry run pytest tests/integration/test_cross_action_group.py -v
poetry run pytest tests/integration/test_e2e_workflow.py -v
```

### Manual Integration Testing
```bash
# Use provided test scripts
./tests/integration/manual/test-websocket.sh
./tests/integration/manual/test-eventbridge.sh
./tests/integration/manual/test-purchase-flow.sh
```

---

## Verify Service Interactions

### Check WebSocket Connections
```bash
# List active connections
aws apigatewayv2 get-connections \
  --api-id YOUR_API_ID \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Check EventBridge Events
```bash
# Describe event bus
aws events describe-event-bus \
  --name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# List rules
aws events list-rules \
  --event-bus-name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Check DynamoDB Data
```bash
# Check sessions
aws dynamodb scan --table-name centli-sessions \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check transactions
aws dynamodb scan --table-name centli-transactions \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check purchases
aws dynamodb scan --table-name centli-purchases \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Check Lambda Logs
```bash
# Tail all Lambda logs
aws logs tail /aws/lambda/centli-app-connect --follow &
aws logs tail /aws/lambda/centli-app-disconnect --follow &
aws logs tail /aws/lambda/centli-app-message --follow &
aws logs tail /aws/lambda/centli-core-banking --follow &
aws logs tail /aws/lambda/centli-marketplace --follow &
aws logs tail /aws/lambda/centli-crm --follow &
```

---

## Cleanup

### After Integration Tests
```bash
# Clear test data from DynamoDB
aws dynamodb delete-item \
  --table-name centli-sessions \
  --key '{"session_id": {"S": "session-abc"}}' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Stop log tailing
# Press Ctrl+C for each tail command

# Close WebSocket connections
# Disconnect from wscat
```

---

## Integration Test Checklist

- [ ] All units deployed successfully
- [ ] Test data seeded in DynamoDB
- [ ] WebSocket connection working
- [ ] EventBridge events flowing
- [ ] AgentCore → Action Groups integration working
- [ ] Action Groups → Action Groups integration working
- [ ] End-to-end workflow completing successfully
- [ ] Response times acceptable (< 3 seconds)
- [ ] No errors in CloudWatch logs

---

## Troubleshooting Integration Issues

### WebSocket Connection Fails
```bash
# Check API Gateway deployment
aws apigatewayv2 get-deployments \
  --api-id YOUR_API_ID \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check Lambda permissions
aws lambda get-policy \
  --function-name centli-app-connect \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### EventBridge Events Not Delivered
```bash
# Check EventBridge rules
aws events list-targets-by-rule \
  --rule YOUR_RULE_NAME \
  --event-bus-name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check Lambda permissions for EventBridge
aws lambda get-policy \
  --function-name centli-core-banking \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### DynamoDB Access Issues
```bash
# Check Lambda IAM role
aws iam get-role \
  --role-name centli-lambda-execution-role \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check DynamoDB table status
aws dynamodb describe-table \
  --table-name centli-sessions \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

## Next Steps

After all integration tests pass:
1. ✅ Proceed to **Performance Testing** (if applicable)
2. ✅ Prepare demo scenarios
3. ✅ Document any integration issues found
4. ✅ Update integration contracts if needed

---

**Integration Test Time**: ~10-15 minutes (manual), ~5 minutes (automated)  
**Test Scenarios**: 4 scenarios (WebSocket, EventBridge, Cross-AG, E2E)  
**Test Status**: Ready for execution when all units are deployed
