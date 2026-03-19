import { useState, useRef, useEffect } from 'react'
import { useChat } from '../../context/ChatContext'
import ComfiAvatar from '../Logo/ComfiAvatar'
import { FAQQuickActions } from '../FAQ'
import { quickFAQs } from '../../data/faqData'
import MarkdownMessage from './MarkdownMessage'
import './ChatWidget.css'
import '../Logo/ComfiAvatar.css'

// Follow-up suggestions based on last bot response keywords
const getSuggestions = (botMessage) => {
  if (!botMessage) return []
  const text = botMessage.toLowerCase()
  
  if (text.includes('afilia') || text.includes('empleador') || text.includes('parafiscal')) {
    return ['¿Cuál es la tarifa de afiliación?', '¿Qué beneficios tengo como afiliado?', '¿Quiénes pueden ser mis beneficiarios?']
  }
  if (text.includes('tarifa') || text.includes('4%') || text.includes('aporte')) {
    return ['¿Cómo me afilio a Comfama?', '¿Qué beneficios tengo como afiliado?']
  }
  if (text.includes('crédito') || text.includes('financier') || text.includes('préstamo')) {
    return ['¿Cuáles son los requisitos para un crédito?', '¿Qué es la cuota monetaria?']
  }
  if (text.includes('subsidio') && text.includes('desempleo')) {
    return ['¿Cuáles son los requisitos para el subsidio al desempleo?', '¿Qué documentos necesito?']
  }
  if (text.includes('subsidio') || text.includes('vivienda')) {
    return ['¿Cómo me postulo al subsidio de vivienda?', '¿Qué es el subsidio familiar?']
  }
  if (text.includes('curso') || text.includes('educa') || text.includes('formación')) {
    return ['¿Los cursos tienen costo?', '¿Qué programas educativos ofrece Comfama?']
  }
  if (text.includes('certificado') || text.includes('carné')) {
    return ['¿Cómo obtengo mi certificado de afiliación?', '¿Cómo obtengo mi carné?']
  }
  if (text.includes('teléfono') || text.includes('contacto') || text.includes('atención')) {
    return ['¿Cuáles son los horarios de atención?', '¿Cómo presento una PQR?']
  }
  // Default suggestions
  return ['¿Cómo me afilio a Comfama?', '¿Qué servicios financieros ofrece?', '¿Cuáles son los canales de atención?']
}

const formatTimestamp = (ts) => {
  if (!ts) return ''
  const d = new Date(ts)
  return d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
}

