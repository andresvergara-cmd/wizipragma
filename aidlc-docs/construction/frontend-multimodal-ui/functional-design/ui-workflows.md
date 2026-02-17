# UI Workflows - Unit 4: Frontend Multimodal UI

## Overview

This document defines the user interface workflows for the CENTLI multimodal banking assistant frontend.

---

## 1. WebSocket Connection Workflow

### 1.1 Initial Connection

```
Flow:
1. User opens application (index.html)
2. UI loads and initializes WebSocketManager
3. Check localStorage for existing session token
4. If token exists and valid:
   - Use existing token
5. If no token or expired:
   - Generate new JWT token (for demo: mock token)
6. Establish WebSocket connection:
   - URL: wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod
   - Query param: ?token={jwt_token}
7. Show connection status indicator (connecting...)
8. On successful connection:
   - Update status indicator (connected)
   - Enable UI controls
   - Load chat history from localStorage
9. On connection error:
   - Show error notification
   - Retry connection (max 3 attempts)
```

**UI Elements**:
- Connection status indicator (top bar)
- Loading spinner during connection
- Error toast for connection failures

---

### 1.2 Auto-Reconnection

```
Flow:
1. WebSocket connection drops (network issue, server restart)
2. Update status indicator (disconnected)
3. Disable UI controls (prevent user actions)
4. Queue any pending messages in memory
5. Attempt reconnection:
   - Retry 1: Immediate
   - Retry 2: After 2 seconds
   - Retry 3: After 5 seconds
6. If reconnection successful:
   - Update status indicator (connected)
   - Enable UI controls
   - Send queued messages
7. If all retries fail:
   - Show error modal
   - Provide manual reconnect button
```

**UI Elements**:
- Reconnecting indicator with retry count
- Queued messages indicator
- Manual reconnect button

---

### 1.3 Session Persistence

```
Flow:
1. On successful connection:
   - Store session data in localStorage:
     * session_id
     * user_id
     * token
     * connection_timestamp
2. On page refresh:
   - Load session data from localStorage
   - Validate token expiration
   - Reconnect with existing session
3. On explicit disconnect (user logout):
   - Clear localStorage
   - Close WebSocket connection
   - Redirect to login/home
```

**Storage Schema**:
```javascript
{
  session_id: "uuid",
  user_id: "test-user-123",
  token: "jwt-token",
  connection_timestamp: "ISO-8601",
  chat_history: [messages]
}
```

---

## 2. Voice Input Workflow

### 2.1 Start Recording

```
Flow:
1. User presses and holds microphone button
2. Request microphone permission (if not granted)
3. If permission denied:
   - Show error notification
   - Disable voice features
4. If permission granted:
   - Initialize MediaRecorder
   - Start recording audio
   - Show recording indicator (pulsing red dot)
   - Show waveform visualization (optional)
   - Start recording timer
5. Capture audio chunks in memory
```

**UI Elements**:
- Microphone button (hold to record)
- Recording indicator (pulsing animation)
- Recording timer (00:00)
- Cancel button (X)

---

### 2.2 Stop Recording & Send

```
Flow:
1. User releases microphone button
2. Stop MediaRecorder
3. Combine audio chunks into single blob
4. Convert to base64 (for WebSocket transmission)
5. Show "Processing..." indicator
6. Send WebSocket message:
   {
     type: "VOICE",
     content: "base64-audio-data",
     metadata: {
       timestamp: "ISO-8601",
       message_id: "uuid",
       user_id: "user-id",
       session_id: "session-id"
     }
   }
7. Add message to chat (user side, voice icon)
8. Wait for response
```

**UI Elements**:
- Processing indicator
- Voice message bubble (user side)

---

### 2.3 Cancel Recording

```
Flow:
1. User clicks cancel button (X) while recording
2. Stop MediaRecorder
3. Discard audio chunks
4. Hide recording indicator
5. Return to idle state
```

---

## 3. Voice Output Workflow

### 3.1 Receive & Play Voice Response

```
Flow:
1. Receive WebSocket message with type "VOICE"
2. Extract base64 audio data
3. Convert base64 to audio blob
4. Create audio URL (blob URL)
5. Add message to chat (bot side, with play button)
6. Auto-play audio:
   - Show playing indicator (animated speaker icon)
   - Update play button to pause button
7. On audio end:
   - Hide playing indicator
   - Reset play button
8. User can replay by clicking play button
```

