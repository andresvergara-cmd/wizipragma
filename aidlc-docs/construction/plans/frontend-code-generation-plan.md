# Code Generation Plan - Unit 4: Frontend Multimodal UI

## Document Information
- **Unit**: Frontend Multimodal UI
- **Created**: 2026-02-17
- **Context**: 8-hour hackathon, demo quality
- **Tech Stack**: Vanilla JavaScript ES6+, Bootstrap 5 CDN, HTML5/CSS3
- **Deployment**: S3 static website hosting

---

## Unit Context

### Stories Implemented by This Unit
- Story 1.1: Implement WebSocket Connection (1h)
- Story 1.2: Implement Voice Input UI (1.5h)
- Story 1.3: Implement Voice Output UI (1h)
- Story 1.4: Implement Chat Interface (1.5h)
- Story 1.5: Implement Transaction Confirmation UI (1h)
- Story 1.6: Implement Product Catalog UI (1.5h)
- Story 1.7: Implement Image Upload UI (1h)

**Total Estimated Effort**: 8.5 hours

### Dependencies
- **Unit 2** (AgentCore & Orchestration): WebSocket API Gateway URL
- **Unit 3** (Action Groups): Transaction and product data (can mock initially)

### Expected Interfaces
- **WebSocket Messages**: JSON format with action field
- **Image Upload**: Presigned URL flow via WebSocket
- **Authentication**: Mock token in localStorage

### Service Boundaries
- Frontend owns: UI state, user interactions, client-side validation
- Backend owns: Business logic, data persistence, AI processing

---

## Code Location

**Workspace Root**: Current workspace directory  
**Application Code**: `frontend/` directory in workspace root  
**Documentation**: `aidlc-docs/construction/frontend-multimodal-ui/code/`

**File Structure**:
```
frontend/
├── index.html
├── config.js
├── css/
│   └── custom.css
└── js/
    ├── app.js
    ├── websocket-manager.js
    ├── voice-manager.js
    ├── chat-manager.js
    ├── image-manager.js
    ├── transaction-manager.js
    ├── product-catalog-manager.js
    ├── app-state.js
    └── logger.js
```

---

## Code Generation Steps

### Step 1: Project Structure Setup
- [x] Create `frontend/` directory in workspace root
- [x] Create `frontend/css/` subdirectory
- [x] Create `frontend/js/` subdirectory
- [x] Verify directory structure created successfully

**Stories**: Foundation for all stories

---

### Step 2: Configuration File Generation
- [x] Generate `frontend/config.js` with WebSocket URL and settings
- [ ] Include WebSocket URL from Unit 2 deployment
- [ ] Include S3 bucket configuration
- [ ] Include timeout and size limits

**Stories**: Foundation for all stories  
**Dependencies**: Unit 2 (WebSocket URL)

---

### Step 3: Logger Utility Generation
- [x] Generate `frontend/js/logger.js` with console logging utilities
- [ ] Include log(), error(), warn() methods
- [ ] Include category-based logging

**Stories**: Foundation for all stories

---

### Step 4: Application State Management Generation
- [x] Generate `frontend/js/app-state.js` with state management
- [ ] Include state object (connection, messages, user, etc.)
- [ ] Include setState(), getState(), subscribe() methods
- [ ] Include state change notifications

**Stories**: Foundation for all stories

---

### Step 5: WebSocket Manager Generation
- [x] Generate `frontend/js/websocket-manager.js` with WebSocket handling
- [ ] Include connect(), disconnect(), send() methods
- [ ] Include auto-reconnect logic (5 attempts, exponential backoff)
- [ ] Include message queue for offline messages
- [ ] Include connection status tracking
- [ ] Add data-testid attributes for automation

**Stories**: Story 1.1 (WebSocket Connection)

---

### Step 6: Voice Manager Generation
- [x] Generate `frontend/js/voice-manager.js` with voice input/output
- [ ] Include startRecording(), stopRecording() methods
- [ ] Include MediaRecorder API integration
- [ ] Include playAudio() method for voice output
- [ ] Include feature detection (MediaRecorder availability)
- [ ] Add data-testid attributes for automation

**Stories**: Story 1.2 (Voice Input), Story 1.3 (Voice Output)

