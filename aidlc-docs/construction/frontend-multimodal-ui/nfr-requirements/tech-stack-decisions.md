# Tech Stack Decisions - Unit 4: Frontend Multimodal UI

## Document Information
- **Unit**: Frontend Multimodal UI
- **Created**: 2026-02-17
- **Context**: 8-hour hackathon, demo quality
- **Decision Criteria**: Speed of development, simplicity, no build complexity

---

## 1. JavaScript Framework Decision

### Decision: Vanilla JavaScript ES6+

**Options Considered**:
- React
- Vue
- Svelte
- Vanilla JavaScript ES6+

**Selected**: Vanilla JavaScript ES6+

**Rationale**:
- ✅ **Fastest for hackathon**: No setup, no build process, no learning curve
- ✅ **No dependencies**: Works immediately in modern browsers
- ✅ **Modular structure**: ES6 classes and modules provide organization
- ✅ **Direct control**: No framework abstractions to debug
- ✅ **Single file deployment**: Can inline everything if needed

**Trade-offs**:
- ❌ No reactive data binding (manual DOM updates)
- ❌ No component reusability (acceptable for small app)
- ❌ More verbose code (acceptable for 8-hour timeline)

**Implementation Approach**:
```javascript
// Modular class-based structure
class WebSocketManager { ... }
class VoiceManager { ... }
class ChatManager { ... }
class ImageManager { ... }
class TransactionManager { ... }
class ProductCatalogManager { ... }

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const app = new App();
  app.init();
});
```

---

## 2. CSS Framework Decision

### Decision: Bootstrap 5 via CDN

**Options Considered**:
- Bootstrap 5
- Tailwind CSS
- Material UI
- Custom CSS

**Selected**: Bootstrap 5 via CDN

**Rationale**:
- ✅ **Zero setup**: Include via CDN link, works immediately
- ✅ **Responsive out-of-the-box**: Mobile-first grid system
- ✅ **Pre-built components**: Buttons, modals, cards, toasts, forms
- ✅ **Icons included**: Bootstrap Icons via CDN
- ✅ **Well-documented**: Easy to reference during hackathon
- ✅ **No build process**: No compilation needed

**Trade-offs**:
- ❌ Larger file size than custom CSS (acceptable with CDN caching)
- ❌ Generic look (can customize with additional CSS)

**Implementation**:
```html
<!-- Bootstrap CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Bootstrap Icons -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">

<!-- Bootstrap JS Bundle (includes Popper) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Custom CSS for specific overrides -->
<style>
  /* Custom styles here */
</style>
```

**Key Components to Use**:
- Grid system (container, row, col)
- Buttons (btn, btn-primary, btn-secondary)
- Cards (card, card-body)
- Modals (modal, modal-dialog)
- Toasts (toast, toast-container)
- Forms (form-control, form-label)
- Spinners (spinner-border)

---

## 3. Build and Bundling Decision

### Decision: NO Build Process

**Options Considered**:
- Webpack
- Vite
- Parcel
- No bundler

**Selected**: No bundler

**Rationale**:
- ✅ **Saves setup time**: No configuration files, no dependencies
- ✅ **Development = Production**: What you write is what deploys
- ✅ **ES6 modules work natively**: Modern browsers support ES6 imports
- ✅ **Faster iteration**: Edit and refresh, no build step
- ✅ **Simpler debugging**: No source maps needed

**Trade-offs**:
- ❌ No transpilation (requires modern browser)
- ❌ No minification (files slightly larger, acceptable for demo)
- ❌ No tree shaking (not needed for small app)

**Implementation**:
```html
<!-- Option 1: Single file with inline JS -->
<script>
  // All JavaScript here
</script>

<!-- Option 2: External JS files -->
<script type="module" src="js/app.js"></script>
<script type="module" src="js/websocket-manager.js"></script>
<script type="module" src="js/voice-manager.js"></script>
```

**Deployment**:
- Upload HTML, CSS, JS files directly to S3
- No build artifacts, no dist folder
- Source code = deployed code

---

## 4. Testing Strategy Decision

### Decision: Manual Testing Only

**Options Considered**:
- Jest (unit tests)
- Vitest (unit tests)
- Playwright (E2E tests)
- Cypress (E2E tests)
- Manual testing

**Selected**: Manual testing only

**Rationale**:
- ✅ **Pragmatic for hackathon**: 8 hours too short for test setup
- ✅ **Focus on functionality**: Working demo > test coverage
- ✅ **Simple testing checklist**: Systematic manual testing sufficient

**Trade-offs**:
- ❌ No automated regression testing (acceptable for one-time demo)
- ❌ Manual effort for each test cycle (acceptable for short timeline)

