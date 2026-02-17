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
          console.error('❌ Error parsing WebSocket message:', error)
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
    
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    
    setIsConnected(false)
    setSessionId(null)
  }

  const sendMessage = (message, type = 'TEXT') => {
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
          user_id: 'user-001', // TODO: Get from auth context
          session_id: sessionId,
          message: message,
          type: type
        }
      }

      console.log('📤 Sending message:', payload)
      wsRef.current.send(JSON.stringify(payload))
      
      // Add user message to local state
      setMessages(prev => [...prev, {
        id: `msg-${Date.now()}`,
        type: 'user',
        content: type === 'TEXT' ? message : `[${type}]`,
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
