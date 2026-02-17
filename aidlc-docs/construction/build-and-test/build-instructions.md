# Build Instructions - CENTLI Project

## Overview
CENTLI is a serverless multimodal banking assistant with 4 units. This document provides build and deployment instructions for all units.

---

## Unit 1: Infrastructure Foundation

### Status
✅ **DEPLOYED** - 2026-02-17

### Build Steps
No build required (SAM template only).

### Deployment
```bash
# Already deployed
# Stack: centli-hackathon
# Resources: EventBridge bus, S3 bucket, IAM roles, CloudWatch log group
```

### Verification
```bash
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

---

## Unit 2: AgentCore & Orchestration

### Status
✅ **DEPLOYED** - 2026-02-17

### Build Steps
```bash
# Build Lambda functions
sam build --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Deployment
```bash
# Deploy stack
sam deploy \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset
```

### Verification
```bash
# Test WebSocket connection
node test-websocket.js

# Check Lambda logs
aws logs tail /aws/lambda/centli-app-message \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Deployed Resources
- WebSocket API: `wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod`
- Lambda Functions: app_connect, app_disconnect, app_message
- DynamoDB Table: centli-sessions
- Bedrock Agent: centli-agentcore (Z6PCEKYNPS)

---

## Unit 3: Action Groups

### Status
⏳ **IN PROGRESS** - Assigned to Developer 2

### Build Steps
```bash
# Build Lambda functions (when ready)
sam build --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Deployment
```bash
# Deploy stack (when ready)
sam deploy \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset
```

### Expected Resources
- Lambda Functions: core_banking, marketplace, crm
- DynamoDB Tables: accounts, transactions, beneficiaries, products, purchases, user-profiles
- EventBridge Rules: Action event subscriptions

---

## Unit 4: Frontend Multimodal UI

### Status
✅ **CODE COMPLETE** - Ready for deployment

### Build Steps
**NO BUILD REQUIRED** - Vanilla JavaScript, no build process

### Pre-Deployment Configuration

#### 1. Enable S3 Static Website Hosting
```bash
aws s3 website s3://centli-frontend-bucket/ \
  --index-document index.html \
  --error-document index.html \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

#### 2. Set Bucket Policy (Public Read)
```bash
aws s3api put-bucket-policy \
  --bucket centli-frontend-bucket \
  --policy file://infrastructure/s3-bucket-policy.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

#### 3. Configure CORS
```bash
aws s3api put-bucket-cors \
  --bucket centli-frontend-bucket \
  --cors-configuration file://infrastructure/s3-cors-config.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

#### 4. Set Lifecycle Policy
```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket centli-frontend-bucket \
  --lifecycle-configuration file://infrastructure/s3-lifecycle-policy.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Deployment
```bash
# Deploy frontend files to S3
./commands/deploy-frontend.sh
```

### Verification
```bash
# Check S3 website endpoint
curl -I http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com

# Or open in browser
open http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com
```

### Frontend URL
- **S3 Website**: `http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com`
- **S3 HTTPS**: `https://centli-frontend-bucket.s3.amazonaws.com/index.html`

---

## Complete System Build

### Prerequisites
- AWS CLI configured with profile `777937796305_Ps-HackatonAgentic-Mexico`
- AWS SAM CLI installed (version 1.154.0+)
- Python 3.11 (for Lambda functions)
- Node.js (for WebSocket testing)

### Build All Units
```bash
# Unit 1 & 2 (already deployed)
sam build --profile 777937796305_Ps-HackatonAgentic-Mexico

# Unit 3 (when ready)
# sam build --profile 777937796305_Ps-HackatonAgentic-Mexico

# Unit 4 (no build needed)
# Just deploy to S3
```

### Deploy All Units
```bash
# Unit 1 & 2 (already deployed)
# Stack: centli-hackathon

# Unit 3 (when ready)
# sam deploy ...

# Unit 4
./commands/deploy-frontend.sh
```

---

## Build Troubleshooting

### SAM Build Fails
```bash
# Clean build artifacts
rm -rf .aws-sam/

# Rebuild
sam build --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Lambda Deployment Fails
```bash
# Check CloudFormation events
aws cloudformation describe-stack-events \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --max-items 20
```

### Frontend Deployment Fails
```bash
# Check S3 bucket exists
aws s3 ls s3://centli-frontend-bucket/ \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check bucket policy
aws s3api get-bucket-policy \
  --bucket centli-frontend-bucket \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

## Build Summary

| Unit | Build Required | Status | Deployment Method |
|------|----------------|--------|-------------------|
| Unit 1 | No | ✅ Deployed | SAM (CloudFormation) |
| Unit 2 | Yes (Python) | ✅ Deployed | SAM (CloudFormation) |
| Unit 3 | Yes (Python) | ⏳ In Progress | SAM (CloudFormation) |
| Unit 4 | No | ✅ Ready | AWS CLI (S3 sync) |

---

## Next Steps

1. ✅ Unit 1 & 2: Already deployed and tested
2. ⏳ Unit 3: Waiting for Developer 2 to complete
3. 🚀 Unit 4: Deploy to S3 and test
4. 🧪 Integration Testing: Test all units together
5. 🎯 Demo Preparation: Final end-to-end testing

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17T16:35:00Z
