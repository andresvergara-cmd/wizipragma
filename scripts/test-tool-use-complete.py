#!/usr/bin/env python3
"""
Test Tool Use - Complete Validation
Tests transfer and purchase flows end-to-end
"""

import asyncio
import websockets
import json
import sys
import ssl
from datetime import datetime

# Configuration
WS_URL = "wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"
USER_ID = "simple-user"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def print_message(role, text):
    color = Colors.BLUE if role == "user" else Colors.GREEN
    print(f"{color}{role.upper()}: {text}{Colors.END}")

async def test_transfer():
    """Test money transfer flow"""
    print_header("TEST 1: Money Transfer")
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with websockets.connect(WS_URL, ssl=ssl_context) as websocket:
            # Send connection message (not needed, just send actual message)
            # Send transfer request
            transfer_msg = {
                "action": "sendMessage",
                "data": {
                    "user_id": USER_ID,
                    "session_id": f"test-{datetime.now().timestamp()}",
                    "type": "TEXT",
                    "message": "Envía $500 a mi mamá"
                }
            }
            print_message("user", "Envía $500 a mi mamá")
            await websocket.send(json.dumps(transfer_msg))
            
            # Collect response
            response_text = ""
            timeout_count = 0
            max_timeout = 30  # 30 seconds max
            
            while timeout_count < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    chunk = response
                    response_text += chunk
                    print(chunk, end='', flush=True)
                    timeout_count = 0  # Reset on successful receive
                except asyncio.TimeoutError:
                    timeout_count += 1
                    if timeout_count >= 3:  # 3 seconds without data = done
                        break
            
            print("\n")
            
            # Validate response
            if "TRF-" in response_text or "transferencia" in response_text.lower():
                print_success("Transfer flow completed")
                if "TRF-" in response_text:
                    print_success("Transaction ID found in response")
                return True
            else:
                print_error("Transfer flow failed - no transaction confirmation")
                return False
                
    except Exception as e:
        print_error(f"Transfer test failed: {str(e)}")
        return False

async def test_purchase():
    """Test product purchase flow"""
    print_header("TEST 2: Product Purchase")
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with websockets.connect(WS_URL, ssl=ssl_context) as websocket:
            # Send connection message (not needed, just send actual message)
            # Send purchase request
            purchase_msg = {
                "action": "sendMessage",
                "data": {
                    "user_id": USER_ID,
                    "session_id": f"test-{datetime.now().timestamp()}",
                    "type": "TEXT",
                    "message": "Quiero comprar un iPhone 15 Pro"
                }
            }
            print_message("user", "Quiero comprar un iPhone 15 Pro")
            await websocket.send(json.dumps(purchase_msg))
            
            # Collect response
            response_text = ""
            timeout_count = 0
            max_timeout = 30
            
            while timeout_count < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    chunk = response
                    response_text += chunk
                    print(chunk, end='', flush=True)
                    timeout_count = 0
                except asyncio.TimeoutError:
                    timeout_count += 1
                    if timeout_count >= 3:
                        break
            
            print("\n")
            
            # Validate response
            if "ORD-" in response_text or "compra" in response_text.lower():
                print_success("Purchase flow completed")
                if "ORD-" in response_text:
                    print_success("Order ID found in response")
                return True
            else:
                print_error("Purchase flow failed - no order confirmation")
                return False
                
    except Exception as e:
        print_error(f"Purchase test failed: {str(e)}")
        return False

async def test_balance_query():
    """Test balance query (no tool use)"""
    print_header("TEST 3: Balance Query (No Tool Use)")
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        async with websockets.connect(WS_URL, ssl=ssl_context) as websocket:
            # Send connection message (not needed, just send actual message)
            # Send balance query
            balance_msg = {
                "action": "sendMessage",
                "data": {
                    "user_id": USER_ID,
                    "session_id": f"test-{datetime.now().timestamp()}",
                    "type": "TEXT",
                    "message": "¿Cuál es mi saldo?"
                }
            }
            print_message("user", "¿Cuál es mi saldo?")
            await websocket.send(json.dumps(balance_msg))
            
            # Collect response
            response_text = ""
            timeout_count = 0
            max_timeout = 30
            
            while timeout_count < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    chunk = response
                    response_text += chunk
                    print(chunk, end='', flush=True)
                    timeout_count = 0
                except asyncio.TimeoutError:
                    timeout_count += 1
                    if timeout_count >= 3:
                        break
            
            print("\n")
            
            # Validate response
            if "MXN" in response_text or "saldo" in response_text.lower():
                print_success("Balance query completed")
                return True
            else:
                print_error("Balance query failed")
                return False
                
    except Exception as e:
        print_error(f"Balance test failed: {str(e)}")
        return False

async def main():
    """Run all tests"""
    print_header("🧪 CENTLI Tool Use - Complete Test Suite")
    print_info(f"Testing WebSocket: {WS_URL}")
    print_info(f"User: {USER_ID}")
    print_info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test 1: Transfer
    result1 = await test_transfer()
    results.append(("Transfer", result1))
    await asyncio.sleep(2)
    
    # Test 2: Purchase
    result2 = await test_purchase()
    results.append(("Purchase", result2))
    await asyncio.sleep(2)
    
    # Test 3: Balance (no tool use)
    result3 = await test_balance_query()
    results.append(("Balance Query", result3))
    
    # Summary
    print_header("📊 Test Results Summary")
    passed = 0
    failed = 0
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
            passed += 1
        else:
            print_error(f"{test_name}: FAILED")
            failed += 1
    
    print(f"\n{Colors.BOLD}Total: {passed} passed, {failed} failed{Colors.END}\n")
    
    if failed == 0:
        print_success("🎉 All tests passed! Tool Use is working correctly!")
        return 0
    else:
        print_error(f"⚠️  {failed} test(s) failed. Check logs for details.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
