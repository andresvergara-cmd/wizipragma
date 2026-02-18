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
  const wsRef = useRef(null)
  const reconnectTimeoutRef = useRef(null)
  const reconnectAttemptsRef = useRef(0)
  const streamMessageIdRef = useRef(null)
  const streamTimeoutRef = useRef(null)
  const isStreamingRef = useRef(false)
  const accumulatedMessageRef = useRef('')

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
            console.log('🏁 Stream ended')
            
            // Add final message using the accumulated stream message
            setCurrentStreamMessage(prevStream => {
              const finalMessage = data.message || prevStream
              if (finalMessage) {
                setMessages(prev => [...prev, {
                  id: streamMessageIdRef.current || `msg-${Date.now()}`,
                  type: 'bot',
                  content: finalMessage,
                  timestamp: new Date().toISOString(),
                  data: data.data
                }])
              }
              return '' // Clear stream message
            })
            
            setIsStreaming(false)
            streamMessageIdRef.current = null
          }
          else if (data.msg_type === 'agent_response') {
            console.log('🤖 Agent response:', data.message)
            setMessages(prev => [...prev, {
              id: `msg-${Date.now()}`,
              type: 'bot',
              content: data.message || data.data?.content || 'Respuesta recibida',
              timestamp: new Date().toISOString(),
              data: data.data
            }])
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
              setMessages(prev => [...prev, {
                id: `msg-${Date.now()}`,
                type: 'bot',
                content: data.message,
                timestamp: new Date().toISOString(),
                data: data.data
              }])
            }
          }
        } catch (error) {
          // Handle plain text streaming chunks
          const chunk = event.data
          console.log('📦 Streaming chunk received:', chunk.substring(0, 50))
          
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
            console.log('🌊 Starting stream (plain text mode)')
            isStreamingRef.current = true
            accumulatedMessageRef.current = chunk
            setIsStreaming(true)
            setCurrentStreamMessage(chunk)
            streamMessageIdRef.current = `msg-${Date.now()}`
          } else {
            // Accumulate chunks
            accumulatedMessageRef.current += chunk
            setCurrentStreamMessage(accumulatedMessageRef.current)
          }
          
          // Clear existing timeout
          if (streamTimeoutRef.current) {
            clearTimeout(streamTimeoutRef.current)
          }
          
          // Set timeout to finalize stream after 500ms of no new chunks
          streamTimeoutRef.current = setTimeout(() => {
            console.log('🏁 Stream ended (timeout)')
            const finalMessage = accumulatedMessageRef.current
            
            if (finalMessage) {
              setMessages(prev => [...prev, {
                id: streamMessageIdRef.current || `msg-${Date.now()}`,
                type: 'bot',
                content: finalMessage,
                timestamp: new Date().toISOString()
              }])
            }
            
            // Reset state
            isStreamingRef.current = false
            accumulatedMessageRef.current = ''
            setIsStreaming(false)
            setCurrentStreamMessage('')
            streamMessageIdRef.current = null
          }, 500)
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

  const sendMessage = (message, type = 'TEXT', audioData = null) => {
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
          type: type
        }
      }

      // Add message or audio data based on type
      if (type === 'AUDIO' && audioData) {
        payload.data.audio = audioData
        console.log('📤 Sending AUDIO message (base64 length:', audioData.length, ')')
      } else {
        payload.data.message = message
        console.log('📤 Sending TEXT message:', message)
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
    sendMessage,
    connect,
    disconnect
  }

  return (
    <WebSocketContext.Provider value={value}>
      {children}
    </WebSocketContext.Provider>
  )
}
