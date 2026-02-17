# Integration Test Instructions - CENTLI Project

## Overview
Integration testing validates that all units work together correctly. Tests the complete end-to-end flow from frontend to backend to AI agent.

---

## Integration Test Scenarios

### Scenario 1: Complete Chat Flow (Text)

**Objective**: Verify text message flows from frontend through WebSocket to Bedrock agent and back

**Prerequisites**:
- Unit 2 deployed and running
- Unit 4 deployed to S3
- Bedrock agent configured

**Steps**:
1. Open frontend: `http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com`
2. Login with user ID: "integration-test-user"
3. Wait for "Conectado" status
4. Send message: "Hola, ¿cómo estás?"
5. Observe typing indicator
6. Wait for agent response

**Expected Results**:
- ✅ WebSocket connects successfully
- ✅ Message sent (appears in chat, right side)
- ✅ Typing indicator shows
- ✅ Agent response received (appears in chat, left side)
- ✅ Response is contextual and relevant
- ✅ No errors in browser console
- ✅ Lambda logs show successful invocation

**Validation**:
```bash
# Check Lambda logs
aws logs tail /aws/lambda/centli-app-message \
  --since 5m \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check DynamoDB session
aws dynamodb get-item \
  --table-name centli-sessions \
  --key '{"connection_id":{"S":"[CONNECTION_ID]"}}' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

### Scenario 2: Voice Input Flow (if supported)

**Objective**: Verify voice recording, transcription, and response

**Prerequisites**:
- Scenario 1 passed
- Browser supports MediaRecorder API
- Microphone permission granted

**Steps**:
1. Click and hold voice button
2. Speak clearly: "¿Cuál es mi saldo?"
3. Release voice button
4. Wait for response

**Expected Results**:
- ✅ Recording starts (indicator shows)
- ✅ Audio captured (WebM format)
- ✅ Voice message sent via WebSocket
- ✅ Backend receives audio (base64 encoded)
- ✅ Bedrock transcribes audio (Nova Sonic)
- ✅ Agent processes transcription
- ✅ Text response received
- ✅ Optional: Voice response received and plays

**Note**: Full voice flow depends on Unit 2 implementing Nova Sonic integration

---

### Scenario 3: Image Upload Flow (if backend ready)

**Objective**: Verify image upload, compression, and analysis

**Prerequisites**:
- Scenario 1 passed
- Backend implements presigned URL generation
- Bedrock Nova Canvas configured

**Steps**:
1. Click "Imagen" button
2. Select test image (JPEG, < 5MB)
3. Observe preview
4. Wait for upload
5. Wait for analysis response

**Expected Results**:
- ✅ Image preview shows
- ✅ Client-side compression works (Canvas API)
- ✅ Presigned URL requested via WebSocket
- ✅ Presigned URL received
- ✅ Direct S3 upload succeeds (PUT request)
- ✅ Image URL sent to backend
- ✅ Bedrock analyzes image (Nova Canvas)
- ✅ Analysis response received
- ✅ Image stored in S3: `uploads/{session_id}/{timestamp}_{filename}`

**Validation**:
```bash
# Check S3 uploads folder
aws s3 ls s3://centli-frontend-bucket/uploads/ \
  --recursive \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

### Scenario 4: Transaction Flow (Unit 3 integration)

**Objective**: Verify transaction request, confirmation, and execution

**Prerequisites**:
- Scenario 1 passed
- Unit 3 deployed (Action Groups)
- Core Banking mock ready

**Steps**:
1. Send message: "Transferir $100 a Juan Pérez"
2. Wait for transaction confirmation modal
3. Review transaction details
4. Click "Confirmar"
5. Wait for confirmation response

**Expected Results**:
- ✅ Agent understands transfer intent
- ✅ Transaction confirmation event sent via WebSocket
- ✅ Modal displays: Type, Amount, Destination
- ✅ User confirms transaction
- ✅ Confirmation sent to backend
- ✅ Backend invokes Core Banking Lambda (Unit 3)
- ✅ EventBridge event published
- ✅ Transaction recorded in DynamoDB
- ✅ Success response received
- ✅ Agent confirms: "Transferencia completada"

