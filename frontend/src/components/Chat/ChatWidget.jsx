import { useState, useRef, useEffect } from 'react'
import { useChat } from '../../context/ChatContext'
import CinteotlLogo from '../Logo/CinteotlLogo'
import './ChatWidget.css'

const ChatWidget = ({ isOpen, onClose }) => {
  const { 
    messages, 
    isTyping, 
    inputValue, 
    isConnected,
    isStreaming,
    currentStreamMessage,
    setInputValue, 
    sendTextMessage,
    sendVoiceMessage 
  } = useChat()

  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [selectedImage, setSelectedImage] = useState(null)
  const [showQuickActions, setShowQuickActions] = useState(true)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const recordingIntervalRef = useRef(null)

  const quickActions = [
    { icon: '💰', text: 'Ver mi saldo', action: '¿Cuál es mi saldo actual?' },
    { icon: '💸', text: 'Hacer transferencia', action: 'Quiero hacer una transferencia' },
    { icon: '🛒', text: 'Ver productos', action: 'Muéstrame productos disponibles' },
    { icon: '📊', text: 'Mis transacciones', action: 'Muéstrame mis últimas transacciones' },
    { icon: '🎁', text: 'Ofertas especiales', action: '¿Qué ofertas hay disponibles?' },
    { icon: '❓', text: 'Ayuda', action: '¿Cómo puedo usar CENTLI?' }
  ]

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (messages.length > 0) {
      setShowQuickActions(false)
    }
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = (e) => {
    e?.preventDefault()
    if (inputValue.trim() || selectedImage) {
      sendTextMessage(inputValue)
      setInputValue('')
      setSelectedImage(null)
    }
  }

  const handleQuickAction = (action) => {
    setInputValue(action)
    setTimeout(() => {
      sendTextMessage(action)
      setInputValue('')
    }, 100)
  }

  const handleVoiceRecord = async () => {
    // Check if we're on HTTPS or localhost
    const isSecureContext = window.isSecureContext || window.location.protocol === 'https:' || window.location.hostname === 'localhost'
    
    if (!isSecureContext) {
      alert('🎤 La grabación de voz requiere una conexión segura (HTTPS).\n\nPor ahora, puedes usar el chat de texto. Estamos trabajando en habilitar HTTPS para esta función.')
      return
    }
    
    if (!isRecording) {
      try {
        // Check if getUserMedia is available
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          alert('Tu navegador no soporta grabación de audio. Por favor, usa un navegador moderno como Chrome, Firefox o Safari.')
          return
        }
        
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        const mediaRecorder = new MediaRecorder(stream)
        mediaRecorderRef.current = mediaRecorder
        
        const audioChunks = []
        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data)
        }
        
        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
          console.log('🎤 Audio recorded:', audioBlob.size, 'bytes')
          
          // Send audio to backend via sendVoiceMessage
          sendVoiceMessage(audioBlob)
          
          // Stop all tracks
          stream.getTracks().forEach(track => track.stop())
        }
        
        mediaRecorder.start()
        setIsRecording(true)
        setRecordingTime(0)
        
        recordingIntervalRef.current = setInterval(() => {
          setRecordingTime(prev => prev + 1)
        }, 1000)
      } catch (error) {
        console.error('Error accessing microphone:', error)
        
        let errorMessage = 'No se pudo acceder al micrófono.'
        
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
          errorMessage = '🎤 Permiso denegado.\n\nPor favor, permite el acceso al micrófono en la configuración de tu navegador.'
        } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
          errorMessage = '🎤 No se encontró ningún micrófono.\n\nPor favor, conecta un micrófono y recarga la página.'
        } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
          errorMessage = '🎤 El micrófono está siendo usado por otra aplicación.\n\nPor favor, cierra otras aplicaciones que puedan estar usando el micrófono.'
        } else if (error.name === 'NotSupportedError') {
          errorMessage = '🎤 La grabación de voz requiere HTTPS.\n\nPor ahora, usa el chat de texto.'
        }
        
        alert(errorMessage)
      }
    } else {
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop()
        setIsRecording(false)
        clearInterval(recordingIntervalRef.current)
      }
    }
  }

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setSelectedImage(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (!isOpen) return null

  return (
    <div className="chat-widget-overlay">
      <div className="chat-widget-container">
        {/* Header */}
        <div className="chat-widget-header">
          <div className="chat-header-left">
            <CinteotlLogo size={32} className="cinteotl-logo pulse" />
            <div className="chat-header-info">
              <h3>CENTLI</h3>
              <span className={`status-indicator ${isConnected ? 'online' : 'offline'}`}>
                {isConnected ? 'En línea' : 'Desconectado'}
              </span>
            </div>
          </div>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        {/* Messages */}
        <div className="chat-widget-body">
          {messages.length === 0 && showQuickActions ? (
            <div className="welcome-section">
              <div className="welcome-logo">
                <CinteotlLogo size={80} className="cinteotl-logo" />
              </div>
              <h2>¡Hola! Soy CENTLI</h2>
              <p>Tu coach financiero inteligente. ¿En qué puedo ayudarte hoy?</p>
              
              <div className="quick-actions-grid">
                {quickActions.map((action, index) => (
                  <button
                    key={index}
                    className="quick-action-btn"
                    onClick={() => handleQuickAction(action.action)}
                  >
                    <span className="quick-action-icon">{action.icon}</span>
                    <span className="quick-action-text">{action.text}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg) => (
                <div key={msg.id} className={`message ${msg.type}`}>
                  {msg.type === 'bot' && (
                    <div className="message-avatar">
                      <CinteotlLogo size={28} className="cinteotl-logo" />
                    </div>
                  )}
                  <div className={`message-bubble ${msg.isError ? 'error' : ''}`}>
                    {msg.content}
                  </div>
                  {msg.type === 'user' && (
                    <div className="message-avatar user-avatar">👤</div>
                  )}
                </div>
              ))}
              
              {/* Streaming message */}
              {isStreaming && currentStreamMessage && (
                <div className="message bot">
                  <div className="message-avatar">
                    <CinteotlLogo size={28} className="cinteotl-logo pulse" />
                  </div>
                  <div className="message-bubble streaming">
                    {currentStreamMessage}
                    <span className="cursor-blink">|</span>
                  </div>
                </div>
              )}
              
              {isTyping && !isStreaming && (
                <div className="message bot">
                  <div className="message-avatar">
                    <CinteotlLogo size={28} className="cinteotl-logo" />
                  </div>
                  <div className="message-bubble typing">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <div className="chat-widget-footer">
          {selectedImage && (
            <div className="image-preview">
              <img src={selectedImage} alt="Preview" />
              <button 
                className="remove-image"
                onClick={() => setSelectedImage(null)}
              >
                ✕
              </button>
            </div>
          )}

          {isRecording && (
            <div className="recording-indicator">
              <div className="recording-animation">
                <div className="wave"></div>
                <div className="wave"></div>
                <div className="wave"></div>
              </div>
              <span className="recording-time">{formatTime(recordingTime)}</span>
              <span className="recording-text">Grabando...</span>
            </div>
          )}

          <form className="chat-input-form" onSubmit={handleSendMessage}>
            <div className="input-actions">
              <button
                type="button"
                className="action-btn"
                onClick={() => fileInputRef.current?.click()}
                title="Adjuntar imagen"
              >
                📷
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                style={{ display: 'none' }}
              />
              
              <button
                type="button"
                className={`action-btn voice-btn ${isRecording ? 'recording' : ''}`}
                onClick={handleVoiceRecord}
                title={isRecording ? 'Detener grabación' : 'Grabar voz'}
              >
                {isRecording ? '⏹️' : '🎤'}
              </button>
            </div>

            <input
              type="text"
              className="chat-input"
              placeholder="Escribe tu mensaje..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={!isConnected || isRecording}
            />

            <button
              type="submit"
              className="send-btn"
              disabled={!isConnected || (!inputValue.trim() && !selectedImage) || isRecording}
            >
              ➤
            </button>
          </form>

          <div className="input-hint">
            Puedes escribir, hablar o enviar imágenes
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatWidget
