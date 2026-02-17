// Voice Manager
// Handles voice input (recording) and output (playback)

class VoiceManager {
  constructor(appState) {
    this.appState = appState;
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.stream = null;
    this.recordingStartTime = null;
    this.recordingTimer = null;
    
    // Check if voice is available
    this.checkVoiceAvailability();
  }

  // Check if MediaRecorder API is available
  checkVoiceAvailability() {
    const available = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);
    this.appState.setState({ voiceAvailable: available });
    
    if (!available) {
      Logger.warn('Voice', 'MediaRecorder API not available');
    }
    
    return available;
  }

  // Start recording
  async startRecording() {
    if (!this.appState.getState().voiceAvailable) {
      this.showToast('Voice input no disponible en este navegador', 'error');
      return;
    }

    try {
      Logger.log('Voice', 'Requesting microphone permission');
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      this.mediaRecorder = new MediaRecorder(this.stream, {
        mimeType: 'audio/webm'
      });
      
      this.audioChunks = [];
      
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };
      
      this.mediaRecorder.onstop = () => {
        this.handleRecordingStop();
      };
      
      this.mediaRecorder.start();
      this.recordingStartTime = Date.now();
      this.appState.setState({ isRecording: true });
      Logger.log('Voice', 'Recording started');
      
      // Auto-stop after max duration
      this.recordingTimer = setTimeout(() => {
        if (this.appState.getState().isRecording) {
          this.stopRecording();
          this.showToast('Grabación detenida (máximo 30 segundos)', 'info');
        }
      }, CONFIG.MAX_RECORDING_DURATION);
      
    } catch (error) {
      Logger.error('Voice', 'Failed to start recording', error);
      this.showToast('No se pudo acceder al micrófono', 'error');
      this.appState.setState({ isRecording: false });
    }
  }

  // Stop recording
  stopRecording() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
      
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
      }
      
      if (this.recordingTimer) {
        clearTimeout(this.recordingTimer);
        this.recordingTimer = null;
      }
      
      this.appState.setState({ isRecording: false });
      Logger.log('Voice', 'Recording stopped');
    }
  }

  // Handle recording stop
  async handleRecordingStop() {
    const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
    const duration = Date.now() - this.recordingStartTime;
    
    Logger.log('Voice', `Recording complete: ${duration}ms, ${audioBlob.size} bytes`);
    
    // Convert to base64 for sending via WebSocket
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64Audio = reader.result.split(',')[1];
      this.sendVoiceMessage(base64Audio, duration);
    };
    reader.readAsDataURL(audioBlob);
  }

  // Send voice message via WebSocket
  sendVoiceMessage(base64Audio, duration) {
    const state = this.appState.getState();
    
    // Add user message to chat
    this.appState.addMessage({
      id: Date.now(),
      sender: 'user',
      type: 'voice',
      content: '🎤 Mensaje de voz',
      timestamp: new Date()
    });
    
    // Send to backend
    window.wsManager.send({
      action: 'voice_message',
      audio: base64Audio,
      format: 'webm',
      duration: duration,
      user_id: state.user.id,
      session_id: state.user.sessionId
    });
    
    // Show typing indicator
    this.appState.setState({ isTyping: true });
    Logger.log('Voice', 'Voice message sent');
  }

  // Play audio response
  playAudio(audioData) {
    try {
      this.appState.setState({ isPlaying: true });
      
      // audioData can be base64 or URL
      let audioSrc;
      if (audioData.startsWith('http')) {
        audioSrc = audioData;
      } else {
        audioSrc = `data:audio/webm;base64,${audioData}`;
      }
      
      const audio = new Audio(audioSrc);
      
      audio.onended = () => {
        this.appState.setState({ isPlaying: false });
        Logger.log('Voice', 'Audio playback ended');
      };
      
      audio.onerror = (error) => {
        Logger.error('Voice', 'Audio playback error', error);
        this.appState.setState({ isPlaying: false });
        this.showToast('Error al reproducir audio', 'error');
      };
      
      audio.play();
      Logger.log('Voice', 'Playing audio response');
      
    } catch (error) {
      Logger.error('Voice', 'Failed to play audio', error);
      this.appState.setState({ isPlaying: false });
      this.showToast('Error al reproducir audio', 'error');
    }
  }

  // Show toast notification
  showToast(message, type = 'info') {
    window.dispatchEvent(new CustomEvent('show-toast', { 
      detail: { message, type }
    }));
  }
}

// Listen for voice response events
window.addEventListener('voice-response', (event) => {
  if (window.voiceManager && event.detail.audio) {
    window.voiceManager.playAudio(event.detail.audio);
  }
});

// Make VoiceManager globally available
window.VoiceManager = VoiceManager;
