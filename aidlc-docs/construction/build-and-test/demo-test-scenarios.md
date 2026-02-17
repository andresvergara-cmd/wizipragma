# Demo Test Scenarios - CENTLI

## Overview

This document provides detailed test scenarios for demo preparation and integration testing. Each scenario represents a complete user workflow that demonstrates CENTLI's capabilities.

---

## Demo Environment Setup

### Prerequisites
```bash
# Set AWS profile
export AWS_PROFILE=777937796305_Ps-HackatonAgentic-Mexico

# Get WebSocket URL
export WEBSOCKET_URL=$(aws apigatewayv2 get-apis \
  --query 'Items[?Name==`centli-websocket-api`].ApiEndpoint' \
  --output text)

echo "WebSocket URL: $WEBSOCKET_URL"

# Seed demo data
aws dynamodb batch-write-item \
  --request-items file://data/users_mx.json

aws dynamodb batch-write-item \
  --request-items file://data/transactions_mx.json

aws dynamodb batch-write-item \
  --request-items file://data/stores_mx.json
```

### Demo User Profiles
```json
{
  "user-001": {
    "name": "María González",
    "account_balance": 15000.00,
    "account_number": "1234567890",
    "recent_transactions": 5,
    "beneficiaries": 3
  },
  "user-002": {
    "name": "Carlos Rodríguez",
    "account_balance": 8500.00,
    "account_number": "0987654321",
    "recent_transactions": 8,
    "beneficiaries": 2
  }
}
```

---

## Scenario 1: Balance Inquiry (Basic Flow)

### Objective
Demonstrate basic conversational interaction and balance retrieval

### User Story
As a user, I want to check my account balance using natural language

### Prerequisites
- User authenticated (user-001: María González)
- Account has balance: $15,000.00 MXN

### Test Steps

1. **User Connects**
   - Open frontend: `open frontend/index.html`
   - Click "Conectar" button
   - **Expected**: Connection status shows "Conectado"

2. **User Sends Message (Text)**
   ```
   User: "Hola, ¿cuál es mi saldo?"
   ```
   - **Expected**: Message appears in chat
   - **Expected**: Loading indicator shows

3. **AgentCore Processes**
   - **Expected**: Intent recognized as "GET_BALANCE"
   - **Expected**: Action event published to EventBridge
   - **Expected**: Core Banking Lambda receives event

4. **Core Banking Responds**
   - **Expected**: Balance retrieved: $15,000.00 MXN
   - **Expected**: Response event published to EventBridge
   - **Expected**: AgentCore receives response

5. **User Receives Response**
   ```
   Agent: "Hola María, tu saldo actual es de $15,000.00 MXN."
   ```
   - **Expected**: Response appears in chat
   - **Expected**: Loading indicator disappears
   - **Expected**: Response time < 3 seconds

### Success Criteria
- ✅ User receives accurate balance
- ✅ Response is conversational and natural
- ✅ Response time < 3 seconds
- ✅ No errors in logs

### Verification
```bash
# Check CloudWatch logs
aws logs tail /aws/lambda/centli-app-message --since 1m
aws logs tail /aws/lambda/centli-core-banking --since 1m

# Check DynamoDB session
aws dynamodb get-item \
  --table-name centli-sessions \
  --key '{"session_id": {"S": "SESSION_ID"}}'
```

---

## Scenario 2: P2P Transfer (Complex Flow)

### Objective
Demonstrate multi-step workflow with confirmation and execution

### User Story
As a user, I want to transfer money to a beneficiary using their alias

### Prerequisites
- User authenticated (user-001: María González)
- Account balance: $15,000.00 MXN
- Beneficiary exists: "Mamá" → account 0987654321

### Test Steps

1. **User Initiates Transfer**
   ```
   User: "Quiero enviar $500 a Mamá"
   ```
   - **Expected**: Intent recognized as "TRANSFER"
   - **Expected**: Alias "Mamá" needs resolution

2. **CRM Resolves Alias**
   - **Expected**: CRM Lambda receives alias resolution request
   - **Expected**: Alias "Mamá" resolved to account 0987654321
   - **Expected**: Beneficiary name: "Rosa González"

