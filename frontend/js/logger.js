// Logger Utility
// Provides structured console logging for debugging

class Logger {
  static log(category, message, data = null) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${category}]`, message, data || '');
  }

  static error(category, message, error = null) {
    const timestamp = new Date().toISOString();
    console.error(`[${timestamp}] [${category}]`, message, error || '');
    
    // Log stack trace if available
    if (error && error.stack) {
      console.error('Stack trace:', error.stack);
    }
  }

  static warn(category, message, data = null) {
    const timestamp = new Date().toISOString();
    console.warn(`[${timestamp}] [${category}]`, message, data || '');
  }

  static debug(category, message, data = null) {
    const timestamp = new Date().toISOString();
    console.debug(`[${timestamp}] [${category}]`, message, data || '');
  }
}

// Make Logger globally available
window.Logger = Logger;
