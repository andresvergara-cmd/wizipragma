# Infrastructure Design - Unit 4: Frontend Multimodal UI

## Document Information
- **Unit**: Frontend Multimodal UI
- **Created**: 2026-02-17
- **Context**: 8-hour hackathon, demo quality, simple deployment
- **Cloud Provider**: AWS
- **Region**: us-east-1

---

## 1. Infrastructure Overview

### 1.1 Architecture Summary
The frontend is a static web application hosted on AWS S3 with static website hosting enabled. It communicates with the backend via WebSocket (Unit 2) and uploads images directly to S3 using presigned URLs.

**Key Characteristics**:
- Serverless (no compute instances)
- Static file hosting (HTML, CSS, JavaScript)
- Direct S3 uploads for images
- WebSocket client (connects to Unit 2)
- Single environment (production)

---

## 2. Hosting Infrastructure

### 2.1 S3 Static Website Hosting

**Service**: Amazon S3  
**Bucket**: `centli-frontend-bucket` (from Unit 1)  
**Configuration**: Static website hosting enabled

**Bucket Properties**:
```yaml
BucketName: centli-frontend-bucket
Region: us-east-1
WebsiteConfiguration:
  IndexDocument: index.html
  ErrorDocument: index.html  # SPA behavior
PublicAccessBlock:
  BlockPublicAcls: false
  IgnorePublicAcls: false
  BlockPublicPolicy: false
  RestrictPublicBuckets: false
BucketPolicy:
  Effect: Allow
  Principal: "*"
  Action: s3:GetObject
  Resource: arn:aws:s3:::centli-frontend-bucket/*
```

**Access URLs**:
- **Website Endpoint** (HTTP): `http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com`
- **Object Endpoint** (HTTPS): `https://centli-frontend-bucket.s3.amazonaws.com/index.html`

**Rationale**: S3 static website hosting is the simplest, fastest deployment option for static files. No server management, automatic scaling, pay-per-use pricing.

---

### 2.2 CORS Configuration

**Purpose**: Allow WebSocket connections and image uploads from frontend

**CORS Rules**:
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

**Rationale**: Permissive CORS for demo. Allows frontend to:
- Load static assets (GET)
- Upload images (PUT)
- Make API calls (POST)

---

## 3. Storage Infrastructure

### 3.1 Image Upload Storage

**Service**: Amazon S3 (same bucket as frontend)  
**Bucket**: `centli-frontend-bucket`  
**Path Structure**: `/uploads/{session_id}/{timestamp}_{filename}.jpg`

**Example Paths**:
```
/uploads/session_1708185600000/1708185612345_receipt.jpg
/uploads/session_1708185600000/1708185623456_product.jpg
```

**Access**: Public read (anyone with URL can view)

**Rationale**: 
- Same bucket simplifies permissions and deployment
- Session-based folders organize uploads
- Timestamp prevents filename collisions
- Public read simplifies demo (no signed URLs needed)

---

### 3.2 Lifecycle Policy

**Purpose**: Auto-delete demo data after 24 hours

**Lifecycle Rule**:
```json
{
  "Rules": [
    {
      "Id": "DeleteUploadsAfter24Hours",
      "Status": "Enabled",
      "Prefix": "uploads/",
      "Expiration": {
        "Days": 1
      }
    }
  ]
}
```

**Rationale**: Demo data doesn't need long-term retention. Auto-cleanup prevents bucket bloat.

---

## 4. Integration Points

### 4.1 WebSocket API Gateway

**Service**: AWS API Gateway (WebSocket)  
**Endpoint**: `wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod`  
**Stage**: prod  
**Protocol**: WSS (WebSocket Secure)

**Connection Flow**:
1. Frontend loads, reads WebSocket URL from config.js
2. Frontend establishes WebSocket connection
3. Frontend sends authentication message with user_id
4. Backend creates session in DynamoDB
5. Frontend sends/receives messages via WebSocket

