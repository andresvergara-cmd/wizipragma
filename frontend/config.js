// CENTLI Frontend Configuration
// Hackathon Demo Configuration

const CONFIG = {
  // WebSocket API Gateway (Unit 2)
  WS_URL: 'wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod',
  
  // S3 Configuration
  S3_BUCKET: 'centli-frontend-bucket',
  S3_REGION: 'us-east-1',
  
  // Timeouts and Limits
  API_TIMEOUT: 30000, // 30 seconds
  WS_RECONNECT_MAX_ATTEMPTS: 5,
  WS_RECONNECT_DELAYS: [1000, 2000, 4000, 8000, 16000], // Exponential backoff
  
  // Image Upload
  MAX_IMAGE_SIZE: 5 * 1024 * 1024, // 5MB
  IMAGE_COMPRESSION_QUALITY: 0.8,
  IMAGE_MAX_WIDTH: 1920,
  IMAGE_MAX_HEIGHT: 1080,
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/png'],
  
  // Voice Recording
  MAX_RECORDING_DURATION: 30000, // 30 seconds
  AUDIO_FORMAT: 'audio/webm',
  
  // Chat
  MAX_MESSAGE_HISTORY: 50,
  
  // UI
  TOAST_DURATION: 5000, // 5 seconds
  TYPING_INDICATOR_TIMEOUT: 30000 // 30 seconds
};

// Make config globally available
window.CONFIG = CONFIG;
