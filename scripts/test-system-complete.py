#!/usr/bin/env python3
"""
CENTLI System Testing & Performance Benchmark
Tests text, audio, and model performance
"""

import json
import time
import asyncio
import websockets
import base64
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
WEBSOCKET_URL = "wss://vp8zwzpjpj.execute-api.us-east-1.amazonaws.com/dev"
TEST_USER_ID = "simple-user"

class CENTLITester:
    def __init__(self):
        self.results = {
            "text_tests": [],
            "audio_tests": [],
            "performance": {},
            "errors": []
        }
    
    async def test_text_message(self, message: str) -> Dict:
        """Test text message and measure performance"""
        print(f"\n🧪 Testing TEXT: '{message}'")
        
        start_time = time.time()
        response_chunks = []
        first_chunk_time = None
        
        try:
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                # Generate session ID
                session_id = f"test-{int(time.time() * 1000)}"
                
                # Send message
                payload = {
                    "action": "sendMessage",
                    "data": {
                        "user_id": TEST_USER_ID,
                        "session_id": session_id,
                        "message": message,
                        "type": "TEXT"
                    }
                }
                
                await websocket.send(json.dumps(payload))
                send_time = time.time()
                
                # Receive response
                full_response = ""
                chunk_count = 0
                
                async for response in websocket:
                    chunk_count += 1
                    
                    if first_chunk_time is None:
                        first_chunk_time = time.time()
                    
                    try:
                        data = json.loads(response)
                        
                        if data.get("msg_type") == "stream_chunk":
                            chunk_text = data.get("message", "")
                            full_response += chunk_text
                            response_chunks.append({
                                "chunk": chunk_count,
                                "text": chunk_text,
                                "time": time.time() - start_time
                            })
                        
                        elif data.get("msg_type") == "stream_end":
                            full_response = data.get("message", full_response)
                            break
                        
                        elif data.get("msg_type") == "error":
                            raise Exception(f"Error: {data.get('message')}")
                    
                    except json.JSONDecodeError:
                        # Plain text chunk
                        full_response += response
                        response_chunks.append({
                            "chunk": chunk_count,
                            "text": response,
                            "time": time.time() - start_time
                        })
                
                end_time = time.time()
                
                result = {
                    "message": message,
                    "success": True,
                    "response": full_response,
                    "metrics": {
                        "total_time": end_time - start_time,
                        "time_to_first_chunk": first_chunk_time - send_time if first_chunk_time else None,
                        "chunk_count": chunk_count,
                        "response_length": len(full_response),
                        "avg_chunk_time": (end_time - first_chunk_time) / chunk_count if first_chunk_time and chunk_count > 0 else None
                    }
                }
                
                print(f"✅ Response received ({len(full_response)} chars, {chunk_count} chunks)")
                print(f"⏱️  Total time: {result['metrics']['total_time']:.2f}s")
                print(f"📊 First chunk: {result['metrics']['time_to_first_chunk']:.2f}s")
                print(f"💬 Response preview: {full_response[:100]}...")
                
                return result
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "message": message,
                "success": False,
                "error": str(e),
                "metrics": {
                    "total_time": time.time() - start_time
                }
            }
    
    async def run_text_tests(self):
        """Run comprehensive text tests"""
        print("\n" + "="*60)
        print("📝 TEXT MESSAGE TESTS")
        print("="*60)
        
        test_messages = [
            "¿Cuál es mi saldo?",
            "Muéstrame mis últimas transacciones",
            "¿Cuánto tengo en mi cuenta de ahorros?",
            "¿Qué productos puedo comprar?",
            "Quiero hacer una transferencia de $1000 a Juan Pérez",
            "¿Cuál es mi score de crédito?",
            "Dame un resumen de mis finanzas",
            "¿Cuándo es mi próximo pago de hipoteca?"
        ]
        
        for message in test_messages:
            result = await self.test_text_message(message)
            self.results["text_tests"].append(result)
            await asyncio.sleep(2)  # Wait between tests
    
    def analyze_results(self):
        """Analyze test results and generate report"""
        print("\n" + "="*60)
        print("📊 PERFORMANCE ANALYSIS")
        print("="*60)
        
        # Text tests analysis
        text_tests = [t for t in self.results["text_tests"] if t["success"]]
        
        if text_tests:
            avg_total_time = sum(t["metrics"]["total_time"] for t in text_tests) / len(text_tests)
            avg_first_chunk = sum(t["metrics"]["time_to_first_chunk"] for t in text_tests if t["metrics"]["time_to_first_chunk"]) / len([t for t in text_tests if t["metrics"]["time_to_first_chunk"]])
            avg_response_length = sum(t["metrics"]["response_length"] for t in text_tests) / len(text_tests)
            
            print(f"\n✅ Successful tests: {len(text_tests)}/{len(self.results['text_tests'])}")
            print(f"⏱️  Average total time: {avg_total_time:.2f}s")
            print(f"📊 Average time to first chunk: {avg_first_chunk:.2f}s")
            print(f"📏 Average response length: {avg_response_length:.0f} chars")
            
            # Performance rating
            if avg_total_time < 3:
                rating = "🟢 EXCELLENT"
            elif avg_total_time < 5:
                rating = "🟡 GOOD"
            elif avg_total_time < 8:
                rating = "🟠 ACCEPTABLE"
            else:
                rating = "🔴 NEEDS IMPROVEMENT"
            
            print(f"\n🎯 Performance Rating: {rating}")
        
        # Failed tests
        failed_tests = [t for t in self.results["text_tests"] if not t["success"]]
        if failed_tests:
            print(f"\n❌ Failed tests: {len(failed_tests)}")
            for test in failed_tests:
                print(f"   - {test['message']}: {test.get('error', 'Unknown error')}")
    
    def generate_report(self):
        """Generate detailed report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# CENTLI System Test Report
**Date**: {timestamp}
**WebSocket URL**: {WEBSOCKET_URL}
**Test User**: {TEST_USER_ID}

---

## Test Results Summary

### Text Message Tests
- **Total tests**: {len(self.results['text_tests'])}
- **Successful**: {len([t for t in self.results['text_tests'] if t['success']])}
- **Failed**: {len([t for t in self.results['text_tests'] if not t['success']])}

### Performance Metrics

"""
        
        text_tests = [t for t in self.results["text_tests"] if t["success"]]
        if text_tests:
            avg_total_time = sum(t["metrics"]["total_time"] for t in text_tests) / len(text_tests)
            avg_first_chunk = sum(t["metrics"]["time_to_first_chunk"] for t in text_tests if t["metrics"]["time_to_first_chunk"]) / len([t for t in text_tests if t["metrics"]["time_to_first_chunk"]])
            
            report += f"""
| Metric | Value |
|--------|-------|
| Average Total Time | {avg_total_time:.2f}s |
| Average Time to First Chunk | {avg_first_chunk:.2f}s |
| Average Response Length | {sum(t["metrics"]["response_length"] for t in text_tests) / len(text_tests):.0f} chars |
| Average Chunks per Response | {sum(t["metrics"]["chunk_count"] for t in text_tests) / len(text_tests):.1f} |

### Detailed Test Results

"""
            
            for i, test in enumerate(text_tests, 1):
                report += f"""
#### Test {i}: {test['message']}
- **Status**: ✅ Success
- **Total Time**: {test['metrics']['total_time']:.2f}s
- **Time to First Chunk**: {test['metrics']['time_to_first_chunk']:.2f}s
- **Chunks**: {test['metrics']['chunk_count']}
- **Response Length**: {test['metrics']['response_length']} chars
- **Response Preview**: {test['response'][:150]}...

"""
        
        # Failed tests
        failed_tests = [t for t in self.results["text_tests"] if not t["success"]]
        if failed_tests:
            report += "\n### Failed Tests\n\n"
            for test in failed_tests:
                report += f"- **{test['message']}**: {test.get('error', 'Unknown error')}\n"
        
        return report

async def main():
    """Main test execution"""
    print("\n" + "="*60)
    print("🎤 CENTLI SYSTEM TESTING")
    print("="*60)
    print(f"WebSocket: {WEBSOCKET_URL}")
    print(f"Test User: {TEST_USER_ID}")
    print("="*60)
    
    tester = CENTLITester()
    
    # Run text tests
    await tester.run_text_tests()
    
    # Analyze results
    tester.analyze_results()
    
    # Generate report
    report = tester.generate_report()
    
    # Save report
    with open("TEST-REPORT.md", "w") as f:
        f.write(report)
    
    print("\n" + "="*60)
    print("✅ Testing complete! Report saved to TEST-REPORT.md")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
