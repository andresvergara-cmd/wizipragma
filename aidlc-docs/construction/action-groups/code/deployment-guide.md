# Deployment Guide - Unit 3: Action Groups

## Document Information
- **Unit**: Unit 3 (Action Groups - Backend Services)
- **Stage**: Deployment
- **Created**: 2026-02-17
- **Status**: Ready for deployment

---

## Prerequisites

### AWS Configuration
```bash
# Configure AWS CLI
aws configure --profile 777937796305_Ps-HackatonAgentic-Mexico

# Verify configuration
aws sts get-caller-identity --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Required Tools
- AWS CLI (v2.x)
- AWS SAM CLI (v1.x)
- Python 3.11+
- boto3

---

## Deployment Steps

### Step 1: Validate SAM Template
```bash
sam validate \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

**Expected Output**: `template.yaml is a valid SAM Template`

---

### Step 2: Build Application
```bash
sam build \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**What it does**:
- Builds all Lambda functions
- Resolves dependencies from requirements.txt
- Prepares deployment package

**Expected Output**: `Build Succeeded`

---

### Step 3: Deploy to AWS
```bash
sam deploy \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --stack-name centli-hackathon \
  --capabilities CAPABILITY_NAMED_IAM \
  --no-confirm-changeset
```

**What it deploys**:
- 6 DynamoDB tables
- 9 Lambda functions
- 9 EventBridge rules
- 9 IAM roles
- CloudWatch Log Groups

**Expected Duration**: 5-7 minutes

---

### Step 4: Verify Deployment
```bash
# Check stack status
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Stacks[0].StackStatus'
```

**Expected Output**: `"CREATE_COMPLETE"` or `"UPDATE_COMPLETE"`

---

### Step 5: Get Stack Outputs
```bash
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Stacks[0].Outputs' \
  --output table
```

**Important Outputs**:
- WebSocketURL
- AccountsTableName
- TransactionsTableName
- ProductsTableName
- BeneficiariesTableName

---

### Step 6: Seed Demo Data
```bash
# Install boto3 if not already installed
pip install boto3

# Run all seed scripts
python scripts/seed_all.py
```

**What it seeds**:
- 3 demo accounts (checking, savings, credit)
- 3 demo products (laptop, iPhone, TV)
- 2 demo retailers (Liverpool, Best Buy)
- 3 demo beneficiaries

**Expected Output**: `✅ Seeding complete! 3/3 scripts succeeded.`

---

## Testing

### Test 1: Balance Query
```bash
# Invoke Lambda directly
sam local invoke CoreBankingBalanceFunction \
  --event events/balance_query.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Or publish to EventBridge
aws events put-events \
  --entries file://events/balance_query.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

**Expected**: Balance response event published

---

### Test 2: Transfer
```bash
aws events put-events \
  --entries file://events/transfer_request.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

**Expected**: Transfer completed, balances updated

---

### Test 3: Alias Resolution
```bash
aws events put-events \
  --entries file://events/alias_resolution_request.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

**Expected**: "mi hermano" resolved to Juan López

---

### Test 4: Purchase Flow (End-to-End)
```bash
# 1. Query catalog
aws events put-events \
  --entries file://events/catalog_query.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1

# 2. Check benefits
aws events put-events \
  --entries file://events/benefits_query.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1

# 3. Purchase product
aws events put-events \
  --entries file://events/purchase_request.json \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

**Expected**: Purchase flow with payment and confirmation

---

## Monitoring

### View Lambda Logs
```bash
# View all logs
sam logs --stack-name centli-hackathon --tail

# View specific Lambda
aws logs tail /aws/lambda/centli-core-banking-transfer \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

### Query Logs with Insights
```bash
# Find errors
aws logs start-query \
  --log-group-name /aws/lambda/centli-core-banking-transfer \
  --start-time $(date -u -d '10 minutes ago' +%s) \
  --end-time $(date -u +%s) \
  --query-string 'fields @timestamp, level, message | filter level = "ERROR" | sort @timestamp desc | limit 20' \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

---

## Troubleshooting

### Issue: Deployment Fails
**Solution**: Check CloudFormation events
```bash
aws cloudformation describe-stack-events \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --max-items 10
```

### Issue: Lambda Function Errors
**Solution**: Check CloudWatch Logs
```bash
aws logs tail /aws/lambda/FUNCTION_NAME \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

### Issue: DynamoDB Table Not Found
**Solution**: Verify table exists
```bash
aws dynamodb describe-table \
  --table-name centli-accounts \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

### Issue: EventBridge Events Not Routing
**Solution**: Check EventBridge rules
```bash
aws events list-rules \
  --event-bus-name centli-event-bus \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

---

## Cleanup

### Delete Stack
```bash
# Empty S3 bucket first (if any)
aws s3 rm s3://centli-assets-777937796305 --recursive \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Delete stack
sam delete \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --no-prompts
```

**Warning**: This deletes all resources and data!

---

## Quick Reference

### Useful Commands
```bash
# Build
sam build

# Deploy
sam deploy --profile 777937796305_Ps-HackatonAgentic-Mexico

# Logs
sam logs --stack-name centli-hackathon --tail

# Validate
sam validate

# Local invoke
sam local invoke FunctionName --event events/event.json
```

### Environment Variables
All Lambdas have these environment variables:
- `EVENT_BUS_NAME`: centli-event-bus
- `ACCOUNTS_TABLE`: centli-accounts
- `TRANSACTIONS_TABLE`: centli-transactions
- `PRODUCTS_TABLE`: centli-products
- `PURCHASES_TABLE`: centli-purchases
- `RETAILERS_TABLE`: centli-retailers
- `BENEFICIARIES_TABLE`: centli-beneficiaries
- `LOG_LEVEL`: INFO

---

**Document Status**: Complete  
**Ready for Deployment**: Yes  
**Estimated Deployment Time**: 10-15 minutes (including seeding)
