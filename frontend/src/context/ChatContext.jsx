import { createContext, useContext, useState } from 'react'
import { useWebSocket } from './WebSocketContext'

const ChatContext = createContext(null)

export const useChat = () => {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error('useChat must be used within ChatProvider')
  }
  return context
}

export const ChatProvider = ({ children }) => {
  const { messages: wsMessages, sendMessage: wsSendMessage, isConnected, isStreaming, currentStreamMessage } = useWebSocket()
  const [isChatOpen, setIsChatOpen] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const [inputValue, setInputValue] = useState('')

  const sendTextMessage = (text) => {
    if (!text.trim()) return false

    const success = wsSendMessage(text, 'TEXT')
    
    if (success) {
      setInputValue('')
      setIsTyping(true)
      
      // Simulate typing indicator
      setTimeout(() => {
        setIsTyping(false)
      }, 2000)
    }
    
    return success
  }

  const sendVoiceMessage = (audioBlob) => {
    console.log('🎤 Processing voice message, size:', audioBlob.size, 'bytes')
    
    // Convert audio blob to base64
    const reader = new FileReader()
    reader.onloadend = () => {
      const base64Audio = reader.result.split(',')[1]
      console.log('🎤 Audio converted to base64, length:', base64Audio.length)
      
      // Send with AUDIO type and audio data
      wsSendMessage('', 'AUDIO', base64Audio)
      
      setIsTyping(true)
      setTimeout(() => {
        setIsTyping(false)
      }, 2000)
    }
    reader.onerror = (error) => {
      console.error('❌ Error reading audio blob:', error)
    }
    reader.readAsDataURL(audioBlob)
  }

  const sendImageMessage = (imageBlob) => {
    // Convert image blob to base64
    const reader = new FileReader()
    reader.onloadend = () => {
      const base64Image = reader.result.split(',')[1]
      wsSendMessage(base64Image, 'IMAGE')
    }
    reader.readAsDataURL(imageBlob)
  }

  const openChat = () => setIsChatOpen(true)
  const closeChat = () => setIsChatOpen(false)
  const toggleChat = () => setIsChatOpen(prev => !prev)

  const clearMessages = () => {
    // This would need to be implemented in WebSocketContext
    console.log('Clear messages not yet implemented')
  }

  const value = {
    messages: wsMessages,
    isChatOpen,
    isTyping,
    inputValue,
    isConnected,
    isStreaming,
    currentStreamMessage,
    setInputValue,
    sendTextMessage,
    sendVoiceMessage,
    sendImageMessage,
    openChat,
    closeChat,
    toggleChat,
    clearMessages
  }

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  )
}
