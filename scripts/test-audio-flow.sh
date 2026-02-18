#!/bin/bash

# Test Audio Flow - Quick Verification Script

echo "🎤 =========================================="
echo "🎤 CENTLI Audio Flow Test"
echo "🎤 =========================================="
echo ""

AWS_PROFILE="pragma-power-user"
LAMBDA_FUNCTION="poc-wizi-mex-lambda-inference-model-dev"

echo "1️⃣  Checking Lambda deployment..."
LAST_MODIFIED=$(aws lambda get-function \
    --function-name $LAMBDA_FUNCTION \
    --profile $AWS_PROFILE \
    --region us-east-1 \
    --query 'Configuration.LastModified' \
    --output text)

echo "   ✅ Lambda last updated: $LAST_MODIFIED"
echo ""

echo "2️⃣  Checking Lambda code includes audio_processor..."
aws lambda get-function \
    --function-name $LAMBDA_FUNCTION \
    --profile $AWS_PROFILE \
    --region us-east-1 \
    --query 'Code.Location' \
    --output text > /tmp/lambda-url.txt

echo "   ℹ️  Downloading Lambda code to verify..."
curl -s $(cat /tmp/lambda-url.txt) -o /tmp/lambda-code.zip
unzip -l /tmp/lambda-code.zip | grep -E "(audio_processor|app\.py)" || echo "   ⚠️  Files not found in package"
echo ""

echo "3️⃣  Checking Bedrock permissions..."
POLICY=$(aws iam get-role-policy \
    --role-name poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD \
    --policy-name InferenceAPIFnRolePolicy0 \
    --profile $AWS_PROFILE \
    --region us-east-1 \
    --query 'PolicyDocument.Statement[0].Action' \
    --output text)

if [[ $POLICY == *"bedrock:*"* ]]; then
    echo "   ✅ Bedrock permissions: OK (bedrock:*)"
else
    echo "   ⚠️  Bedrock permissions: $POLICY"
fi
echo ""

echo "4️⃣  Checking CloudFront invalidation status..."
INVALIDATION_STATUS=$(aws cloudfront get-invalidation \
    --distribution-id E29CTPS84NA5BZ \
    --id I4WAN4SXALBCTX4WTAHHWXB8AC \
    --profile $AWS_PROFILE \
    --region us-east-1 \
    --query 'Invalidation.Status' \
    --output text 2>/dev/null || echo "Unknown")

echo "   Status: $INVALIDATION_STATUS"
if [[ $INVALIDATION_STATUS == "Completed" ]]; then
    echo "   ✅ Cache invalidation complete - frontend ready!"
else
    echo "   ⏳ Cache invalidation in progress - wait 1-2 more minutes"
fi
echo ""

echo "5️⃣  Testing Nova Sonic model availability..."
echo "   ℹ️  Attempting to list Bedrock models..."
aws bedrock list-foundation-models \
    --profile $AWS_PROFILE \
    --region us-east-1 \
    --query "modelSummaries[?contains(modelId, 'nova-sonic')].{ModelId:modelId,Status:modelLifecycle.status}" \
    --output table 2>/dev/null || echo "   ⚠️  Could not verify Nova Sonic availability"
echo ""

echo "6️⃣  Frontend URLs:"
echo "   🌐 Frontend: https://d210pgg1e91kn6.cloudfront.net"
echo "   🔌 WebSocket: wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"
echo ""

echo "7️⃣  Test Instructions:"
echo "   1. Open: https://d210pgg1e91kn6.cloudfront.net"
echo "   2. Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)"
echo "   3. Open browser console (F12)"
echo "   4. Click chat button to open CENTLI"
echo "   5. Click 🎤 microphone button"
echo "   6. Allow microphone access"
echo "   7. Say: '¿Cuál es mi saldo?'"
echo "   8. Click ⏹️ to stop recording"
echo "   9. Watch console for logs:"
echo "      - 🎤 Processing voice message"
echo "      - 🎤 Audio converted to base64"
echo "      - 📤 Sending AUDIO message"
echo "   10. Wait for CENTLI response"
echo ""

echo "8️⃣  Monitor Lambda logs:"
echo "   aws logs tail /aws/lambda/$LAMBDA_FUNCTION --follow --profile $AWS_PROFILE"
echo ""

echo "✅ =========================================="
echo "✅ Pre-flight checks complete!"
echo "✅ =========================================="
echo ""

# Cleanup
rm -f /tmp/lambda-url.txt /tmp/lambda-code.zip
