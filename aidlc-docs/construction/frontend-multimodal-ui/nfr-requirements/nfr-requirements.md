# NFR Requirements - Unit 4: Frontend Multimodal UI

## Document Information
- **Unit**: Frontend Multimodal UI
- **Created**: 2026-02-17
- **Context**: 8-hour hackathon, demo quality
- **Approach**: Pragmatic, minimal viable implementation

---

## 1. Performance Requirements

### 1.1 Page Load Performance
**Requirement**: Fast initial page load for demo presentation

**Targets**:
- Initial page load (HTML, CSS, JS): < 3 seconds
- Time to interactive: < 4 seconds
- First contentful paint: < 1.5 seconds

**Rationale**: Hackathon demo context allows for pragmatic targets. Unminified files acceptable. Focus on functionality over extreme optimization.

**Implementation**:
- Single HTML file with inline or external JS/CSS
- Bootstrap 5 via CDN (cached by browsers)
- No heavy dependencies or frameworks
- Lazy load non-critical assets

---

### 1.2 WebSocket Communication Latency
**Requirement**: Responsive real-time communication

**Targets**:
- Message send to acknowledgment: < 500ms
- Agent response time: 2-5 seconds (Bedrock processing)
- Voice message processing: 3-7 seconds
- Show loading indicator for operations > 1 second

**Rationale**: User expects immediate feedback. Agent processing time depends on Bedrock, which is acceptable for conversational AI.

**Implementation**:
- Immediate UI feedback on message send
- Typing indicator while agent processes
- WebSocket ping/pong for connection health
- Timeout handling after 30 seconds

---

### 1.3 Voice Processing Performance
**Requirement**: Smooth voice input/output experience

**Targets**:
- Recording start delay: < 500ms
- Audio playback start latency: < 300ms
- Processing approach: Batch (not streaming)
- Maximum recording duration: 30 seconds

**Rationale**: 30 seconds sufficient for banking commands. Batch processing simpler than streaming for hackathon timeline.

**Implementation**:
- MediaRecorder API with WebM format
- Immediate visual feedback on record start
- Audio element for playback
- Progress indicator during recording

---

### 1.4 Image Upload Performance
**Requirement**: Efficient image handling

**Targets**:
- Maximum acceptable upload time: < 5 seconds
- Client-side compression: Yes (resize to max 1920x1080, quality 0.8)
- Upload progress: Show progress bar
- Maximum file size: 5MB
- Supported formats: JPEG, PNG

**Rationale**: Client-side compression reduces upload time and backend storage. 5MB limit prevents abuse.

**Implementation**:
- Canvas API for image resizing
- FileReader API for preview
- XMLHttpRequest or Fetch with progress events
- File size validation before upload

---

### 1.5 UI Responsiveness
**Requirement**: Smooth user interactions

**Targets**:
- Target frame rate: 30fps (sufficient for demo)
- User interaction feedback: < 100ms
- Priority: Fast data loading over complex animations
- Animations: Simple CSS transitions (fade, slide)

**Rationale**: 30fps adequate for demo. Avoid animation blocking. Prioritize functionality.

**Implementation**:
- CSS transitions for smooth effects
- No JavaScript-based animations
- RequestAnimationFrame if needed
- Debounce/throttle for frequent events

---

## 2. Scalability Requirements

### 2.1 Concurrent User Support
**Requirement**: Support demo audience

**Targets**:
- Expected concurrent users: 1-3 (hackathon judges)
- Optimization: Single user experience
- Load testing: Not required
- Frontend: Stateless (can handle multiple users)

**Rationale**: Demo scenario with limited audience. Frontend is stateless, scalability handled by backend.

**Implementation**:
- No client-side user limits
- Each user gets independent session
- No shared state between users

---

### 2.2 Message Throughput
**Requirement**: Handle conversational message volume

**Targets**:
- Messages per second: 1-2 maximum (human conversation rate)
- Chat history display: Last 50 messages
- Pagination: Not needed
- Memory management: Simple array, clear on refresh

**Rationale**: 50 messages sufficient for 15-20 minute demo. No long-term persistence needed.

**Implementation**:
- In-memory message array
- Auto-scroll to latest message
- No virtualization (50 messages is small)
- Clear history on page refresh

---

### 2.3 Asset Loading Strategy
**Requirement**: Simple, fast asset delivery

**Targets**:
- Hosting: Direct S3 (skip CloudFront)
- Browser caching: Basic (Cache-Control: max-age=3600)
- Service worker: No (unnecessary complexity)
- Structure: Single HTML file with inline CSS/JS if possible

**Rationale**: CloudFront adds setup time. Direct S3 sufficient for demo. Single file simplifies deployment.

**Implementation**:
- S3 bucket with public read access
- Static website hosting enabled
- Cache headers configured
- All assets in one or few files

---

## 3. Availability Requirements

### 3.1 Uptime Expectations
**Requirement**: Reliable during demo period

**Targets**:
- Required uptime: 2-3 hours (demo duration)
- Graceful degradation: Show clear error if backend down
- Offline caching: No
- Redundancy: No

**Rationale**: Demo-focused. Full availability not critical outside demo window.

**Implementation**:
- Error message: "Servicio temporalmente no disponible, intenta reconectar"
- Reconnect button on error
- No offline mode

---

### 3.2 Connection Resilience
**Requirement**: Automatic recovery from connection issues

**Targets**:
- Auto-reconnect: Yes
- Maximum reconnection attempts: 5
- Backoff strategy: Exponential (1s, 2s, 4s, 8s, 16s)
- Message queuing: Yes (max 10 messages while disconnected)

**Rationale**: Network issues common. Auto-reconnect improves UX. Exponential backoff prevents server overload.

**Implementation**:
- WebSocket onclose event triggers reconnect
- Display status: "Reconectando... (intento X/5)"
- Queue messages in array
- Send queued messages on reconnect
- Give up after 5 attempts, show manual reconnect button

---

### 3.3 Error Recovery
**Requirement**: User-friendly error handling

**Targets**:
- Auto-retry: WebSocket only (see 3.2)
- User-initiated retry: Buttons for failed operations
- State persistence: session_id in localStorage
- Session recovery: No full state recovery (refresh = new session OK)

**Rationale**: Demo is short, full state recovery unnecessary. Session ID persistence allows reconnection.

**Implementation**:
- localStorage.setItem('session_id', sessionId)
- Retry buttons on error toasts
- Clear error messages with actions
- No complex state serialization

---

## 4. Browser Compatibility Requirements

### 4.1 Supported Browsers
**Requirement**: Modern browser support

**Targets**:
- **Priority**: Chrome/Edge (latest 2 versions)
- **Best effort**: Firefox, Safari
- **Mobile**: iOS Safari 14+, Chrome Mobile
- **Warning**: Show if MediaRecorder API unavailable

**Rationale**: Demo primarily on Chrome desktop. Mobile support for judges testing on phones.

**Implementation**:
- Feature detection on page load
- Warning banner for unsupported browsers
- Graceful degradation (hide unavailable features)
- Test on Chrome, Safari, mobile Chrome

---

### 4.2 Feature Detection
**Requirement**: Handle missing browser APIs

**Targets**:
- **WebSocket**: Required (show error if unavailable)
- **MediaRecorder API**: Fallback to text-only mode
- **Audio API**: Required for playback
- **Approach**: Degraded experience, don't block completely

**Rationale**: WebSocket essential for app. Voice is nice-to-have, text mode sufficient fallback.

**Implementation**:
```javascript
if (!window.WebSocket) {
  showError('WebSocket no soportado. Usa un navegador moderno.');
}
if (!navigator.mediaDevices || !window.MediaRecorder) {
  hideVoiceButton();
  showMessage('Voice input no disponible en este navegador');
}
```

---

### 4.3 Mobile Support
**Requirement**: Mobile-first responsive design

**Targets**:
- Design approach: Mobile-first
- Touch gestures: Basic (tap, scroll)
- Responsive breakpoints: 320px (mobile), 768px (tablet), 1024px (desktop)
- Platform: Web only (no native app)

**Rationale**: Banking = mobile priority. Web app works on all devices.

**Implementation**:
- Bootstrap responsive grid
- Touch-friendly button sizes (min 44x44px)
- Viewport meta tag
- Test on iOS Safari and Chrome Mobile

---

## 5. Security Requirements

### 5.1 Authentication Mechanism
**Requirement**: Simple demo authentication

**Targets**:
- Approach: Mock authentication
- Token: JWT hardcoded or simple form (user_id input)
- Token refresh: No (session lasts entire demo)
- Session timeout: 2 hours

**Rationale**: Focus on multimodal functionality, not complex auth. Real auth out of scope for hackathon.

**Implementation**:
- Simple login form: user_id input
- Generate or use hardcoded JWT
- Store in localStorage
- Include in WebSocket connection

---

### 5.2 Data Transmission Security
**Requirement**: Secure communication

**Targets**:
- WebSocket: WSS (WebSocket Secure) - Yes
- Assets: HTTPS - Yes
- Client-side encryption: No (unnecessary for demo)
- TLS/SSL: Handled by AWS

**Rationale**: AWS API Gateway provides WSS. S3 provides HTTPS. No additional encryption needed.

**Implementation**:
- Use wss:// protocol for WebSocket
- S3 bucket accessed via HTTPS
- No custom encryption code

---

### 5.3 Client-Side Data Protection
**Requirement**: Basic data protection

**Targets**:
- Token storage: localStorage (persists between refreshes)
- Clear on logout: Yes
- Console logging: OK for demo/debugging
- XSS protection: Sanitize user input before innerHTML

**Rationale**: Demo uses mock data. Basic XSS protection sufficient.

**Implementation**:
- localStorage for session_id
- Clear localStorage on logout
- Use textContent instead of innerHTML where possible
- Sanitize HTML if needed (DOMPurify library)

---

## 6. Accessibility Requirements

### 6.1 WCAG Compliance
**Requirement**: Basic accessibility

**Targets**:
- Level: WCAG 2.1 Level A (basic)
- Priority: Semantic HTML, alt text, form labels
- Screen reader testing: No formal testing
- Approach: Best effort, not certified compliance

**Rationale**: Voice interface already improves accessibility. Basic compliance sufficient for demo.

**Implementation**:
- Semantic HTML5 elements
- Alt text for all images
- Labels for all form inputs
- ARIA labels where needed

---

### 6.2 Keyboard Navigation
**Requirement**: Basic keyboard support

**Targets**:
- Tab navigation: All buttons/inputs accessible
- Enter: Submit forms
- Escape: Close modals
- Custom shortcuts: No
- Focus management: Basic (trap focus in modals)

**Rationale**: Sufficient for demo. Full keyboard shortcuts out of scope.

**Implementation**:
- Proper tab order
- Focus visible styles
- Modal focus trap
- Keyboard event listeners for Enter/Escape

---

### 6.3 Visual Accessibility
**Requirement**: Readable, high-contrast design

**Targets**:
- Color contrast: 4.5:1 for text (WCAG AA)
- High contrast mode: No custom mode
- Font size: Use rem units (respects browser settings)
- Information: Icons + text labels (not color-only)

**Rationale**: Clean, legible design benefits all users.

**Implementation**:
- Dark text on light background
- Sufficient font sizes (16px base)
- Icons with text labels
- Test with browser zoom

---

## 7. Reliability Requirements

### 7.1 Error Handling Strategy
**Requirement**: Clear, actionable error messages

**Targets**:
- Display: Toast notifications (non-critical), Modal dialogs (critical)
- Logging: Console for debugging
- Messages: User-friendly + technical details in console
- Retry: Retry button in toasts

**Rationale**: Users need clear feedback. Developers need debugging info.

**Implementation**:
- Bootstrap toasts for errors
- Modal for critical errors (WebSocket failed)
- console.error() for all errors
- Retry buttons where applicable

---

### 7.2 Monitoring and Logging
**Requirement**: Simple debugging capability

**Targets**:
- Client-side tracking: No (Sentry, CloudWatch RUM)
- Performance monitoring: No (Web Vitals)
- Analytics: No (Google Analytics)
- Approach: Console logging only

**Rationale**: External services add complexity. Console sufficient for demo debugging.

**Implementation**:
- Structured console logs: `console.log('[WebSocket]', ...)`
- Error logs: `console.error('[Error]', ...)`
- Browser DevTools for debugging during demo

---

### 7.3 Graceful Degradation
**Requirement**: Handle missing features gracefully

**Targets**:
- WebSocket unavailable: Show error, no fallback
- Voice unavailable: Hide voice button, text-only mode
- Image upload unavailable: Hide upload button
- Feature status: Show indicators ("Voice: ✓" or "Voice: ✗")

**Rationale**: Core features (WebSocket) required. Nice-to-have features (voice) can degrade.

**Implementation**:
- Feature detection on load
- Show/hide UI elements based on availability
- Status indicators in UI
- Clear messaging about unavailable features

---

## 8. Summary

### Critical NFRs (Must Have)
1. ✅ Page load < 4 seconds
2. ✅ WebSocket auto-reconnect (5 attempts)
3. ✅ Mobile-first responsive design
4. ✅ Chrome/Edge support (latest 2 versions)
5. ✅ WSS (secure WebSocket)
6. ✅ Basic error handling with retry

### Important NFRs (Should Have)
1. ✅ Voice processing < 7 seconds
2. ✅ Image upload with compression
3. ✅ Toast notifications for errors
4. ✅ Keyboard navigation
5. ✅ WCAG Level A compliance
6. ✅ Console logging for debugging

### Nice-to-Have NFRs (Could Have)
1. ⚠️ Safari/Firefox full compatibility (best effort)
2. ⚠️ Offline mode (not implemented)
3. ⚠️ Advanced animations (simple only)
4. ⚠️ External monitoring (console only)

---

## Acceptance Criteria

The frontend meets NFR requirements if:

1. ✅ Loads and becomes interactive in < 4 seconds on Chrome
2. ✅ Establishes WebSocket connection and auto-reconnects on disconnect
3. ✅ Displays correctly on mobile (320px) and desktop (1024px+)
4. ✅ Handles voice input/output (if browser supports MediaRecorder)
5. ✅ Uploads and compresses images < 5MB
6. ✅ Shows clear error messages with retry options
7. ✅ Works without build process (vanilla JS + Bootstrap CDN)
8. ✅ Provides basic keyboard navigation (tab, enter, escape)

---

**Document Status**: Complete  
**Next Stage**: NFR Design (if needed) or Infrastructure Design
