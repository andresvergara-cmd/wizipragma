import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, act } from '@testing-library/react'
import { WebSocketProvider } from '../context/WebSocketContext'
import { ChatProvider } from '../context/ChatContext'
import ChatWidget from '../components/Chat/ChatWidget'

// Mock WebSocket
class MockWebSocket {
  constructor(url) {
    this.url = url
    this.readyState = WebSocket.CONNECTING
    this.onopen = null
    this.onmessage = null
    this.onerror = null
    this.onclose = null
    
    // Simulate connection after a short delay
    setTimeout(() => {
      this.readyState = WebSocket.OPEN
      if (this.onopen) this.onopen()
    }, 10)
  }
  
  send(data) {
    console.log('MockWebSocket send:', data)
  }
  
  close() {
    this.readyState = WebSocket.CLOSED
    if (this.onclose) this.onclose()
  }
  
  // Helper to simulate receiving messages
  simulateMessage(data) {
    if (this.onmessage) {
      this.onmessage({ data: JSON.stringify(data) })
    }
  }
  
  // Helper to simulate streaming chunks
  simulateStreamChunk(chunk) {
    if (this.onmessage) {
      this.onmessage({ data: chunk })
    }
  }
}

describe('Chat Experience Tests', () => {
  let mockWs
  
  beforeEach(() => {
    // Mock WebSocket globally
    global.WebSocket = vi.fn((url) => {
      mockWs = new MockWebSocket(url)
      return mockWs
    })
    global.WebSocket.CONNECTING = 0
    global.WebSocket.OPEN = 1
    global.WebSocket.CLOSING = 2
    global.WebSocket.CLOSED = 3
  })
  
  afterEach(() => {
    vi.clearAllMocks()
  })
  
  const renderChat = () => {
    return render(
      <WebSocketProvider>
        <ChatProvider>
          <ChatWidget isOpen={true} onClose={() => {}} />
        </ChatProvider>
      </WebSocketProvider>
    )
  }
  
  describe('Message Persistence', () => {
    it('should keep user message visible after sending', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Find input and send button
      const input = container.querySelector('.chat-input')
      const sendBtn = container.querySelector('.send-btn')
      
      // Send a message
      await act(async () => {
        input.value = 'Hola Comfi'
        input.dispatchEvent(new Event('input', { bubbles: true }))
        sendBtn.click()
      })
      
      // User message should be visible
      await waitFor(() => {
        const userMessages = container.querySelectorAll('.message.user')
        expect(userMessages.length).toBeGreaterThan(0)
      })
      
      // User message should stay visible
      await new Promise(resolve => setTimeout(resolve, 100))
      const userMessages = container.querySelectorAll('.message.user')
      expect(userMessages.length).toBeGreaterThan(0)
      expect(userMessages[0].textContent).toContain('Hola Comfi')
    })
    
    it('should keep bot response visible after streaming ends', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Simulate streaming response
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_start' })
      })
      
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_chunk', message: 'Hola, ' })
      })
      
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_chunk', message: 'soy Comfi' })
      })
      
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_end', message: 'Hola, soy Comfi' })
      })
      
      // Wait for message to be added
      await waitFor(() => {
        const botMessages = container.querySelectorAll('.message.bot')
        expect(botMessages.length).toBeGreaterThan(0)
      }, { timeout: 3000 })
      
      // Message should stay visible
      await new Promise(resolve => setTimeout(resolve, 200))
      const botMessages = container.querySelectorAll('.message.bot')
      expect(botMessages.length).toBeGreaterThan(0)
      expect(botMessages[0].textContent).toContain('Hola, soy Comfi')
    })
    
    it('should not remove messages when streaming indicator disappears', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Start streaming
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_start' })
      })
      
      // Add chunks
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_chunk', message: 'Respuesta completa' })
      })
      
      // End streaming
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_end', message: 'Respuesta completa' })
      })
      
      // Wait for message to be rendered
      await waitFor(() => {
        const botMessages = container.querySelectorAll('.message.bot .message-bubble:not(.streaming)')
        expect(botMessages.length).toBeGreaterThan(0)
      }, { timeout: 3000 })
      
      // Verify streaming indicator is gone but message remains
      await new Promise(resolve => setTimeout(resolve, 200))
      const streamingBubbles = container.querySelectorAll('.message-bubble.streaming')
      const regularBubbles = container.querySelectorAll('.message.bot .message-bubble:not(.streaming)')
      
      expect(streamingBubbles.length).toBe(0) // No streaming indicator
      expect(regularBubbles.length).toBeGreaterThan(0) // Message still there
      expect(regularBubbles[0].textContent).toContain('Respuesta completa')
    })
  })
  
  describe('Processing Indicator', () => {
    it('should show processing indicator after user sends message', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Send message
      const input = container.querySelector('.chat-input')
      const sendBtn = container.querySelector('.send-btn')
      
      await act(async () => {
        input.value = 'Test message'
        input.dispatchEvent(new Event('input', { bubbles: true }))
        sendBtn.click()
      })
      
      // Processing indicator should appear
      await waitFor(() => {
        const processingIndicator = container.querySelector('.message.processing-message')
        expect(processingIndicator).toBeTruthy()
      })
    })
    
    it('should hide processing indicator when streaming starts', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Send message
      const input = container.querySelector('.chat-input')
      const sendBtn = container.querySelector('.send-btn')
      
      await act(async () => {
        input.value = 'Test message'
        input.dispatchEvent(new Event('input', { bubbles: true }))
        sendBtn.click()
      })
      
      // Wait for processing indicator
      await waitFor(() => {
        const processingIndicator = container.querySelector('.message.processing-message')
        expect(processingIndicator).toBeTruthy()
      })
      
      // Start streaming
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_start' })
      })
      
      // Processing indicator should disappear
      await waitFor(() => {
        const processingIndicator = container.querySelector('.message.processing-message')
        expect(processingIndicator).toBeFalsy()
      })
    })
  })
  
  describe('Streaming Behavior', () => {
    it('should accumulate streaming chunks correctly', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Start streaming
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_start' })
      })
      
      // Add chunks
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_chunk', message: 'Parte 1 ' })
      })
      
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_chunk', message: 'Parte 2 ' })
      })
      
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_chunk', message: 'Parte 3' })
      })
      
      // Check streaming message contains all parts
      await waitFor(() => {
        const streamingBubble = container.querySelector('.message-bubble.streaming')
        expect(streamingBubble).toBeTruthy()
        expect(streamingBubble.textContent).toContain('Parte 1 Parte 2 Parte 3')
      })
    })
    
    it('should convert streaming message to permanent message on stream_end', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Complete streaming cycle
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_start' })
      })
      
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_chunk', message: 'Mensaje completo' })
      })
      
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'stream_end', message: 'Mensaje completo' })
      })
      
      // Wait for permanent message
      await waitFor(() => {
        const regularBubbles = container.querySelectorAll('.message.bot .message-bubble:not(.streaming)')
        expect(regularBubbles.length).toBeGreaterThan(0)
        expect(regularBubbles[0].textContent).toContain('Mensaje completo')
      }, { timeout: 3000 })
      
      // Streaming bubble should be gone
      const streamingBubbles = container.querySelectorAll('.message-bubble.streaming')
      expect(streamingBubbles.length).toBe(0)
    })
  })
  
  describe('Multiple Messages', () => {
    it('should handle multiple messages without losing any', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Send first message and get response
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'agent_response', message: 'Respuesta 1' })
      })
      
      await waitFor(() => {
        const botMessages = container.querySelectorAll('.message.bot')
        expect(botMessages.length).toBe(1)
      })
      
      // Send second message and get response
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'agent_response', message: 'Respuesta 2' })
      })
      
      await waitFor(() => {
        const botMessages = container.querySelectorAll('.message.bot')
        expect(botMessages.length).toBe(2)
      })
      
      // Both messages should be visible
      const botMessages = container.querySelectorAll('.message.bot')
      expect(botMessages[0].textContent).toContain('Respuesta 1')
      expect(botMessages[1].textContent).toContain('Respuesta 2')
    })
  })
  
  describe('Error Handling', () => {
    it('should display error messages without removing previous messages', async () => {
      const { container } = renderChat()
      
      // Wait for connection
      await waitFor(() => {
        expect(mockWs.readyState).toBe(WebSocket.OPEN)
      })
      
      // Add a normal message
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'agent_response', message: 'Mensaje normal' })
      })
      
      await waitFor(() => {
        const botMessages = container.querySelectorAll('.message.bot')
        expect(botMessages.length).toBe(1)
      })
      
      // Add an error message
      await act(async () => {
        mockWs.simulateMessage({ msg_type: 'error', message: 'Error de prueba' })
      })
      
      await waitFor(() => {
        const botMessages = container.querySelectorAll('.message.bot')
        expect(botMessages.length).toBe(2)
      })
      
      // Both messages should be visible
      const botMessages = container.querySelectorAll('.message.bot')
      expect(botMessages[0].textContent).toContain('Mensaje normal')
      expect(botMessages[1].textContent).toContain('Error de prueba')
    })
  })
})
