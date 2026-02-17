# Unit Test Instructions - CENTLI Project

## Overview
Unit testing instructions for each unit. Given the hackathon context (8 hours, demo quality), testing approach is pragmatic with focus on manual testing.

---

## Unit 1: Infrastructure Foundation

### Test Type
Infrastructure validation (no code to unit test)

### Test Steps
```bash
# Verify EventBridge bus exists
aws events describe-event-bus \
  --name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Verify S3 bucket exists
aws s3 ls s3://centli-frontend-bucket/ \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Verify IAM role exists
aws iam get-role \
  --role-name CentliBedrockAgentRole \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Expected Results
- ✅ EventBridge bus: centli-event-bus exists
- ✅ S3 bucket: centli-frontend-bucket exists
- ✅ IAM role: CentliBedrockAgentRole exists
- ✅ CloudWatch log group: /aws/centli exists

---

## Unit 2: AgentCore & Orchestration

### Test Type
Manual testing (no automated unit tests for hackathon)

### Test Steps

#### 1. Test WebSocket Connection
```bash
# Install wscat if not already installed
npm install -g wscat

# Connect to WebSocket
wscat -c wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod

# Send test message
{"action": "message", "content": "Hello", "user_id": "test-user", "session_id": "test-session"}
```

**Expected Result**: Connection established, receive response from agent

#### 2. Test Lambda Functions
```bash
# Check Lambda function exists
aws lambda get-function \
  --function-name centli-app-message \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# View recent logs
aws logs tail /aws/lambda/centli-app-message \
  --since 10m \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**Expected Result**: Lambda functions exist and have recent invocations

#### 3. Test DynamoDB Session Storage
```bash
# Check table exists
aws dynamodb describe-table \
  --table-name centli-sessions \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Scan table (check for test sessions)
aws dynamodb scan \
  --table-name centli-sessions \
  --limit 5 \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**Expected Result**: Table exists, sessions are created on WebSocket connect

#### 4. Test Bedrock Agent
```bash
# Test Bedrock agent invocation
python test-bedrock-direct.py
```

**Expected Result**: Agent responds with text output

### Manual Test Checklist
- [ ] WebSocket connects successfully
- [ ] Can send text message
- [ ] Receive response from Bedrock agent
- [ ] Session created in DynamoDB
- [ ] Lambda logs show successful invocation
- [ ] No errors in CloudWatch logs

---

## Unit 3: Action Groups

### Test Type
Manual testing (when code is complete)

### Test Steps (Future)

#### 1. Test Core Banking Lambda
```bash
# Invoke Lambda directly
aws lambda invoke \
  --function-name centli-core-banking \
  --payload '{"action":"get_balance","user_id":"test-user"}' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  response.json

cat response.json
```

**Expected Result**: Returns account balance

#### 2. Test Marketplace Lambda
```bash
# Invoke Lambda directly
aws lambda invoke \
  --function-name centli-marketplace \
  --payload '{"action":"list_products"}' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  response.json

cat response.json
```

**Expected Result**: Returns product list

#### 3. Test CRM Lambda
```bash
# Invoke Lambda directly
aws lambda invoke \
  --function-name centli-crm \
  --payload '{"action":"search_beneficiary","query":"Juan"}' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  response.json

cat response.json
```

**Expected Result**: Returns beneficiary list

### Manual Test Checklist (Future)
- [ ] Core Banking: Get balance works
- [ ] Core Banking: Transfer works
- [ ] Marketplace: List products works
- [ ] Marketplace: Purchase works
- [ ] CRM: Search beneficiary works
- [ ] CRM: Add beneficiary works
- [ ] EventBridge events published correctly
- [ ] DynamoDB tables populated correctly

---

## Unit 4: Frontend Multimodal UI

### Test Type
Manual browser testing (no automated tests for hackathon)

### Test Environment
- **Browser**: Chrome (latest version) - PRIMARY
- **Fallback**: Firefox, Safari, Edge
- **Mobile**: iOS Safari, Chrome Mobile

### Test Steps

#### 1. Page Load Test
```bash
# Open frontend in browser
open http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com

