#!/bin/bash

# Deploy Tool Use Fix to Lambda
# Fixes tool input parameter parsing in streaming API

echo "🚀 Deploying Tool Use Fix..."
echo "================================"

# Configuration
LAMBDA_NAME="poc-wizi-mex-lambda-inference-model-dev"
AWS_PROFILE="pragma-power-user"
REGION="us-east-1"

# Create deployment package
echo "📦 Creating deployment package..."
cd src_aws/app_inference
zip -r ../../lambda-tool-use-fix.zip . -x "*.pyc" -x "__pycache__/*" -x "*.git*"
cd ../..

# Deploy to Lambda
echo "☁️  Uploading to Lambda..."
aws lambda update-function-code \
    --function-name $LAMBDA_NAME \
    --zip-file fileb://lambda-tool-use-fix.zip \
    --profile $AWS_PROFILE \
    --region $REGION

# Wait for update to complete
echo "⏳ Waiting for Lambda update..."
aws lambda wait function-updated \
    --function-name $LAMBDA_NAME \
    --profile $AWS_PROFILE \
    --region $REGION

# Clean up
rm lambda-tool-use-fix.zip

echo ""
echo "✅ Tool Use Fix Deployed Successfully!"
echo "================================"
echo ""
echo "🧪 Test with:"
echo "   'Envía \$500 a mi mamá'"
echo "   'Quiero comprar un iPhone 15 Pro'"
echo ""
echo "📊 Monitor logs:"
echo "   aws logs tail /aws/lambda/$LAMBDA_NAME --follow --profile $AWS_PROFILE"