**Validation**:
```bash
# Check transactions table
aws dynamodb scan \
  --table-name centli-transactions \
  --filter-expression "user_id = :uid" \
  --expression-attribute-values '{":uid":{"S":"integration-test-user"}}' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

### Scenario 5: Product Catalog Flow (Unit 3 integration)

**Objective**: Verify product listing, selection, and purchase

**Prerequisites**:
- Scenario 1 passed
- Unit 3 deployed (Action Groups)
- Marketplace mock ready

**Steps**:
1. Send message: "Muéstrame productos disponibles"
2. Wait for products to appear in sidebar
3. Click "Ver Detalles" on a product
4. Send message: "Quiero comprar este producto"
5. Confirm purchase

**Expected Results**:
- ✅ Agent understands product request
- ✅ Backend invokes Marketplace Lambda (Unit 3)
- ✅ Product catalog event sent via WebSocket
- ✅ Products display in sidebar (grid layout)
- ✅ Product selection works
- ✅ Purchase flow initiated
- ✅ Purchase recorded in DynamoDB
- ✅ Benefits calculated and displayed
- ✅ Agent confirms purchase

**Validation**:
```bash
# Check products table
aws dynamodb scan \
  --table-name centli-products \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check purchases table
aws dynamodb scan \
  --table-name centli-purchases \
  --filter-expression "user_id = :uid" \
  --expression-attribute-values '{":uid":{"S":"integration-test-user"}}' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

### Scenario 6: Beneficiary Management Flow (Unit 3 integration)

**Objective**: Verify beneficiary search, add, and transfer

**Prerequisites**:
- Scenario 1 passed
- Unit 3 deployed (Action Groups)
- CRM mock ready

**Steps**:
1. Send message: "Buscar beneficiario Juan"
2. Wait for beneficiary list
3. Send message: "Agregar beneficiario María López, cuenta 1234567890"
4. Confirm beneficiary added
5. Send message: "Transferir $50 a María López"
6. Confirm transfer

**Expected Results**:
- ✅ Agent understands beneficiary search
- ✅ Backend invokes CRM Lambda (Unit 3)
- ✅ Beneficiary list returned
- ✅ Add beneficiary works
- ✅ Beneficiary stored in DynamoDB
- ✅ Transfer to beneficiary works
- ✅ Frequent beneficiary counter incremented

