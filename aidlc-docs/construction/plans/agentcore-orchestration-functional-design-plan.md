# Functional Design Plan - Unit 2: AgentCore & Orchestration

## Unit Context

**Unit Name**: AgentCore & Orchestration  
**Unit Type**: AI/ML Orchestration Unit  
**Purpose**: Provide intelligent orchestration, multimodal processing, and WebSocket communication

**Stories Assigned** (Dev 3 - AgentCore/AI):
- Story 3.1: Setup AWS Bedrock AgentCore (2h) - Must Have
- Story 3.2: Configure Action Groups (2h) - Must Have
- Story 3.3: Integrate Nova Sonic for Voice (2h) - Must Have
- Story 3.4: Integrate Nova Canvas for Images (1.5h) - Could Have
- Story 3.5: Implement Intent Recognition (1.5h) - Must Have
- Story 3.6: Implement Managed Memory (1.5h) - Should Have

**Total Estimated Effort**: 10.5 hours

---

## Functional Design Steps

### Step 1: Business Logic Modeling
- [x] Define message processing workflow (WebSocket → Orchestration → AgentCore → EventBridge)
- [x] Model intent recognition logic (user utterance → intent + entities)
- [x] Define session lifecycle (connect → active → disconnect)
- [x] Model voice processing pipeline (audio stream → transcription → processing → synthesis)
- [x] Model image processing pipeline (upload → analysis → context enrichment)
- [x] Define action event publishing logic (intent → action event → EventBridge)
- [x] Model response handling (EventBridge response → AgentCore → WebSocket)

### Step 2: Domain Entity Modeling
- [x] Define Session entity (session_id, user_id, connection_id, state, metadata)
- [x] Define Message entity (message_id, session_id, type, content, timestamp)
- [x] Define Intent entity (intent_type, confidence, entities, context)
- [x] Define ActionEvent entity (action_type, action_data, request_id, session_id)
- [x] Define VoiceInput entity (audio_data, format, duration, language)
- [x] Define ImageInput entity (image_data, format, s3_key, analysis_results)
- [x] Define AgentResponse entity (response_text, response_audio, metadata)

### Step 3: Business Rules Definition
- [x] Define authentication validation rules (token validation, user identity verification)
- [x] Define session management rules (timeout, expiration, cleanup)
- [x] Define intent recognition rules (confidence thresholds, ambiguity handling)
- [x] Define voice processing rules (audio format validation, language detection, quality checks)
- [x] Define image processing rules (format validation, size limits, content analysis)
- [x] Define action event routing rules (intent → action group mapping)
- [x] Define error handling rules (retry logic, fallback strategies, error messages)

### Step 4: Data Flow Design
- [x] Define WebSocket message flow (client → API Gateway → Lambda → AgentCore)
- [x] Define voice data flow (audio stream → Nova Sonic → text → AgentCore)
- [x] Define image data flow (image upload → S3 → Nova Canvas → analysis → AgentCore)
- [x] Define action event flow (AgentCore → EventBridge → Action Groups)
- [x] Define response flow (Action Groups → EventBridge → AgentCore → WebSocket)
- [x] Define session state flow (local DynamoDB ↔ Managed Memory sync)

### Step 5: Integration Point Design
- [x] Define Bedrock AgentCore integration (API calls, configuration, error handling)
- [x] Define Nova Sonic integration (audio streaming, transcription, synthesis)
- [x] Define Nova Canvas integration (image upload, analysis, results retrieval)
- [x] Define EventBridge integration (event publishing, event subscription, event schemas)
- [x] Define DynamoDB integration (session storage, query patterns, TTL)
- [x] Define S3 integration (image upload, presigned URLs, access control)

### Step 6: Error Handling Design
- [x] Define connection error scenarios (WebSocket disconnect, timeout, network failure)
- [x] Define authentication error scenarios (invalid token, expired session, unauthorized access)
- [x] Define processing error scenarios (AgentCore failure, Nova service errors, timeout)
- [x] Define action error scenarios (Action Group failure, EventBridge delivery failure)
- [x] Define validation error scenarios (invalid input, malformed data, unsupported format)
- [x] Define retry strategies (exponential backoff, max retries, circuit breaker)
- [x] Define fallback strategies (graceful degradation, error messages, alternative flows)