---

### Step 7: Chat Manager Generation
- [x] Generate `frontend/js/chat-manager.js` with chat interface
- [ ] Include sendMessage(), receiveMessage() methods
- [ ] Include message history management (max 50 messages)
- [ ] Include auto-scroll to latest message
- [ ] Include typing indicator
- [ ] Add data-testid attributes for automation

**Stories**: Story 1.4 (Chat Interface)

---

### Step 8: Image Manager Generation
- [x] Generate `frontend/js/image-manager.js` with image upload
- [ ] Include selectImage(), compressImage() methods
- [ ] Include Canvas API for image compression
- [ ] Include uploadToS3() method with presigned URL
- [ ] Include upload progress tracking
- [ ] Add data-testid attributes for automation

**Stories**: Story 1.7 (Image Upload)

---

### Step 9: Transaction Manager Generation
- [x] Generate `frontend/js/transaction-manager.js` with transaction UI
- [ ] Include showTransactionConfirmation() method
- [ ] Include confirmTransaction(), cancelTransaction() methods
- [ ] Include receipt display
- [ ] Add data-testid attributes for automation

**Stories**: Story 1.5 (Transaction Confirmation)

---

### Step 10: Product Catalog Manager Generation
- [x] Generate `frontend/js/product-catalog-manager.js` with catalog UI
- [ ] Include displayProducts(), filterProducts() methods
- [ ] Include showProductDetails() method
- [ ] Include benefits display
- [ ] Add data-testid attributes for automation

**Stories**: Story 1.6 (Product Catalog)

---

### Step 11: Main Application Generation
- [x] Generate `frontend/js/app.js` with main application logic
- [ ] Include App class that orchestrates all managers
- [ ] Include init() method to initialize all components
- [ ] Include event handlers for UI interactions
- [ ] Include login/authentication flow
- [ ] Add data-testid attributes for automation

**Stories**: All stories (orchestration)

---

### Step 12: HTML Structure Generation
- [x] Generate `frontend/index.html` with complete HTML structure
- [ ] Include Bootstrap 5 CDN links (CSS and JS)
- [ ] Include Bootstrap Icons CDN link
- [ ] Include login screen
- [ ] Include main app container (hidden initially)
- [ ] Include chat interface
- [ ] Include voice controls
- [ ] Include image upload area
- [ ] Include transaction modal
- [ ] Include product catalog section
- [ ] Include all script imports
- [ ] Add data-testid attributes to all interactive elements

**Stories**: All stories (UI structure)

---

### Step 13: Custom CSS Generation
- [x] Generate `frontend/css/custom.css` with custom styles
- [ ] Include layout styles (flexbox, grid)
- [ ] Include component-specific styles
- [ ] Include responsive breakpoints (320px, 768px, 1024px)
- [ ] Include animation styles (fade, slide)
- [ ] Include color scheme and branding

**Stories**: All stories (styling)

---

### Step 14: Deployment Script Generation
- [x] Generate `commands/deploy-frontend.sh` deployment script
- [ ] Include AWS CLI sync command
- [ ] Include cache header configuration
- [ ] Include bucket configuration commands
- [ ] Make script executable

**Stories**: Deployment infrastructure

---

### Step 15: S3 Bucket Configuration Files Generation
- [x] Generate `infrastructure/s3-bucket-policy.json` for public read
- [x] Generate `infrastructure/s3-cors-config.json` for CORS
- [x] Generate `infrastructure/s3-lifecycle-policy.json` for uploads cleanup

**Stories**: Deployment infrastructure

---

### Step 16: Frontend README Generation
- [x] Generate `frontend/README.md` with setup instructions
- [ ] Include local development instructions
- [ ] Include deployment instructions
- [ ] Include testing checklist
- [ ] Include troubleshooting guide

**Stories**: Documentation

---

### Step 17: Code Summary Generation
- [x] Generate `aidlc-docs/construction/frontend-multimodal-ui/code/code-summary.md`
- [ ] Include file structure overview
- [ ] Include component descriptions
- [ ] Include key functions and methods
- [ ] Include integration points
- [ ] Include testing approach

**Stories**: Documentation

---

