#!/bin/bash
# Comfi Unit Tests Runner
set -e

echo "🧪 Comfi - Unit Tests"
echo "====================="

# Set Python path
export PYTHONPATH="${PWD}/src_aws/app_message:${PWD}/src_aws/app_connect:${PWD}/src_aws/app_disconnect:${PWD}/src_aws"

# Run all unit tests
python3 -m pytest tests/unit/ -v --tb=short -p no:anyio

echo ""
echo "✅ All tests complete"
