#!/bin/bash
# Deploy Unit 2: AgentCore & Orchestration
# This script deploys the WebSocket API, Lambda functions, and DynamoDB table

set -e

echo "=========================================="
echo "CENTLI - Unit 2 Deployment"
echo "AgentCore & Orchestration"
echo "=========================================="
echo ""

# Configuration
PROFILE="777937796305_Ps-HackatonAgentic-Mexico"
REGION="us-east-1"
STACK_NAME="centli-hackathon"

echo "Configuration:"
echo "  AWS Profile: $PROFILE"
echo "  AWS Region: $REGION"
echo "  Stack Name: $STACK_NAME"
echo ""

# Step 1: Build SAM application
echo "Step 1: Building SAM application..."
sam build --profile $PROFILE

if [ $? -ne 0 ]; then
    echo "❌ SAM build failed"
    exit 1
fi
echo "✅ SAM build successful"
echo ""

# Step 2: Deploy SAM application
echo "Step 2: Deploying SAM application..."
sam deploy \
    --profile $PROFILE \
    --region $REGION \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_NAMED_IAM \
    --no-confirm-changeset \
    --no-fail-on-empty-changeset

if [ $? -ne 0 ]; then
    echo "❌ SAM deploy failed"
    exit 1
fi
echo "✅ SAM deploy successful"
echo ""

# Step 3: Get stack outputs
echo "Step 3: Retrieving stack outputs..."
WEBSOCKET_URL=$(aws cloudformation describe-stacks \
    --profile $PROFILE \
    --region $REGION \
    --stack-name $STACK_NAME \
    --query "Stacks[0].Outputs[?OutputKey=='WebSocketURL'].OutputValue" \
    --output text)

SESSIONS_TABLE=$(aws cloudformation describe-stacks \
    --profile $PROFILE \
    --region $REGION \
    --stack-name $STACK_NAME \
    --query "Stacks[0].Outputs[?OutputKey=='SessionsTableName'].OutputValue" \
    --output text)

echo "✅ Stack outputs retrieved"
echo ""

# Step 4: Display deployment summary
echo "=========================================="
echo "Deployment Summary"
echo "=========================================="
echo "WebSocket URL: $WEBSOCKET_URL"
echo "Sessions Table: $SESSIONS_TABLE"
echo ""
echo "Next Steps:"
echo "1. Configure Bedrock AgentCore (run scripts/configure-bedrock.sh)"
echo "2. Update MessageFunction environment variable AGENTCORE_ID"
echo "3. Test WebSocket connection with wscat:"
echo "   wscat -c \"$WEBSOCKET_URL\""
echo ""
echo "✅ Unit 2 deployment complete!"
