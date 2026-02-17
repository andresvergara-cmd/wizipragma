#!/bin/bash
# Deploy Frontend to S3
# Usage: ./commands/deploy-frontend.sh

BUCKET="centli-frontend-bucket"
PROFILE="777937796305_Ps-HackatonAgentic-Mexico"
REGION="us-east-1"

echo "🚀 Deploying CENTLI Frontend to S3..."

# Sync frontend files to S3
echo "📦 Syncing files..."
aws s3 sync frontend/ s3://$BUCKET/ \
  --exclude "*.md" \
  --exclude ".DS_Store" \
  --delete \
  --profile $PROFILE \
  --region $REGION

# Set cache headers for HTML (no cache)
echo "⚙️  Setting cache headers for HTML..."
aws s3 cp s3://$BUCKET/index.html s3://$BUCKET/index.html \
  --metadata-directive REPLACE \
  --cache-control "max-age=0, no-cache" \
  --content-type "text/html" \
  --profile $PROFILE \
  --region $REGION

# Set cache headers for JS/CSS (1 hour cache)
echo "⚙️  Setting cache headers for JS/CSS..."
aws s3 cp s3://$BUCKET/js/ s3://$BUCKET/js/ \
  --recursive \
  --metadata-directive REPLACE \
  --cache-control "max-age=3600" \
  --profile $PROFILE \
  --region $REGION

aws s3 cp s3://$BUCKET/css/ s3://$BUCKET/css/ \
  --recursive \
  --metadata-directive REPLACE \
  --cache-control "max-age=3600" \
  --profile $PROFILE \
  --region $REGION

echo "✅ Deployment complete!"
echo "🌐 URL: http://$BUCKET.s3-website-$REGION.amazonaws.com"
echo ""
echo "📋 Next steps:"
echo "1. Test the frontend URL"
echo "2. Run manual testing checklist"
echo "3. Verify WebSocket connection"