**Configuration File** (`config.js`):
```javascript
const CONFIG = {
  WS_URL: 'wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod',
  S3_BUCKET: 'centli-frontend-bucket',
  S3_REGION: 'us-east-1',
  API_TIMEOUT: 30000, // 30 seconds
  MAX_IMAGE_SIZE: 5 * 1024 * 1024, // 5MB
  MAX_RECORDING_DURATION: 30000 // 30 seconds
};
```

---

### 4.2 Authentication

**Approach**: Mock client-side token generation

**Token Generation**:
```javascript
function generateMockToken(userId) {
  const payload = {
    user_id: userId,
    timestamp: Date.now(),
    session_id: 'session_' + Date.now()
  };
  // Simple base64 encoding (not real JWT for demo)
  return btoa(JSON.stringify(payload));
}
```

**Token Usage**:
- Stored in localStorage
- Sent in WebSocket connection message
- Included in image upload requests (optional)

**Rationale**: Real authentication out of scope for hackathon. Focus on multimodal functionality.

---

### 4.3 Image Upload Flow

**Approach**: Direct S3 upload with presigned URL

**Flow**:
1. User selects image in frontend
2. Frontend compresses image (Canvas API)
3. Frontend requests presigned URL from backend (via WebSocket)
4. Backend generates presigned URL (S3 PutObject)
5. Backend sends presigned URL to frontend (via WebSocket)
6. Frontend uploads image directly to S3 (HTTP PUT)
7. Frontend sends image URL to backend for processing

**Presigned URL Request** (WebSocket message):
```json
{
  "action": "request_presigned_url",
  "filename": "receipt.jpg",
  "content_type": "image/jpeg",
  "session_id": "session_1708185600000"
}
```

**Presigned URL Response** (WebSocket message):
```json
{
  "action": "presigned_url_response",
  "upload_url": "https://centli-frontend-bucket.s3.amazonaws.com/uploads/...",
  "image_url": "https://centli-frontend-bucket.s3.amazonaws.com/uploads/...",
  "expires_in": 300
}
```

**Rationale**: Direct S3 upload is more efficient than proxying through backend. Reduces backend load and latency.

---

### 4.4 Error Handling

**WebSocket Errors**:
- Connection failure: Auto-reconnect (5 attempts, exponential backoff)
- Message send failure: Queue message, retry on reconnect
- Timeout: 30 seconds, show error toast

**Image Upload Errors**:
- File too large: Show error before upload
- Upload failure: Retry button in error toast
- Presigned URL expired: Request new URL

**Network Errors**:
- Offline detection: Show "Sin conexión" message
- Reconnect button: Manual reconnect option

---

## 5. Deployment Architecture

### 5.1 Deployment Process

**Tool**: AWS CLI  
**Command**: `aws s3 sync`  
**Script**: `deploy-frontend.sh`

**Deployment Script**:
```bash
#!/bin/bash
# deploy-frontend.sh

BUCKET="centli-frontend-bucket"
PROFILE="777937796305_Ps-HackatonAgentic-Mexico"
REGION="us-east-1"

echo "Deploying frontend to S3..."

# Sync frontend files to S3
aws s3 sync frontend/ s3://$BUCKET/ \
  --exclude "*.md" \
  --exclude ".DS_Store" \
  --delete \
  --profile $PROFILE \
  --region $REGION

# Set cache headers
aws s3 cp s3://$BUCKET/index.html s3://$BUCKET/index.html \
  --metadata-directive REPLACE \
  --cache-control "max-age=0, no-cache" \
  --content-type "text/html" \
  --profile $PROFILE

aws s3 cp s3://$BUCKET/js/ s3://$BUCKET/js/ \
  --recursive \
  --metadata-directive REPLACE \
  --cache-control "max-age=3600" \
  --profile $PROFILE

echo "Deployment complete!"
echo "URL: http://$BUCKET.s3-website-$REGION.amazonaws.com"
```

**Deployment Steps**:
1. Run `./deploy-frontend.sh`
2. Wait for sync to complete (~10 seconds)
3. Test frontend URL
4. Run manual testing checklist

