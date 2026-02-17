// Main Application
// Orchestrates all managers and handles app lifecycle

class App {
  constructor() {
    this.appState = new AppState();
    this.wsManager = null;
    this.voiceManager = null;
    this.chatManager = null;
    this.imageManager = null;
    this.transactionManager = null;
    this.productCatalogManager = null;
    this.toastContainer = null;
  }

  // Initialize application
  init() {
    Logger.log('App', 'Initializing CENTLI application');
    
    // Create toast container
    this.createToastContainer();
    
    // Setup toast event listener
    window.addEventListener('show-toast', (e) => {
      this.showToast(e.detail.message, e.detail.type);
    });
    
    // Check if user is already logged in
    const userId = localStorage.getItem('user_id');
    const sessionId = localStorage.getItem('session_id');
    
    if (userId && sessionId) {
      this.login(userId, sessionId);
    } else {
      this.showLoginScreen();
    }
    
    Logger.log('App', 'Application initialized');
  }

  // Show login screen
  showLoginScreen() {
    document.getElementById('login-screen').style.display = 'flex';
    document.getElementById('app-container').style.display = 'none';
    
    document.getElementById('login-button').addEventListener('click', () => {
      const userId = document.getElementById('user-id-input').value.trim();
      if (userId) {
        const sessionId = 'session_' + Date.now();
        this.login(userId, sessionId);
      } else {
        this.showToast('Por favor ingresa tu ID de usuario', 'warning');
      }
    });
  }

  // Login user
  login(userId, sessionId) {
    // Generate mock token
    const token = btoa(JSON.stringify({ user_id: userId, timestamp: Date.now() }));
    
    // Save to localStorage
    localStorage.setItem('user_id', userId);
    localStorage.setItem('session_id', sessionId);
    
    // Update state
    this.appState.setNestedState('user.id', userId);
    this.appState.setNestedState('user.sessionId', sessionId);
    this.appState.setNestedState('user.token', token);
    this.appState.setState({ currentView: 'chat' });
    
    // Hide login, show app
    document.getElementById('login-screen').style.display = 'none';
    document.getElementById('app-container').style.display = 'flex';
    
    // Initialize managers
    this.initializeManagers();
    
    // Connect WebSocket
    this.wsManager.connect();
    
    Logger.log('App', 'User logged in', userId);
    this.showToast(`Bienvenido, ${userId}!`, 'success');
  }

  // Initialize all managers
  initializeManagers() {
    this.wsManager = new WebSocketManager(this.appState);
    this.voiceManager = new VoiceManager(this.appState);
    this.chatManager = new ChatManager(this.appState);
    this.imageManager = new ImageManager(this.appState);
    this.transactionManager = new TransactionManager(this.appState);
    this.productCatalogManager = new ProductCatalogManager(this.appState);
    
    // Make managers globally available
    window.wsManager = this.wsManager;
    window.voiceManager = this.voiceManager;
    window.chatManager = this.chatManager;
    window.imageManager = this.imageManager;
    window.transactionManager = this.transactionManager;
    window.productCatalogManager = this.productCatalogManager;
    
    // Initialize managers
    this.chatManager.init();
    this.imageManager.init();
    this.transactionManager.init();
    this.productCatalogManager.init();
    
    // Setup voice button
    const voiceButton = document.getElementById('voice-button');
    if (this.appState.getState().voiceAvailable) {
      voiceButton.addEventListener('mousedown', () => this.voiceManager.startRecording());
      voiceButton.addEventListener('mouseup', () => this.voiceManager.stopRecording());
      voiceButton.addEventListener('touchstart', (e) => {
        e.preventDefault();
        this.voiceManager.startRecording();
      });
      voiceButton.addEventListener('touchend', (e) => {
        e.preventDefault();
        this.voiceManager.stopRecording();
      });
    } else {
      voiceButton.disabled = true;
      voiceButton.title = 'Voice no disponible en este navegador';
    }
    
    // Setup logout button
    document.getElementById('logout-button').addEventListener('click', () => this.logout());
    
    // Setup connection status display
    this.appState.subscribe((state) => {
      this.updateConnectionStatus(state.connectionStatus);
    });
  }

  // Update connection status display
  updateConnectionStatus(status) {
    const statusEl = document.getElementById('connection-status');
    const statusMap = {
      'disconnected': { text: 'Desconectado', class: 'text-danger' },
      'connecting': { text: 'Conectando...', class: 'text-warning' },
      'connected': { text: 'Conectado', class: 'text-success' },
      'error': { text: 'Error', class: 'text-danger' }
    };
    
    const statusInfo = statusMap[status] || statusMap['disconnected'];
    statusEl.textContent = statusInfo.text;
    statusEl.className = statusInfo.class;
  }

  // Logout
  logout() {
    // Disconnect WebSocket
    if (this.wsManager) {
      this.wsManager.disconnect();
    }
    
    // Clear localStorage
    localStorage.removeItem('user_id');
    localStorage.removeItem('session_id');
    
    // Reset state
    this.appState.reset();
    
    // Show login screen
    this.showLoginScreen();
    
    Logger.log('App', 'User logged out');
    this.showToast('Sesión cerrada', 'info');
  }

  // Create toast container
  createToastContainer() {
    this.toastContainer = document.createElement('div');
    this.toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
    this.toastContainer.style.zIndex = '9999';
    document.body.appendChild(this.toastContainer);
  }

  // Show toast notification
  showToast(message, type = 'info') {
    const toastId = 'toast-' + Date.now();
    const bgClass = {
      'success': 'bg-success',
      'error': 'bg-danger',
      'warning': 'bg-warning',
      'info': 'bg-info'
    }[type] || 'bg-info';
    
    const toastHTML = `
      <div id="${toastId}" class="toast ${bgClass} text-white" role="alert">
        <div class="toast-body">
          ${message}
        </div>
      </div>
    `;
    
    this.toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastEl = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastEl, { delay: CONFIG.TOAST_DURATION });
    toast.show();
    
    // Remove after hiding
    toastEl.addEventListener('hidden.bs.toast', () => {
      toastEl.remove();
    });
  }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new App();
  window.app.init();
});
