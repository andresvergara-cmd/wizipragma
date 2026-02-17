// Application State Management
// Simple state management with observer pattern

class AppState {
  constructor() {
    this.state = {
      // Connection
      connectionStatus: 'disconnected', // disconnected, connecting, connected, error
      reconnectAttempts: 0,
      
      // User
      user: {
        id: null,
        sessionId: null,
        token: null
      },
      
      // Chat
      messages: [],
      isTyping: false,
      
      // Voice
      isRecording: false,
      isPlaying: false,
      voiceAvailable: false,
      
      // Image
      isUploading: false,
      uploadProgress: 0,
      
      // Transaction
      currentTransaction: null,
      
      // Product Catalog
      products: [],
      selectedProduct: null,
      
      // UI
      currentView: 'login', // login, chat
      error: null
    };
    
    this.listeners = [];
  }

  // Get current state
  getState() {
    return { ...this.state };
  }

  // Update state and notify listeners
  setState(updates) {
    this.state = { ...this.state, ...updates };
    this.notifyListeners();
  }

  // Update nested state (e.g., user.id)
  setNestedState(path, value) {
    const keys = path.split('.');
    const newState = { ...this.state };
    let current = newState;
    
    for (let i = 0; i < keys.length - 1; i++) {
      current[keys[i]] = { ...current[keys[i]] };
      current = current[keys[i]];
    }
    
    current[keys[keys.length - 1]] = value;
    this.state = newState;
    this.notifyListeners();
  }

  // Subscribe to state changes
  subscribe(listener) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  // Notify all listeners
  notifyListeners() {
    this.listeners.forEach(listener => {
      try {
        listener(this.state);
      } catch (error) {
        Logger.error('AppState', 'Error in state listener', error);
      }
    });
  }

  // Add message to chat history
  addMessage(message) {
    const messages = [...this.state.messages, message];
    
    // Keep only last MAX_MESSAGE_HISTORY messages
    if (messages.length > CONFIG.MAX_MESSAGE_HISTORY) {
      messages.shift();
    }
    
    this.setState({ messages });
  }

  // Clear messages
  clearMessages() {
    this.setState({ messages: [] });
  }

  // Reset state (logout)
  reset() {
    this.state = {
      connectionStatus: 'disconnected',
      reconnectAttempts: 0,
      user: { id: null, sessionId: null, token: null },
      messages: [],
      isTyping: false,
      isRecording: false,
      isPlaying: false,
      voiceAvailable: false,
      isUploading: false,
      uploadProgress: 0,
      currentTransaction: null,
      products: [],
      selectedProduct: null,
      currentView: 'login',
      error: null
    };
    this.notifyListeners();
  }
}

// Make AppState globally available
window.AppState = AppState;
