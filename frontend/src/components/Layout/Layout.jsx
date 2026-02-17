import { Link, useLocation } from 'react-router-dom'
import { useChat } from '../../context/ChatContext'
import CinteotlLogo from '../Logo/CinteotlLogo'
import ChatWidget from '../Chat/ChatWidget'
import './Layout.css'
import '../Logo/CinteotlLogo.css'

const Layout = ({ children }) => {
  const location = useLocation()
  const { isChatOpen, isConnected, toggleChat, closeChat } = useChat()

  const isActivePath = (path) => {
    return location.pathname === path
  }

  return (
    <div className="layout">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <Link to="/" className="logo">
            <CinteotlLogo size={40} className="cinteotl-logo" />
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

      {/* Chat FAB */}
      <button 
        className={`chat-fab ${isChatOpen ? 'open' : ''}`}
        onClick={toggleChat}
        title="Chat con CENTLI"
      >
        {isChatOpen ? '✕' : '💬'}
      </button>

      {/* Chat Widget */}
      <ChatWidget isOpen={isChatOpen} onClose={closeChat} />
    </div>
  )
}

export default Layout
