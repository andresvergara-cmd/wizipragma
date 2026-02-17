// Image Manager - Handles image upload with compression
class ImageManager {
  constructor(appState) {
    this.appState = appState;
    this.fileInput = null;
    this.previewContainer = null;
    this.pendingUpload = null;
  }

  init() {
    this.fileInput = document.getElementById('image-input');
    this.previewContainer = document.getElementById('image-preview');
    
    this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    window.addEventListener('presigned-url', (e) => this.handlePresignedUrl(e));
    
    Logger.log('Image', 'Image manager initialized');
  }

  async handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate file
    if (!CONFIG.ALLOWED_IMAGE_TYPES.includes(file.type)) {
      this.showToast('Formato no soportado. Usa JPEG o PNG', 'error');
      return;
    }
    
    if (file.size > CONFIG.MAX_IMAGE_SIZE) {
      this.showToast('Imagen muy grande. Máximo 5MB', 'error');
      return;
    }
    
    // Show preview
    this.showPreview(file);
    
    // Compress image
    const compressedBlob = await this.compressImage(file);
    this.pendingUpload = compressedBlob;
    
    // Request presigned URL
    this.requestPresignedUrl(file.name);
  }

  showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      this.previewContainer.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 200px;">`;
    };
    reader.readAsDataURL(file);
  }

  async compressImage(file) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          let { width, height } = img;
          
          if (width > CONFIG.IMAGE_MAX_WIDTH) {
            height *= CONFIG.IMAGE_MAX_WIDTH / width;
            width = CONFIG.IMAGE_MAX_WIDTH;
          }
          if (height > CONFIG.IMAGE_MAX_HEIGHT) {
            width *= CONFIG.IMAGE_MAX_HEIGHT / height;
            height = CONFIG.IMAGE_MAX_HEIGHT;
          }
          
          canvas.width = width;
          canvas.height = height;
          canvas.getContext('2d').drawImage(img, 0, 0, width, height);
          canvas.toBlob((blob) => resolve(blob), 'image/jpeg', CONFIG.IMAGE_COMPRESSION_QUALITY);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  requestPresignedUrl(filename) {
    const state = this.appState.getState();
    window.wsManager.send({
      action: 'request_presigned_url',
      filename: filename,
      content_type: 'image/jpeg',
      session_id: state.user.sessionId
    });
    this.appState.setState({ isUploading: true, uploadProgress: 0 });
  }

  async handlePresignedUrl(event) {
    const { upload_url, image_url } = event.detail;
    
    try {
      // Upload to S3
      const response = await fetch(upload_url, {
        method: 'PUT',
        body: this.pendingUpload,
        headers: { 'Content-Type': 'image/jpeg' }
      });
      
      if (response.ok) {
        this.showToast('Imagen subida correctamente', 'success');
        this.sendImageMessage(image_url);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      Logger.error('Image', 'Upload failed', error);
      this.showToast('Error al subir imagen', 'error');
    } finally {
      this.appState.setState({ isUploading: false });
      this.previewContainer.innerHTML = '';
      this.fileInput.value = '';
    }
  }

  sendImageMessage(imageUrl) {
    const state = this.appState.getState();
    this.appState.addMessage({
      id: Date.now(),
      sender: 'user',
      type: 'image',
      content: '📷 Imagen enviada',
      timestamp: new Date()
    });
    
    window.wsManager.send({
      action: 'image_message',
      image_url: imageUrl,
      user_id: state.user.id,
      session_id: state.user.sessionId
    });
    
    this.appState.setState({ isTyping: true });
  }

  showToast(message, type) {
    window.dispatchEvent(new CustomEvent('show-toast', { detail: { message, type } }));
  }
}

window.ImageManager = ImageManager;