**Testing Checklist**:
```markdown
## Manual Testing Checklist

### WebSocket Connection
- [ ] Connect on page load
- [ ] Reconnect after disconnect
- [ ] Show connection status
- [ ] Queue messages while disconnected

### Voice Input
- [ ] Request microphone permission
- [ ] Start recording on button press
- [ ] Stop recording on button release
- [ ] Send audio to backend
- [ ] Show recording indicator

### Voice Output
- [ ] Receive audio from backend
- [ ] Play audio automatically
- [ ] Show playback controls
- [ ] Handle playback errors

### Chat Interface
- [ ] Send text message
- [ ] Receive text response
- [ ] Display message history
- [ ] Auto-scroll to latest
- [ ] Show typing indicator

### Image Upload
- [ ] Select image from file picker
- [ ] Show image preview
- [ ] Compress image client-side
- [ ] Upload to backend
- [ ] Show upload progress

### Transaction Confirmation
- [ ] Display transaction details
- [ ] Confirm transaction
- [ ] Cancel transaction
- [ ] Show receipt

### Product Catalog
- [ ] Display product list
- [ ] Filter products
- [ ] View product details
- [ ] Show benefits

### Error Handling
- [ ] Show error toasts
- [ ] Show retry buttons
- [ ] Handle WebSocket errors
- [ ] Handle API errors

### Browser Testing
- [ ] Chrome desktop (primary)
- [ ] Chrome mobile
- [ ] Safari mobile (iOS)
```

---

## 5. Browser APIs Decision

### 5.1 WebSocket API

**Decision**: Native WebSocket API

**Rationale**:
- ✅ Built into all modern browsers
- ✅ No library needed
- ✅ Simple API
- ✅ Sufficient for our needs

**Implementation**:
```javascript
class WebSocketManager {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => this.onOpen();
    this.ws.onmessage = (event) => this.onMessage(event);
    this.ws.onclose = () => this.onClose();
    this.ws.onerror = (error) => this.onError(error);
  }

  send(message) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      this.queueMessage(message);
    }
  }
}
```

---

### 5.2 MediaRecorder API

**Decision**: Native MediaRecorder API

**Rationale**:
- ✅ Built into modern browsers
- ✅ Records audio directly
- ✅ WebM format supported
- ✅ No library needed

**Fallback**: Hide voice button if unavailable

**Implementation**:
```javascript
class VoiceManager {
  async startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    this.mediaRecorder = new MediaRecorder(stream);
    this.audioChunks = [];

    this.mediaRecorder.ondataavailable = (event) => {
      this.audioChunks.push(event.data);
    };

    this.mediaRecorder.onstop = () => {
      const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
      this.sendAudio(audioBlob);
    };

    this.mediaRecorder.start();
  }

  stopRecording() {
    this.mediaRecorder.stop();
  }
}
```

---

### 5.3 Audio API

**Decision**: HTML5 Audio Element

**Rationale**:
- ✅ Simple playback
- ✅ Built-in controls
- ✅ No library needed

**Implementation**:
```javascript
class VoiceManager {
  playAudio(audioUrl) {
    const audio = new Audio(audioUrl);
    audio.play();
  }
}
```

---

### 5.4 Canvas API

**Decision**: Canvas API for Image Compression

**Rationale**:
- ✅ Client-side image resizing
- ✅ Reduces upload size
- ✅ Built into browsers

**Implementation**:
```javascript
class ImageManager {
  compressImage(file, maxWidth, maxHeight, quality) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          let width = img.width;
          let height = img.height;

          if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
          }
          if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
          }

          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, width, height);

          canvas.toBlob((blob) => resolve(blob), 'image/jpeg', quality);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }
}
```

---

## 6. State Management Decision

### Decision: Simple Object-Based State

**Rationale**:
- ✅ No library needed
- ✅ Sufficient for small app
- ✅ Easy to understand

**Implementation**:
```javascript
class AppState {
  constructor() {
    this.state = {
      connectionStatus: 'disconnected', // disconnected, connecting, connected
      messages: [],
      isRecording: false,
      isPlaying: false,
      currentTransaction: null,
      products: [],
      selectedProduct: null,
      user: {
        id: null,
        sessionId: null
      }
    };
    this.listeners = [];
  }

  setState(updates) {
    this.state = { ...this.state, ...updates };
    this.notifyListeners();
  }

  getState() {
    return this.state;
  }

  subscribe(listener) {
    this.listeners.push(listener);
  }

  notifyListeners() {
    this.listeners.forEach(listener => listener(this.state));
  }
}
```

---

## 7. Deployment Strategy Decision

### Decision: Direct S3 Static Website Hosting

**Rationale**:
- ✅ Simple deployment
- ✅ No server needed
- ✅ HTTPS by default
- ✅ Fast for demo

**Skip CloudFront**: Saves setup time, S3 sufficient for demo

