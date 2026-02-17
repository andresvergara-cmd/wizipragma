# Deployment Architecture - Unit 4: Frontend Multimodal UI

## Document Information
- **Unit**: Frontend Multimodal UI
- **Created**: 2026-02-17
- **Context**: 8-hour hackathon, demo quality
- **Cloud Provider**: AWS
- **Region**: us-east-1

---

## 1. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER DEVICES                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Desktop    │  │    Mobile    │  │    Tablet    │          │
│  │   Browser    │  │   Browser    │  │   Browser    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │ HTTP/HTTPS       │                  │
          │ (Static Files)   │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AWS CLOUD (us-east-1)                       │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Amazon S3 Bucket                         │ │
│  │              centli-frontend-bucket                         │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │ │
│  │  │  index.html  │  │  config.js   │  │   /uploads/     │  │ │
│  │  │  (Main App)  │  │  (Config)    │  │  (User Images)  │  │ │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘  │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐                        │ │
│  │  │   /css/      │  │    /js/      │                        │ │
│  │  │  (Styles)    │  │  (Scripts)   │                        │ │
│  │  └──────────────┘  └──────────────┘                        │ │
│  │                                                              │ │
│  │  Static Website Hosting: Enabled                            │ │
│  │  Public Access: Allowed                                     │ │
│  │  CORS: Enabled                                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│         │                                                         │
│         │ WSS (WebSocket Secure)                                 │
│         │ wss://vvg621xawg.execute-api.us-east-1.amazonaws.com  │
│         ▼                                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              API Gateway (WebSocket)                        │ │
│  │                    (Unit 2)                                 │ │
│  │                                                              │ │
│  │  Routes:                                                     │ │
│  │  - $connect    → app_connect Lambda                         │ │
│  │  - $disconnect → app_disconnect Lambda                      │ │
│  │  - $default    → app_message Lambda                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│         │                                                         │
│         │ Invoke                                                  │
│         ▼                                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  AWS Lambda Functions                       │ │
│  │                      (Unit 2)                               │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│  │  │app_connect   │  │app_disconnect│  │ app_message  │     │ │
│  │  │(Session      │  │(Session      │  │(Bedrock      │     │ │
│  │  │ Create)      │  │ Cleanup)     │  │ Agent)       │     │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│         │                                                         │
│         │ Read/Write                                              │
│         ▼                                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Amazon DynamoDB                          │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  centli-sessions                                      │  │ │
│  │  │  (WebSocket connection tracking)                      │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│         │                                                         │
│         │ Invoke                                                  │
│         ▼                                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  Amazon Bedrock                             │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Agent: centli-agentcore (Z6PCEKYNPS)                │  │ │
│  │  │  Model: Claude 3.5 Sonnet v2                         │  │ │
│  │  │  Alias: prod (BRUXPV975I)                            │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Interactions

### 2.1 Page Load Flow

```
User Browser
    │
    │ 1. HTTP GET index.html
    ▼
S3 Bucket (Static Website)
    │
    │ 2. Return HTML + CSS + JS
    ▼
User Browser
    │
    │ 3. Parse HTML, load Bootstrap CDN
    │ 4. Execute JavaScript (app.js)
    │ 5. Read config.js (WebSocket URL)
    │
    │ 6. Establish WebSocket connection
    ▼
API Gateway (WebSocket)
    │
    │ 7. Trigger $connect route
    ▼
Lambda (app_connect)
    │
    │ 8. Create session in DynamoDB
    ▼
DynamoDB (centli-sessions)
    │
    │ 9. Return connection_id
    ▼
User Browser
    │
    │ 10. Display "Connected" status
    │ 11. Enable chat input
    │
```

---

### 2.2 Text Message Flow

```
User Browser
    │
    │ 1. User types message, clicks send
    │ 2. WebSocket.send(JSON message)
    ▼
API Gateway (WebSocket)
    │
    │ 3. Trigger $default route
    ▼
Lambda (app_message)
    │
    │ 4. Parse message
    │ 5. Invoke Bedrock Agent
    ▼
Bedrock Agent (centli-agentcore)
    │
    │ 6. Process with Claude 3.5 Sonnet
    │ 7. Generate response
    ▼
Lambda (app_message)
    │
    │ 8. Format response
    │ 9. Send via WebSocket
    ▼
API Gateway (WebSocket)
    │
    │ 10. Push to connection_id
    ▼
User Browser
    │
    │ 11. Display response in chat
    │
```

---

### 2.3 Voice Input Flow

