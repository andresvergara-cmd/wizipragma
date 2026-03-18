import { createContext, useContext, useEffect, useState, useRef } from 'react'

const WebSocketContext = createContext(null)

export const useWebSocket = () => {
  const context = useContext(WebSocketContext)
  if (!context) {
    throw new Error('useWebSocket must be used within WebSocketProvider')
  }
  return context
}

export const WebSocketProvider = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [isStreaming, setIsStreaming] = useState(false)
  const [currentStreamMessage, setCurrentStreamMessage] = useState('')
  const [isPlayingAudio, setIsPlayingAudio] = useState(false)
  const wsRef = useRef(null)
  const reconnectTimeoutRef = useRef(null)
  const reconnectAttemptsRef = useRef(0)
  const streamMessageIdRef = useRef(null)
  const streamTimeoutRef = useRef(null)
  const isStreamingRef = useRef(false)
  const accumulatedMessageRef = useRef('')
  const audioRef = useRef(null)
  const audioChunksRef = useRef([])  // For assembling audio chunks

  // Debug: Log messages changes
  useEffect(() => {
    console.log('📋 Messages array updated, count:', messages.length)
    if (messages.length > 0) {
      console.log('📋 Last message:', messages[messages.length - 1])
      console.log('📋 All message IDs:', messages.map(m => m.id))
    }
  }, [messages])
  
  // Debug: Log streaming state changes
  useEffect(() => {
    console.log('🌊 isStreaming changed:', isStreaming)
  }, [isStreaming])
  
  // Debug: Log currentStreamMessage changes
  useEffect(() => {
    console.log('💬 currentStreamMessage changed (length):', currentStreamMessage.length)
  }, [currentStreamMessage])

  const WEBSOCKET_URL = import.meta.env.VITE_WEBSOCKET_URL || 'wss://vvg621xawg.execute-api.us-east-1.amazonaws.com/prod'
  const MAX_RECONNECT_ATTEMPTS = 5
  const RECONNECT_DELAY = 3000

  const connect = () => {
    try {
      console.log('🔌 Connecting to WebSocket:', WEBSOCKET_URL)
      
      wsRef.current = new WebSocket(WEBSOCKET_URL)

      wsRef.current.onopen = () => {
        console.log('✅ WebSocket connected')
        setIsConnected(true)
        reconnectAttemptsRef.current = 0
        
        // Generate session ID
        const newSessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
        setSessionId(newSessionId)
        console.log('🆔 Session ID:', newSessionId)
      }

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          console.log('📨 WebSocket message received:', data)
          
          // Handle transcription from STT
          if (data.msg_type === 'transcription') {
            console.log('🎤 Transcription received:', data.text)
            setMessages(prev => [...prev, {
              id: `msg-${Date.now()}`,
              type: 'user',
              content: `🎤 ${data.text}`,
              timestamp: new Date().toISOString(),
              isTranscription: true
            }])
            return
          }
          
          // Handle audio chunks from TTS
          if (data.msg_type === 'audio_chunk') {
            console.log(`🔊 Audio chunk ${data.chunk_index + 1}/${data.total_chunks} received`)
            
            // Store chunk
            if (!audioChunksRef.current[data.chunk_index]) {
              audioChunksRef.current[data.chunk_index] = data.audio_chunk
            }
            
            // If this is the last chunk, assemble and play
            if (data.chunk_index === data.total_chunks - 1) {
              console.log('🔊 All audio chunks received, assembling...')
              assembleAndPlayAudio(audioChunksRef.current, data.audio_format, data.sample_rate)
              audioChunksRef.current = []  // Reset for next audio
            }
            return
          }
          
          // Handle audio response
          if (data.msg_type === 'audio_response') {
            console.log('🔊 Audio response received')
            if (data.audio) {
              playAudio(data.audio)
            }
            return
          }
          
          // Handle different message types from backend
          if (data.msg_type === 'stream_start') {
            console.log('🌊 Stream started')
            setIsStreaming(true)
            setCurrentStreamMessage('')
            streamMessageIdRef.current = `msg-${Date.now()}`
          } 
          else if (data.msg_type === 'stream_chunk') {
            console.log('📦 Stream chunk:', data.message)
            setCurrentStreamMessage(prev => prev + data.message)
          }
          else if (data.msg_type === 'stream_end') {
            console.log('🏁 Stream ended (JSON mode)')
            
            // Get final message
            const finalMessage = data.message || currentStreamMessage
            const messageId = streamMessageIdRef.current || `msg-${Date.now()}`
            
            console.log('💾 Final message from stream_end:', finalMessage.substring(0, 200))
            
            if (finalMessage && finalMessage.length > 0) {
              // Create message object
              const newMessage = {
                id: messageId,
                type: 'bot',
                content: finalMessage,
                timestamp: new Date().toISOString(),
                data: data.data
              }
              
              console.log('➕ Adding message to array (JSON mode):', newMessage)
              
              // Add to messages array
              setMessages(prevMessages => {
                const updatedMessages = [...prevMessages, newMessage]
                console.log('✅ Messages array now has', updatedMessages.length, 'messages')
                return updatedMessages
              })
              
              // Play audio if included
              if (data.audio) {
                console.log('🔊 Playing audio from stream_end')
                playAudio(data.audio)
              }
              
              // Reset state
              console.log('🧹 Resetting streaming state (JSON mode)')
              setIsStreaming(false)
              setCurrentStreamMessage('')
              streamMessageIdRef.current = null
            } else {
              console.warn('⚠️ No message in stream_end')
              setIsStreaming(false)
              setCurrentStreamMessage('')
              streamMessageIdRef.current = null
            }
          }
          else if (data.msg_type === 'agent_response') {
            console.log('🤖 Agent response:', data.message)
            const newMessage = {
              id: `msg-${Date.now()}`,
              type: 'bot',
              content: data.message || data.data?.content || 'Respuesta recibida',
              timestamp: new Date().toISOString(),
              data: data.data
            }
            setMessages(prev => [...prev, newMessage])
            
            // Play audio if included
            if (data.audio) {
              console.log('🔊 Playing audio from agent_response')
              playAudio(data.audio)
            }
          }
          else if (data.msg_type === 'error') {
            console.error('❌ Error from backend:', data.message)
            setMessages(prev => [...prev, {
              id: `msg-${Date.now()}`,
              type: 'bot',
              content: `Error: ${data.message || 'Ocurrió un error'}`,
              timestamp: new Date().toISOString(),
              isError: true
            }])
          }
          else {
            // Generic message handling
            console.log('📬 Generic message:', data)
            if (data.message) {
              const newMessage = {
                id: `msg-${Date.now()}`,
                type: 'bot',
                content: data.message,
                timestamp: new Date().toISOString(),
                data: data.data
              }
              setMessages(prev => [...prev, newMessage])
              
              // Play audio if included
              if (data.audio) {
                console.log('🔊 Playing audio from generic message')
                playAudio(data.audio)
              }
            }
          }
        } catch (error) {
          // Handle plain text streaming chunks
          const chunk = event.data
          console.log('📦 Plain text chunk received (length:', chunk.length, '):', chunk.substring(0, 100))
          
          // Check for error messages
          if (chunk.includes('Internal server error')) {
            console.error('❌ Internal server error')
            isStreamingRef.current = false
            accumulatedMessageRef.current = ''
            setIsStreaming(false)
            setCurrentStreamMessage('')
            setMessages(prev => [...prev, {
              id: `msg-${Date.now()}`,
              type: 'bot',
              content: 'Lo siento, hubo un error procesando tu mensaje. Por favor intenta de nuevo.',
              timestamp: new Date().toISOString(),
              isError: true
            }])
            return
          }
          
          // Start streaming if not already started
          if (!isStreamingRef.current) {
            console.log('🌊 Starting plain text stream')
            isStreamingRef.current = true
            accumulatedMessageRef.current = chunk
            setIsStreaming(true)
            setCurrentStreamMessage(chunk)
            streamMessageIdRef.current = `msg-${Date.now()}`
            console.log('🆔 Stream message ID:', streamMessageIdRef.current)
          } else {
            // Accumulate chunks
            accumulatedMessageRef.current += chunk
            setCurrentStreamMessage(accumulatedMessageRef.current)
            console.log('📊 Total accumulated length:', accumulatedMessageRef.current.length)
          }
          
          // Clear existing timeout
          if (streamTimeoutRef.current) {
            clearTimeout(streamTimeoutRef.current)
          }
          
          // Set timeout to finalize stream after 1000ms of no new chunks
          streamTimeoutRef.current = setTimeout(() => {
            console.log('🏁 Stream timeout - finalizing message')
            const finalMessage = accumulatedMessageRef.current
            const messageId = streamMessageIdRef.current || `msg-${Date.now()}`
            
            console.log('💾 Final message length:', finalMessage.length)
            console.log('💾 Final message preview:', finalMessage.substring(0, 200))
            
            if (finalMessage && finalMessage.length > 0) {
              // Create the message object
              const newMessage = {
                id: messageId,
                type: 'bot',
                content: finalMessage,
                timestamp: new Date().toISOString()
              }
              
              console.log('➕ Adding message to array:', newMessage)
              
              // Add to messages array - THIS IS THE CRITICAL PART
              setMessages(prevMessages => {
                const updatedMessages = [...prevMessages, newMessage]
                console.log('✅ Messages array now has', updatedMessages.length, 'messages')
                console.log('✅ Message IDs:', updatedMessages.map(m => `${m.type}:${m.id.substring(0, 10)}`))
                return updatedMessages
              })
              
              // Reset streaming state
              console.log('🧹 Resetting streaming state')
              isStreamingRef.current = false
              accumulatedMessageRef.current = ''
              streamMessageIdRef.current = null
              setIsStreaming(false)
              setCurrentStreamMessage('')
            } else {
              console.warn('⚠️ No message to save (empty or null)')
              // Just reset state
              isStreamingRef.current = false
              accumulatedMessageRef.current = ''
              streamMessageIdRef.current = null
              setIsStreaming(false)
              setCurrentStreamMessage('')
            }
          }, 1000)
        }
      }

      wsRef.current.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
      }

      wsRef.current.onclose = () => {
        console.log('🔌 WebSocket disconnected')
        setIsConnected(false)
        
        // Attempt to reconnect
        if (reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
          reconnectAttemptsRef.current += 1
          console.log(`🔄 Reconnecting... Attempt ${reconnectAttemptsRef.current}/${MAX_RECONNECT_ATTEMPTS}`)
          
          reconnectTimeoutRef.current = setTimeout(() => {
            connect()
          }, RECONNECT_DELAY)
        } else {
          console.error('❌ Max reconnection attempts reached')
          setMessages(prev => [...prev, {
            id: `msg-${Date.now()}`,
            type: 'bot',
            content: 'No se pudo conectar con el servidor. Por favor, recarga la página.',
            timestamp: new Date().toISOString(),
            isError: true
          }])
        }
      }
    } catch (error) {
      console.error('❌ Error creating WebSocket connection:', error)
    }
  }

  const disconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
    
    if (streamTimeoutRef.current) {
      clearTimeout(streamTimeoutRef.current)
    }
    
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    
    // Reset all refs
    isStreamingRef.current = false
    accumulatedMessageRef.current = ''
    streamMessageIdRef.current = null
    
    setIsConnected(false)
    setSessionId(null)
    setIsStreaming(false)
    setCurrentStreamMessage('')
  }

  const sendMessage = (message, type = 'TEXT', audioData = null, includeAudio = false) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      console.error('❌ WebSocket is not connected')
      setMessages(prev => [...prev, {
        id: `msg-${Date.now()}`,
        type: 'bot',
        content: 'No estás conectado. Intentando reconectar...',
        timestamp: new Date().toISOString(),
        isError: true
      }])
      return false
    }

    try {
      const payload = {
        action: 'sendMessage',
        data: {
          user_id: 'simple-user', // Using test user
          session_id: sessionId,
          type: type,
          includeAudio: includeAudio  // Request audio response
        }
      }

      // Add message or audio data based on type
      if (type === 'AUDIO' && audioData) {
        payload.data.audio = audioData
        console.log('📤 Sending AUDIO message (base64 length:', audioData.length, ')')
      } else {
        payload.data.message = message
        console.log('📤 Sending TEXT message:', message, 'includeAudio:', includeAudio)
      }

      wsRef.current.send(JSON.stringify(payload))
      
      // Add user message to local state
      setMessages(prev => [...prev, {
        id: `msg-${Date.now()}`,
        type: 'user',
        content: type === 'TEXT' ? message : type === 'AUDIO' ? '🎤 Mensaje de voz' : `[${type}]`,
        timestamp: new Date().toISOString()
      }])
      
      return true
    } catch (error) {
      console.error('❌ Error sending message:', error)
      return false
    }
  }

  const playAudio = (audioBase64) => {
    try {
      console.log('🔊 Playing audio response')
      setIsPlayingAudio(true)
      
      // Convert base64 to blob
      const audioData = atob(audioBase64)
      const arrayBuffer = new ArrayBuffer(audioData.length)
      const view = new Uint8Array(arrayBuffer)
      for (let i = 0; i < audioData.length; i++) {
        view[i] = audioData.charCodeAt(i)
      }
      const blob = new Blob([arrayBuffer], { type: 'audio/mpeg' })
      const audioUrl = URL.createObjectURL(blob)
      
      // Create and play audio
      const audio = new Audio(audioUrl)
      audioRef.current = audio
      
      audio.onended = () => {
        console.log('🔊 Audio playback finished')
        setIsPlayingAudio(false)
        URL.revokeObjectURL(audioUrl)
      }
      
      audio.onerror = (error) => {
        console.error('❌ Audio playback error:', error)
        setIsPlayingAudio(false)
        URL.revokeObjectURL(audioUrl)
      }
      
      audio.play()
    } catch (error) {
      console.error('❌ Error playing audio:', error)
      setIsPlayingAudio(false)
    }
  }

  const assembleAndPlayAudio = (chunks, format, sampleRate) => {
    try {
      console.log(`🔊 Assembling ${chunks.length} audio chunks (format: ${format}, rate: ${sampleRate})`)
      setIsPlayingAudio(true)
      
      // Combine all base64 chunks
      const combinedBase64 = chunks.join('')
      
      if (format === 'mp3') {
        // MP3 format - use Audio element (simpler)
        console.log('🔊 Playing MP3 audio')
        playAudio(combinedBase64)
      } else if (format === 'pcm') {
        // PCM format - use Web Audio API
        console.log('🔊 Playing PCM audio')
        
        // Decode base64 to binary
        const audioData = atob(combinedBase64)
        const arrayBuffer = new ArrayBuffer(audioData.length)
        const view = new Uint8Array(arrayBuffer)
        for (let i = 0; i < audioData.length; i++) {
          view[i] = audioData.charCodeAt(i)
        }
        
        // Create audio context for PCM playback
        const audioContext = new (window.AudioContext || window.webkitAudioContext)()
        
        // PCM is raw audio data: 16-bit, mono, at specified sample rate
        const numSamples = arrayBuffer.byteLength / 2  // 16-bit = 2 bytes per sample
        const audioBuffer = audioContext.createBuffer(1, numSamples, parseInt(sampleRate))
        const channelData = audioBuffer.getChannelData(0)
        
        // Convert 16-bit PCM to float32 (-1.0 to 1.0)
        const dataView = new DataView(arrayBuffer)
        for (let i = 0; i < numSamples; i++) {
          const sample = dataView.getInt16(i * 2, true)  // true = little-endian
          channelData[i] = sample / 32768.0  // Normalize to -1.0 to 1.0
        }
        
        // Create source and play
        const source = audioContext.createBufferSource()
        source.buffer = audioBuffer
        source.connect(audioContext.destination)
        
        source.onended = () => {
          console.log('🔊 PCM audio playback finished')
          setIsPlayingAudio(false)
          audioContext.close()
        }
        
        source.start(0)
        audioRef.current = { stop: () => source.stop() }
        
        console.log('🔊 PCM audio playback started')
      } else {
        console.error('❌ Unknown audio format:', format)
        setIsPlayingAudio(false)
      }
      
    } catch (error) {
      console.error('❌ Error assembling/playing audio:', error)
      setIsPlayingAudio(false)
    }
  }

  const stopAudio = () => {
    if (audioRef.current) {
      if (audioRef.current.pause) {
        audioRef.current.pause()
        audioRef.current.currentTime = 0
      } else if (audioRef.current.stop) {
        audioRef.current.stop()
      }
      setIsPlayingAudio(false)
    }
  }

  useEffect(() => {
    connect()

    return () => {
      disconnect()
    }
  }, [])

  const value = {
    isConnected,
    sessionId,
    messages,
    isStreaming,
    currentStreamMessage,
    isPlayingAudio,
    sendMessage,
    playAudio,
    stopAudio,
    connect,
    disconnect
  }

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  )
}