**Implementation**:
```bash
# Upload to S3 bucket (from Unit 1)
aws s3 cp frontend/ s3://centli-frontend-bucket/ --recursive --profile 777937796305_Ps-HackatonAgentic-Mexico

# Enable static website hosting
aws s3 website s3://centli-frontend-bucket/ --index-document index.html --profile 777937796305_Ps-HackatonAgentic-Mexico
```

**URL Structure**:
- S3 Website URL: `http://centli-frontend-bucket.s3-website-us-east-1.amazonaws.com`
- Or via S3 HTTPS: `https://centli-frontend-bucket.s3.amazonaws.com/index.html`

---

## 8. Logging and Debugging Decision

### Decision: Console Logging Only

**Rationale**:
- ✅ Built into browsers
- ✅ No external service setup
- ✅ Sufficient for demo debugging

**Implementation**:
```javascript
class Logger {
  static log(category, message, data = null) {
    console.log(`[${category}]`, message, data || '');
  }

  static error(category, message, error = null) {
    console.error(`[${category}]`, message, error || '');
  }

  static warn(category, message, data = null) {
    console.warn(`[${category}]`, message, data || '');
  }
}

// Usage
Logger.log('WebSocket', 'Connected successfully');
Logger.error('Voice', 'MediaRecorder not supported', error);
```

---

## 9. Authentication Decision

### Decision: Mock Authentication with Simple Form

**Rationale**:
- ✅ Focus on multimodal features, not auth
- ✅ Sufficient for demo
- ✅ Fast to implement

**Implementation**:
```html
<!-- Simple login form -->
<div id="login-screen">
  <h2>CENTLI Banking Assistant</h2>
  <input type="text" id="user-id" placeholder="Ingresa tu ID de usuario">
  <button onclick="login()">Iniciar Sesión</button>
</div>

<script>
function login() {
  const userId = document.getElementById('user-id').value;
  if (userId) {
    localStorage.setItem('user_id', userId);
    // Generate simple session ID
    const sessionId = 'session_' + Date.now();
    localStorage.setItem('session_id', sessionId);
    // Hide login, show app
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('app').style.display = 'block';
    // Connect WebSocket
    app.connect();
  }
}
</script>
```

---

## 10. Summary of Tech Stack

### Core Technologies
- **Language**: JavaScript ES6+
- **CSS Framework**: Bootstrap 5 (via CDN)
- **Icons**: Bootstrap Icons (via CDN)
- **Build Process**: None
- **Testing**: Manual only

### Browser APIs
- **WebSocket API**: Real-time communication
- **MediaRecorder API**: Voice input
- **Audio Element**: Voice output
- **Canvas API**: Image compression
- **FileReader API**: Image preview
- **localStorage API**: Session persistence

### Development Tools
- **Editor**: Any text editor
- **Browser**: Chrome DevTools
- **Testing**: Manual checklist
- **Deployment**: AWS CLI for S3 upload

### External Dependencies
- **Bootstrap 5**: CSS framework (CDN)
- **Bootstrap Icons**: Icon library (CDN)
- **None**: No npm packages, no build tools

---

## 11. File Structure

```
frontend/
├── index.html                      # Main HTML file (single page)
├── css/
│   └── custom.css                  # Custom styles (optional)
├── js/
│   ├── app.js                      # Main application
│   ├── websocket-manager.js        # WebSocket handling
│   ├── voice-manager.js            # Voice input/output
│   ├── chat-manager.js             # Chat interface
│   ├── image-manager.js            # Image upload
│   ├── transaction-manager.js      # Transaction confirmation
│   ├── product-catalog-manager.js  # Product catalog
│   ├── app-state.js                # State management
│   └── logger.js                   # Logging utility
└── README.md                       # Setup instructions
```

**Alternative**: Single `index.html` file with all CSS/JS inline for simplest deployment.

---

## 12. Decision Summary Table

| Category | Decision | Rationale |
|----------|----------|-----------|
| **JavaScript** | Vanilla ES6+ | No build process, fastest for hackathon |
| **CSS** | Bootstrap 5 CDN | Pre-built components, responsive |
| **Build** | None | Saves time, direct deployment |
| **Testing** | Manual only | Pragmatic for 8-hour timeline |
| **WebSocket** | Native API | Built-in, no library needed |
| **Voice Input** | MediaRecorder API | Native, WebM format |
| **Voice Output** | Audio Element | Simple playback |
| **Images** | Canvas API | Client-side compression |
| **State** | Simple object | No library needed |
| **Deployment** | S3 Static | Simple, fast, HTTPS |
| **Logging** | Console only | Built-in, sufficient for demo |
| **Auth** | Mock form | Focus on multimodal features |

---

**Document Status**: Complete  
**Next Stage**: Infrastructure Design or Code Generation