const ChatWidget = ({ isOpen, onClose }) => {
  const { 
    messages, isTyping, inputValue, isConnected, isStreaming,
    currentStreamMessage, voiceEnabled,
    setInputValue, setVoiceEnabled, sendTextMessage, sendVoiceMessage
  } = useChat()

  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [selectedImage, setSelectedImage] = useState(null)
  const [showFAQQuickActions, setShowFAQQuickActions] = useState(true)
  const [isProcessing, setIsProcessing] = useState(false)
  const [copiedId, setCopiedId] = useState(null)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const recordingIntervalRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => { scrollToBottom() }, [messages, currentStreamMessage, isStreaming])

  // Auto-focus input when chat opens
  useEffect(() => {
    if (isOpen) setTimeout(() => inputRef.current?.focus(), 300)
  }, [isOpen])

  useEffect(() => {
    const lastMessage = messages[messages.length - 1]
    if (lastMessage?.type === 'user' && !isStreaming) setIsProcessing(true)
    if (isStreaming || lastMessage?.type === 'bot') setIsProcessing(false)
  }, [messages, isStreaming])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }

  const handleSendMessage = (e) => {
    e?.preventDefault()
    if (inputValue.trim() || selectedImage) {
      sendTextMessage(inputValue)
      setInputValue('')
      setSelectedImage(null)
      setShowFAQQuickActions(false)
      setIsProcessing(true)
    }
  }

  const handleSuggestionClick = (question) => {
    sendTextMessage(question)
    setIsProcessing(true)
  }

  const handleQuickFAQClick = (faqId) => {
    if (faqId === 'help') {
      sendTextMessage('¿Cómo puedo usar Comfi?')
    } else {
      // Send the shortQuestion text directly
      const faq = quickFAQs.find(f => f.id === faqId)
      if (faq) sendTextMessage(faq.shortQuestion)
    }
    setIsProcessing(true)
  }

  const handleCopy = async (content, msgId) => {
    try {
      await navigator.clipboard.writeText(content)
      setCopiedId(msgId)
      setTimeout(() => setCopiedId(null), 2000)
    } catch { /* clipboard not available */ }
  }

  const handleShowFAQs = () => {
    setShowFAQQuickActions(true)
    // Scroll to show FAQs would need welcome section, so just send a help message
    sendTextMessage('¿Cuáles son las preguntas frecuentes?')
    setIsProcessing(true)
  }

  const MAX_RECORDING_SECONDS = 15 // API Gateway WebSocket limit ~128KB
  const audioContextRef = useRef(null)
  const audioStreamRef = useRef(null)
  const mediaRecorderRef = useRef(null)

  // Auto-stop recording at max duration
  useEffect(() => {
    if (isRecording && recordingTime >= MAX_RECORDING_SECONDS) {
      stopRecordingAndSend()
    }
  }, [isRecording, recordingTime])

  const stopRecordingAndSend = () => {
    setIsRecording(false)
    clearInterval(recordingIntervalRef.current)

    // Stop MediaRecorder — onstop handler will process and send
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
    }
  }

  const handleVoiceRecord = async () => {
    const isSecureContext = window.isSecureContext || window.location.protocol === 'https:' || window.location.hostname === 'localhost'
    if (!isSecureContext) {
      alert('🎤 La grabación de voz requiere HTTPS.\nPor ahora, usa el chat de texto.')
      return
    }
    if (!isRecording) {
      try {
        if (!navigator.mediaDevices?.getUserMedia) {
          alert('Tu navegador no soporta grabación de audio.')
          return
        }
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true
          }
        })
        audioStreamRef.current = stream

        // Strategy: Use AudioContext to route audio through a destination node,
        // then use MediaRecorder on that destination. This ensures we always
        // get audio data (AudioContext capture is 100% reliable) while still
        // getting Opus compression (small file size for WebSocket).
        const audioContext = new (window.AudioContext || window.webkitAudioContext)()
        audioContextRef.current = audioContext
        const source = audioContext.createMediaStreamSource(stream)
        const destination = audioContext.createMediaStreamDestination()
        source.connect(destination)

        const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
          ? 'audio/webm;codecs=opus'
          : 'audio/webm'

        const mediaRecorder = new MediaRecorder(destination.stream, {
          mimeType,
          audioBitsPerSecond: 32000 // Low bitrate to keep file small
        })
        mediaRecorderRef.current = mediaRecorder
        const audioChunks = []

        mediaRecorder.ondataavailable = (event) => {
          console.log('🎤 ondataavailable:', event.data.size, 'bytes')
          if (event.data.size > 0) audioChunks.push(event.data)
        }

        mediaRecorder.onstop = () => {
          console.log('🎤 MediaRecorder stopped, chunks:', audioChunks.length, 'sizes:', audioChunks.map(c => c.size))
          const audioBlob = new Blob(audioChunks, { type: mimeType })
          console.log('🎤 Final blob:', audioBlob.size, 'bytes')

          // Cleanup
          if (audioStreamRef.current) {
            audioStreamRef.current.getTracks().forEach(t => t.stop())
            audioStreamRef.current = null
          }
          if (audioContextRef.current) {
            audioContextRef.current.close().catch(() => {})
            audioContextRef.current = null
          }

          if (audioBlob.size < 500) {
            console.error('❌ Audio blob too small:', audioBlob.size, 'bytes')
            alert('La grabación fue muy corta o no se capturó audio. Intenta de nuevo.')
            return
          }
          if (audioBlob.size > 90000) {
            console.warn('⚠️ Audio large:', audioBlob.size, 'bytes. May exceed WebSocket limit.')
          }
          sendVoiceMessage(audioBlob)
        }

        // Use timeslice of 500ms to ensure data is captured incrementally.
        // With AudioContext destination, the WebM headers are handled properly.
        mediaRecorder.start(500)
        console.log('🎤 Recording started (AudioContext → MediaRecorder, rate:', audioContext.sampleRate, 'Hz, mime:', mimeType, ')')

        setIsRecording(true)
        setRecordingTime(0)
        recordingIntervalRef.current = setInterval(() => setRecordingTime(prev => prev + 1), 1000)
      } catch (error) {
        let msg = 'No se pudo acceder al micrófono.'
        if (error.name === 'NotAllowedError') msg = '🎤 Permiso denegado. Permite el acceso al micrófono.'
        else if (error.name === 'NotFoundError') msg = '🎤 No se encontró micrófono.'
        alert(msg)
      }
    } else {
      stopRecordingAndSend()
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  // Get last bot message for suggestions
  const lastBotMessage = [...messages].reverse().find(m => m.type === 'bot')
  const showSuggestions = lastBotMessage && !isStreaming && !isProcessing && messages[messages.length - 1]?.type === 'bot'
  const suggestions = showSuggestions ? getSuggestions(lastBotMessage.content) : []

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
              aria-label={voiceEnabled ? 'Desactivar respuestas de voz' : 'Activar respuestas de voz'}
            >
              {voiceEnabled ? '🔊' : '🔇'}
            </button>
            <button className="close-button" onClick={onClose}>✕</button>
          </div>
        </div>

        {/* Messages */}
        <div className="chat-widget-body">
          {messages.length === 0 ? (
            <div className="welcome-section">
              <div className="welcome-logo">
                <ComfiAvatar size={50} className="comfi-avatar comfi-wave" animated={true} />
              </div>
              <h2>¡Hola! Soy Comfi</h2>
              <p>Tu asistente de Comfama. ¿En qué puedo ayudarte hoy?</p>
              {showFAQQuickActions && (
                <FAQQuickActions quickFAQs={quickFAQs} onQuickFAQClick={handleQuickFAQClick} />
              )}
            </div>
          ) : (
            <>
              {messages.map((msg) => (
                <div key={msg.id} className={`message ${msg.type}`}>
                  {msg.type === 'bot' && (
                    <div className="message-avatar">
                      <ComfiAvatar size={28} className="comfi-avatar" />
                    </div>
                  )}
                  
                  <div className="message-content-wrapper">
                    <div className={`message-bubble ${msg.isError ? 'error' : ''}`}>
                      {msg.type === 'bot' && !msg.isError ? (
                        <MarkdownMessage content={msg.content} />
                      ) : (
                        msg.content
                      )}
                    </div>
                    
                    {/* Timestamp + Copy button for bot messages */}
                    <div className={`message-meta ${msg.type}`}>
                      <span className="message-time">{formatTimestamp(msg.timestamp)}</span>
                      {msg.type === 'bot' && !msg.isError && (
                        <button 
                          className={`copy-btn ${copiedId === msg.id ? 'copied' : ''}`}
                          onClick={() => handleCopy(msg.content, msg.id)}
                          title="Copiar respuesta"
                        >
                          {copiedId === msg.id ? '✓' : '📋'}
                        </button>
                      )}
                    </div>
                  </div>
                  
                  {msg.type === 'user' && (
                    <div className="message-avatar user-avatar"></div>
                  )}
                </div>
              ))}
              
              {/* Streaming message */}
              {isStreaming && currentStreamMessage && (
                <div className="message bot">
                  <div className="message-avatar">
                    <ComfiAvatar size={28} className="comfi-avatar comfi-speaking" animated={true} />
                  </div>
                  <div className="message-content-wrapper">
                    <div className="message-bubble streaming">
                      <MarkdownMessage content={currentStreamMessage} />
                      <span className="cursor-blink">|</span>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Processing indicator */}
              {isProcessing && !isStreaming && (
                <div className="message bot processing-message">
                  <div className="message-avatar">
                    <ComfiAvatar size={28} className="comfi-avatar comfi-thinking" animated={true} />
                  </div>
                  <div className="message-bubble processing">
                    <div className="typing-indicator">
                      <span></span><span></span><span></span>
                    </div>
                    <span className="typing-text">
                      {messages[messages.length - 1]?.content?.includes('🎤') 
                        ? 'Procesando audio...' 
                        : 'Comfi está escribiendo...'}
                    </span>
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
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                </div>
              )}

              {/* Follow-up suggestions */}
              {suggestions.length > 0 && (
                <div className="suggestions-container">
                  <span className="suggestions-label">Preguntas relacionadas:</span>
                  <div className="suggestions-chips">
                    {suggestions.map((s, i) => (
                      <button key={i} className="suggestion-chip" onClick={() => handleSuggestionClick(s)}>
                        {s}
                      </button>
                    ))}
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
              <button className="remove-image" onClick={() => setSelectedImage(null)}>✕</button>
            </div>
          )}

          {isRecording && (
            <div className="recording-indicator">
              <div className="recording-animation">
                <div className="wave"></div><div className="wave"></div><div className="wave"></div>
              </div>
              <span className="recording-time">{formatTime(recordingTime)}</span>
              <span className="recording-text">
                {recordingTime >= MAX_RECORDING_SECONDS - 3 
                  ? `Deteniendo en ${MAX_RECORDING_SECONDS - recordingTime}s...` 
                  : `Grabando... (máx ${MAX_RECORDING_SECONDS}s)`}
              </span>
            </div>
          )}

          <form className="chat-input-form" onSubmit={handleSendMessage}>
            <div className="input-actions">
              <button type="button" className="action-btn" onClick={() => fileInputRef.current?.click()} title="Adjuntar imagen" aria-label="Adjuntar imagen">
                📷
              </button>
              <input ref={fileInputRef} type="file" accept="image/*" onChange={(e) => {
                const file = e.target.files[0]
                if (file) {
                  const reader = new FileReader()
                  reader.onloadend = () => setSelectedImage(reader.result)
                  reader.readAsDataURL(file)
                }
              }} style={{ display: 'none' }} />
              <button type="button" className={`action-btn voice-btn ${isRecording ? 'recording' : ''}`} onClick={handleVoiceRecord} title={isRecording ? 'Detener' : 'Grabar voz'} aria-label={isRecording ? 'Detener grabación' : 'Grabar mensaje de voz'}>
                {isRecording ? '⏹️' : '🎤'}
              </button>
            </div>

            <input
              ref={inputRef}
              type="text"
              className="chat-input"
              placeholder="Escribe tu mensaje..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={!isConnected || isRecording}
              aria-label="Escribe tu mensaje"
            />

            <button type="submit" className="send-btn" disabled={!isConnected || (!inputValue.trim() && !selectedImage) || isRecording}>
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
