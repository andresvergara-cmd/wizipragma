#!/bin/bash

# CENTLI Infrastructure Cleanup Script
# Deletes the entire CENTLI stack from AWS

set -e  # Exit on error

echo "========================================="
echo "CENTLI Infrastructure Cleanup"
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

# Warning
echo -e "${RED}WARNING: This will delete the entire CENTLI infrastructure!${NC}"
echo "Stack Name: $STACK_NAME"
echo "Region: $AWS_REGION"
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi
echo ""

# Step 1: Validate AWS credentials
echo -e "${YELLOW}Step 1: Validating AWS credentials...${NC}"
if ! aws sts get-caller-identity --profile $AWS_PROFILE --region $AWS_REGION > /dev/null 2>&1; then
    echo -e "${RED}ERROR: AWS credentials validation failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ AWS credentials validated${NC}"
echo ""

# Step 2: Check if stack exists
echo -e "${YELLOW}Step 2: Checking if stack exists...${NC}"
if ! aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --profile $AWS_PROFILE \
    --region $AWS_REGION > /dev/null 2>&1; then
    echo -e "${YELLOW}Stack $STACK_NAME does not exist${NC}"
    exit 0
fi
echo -e "${GREEN}✓ Stack found${NC}"
echo ""

# Step 3: Empty S3 bucket (required before deletion)
echo -e "${YELLOW}Step 3: Emptying S3 assets bucket...${NC}"
ACCOUNT_ID=$(aws sts get-caller-identity --profile $AWS_PROFILE --region $AWS_REGION --query Account --output text)
BUCKET_NAME="centli-assets-$ACCOUNT_ID"

if aws s3 ls s3://$BUCKET_NAME --profile $AWS_PROFILE --region $AWS_REGION > /dev/null 2>&1; then
    echo "Emptying bucket: $BUCKET_NAME"
    aws s3 rm s3://$BUCKET_NAME --recursive --profile $AWS_PROFILE --region $AWS_REGION
    echo -e "${GREEN}✓ S3 bucket emptied${NC}"
else
    echo -e "${YELLOW}S3 bucket does not exist or already empty${NC}"
fi
echo ""

# Step 4: Delete CloudFormation stack
echo -e "${YELLOW}Step 4: Deleting CloudFormation stack...${NC}"
echo "This may take a few minutes..."
echo ""

if ! aws cloudformation delete-stack \
    --stack-name $STACK_NAME \
    --profile $AWS_PROFILE \
    --region $AWS_REGION; then
    echo -e "${RED}ERROR: Stack deletion failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Stack deletion initiated${NC}"
echo ""

# Step 5: Wait for stack deletion
echo -e "${YELLOW}Step 5: Waiting for stack deletion to complete...${NC}"
echo "This may take several minutes..."
echo ""

if ! aws cloudformation wait stack-delete-complete \
    --stack-name $STACK_NAME \
    --profile $AWS_PROFILE \
    --region $AWS_REGION; then
    echo -e "${RED}ERROR: Stack deletion did not complete successfully${NC}"
    echo "Check AWS Console for details"
    exit 1
fi
echo -e "${GREEN}✓ Stack deletion completed${NC}"
echo ""

# Step 6: Verify deletion
echo -e "${YELLOW}Step 6: Verifying deletion...${NC}"
if aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --profile $AWS_PROFILE \
    --region $AWS_REGION > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Stack still exists${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Stack successfully deleted${NC}"
echo ""

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Cleanup Successful!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "All CENTLI infrastructure has been removed from AWS."
echo ""
