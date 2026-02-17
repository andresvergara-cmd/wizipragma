# CENTLI - Multimodal Banking Assistant

CENTLI is an AI-powered multimodal banking assistant built for a hackathon, enabling users to perform banking operations through voice, text, and images using AWS Bedrock AgentCore.

## Overview

CENTLI transforms traditional banking interactions into natural, conversational experiences. Users can:
- Transfer money by voice: "Envíale 50 lucas a mi hermano"
- Browse and purchase products with benefits comparison
- Upload images for analysis (receipts, products)
- Interact via text, voice, or images seamlessly

## Architecture

CENTLI is built on AWS serverless architecture with 4 main units:

### Unit 1: Infrastructure Foundation
- EventBridge Event Bus for event-driven communication
- S3 bucket for image storage
- IAM roles and policies
- CloudWatch Logs for monitoring

### Unit 2: AgentCore & Orchestration
- AWS Bedrock AgentCore with Claude 3.7 Sonnet
- Nova Sonic for voice processing (STT/TTS)
- Nova Canvas for image analysis
- WebSocket API for real-time communication
- 3 Lambda functions (Connect, Disconnect, Message)

### Unit 3: Action Groups
- Core Banking Mock (accounts, transfers, transactions)
- Marketplace Mock (products, benefits, purchases)
- CRM Mock (beneficiaries, alias resolution)
- 6 DynamoDB tables for business data

### Unit 4: Frontend Multimodal UI
- HTML/CSS/JavaScript (vanilla, no frameworks)
- WebSocket client for real-time communication
- Voice input/output using browser APIs
- Image upload functionality
- Responsive mobile-first design

## Technology Stack

- **AWS Services**: Lambda, API Gateway, EventBridge, S3, DynamoDB, CloudWatch
- **AI/ML**: AWS Bedrock (AgentCore, Nova Sonic, Nova Canvas, Claude 3.7 Sonnet)
- **Infrastructure**: AWS SAM (Serverless Application Model)
- **Backend**: Python 3.9
- **Frontend**: HTML5, CSS3, JavaScript ES6+

## Prerequisites

Before deploying CENTLI, ensure you have:

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
   ```bash
   aws --version
   ```
3. **AWS SAM CLI** installed
   ```bash
   sam --version
   ```
4. **Python 3.9+** installed
   ```bash
   python --version
   ```
5. **Poetry** (optional, for dependency management)
   ```bash
   poetry --version
   ```

## Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd PoC-Wizi-Mex
```

### 2. Configure AWS Credentials

```bash
aws configure --profile 777937796305_Ps-HackatonAgentic-Mexico
```

Enter your AWS credentials when prompted.

### 3. Deploy Infrastructure

```bash
# Option 1: Using deployment script (recommended)
./commands/deploy-infrastructure.sh

# Option 2: Using SAM CLI directly
sam build
sam deploy
```

The deployment script will:
- Validate AWS credentials
- Validate SAM template
- Build the application
- Deploy to AWS
- Display stack outputs

### 4. Verify Deployment

After deployment, verify the stack status:

```bash
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Stacks[0].StackStatus'
```

Expected output: `CREATE_COMPLETE`

### 5. Get Stack Outputs

Retrieve important resource identifiers:

```bash
aws cloudformation describe-stacks \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --query 'Stacks[0].Outputs' \
  --output table
```

## Project Structure

```
PoC-Wizi-Mex/
├── template.yaml                 # SAM template (infrastructure as code)
├── samconfig.toml               # SAM deployment configuration
├── commands/
│   ├── deploy-infrastructure.sh # Automated deployment script
│   └── cleanup-infrastructure.sh # Automated cleanup script
├── src_aws/                     # Lambda function code (Units 2, 3)
│   ├── app_connect/            # WebSocket connect handler
│   ├── app_disconnect/         # WebSocket disconnect handler
│   ├── app_message/            # WebSocket message handler
│   ├── core_banking/           # Core Banking Action Group
│   ├── marketplace/            # Marketplace Action Group
│   └── crm/                    # CRM Action Group
├── frontend/                    # Frontend code (Unit 4)
│   ├── index.html
│   ├── css/
│   └── js/
├── data/                        # Mock data for seeding
├── aidlc-docs/                  # AI-DLC documentation
│   ├── inception/              # Requirements, stories, design
│   └── construction/           # Implementation artifacts
├── pyproject.toml              # Python dependencies
└── README.md                   # This file
```

## Development Workflow

### Local Testing

```bash
# Validate SAM template
sam validate