---

### 5.2 File Structure

**Frontend Directory**:
```
frontend/
├── index.html                      # Main HTML file
├── config.js                       # Configuration (WebSocket URL, etc.)
├── css/
│   └── custom.css                  # Custom styles
├── js/
│   ├── app.js                      # Main application
│   ├── websocket-manager.js        # WebSocket handling
│   ├── voice-manager.js            # Voice input/output
│   ├── chat-manager.js             # Chat interface
│   ├── image-manager.js            # Image upload
│   ├── transaction-manager.js      # Transaction confirmation
│   ├── product-catalog-manager.js  # Product catalog
│   ├── app-state.js                # State management
│   └── logger.js                   # Logging utility
└── README.md                       # Setup instructions
```

---

### 5.3 Environment Configuration

**Environments**: Single environment (production)

**Configuration Management**:
- `config.js` file with environment-specific values
- No build process, no environment variables
- Change config.js for different environments

**Development**:
- Local file:// or local HTTP server (python -m http.server)
- Edit files, refresh browser
- No build step

**Production**:
- Deploy to S3 with deploy-frontend.sh
- Access via S3 website URL

---

### 5.4 Rollback Strategy

**Approach**: Fix forward (no formal rollback)

**Rationale**: 
- Hackathon demo, fast iteration
- Git history available for recovery
- S3 versioning optional but not critical

**Recovery Options**:
1. Git checkout previous commit, redeploy
2. S3 versioning (if enabled)
3. Local backup of previous deployment

---

### 5.5 Testing Approach

**Manual Testing Checklist**:
```markdown
## Post-Deployment Testing

### Page Load
- [ ] Page loads successfully
- [ ] No console errors
- [ ] Bootstrap styles applied
- [ ] All JavaScript files loaded

### WebSocket Connection
- [ ] WebSocket connects on page load
- [ ] Connection status shows "Connected"
- [ ] Can send test message
- [ ] Receives echo response

### Voice Input
- [ ] Microphone permission requested
- [ ] Recording starts on button press
- [ ] Recording indicator shows
- [ ] Recording stops on button release
- [ ] Audio sent to backend

### Voice Output
- [ ] Receives audio from backend
- [ ] Audio plays automatically
- [ ] Playback controls work

### Chat Interface
- [ ] Can send text message
- [ ] Message appears in chat
- [ ] Receives response from agent
- [ ] Auto-scrolls to latest message

### Image Upload
- [ ] File picker opens
- [ ] Image preview shows
- [ ] Upload progress displays
- [ ] Image uploaded successfully

### Error Handling
- [ ] Disconnect WebSocket, auto-reconnects
- [ ] Upload large file, shows error
- [ ] Network offline, shows error message

### Mobile Testing
- [ ] Responsive on mobile (320px)
- [ ] Touch interactions work
- [ ] Voice works on mobile browser
```

---

## 6. Monitoring and Observability

### 6.1 Logging

**Approach**: Console logging only

**Log Categories**:
- `[WebSocket]` - Connection events, messages
- `[Voice]` - Recording, playback events
- `[Chat]` - Message send/receive
- `[Image]` - Upload progress, errors
- `[Error]` - All errors with stack traces

**Example Logs**:
```javascript
Logger.log('WebSocket', 'Connected successfully');
Logger.log('Voice', 'Recording started');
Logger.error('Image', 'Upload failed', error);
```

---

### 6.2 Monitoring

**Approach**: No external monitoring

**Rationale**: 
- Hackathon demo, console logs sufficient
- Browser DevTools for debugging
- No time for monitoring setup

**Optional** (if time permits):
- S3 access logs (track page views)
- CloudWatch RUM (real user monitoring)

---

## 7. Security

### 7.1 CORS Configuration

**Configuration**: Permissive (allow all origins)

**Rationale**: Demo context, internal hackathon, no sensitive data

**Production Recommendation**: Restrict origins to specific domains

---

### 7.2 Content Security Policy