3. **Agent Requests Confirmation**
   ```
   Agent: "¿Confirmas la transferencia de $500.00 MXN a Rosa González (cuenta 0987654321)?"
   ```
   - **Expected**: Confirmation dialog appears in UI
   - **Expected**: Shows transfer details

4. **User Confirms**
   ```
   User: "Sí, confirmo"
   ```
   - **Expected**: Confirmation sent to AgentCore

5. **Core Banking Executes Transfer**
   - **Expected**: Funds validation (balance ≥ $500)
   - **Expected**: Debit from user-001: $15,000 → $14,500
   - **Expected**: Credit to beneficiary: $8,500 → $9,000
   - **Expected**: Transaction recorded in both accounts

6. **User Receives Confirmation**
   ```
   Agent: "Transferencia exitosa. Enviaste $500.00 MXN a Rosa González. Tu nuevo saldo es $14,500.00 MXN."
   ```
   - **Expected**: Success message with receipt
   - **Expected**: Transaction ID displayed
   - **Expected**: Updated balance shown

### Success Criteria
- ✅ Alias resolved correctly
- ✅ Confirmation dialog shown
- ✅ Transfer executed successfully
- ✅ Balances updated correctly
- ✅ Transaction recorded
- ✅ Receipt provided

### Verification
```bash
# Check transactions table
aws dynamodb query \
  --table-name centli-transactions \
  --key-condition-expression "user_id = :uid" \
  --expression-attribute-values '{":uid":{"S":"user-001"}}' \
  --scan-index-forward false \
  --limit 1

# Check beneficiary account balance
aws dynamodb get-item \
  --table-name centli-accounts \
  --key '{"user_id": {"S": "user-002"}}'
```

---

## Scenario 3: Product Purchase with Benefits (Marketplace Flow)

### Objective
Demonstrate marketplace integration, benefits calculation, and payment processing

### User Story
As a user, I want to purchase a product and see my benefits applied

### Prerequisites
- User authenticated (user-001: María González)
- Account balance: $14,500.00 MXN
- Product available: "iPhone 15 Pro" - $25,000.00 MXN
- User has benefits: 10% cashback on electronics

### Test Steps

1. **User Browses Products**
   ```
   User: "Muéstrame productos de electrónica"
   ```
   - **Expected**: Product catalog displayed
   - **Expected**: Shows 5-10 products with images
   - **Expected**: Benefits badge shown on eligible products

2. **User Selects Product**
   ```
   User: "Quiero comprar el iPhone 15 Pro"
   ```
   - **Expected**: Product details shown
   - **Expected**: Price: $25,000.00 MXN
   - **Expected**: Benefits calculated: 10% cashback = $2,500.00 MXN

3. **Agent Shows Benefits**
   ```
   Agent: "El iPhone 15 Pro cuesta $25,000.00 MXN. Con tu beneficio de 10% cashback, recibirás $2,500.00 MXN de regreso. ¿Deseas continuar?"
   ```
   - **Expected**: Benefits comparison shown
   - **Expected**: Final cost displayed
   - **Expected**: Confirmation button enabled

4. **User Confirms Purchase**
   ```
   User: "Sí, comprar"
   ```
   - **Expected**: Purchase request sent to Marketplace

5. **Marketplace Processes Purchase**
   - **Expected**: Product availability verified
   - **Expected**: Benefits calculated and applied
   - **Expected**: Payment event published to EventBridge

6. **Core Banking Processes Payment**
   - **Expected**: Funds validation (balance ≥ $25,000)
   - **Expected**: Debit from account: $14,500 → insufficient funds!
   - **Expected**: Payment declined

7. **User Receives Error**
   ```
   Agent: "Lo siento, no tienes fondos suficientes. Tu saldo actual es $14,500.00 MXN y el producto cuesta $25,000.00 MXN. ¿Te gustaría ver productos en tu rango de precio?"
   ```
   - **Expected**: Error message shown
   - **Expected**: Alternative suggestions offered

### Alternative Path: Successful Purchase

**Prerequisites**: User balance: $30,000.00 MXN

**Steps 5-7 (Alternative)**:

5. **Core Banking Processes Payment**
   - **Expected**: Funds validation passed
   - **Expected**: Debit from account: $30,000 → $5,000
   - **Expected**: Transaction recorded

6. **Marketplace Completes Purchase**
   - **Expected**: Purchase record created
   - **Expected**: Cashback credited: $5,000 + $2,500 = $7,500
   - **Expected**: Order confirmation generated

7. **User Receives Confirmation**
   ```
   Agent: "¡Compra exitosa! Has adquirido el iPhone 15 Pro por $25,000.00 MXN. Recibirás $2,500.00 MXN de cashback. Tu nuevo saldo es $7,500.00 MXN. Número de orden: ORD-12345."
   ```
   - **Expected**: Purchase confirmation with order number
   - **Expected**: Cashback amount shown
   - **Expected**: Updated balance displayed

### Success Criteria
- ✅ Product catalog displayed correctly
- ✅ Benefits calculated accurately
- ✅ Payment processed (or declined if insufficient funds)
- ✅ Cashback applied (if successful)
- ✅ Order confirmation provided
- ✅ Cross-unit communication working (Marketplace → Core Banking)

### Verification
```bash
# Check purchase record
aws dynamodb scan \
  --table-name centli-purchases \
  --filter-expression "user_id = :uid" \
  --expression-attribute-values '{":uid":{"S":"user-001"}}'

# Check transaction
aws dynamodb query \
  --table-name centli-transactions \
  --key-condition-expression "user_id = :uid" \
  --expression-attribute-values '{":uid":{"S":"user-001"}}' \
  --scan-index-forward false \
  --limit 1
```

---

## Scenario 4: Voice Interaction (Multimodal)

### Objective
Demonstrate voice input and output capabilities

### User Story
As a user, I want to interact with the agent using voice commands

### Prerequisites
- User authenticated
- Microphone access granted
- Nova Sonic configured

### Test Steps

1. **User Activates Voice**
   - Click microphone button
   - **Expected**: Recording indicator shows
   - **Expected**: Microphone icon changes to "recording" state

2. **User Speaks**
   ```
   User (voice): "¿Cuánto gasté esta semana?"
   ```
   - **Expected**: Audio captured
   - **Expected**: Audio streamed to AgentCore
   - **Expected**: Nova Sonic transcribes audio

3. **AgentCore Processes Voice**
   - **Expected**: Transcription: "¿Cuánto gasté esta semana?"
   - **Expected**: Intent recognized as "GET_SPENDING_SUMMARY"
   - **Expected**: Time range: last 7 days

4. **Core Banking Calculates**
   - **Expected**: Transactions retrieved for last 7 days
   - **Expected**: Total spending calculated: $3,450.00 MXN
   - **Expected**: Category breakdown calculated

5. **Agent Responds with Voice**
   ```
   Agent (voice): "Esta semana gastaste $3,450.00 pesos. La mayor parte fue en supermercado: $1,200 pesos."
   ```
   - **Expected**: Text response generated
   - **Expected**: Nova Sonic synthesizes voice
   - **Expected**: Audio played through speakers
   - **Expected**: Text also shown in chat

### Success Criteria
- ✅ Voice input captured correctly
- ✅ Transcription accurate
- ✅ Intent recognized from voice
- ✅ Voice response generated
- ✅ Audio quality acceptable
- ✅ Latency < 5 seconds

### Verification
```bash
# Check S3 for audio files
aws s3 ls s3://centli-assets-777937796305/audio/

# Check CloudWatch logs for Nova Sonic calls
aws logs tail /aws/lambda/centli-app-message --since 1m | grep "nova-sonic"
```

---

## Scenario 5: Image Upload (Receipt Processing)

### Objective
Demonstrate image processing with Nova Canvas

### User Story
As a user, I want to upload a receipt image for expense tracking

### Prerequisites
- User authenticated
- Camera/file picker access granted
- Nova Canvas configured

### Test Steps

1. **User Uploads Image**
   - Click camera/upload button
   - Select receipt image
   - **Expected**: Image preview shown
   - **Expected**: Upload progress indicator

