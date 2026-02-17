# UI Components - Unit 4: Frontend Multimodal UI

## Overview

This document defines the UI component structure, responsibilities, and state management for the CENTLI frontend.

---

## 1. Component Architecture

### 1.1 Component Hierarchy

```
App (index.html)
├── ConnectionStatusBar
├── ChatContainer
│   ├── MessageList
│   │   ├── MessageBubble (user/bot)
│   │   ├── VoiceMessage
│   │   ├── ImageMessage
│   │   ├── TransactionCard
│   │   └── ProductCard
│   ├── TypingIndicator
│   └── ScrollToBottomButton
├── InputContainer
│   ├── TextInput
│   ├── SendButton
│   ├── VoiceButton
│   └── ImageButton
├── VoiceRecordingOverlay
├── TransactionConfirmationModal
├── ProductCatalogModal
├── ReceiptModal
└── NotificationToast
```

---

## 2. Core Components

### 2.1 WebSocketManager

**Purpose**: Manage WebSocket connection lifecycle and message handling

**Responsibilities**:
- Establish and maintain WebSocket connection
- Handle connection events (open, close, error, message)
- Implement auto-reconnection logic
- Queue messages during disconnection
- Persist session data

**State**:
```javascript
{
  status: 'disconnected' | 'connecting' | 'connected' | 'reconnecting' | 'error',
  reconnectAttempts: 0,
  maxReconnectAttempts: 3,
  messageQueue: [],
  sessionData: {
    session_id: string,
    user_id: string,
    token: string
  }
}
```

**Methods**:
- `connect(url, token)` - Establish WebSocket connection
- `disconnect()` - Close connection gracefully
- `sendMessage(message)` - Send message (queue if disconnected)
- `onMessage(callback)` - Register message handler
- `reconnect()` - Attempt reconnection
- `getStatus()` - Get current connection status

**Events**:
- `onConnected` - Fired when connection established
- `onDisconnected` - Fired when connection lost
- `onMessage` - Fired when message received
- `onError` - Fired on connection error

---

### 2.2 VoiceManager

**Purpose**: Handle voice input recording and output playback

**Responsibilities**:
- Request microphone permission
- Record audio using MediaRecorder API
- Convert audio to base64 for transmission
- Play received audio responses
- Manage recording/playback state

**State**:
```javascript
{
  recordingState: 'idle' | 'recording' | 'processing',
  playbackState: 'idle' | 'playing' | 'paused',
  mediaRecorder: MediaRecorder | null,
  audioChunks: Blob[],
  currentAudio: HTMLAudioElement | null,
  recordingDuration: number,
  hasPermission: boolean
}
```

**Methods**:
- `requestPermission()` - Request microphone access
- `startRecording()` - Start audio recording
- `stopRecording()` - Stop recording and return audio blob
- `cancelRecording()` - Cancel recording without saving
- `playAudio(audioData)` - Play audio from base64 data
- `pauseAudio()` - Pause current playback
- `stopAudio()` - Stop current playback

**Configuration**:
```javascript
{
  audioFormat: 'audio/webm',
  sampleRate: 16000,
  maxDuration: 60000, // 60 seconds
  audioBitsPerSecond: 128000
}
```

---

### 2.3 ChatManager

**Purpose**: Manage chat message display and history

**Responsibilities**:
- Render message list
- Add new messages (user and bot)
- Handle auto-scroll behavior
- Persist chat history to localStorage
- Render different message types

**State**:
```javascript
{
  messages: [
    {
      id: string,
      type: 'text' | 'voice' | 'image' | 'transaction' | 'product',
      sender: 'user' | 'bot',
      content: string | object,
      timestamp: string,
      status: 'sending' | 'sent' | 'error'
    }
  ],
  isAtBottom: boolean,
  isTyping: boolean
}
```

