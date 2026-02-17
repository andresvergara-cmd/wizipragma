import { Link, useLocation } from 'react-router-dom'
import { useChat } from '../../context/ChatContext'
import './Layout.css'

const Layout = ({ children }) => {
  const location = useLocation()
  const { 
    messages, 
    isChatOpen, 
    isTyping, 
    inputValue, 
    isConnected,
    setInputValue, 
    sendTextMessage, 
    toggleChat,
    closeChat 
  } = useChat()

  const handleSendMessage = (e) => {
    e.preventDefault()
    if (inputValue.trim()) {
      sendTextMessage(inputValue)
    }
  }

  const isActivePath = (path) => {
    return location.pathname === path
  }

  return (
    <div className="layout">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <Link to="/" className="logo">
            <span className="logo-icon">🦉</span>
            <span className="logo-text">CENTLI</span>
          </Link>
          
          <nav className="nav">
            <Link to="/" className={`nav-link ${isActivePath('/') ? 'active' : ''}`}>
              Inicio
            </Link>
            <Link to="/marketplace" className={`nav-link ${isActivePath('/marketplace') ? 'active' : ''}`}>
              Marketplace
            </Link>
            <Link to="/transactions" className={`nav-link ${isActivePath('/transactions') ? 'active' : ''}`}>
              Transacciones
            </Link>
          </nav>

          <div className="header-actions">
            <div className="connection-status">
              <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}></span>
              <span className="status-text">{isConnected ? 'Conectado' : 'Desconectado'}</span>
            </div>
            <button className="user-button">
              <span>👤</span>
              <span>@carlos.rodriguez</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {children}
      </main>

      {/* Chat Button */}
      <button 
        className={`chat-fab ${isChatOpen ? 'open' : ''}`}
        onClick={toggleChat}
        title="Chat con CENTLI"
      >
        {isChatOpen ? '✕' : '💬'}
      </button>

      {/* Chat Widget */}
      {isChatOpen && (
        <div className="chat-widget">
          <div className="chat-header">
            <div className="chat-title">
              <span>🦉</span>
              <span>Chat con CENTLI</span>
            </div>
            <button onClick={closeChat} className="close-button">✕</button>
          </div>
          
          <div className="chat-body">
            {messages.length === 0 ? (
              <div className="chat-message bot">
                <div className="message-avatar">🦉</div>
                <div className="message-content">
                  ¡Hola! Soy CENTLI, tu coach financiero. ¿En qué puedo ayudarte hoy?
                </div>
              </div>
            ) : (
              messages.map((msg) => (
                <div key={msg.id} className={`chat-message ${msg.type}`}>
                  {msg.type === 'bot' && <div className="message-avatar">🦉</div>}
                  <div className="message-content">
                    {msg.content}
                  </div>
                  {msg.type === 'user' && <div className="message-avatar">👤</div>}
                </div>
              ))
            )}
            
            {isTyping && (
              <div className="chat-message bot">
                <div className="message-avatar">🦉</div>
                <div className="message-content typing">
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                </div>
              </div>
            )}
          </div>
          
          <form className="chat-input" onSubmit={handleSendMessage}>
            <input 
              type="text" 
              placeholder="Escribe tu mensaje..." 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={!isConnected}
            />
            <button type="submit" disabled={!isConnected || !inputValue.trim()}>
              ➤
            </button>
          </form>
        </div>
      )}
    </div>
  )
}

export default Layout
