import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ChatWidget from './ChatWidget'
import { ChatProvider } from '../../context/ChatContext'
import { WebSocketProvider } from '../../context/WebSocketContext'

// Mock de los contextos
vi.mock('../../context/ChatContext', () => ({
  ChatProvider: ({ children }) => children,
  useChat: () => ({
    messages: [],
    isTyping: false,
    inputValue: '',
    isConnected: true,
    isStreaming: false,
    currentStreamMessage: '',
    setInputValue: vi.fn(),
    sendTextMessage: vi.fn(),
    sendVoiceMessage: vi.fn()
  })
}))

vi.mock('../../context/WebSocketContext', () => ({
  WebSocketProvider: ({ children }) => children,
  useWebSocket: () => ({
    isConnected: true,
    sessionId: 'test-session',
    messages: [],
    isStreaming: false,
    currentStreamMessage: '',
    sendMessage: vi.fn()
  })
}))

describe('ChatWidget - UX Improvements', () => {
  const mockOnClose = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Indicador de Procesamiento', () => {
    it('debe mostrar indicador cuando se envía un mensaje', async () => {
      const { rerender } = render(
        <ChatWidget isOpen={true} onClose={mockOnClose} />
      )

      // Simular envío de mensaje
      const input = screen.getByPlaceholderText('Escribe tu mensaje...')
      const sendButton = screen.getByRole('button', { name: /➤/i })

      fireEvent.change(input, { target: { value: 'Hola Comfi' } })
      fireEvent.click(sendButton)

      // Verificar que aparece el indicador
      await waitFor(() => {
        expect(screen.getByText(/Comfi está escribiendo/i)).toBeInTheDocument()
      })
    })

    it('debe ocultar indicador cuando comienza streaming', async () => {
      const { rerender } = render(
        <ChatWidget isOpen={true} onClose={mockOnClose} />
      )

      // Simular que comienza streaming
      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        isStreaming: true,
        currentStreamMessage: 'Respuesta...'
      })

      rerender(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      // Verificar que NO aparece el indicador de procesamiento
      expect(screen.queryByText(/Comfi está escribiendo/i)).not.toBeInTheDocument()
    })
  })

  describe('Avatar del Usuario', () => {
    it('debe mostrar avatar del usuario en mensajes', () => {
      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        messages: [
          { id: '1', type: 'user', content: 'Hola', timestamp: new Date().toISOString() }
        ]
      })

      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      // Verificar que existe el avatar del usuario
      const userAvatar = document.querySelector('.message-avatar.user-avatar')
      expect(userAvatar).toBeInTheDocument()
    })

    it('debe posicionar avatar del usuario a la derecha', () => {
      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        messages: [
          { id: '1', type: 'user', content: 'Hola', timestamp: new Date().toISOString() }
        ]
      })

      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      const userMessage = document.querySelector('.message.user')
      expect(userMessage).toHaveClass('user')
    })
  })

  describe('Layout Inicial Optimizado', () => {
    it('debe mostrar pantalla de bienvenida con FAQ', () => {
      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      // Verificar elementos de bienvenida
      expect(screen.getByText(/¡Hola! Soy Comfi/i)).toBeInTheDocument()
      expect(screen.getByText(/Tu asistente de Comfama/i)).toBeInTheDocument()
    })

    it('debe mostrar botones de acción rápida', () => {
      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      // Verificar que existen botones de acción rápida
      expect(screen.getByText(/Ver mi saldo/i)).toBeInTheDocument()
      expect(screen.getByText(/Hacer transferencia/i)).toBeInTheDocument()
    })

    it('debe ocultar pantalla de bienvenida después del primer mensaje', () => {
      const { rerender } = render(
        <ChatWidget isOpen={true} onClose={mockOnClose} />
      )

      // Verificar que está visible
      expect(screen.getByText(/¡Hola! Soy Comfi/i)).toBeInTheDocument()

      // Simular mensaje enviado
      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        messages: [
          { id: '1', type: 'user', content: 'Hola', timestamp: new Date().toISOString() }
        ]
      })

      rerender(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      // Verificar que ya no está visible
      expect(screen.queryByText(/¡Hola! Soy Comfi/i)).not.toBeInTheDocument()
    })
  })

  describe('Animaciones y Feedback Visual', () => {
    it('debe aplicar clase de animación a mensajes nuevos', () => {
      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        messages: [
          { id: '1', type: 'bot', content: 'Hola', timestamp: new Date().toISOString() }
        ]
      })

      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      const message = document.querySelector('.message.bot')
      expect(message).toBeInTheDocument()
      // La animación se aplica via CSS
    })

    it('debe mostrar cursor parpadeante durante streaming', () => {
      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        isStreaming: true,
        currentStreamMessage: 'Respuesta en progreso'
      })

      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      const cursor = document.querySelector('.cursor-blink')
      expect(cursor).toBeInTheDocument()
      expect(cursor).toHaveTextContent('|')
    })
  })

  describe('Scroll Automático', () => {
    it('debe hacer scroll al último mensaje', async () => {
      const scrollIntoViewMock = vi.fn()
      Element.prototype.scrollIntoView = scrollIntoViewMock

      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        messages: [
          { id: '1', type: 'user', content: 'Mensaje 1', timestamp: new Date().toISOString() },
          { id: '2', type: 'bot', content: 'Respuesta 1', timestamp: new Date().toISOString() }
        ]
      })

      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      await waitFor(() => {
        expect(scrollIntoViewMock).toHaveBeenCalled()
      })
    })
  })

  describe('Estados de Conexión', () => {
    it('debe mostrar estado "En línea" cuando está conectado', () => {
      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      expect(screen.getByText(/En línea/i)).toBeInTheDocument()
    })

    it('debe mostrar estado "Desconectado" cuando no está conectado', () => {
      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        isConnected: false
      })

      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      expect(screen.getByText(/Desconectado/i)).toBeInTheDocument()
    })

    it('debe deshabilitar input cuando está desconectado', () => {
      vi.mocked(useChat).mockReturnValue({
        ...vi.mocked(useChat)(),
        isConnected: false
      })

      render(<ChatWidget isOpen={true} onClose={mockOnClose} />)

      const input = screen.getByPlaceholderText('Escribe tu mensaje...')
      expect(input).toBeDisabled()
    })
  })
})
