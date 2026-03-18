import { Link, useLocation } from 'react-router-dom'
import { useChat } from '../../context/ChatContext'
import ChatWidget from '../Chat/ChatWidget'
import ComfiAvatar from '../Logo/ComfiAvatar'
import comfamaLogo from '../../assets/comfama-logo.svg'
import './Layout.css'

const Layout = ({ children }) => {
  const location = useLocation()
  const { isChatOpen, isConnected, toggleChat, closeChat } = useChat()

  const isActivePath = (path) => {
    return location.pathname === path
  }

  return (
    <div className="layout">
      {/* Header Comfama Style */}
      <header className="header-comfama">
        <div className="header-container">
          <div className="header-top">
            <div className="header-left">
              <Link to="/" className="logo-comfama">
                <img 
                  src={comfamaLogo} 
                  alt="Comfama Logo" 
                  className="logo-img"
                />
              </Link>
              <nav className="nav-comfama">
                <Link to="/" className={`nav-link-comfama ${isActivePath('/') ? 'active' : ''}`}>
                  Afiliaciones
                </Link>
                <Link to="/marketplace" className={`nav-link-comfama ${isActivePath('/marketplace') ? 'active' : ''}`}>
                  Créditos
                </Link>
                <Link to="/transactions" className={`nav-link-comfama ${isActivePath('/transactions') ? 'active' : ''}`}>
                  Subsidios
                </Link>
                <a href="#" className="nav-link-comfama">Servicios de empleo</a>
                <a href="#" className="nav-link-comfama">Tienda Comfama</a>
              </nav>
            </div>
            
            <div className="header-right">
              <div className="zona-transaccional">
                Zona transaccional
                <svg className="dropdown-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M19 9l-7 7-7-7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                </svg>
              </div>
              
              <button className="header-btn-icon">
                Ayuda
                <svg className="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                </svg>
              </button>
              
              <button className="header-btn-icon">
                Buscador
                <svg className="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                </svg>
              </button>
              
              <button className="menu-btn-comfama">
                Menú
                <svg className="icon-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M4 6h16M4 12h16m-7 6h7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                </svg>
              </button>
            </div>
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
        title="Habla con Comfi"
      >
        {isChatOpen ? (
          <span className="chat-fab-close">✕</span>
        ) : (
          <div className="chat-fab-content">
            <ComfiAvatar size={48} animated={true} />
            <span className="chat-fab-text">Habla con Comfi</span>
          </div>
        )}
      </button>

      {/* Chat Widget */}
      <ChatWidget isOpen={isChatOpen} onClose={closeChat} />
    </div>
  )
}

export default Layout