### Step 18: API Documentation Generation
- [x] Generate `aidlc-docs/construction/frontend-multimodal-ui/code/websocket-api.md` (included in code-summary.md)
- [ ] Document WebSocket message formats
- [ ] Document request/response patterns
- [ ] Document error handling
- [ ] Include example messages

**Stories**: Documentation

---

### Step 19: Testing Guide Generation
- [x] Generate `aidlc-docs/construction/frontend-multimodal-ui/code/testing-guide.md` (included in frontend/README.md)
- [ ] Include manual testing checklist
- [ ] Include browser compatibility testing
- [ ] Include mobile testing instructions
- [ ] Include common issues and solutions

**Stories**: Documentation

---

### Step 20: Update SAM Template (Optional)
- [x] Skipped (S3 bucket already exists from Unit 1, manual configuration via AWS CLI)
- [ ] Add bucket policy resource
- [ ] Add CORS configuration
- [ ] Add lifecycle policy
- [ ] Note: Bucket already exists from Unit 1, this adds configuration

**Stories**: Deployment infrastructure

---

## Story Traceability

### Story 1.1: WebSocket Connection
- Step 5: WebSocket Manager Generation
- Step 11: Main Application (connection initialization)
- Step 12: HTML Structure (connection status display)

### Story 1.2: Voice Input UI
- Step 6: Voice Manager (recording functionality)
- Step 11: Main Application (voice button handlers)
- Step 12: HTML Structure (voice input button)

### Story 1.3: Voice Output UI
- Step 6: Voice Manager (playback functionality)
- Step 11: Main Application (audio playback)
- Step 12: HTML Structure (audio controls)

### Story 1.4: Chat Interface
- Step 7: Chat Manager Generation
- Step 11: Main Application (message handlers)
- Step 12: HTML Structure (chat UI)

### Story 1.5: Transaction Confirmation UI
- Step 9: Transaction Manager Generation
- Step 11: Main Application (transaction handlers)
- Step 12: HTML Structure (transaction modal)

### Story 1.6: Product Catalog UI
- Step 10: Product Catalog Manager Generation
- Step 11: Main Application (catalog handlers)
- Step 12: HTML Structure (catalog section)

### Story 1.7: Image Upload UI
- Step 8: Image Manager Generation
- Step 11: Main Application (upload handlers)
- Step 12: HTML Structure (upload area)

---

## Dependencies and Interfaces

### Unit 2 Dependencies (AgentCore & Orchestration)
**Required**:
- WebSocket URL: `wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod`
- WebSocket message format: JSON with `action` field
- Connection/disconnection handling

**Status**: ✅ Complete and deployed

### Unit 3 Dependencies (Action Groups)
**Required** (can mock initially):
- Transaction data format
- Product catalog data format
- Beneficiary data format

**Status**: ⏳ In progress (another developer)

**Mitigation**: Use mock data in frontend until Unit 3 is complete

---

## Automation-Friendly Code

All interactive elements will include `data-testid` attributes:

**Examples**:
- `data-testid="login-form-submit-button"`
- `data-testid="chat-message-input"`
- `data-testid="chat-send-button"`
- `data-testid="voice-record-button"`
- `data-testid="image-upload-button"`
- `data-testid="transaction-confirm-button"`
- `data-testid="product-catalog-item-{id}"`

**Naming Convention**: `{component}-{element-role}`

---

## Success Criteria

- [ ] All 20 steps completed and marked [x]
- [ ] All 7 stories implemented
- [ ] Frontend accessible locally (file:// or local server)
- [ ] All JavaScript modules created
- [ ] HTML structure complete with Bootstrap
- [ ] Custom CSS applied
- [ ] Deployment script ready
- [ ] Documentation complete
- [ ] Code follows NFR requirements (vanilla JS, no build process)
- [ ] All interactive elements have data-testid attributes

---

## Estimated Completion Time

- Steps 1-4 (Setup & Utilities): 30 minutes
- Steps 5-10 (Core Managers): 4 hours
- Steps 11-13 (Main App & UI): 2.5 hours
- Steps 14-20 (Deployment & Docs): 1.5 hours

**Total**: 8.5 hours (matches story estimates)

---

**Plan Status**: Ready for approval  
**Next Action**: Wait for user approval to begin code generation