# Build application
sam build

# Run local API (if applicable)
sam local start-api
```

### Update Deployment

After making changes:

```bash
sam build && sam deploy
```

### View Logs

```bash
# View all Lambda logs
sam logs --stack-name centli-hackathon --tail

# View specific function logs
sam logs -n ConnectFunction --stack-name centli-hackathon --tail
```

## Cleanup

To remove all CENTLI infrastructure from AWS:

```bash
./commands/cleanup-infrastructure.sh
```

This will:
- Empty the S3 bucket
- Delete the CloudFormation stack
- Remove all resources

**Warning**: This action is irreversible. All data will be lost.

## Demo Scenarios

### Scenario 1: Voice Transfer
1. User speaks: "Envíale 50 lucas a mi hermano"
2. System transcribes voice to text
3. AgentCore recognizes TRANSFER intent
4. CRM resolves "mi hermano" to Juan López
5. Core Banking executes transfer
6. System responds with voice: "Listo, le envié $50,000 a Juan López"

### Scenario 2: Product Purchase
1. User types: "Quiero comprar una laptop"
2. System shows product catalog with benefits
3. User selects laptop and MSI 6 months option
4. System confirms purchase details
5. Marketplace executes purchase
6. Core Banking processes payment
7. System displays receipt

## Cost Estimation

Estimated costs for hackathon usage (8 hours):

| Service | Estimated Cost |
|---------|---------------|
| Lambda | $0.00 (free tier) |
| API Gateway | $0.00 (free tier) |
| DynamoDB | $0.00 (free tier) |
| S3 | $0.00 (free tier) |
| EventBridge | $0.00 (free tier) |
| CloudWatch Logs | $0.50 |
| Bedrock AgentCore | $5.00 |
| Bedrock Nova Sonic | $2.00 |
| Bedrock Nova Canvas | $1.00 |
| **Total** | **~$8.50** |

Most services stay within AWS free tier for hackathon usage.

## Troubleshooting

### Issue: Deployment Fails

**Solution**: Check CloudFormation events in AWS Console for specific error.

```bash
aws cloudformation describe-stack-events \
  --stack-name centli-hackathon \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1 \
  --max-items 10
```

### Issue: Lambda Function Errors

**Solution**: Check CloudWatch Logs for detailed error messages.

```bash
aws logs tail /aws/lambda/centli \
  --follow \
  --profile 777937796305_Ps-HackatonAgentic-Mexico \
  --region us-east-1
```

### Issue: S3 Bucket Already Exists

**Solution**: S3 bucket names must be globally unique. The template uses your AWS Account ID to ensure uniqueness.

## Documentation

Comprehensive documentation is available in the `aidlc-docs/` directory:

- **Inception Phase**: Requirements, user stories, architecture design
- **Construction Phase**: Infrastructure design, code summaries, deployment guides
- **Shared Infrastructure**: Integration contracts, access patterns, troubleshooting

Key documents:
- [Infrastructure Design](aidlc-docs/construction/infrastructure-foundation/infrastructure-design/infrastructure-design.md)
- [Deployment Architecture](aidlc-docs/construction/infrastructure-foundation/infrastructure-design/deployment-architecture.md)
- [Shared Infrastructure](aidlc-docs/construction/shared-infrastructure.md)
- [Code Summary](aidlc-docs/construction/infrastructure-foundation/code/infrastructure-code-summary.md)

## Contributing

This is a hackathon project. For questions or issues, please contact the CENTLI team.

## License

[Add license information]

## Acknowledgments

- AWS Bedrock team for AgentCore, Nova Sonic, and Nova Canvas
- Hackathon organizers and participants
- CENTLI development team

---

**Built with ❤️ for the AWS Bedrock Hackathon**
