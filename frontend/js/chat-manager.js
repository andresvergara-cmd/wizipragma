// Chat Manager
// Handles chat interface and message display

class ChatManager {
  constructor(appState) {
    this.appState = appState;
    this.messageContainer = null;
    this.messageInput = null;
    this.sendButton = null;
  }

  // Initialize chat UI
  init() {
    this.messageContainer = document.getElementById('message-container');
    this.messageInput = document.getElementById('message-input');
    this.sendButton = document.getElementById('send-button');
    
    // Subscribe to state changes
    this.appState.subscribe((state) => {
      this.renderMessages(state.messages);
      this.updateTypingIndicator(state.isTyping);
    });
    
    // Setup event listeners
    this.sendButton.addEventListener('click', () => this.sendMessage());
    this.messageInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
    
    Logger.log('Chat', 'Chat manager initialized');
  }

  // Send text message
  sendMessage() {
    const text = this.messageInput.value.trim();
    
    if (!text) {
      return;
    }
    
    const state = this.appState.getState();
    
    if (state.connectionStatus !== 'connected') {
      this.showToast('No conectado al servidor', 'error');
      return;
    }
    
    // Add user message to chat
    this.appState.addMessage({
      id: Date.now(),
      sender: 'user',
      type: 'text',
      content: text,
      timestamp: new Date()
    });
    
    // Clear input
    this.messageInput.value = '';
    
    // Send to backend
    window.wsManager.send({
      action: 'message',
      content: text,
      user_id: state.user.id,
      session_id: state.user.sessionId
    });
    
    // Show typing indicator
    this.appState.setState({ isTyping: true });
    
    Logger.log('Chat', 'Message sent', text);
  }

  // Render messages
  renderMessages(messages) {
    if (!this.messageContainer) return;
    
    this.messageContainer.innerHTML = '';
    
    messages.forEach(message => {
      const messageEl = this.createMessageElement(message);
      this.messageContainer.appendChild(messageEl);
    });
    
    // Auto-scroll to bottom
    this.scrollToBottom();
  }

  // Create message element
  createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message message-${message.sender}`;
    div.setAttribute('data-testid', `chat-message-${message.id}`);
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = message.content;
    
    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = this.formatTime(message.timestamp);
    
    div.appendChild(content);
    div.appendChild(time);
    
    return div;
  }

  // Update typing indicator
  updateTypingIndicator(isTyping) {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
      indicator.style.display = isTyping ? 'block' : 'none';
    }
  }

  // Scroll to bottom
  scrollToBottom() {
    if (this.messageContainer) {
      this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
  }

  // Format timestamp
  formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' });
  }

  // Show toast notification
  showToast(message, type = 'info') {
    window.dispatchEvent(new CustomEvent('show-toast', { 
      detail: { message, type }
    }));
  }
}

// Make ChatManager globally available
window.ChatManager = ChatManager;
