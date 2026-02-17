# Code Summary - Unit 2: AgentCore & Orchestration

## Overview

Unit 2 code generation complete. Created 3 Lambda functions for WebSocket handling and AgentCore orchestration.

**Code Location**: `src_aws/` (workspace root)

---

## Generated Files

### 1. Lambda Functions

**app_connect/app_connect.py** (~100 lines)
- Handles WebSocket $connect route
- JWT token validation (simplified for hackathon)
- Session creation in DynamoDB
- Returns 200 (success) or 401/403 (auth failure)

**app_disconnect/app_disconnect.py** (~60 lines)
- Handles WebSocket $disconnect route
- Updates session state to DISCONNECTED
- Cleans up resources
- Always returns 200

**app_message/app_message.py** (~250 lines)
- Handles WebSocket $default route (messages)
- Routes by message type (TEXT, VOICE, IMAGE)
- Invokes Bedrock AgentCore for text processing
- Sends responses via WebSocket
- Placeholders for voice/image processing

---

## Code Structure

```
src_aws/
├── app_connect/
│   └── app_connect.py          # WebSocket connect handler
├── app_disconnect/
│   └── app_disconnect.py       # WebSocket disconnect handler
└── app_message/
    └── app_message.py          # WebSocket message handler
```

---

## Key Features Implemented

### Authentication
- JWT token validation (simplified)
- User ID extraction from token
- Token expiration check
- Session creation with user context

### Session Management
- DynamoDB session storage
- Session state tracking (ACTIVE, DISCONNECTED)
- Last activity timestamp updates
- Message count tracking
- TTL for automatic cleanup

### Message Processing
- Text message processing via AgentCore
- Voice message placeholder (returns text response)
- Image message placeholder (returns text response)
- Error handling and user feedback

### WebSocket Communication
- Send messages to connections
- Send error messages
- Handle connection failures gracefully

---

## Next Steps for Full Implementation

### Voice Processing (Story 3.3)
1. Decode base64 audio in `process_voice_message()`
2. Invoke Nova Sonic for transcription
3. Process transcribed text through AgentCore
4. Invoke Nova Sonic for synthesis
5. Return base64 audio response

### Image Processing (Story 3.4)
1. Decode base64 image in `process_image_message()`
2. Upload image to S3
3. Invoke Nova Canvas for analysis
4. Merge analysis with text context
5. Process through AgentCore

### Event Publishing (Story 3.2)
1. Extract intent from AgentCore response
2. Build EventBridge event payload
3. Publish to `centli-event-bus`
4. Handle response events from Action Groups

### Managed Memory (Story 3.6)
1. Sync session state to Bedrock Managed Memory
2. Retrieve conversation history
3. Include context in AgentCore invocations

---

## Deployment Instructions

### Prerequisites
- AWS SAM CLI installed (version 1.154.0+)
- AWS CLI configured with profile `777937796305_Ps-HackatonAgentic-Mexico`
- Python 3.11 runtime available

### 1. Deploy Unit 2 Infrastructure

```bash
# Run deployment script
./commands/deploy-unit2.sh
```

This script will:
1. Build Lambda functions with SAM
2. Deploy CloudFormation stack with all Unit 2 resources
3. Display WebSocket URL and other outputs

### 2. Configure Bedrock AgentCore (Manual)

```bash
# Run configuration script for instructions
./scripts/configure-bedrock.sh
```

Manual steps required:
1. Create Bedrock Agent via AWS Console
   - Agent name: `centli-agentcore`
   - Foundation model: Claude 3.5 Sonnet v2
   - Instructions: Banking assistant prompt
2. Enable Managed Memory (session-based)
3. Create Agent Alias: `prod`
4. Note Agent ID and Alias ID

### 3. Update Lambda Environment Variable

```bash
# Replace <AGENT_ID> with actual Agent ID from step 2
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
# Install wscat (if not already installed)
npm install -g wscat

# Get WebSocket URL from stack outputs
WEBSOCKET_URL=$(aws cloudformation describe-stacks \
    --profile 777937796305_Ps-HackatonAgentic-Mexico \
    --region us-east-1 \
    --stack-name centli-hackathon \
    --query "Stacks[0].Outputs[?OutputKey=='WebSocketURL'].OutputValue" \
    --output text)

# Connect with test JWT token
wscat -c "$WEBSOCKET_URL?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdC11c2VyIiwiZXhwIjoxNzQwMDAwMDAwfQ.test"

# Send test message
{"type":"TEXT","content":"Hola, ¿cuál es mi saldo?"}
```

---

## Testing Checklist

- [ ] WebSocket connection succeeds with valid token
- [ ] WebSocket connection fails with invalid token
- [ ] Session created in DynamoDB on connect
- [ ] Text message processed and response received
- [ ] Session updated with last_activity on message
- [ ] Disconnect updates session state
- [ ] Error messages sent for failures

---

## Known Limitations (Hackathon Scope)

1. **JWT Validation**: Simplified (no signature verification)
2. **Voice Processing**: Placeholder only
3. **Image Processing**: Placeholder only
4. **Event Publishing**: Not yet implemented
5. **Managed Memory**: Not yet synced
6. **Error Handling**: Basic (no retry logic)
7. **Logging**: Print statements (no structured logging)

---

## Production Enhancements Needed

1. **Security**:
   - Proper JWT validation with signature verification
   - Rate limiting per user
   - Input sanitization

2. **Reliability**:
   - Retry logic with exponential backoff
   - Circuit breaker for external services
   - Dead letter queues for failed messages

3. **Observability**:
   - Structured logging (JSON format)
   - CloudWatch metrics and alarms
   - X-Ray tracing

4. **Performance**:
   - Connection pooling
   - Lambda provisioned concurrency
   - DynamoDB DAX caching

---

**Document Status**: Complete  
**Created**: 2026-02-17  
**Code Files**: 3 Lambda functions (~410 lines total)  
**Status**: Minimal working implementation for hackathon demo