**Methods**:
- `addMessage(message)` - Add message to chat
- `updateMessage(id, updates)` - Update existing message
- `clearChat()` - Clear all messages
- `loadHistory()` - Load from localStorage
- `saveHistory()` - Save to localStorage
- `scrollToBottom()` - Scroll chat to bottom
- `showTypingIndicator()` - Show bot typing
- `hideTypingIndicator()` - Hide bot typing

**Message Types**:
- **Text**: Simple text message
- **Voice**: Audio message with transcript
- **Image**: Image with thumbnail
- **Transaction**: Transaction confirmation/receipt
- **Product**: Product card with details

---

### 2.4 ImageManager

**Purpose**: Handle image selection, preview, and upload

**Responsibilities**:
- Open file picker
- Validate image files
- Show image preview
- Compress images client-side
- Convert to base64 for transmission

**State**:
```javascript
{
  selectedImage: File | null,
  previewUrl: string | null,
  isCompressing: boolean,
  uploadProgress: number
}
```

**Methods**:
- `selectImage()` - Open file picker
- `validateImage(file)` - Validate file type and size
- `showPreview(file)` - Show image preview modal
- `compressImage(file)` - Compress image
- `uploadImage(file)` - Convert and send image
- `cancelUpload()` - Cancel current upload

**Validation Rules**:
```javascript
{
  allowedTypes: ['image/jpeg', 'image/png', 'image/gif'],
  maxFileSize: 5 * 1024 * 1024, // 5MB
  maxDimensions: { width: 1024, height: 1024 },
  compressionQuality: 0.8
}
```

---

### 2.5 TransactionManager

**Purpose**: Display transaction confirmations and receipts

**Responsibilities**:
- Show transaction confirmation modal
- Display transaction details
- Handle user confirmation/cancellation
- Show receipt after successful transaction

**State**:
```javascript
{
  currentTransaction: {
    id: string,
    type: 'transfer' | 'purchase',
    amount: number,
    currency: string,
    source: string,
    destination: string,
    fees: number,
    total: number,
    details: object
  } | null,
  isConfirming: boolean,
  showReceipt: boolean
}
```

**Methods**:
- `showConfirmation(transaction)` - Show confirmation modal
- `confirmTransaction()` - Send confirmation to backend
- `cancelTransaction()` - Cancel transaction
- `showReceipt(transaction)` - Show receipt modal
- `closeReceipt()` - Close receipt modal

**UI Components**:
- Confirmation modal with transaction details
- Receipt modal with transaction summary
- Loading indicator during processing

---

### 2.6 ProductCatalogManager

**Purpose**: Display and manage product catalog

**Responsibilities**:
- Render product grid
- Handle product filtering
- Show product details
- Manage purchase flow

**State**:
```javascript
{
  products: [
    {
      id: string,
      name: string,
      description: string,
      price: number,
      image_url: string,
      category: string,
      benefits: [
        {
          id: string,
          type: 'cashback' | 'msi' | 'discount',
          value: number,
          description: string
        }
      ]
    }
  ],
  selectedProduct: object | null,
  selectedCategory: string | null,
  isLoading: boolean
}
```

**Methods**:
- `loadProducts()` - Fetch product list
- `filterByCategory(category)` - Filter products
- `showProductDetails(productId)` - Show detail modal
- `selectBenefits(benefits)` - Select benefits for purchase
- `initiatePurchase(product, benefits)` - Start purchase flow

**UI Components**:
- Product grid (responsive)
- Product card (image, name, price, benefits)
- Product detail modal
- Benefits selector
- Purchase confirmation

---

## 3. Shared UI Components

### 3.1 ConnectionStatusBar

**Purpose**: Display WebSocket connection status

**Props**:
- `status`: Connection status
- `reconnectAttempts`: Current retry count

**UI States**:
- Connected: Green indicator, "Connected"
- Connecting: Yellow indicator, "Connecting..."
- Reconnecting: Yellow indicator, "Reconnecting (attempt X/3)"
- Disconnected: Red indicator, "Disconnected"
- Error: Red indicator, "Connection error"

---

### 3.2 MessageBubble

**Purpose**: Display individual chat message

