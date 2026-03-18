#!/bin/bash

# Deploy Transcribe + Polly Implementation
# This script deploys the updated Lambda with Transcribe STT and Polly TTS

set -e

echo "🚀 Deploying Transcribe + Polly Implementation"
echo "=============================================="

# Configuration
LAMBDA_FUNCTION="centli-app-message"
REGION="us-east-1"
ACCOUNT_ID="777937796305"

# Step 1: Package Lambda
echo ""
echo "📦 Step 1: Packaging Lambda..."
cd src_aws/app_message

# Create deployment package
zip -r app_message.zip . -x "*.pyc" -x "__pycache__/*" -x "*.git*"

echo "✅ Package created: $(du -h app_message.zip | cut -f1)"

# Step 2: Update Lambda function code
echo ""
echo "🔄 Step 2: Updating Lambda function code..."
aws lambda update-function-code \
  --function-name $LAMBDA_FUNCTION \
  --zip-file fileb://app_message.zip \
  --region $REGION

echo "✅ Lambda code updated"

# Step 3: Wait for Lambda to be ready
echo ""
echo "⏳ Step 3: Waiting for Lambda to be ready..."
aws lambda wait function-updated \
  --function-name $LAMBDA_FUNCTION \
  --region $REGION

echo "✅ Lambda is ready"

# Step 4: Update Lambda permissions (if needed)
echo ""
echo "🔐 Step 4: Checking Lambda permissions..."

# Get current Lambda role
LAMBDA_ROLE=$(aws lambda get-function-configuration \
  --function-name $LAMBDA_FUNCTION \
  --region $REGION \
  --query 'Role' \
  --output text)

ROLE_NAME=$(echo $LAMBDA_ROLE | awk -F'/' '{print $NF}')

echo "Lambda role: $ROLE_NAME"

# Create policy document for Transcribe and S3
cat > /tmp/transcribe-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "transcribe:DeleteTranscriptionJob"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::centli-assets-$ACCOUNT_ID/transcribe-temp/*"
    }
  ]
}
EOF

# Check if policy already exists
POLICY_ARN="arn:aws:iam::$ACCOUNT_ID:policy/TranscribePollyPolicy"

if aws iam get-policy --policy-arn $POLICY_ARN --region $REGION 2>/dev/null; then
  echo "Policy already exists, updating..."
  
  # Create new policy version
  aws iam create-policy-version \
    --policy-arn $POLICY_ARN \
    --policy-document file:///tmp/transcribe-policy.json \
    --set-as-default \
    --region $REGION
else
  echo "Creating new policy..."
  
  # Create policy
  aws iam create-policy \
    --policy-name TranscribePollyPolicy \
    --policy-document file:///tmp/transcribe-policy.json \
    --region $REGION
fi

# Attach policy to role
echo "Attaching policy to role..."
aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn $POLICY_ARN \
  --region $REGION 2>/dev/null || echo "Policy already attached"

echo "✅ Permissions configured"

# Step 5: Test Lambda
echo ""
echo "🧪 Step 5: Testing Lambda..."

# Create test event
cat > /tmp/test-event.json <<EOF
{
  "requestContext": {
    "connectionId": "test-connection-id",
    "domainName": "vvg621xawg.execute-api.us-east-1.amazonaws.com",
    "stage": "prod"
  },
  "body": "{\"action\":\"sendMessage\",\"data\":{\"user_id\":\"test-user\",\"session_id\":\"test-session\",\"type\":\"TEXT\",\"message\":\"Hola\"}}"
}
EOF

echo "Invoking Lambda with test event..."
aws lambda invoke \
  --function-name $LAMBDA_FUNCTION \
  --payload file:///tmp/test-event.json \
  --region $REGION \
  /tmp/lambda-response.json

echo ""
echo "Lambda response:"
cat /tmp/lambda-response.json
echo ""

# Check for errors
if grep -q "errorMessage" /tmp/lambda-response.json; then
  echo "❌ Lambda test failed"
  exit 1
else
  echo "✅ Lambda test passed"
fi

# Cleanup
rm -f app_message.zip
rm -f /tmp/transcribe-policy.json
rm -f /tmp/test-event.json
rm -f /tmp/lambda-response.json

echo ""
echo "=============================================="
echo "✅ Deployment Complete!"
echo ""
echo "Lambda Function: $LAMBDA_FUNCTION"
echo "Region: $REGION"
echo ""
echo "Next steps:"
echo "1. Deploy frontend: cd frontend && npm run build && ./deploy-frontend.sh"
echo "2. Test voice message in browser"
echo "3. Monitor logs: aws logs tail /aws/lambda/$LAMBDA_FUNCTION --follow"
echo ""