```
User Browser
    │
    │ 1. User presses voice button
    │ 2. Request microphone permission
    │ 3. Start MediaRecorder
    │ 4. Record audio (WebM format)
    │ 5. User releases button
    │ 6. Stop MediaRecorder
    │ 7. Convert to Blob
    │ 8. Base64 encode audio
    │ 9. Send via WebSocket
    ▼
API Gateway (WebSocket)
    │
    │ 10. Trigger $default route
    ▼
Lambda (app_message)
    │
    │ 11. Decode base64 audio
    │ 12. Send to Bedrock Agent (Nova Sonic)
    │ 13. Transcribe audio to text
    │ 14. Process with Claude
    │ 15. Generate text response
    │ 16. Convert to audio (Nova Sonic)
    │ 17. Base64 encode audio
    │ 18. Send via WebSocket
    ▼
User Browser
    │
    │ 19. Decode base64 audio
    │ 20. Create Audio element
    │ 21. Play audio response
    │
```

---

### 2.4 Image Upload Flow

```
User Browser
    │
    │ 1. User selects image
    │ 2. Show preview
    │ 3. Compress image (Canvas API)
    │ 4. Request presigned URL
    │ 5. Send request via WebSocket
    ▼
API Gateway (WebSocket)
    │
    │ 6. Trigger $default route
    ▼
Lambda (app_message)
    │
    │ 7. Generate S3 presigned URL
    │ 8. Return URL via WebSocket
    ▼
User Browser
    │
    │ 9. Receive presigned URL
    │ 10. HTTP PUT image to S3
    ▼
S3 Bucket (/uploads/)
    │
    │ 11. Store image
    │ 12. Return success
    ▼
User Browser
    │
    │ 13. Send image URL via WebSocket
    ▼
Lambda (app_message)
    │
    │ 14. Send image URL to Bedrock (Nova Canvas)
    │ 15. Process image
    │ 16. Generate response
    │ 17. Send via WebSocket
    ▼
User Browser
    │
    │ 18. Display response
    │
```

---

## 3. Deployment Flow

### 3.1 Initial Setup (One-Time)

```
Developer Machine
    │
    │ 1. Verify S3 bucket exists (Unit 1)
    │ 2. Enable static website hosting
    │ 3. Configure bucket policy (public read)
    │ 4. Configure CORS
    │ 5. Set lifecycle policy (uploads/)
    │
    │ AWS CLI commands:
    │ aws s3 website s3://centli-frontend-bucket/ \
    │   --index-document index.html \
    │   --error-document index.html
    │
    │ aws s3api put-bucket-policy \
    │   --bucket centli-frontend-bucket \
    │   --policy file://bucket-policy.json
    │
    │ aws s3api put-bucket-cors \
    │   --bucket centli-frontend-bucket \
    │   --cors-configuration file://cors-config.json
    │
```

---

### 3.2 Code Deployment (Repeatable)

```
Developer Machine
    │
    │ 1. Update frontend code
    │ 2. Update config.js (if needed)
    │ 3. Test locally
    │
    │ 4. Run deployment script
    │    ./deploy-frontend.sh
    │
    ▼
AWS CLI
    │
    │ 5. Sync files to S3
    │    aws s3 sync frontend/ s3://centli-frontend-bucket/
    │
    │ 6. Set cache headers
    │    - index.html: no-cache
    │    - JS/CSS: max-age=3600
    │
    ▼
S3 Bucket
    │
    │ 7. Files updated
    │ 8. Immediately available
    │
    ▼
Developer Machine
    │
    │ 9. Access frontend URL
    │ 10. Run manual testing checklist
    │ 11. Verify functionality
    │
```

---

## 4. Network Architecture

### 4.1 Network Flow

```
Internet
    │
    │ HTTPS/HTTP
    ▼
┌─────────────────────────────────────────┐
│         AWS Edge Locations              │
│         (S3 Global Network)             │
└─────────────────────────────────────────┘
    │
    │ Route to nearest region
    ▼
┌─────────────────────────────────────────┐
│         AWS Region: us-east-1           │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │         S3 Bucket                  │ │
│  │   centli-frontend-bucket           │ │
│  │   (Static Website Hosting)         │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │    API Gateway (WebSocket)         │ │
│  │    wss://vvg621xawg...             │ │
│  └────────────────────────────────────┘ │
│                                          │
└─────────────────────────────────────────┘
```

### 4.2 Security Groups

**Not Applicable**: S3 and API Gateway are managed services with built-in security.

---

## 5. Scalability Architecture

### 5.1 Auto-Scaling

**S3**: Automatically scales to handle any number of requests  
**API Gateway**: Automatically scales to handle concurrent connections  
**Lambda**: Automatically scales based on invocations

**No manual scaling configuration needed.**

---

### 5.2 Performance Optimization

**S3**:
- Static files cached by browsers (Cache-Control headers)
- Gzip compression enabled by default
- Global edge locations for fast delivery

