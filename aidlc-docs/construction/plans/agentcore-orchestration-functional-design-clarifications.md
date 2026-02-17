# Functional Design Clarification Questions - Unit 2: AgentCore & Orchestration

## Ambiguities Detected

### Clarification 1: Session Timeout (Question 8)

**Original Answer**: "15"

**Ambiguity**: You provided "15" instead of selecting an option (A-E).

**Clarification Needed**: Did you mean:
- B) Standard: 15 minutes (balanced)

Please confirm:

A) Yes, I meant option B (15 minutes)  
B) No, I meant something different (please specify)

[Answer]:A

---

### Clarification 2: AgentCore Configuration Complexity (Question 13)

**Original Answer**: C) Advanced: Multiple agents for different domains (banking, marketplace, CRM)

**Concern**: Multiple agents adds significant complexity for an 8-hour hackathon. This approach requires:
- 3 separate Bedrock Agents (one per domain)
- 3 separate configurations and prompt engineering efforts
- Complex routing logic to determine which agent to invoke
- More integration testing and debugging time

**Alternative Recommendation**: Option B (Standard: Single agent with detailed prompts, guardrails, memory configuration) would be more achievable within the hackathon timeline while still providing robust functionality.

**Clarification Needed**: 

A) Keep multiple agents (I understand the complexity and timeline risk)  
B) Switch to single agent with detailed configuration (recommended for hackathon)  
C) Use simple single agent (Option A - fastest to implement)  
D) Other (please describe)

[Answer]:B

---

### Clarification 3: EventBridge Routing Strategy (Question 15)

**Original Answer**: D) Topic-based: Use separate event buses for each Action Group

**Concern**: Separate event buses for each Action Group adds unnecessary infrastructure complexity:
- 3 separate EventBridge buses (CoreBanking, Marketplace, CRM)
- More complex cross-bus communication for multi-Action Group flows
- Higher operational overhead
- Overkill for a hackathon demo with 3 Action Groups

**Alternative Recommendation**: Option A (Simple: Use `detail-type` field to route) is standard practice and sufficient for this use case. Single event bus with pattern-based routing is simpler and more maintainable.

**Clarification Needed**:

A) Keep separate event buses (I understand the added complexity)  
B) Switch to single event bus with detail-type routing (recommended)  
C) Switch to pattern-based routing on single bus (Option B from original question)  
D) Other (please describe)

[Answer]:B

---

## Summary

**Total Clarifications Needed**: 3

**Impact on Timeline**:
- Clarification 1: Low impact (just confirming timeout value)
- Clarification 2: HIGH impact (multiple agents could add 2-3 hours to development)
- Clarification 3: Medium impact (separate buses could add 1 hour to infrastructure setup)

**Recommendation**: Consider simplifying Clarifications 2 and 3 to stay within the 8-hour hackathon timeline while maintaining demo quality.

---

**Next Step**: Please answer all [Answer]: tags above, then I will proceed to generate functional design artifacts.
