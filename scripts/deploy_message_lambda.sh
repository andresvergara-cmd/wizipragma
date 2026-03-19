#!/bin/bash
# Deploy centli-app-message Lambda with Transcribe Streaming STT
# This replaces the slow batch Transcribe with streaming (~1-3s vs 5-60s)

set -e

FUNCTION_NAME="centli-app-message"
REGION="us-east-1"
SRC_DIR="src_aws/app_message"
ZIP_FILE="/tmp/app_message_deploy.zip"

echo "📦 Packaging Lambda function..."
rm -f "$ZIP_FILE"

# Create zip from the app_message directory
cd "$SRC_DIR"
zip -r "$ZIP_FILE" . -x "*.pyc" -x "__pycache__/*" -x "*.DS_Store"
cd -

echo "📊 Package size: $(du -h $ZIP_FILE | cut -f1)"

echo "🚀 Deploying to Lambda: $FUNCTION_NAME..."
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file "fileb://$ZIP_FILE" \
    --region "$REGION" \
    --no-cli-pager

echo ""
echo "⏱️ Updating Lambda timeout to 45s (was 180s)..."
aws lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --timeout 45 \
    --region "$REGION" \
    --no-cli-pager

echo ""
echo "✅ Deployment complete!"
echo "   - Transcribe Streaming SDK included"
echo "   - Timeout: 45s (was 180s)"
echo "   - Expected voice pipeline: ~6-10s total"
