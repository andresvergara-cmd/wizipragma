# Code Generation Plan - Unit 2: AgentCore & Orchestration

## Unit Context

**Unit Name**: AgentCore & Orchestration  
**Stories**: 6 stories (3.1-3.6) - AgentCore setup, Action Groups, Nova Sonic, Nova Canvas, Intent Recognition, Managed Memory  
**Code Location**: Workspace root (src_aws/)  
**Dependencies**: Unit 1 (EventBridge, S3, IAM, CloudWatch)

---

## Code Generation Steps

### Step 1: Lambda Function - Connect Handler
- [x] Create `src_aws/app_connect/app_connect.py`
- [x] Implement JWT validation
- [x] Create session in DynamoDB
- [x] Return connection success

### Step 2: Lambda Function - Disconnect Handler
- [x] Create `src_aws/app_disconnect/app_disconnect.py`
- [x] Update session state to DISCONNECTED
- [x] Sync final state to Managed Memory
- [x] Clean up resources

### Step 3: Lambda Function - Message Handler
- [x] Create `src_aws/app_message/app_message.py`
- [x] Route messages by type (TEXT, VOICE, IMAGE)
- [x] Invoke AgentCore for processing
- [x] Publish events to EventBridge
- [x] Send responses via WebSocket

### Step 4: Shared Utilities
- [x] SKIPPED - Utilities integrated directly into Lambda functions for hackathon speed

### Step 5: SAM Template Update
- [x] Add WebSocket API resources to `template.yaml`
- [x] Add 3 Lambda functions
- [x] Add DynamoDB sessions table
- [x] Add Lambda permissions
- [x] Add outputs

### Step 6: Bedrock Configuration Script
- [x] Create `scripts/configure-bedrock.sh`
- [x] Script to create AgentCore
- [x] Script to configure Action Groups
- [x] Script to enable Managed Memory

### Step 7: Deployment Script
- [x] Create `commands/deploy-unit2.sh`
- [x] SAM build and deploy commands
- [x] Bedrock configuration commands
- [x] Verification commands

### Step 8: Documentation
- [x] Create `aidlc-docs/construction/agentcore-orchestration/code/code-summary.md`
- [x] Document code structure
- [x] Document deployment steps
- [x] Document testing procedures

---

## Success Criteria

- [x] All Lambda functions created with minimal working code
- [x] SAM template updated with Unit 2 resources
- [x] Bedrock configuration script created
- [x] Deployment script created
- [x] Documentation created
- [x] Code follows Python 3.11 standards
- [ ] User approval obtained

---

**Plan Status**: Execution complete - Ready for deployment  
**Total Steps**: 8 steps (7 complete, 1 skipped)  
**Estimated Time**: 45-60 minutes

