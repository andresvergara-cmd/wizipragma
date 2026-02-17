# Shared Infrastructure - CENTLI

## Overview

This document catalogs all shared infrastructure resources provided by Unit 1 (Infrastructure Foundation) and describes how Units 2, 3, and 4 access and use these resources.

**Purpose**: Enable cross-unit integration and resource sharing  
**Scope**: All shared AWS resources across CENTLI units  
**Maintenance**: Managed by Unit 1 deployment

---

## Shared Resources Catalog

### 1. EventBridge Event Bus

**Resource Name**: `centli-event-bus`  
**Type**: AWS::Events::EventBus  
**ARN**: `arn:aws:events:us-east-1:777937796305:event-bus/centli-event-bus`  
**Purpose**: Event-driven communication between AgentCore and Action Groups

**Used By**:
- Unit 2 (AgentCore): Publishes ActionRequest events, subscribes to ActionResponse events
- Unit 3 (Action Groups): Subscribes to ActionRequest events, publishes ActionResponse events

**Access Pattern**:
```python
import boto3

events_client = boto3.client('events')

# Publish event
response = events_client.put_events(
    Entries=[
        {
            'Source': 'centli.agentcore',
            'DetailType': 'ActionRequest',
            'Detail': json.dumps({
                'action_type': 'TRANSFER',
                'action_data': {...},
                'user_id': 'user_carlos',
                'session_id': 'sess_123',
                'request_id': 'req_456'
            }),
            'EventBusName': 'centli-event-bus'
        }
    ]
)
```

