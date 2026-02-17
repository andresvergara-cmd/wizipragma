# NFR Requirements Plan - Unit 4: Frontend Multimodal UI

## Unit Context

**Unit Name**: Frontend Multimodal UI  
**Purpose**: Provide multimodal user interface for voice, text, and image interactions  
**Technology Stack**: HTML5/CSS3/JavaScript (ES6+), WebSocket API, MediaRecorder API, Audio API  
**Dependencies**: Unit 2 (WebSocket API Gateway), Unit 3 (Action Groups for data)  
**Context**: 8-hour hackathon, demo quality (not production)

---

## NFR Assessment Steps

### Step 1: Performance Requirements
- [x] Define page load performance targets
- [x] Define WebSocket message latency requirements
- [x] Define voice processing performance expectations
- [x] Define image upload performance targets
- [x] Define UI responsiveness requirements

### Step 2: Scalability Requirements
- [x] Define concurrent user expectations
- [x] Define message throughput requirements
- [x] Define asset loading strategy (CDN, caching)
- [x] Define client-side resource management

### Step 3: Availability Requirements
- [x] Define uptime expectations for frontend
- [x] Define offline capability requirements
- [x] Define connection resilience strategy
- [x] Define error recovery mechanisms

### Step 4: Browser Compatibility
- [x] Define supported browsers and versions
- [x] Define mobile browser support
- [x] Define feature detection and fallbacks
- [x] Define progressive enhancement strategy

### Step 5: Security Requirements
- [x] Define authentication mechanism
- [x] Define data transmission security
- [x] Define client-side data protection
- [x] Define XSS and CSRF protection

### Step 6: Accessibility Requirements
- [x] Define WCAG compliance level
- [x] Define keyboard navigation support
- [x] Define screen reader compatibility
- [x] Define color contrast and visual requirements

### Step 7: Tech Stack Decisions
- [x] Define JavaScript framework/library choice
- [x] Define CSS framework choice
- [x] Define build/bundling strategy
- [x] Define testing framework

### Step 8: Reliability Requirements
- [x] Define error handling strategy
- [x] Define logging and monitoring approach
- [x] Define connection retry logic
- [x] Define graceful degradation patterns

---

## NFR Clarification Questions

### Performance Requirements

**Q1: Page Load Performance**  
What are the acceptable page load times for the frontend?
- Initial page load (HTML, CSS, JS)?
- Time to interactive (when user can start using)?
- First contentful paint?
- Given hackathon context, what's the minimum acceptable performance?

[Answer]: Para el hackathon, targets pragmáticos: Initial page load < 3 segundos, Time to interactive < 4 segundos, First contentful paint < 1.5 segundos. Prioridad en funcionalidad sobre optimización extrema. Archivos sin minificar está bien para demo.

---

**Q2: WebSocket Message Latency**  
What latency is acceptable for WebSocket communication?
- Message send to acknowledgment?
- Agent response time expectations?
- Voice message processing time?
- Should we show loading indicators for operations > X seconds?

[Answer]: Message send acknowledgment < 500ms. Agent response 2-5 segundos (depende de Bedrock). Voice processing 3-7 segundos. Mostrar loading indicator para operaciones > 1 segundo. Typing indicator mientras el agente procesa.

---

**Q3: Voice Processing Performance**  
What performance is expected for voice features?
- Maximum acceptable delay for voice recording start?
- Audio playback start latency?
- Should we support real-time streaming or batch processing?
- Maximum recording duration?

[Answer]: Recording start delay < 500ms. Audio playback start < 300ms. Batch processing (no streaming para simplificar). Maximum recording duration: 30 segundos (suficiente para comandos bancarios). WebM format para compatibilidad.

---

**Q4: Image Upload Performance**  
What are the image upload performance requirements?
- Maximum acceptable upload time?
- Should we compress images client-side?
- Should we show upload progress?
- Maximum image file size?

