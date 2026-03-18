#!/bin/bash

# Deploy Audio Fix for Comfi
# Includes polly_tts.py in Lambda and updates frontend

set -e

echo "🚀 Deploying Audio Fix for Comfi..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
LAMBDA_FUNCTION="centli-app-message"
REGION="us-east-1"
S3_BUCKET="comfi-frontend-pragma"
CLOUDFRONT_ID="E2UWNXJTS2NM3V"

echo -e "${BLUE}📦 Step 1: Building Lambda package...${NC}"
cd src_aws/app_message

# Clean previous builds
rm -f function.zip

# Create ZIP with all required files
echo "  - Adding app_message.py"
zip -q function.zip app_message.py

echo "  - Adding polly_tts.py"
zip -q function.zip polly_tts.py

echo "  ✅ Lambda package created: function.zip"
ls -lh function.zip

echo ""
echo -e "${BLUE}🚀 Step 2: Deploying Lambda function...${NC}"
aws lambda update-function-code \
  --function-name $LAMBDA_FUNCTION \
  --zip-file fileb://function.zip \
  --region $REGION

echo "  ✅ Lambda function updated"

echo ""
echo -e "${BLUE}⏳ Step 3: Waiting for Lambda to be ready...${NC}"
aws lambda wait function-updated \
  --function-name $LAMBDA_FUNCTION \
  --region $REGION

echo "  ✅ Lambda is ready"

# Go back to project root
cd ../..

echo ""
echo -e "${BLUE}🎨 Step 4: Building frontend...${NC}"
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "  - Installing dependencies..."
  npm install
fi

# Build
echo "  - Building React app..."
npm run build

echo "  ✅ Frontend built"

echo ""
echo -e "${BLUE}☁️  Step 5: Deploying to S3...${NC}"
aws s3 sync dist/ s3://$S3_BUCKET/ --delete --region $REGION

echo "  ✅ Files uploaded to S3"

echo ""
echo -e "${BLUE}🔄 Step 6: Invalidating CloudFront cache...${NC}"
INVALIDATION_ID=$(aws cloudfront create-invalidation \
  --distribution-id $CLOUDFRONT_ID \
  --paths "/*" \
  --query 'Invalidation.Id' \
  --output text)

echo "  ✅ Invalidation created: $INVALIDATION_ID"

cd ..

echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo "📋 Summary:"
echo "  - Lambda: $LAMBDA_FUNCTION (with polly_tts.py)"
echo "  - S3: s3://$S3_BUCKET/"
echo "  - CloudFront: $CLOUDFRONT_ID"
echo "  - URL: https://db4aulosarsdo.cloudfront.net"
echo ""
echo -e "${YELLOW}⏳ CloudFront invalidation in progress...${NC}"
echo "   It may take 2-5 minutes for changes to propagate."
echo ""
echo "🧪 Testing:"
echo "  1. Open https://db4aulosarsdo.cloudfront.net"
echo "  2. Click the 🔇 button to activate voice"
echo "  3. Send a message"
echo "  4. Audio should play automatically"
echo ""