---

## Functional Design Questions

### Business Logic Modeling Questions

**Question 1: Intent Recognition Strategy**

When AgentCore processes a user message, how should intent recognition handle ambiguous or low-confidence intents?

A) Always execute the highest confidence intent (even if confidence is low)  
B) Ask for clarification when confidence is below a threshold (e.g., 70%)  
C) Present multiple intent options to the user for selection  
D) Use conversation context to disambiguate automatically  
E) Other (please describe)

[Answer]:B

**Question 2: Session State Synchronization**

How should the Orchestration Service synchronize session state between local DynamoDB and Bedrock Managed Memory?

A) Write to both simultaneously (strong consistency, higher latency)  
B) Write to local first, async sync to Managed Memory (eventual consistency)  
C) Write to Managed Memory only (simpler, but slower reads)  
D) Write to local only, sync to Managed Memory on disconnect (best performance)  
E) Other (please describe)

[Answer]:A

**Question 3: Voice Processing Mode**

How should voice input be processed for optimal latency and user experience?

A) Streaming mode (real-time transcription as user speaks)  
B) Batch mode (wait for complete utterance, then transcribe)  
C) Hybrid mode (stream for feedback, batch for final processing)  
D) Push-to-talk mode (user controls recording start/stop)  
E) Other (please describe)

[Answer]:B

**Question 4: Multimodal Message Handling**

When a user sends a message with both voice and image (e.g., "¿Cuánto cuesta esto?" + product photo), how should AgentCore process it?

A) Sequential processing (voice first, then image)  
B) Parallel processing (both simultaneously, merge results)  
C) Prioritize voice, use image only if needed for clarification  
D) Prioritize image, use voice as supplementary context  
E) Other (please describe)

[Answer]:B

### Domain Entity Questions

**Question 5: Session Entity Attributes**

What additional attributes should the Session entity include beyond the basics (session_id, user_id, connection_id)?

A) Minimal: Just add `created_at`, `expires_at`, `state` (active/disconnected)  
B) Standard: Add `last_activity`, `message_count`, `user_preferences`  
C) Comprehensive: Add `device_info`, `location`, `language`, `conversation_summary`  
D) Custom: Specify your own attributes  
E) Other (please describe)

[Answer]: B

**Question 6: Intent Entity Structure**

How should the Intent entity represent extracted entities and context?

A) Flat structure: `{intent_type, confidence, entity1, entity2, ...}`  
B) Nested structure: `{intent_type, confidence, entities: [{type, value, confidence}], context: {}}`  
C) Typed structure: `{intent_type, confidence, transfer_data: {}, purchase_data: {}, ...}`  
D) Flexible structure: `{intent_type, confidence, data: {}}` (schema-less)  
E) Other (please describe)

[Answer]:C

### Business Rules Questions

**Question 7: Authentication Validation**

What level of authentication validation should the Orchestration Service perform?

A) Basic: Validate JWT token signature and expiration only  
B) Standard: Validate token + check user exists in DynamoDB  
C) Strict: Validate token + check user + verify biometric data  
D) Delegated: Pass token to AgentCore, let it handle validation  
E) Other (please describe)

[Answer]:C

**Question 8: Session Timeout Policy**

How long should a WebSocket session remain active without user activity?

A) Short: 5 minutes (aggressive cleanup, lower costs)  
B) Standard: 15 minutes (balanced)  
C) Long: 30 minutes (better UX, higher costs)  
D) Configurable: User can set their own timeout  
E) Other (please describe)

[Answer]:15

**Question 9: Voice Quality Validation**

What validation should be performed on voice input before processing?

A) None: Accept all audio, let Nova Sonic handle it  
B) Basic: Check audio format and size only  
C) Standard: Check format, size, duration (min/max length)  
D) Strict: Check format, size, duration, audio quality (noise level, clarity)  
E) Other (please describe)

[Answer]: C

**Question 10: Image Processing Rules**

What validation and processing rules should apply to image uploads?