**Event Schemas**: See [Integration Contracts](#integration-contracts) section

---

### 2. S3 Assets Bucket

**Resource Name**: `centli-assets-777937796305`  
**Type**: AWS::S3::Bucket  
**ARN**: `arn:aws:s3:::centli-assets-777937796305`  
**Purpose**: Storage for user-uploaded images and static assets

**Used By**:
- Unit 2 (AgentCore): Reads images for Nova Canvas processing
- Unit 4 (Frontend): Uploads images directly from browser

**Access Pattern**:

**Upload from Frontend** (presigned URL):
```javascript
// Frontend requests presigned URL from backend
const response = await fetch('/api/get-upload-url', {
    method: 'POST',
    body: JSON.stringify({ filename: 'image.jpg', contentType: 'image/jpeg' })
});
const { uploadUrl } = await response.json();

// Upload directly to S3
await fetch(uploadUrl, {
    method: 'PUT',
    body: imageFile,
    headers: { 'Content-Type': 'image/jpeg' }
});
```

**Read from Lambda**:
```python
import boto3

s3_client = boto3.client('s3')

# Get image
response = s3_client.get_object(
    Bucket='centli-assets-777937796305',
    Key=f'images/{user_id}/{timestamp}_{filename}'
)
image_data = response['Body'].read()
```

**Key Structure**:
- Images: `images/{user_id}/{timestamp}_{filename}`
- Static assets: `static/{asset_type}/{filename}`

**CORS Configuration**:
- Allowed Origins: `http://localhost:3000`, `http://localhost:8080`, `http://127.0.0.1:*`
- Allowed Methods: GET, PUT, POST, DELETE
- Allowed Headers: *
- Max Age: 3600 seconds

---

### 3. IAM Lambda Execution Role

**Resource Name**: `CentliLambdaExecutionRole`  
**Type**: AWS::IAM::Role  
**ARN**: `arn:aws:iam::777937796305:role/CentliLambdaExecutionRole`  
**Purpose**: Shared execution role for all Lambda functions

**Used By**:
- Unit 2 (AgentCore): All 3 Lambdas (Connect, Disconnect, Message)
- Unit 3 (Action Groups): All 3 Lambdas (Core Banking, Marketplace, CRM)

**Permissions Granted**:
- EventBridge: `events:PutEvents` on `centli-event-bus`
- DynamoDB: Full access to `centli-*` tables
- S3: Read/Write access to `centli-assets-777937796305`
- Bedrock: Invoke models and agents
- API Gateway: Manage WebSocket connections
- CloudWatch Logs: Write logs

**Usage in SAM Template**:
```yaml
MyLambdaFunction:
  Type: AWS::Serverless::Function
  Properties:
    Role: !GetAtt CentliLambdaExecutionRole.Arn
```

---

### 4. CloudWatch Log Group

**Resource Name**: `/aws/lambda/centli`  
**Type**: AWS::Logs::LogGroup  
**ARN**: `arn:aws:logs:us-east-1:777937796305:log-group:/aws/lambda/centli`  
**Purpose**: Centralized logging for all Lambda functions  
**Retention**: 7 days

**Used By**:
- Unit 2 (AgentCore): All Lambda logs
- Unit 3 (Action Groups): All Lambda logs

**Access Pattern**:
```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Structured logging
logger.info(json.dumps({
    'timestamp': datetime.utcnow().isoformat(),
    'level': 'INFO',
    'unit': 'agentcore',
    'function': 'message_handler',
    'message': 'Processing user message',
    'context': {
        'user_id': user_id,
        'session_id': session_id,
        'request_id': request_id
    }
}))
```

**Log Queries**: See [Monitoring](#monitoring) section

---

## Integration Contracts

### EventBridge Event Schemas

#### ActionRequest Event (AgentCore → Action Groups)

**Source**: `centli.agentcore`  
**DetailType**: `ActionRequest`

```json
{
  "source": "centli.agentcore",
  "detail-type": "ActionRequest",
  "detail": {
    "action_type": "TRANSFER | PURCHASE | QUERY_BENEFICIARY | QUERY_BALANCE | LIST_PRODUCTS",
    "action_data": {
      "user_id": "string",
      "amount": "number (optional)",
      "beneficiary_alias": "string (optional)",
      "product_id": "string (optional)",
      "to_account_number": "string (optional)",
      "concept": "string (optional)",
      "benefit_option": "dict (optional)",
      "payment_method": "string (optional)"
    },
    "user_id": "string",
    "session_id": "string",
    "request_id": "string (UUID)",
    "timestamp": "string (ISO 8601)"
  }
}
```

**Action Types**:
- `TRANSFER`: P2P transfer request
- `PURCHASE`: Product purchase request
- `QUERY_BENEFICIARY`: Search beneficiary by alias
- `QUERY_BALANCE`: Get account balance
- `LIST_PRODUCTS`: Get product catalog

---

#### ActionResponse Event (Action Groups → AgentCore)

**Source**: `centli.actiongroup.{corebanking|marketplace|crm}`  
**DetailType**: `ActionResponse`

```json
{
  "source": "centli.actiongroup.corebanking",
  "detail-type": "ActionResponse",
  "detail": {
    "request_id": "string (UUID - matches ActionRequest)",
    "success": true,
    "result": {
      "data": {
        "transaction_id": "string",
        "new_balance": "number",
        "message": "Transferencia exitosa"
      },
      "message": "Transfer completed successfully"
    },
    "timestamp": "string (ISO 8601)"
  }
}
```

**Error Response**:
```json
{
  "source": "centli.actiongroup.corebanking",
  "detail-type": "ActionResponse",
  "detail": {
    "request_id": "string (UUID)",
    "success": false,
    "error": "Insufficient funds",
    "timestamp": "string (ISO 8601)"
  }
}
```

---

#### PaymentRequest Event (Marketplace → Core Banking)

**Source**: `centli.actiongroup.marketplace`  
**DetailType**: `PaymentRequest`

```json
{
  "source": "centli.actiongroup.marketplace",
  "detail-type": "PaymentRequest",
  "detail": {
    "user_id": "string",
    "amount": "number",
    "purchase_id": "string",
    "payment_method": "DEBIT | CREDIT",
    "request_id": "string (UUID)",
    "timestamp": "string (ISO 8601)"
  }
}
```

---

## Access Patterns by Unit

### Unit 2: AgentCore & Orchestration

**Resources Used**:
- ✅ EventBridge Event Bus (publish/subscribe)
- ✅ S3 Assets Bucket (read images)
- ✅ IAM Lambda Execution Role (all Lambdas)
- ✅ CloudWatch Log Group (logging)

**Integration Points**:
1. **Publish ActionRequest** when user intent requires Action Group
2. **Subscribe to ActionResponse** to get Action Group results
3. **Read images from S3** for Nova Canvas processing
4. **Log to CloudWatch** for debugging and monitoring

**Code Example**:
```python
# Publish ActionRequest
events_client.put_events(
    Entries=[{
        'Source': 'centli.agentcore',
        'DetailType': 'ActionRequest',
        'Detail': json.dumps(action_request),
        'EventBusName': os.environ['EVENT_BUS_NAME']
    }]
)

# Read image from S3
s3_client.get_object(
    Bucket=os.environ['ASSETS_BUCKET_NAME'],
    Key=image_key
)
```

---

### Unit 3: Action Groups

**Resources Used**:
- ✅ EventBridge Event Bus (subscribe/publish)
- ✅ IAM Lambda Execution Role (all Lambdas)
- ✅ CloudWatch Log Group (logging)

**Integration Points**:
1. **Subscribe to ActionRequest** events from AgentCore
2. **Publish ActionResponse** events back to AgentCore
3. **Publish PaymentRequest** events (Marketplace → Core Banking)
4. **Log to CloudWatch** for debugging and monitoring

**Code Example**:
```python
# Lambda triggered by EventBridge ActionRequest
def lambda_handler(event, context):
    detail = event['detail']
    action_type = detail['action_type']
    request_id = detail['request_id']
    
    # Process action
    result = process_action(action_type, detail['action_data'])
    
    # Publish ActionResponse
    events_client.put_events(
        Entries=[{
            'Source': 'centli.actiongroup.corebanking',
            'DetailType': 'ActionResponse',
            'Detail': json.dumps({
                'request_id': request_id,
                'success': True,
                'result': result
            }),
            'EventBusName': os.environ['EVENT_BUS_NAME']
        }]
    )
```

---

### Unit 4: Frontend

**Resources Used**:
- ✅ S3 Assets Bucket (upload images)

**Integration Points**:
1. **Upload images to S3** using presigned URLs
2. **Connect to WebSocket API** (provided by Unit 2, not Unit 1)

**Code Example**:
```javascript
// Request presigned URL from backend
async function uploadImage(file) {
    const response = await fetch('/api/get-upload-url', {
        method: 'POST',
        body: JSON.stringify({
            filename: file.name,
            contentType: file.type
        })
    });
    const { uploadUrl, imageKey } = await response.json();
    
    // Upload to S3
    await fetch(uploadUrl, {
        method: 'PUT',
        body: file,
        headers: { 'Content-Type': file.type }
    });
    
    return imageKey;
}
```

---

## Environment Variables

All Lambda functions receive these environment variables from Unit 1:

```yaml
Environment:
  Variables:
    EVENT_BUS_NAME: centli-event-bus
    ASSETS_BUCKET_NAME: centli-assets-777937796305
    LOG_LEVEL: INFO
    AWS_ACCOUNT_ID: '777937796305'
    AWS_REGION: us-east-1
```

**Usage in Code**:
```python
import os

EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']
ASSETS_BUCKET_NAME = os.environ['ASSETS_BUCKET_NAME']
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
```

---

## Monitoring

### CloudWatch Metrics

**EventBridge Metrics**:
- `Invocations`: Number of events published
- `FailedInvocations`: Number of failed event deliveries
- `TriggeredRules`: Number of rules triggered

**S3 Metrics**:
- `NumberOfObjects`: Total objects in bucket
- `BucketSizeBytes`: Total bucket size
- `AllRequests`: Total requests to bucket

**Lambda Metrics** (via shared role):
- `Invocations`: Total Lambda invocations
- `Errors`: Total Lambda errors
- `Duration`: Lambda execution time

### CloudWatch Log Insights Queries

**Query 1: All Events Published**
```
fields @timestamp, detail.source, detail.detail-type, detail.detail.request_id
| filter detail.source like /centli/
| sort @timestamp desc
```

**Query 2: Failed Events**
```
fields @timestamp, detail.source, detail.detail.error
| filter detail.success = false
| sort @timestamp desc
```

**Query 3: S3 Upload Activity**
```
fields @timestamp, requestParameters.bucketName, requestParameters.key
| filter eventName = "PutObject"
| sort @timestamp desc
```

---

## Troubleshooting Guide

### Issue: Events Not Delivered

**Symptoms**: ActionRequest published but Action Group not triggered

**Possible Causes**:
1. Event pattern mismatch
2. EventBridge rule not created
3. Lambda not subscribed to event bus
4. IAM permissions missing

**Solutions**:
1. Verify event source and detail-type match rule pattern
2. Check EventBridge rules in AWS Console
3. Verify Lambda has EventBridge trigger configured
4. Check IAM role has `events:PutEvents` permission
5. Review CloudWatch Logs for Lambda invocation errors

**Debug Commands**:
```bash
# List EventBridge rules
aws events list-rules \
  --event-bus-name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1

# Describe specific rule
aws events describe-rule \
  --name <rule-name> \
  --event-bus-name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1

# List targets for rule
aws events list-targets-by-rule \
  --rule <rule-name> \
  --event-bus-name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

---

### Issue: S3 Upload Fails

**Symptoms**: Frontend can't upload images to S3

**Possible Causes**:
1. CORS configuration incorrect
2. Presigned URL expired
3. Bucket policy restrictive
4. Network connectivity issue

**Solutions**:
1. Verify CORS allows frontend origin
2. Check presigned URL expiration (default 15 minutes)
3. Review S3 bucket policy
4. Test with curl to isolate browser issue

**Debug Commands**:
```bash
# Get bucket CORS configuration
aws s3api get-bucket-cors \
  --bucket centli-assets-777937796305 \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1

# Test upload with curl
curl -X PUT \
  -H "Content-Type: image/jpeg" \
  --data-binary @test.jpg \
  "<presigned-url>"
```

---

### Issue: Lambda Permission Denied

**Symptoms**: Lambda can't access EventBridge/S3/DynamoDB

**Possible Causes**:
1. Lambda not using shared IAM role
2. IAM policy missing permissions
3. Resource ARN incorrect

**Solutions**:
1. Verify Lambda uses `CentliLambdaExecutionRole`
2. Check IAM role policies in AWS Console
3. Verify resource ARNs in policy statements
4. Review CloudWatch Logs for specific permission error

**Debug Commands**:
```bash
# Get Lambda function configuration
aws lambda get-function-configuration \
  --function-name <function-name> \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Role'

# Get IAM role policies
aws iam list-attached-role-policies \
  --role-name CentliLambdaExecutionRole \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

aws iam list-role-policies \
  --role-name CentliLambdaExecutionRole \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

---

## Best Practices

### EventBridge

✅ Always include `request_id` for correlation  
✅ Use structured event schemas  
✅ Include timestamps in ISO 8601 format  
✅ Handle event delivery failures gracefully  
✅ Log all published events for debugging

### S3

✅ Use presigned URLs for frontend uploads  
✅ Organize objects with clear key structure  
✅ Set appropriate content types  
✅ Clean up old images periodically (lifecycle policy)  
✅ Validate file types and sizes before upload

### IAM

✅ Use shared role for simplicity (hackathon)  
✅ Scope permissions to specific resources  
✅ Avoid wildcard (*) permissions where possible  
✅ Review CloudTrail for permission issues  
✅ Plan for separate roles in production

### CloudWatch Logs

✅ Use structured JSON logging  
✅ Include context (user_id, session_id, request_id)  
✅ Log at appropriate levels (ERROR, WARN, INFO, DEBUG)  
✅ Use Log Insights for querying  
✅ Set up alarms for critical errors

---

## Summary

Shared infrastructure from Unit 1 enables:
- ✅ Event-driven communication via EventBridge
- ✅ Image storage and retrieval via S3
- ✅ Unified permissions via shared IAM role
- ✅ Centralized logging via CloudWatch
- ✅ Clear integration contracts for all units
- ✅ Comprehensive troubleshooting guidance

**All units depend on these shared resources for successful integration.**

**Next Steps**: Units 2, 3, 4 will reference these resources during their Code Generation phases.
