// WebSocket Manager
// Handles WebSocket connection, reconnection, and message handling

class WebSocketManager {
  constructor(appState) {
    this.appState = appState;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.reconnectTimer = null;
    this.messageQueue = [];
    this.isIntentionalClose = false;
  }

  // Connect to WebSocket
  connect() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      Logger.warn('WebSocket', 'Already connected');
      return;
    }

    this.appState.setState({ connectionStatus: 'connecting' });
    Logger.log('WebSocket', 'Connecting to', CONFIG.WS_URL);

    try {
      this.ws = new WebSocket(CONFIG.WS_URL);
      
      this.ws.onopen = () => this.onOpen();
      this.ws.onmessage = (event) => this.onMessage(event);
      this.ws.onclose = (event) => this.onClose(event);
      this.ws.onerror = (error) => this.onError(error);
    } catch (error) {
      Logger.error('WebSocket', 'Connection error', error);
      this.appState.setState({ 
        connectionStatus: 'error',
        error: 'Failed to connect to server'
      });
    }
  }

  // Handle connection open
  onOpen() {
    Logger.log('WebSocket', 'Connected successfully');
    this.appState.setState({ 
      connectionStatus: 'connected',
      reconnectAttempts: 0,
      error: null
    });
    this.reconnectAttempts = 0;

    // Send authentication message
    const state = this.appState.getState();
    this.send({
      action: 'authenticate',
      user_id: state.user.id,
      session_id: state.user.sessionId,
      token: state.user.token
    });

    // Send queued messages
    this.flushMessageQueue();

    // Show success toast
    this.showToast('Conectado al servidor', 'success');
  }

  // Handle incoming message
  onMessage(event) {
    try {
      const message = JSON.parse(event.data);
      Logger.log('WebSocket', 'Received message', message);

      // Handle different message types
      switch (message.action) {
        case 'authenticated':
          this.handleAuthenticated(message);
          break;
        case 'message':
          this.handleChatMessage(message);
          break;
        case 'voice_response':
          this.handleVoiceResponse(message);
          break;
        case 'image_processed':
          this.handleImageProcessed(message);
          break;
        case 'presigned_url':
          this.handlePresignedUrl(message);
          break;
        case 'transaction_confirmation':
          this.handleTransactionConfirmation(message);
          break;
        case 'product_catalog':
          this.handleProductCatalog(message);
          break;
        case 'error':
          this.handleError(message);
          break;
        default:
          Logger.warn('WebSocket', 'Unknown message action', message.action);
      }
    } catch (error) {
      Logger.error('WebSocket', 'Error parsing message', error);
    }
  }

  // Handle connection close
  onClose(event) {
    Logger.log('WebSocket', 'Connection closed', { code: event.code, reason: event.reason });
    
    if (this.isIntentionalClose) {
      this.appState.setState({ connectionStatus: 'disconnected' });
      this.isIntentionalClose = false;
      return;
    }

    this.appState.setState({ connectionStatus: 'disconnected' });

    // Attempt reconnection
    if (this.reconnectAttempts < CONFIG.WS_RECONNECT_MAX_ATTEMPTS) {
      const delay = CONFIG.WS_RECONNECT_DELAYS[this.reconnectAttempts] || 16000;
      this.reconnectAttempts++;
      
      Logger.log('WebSocket', `Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${CONFIG.WS_RECONNECT_MAX_ATTEMPTS})`);
      this.showToast(`Reconectando... (intento ${this.reconnectAttempts}/${CONFIG.WS_RECONNECT_MAX_ATTEMPTS})`, 'warning');
      
      this.reconnectTimer = setTimeout(() => {
        this.connect();
      }, delay);
    } else {
      Logger.error('WebSocket', 'Max reconnection attempts reached');
      this.appState.setState({ 
        connectionStatus: 'error',
        error: 'No se pudo conectar al servidor. Por favor, recarga la página.'
      });
      this.showToast('Conexión perdida. Recarga la página.', 'error');
    }
  }

  // Handle connection error
  onError(error) {
    Logger.error('WebSocket', 'WebSocket error', error);
  }

  // Send message
  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const messageStr = JSON.stringify(message);
      this.ws.send(messageStr);
      Logger.log('WebSocket', 'Sent message', message);
    } else {
      Logger.warn('WebSocket', 'Not connected, queueing message', message);
      this.queueMessage(message);
    }
  }

  // Queue message for later sending
  queueMessage(message) {
    if (this.messageQueue.length < 10) {
      this.messageQueue.push(message);
    } else {
      Logger.warn('WebSocket', 'Message queue full, dropping message');
    }
  }

  // Send all queued messages
  flushMessageQueue() {
    if (this.messageQueue.length > 0) {
      Logger.log('WebSocket', `Sending ${this.messageQueue.length} queued messages`);
      this.messageQueue.forEach(message => this.send(message));
      this.messageQueue = [];
    }
  }

  // Disconnect
  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.ws) {
      this.isIntentionalClose = true;
      this.ws.close();
      this.ws = null;
    }

    this.reconnectAttempts = 0;
    this.messageQueue = [];
    this.appState.setState({ connectionStatus: 'disconnected' });
    Logger.log('WebSocket', 'Disconnected');
  }

  // Message handlers
  handleAuthenticated(message) {
    Logger.log('WebSocket', 'Authenticated', message);
    this.showToast('Autenticado correctamente', 'success');
  }

  handleChatMessage(message) {
    this.appState.addMessage({
      id: Date.now(),
      sender: 'agent',
      type: 'text',
      content: message.content || message.text,
      timestamp: new Date()
    });
    this.appState.setState({ isTyping: false });
  }

  handleVoiceResponse(message) {
    // Voice manager will handle this
    window.dispatchEvent(new CustomEvent('voice-response', { detail: message }));
  }

  handleImageProcessed(message) {
    this.appState.addMessage({
      id: Date.now(),
      sender: 'agent',
      type: 'text',
      content: message.analysis || 'Imagen procesada correctamente',
      timestamp: new Date()
    });
  }

  handlePresignedUrl(message) {
    // Image manager will handle this
    window.dispatchEvent(new CustomEvent('presigned-url', { detail: message }));
  }

  handleTransactionConfirmation(message) {
    // Transaction manager will handle this
    window.dispatchEvent(new CustomEvent('transaction-confirmation', { detail: message }));
  }

  handleProductCatalog(message) {
    this.appState.setState({ products: message.products || [] });
  }

  handleError(message) {
    Logger.error('WebSocket', 'Server error', message);
    this.showToast(message.message || 'Error del servidor', 'error');
  }

  // Show toast notification
  showToast(message, type = 'info') {
    // This will be implemented in the main app
    window.dispatchEvent(new CustomEvent('show-toast', { 
      detail: { message, type }
    }));
  }
}

// Make WebSocketManager globally available
window.WebSocketManager = WebSocketManager;
