#!/bin/bash

# Add Audio Transcription Permissions to Lambda Role
# Run this with admin credentials

echo "🔐 Adding Audio Transcription Permissions..."
echo "================================"

# Configuration
ROLE_NAME="poc-wizi-mex-stack-InferenceAPIFnRole-gNaIeNvDMIxD"
POLICY_NAME="AudioTranscriptionPolicy"
AWS_PROFILE="${1:-pragma-power-user}"  # Use first argument or default

echo "Role: $ROLE_NAME"
echo "Policy: $POLICY_NAME"
echo "Profile: $AWS_PROFILE"
echo ""

# Check if policy file exists
if [ ! -f "audio-iam-policy.json" ]; then
    echo "❌ Error: audio-iam-policy.json not found"
    exit 1
fi

# Try to add the policy
echo "Adding policy to role..."
aws iam put-role-policy \
    --role-name $ROLE_NAME \
    --policy-name $POLICY_NAME \
    --policy-document file://audio-iam-policy.json \
    --profile $AWS_PROFILE

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Permissions added successfully!"
    echo ""
    echo "Verify with:"
    echo "aws iam get-role-policy --role-name $ROLE_NAME --policy-name $POLICY_NAME --profile $AWS_PROFILE"
else
    echo ""
    echo "❌ Failed to add permissions"
    echo ""
    echo "You need admin/IAM permissions to run this command."
    echo ""
    echo "Alternative: Add the policy manually in IAM Console"
    echo "1. Go to: https://console.aws.amazon.com/iam/"
    echo "2. Find role: $ROLE_NAME"
    echo "3. Add inline policy with content from: audio-iam-policy.json"
    echo ""
fi
