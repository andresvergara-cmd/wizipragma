# Build Instructions - CENTLI

## Prerequisites

### Required Tools
- **AWS CLI**: Version 2.x or higher
- **AWS SAM CLI**: Version 1.100.0 or higher
- **Python**: 3.9 or 3.10
- **Poetry**: 1.7.0 or higher (Python dependency management)
- **Node.js**: 18.x or higher (for frontend build tools, optional)
- **Git**: For version control

### AWS Configuration
- **AWS Profile**: `777937796305_Ps-HackatonAgentic-Mexico`
- **AWS Region**: `us-east-1`
- **AWS Account ID**: `777937796305`

### Environment Variables
```bash
export AWS_PROFILE=777937796305_Ps-HackatonAgentic-Mexico
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=777937796305
export PROJECT_NAME=centli
```

### System Requirements
- **OS**: macOS, Linux, or Windows with WSL2
- **Memory**: Minimum 8GB RAM
- **Disk Space**: Minimum 2GB free space
- **Network**: Internet connection for AWS services

---

## Build Steps

### 1. Install Dependencies

#### Python Dependencies (Backend Lambdas)
```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Verify installation
poetry run python --version
```

#### AWS SAM CLI
```bash
# macOS
brew install aws-sam-cli

# Linux
pip install aws-sam-cli

# Verify installation
sam --version
```

### 2. Configure Environment

#### Set AWS Credentials
```bash
# Configure AWS CLI with your credentials
aws configure --profile 777937796305_Ps-HackatonAgentic-Mexico

# Verify AWS access
aws sts get-caller-identity --profile 777937796305_Ps-HackatonAgentic-Mexico
```

Expected output:
```json
{
    "UserId": "...",
    "Account": "777937796305",
    "Arn": "..."
}
```

#### Create Local Environment File
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your specific values
# (This file is gitignored)
```

### 3. Build All Units

#### Unit 1: Infrastructure Foundation
```bash
# Validate base template
sam validate --template infrastructure/base-template.yaml

# Build (no code to build, just validation)
echo "✅ Unit 1: Infrastructure validated"
```

#### Unit 2: AgentCore & Orchestration
```bash
# Build Lambda functions
sam build \
  --template template.yaml \
  --build-dir .aws-sam/build \
  --profile 777937796305_Ps-HackatonAgentic-Mexico

# Verify build artifacts
ls -la .aws-sam/build/
```

Expected output:
```
AppConnectFunction/
AppDisconnectFunction/
AppMessageFunction/
template.yaml
```

#### Unit 3: Action Groups (When Ready)
```bash
# Build Action Group Lambdas
sam build \
  --template infrastructure/action-groups-template.yaml \
  --build-dir .aws-sam/build-action-groups \
  --profile 777937796305_Ps-HackatonAgentic-Mexico
```

#### Unit 4: Frontend (When Ready)
```bash
# No build step required for static HTML/CSS/JS
# Validate HTML syntax
echo "✅ Unit 4: Frontend files ready for deployment"
```

### 4. Verify Build Success

#### Check Build Artifacts
```bash
# List all build artifacts
find .aws-sam/build -type f -name "*.py" | head -10

# Check Lambda function sizes
du -sh .aws-sam/build/*/
```

#### Expected Output
- **Build Status**: SUCCESS
- **Build Artifacts**:
  - `.aws-sam/build/AppConnectFunction/` - WebSocket connect handler
  - `.aws-sam/build/AppDisconnectFunction/` - WebSocket disconnect handler
  - `.aws-sam/build/AppMessageFunction/` - WebSocket message handler
  - `.aws-sam/build/template.yaml` - Processed SAM template

#### Common Warnings (Acceptable)
- `WARNING: Skipping build for function X (no code changes)` - OK if function already built
- `WARNING: Using Python 3.9 runtime` - OK, this is our target runtime

---

## Troubleshooting

### Build Fails with Dependency Errors

**Symptom**: `ModuleNotFoundError` or `ImportError` during build

**Cause**: Missing Python dependencies or Poetry not configured

**Solution**:
```bash
# Reinstall dependencies
poetry install --no-root

# Clear Poetry cache
poetry cache clear pypi --all

# Rebuild
sam build --use-container
```

### Build Fails with SAM Template Errors

**Symptom**: `Template validation error` or `Invalid template`

**Cause**: Syntax error in YAML template

**Solution**:
```bash
# Validate template syntax
sam validate --template template.yaml --lint

# Check for YAML syntax errors
python -c "import yaml; yaml.safe_load(open('template.yaml'))"

# Fix errors and rebuild
```

### Build Fails with Permission Errors

**Symptom**: `Access Denied` or `Permission denied`

**Cause**: AWS credentials not configured or insufficient permissions

**Solution**:
```bash
# Verify AWS credentials
aws sts get-caller-identity --profile 777937796305_Ps-HackatonAgentic-Mexico

# Check IAM permissions (need Lambda, S3, DynamoDB, EventBridge access)
aws iam get-user --profile 777937796305_Ps-HackatonAgentic-Mexico

# Reconfigure credentials if needed
aws configure --profile 777937796305_Ps-HackatonAgentic-Mexico
```

### Build is Slow

**Symptom**: Build takes more than 5 minutes

**Cause**: Large dependencies or network issues

**Solution**:
```bash
# Use container build for faster dependency resolution
sam build --use-container --parallel

# Or use cached build
sam build --cached
```

---

## Build Optimization Tips

### 1. Use Cached Builds
```bash
# Enable caching for faster subsequent builds
sam build --cached --parallel
```

### 2. Build Specific Functions
```bash
# Build only changed functions
sam build AppMessageFunction --use-container
```

### 3. Use Container Builds
```bash
# Build in Docker container (consistent environment)
sam build --use-container
```

### 4. Parallel Builds
```bash
# Build multiple functions in parallel
sam build --parallel
```

---

## Build Verification Checklist

- [ ] Poetry dependencies installed successfully
- [ ] AWS SAM CLI installed and configured
- [ ] AWS credentials configured and verified
- [ ] Base template validated (Unit 1)
- [ ] Lambda functions built successfully (Unit 2)
- [ ] Build artifacts present in `.aws-sam/build/`
- [ ] No critical errors in build output
- [ ] Lambda function sizes are reasonable (<50MB each)

---

## Next Steps

After successful build:
1. ✅ Proceed to **Unit Test Execution** (unit-test-instructions.md)
2. ✅ Deploy to AWS (see DEPLOYMENT-UNIT2.md)
3. ✅ Run integration tests (integration-test-instructions.md)

---

**Build Time**: ~2-5 minutes (first build), ~30 seconds (cached builds)  
**Build Artifacts Location**: `.aws-sam/build/`  
**Build Status**: Ready for deployment