**Approach**: No CSP for demo

**Rationale**: Simplifies development, Bootstrap CDN allowed by default

**Production Recommendation**: Implement CSP to whitelist CDN sources

---

### 7.3 HTTPS

**Current**: HTTP (S3 website endpoint)

**Fallback**: HTTPS (S3 object endpoint) if browser blocks WSS from HTTP origin

**Production Recommendation**: CloudFront with custom domain and SSL certificate

---

### 7.4 Secrets Management

**Approach**: Hardcoded in config.js

**Rationale**: No real secrets (WebSocket URL, bucket names are public)

**Production Recommendation**: Use environment variables or AWS Secrets Manager

---

## 8. Cost Estimation

### 8.1 S3 Costs

**Storage**: ~1 GB (frontend files + uploads)  
**Requests**: ~1000 GET requests (demo traffic)  
**Data Transfer**: ~10 GB out (demo traffic)

**Estimated Cost**: < $1 for demo period

---

### 8.2 Total Infrastructure Cost

**Unit 4 Only**: < $1 (S3 only)  
**Combined with Unit 1 & 2**: ~$5-10 for demo period

---

## 9. Infrastructure Dependencies

### 9.1 Unit 1 Dependencies

**Required from Unit 1**:
- ✅ S3 bucket (centli-frontend-bucket) - Already created
- ✅ IAM role for S3 access - Already created

**Status**: Unit 1 infrastructure complete and deployed

---

### 9.2 Unit 2 Dependencies

**Required from Unit 2**:
- ✅ WebSocket API Gateway URL - Already deployed
- ✅ WebSocket connection handler - Already implemented
- ✅ Message processing Lambda - Already implemented

**Status**: Unit 2 infrastructure complete and deployed

---

### 9.3 Unit 3 Dependencies

**Required from Unit 3** (future):
- ⏳ Action Groups for transaction processing
- ⏳ Action Groups for product catalog
- ⏳ DynamoDB tables for business data

**Status**: Unit 3 in progress (another developer)

**Impact**: Frontend can be developed and tested with mock data before Unit 3 is complete

---

## 10. Deployment Checklist

### Pre-Deployment
- [ ] Frontend code complete
- [ ] config.js updated with correct WebSocket URL
- [ ] Manual testing complete locally
- [ ] S3 bucket exists (from Unit 1)
- [ ] S3 bucket policy allows public read

### Deployment
- [ ] Run `./deploy-frontend.sh`
- [ ] Verify files uploaded to S3
- [ ] Enable static website hosting on bucket
- [ ] Configure CORS on bucket
- [ ] Set lifecycle policy for uploads folder

### Post-Deployment
- [ ] Access frontend URL
- [ ] Run manual testing checklist
- [ ] Verify WebSocket connection
- [ ] Test voice input/output
- [ ] Test image upload
- [ ] Test on mobile device

### Demo Preparation
- [ ] Clear browser cache
- [ ] Test on demo machine
- [ ] Prepare demo script
- [ ] Have backup plan (local version)

---

## 11. Summary

### Infrastructure Components
- **Hosting**: S3 static website hosting
- **Storage**: S3 (same bucket, /uploads/ folder)
- **Integration**: WebSocket API Gateway (Unit 2)
- **Authentication**: Mock client-side tokens
- **Deployment**: AWS CLI (manual sync)
- **Monitoring**: Console logs only

### Key Decisions
- ✅ Use existing S3 bucket from Unit 1
- ✅ No CloudFront (saves setup time)
- ✅ Direct S3 uploads with presigned URLs
- ✅ Single environment (production)
- ✅ Manual deployment (fast, simple)
- ✅ No external monitoring (console only)

### Success Criteria
- ✅ Frontend accessible via S3 URL
- ✅ WebSocket connection established
- ✅ Voice input/output working
- ✅ Image upload working
- ✅ Responsive on mobile and desktop
- ✅ Deployment time < 5 minutes

---

**Document Status**: Complete  
**Next Stage**: Code Generation
