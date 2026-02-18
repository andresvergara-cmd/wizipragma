#!/bin/bash

# Deploy Audio Transcription with Amazon Transcribe
# Creates S3 bucket and deploys Lambda with audio support

echo "🎤 Deploying Audio Transcription..."
echo "================================"

# Configuration
LAMBDA_NAME="poc-wizi-mex-lambda-inference-model-dev"
AWS_PROFILE="pragma-power-user"
REGION="us-east-1"
S3_BUCKET="poc-wizi-mex-audio-temp"
ACCOUNT_ID=$(aws sts get-caller-identity --profile $AWS_PROFILE --query Account --output text)

# Step 1: Create S3 bucket for temporary audio storage
echo "📦 Creating S3 bucket for audio..."
aws s3 mb s3://$S3_BUCKET --profile $AWS_PROFILE --region $REGION 2>/dev/null || echo "Bucket already exists"

# Configure bucket lifecycle to delete files after 1 day
cat > /tmp/lifecycle-policy.json <<EOF
{
  "Rules": [
    {
      "Id": "DeleteAudioAfter1Day",
      "Status": "Enabled",
      "Prefix": "audio-input/",
      "Expiration": {
        "Days": 1
      }
    }
  ]
}
EOF

aws s3api put-bucket-lifecycle-configuration \
    --bucket $S3_BUCKET \
    --lifecycle-configuration file:///tmp/lifecycle-policy.json \
    --profile $AWS_PROFILE

echo "✅ S3 bucket configured"

# Step 2: Update Lambda IAM role to allow Transcribe and S3 access
echo "🔐 Updating Lambda IAM permissions..."

# Get Lambda role name
ROLE_NAME=$(aws lambda get-function \
    --function-name $LAMBDA_NAME \
    --profile $AWS_PROFILE \
    --region $REGION \
    --query 'Configuration.Role' \
    --output text | awk -F'/' '{print $NF}')

echo "Lambda role: $ROLE_NAME"

# Create policy for Transcribe and S3
cat > /tmp/audio-policy.json <<EOF
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
      "Resource": "arn:aws:s3:::${S3_BUCKET}/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::${S3_BUCKET}"
    }
  ]
}
EOF

# Create or update inline policy
aws iam put-role-policy \
    --role-name $ROLE_NAME \
    --policy-name AudioTranscriptionPolicy \
    --policy-document file:///tmp/audio-policy.json \
    --profile $AWS_PROFILE

echo "✅ IAM permissions updated"

# Step 3: Deploy Lambda code
echo "📦 Creating deployment package..."
cd src_aws/app_inference
zip -r ../../lambda-audio-transcribe.zip . -x "*.pyc" -x "__pycache__/*" -x "*.git*" -x "lambda-*.zip"
cd ../..

echo "☁️  Uploading to Lambda..."
aws lambda update-function-code \
    --function-name $LAMBDA_NAME \
    --zip-file fileb://lambda-audio-transcribe.zip \
    --profile $AWS_PROFILE \
    --region $REGION

# Wait for update to complete
echo "⏳ Waiting for Lambda update..."
aws lambda wait function-updated \
    --function-name $LAMBDA_NAME \
    --profile $AWS_PROFILE \
    --region $REGION

# Clean up
rm lambda-audio-transcribe.zip
rm /tmp/lifecycle-policy.json
rm /tmp/audio-policy.json

echo ""
echo "✅ Audio Transcription Deployed Successfully!"
echo "================================"
echo ""
echo "🎤 Configuración:"
echo "   S3 Bucket: $S3_BUCKET"
echo "   Lambda: $LAMBDA_NAME"
echo "   Región: $REGION"
echo ""
echo "🧪 Prueba con audio:"
echo "   1. Abre: https://d210pgg1e91kn6.cloudfront.net"
echo "   2. Haz hard refresh (Cmd+Shift+R)"
echo "   3. Graba un mensaje de voz"
echo "   4. Prueba: 'Envía quinientos pesos a mi mamá'"
echo ""
echo "📊 Monitor logs:"
echo "   aws logs tail /aws/lambda/$LAMBDA_NAME --follow --profile $AWS_PROFILE"
echo ""
