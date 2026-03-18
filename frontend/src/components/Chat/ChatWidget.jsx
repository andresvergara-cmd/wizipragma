import { useState, useRef, useEffect } from 'react'
import { useChat } from '../../context/ChatContext'
import ComfiAvatar from '../Logo/ComfiAvatar'
import { FAQCard, FAQQuickActions } from '../FAQ'
import { getFAQById, quickFAQs } from '../../data/faqData'
import './ChatWidget.css'
import '../Logo/ComfiAvatar.css'

const ChatWidget = ({ isOpen, onClose }) => {
  const { 
    messages, 
    isTyping, 
    inputValue, 
    isConnected,
    isStreaming,
    currentStreamMessage,
    isPlayingAudio,
    voiceEnabled,
    setInputValue, 
    setVoiceEnabled,
    sendTextMessage,
    sendVoiceMessage,
    playAudio,
    stopAudio
  } = useChat()

  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [selectedImage, setSelectedImage] = useState(null)
  const [showQuickActions, setShowQuickActions] = useState(true)
  const [showFAQQuickActions, setShowFAQQuickActions] = useState(true)
  const [isProcessing, setIsProcessing] = useState(false) // Nuevo estado para indicador de procesamiento
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const recordingIntervalRef = useRef(null)

  const quickActions = []

  useEffect(() => {
    scrollToBottom()
  }, [messages, currentStreamMessage, isStreaming])

  useEffect(() => {
    if (messages.length > 0) {
      setShowQuickActions(false)
    }
  }, [messages])

  // Control del indicador de procesamiento
  useEffect(() => {
    // Activar cuando se envía un mensaje del usuario y no hay streaming ni respuesta del bot
    const lastMessage = messages[messages.length - 1]
    const hasUserMessage = lastMessage && lastMessage.type === 'user'
    const waitingForResponse = hasUserMessage && !isStreaming
    
    if (waitingForResponse) {
      setIsProcessing(true)
    }
    
    // Desactivar cuando comienza el streaming o llega respuesta del bot
    if (isStreaming || (lastMessage && lastMessage.type === 'bot')) {
      setIsProcessing(false)
    }
  }, [messages, isStreaming])

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ 
        behavior: 'smooth',
        block: 'end',
        inline: 'nearest'
      })
    }
  }

  const handleSendMessage = (e) => {
    e?.preventDefault()
    if (inputValue.trim() || selectedImage) {
      sendTextMessage(inputValue)
      setInputValue('')
      setSelectedImage(null)
      setShowFAQQuickActions(false) // Hide FAQ actions after first message
      setIsProcessing(true) // Activar indicador de procesamiento
    }
  }

  const handleQuickAction = (action) => {
    setInputValue(action)
    setTimeout(() => {
      sendTextMessage(action)
      setInputValue('')
      setIsProcessing(true) // Activar indicador de procesamiento
    }, 100)
  }

  const handleQuickFAQClick = (faqId) => {
    if (faqId === 'help') {
      // Si es el botón de ayuda, enviar mensaje de ayuda
      sendTextMessage('¿Cómo puedo usar Comfi?')
      setIsProcessing(true)
    } else {
      // Si es una FAQ normal, buscar y enviar la pregunta
      const faq = getFAQById(faqId)
      if (faq) {
        sendTextMessage(faq.question)
        setIsProcessing(true)
      }
    }
  }

  const handleFAQAction = (action) => {
    console.log('FAQ Action:', action)
    // Handle FAQ actions (activate_account, check_affiliation, etc.)
  }

  const handleFAQRelatedClick = (faqId) => {
    const faq = getFAQById(faqId)
    if (faq) {
      sendTextMessage(faq.question)
    }
  }

  const handleFAQFeedback = (faqId, isHelpful, comment) => {
    console.log('FAQ Feedback:', { faqId, isHelpful, comment })
    // Send feedback to backend
  }

  // Check if message is an FAQ response
  const isFAQResponse = (message) => {
    return message.content && typeof message.content === 'string' && 
           message.content.includes('✅ Encontré información sobre:')
  }

  // Parse FAQ from message
  const parseFAQFromMessage = (message) => {
    // Try to extract FAQ ID from message
    const content = message.content.toLowerCase()
    
    // Check if it's an FAQ response by looking for FAQ patterns
    // IMPORTANT: Check more specific patterns first to avoid false matches
    
    // Tarifa (check first because it's more specific than afiliación)
    if ((content.includes('tarifa') || content.includes('aporte') || 
         content.includes('4%')) && !content.includes('tipos de crédito')) {
      return getFAQById('faq-afiliacion-002')
    }
    // Afiliación (only if no tarifa keywords)
    else if ((content.includes('afilia') || content.includes('empleador') || 
              content.includes('registro') || content.includes('parafiscal')) &&
             !content.includes('tarifa') && !content.includes('aporte')) {
      return getFAQById('faq-afiliacion-001')
    } 
    // Requisitos crédito (check before tipos de crédito)
    else if ((content.includes('requisitos') || content.includes('requisito')) && 
             content.includes('crédito')) {
      return getFAQById('faq-creditos-002')
    }
    // Tipos de crédito
    else if (content.includes('tipos de crédito') || content.includes('líneas de crédito') ||
             content.includes('crédito de vivienda') || content.includes('crédito de educación') ||
             content.includes('libre inversión')) {
      return getFAQById('faq-creditos-001')
    } 
    // Subsidios
    else if (content.includes('subsidios') || content.includes('subsidio')) {
      return getFAQById('faq-subsidios-001')
    }
    
    return null
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
            <ComfiAvatar 
              size={32} 
              className={`comfi-avatar ${isStreaming ? 'comfi-speaking' : isTyping ? 'comfi-thinking' : ''}`}
              animated={isConnected}
            />
            <div className="chat-header-info">
              <h3>Comfi</h3>
              <span className={`status-indicator ${isConnected ? 'online' : 'offline'}`}>
                {isConnected ? 'En línea' : 'Desconectado'}
              </span>
            </div>
          </div>
          <div className="chat-header-right">
            <button 
              className={`voice-toggle-btn ${voiceEnabled ? 'active' : ''}`}
              onClick={() => setVoiceEnabled(!voiceEnabled)}
              title={voiceEnabled ? 'Desactivar respuestas de voz' : 'Activar respuestas de voz'}
            >
              {voiceEnabled ? '🔊' : '🔇'}
            </button>
            <button className="close-button" onClick={onClose}>✕</button>
          </div>
        </div>

        {/* Messages */}
        <div className="chat-widget-body">
          {console.log('🎨 RENDER: messages.length =', messages.length, 'messages =', messages)}
          {messages.length === 0 ? (
            <div className="welcome-section">
              {console.log('🎨 RENDER: Showing welcome section')}
              <div className="welcome-logo">
                <ComfiAvatar size={50} className="comfi-avatar comfi-wave" animated={true} />
              </div>
              <h2>¡Hola! Soy Comfi</h2>
              <p>Tu asistente de Comfama. ¿En qué puedo ayudarte hoy?</p>
              
              {showFAQQuickActions && (
                <FAQQuickActions
                  quickFAQs={quickFAQs}
                  onQuickFAQClick={handleQuickFAQClick}
                />
              )}
            </div>
          ) : (
            <>
              {console.log('🎨 RENDER: Showing messages, count =', messages.length)}
              {messages.map((msg) => {
                console.log('🎨 RENDER: Rendering message', msg.id, msg.type, msg.content.substring(0, 50))
                const faq = msg.type === 'bot' ? parseFAQFromMessage(msg) : null
                
                // Si es una FAQ, solo mostrar la tarjeta, NO el texto plano
                if (faq) {
                  return (
                    <div key={msg.id} className={`message ${msg.type}`}>
                      <div className="message-avatar">
                        <ComfiAvatar size={28} className="comfi-avatar" />
                      </div>
                      <div className="message-faq-container">
                        <FAQCard
                          faq={faq}
                          onActionClick={handleFAQAction}
                          onRelatedClick={handleFAQRelatedClick}
                          onFeedback={handleFAQFeedback}
                        />
                      </div>
                    </div>
                  )
                }
                
                // Si no es FAQ, mostrar mensaje normal
                return (
                  <div key={msg.id} className={`message ${msg.type}`}>
                    {msg.type === 'bot' && (
                      <div className="message-avatar">
                        <ComfiAvatar size={28} className="comfi-avatar" />
                      </div>
                    )}
                    
                    <div className={`message-bubble ${msg.isError ? 'error' : ''}`}>
                      {msg.content}
                    </div>
                    
                    {msg.type === 'user' && (
                      <div className="message-avatar user-avatar"></div>
                    )}
                  </div>
                )
              })}
              
              {/* Streaming message */}
              {isStreaming && currentStreamMessage && (
                (() => {
                  // Check if streaming message is a FAQ
                  const tempMsg = { content: currentStreamMessage.toLowerCase() }
                  const isFAQ = tempMsg.content.includes('afilia') || 
                                tempMsg.content.includes('empleador') ||
                                tempMsg.content.includes('tarifa') || 
                                tempMsg.content.includes('aporte') ||
                                tempMsg.content.includes('crédito') ||
                                tempMsg.content.includes('subsidio')
                  
                  // If it's a FAQ, show "Procesando..." instead of streaming text
                  if (isFAQ) {
                    return (
                      <div className="message bot processing-message">
                        <div className="message-avatar">
                          <ComfiAvatar size={28} className="comfi-avatar comfi-thinking" animated={true} />
                        </div>
                        <div className="message-bubble processing">
                          <div className="processing-indicator">
                            <div className="processing-spinner"></div>
                            <span className="processing-text">Procesando...</span>
                          </div>
                        </div>
                      </div>
                    )
                  }
                  
                  // Otherwise show streaming text normally
                  return (
                    <div className="message bot">
                      <div className="message-avatar">
                        <ComfiAvatar size={28} className="comfi-avatar comfi-speaking" animated={true} />
                      </div>
                      <div className="message-bubble streaming">
                        {currentStreamMessage}
                        <span className="cursor-blink">|</span>
                      </div>
                    </div>
                  )
                })()
              )}
              
              {/* Indicador de procesamiento - Comfi está escribiendo */}
              {isProcessing && !isStreaming && (
                <div className="message bot processing-message">
                  <div className="message-avatar">
                    <ComfiAvatar size={28} className="comfi-avatar comfi-thinking" animated={true} />
                  </div>
                  <div className="message-bubble processing">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span className="typing-text">Comfi está escribiendo...</span>
                  </div>
                </div>
              )}
              
              {isTyping && !isStreaming && !isProcessing && (
                <div className="message bot">
                  <div className="message-avatar">
                    <ComfiAvatar size={28} className="comfi-avatar comfi-thinking" />
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