[Answer]: Upload time < 5 segundos para imágenes típicas. Compresión client-side básica (resize a max 1920x1080, quality 0.8). Mostrar upload progress bar. Maximum file size: 5MB. Formatos: JPEG, PNG.

---

**Q5: UI Responsiveness**  
How responsive should the UI be?
- Target frame rate for animations (30fps, 60fps)?
- Maximum acceptable delay for user interactions?
- Should we prioritize smooth animations or fast data loading?
- Given hackathon context, what's acceptable?

[Answer]: Target 30fps (suficiente para demo). User interactions < 100ms feedback. Priorizar fast data loading sobre animaciones complejas. Animaciones simples (fade, slide) con CSS transitions. No animaciones bloqueantes.

---

### Scalability Requirements

**Q6: Concurrent User Expectations**  
How many concurrent users should the frontend support?
- Expected number of demo users?
- Should we optimize for single user or multiple?
- Any load testing requirements?
- Given hackathon demo, what's realistic?

[Answer]: Demo para 1-3 usuarios concurrentes (jueces del hackathon). Optimizar para single user experience. No load testing requerido. Frontend puede manejar múltiples usuarios sin problema (stateless).

---

**Q7: Message Throughput**  
What message volume should the frontend handle?
- Messages per second per user?
- Maximum chat history size to display?
- Should we paginate or virtualize long message lists?
- Memory management strategy for long sessions?

[Answer]: 1-2 messages por segundo máximo (conversación humana). Display últimos 50 mensajes (suficiente para demo de 15-20 minutos). No pagination necesaria. Simple array en memoria, clear on page refresh.

---

**Q8: Asset Loading Strategy**  
How should we load and cache frontend assets?
- Use CDN (CloudFront) or direct S3?
- Browser caching strategy (cache headers)?
- Service worker for offline support?
- Given hackathon timeline, what's practical?

[Answer]: Direct S3 (skip CloudFront para ahorrar tiempo). Browser caching básico (Cache-Control: max-age=3600). No service worker (complejidad innecesaria). Todos los assets en single HTML file si es posible (inline CSS/JS).

---

### Availability Requirements

**Q9: Uptime Expectations**  
What availability is expected for the frontend?
- Should frontend work if backend is down (graceful degradation)?
- Should we cache data locally for offline viewing?
- What's acceptable for a hackathon demo?
- Any redundancy requirements?

[Answer]: Uptime durante demo (2-3 horas) es suficiente. Mostrar error claro si backend down. No offline caching. No redundancy. Graceful error messages: "Servicio temporalmente no disponible, intenta reconectar".

---

**Q10: Connection Resilience**  
How should we handle connection issues?
- Auto-reconnect on WebSocket disconnect?
- Maximum reconnection attempts?
- Exponential backoff strategy?
- Should we queue messages while disconnected?

[Answer]: Auto-reconnect: Sí. Max 5 intentos. Exponential backoff: 1s, 2s, 4s, 8s, 16s. Queue messages mientras disconnected (max 10 mensajes). Mostrar status: "Reconectando..." con contador de intentos.

---

**Q11: Error Recovery**  
How should the frontend recover from errors?
- Automatic retry for failed operations?
- User-initiated retry buttons?
- Should we persist state across page refreshes?
- Session recovery after browser crash?

[Answer]: Auto-retry para WebSocket (ver Q10). User-initiated retry button para operaciones fallidas (enviar mensaje, upload imagen). Persist session_id en localStorage. No full state recovery (demo corta, refresh = new session OK).

---

### Browser Compatibility

**Q12: Supported Browsers**  
Which browsers must we support?
- Desktop browsers (Chrome, Firefox, Safari, Edge)?
- Minimum browser versions?
- Mobile browsers (iOS Safari, Chrome Mobile)?
- Should we show "unsupported browser" warnings?

[Answer]: Chrome/Edge (últimas 2 versiones) - PRIORITY. Firefox, Safari: best effort. Mobile: iOS Safari 14+, Chrome Mobile. Mostrar warning si MediaRecorder API no disponible. Demo principalmente en Chrome desktop.

---

**Q13: Feature Detection**  
How should we handle missing browser features?
- WebSocket support (fallback to polling)?
- MediaRecorder API (fallback to file upload)?
- Audio API support?
- Should we block usage or provide degraded experience?

[Answer]: WebSocket: requerido (no fallback, mostrar error). MediaRecorder: fallback a text-only mode con mensaje "Voice no soportado en este browser". Audio API: requerido para playback. Degraded experience OK, no bloquear completamente.

---

**Q14: Mobile Support**  
What level of mobile support is required?
- Mobile-first design or desktop-first?
- Touch gestures support?
- Responsive breakpoints?
- Native mobile app or web only?

[Answer]: Mobile-first design (banking = mobile priority). Touch gestures básicos (tap, scroll). Breakpoints: 320px (mobile), 768px (tablet), 1024px (desktop). Web only (no native app). Demo funciona bien en mobile y desktop.

---

### Security Requirements

**Q15: Authentication Mechanism**  
How should users authenticate?
- JWT tokens from where (login page, hardcoded for demo)?
- Token refresh mechanism?
- Session timeout?
- Given hackathon, can we use mock authentication?

[Answer]: Mock authentication para demo. JWT hardcoded o simple form (user_id input). No token refresh (session dura toda la demo). Session timeout: 2 horas. Focus en funcionalidad multimodal, no en auth complejo.

---

**Q16: Data Transmission Security**  
How should we secure data transmission?
- WSS (WebSocket Secure) required?
- HTTPS for all assets?
- Encrypt sensitive data client-side?
- Given hackathon, what's minimum acceptable?