**Props**:
- `message`: Message object
- `sender`: 'user' | 'bot'
- `type`: Message type

**Variants**:
- User message: Right-aligned, blue background
- Bot message: Left-aligned, gray background
- Voice message: With play button
- Image message: With thumbnail
- Transaction: With card layout
- Product: With product card

---

### 3.3 TypingIndicator

**Purpose**: Show bot typing animation

**UI**: Three animated dots (...)

---

### 3.4 NotificationToast

**Purpose**: Display temporary notifications

**Props**:
- `message`: Notification text
- `type`: 'success' | 'error' | 'info' | 'warning'
- `duration`: Auto-dismiss duration (default: 3000ms)

**Position**: Top-right corner

**Variants**:
- Success: Green background, checkmark icon
- Error: Red background, X icon
- Info: Blue background, info icon
- Warning: Yellow background, warning icon

---

### 3.5 Modal

**Purpose**: Reusable modal dialog

**Props**:
- `title`: Modal title
- `content`: Modal content (HTML)
- `onClose`: Close callback
- `showCloseButton`: Show X button (default: true)

**Features**:
- Semi-transparent overlay
- Centered on screen
- Responsive (full-screen on mobile)
- ESC key to close
- Click outside to close

---

## 4. State Management

### 4.1 Application State

**Global State** (stored in App):
```javascript
{
  // Connection
  connectionStatus: string,
  sessionData: object,
  
  // Chat
  messages: array,
  isTyping: boolean,
  
  // Voice
  isRecording: boolean,
  isPlayingAudio: boolean,
  
  // UI
  activeModal: string | null,
  notifications: array,
  
  // Data
  currentTransaction: object | null,
  products: array,
  selectedProduct: object | null
}
```

---

### 4.2 Local Storage

**Persisted Data**:
```javascript
{
  // Session
  'centli_session': {
    session_id: string,
    user_id: string,
    token: string,
    timestamp: string
  },
  
  // Chat History
  'centli_chat_history': [messages],
  
  // User Preferences
  'centli_preferences': {
    theme: 'light' | 'dark',
    voiceEnabled: boolean,
    notificationsEnabled: boolean
  }
}
```

---

### 4.3 Component Communication

**Event-Driven Architecture**:

```javascript
// Custom Events
const events = {
  // WebSocket
  'ws:connected': {},
  'ws:disconnected': {},
  'ws:message': { message },
  'ws:error': { error },
  
  // Chat
  'chat:message-sent': { message },
  'chat:message-received': { message },
  
  // Voice
  'voice:recording-started': {},
  'voice:recording-stopped': { audioBlob },
  'voice:playback-started': {},
  'voice:playback-ended': {},
  
  // Transaction
  'transaction:confirmation-requested': { transaction },
  'transaction:confirmed': { transaction },
  'transaction:cancelled': {},
  
  // UI
  'ui:modal-opened': { modalType },
  'ui:modal-closed': {},
  'ui:notification': { message, type }
};
```

**Usage**:
```javascript
// Dispatch event
document.dispatchEvent(new CustomEvent('ws:message', { 
  detail: { message } 
}));

// Listen to event
document.addEventListener('ws:message', (e) => {
  handleMessage(e.detail.message);
});
```

---

## 5. Component Lifecycle

### 5.1 Initialization Sequence

```
1. Load index.html
2. Initialize App
3. Load session from localStorage
4. Initialize WebSocketManager
5. Connect to WebSocket
6. Initialize VoiceManager (request permission)
7. Initialize ChatManager (load history)
8. Render UI
9. Enable user interactions
```

---

### 5.2 Cleanup on Page Unload

```
1. Save chat history to localStorage
2. Save session data
3. Close WebSocket connection gracefully
4. Stop any active audio playback
5. Cancel any pending operations
```

---

## Success Criteria

- [x] All UI components defined with responsibilities
- [x] Component state management specified
- [x] Component methods documented
- [x] Component communication patterns defined
- [x] Lifecycle and initialization documented

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17  
**Next Step**: Generate UI Validation Rules document