**Frontend**:
- Minimal dependencies (Bootstrap CDN only)
- No build process (no bundle size issues)
- Lazy loading for non-critical features

---

## 6. High Availability Architecture

### 6.1 Availability Zones

**S3**: Automatically replicated across multiple AZs in us-east-1  
**API Gateway**: Multi-AZ by default  
**Lambda**: Multi-AZ by default

**No manual HA configuration needed.**

---

### 6.2 Disaster Recovery

**RTO** (Recovery Time Objective): < 5 minutes  
**RPO** (Recovery Point Objective): 0 (no data loss)

**Recovery Process**:
1. Redeploy frontend from Git repository
2. Run `./deploy-frontend.sh`
3. Verify deployment

**Backup Strategy**:
- Git repository (source code)
- S3 versioning (optional, for uploaded images)

---

## 7. Monitoring Architecture

### 7.1 Logging

**Frontend Logs**: Browser console only  
**S3 Access Logs**: Optional (not enabled for demo)  
**API Gateway Logs**: CloudWatch (from Unit 2)  
**Lambda Logs**: CloudWatch (from Unit 2)

---

### 7.2 Metrics

**S3 Metrics**: 
- Request count
- Error rate
- Data transfer

**API Gateway Metrics** (from Unit 2):
- Connection count
- Message count
- Error rate

**Lambda Metrics** (from Unit 2):
- Invocation count
- Duration
- Error rate

---

## 8. Cost Architecture

### 8.1 Cost Breakdown

**S3**:
- Storage: $0.023/GB/month × 1 GB = $0.023/month
- GET requests: $0.0004/1000 × 1000 = $0.0004
- Data transfer: $0.09/GB × 10 GB = $0.90

**Total Unit 4 Cost**: ~$1/month for demo

---

### 8.2 Cost Optimization

**Strategies**:
- Lifecycle policy (auto-delete uploads after 24 hours)
- No CloudFront (saves $0.50/month minimum)
- No monitoring services (saves $10+/month)
- Single environment (no dev/staging costs)

---

## 9. Security Architecture

### 9.1 Security Layers

```
┌─────────────────────────────────────────┐
│         User Browser                     │
│  - HTTPS (optional)                      │
│  - WSS (WebSocket Secure)                │
│  - Content Security Policy (optional)    │
└─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│         AWS Edge / Network               │
│  - DDoS protection (AWS Shield)          │
│  - TLS 1.2+ (API Gateway)                │
└─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│         Application Layer                │
│  - CORS (S3 bucket)                      │
│  - Bucket policy (public read only)      │
│  - IAM roles (Lambda execution)          │
└─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│         Data Layer                       │
│  - Encryption at rest (S3, DynamoDB)     │
│  - Encryption in transit (TLS)           │
└─────────────────────────────────────────┘
```

---

### 9.2 IAM Roles

**S3 Bucket Policy**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::centli-frontend-bucket/*"
    }
  ]
}
```

**Lambda Execution Role** (from Unit 2):
- S3 read/write (for presigned URLs)
- DynamoDB read/write (for sessions)
- Bedrock invoke (for AI processing)
- CloudWatch logs write

---

## 10. Deployment Environments

### 10.1 Environment Matrix

| Environment | S3 Bucket | WebSocket URL | Purpose |
|-------------|-----------|---------------|---------|
| **Production** | centli-frontend-bucket | wss://vvg621xawg...amazonaws.com/prod | Demo |

**Note**: Single environment for hackathon. No dev/staging environments.

---

### 10.2 Configuration Management

**config.js** (production):
```javascript
const CONFIG = {
  WS_URL: 'wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod',
  S3_BUCKET: 'centli-frontend-bucket',
  S3_REGION: 'us-east-1',
  API_TIMEOUT: 30000,
  MAX_IMAGE_SIZE: 5242880, // 5MB
  MAX_RECORDING_DURATION: 30000 // 30 seconds
};
```

---

## 11. Summary

### Architecture Characteristics
- **Serverless**: No servers to manage
- **Scalable**: Auto-scales with demand
- **Available**: Multi-AZ by default
- **Simple**: Minimal components
- **Cost-effective**: Pay-per-use, ~$1/month

### Key Components
- S3 static website hosting (frontend files)
- S3 storage (/uploads/ for images)
- API Gateway WebSocket (backend communication)
- Lambda functions (message processing)
- DynamoDB (session storage)
- Bedrock Agent (AI processing)

### Deployment Process
1. One-time S3 bucket setup
2. Repeatable deployment script
3. Manual testing checklist
4. Ready for demo in < 5 minutes

---

**Document Status**: Complete  
**Next Stage**: Code Generation