**UI Elements**:
- Voice message bubble (bot side)
- Play/pause button
- Playing indicator (animated icon)
- Audio progress bar (optional)

---

### 3.2 Text Transcript Display

```
Flow:
1. Voice response always includes text transcript
2. Display text below/alongside voice message
3. User can read transcript while audio plays
4. Transcript remains visible after audio ends
```

**UI Elements**:
- Text transcript (below voice bubble)
- Expandable/collapsible (if long)

---

## 4. Chat Interface Workflow

### 4.1 Send Text Message

```
Flow:
1. User types message in input field
2. User presses Enter or clicks Send button
3. Validate message:
   - Not empty
   - Length <= 500 characters
4. If invalid:
   - Show inline error
   - Keep focus on input
5. If valid:
   - Clear input field
   - Add message to chat (user side)
   - Show typing indicator (bot side)
   - Send WebSocket message:
     {
       type: "TEXT",
       content: "message text",
       metadata: {...}
     }
6. Wait for response
```

**UI Elements**:
- Text input field (with placeholder)
- Send button
- Character counter (optional)
- Typing indicator (three dots animation)

---

### 4.2 Receive Text Response

```
Flow:
1. Receive WebSocket message with type "TEXT"
2. Hide typing indicator
3. Add message to chat (bot side)
4. Auto-scroll to bottom (if user is at bottom)
5. If message contains structured data:
   - Render special components (transaction, product)
```

**UI Elements**:
- Text message bubble (bot side)
- Timestamp
- Special components (transaction card, product card)

---

### 4.3 Chat History & Scroll

```
Flow:
1. On page load:
   - Load chat history from localStorage
   - Render messages in chronological order
   - Scroll to bottom
2. On new message:
   - Append to chat
   - Auto-scroll if user is at bottom
   - Don't scroll if user is reading history
3. On manual scroll:
   - Track scroll position
   - Show "scroll to bottom" button if not at bottom
```

**UI Elements**:
- Chat message list (scrollable)
- Scroll to bottom button (floating)
- Message timestamps

---

## 5. Image Upload Workflow

### 5.1 Select Image

```
Flow:
1. User clicks image upload button
2. Show file picker dialog
3. User selects image file
4. Validate file:
   - Type: JPEG, PNG, GIF
   - Size: <= 5MB
5. If invalid:
   - Show error notification
   - Return to idle
6. If valid:
   - Show image preview modal
   - Show file size and dimensions
   - Provide "Send" and "Cancel" buttons
```

**UI Elements**:
- Image upload button (camera icon)
- File picker dialog
- Image preview modal
- File info display

---

### 5.2 Upload & Send Image

```
Flow:
1. User clicks "Send" in preview modal
2. Compress image (client-side):
   - Max dimensions: 1024x1024
   - Quality: 80%
3. Convert to base64
4. Show upload progress indicator
5. Send WebSocket message:
   {
     type: "IMAGE",
     content: "base64-image-data",
     metadata: {...}
   }
6. Add message to chat (user side, image thumbnail)
7. Close preview modal
8. Wait for response
```

**UI Elements**:
- Upload progress bar
- Image message bubble (user side)
- Image thumbnail (clickable to enlarge)

---

## 6. Transaction Confirmation Workflow

### 6.1 Show Confirmation Dialog

```
Flow:
1. Receive WebSocket message with type "CONFIRMATION"
2. Extract transaction details:
   - Transaction type (transfer, purchase)
   - Amount and currency
   - Source account
   - Destination account/product
   - Fees (if any)
   - Total amount
3. Show modal dialog with details
4. Provide "Confirm" and "Cancel" buttons
5. Disable background UI (modal overlay)
```

**UI Elements**:
- Modal dialog (centered)
- Transaction details card
- Confirm button (primary, green)
- Cancel button (secondary, gray)
- Modal overlay (semi-transparent)

---

### 6.2 Confirm Transaction

```
Flow:
1. User clicks "Confirm" button
2. Disable buttons (prevent double-click)
3. Show processing indicator
4. Send WebSocket message:
   {
     type: "COMMAND",
     content: "CONFIRM_TRANSACTION",
     metadata: {
       transaction_id: "uuid"
     }
   }
5. Wait for response
6. On success:
   - Close confirmation dialog
   - Show receipt modal
7. On error:
   - Show error in dialog
   - Re-enable buttons
```

