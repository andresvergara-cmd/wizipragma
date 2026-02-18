#!/bin/bash

# Deploy Performance Optimizations - Phase 1
# Reduces latency from 4.54s to ~3.54s (-22%)

set -e

echo "🚀 =========================================="
echo "🚀 CENTLI - Performance Optimizations Phase 1"
echo "🚀 =========================================="
echo ""

# Configuration
AWS_PROFILE="pragma-power-user"
LAMBDA_FUNCTION="poc-wizi-mex-lambda-inference-model-dev"
REGION="us-east-1"

echo "📋 Optimizations to deploy:"
echo "   1. ✅ Reduce transactions to 50 (from 300)"
echo "   2. ✅ Lower temperature to 0.5 (from 0.6)"
echo "   3. ✅ Optimize system prompt (simplified)"
echo "   4. ✅ Add audio output with Nova Sonic (TTS)"
echo ""
echo "Expected impact: -1.0s latency (22% improvement)"
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Deployment cancelled"
    exit 1
fi

echo ""
echo "📦 Step 1: Package Lambda with optimizations"
cd src_aws/app_inference

# Create deployment package
echo "Creating deployment package..."
zip -r ../../lambda-optimized.zip . -x "*.pyc" -x "__pycache__/*" -x "*.git*"

cd ../..

echo ""
echo "☁️  Step 2: Deploy Lambda Function"
aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION \
    --zip-file fileb://lambda-optimized.zip \
    --profile $AWS_PROFILE \
    --region $REGION

echo "Waiting for Lambda update to complete..."
aws lambda wait function-updated \
    --function-name $LAMBDA_FUNCTION \
    --profile $AWS_PROFILE \
    --region $REGION

echo ""
echo "✅ =========================================="
echo "✅ Deployment Complete!"
echo "✅ =========================================="
echo ""
echo "📊 Optimizations Deployed:"
echo "   ✅ Transactions limited to 50 most recent"
echo "   ✅ Temperature reduced to 0.5"
echo "   ✅ System prompt optimized (50% shorter)"
echo "   ✅ Audio output with Nova Sonic added"
echo ""
echo "📈 Expected Performance:"
echo "   Before: 4.54s average latency"
echo "   After:  ~3.54s average latency"
echo "   Improvement: -1.0s (22% faster)"
echo ""
echo "🧪 Testing:"
echo "   1. Open: https://d210pgg1e91kn6.cloudfront.net"
echo "   2. Send test message: '¿Cuál es mi saldo?'"
echo "   3. Measure response time (should be ~3.5s)"
echo "   4. Try audio input (should generate audio response)"
echo ""
echo "📝 Monitor logs:"
echo "   aws logs tail /aws/lambda/$LAMBDA_FUNCTION --follow --profile $AWS_PROFILE"
echo ""
echo "🔍 Look for in logs:"
echo "   - 'Processing X most recent transactions (optimized from full set)'"
echo "   - 'Generating audio response with Nova Sonic'"
echo "   - Reduced total duration in REPORT lines"
echo ""

# Cleanup
rm -f lambda-optimized.zip

echo "✅ Done!"