2. **Image Uploaded to S3**
   - **Expected**: Image uploaded to S3 bucket
   - **Expected**: S3 URL generated
   - **Expected**: Image metadata sent to AgentCore

3. **Nova Canvas Processes Image**
   - **Expected**: OCR extracts text from receipt
   - **Expected**: Amount detected: $450.00 MXN
   - **Expected**: Merchant detected: "Walmart"
   - **Expected**: Date detected: "2026-02-17"

4. **Agent Confirms Details**
   ```
   Agent: "Detecté un gasto de $450.00 MXN en Walmart el 17 de febrero. ¿Es correcto?"
   ```
   - **Expected**: Extracted details shown
   - **Expected**: Confirmation requested

5. **User Confirms**
   ```
   User: "Sí, correcto"
   ```
   - **Expected**: Transaction recorded
   - **Expected**: Receipt linked to transaction

6. **Agent Confirms**
   ```
   Agent: "Gasto registrado. Tu nuevo saldo es $14,050.00 MXN."
   ```
   - **Expected**: Transaction saved
   - **Expected**: Receipt image linked
   - **Expected**: Balance updated

### Success Criteria
- ✅ Image uploaded successfully
- ✅ OCR extracts key information
- ✅ Transaction recorded with receipt
- ✅ Image accessible via S3 URL

### Verification
```bash
# Check S3 for uploaded image
aws s3 ls s3://centli-assets-777937796305/receipts/

# Check transaction with receipt link
aws dynamodb query \
  --table-name centli-transactions \
  --key-condition-expression "user_id = :uid" \
  --expression-attribute-values '{":uid":{"S":"user-001"}}' \
  --scan-index-forward false \
  --limit 1
```

---

## Demo Execution Checklist

### Pre-Demo (30 minutes before)
- [ ] Deploy all units to AWS
- [ ] Seed demo data in DynamoDB
- [ ] Verify WebSocket API is accessible
- [ ] Test frontend loads correctly
- [ ] Verify all Lambda functions are warm (invoke once)
- [ ] Check CloudWatch logs are accessible
- [ ] Prepare backup screenshots/videos
- [ ] Test microphone and speakers
- [ ] Test camera/file upload

### During Demo
- [ ] Start with Scenario 1 (simplest)
- [ ] Show CloudWatch logs in separate window
- [ ] Explain architecture between scenarios
- [ ] Have backup plan if live demo fails
- [ ] Monitor for errors in real-time

### Post-Demo
- [ ] Clean up test data
- [ ] Review CloudWatch logs for issues
- [ ] Document any bugs found
- [ ] Gather feedback

---

## Troubleshooting During Demo

### WebSocket Connection Fails
**Backup**: Show pre-recorded video of working connection

### Voice Not Working
**Backup**: Use text input instead, explain voice capability

### Image Upload Fails
**Backup**: Show pre-processed receipt example

### Lambda Timeout
**Backup**: Explain architecture, show logs, retry

### General Failure
**Backup**: Switch to presentation mode with screenshots

---

## Demo Talking Points

### Introduction (2 minutes)
- "CENTLI is a conversational financial coach powered by AWS Bedrock"
- "Built in 8 hours during a hackathon"
- "Demonstrates multimodal AI: text, voice, and images"

### Architecture (3 minutes)
- "4 units: Infrastructure, AgentCore, Action Groups, Frontend"
- "Event-driven architecture with EventBridge"
- "Serverless: Lambda, DynamoDB, S3, API Gateway"
- "AI/ML: Bedrock AgentCore, Nova Sonic, Nova Canvas"

### Demo (10 minutes)
- Scenario 1: Balance inquiry (2 min)
- Scenario 2: P2P transfer (3 min)
- Scenario 3: Product purchase (3 min)
- Scenario 4 or 5: Voice or Image (2 min)

### Conclusion (2 minutes)
- "Fully functional in 8 hours"
- "Scalable, serverless architecture"
- "Ready for production with additional hardening"

---

**Total Demo Time**: 15-20 minutes  
**Scenarios**: 5 scenarios (3 must-show, 2 optional)  
**Backup Plan**: Screenshots, videos, presentation slides
