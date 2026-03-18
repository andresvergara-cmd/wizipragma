#!/bin/bash

# Test Transcribe + Polly Implementation
# This script tests the deployed Lambda function

set -e

echo "🧪 Testing Transcribe + Polly Implementation"
echo "=============================================="

LAMBDA_FUNCTION="centli-app-message"
REGION="us-east-1"

# Test 1: Lambda Configuration
echo ""
echo "📋 Test 1: Lambda Configuration"
echo "--------------------------------"

CONFIG=$(aws lambda get-function-configuration \
  --function-name $LAMBDA_FUNCTION \
  --region $REGION \
  --output json)

echo "Function: $(echo $CONFIG | jq -r '.FunctionName')"
echo "Runtime: $(echo $CONFIG | jq -r '.Runtime')"
echo "Memory: $(echo $CONFIG | jq -r '.MemorySize') MB"
echo "Timeout: $(echo $CONFIG | jq -r '.Timeout') seconds"
echo "Code Size: $(echo $CONFIG | jq -r '.CodeSize') bytes"
echo "Last Modified: $(echo $CONFIG | jq -r '.LastModified')"

# Test 2: Lambda Permissions
echo ""
echo "🔐 Test 2: Lambda Permissions"
echo "------------------------------"

ROLE_NAME="CentliLambdaExecutionRole"

echo "Checking inline policies..."
POLICIES=$(aws iam list-role-policies \
  --role-name $ROLE_NAME \
  --region $REGION \
  --output json)

echo "Inline policies: $(echo $POLICIES | jq -r '.PolicyNames | join(", ")')"

# Test 3: S3 Bucket for Transcribe
echo ""
echo "📦 Test 3: S3 Bucket for Transcribe"
echo "------------------------------------"

BUCKET="centli-assets-777937796305"
PREFIX="transcribe-temp/"

# Check if bucket exists
if aws s3 ls s3://$BUCKET --region $REGION > /dev/null 2>&1; then
  echo "✅ Bucket exists: s3://$BUCKET"
  
  # Check if prefix exists (create if not)
  if ! aws s3 ls s3://$BUCKET/$PREFIX --region $REGION > /dev/null 2>&1; then
    echo "Creating prefix: $PREFIX"
    aws s3api put-object \
      --bucket $BUCKET \
      --key $PREFIX \
      --region $REGION > /dev/null
  fi
  echo "✅ Prefix exists: s3://$BUCKET/$PREFIX"
else
  echo "❌ Bucket does not exist: s3://$BUCKET"
  exit 1
fi

# Test 4: Invoke Lambda with Text Message
echo ""
echo "💬 Test 4: Invoke Lambda with Text Message"
echo "-------------------------------------------"

cat > /tmp/test-text-event.json <<EOF
{
  "requestContext": {
    "connectionId": "test-connection-$(date +%s)",
    "domainName": "vvg621xawg.execute-api.us-east-1.amazonaws.com",
    "stage": "prod"
  },
  "body": "{\"action\":\"sendMessage\",\"data\":{\"user_id\":\"test-user\",\"session_id\":\"test-session-$(date +%s)\",\"type\":\"TEXT\",\"message\":\"Hola Comfi\"}}"
}
EOF

echo "Invoking Lambda with text message..."
aws lambda invoke \
  --function-name $LAMBDA_FUNCTION \
  --payload file:///tmp/test-text-event.json \
  --region $REGION \
  /tmp/lambda-text-response.json > /dev/null

echo "Response:"
cat /tmp/lambda-text-response.json | jq '.'

if grep -q "errorMessage" /tmp/lambda-text-response.json; then
  echo "❌ Lambda invocation failed"
  exit 1
else
  echo "✅ Lambda invocation successful"
fi

# Test 5: Check CloudWatch Logs
echo ""
echo "📊 Test 5: Check CloudWatch Logs"
echo "---------------------------------"

echo "Recent logs (last 5 minutes):"
aws logs filter-log-events \
  --log-group-name /aws/lambda/$LAMBDA_FUNCTION \
  --start-time $(($(date +%s) * 1000 - 300000)) \
  --region $REGION \
  --query 'events[*].message' \
  --output text | tail -20

# Test 6: Frontend Deployment
echo ""
echo "🌐 Test 6: Frontend Deployment"
echo "-------------------------------"

CLOUDFRONT_URL="https://db4aulosarsdo.cloudfront.net"

echo "Testing frontend URL: $CLOUDFRONT_URL"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $CLOUDFRONT_URL)

if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ Frontend is accessible (HTTP $HTTP_CODE)"
else
  echo "❌ Frontend is not accessible (HTTP $HTTP_CODE)"
fi

# Cleanup
rm -f /tmp/test-text-event.json
rm -f /tmp/lambda-text-response.json

echo ""
echo "=============================================="
echo "✅ All Tests Completed!"
echo ""
echo "Next steps:"
echo "1. Open browser: $CLOUDFRONT_URL"
echo "2. Click microphone button (🎤)"
echo "3. Say: '¿Cómo me afilio a Comfama?'"
echo "4. Verify transcription appears"
echo "5. Verify audio plays automatically"
echo ""
echo "Monitor logs:"
echo "aws logs tail /aws/lambda/$LAMBDA_FUNCTION --follow --region $REGION"
echo ""