[Answer]: WSS (wss://) - Sí, API Gateway ya lo provee. HTTPS para S3 assets - Sí (default). No client-side encryption adicional (complejidad innecesaria para demo). AWS maneja TLS/SSL.

---

**Q17: Client-Side Data Protection**  
How should we protect data on the client?
- Store tokens in localStorage, sessionStorage, or cookies?
- Clear sensitive data on logout?
- Prevent data leakage in browser console?
- XSS protection measures?

[Answer]: localStorage para session_id (persiste entre refreshes). Clear on explicit logout. Console logging OK para demo/debugging. XSS básico: sanitize user input antes de innerHTML. No datos financieros reales en demo.

---

### Accessibility Requirements

**Q18: WCAG Compliance**  
What accessibility level should we target?
- WCAG 2.1 Level A, AA, or AAA?
- Given hackathon timeline, what's realistic?
- Should we prioritize certain accessibility features?
- Screen reader testing required?

[Answer]: Target WCAG 2.1 Level A (básico). Priorizar: semantic HTML, alt text en imágenes, labels en forms. No screen reader testing formal. Best effort accessibility, no compliance certificada. Voice interface ya ayuda con accesibilidad.

---

**Q19: Keyboard Navigation**  
What keyboard navigation support is needed?
- Full keyboard navigation (tab, enter, escape)?
- Keyboard shortcuts for common actions?
- Focus management for modals and dialogs?
- Given hackathon, what's minimum acceptable?

[Answer]: Tab navigation básico (todos los botones/inputs accesibles). Enter para submit, Escape para cerrar modals. No keyboard shortcuts custom. Focus management básico en modals (trap focus). Suficiente para demo funcional.

---

**Q20: Visual Accessibility**  
What visual accessibility features are needed?
- Color contrast ratios (WCAG AA: 4.5:1)?
- Support for high contrast mode?
- Font size adjustments?
- Avoid color-only information?

[Answer]: Color contrast 4.5:1 para texto principal (usar dark text on light background). No high contrast mode custom. Font size: usar rem units (respeta browser settings). Icons + text labels (no color-only). Diseño limpio y legible.

---

### Tech Stack Decisions

**Q21: JavaScript Framework**  
Should we use a JavaScript framework or vanilla JS?
- React, Vue, Svelte, or vanilla JS?
- Given hackathon timeline (8 hours), what's fastest?
- Team familiarity with frameworks?
- Build complexity vs development speed?

[Answer]: Vanilla JavaScript ES6+ (más rápido para hackathon, no build process). Modular structure con classes. No framework overhead. Single HTML file con inline/external JS. Prioridad: funcionalidad working sobre arquitectura elegante.

---

**Q22: CSS Framework**  
Should we use a CSS framework?
- Bootstrap, Tailwind, Material UI, or custom CSS?
- Given hackathon timeline, what's fastest?
- Mobile responsiveness out of the box?
- Component library for faster development?

[Answer]: Bootstrap 5 via CDN (rápido, no build, responsive out-of-the-box). Componentes pre-built (buttons, modals, cards). Custom CSS solo para específicos. Mobile-first grid system. Icons: Bootstrap Icons via CDN.

---

**Q23: Build and Bundling**  
Do we need a build process?
- Webpack, Vite, Parcel, or no bundler?
- Transpilation (Babel) for older browsers?
- Minification and optimization?
- Given hackathon, can we skip build process?

[Answer]: NO build process (ahorra tiempo setup). ES6+ directo (Chrome moderno lo soporta). No transpilation. No minification (archivos pequeños OK para demo). Deploy directo a S3. Desarrollo = Producción.

---

**Q24: Testing Strategy**  
What testing is required?
- Unit tests (Jest, Vitest)?
- Integration tests?
- E2E tests (Playwright, Cypress)?
- Given hackathon, manual testing only?

[Answer]: Manual testing only (pragmático para hackathon). No automated tests. Testing checklist: WebSocket connect, voice record/play, chat send/receive, image upload, transaction confirm, product catalog. Browser testing en Chrome + mobile.

---

### Reliability Requirements

**Q25: Error Handling Strategy**  
How should we handle errors?
- Toast notifications, modal dialogs, or inline messages?
- Error logging to console or external service?
- User-friendly error messages vs technical details?
- Retry mechanisms for failed operations?

[Answer]: Toast notifications (Bootstrap toasts) para errores no-críticos. Modal dialogs para errores críticos (WebSocket failed). Console logging para debugging. User-friendly messages + technical details en console. Retry button en toasts.

---

**Q26: Monitoring and Logging**  
What monitoring is needed?
- Client-side error tracking (Sentry, CloudWatch RUM)?
- Performance monitoring (Web Vitals)?
- User analytics (Google Analytics)?
- Given hackathon, console logging only?

[Answer]: Console logging only (suficiente para demo). No external monitoring services. Structured console logs: console.log('[WebSocket]', ...), console.error('[Error]', ...). Browser DevTools para debugging durante demo.

---

**Q27: Graceful Degradation**  
How should we handle degraded scenarios?
- WebSocket unavailable (fallback to HTTP polling)?
- Voice features unavailable (text-only mode)?
- Image upload unavailable (skip images)?
- Show feature availability status to user?

[Answer]: WebSocket unavailable: mostrar error, no fallback. Voice unavailable: hide voice button, text-only mode. Image upload unavailable: hide upload button. Feature detection on page load, show/hide features accordingly. Status indicator: "Voice: ✓" o "Voice: ✗".

---

## Success Criteria

- [x] All NFR questions answered
- [x] Performance requirements defined
- [x] Scalability requirements defined
- [x] Availability requirements defined
- [x] Browser compatibility defined
- [x] Security requirements defined
- [x] Accessibility requirements defined
- [x] Tech stack decisions made
- [x] Reliability requirements defined
- [x] User approval obtained

---

**Plan Status**: COMPLETED  
**Completion Date**: 2026-02-17T15:30:00Z  
**Total Questions**: 27 questions across 8 NFR categories  
**Artifacts Generated**:
- `nfr-requirements.md` - Complete NFR requirements with acceptance criteria
- `tech-stack-decisions.md` - Tech stack decisions with rationale and implementation details
