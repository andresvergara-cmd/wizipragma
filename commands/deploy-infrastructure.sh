#!/bin/bash

# CENTLI Infrastructure Deployment Script
# Deploys Unit 1 (Infrastructure Foundation) to AWS

set -e  # Exit on error

echo "========================================="
echo "CENTLI Infrastructure Deployment"
echo "========================================="
echo ""

# Configuration
AWS_PROFILE="777937796305_Ps-HackatonAgentic-Mexico"
AWS_REGION="us-east-1"
STACK_NAME="centli-hackathon"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Validate AWS credentials
echo -e "${YELLOW}Step 1: Validating AWS credentials...${NC}"
if ! aws sts get-caller-identity --profile $AWS_PROFILE --region $AWS_REGION > /dev/null 2>&1; then
    echo -e "${RED}ERROR: AWS credentials validation failed${NC}"
    echo "Please configure AWS profile: $AWS_PROFILE"
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --profile $AWS_PROFILE --region $AWS_REGION --query Account --output text)
echo -e "${GREEN}✓ AWS Account: $ACCOUNT_ID${NC}"
echo -e "${GREEN}✓ AWS Region: $AWS_REGION${NC}"
echo ""

# Step 2: Validate SAM template
echo -e "${YELLOW}Step 2: Validating SAM template...${NC}"
if ! sam validate --profile $AWS_PROFILE --region $AWS_REGION; then
    echo -e "${RED}ERROR: SAM template validation failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ SAM template is valid${NC}"
echo ""

# Step 3: Build SAM application
echo -e "${YELLOW}Step 3: Building SAM application...${NC}"
if ! sam build --cached --parallel; then
    echo -e "${RED}ERROR: SAM build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ SAM build completed${NC}"
echo ""

# Step 4: Deploy to AWS
echo -e "${YELLOW}Step 4: Deploying to AWS...${NC}"
echo "Stack Name: $STACK_NAME"
echo "This may take a few minutes..."
echo ""

if ! sam deploy \
    --stack-name $STACK_NAME \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --capabilities CAPABILITY_NAMED_IAM \
    --no-confirm-changeset \
    --parameter-overrides Environment=hackathon LogLevel=INFO \
    --tags Project=CENTLI Environment=Hackathon; then
    echo -e "${RED}ERROR: SAM deployment failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Deployment completed${NC}"
echo ""

# Step 5: Verify stack status
echo -e "${YELLOW}Step 5: Verifying stack status...${NC}"
STACK_STATUS=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --query 'Stacks[0].StackStatus' \
    --output text)

if [ "$STACK_STATUS" != "CREATE_COMPLETE" ] && [ "$STACK_STATUS" != "UPDATE_COMPLETE" ]; then
    echo -e "${RED}ERROR: Stack status is $STACK_STATUS${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Stack Status: $STACK_STATUS${NC}"
echo ""

# Step 6: Get stack outputs
echo -e "${YELLOW}Step 6: Retrieving stack outputs...${NC}"
echo ""
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --query 'Stacks[0].Outputs' \
    --output table

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Deployment Successful!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Stack Name: $STACK_NAME"
echo "Region: $AWS_REGION"
echo "Account: $ACCOUNT_ID"
echo ""
echo "Next Steps:"
echo "1. Review stack outputs above"
echo "2. Proceed to Unit 2 (AgentCore & Orchestration) deployment"
echo "3. Proceed to Unit 3 (Action Groups) deployment"
echo "4. Proceed to Unit 4 (Frontend) deployment"
echo ""
