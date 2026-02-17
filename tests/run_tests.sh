#!/bin/bash
# Script to run CENTLI Unit 2 tests
# Usage: ./tests/run_tests.sh

set -e

echo "🧪 CENTLI Unit 2 - Test Runner"
echo "================================"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest not found. Installing..."
    pip3 install pytest pytest-cov pytest-mock --quiet
    echo "✅ pytest installed"
fi

# Set Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/src_aws"

echo "📦 Python path: $PYTHONPATH"
echo ""

# Run tests
echo "🏃 Running Unit 2 tests..."
echo ""

# Test app_connect
echo "Testing app_connect..."
python3 -m pytest tests/unit/test_app_connect.py -v --tb=short || true

echo ""
echo "Testing app_disconnect..."
python3 -m pytest tests/unit/test_app_disconnect.py -v --tb=short || true

echo ""
echo "Testing app_message..."
python3 -m pytest tests/unit/test_app_message.py -v --tb=short || true

echo ""
echo "================================"
echo "✅ Test execution complete"
echo ""
echo "To run with coverage:"
echo "  python3 -m pytest tests/unit/ --cov=src_aws --cov-report=html"
echo ""
echo "To view coverage report:"
echo "  open htmlcov/index.html"