# Or use local server for testing
cd frontend
python3 -m http.server 8000
open http://localhost:8000
```

**Expected Result**: Page loads, no console errors, Bootstrap styles applied

#### 2. Login Test
- [ ] Enter user ID: "test-user"
- [ ] Click "Iniciar Sesión"
- [ ] Login screen hides
- [ ] Main app shows
- [ ] Connection status shows "Conectando..." then "Conectado"

**Expected Result**: Successful login, WebSocket connected

#### 3. Chat Test
- [ ] Type message: "Hola"
- [ ] Click send button (or press Enter)
- [ ] Message appears in chat (user side, right-aligned, blue)
- [ ] Typing indicator shows
- [ ] Agent response appears (agent side, left-aligned, white)
- [ ] Auto-scroll to latest message

**Expected Result**: Bidirectional chat working

#### 4. Voice Input Test (if browser supports)
- [ ] Click and hold voice button
- [ ] Microphone permission requested (first time)
- [ ] Recording indicator shows
- [ ] Speak: "¿Cuál es mi saldo?"
- [ ] Release voice button
- [ ] Voice message appears in chat
- [ ] Typing indicator shows
- [ ] Agent response appears

**Expected Result**: Voice recording and sending works

**Note**: If MediaRecorder not supported, voice button should be disabled

#### 5. Voice Output Test
- [ ] Send message that triggers voice response
- [ ] Audio plays automatically
- [ ] Can hear agent voice

**Expected Result**: Audio playback works

**Note**: Depends on backend implementing voice response

#### 6. Image Upload Test
- [ ] Click "Imagen" button
- [ ] Select JPEG or PNG image (< 5MB)
- [ ] Image preview shows
- [ ] Upload progress shows
- [ ] Image uploaded message appears in chat
- [ ] Agent response with image analysis

**Expected Result**: Image upload and processing works

**Note**: Depends on backend implementing presigned URLs

#### 7. Transaction Confirmation Test
- [ ] Send message: "Transferir $100 a Juan"
- [ ] Transaction modal appears
- [ ] Shows: Type, Amount, Destination
- [ ] Click "Confirmar"
- [ ] Modal closes
- [ ] Success toast shows
- [ ] Agent confirms transaction

**Expected Result**: Transaction confirmation flow works

**Note**: Depends on backend sending transaction confirmation event

#### 8. Product Catalog Test
- [ ] Send message: "Muéstrame productos"
- [ ] Products appear in sidebar
- [ ] Shows: Name, Price, Benefits
- [ ] Click "Ver Detalles" on a product
- [ ] Product selected toast shows
- [ ] Agent responds with product details

**Expected Result**: Product catalog display works

**Note**: Depends on backend sending product catalog event

#### 9. Error Handling Test
- [ ] Disconnect internet
- [ ] Try to send message
- [ ] Error toast shows: "No conectado al servidor"
- [ ] Reconnect internet
- [ ] Auto-reconnect happens (5 attempts)
- [ ] Connection status shows "Reconectando..."
- [ ] Eventually reconnects
- [ ] Queued messages sent

**Expected Result**: Error handling and auto-reconnect works

#### 10. Logout Test
- [ ] Click "Salir" button
- [ ] WebSocket disconnects
- [ ] Login screen shows
- [ ] localStorage cleared

**Expected Result**: Logout works

### Browser Console Checks
- [ ] No JavaScript errors
- [ ] Structured logs visible: [WebSocket], [Voice], [Chat], [Image]
- [ ] WebSocket messages logged
- [ ] State changes logged

### Mobile Testing
- [ ] Open on mobile device
- [ ] Responsive layout (mobile-first)
- [ ] Touch interactions work
- [ ] Voice button works (push-to-talk)
- [ ] Image upload works (camera option)
- [ ] Scrolling smooth

### Manual Test Checklist
- [ ] Page loads successfully
- [ ] Login works
- [ ] WebSocket connects
- [ ] Chat messaging works
- [ ] Voice input works (if supported)
- [ ] Voice output works (if backend ready)
- [ ] Image upload works (if backend ready)
- [ ] Transaction confirmation works (if backend ready)
- [ ] Product catalog works (if backend ready)
- [ ] Error handling works
- [ ] Auto-reconnect works
- [ ] Logout works
- [ ] Mobile responsive
- [ ] No console errors

---

## Test Summary

| Unit | Test Type | Status | Coverage |
|------|-----------|--------|----------|
| Unit 1 | Infrastructure | ✅ Passed | 100% |
| Unit 2 | Manual | ✅ Passed | WebSocket, Lambda, DynamoDB, Bedrock |
| Unit 3 | Manual | ⏳ Pending | Awaiting code completion |
| Unit 4 | Manual | 🧪 Ready | All features testable |

---

## Test Execution Order

1. ✅ Unit 1: Infrastructure validation (complete)
2. ✅ Unit 2: WebSocket and Bedrock testing (complete)
3. 🚀 Unit 4: Frontend testing (ready to execute)
4. ⏳ Unit 3: Action Groups testing (when code complete)
5. 🧪 Integration testing (all units together)

---

## Test Reporting

### Test Results Format
```markdown
## Test Execution Report

**Date**: YYYY-MM-DD  
**Tester**: [Name]  
**Environment**: [Local/S3]  
**Browser**: [Chrome/Firefox/Safari]

### Results
- ✅ Test passed
- ❌ Test failed
- ⚠️ Test partially passed
- ⏭️ Test skipped

### Issues Found
1. [Description]
2. [Description]

### Notes
[Additional observations]
```

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17T16:35:00Z