**UI Elements**:
- Processing spinner
- Success/error notification

---

### 6.3 Show Receipt

```
Flow:
1. Receive transaction success response
2. Show receipt modal with:
   - Transaction ID
   - Date and time
   - Amount and details
   - New balance (if applicable)
   - "Done" button
3. User clicks "Done"
4. Close receipt modal
5. Add receipt to chat history
```

**UI Elements**:
- Receipt modal (styled like paper receipt)
- Transaction details
- Done button

---

## 7. Product Catalog Workflow

### 7.1 Browse Products

```
Flow:
1. User requests product catalog (via chat or button)
2. Receive WebSocket message with type "PRODUCT_CATALOG"
3. Extract product list
4. Show product grid view:
   - Product image
   - Product name
   - Price
   - Benefits badges (cashback, MSI, discount)
5. Provide category filter (optional)
6. User can scroll through products
```

**UI Elements**:
- Product grid (responsive, 2-3 columns)
- Product card (image, name, price, benefits)
- Category filter dropdown
- Loading skeleton (while fetching)

---

### 7.2 View Product Details

```
Flow:
1. User clicks on product card
2. Show product detail modal:
   - Large product image
   - Product name and description
   - Price
   - Available benefits (detailed)
   - "Buy Now" button
   - "Close" button
3. User can view benefit details:
   - Cashback percentage
   - MSI months
   - Discount amount
```

**UI Elements**:
- Product detail modal (full screen on mobile)
- Image gallery (if multiple images)
- Benefits comparison table
- Buy Now button (primary)

---

### 7.3 Purchase Product

```
Flow:
1. User clicks "Buy Now" button
2. Show purchase confirmation:
   - Product details
   - Selected benefits
   - Total amount (with benefits applied)
   - Payment account selector
3. User selects payment account
4. User confirms purchase
5. Send WebSocket message:
   {
     type: "COMMAND",
     content: "PURCHASE_PRODUCT",
     metadata: {
       product_id: "uuid",
       benefits: ["benefit-id-1", "benefit-id-2"],
       payment_account_id: "account-id"
     }
   }
6. Show processing indicator
7. Wait for transaction confirmation workflow
```

**UI Elements**:
- Purchase confirmation dialog
- Payment account selector
- Total amount display
- Confirm purchase button

---

## 8. Error Handling Workflows

### 8.1 Connection Error

```
Flow:
1. WebSocket connection fails or drops
2. Show toast notification: "Connection lost. Reconnecting..."
3. Attempt auto-reconnection (see 1.2)
4. If reconnection fails:
   - Show persistent error banner
   - Provide "Retry" button
```

**UI Elements**:
- Toast notification (top-right)
- Error banner (top of page)
- Retry button

---

### 8.2 Operation Error

```
Flow:
1. Receive error response from server
2. Extract error message and code
3. Show user-friendly error notification:
   - Toast for minor errors
   - Modal for critical errors
4. Provide retry action (if applicable)
5. Log error to console (for debugging)
```

**UI Elements**:
- Error toast (red, with icon)
- Error modal (for critical errors)
- Retry button

---

### 8.3 Validation Error

```
Flow:
1. User input fails validation
2. Show inline error message:
   - Below input field
   - Red border on input
3. Keep focus on input field
4. Clear error on user correction
```

**UI Elements**:
- Inline error message (red text)
- Input field border (red)
- Error icon

---

## 9. Loading States

### 9.1 Initial Page Load

```
Flow:
1. Show loading spinner (centered)
2. Load application resources
3. Initialize WebSocket connection
4. Hide spinner when ready
5. Show main UI
```

**UI Elements**:
- Full-page loading spinner
- CENTLI logo (animated)

---

### 9.2 Operation Loading

```
Flow:
1. User initiates operation (send message, upload image)
2. Show loading indicator:
   - Spinner for short operations (< 2s)
   - Progress bar for long operations (> 2s)
3. Disable UI controls during loading
4. Hide indicator when complete
```

**UI Elements**:
- Inline spinner (next to button)
- Progress bar (for uploads)
- Disabled state (grayed out buttons)

---

## Success Criteria

- [x] All UI workflows documented with step-by-step flows
- [x] User interactions clearly defined
- [x] UI elements specified for each workflow
- [x] Error handling workflows included
- [x] Loading states defined

---

**Document Status**: Complete  
**Last Updated**: 2026-02-17  
**Next Step**: Generate UI Components document
