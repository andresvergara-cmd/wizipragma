# NFR Requirements Clarification Questions - Unit 2: AgentCore & Orchestration

## Missing Answer

### Clarification 1: Voice Processing Latency (Question 1)

**Missing Answer**: Question 1 has no answer provided.

**Question**: What is the acceptable latency for voice processing (user speaks → text response)?

A) Fast: < 2 seconds (aggressive, may require optimization)  
B) Standard: < 3 seconds (balanced, achievable)  
C) Relaxed: < 5 seconds (safe for demo)  
D) Custom: Specify your target

[Answer]: B

---

## Potential Issues Detected

### Clarification 2: Python 3.12 Runtime (Question 15)

**Original Answer**: D) Python 3.12 (cutting edge, may have compatibility issues)

**Concern**: Python 3.12 is very new and may have compatibility issues with AWS Lambda and Bedrock SDK:
- AWS Lambda Python 3.12 support is recent (may have limited library support)
- Boto3 and AWS SDK compatibility may be incomplete
- Third-party libraries may not be fully compatible
- Could cause unexpected issues during hackathon

**Recommendation**: Python 3.10 or 3.11 would be safer choices for a hackathon with tight timeline.

**Clarification Needed**:

A) Keep Python 3.12 (I understand the compatibility risk)  
B) Switch to Python 3.11 (latest with good compatibility)  
C) Switch to Python 3.10 (stable, widely supported - recommended)  
D) Switch to Python 3.9 (most stable, guaranteed compatibility)

[Answer]: B

---

### Clarification 3: High Uptime + Queue Strategy Mismatch (Questions 7 & 8)

**Original Answers**:
- Question 7: A) High: 99.9% uptime (production-like, requires robust error handling)
- Question 8: D) Queue: Queue for later processing

**Concern**: These two answers create a potential mismatch:
- 99.9% uptime target requires robust error handling and immediate feedback
- Queue strategy means delayed processing and no immediate response
- For a demo, users expect immediate feedback (even if it's an error)
- Queueing adds complexity (need queue infrastructure, background workers, notification system)

**Recommendation for Hackathon**:
- Either: Lower uptime target (90-95%) + Retry strategy (simpler, immediate feedback)
- Or: Keep high uptime + Retry strategy (more work but better UX)

**Clarification Needed**:

A) Keep both (99.9% uptime + Queue) - I'll implement queue infrastructure  
B) Change to: 95% uptime + Retry with exponential backoff (recommended for hackathon)  
C) Change to: 99.9% uptime + Retry with exponential backoff (more robust, more work)  
D) Other (please describe)

[Answer]: B

---

### Clarification 4: Strict Auth + Hackathon Timeline (Question 9)

**Original Answer**: C) Strict: JWT + user exists + biometric verification

**Concern**: Strict authentication with biometric verification adds significant complexity for an 8-hour hackathon:
- Requires biometric data capture and storage
- Requires biometric verification logic
- Requires handling biometric failures and re-authentication
- May not be necessary for a demo (can be simulated)

**Recommendation**: Standard authentication (JWT + user exists) is sufficient for demo quality while keeping timeline realistic.

**Clarification Needed**:

A) Keep strict auth with biometric (I understand the added complexity)  
B) Switch to standard auth (JWT + user exists - recommended for hackathon)  
C) Switch to basic auth (JWT only - fastest to implement)  
D) Simulated biometric (check flag in token, don't implement actual verification)

[Answer]: B,D

---

## Summary

**Total Clarifications Needed**: 4

**Impact on Timeline**:
- Clarification 1: Low impact (just need to select latency target)
- Clarification 2: Medium impact (Python 3.12 compatibility issues could cost 1-2 hours debugging)
- Clarification 3: HIGH impact (Queue infrastructure could add 2-3 hours vs simple retry)
- Clarification 4: HIGH impact (Biometric verification could add 2-3 hours vs standard auth)

**Recommendation**: Consider simplifying Clarifications 2, 3, and 4 to stay within 8-hour hackathon timeline while maintaining demo quality.

---

**Next Step**: Please answer all [Answer]: tags above, then I will proceed to generate NFR requirements artifacts.