A) Minimal: Accept common formats (JPEG, PNG), max 5MB  
B) Standard: Validate format, size, dimensions, run basic content check  
C) Strict: Validate format, size, dimensions, content moderation, PII detection  
D) Custom: Specify your own rules  
E) Other (please describe)

[Answer]: B

### Data Flow Questions

**Question 11: Action Event Schema**

How detailed should the action event schema be when publishing to EventBridge?

A) Minimal: `{action_type, user_id, session_id, data: {}}`  
B) Standard: `{action_type, user_id, session_id, request_id, timestamp, data: {}, metadata: {}}`  
C) Comprehensive: Include full conversation context, user preferences, intent confidence  
D) Custom: Specify your own schema  
E) Other (please describe)

[Answer]:C

**Question 12: Response Aggregation**

When multiple Action Groups respond to a single intent (e.g., transfer requires CRM + CoreBanking), how should responses be aggregated?

A) Sequential: Wait for each response in order, process one at a time  
B) Parallel: Wait for all responses, aggregate, then respond to user  
C) Streaming: Send partial responses to user as they arrive  
D) Smart: AgentCore decides based on intent type  
E) Other (please describe)

[Answer]:D

### Integration Point Questions

**Question 13: Bedrock AgentCore Configuration**

What AgentCore configuration strategy should be used for the hackathon?

A) Simple: Single agent with all Action Groups, basic prompts  
B) Standard: Single agent with detailed prompts, guardrails, memory configuration  
C) Advanced: Multiple agents for different domains (banking, marketplace, CRM)  
D) Minimal: Use Bedrock Converse API instead of AgentCore (simpler fallback)  
E) Other (please describe)

[Answer]: C

**Question 14: Nova Sonic Voice Configuration**

What voice characteristics should Nova Sonic use for CENTLI responses?

A) Default: Use Nova Sonic default Spanish voice  
B) Customized: Specify gender, accent (Mexican Spanish), speaking rate  
C) Persona-based: Configure voice to match CENTLI brand personality  
D) User-selectable: Let users choose their preferred voice  
E) Other (please describe)

[Answer]:B

**Question 15: EventBridge Event Routing**

How should EventBridge route action events to the correct Action Group?

A) Simple: Use `detail-type` field to route (e.g., "TransferRequest" → CoreBanking)  
B) Pattern-based: Use event pattern matching on multiple fields  
C) Content-based: Route based on event payload content  
D) Topic-based: Use separate event buses for each Action Group  
E) Other (please describe)

[Answer]:D

### Error Handling Questions

**Question 16: AgentCore Failure Handling**

What should happen if AgentCore fails to process a message?

A) Fail fast: Return error to user immediately  
B) Retry: Retry up to 3 times with exponential backoff  
C) Fallback: Fall back to simpler Bedrock Converse API  
D) Queue: Queue message for later processing, notify user of delay  
E) Other (please describe)

[Answer]:D

**Question 17: Action Group Timeout**

How long should AgentCore wait for an Action Group response before timing out?

A) Short: 3 seconds (fast fail, better UX)  
B) Standard: 10 seconds (balanced)  
C) Long: 30 seconds (accommodate slow operations)  
D) Variable: Different timeouts for different action types  
E) Other (please describe)

[Answer]:A

**Question 18: WebSocket Disconnect Handling**

What should happen when a WebSocket connection is lost during message processing?

A) Abort: Cancel processing, discard message  
B) Complete: Finish processing, store response for reconnection  
C) Notify: Send notification via alternative channel (email, SMS)  
D) Retry: Attempt to reconnect and deliver response  
E) Other (please describe)

[Answer]: D

---

## Success Criteria

- [x] All business logic workflows clearly defined
- [x] All domain entities modeled with attributes and relationships
- [x] All business rules documented with validation logic
- [x] All data flows mapped from input to output
- [x] All integration points specified with error handling
- [x] All error scenarios identified with mitigation strategies
- [x] All questions answered by user
- [x] No ambiguities remaining in functional design

---

**Plan Status**: Complete - All artifacts generated  
**Total Questions**: 18 questions across 6 categories  
**Artifacts Created**: 
- business-logic-model.md (10 workflows, 80+ pages)
- business-rules.md (44 rules across 11 categories)
- domain-entities.md (10 entities with full specifications)