**Validation**:
```bash
# Check beneficiaries table
aws dynamodb scan \
  --table-name centli-beneficiaries \
  --filter-expression "user_id = :uid" \
  --expression-attribute-values '{":uid":{"S":"integration-test-user"}}' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

### Scenario 7: Error Handling and Recovery

**Objective**: Verify system handles errors gracefully

**Test Cases**:

#### 7.1: Network Disconnection
1. Establish connection
2. Disable network
3. Try to send message
4. Observe error handling
5. Re-enable network
6. Observe auto-reconnect

**Expected**: Error toast, auto-reconnect (5 attempts), queued messages sent

#### 7.2: Backend Error
1. Send invalid message format
2. Observe error handling

**Expected**: Error response from backend, user-friendly error message

#### 7.3: Large File Upload
1. Try to upload image > 5MB
2. Observe validation

**Expected**: Client-side validation, error message before upload

#### 7.4: Session Timeout
1. Leave page idle for extended period
2. Try to send message
3. Observe session handling

**Expected**: Session refresh or re-authentication prompt

---

## Integration Test Matrix

| Scenario | Unit 1 | Unit 2 | Unit 3 | Unit 4 | Status |
|----------|--------|--------|--------|--------|--------|
| Chat Flow | ✅ | ✅ | - | ✅ | Ready |
| Voice Input | ✅ | ⏳ | - | ✅ | Partial |
| Image Upload | ✅ | ⏳ | - | ✅ | Partial |
| Transaction | ✅ | ✅ | ⏳ | ✅ | Waiting Unit 3 |
| Product Catalog | ✅ | ✅ | ⏳ | ✅ | Waiting Unit 3 |
| Beneficiary | ✅ | ✅ | ⏳ | ✅ | Waiting Unit 3 |
| Error Handling | ✅ | ✅ | - | ✅ | Ready |

**Legend**:
- ✅ Ready
- ⏳ Partial/In Progress
- - Not Required

---

## End-to-End Test Flow

### Complete User Journey

**Scenario**: User checks balance, views products, makes purchase

**Steps**:
1. **Login**: User opens frontend, logs in
2. **Greeting**: Agent greets user
3. **Balance Check**: "¿Cuál es mi saldo?"
4. **Product Browse**: "Muéstrame productos"
5. **Product Selection**: Click product in catalog
6. **Purchase**: "Quiero comprar este producto"
7. **Confirmation**: Confirm purchase in modal
8. **Receipt**: Agent shows purchase confirmation
9. **Balance Update**: "¿Cuál es mi saldo ahora?"
10. **Logout**: User logs out

**Expected Duration**: 2-3 minutes

**Success Criteria**:
- ✅ All steps complete without errors
- ✅ Data persists correctly in DynamoDB
- ✅ UI responsive and smooth
- ✅ Agent responses contextual and helpful
- ✅ No console errors
- ✅ No Lambda errors

---

## Performance Testing

### Load Test (Optional)

**Objective**: Verify system handles multiple concurrent users

**Tool**: Artillery, k6, or manual (multiple browser tabs)

**Test**:
```bash
# Simple load test with Artillery
artillery quick --count 10 --num 5 wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
```

**Expected**:
- WebSocket connections: < 500ms
- Message latency: < 1 second
- No connection drops
- Lambda cold starts: < 3 seconds
- Lambda warm: < 500ms

---

## Integration Test Checklist

### Pre-Test
- [ ] All units deployed
- [ ] AWS resources verified
- [ ] Frontend accessible
- [ ] Backend WebSocket URL correct in config.js
- [ ] Test data prepared

### Execution
- [ ] Scenario 1: Chat Flow ✅
- [ ] Scenario 2: Voice Input (if ready)
- [ ] Scenario 3: Image Upload (if ready)
- [ ] Scenario 4: Transaction (if Unit 3 ready)
- [ ] Scenario 5: Product Catalog (if Unit 3 ready)
- [ ] Scenario 6: Beneficiary (if Unit 3 ready)
- [ ] Scenario 7: Error Handling ✅

### Post-Test
- [ ] All scenarios passed
- [ ] No critical errors
- [ ] Performance acceptable
- [ ] Data integrity verified
- [ ] Logs reviewed
- [ ] Issues documented

---

## Test Reporting

### Integration Test Report Template

```markdown
# Integration Test Report - CENTLI

**Date**: 2026-02-17  
**Tester**: [Name]  
**Environment**: Production (S3 + AWS)  
**Duration**: [X] minutes

## Test Summary
- Total Scenarios: 7
- Passed: X
- Failed: X
- Skipped: X

## Scenario Results

### Scenario 1: Chat Flow
- Status: ✅ Passed
- Duration: 30 seconds
- Notes: All messages delivered successfully

### Scenario 2: Voice Input
- Status: ⏭️ Skipped
- Reason: Backend voice processing not implemented

[... continue for all scenarios ...]

## Issues Found
1. [Issue description]
   - Severity: High/Medium/Low
   - Unit: [Unit number]
   - Steps to reproduce: [...]

## Performance Observations
- WebSocket latency: [X]ms
- Agent response time: [X]s
- Page load time: [X]s

## Recommendations
1. [Recommendation]
2. [Recommendation]

## Conclusion
[Overall assessment]
```

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17T16:35:00Z
