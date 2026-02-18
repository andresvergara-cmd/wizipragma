#!/bin/bash

# Deploy Audio Processing Fix
# This script deploys the complete audio processing implementation

set -e

echo "🎤 =========================================="
echo "🎤 CENTLI - Audio Processing Deployment"
echo "🎤 =========================================="
echo ""

# Configuration
AWS_PROFILE="pragma-power-user"
LAMBDA_FUNCTION="poc-wizi-mex-lambda-inference-model-dev"
REGION="us-east-1"
FRONTEND_BUCKET="poc-wizi-mex-front"
CLOUDFRONT_ID="E29CTPS84NA5BZ"

echo "📦 Step 1: Package Lambda with audio_processor.py"
cd src_aws/app_inference

# Create deployment package
echo "Creating deployment package..."
zip -r ../../lambda-deployment.zip . -x "*.pyc" -x "__pycache__/*" -x "*.git*"

cd ../..

echo ""
echo "☁️  Step 2: Deploy Lambda Function"
aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION \
    --zip-file fileb://lambda-deployment.zip \
    --profile $AWS_PROFILE \
    --region $REGION

echo "Waiting for Lambda update to complete..."
aws lambda wait function-updated \
    --function-name $LAMBDA_FUNCTION \
    --profile $AWS_PROFILE \
    --region $REGION

echo ""
echo "🔧 Step 3: Verify Lambda has Bedrock permissions"
echo "Checking Lambda execution role..."
ROLE_NAME=$(aws lambda get-function \
    --function-name $LAMBDA_FUNCTION \
    --profile $AWS_PROFILE \
    --region $REGION \
    --query 'Configuration.Role' \
    --output text | awk -F'/' '{print $NF}')

echo "Lambda role: $ROLE_NAME"
echo ""
echo "⚠️  IMPORTANT: Verify this role has permission to invoke:"
echo "   - bedrock:InvokeModel for amazon.nova-sonic-v1:0"
echo "   - bedrock:InvokeModelWithResponseStream for amazon.nova-sonic-v1:0"
echo ""

echo "🌐 Step 4: Build and Deploy Frontend"
cd frontend

echo "Installing dependencies..."
npm install

echo "Building production bundle..."
npm run build

echo "Deploying to S3..."
aws s3 sync dist/ s3://$FRONTEND_BUCKET/ \
    --profile $AWS_PROFILE \
    --region $REGION \
    --delete

echo ""
echo "🔄 Step 5: Invalidate CloudFront Cache"
aws cloudfront create-invalidation \
    --distribution-id $CLOUDFRONT_ID \
    --paths "/*" \
    --profile $AWS_PROFILE \
    --region $REGION

cd ..

# Cleanup
rm -f lambda-deployment.zip

echo ""
echo "✅ =========================================="
echo "✅ Deployment Complete!"
echo "✅ =========================================="
echo ""
echo "🎤 Audio Processing Status:"
echo "   ✅ Backend: Lambda updated with audio_processor.py"
echo "   ✅ Frontend: Updated to send audio via WebSocket"
echo "   ✅ Model: Amazon Bedrock Nova Sonic (amazon.nova-sonic-v1:0)"
echo ""
echo "🌐 Frontend URL: https://d210pgg1e91kn6.cloudfront.net"
echo "🔌 WebSocket URL: wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"
echo ""
echo "📝 Next Steps:"
echo "   1. Wait 2-3 minutes for CloudFront cache invalidation"
echo "   2. Open frontend in browser (hard refresh: Cmd+Shift+R)"
echo "   3. Test audio recording with microphone button"
echo "   4. Check browser console for audio processing logs"
echo ""
echo "🔍 Troubleshooting:"
echo "   - Check Lambda logs: aws logs tail /aws/lambda/$LAMBDA_FUNCTION --follow --profile $AWS_PROFILE"
echo "   - Verify Bedrock permissions in IAM role: $ROLE_NAME"
echo "   - Test in browser console: Check for '🎤 Audio' logs"
echo ""
