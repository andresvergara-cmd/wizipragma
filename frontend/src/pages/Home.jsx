import { Link } from 'react-router-dom'
import CinteotlLogo from '../components/Logo/CinteotlLogo'
import '../components/Logo/CinteotlLogo.css'
import './Home.css'

const Home = () => {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              <CinteotlLogo size={60} className="cinteotl-logo hero-icon" />
              Bienvenido a CENTLI
            </h1>
            <p className="hero-subtitle">
              Tu coach financiero inteligente con IA
            </p>
            <p className="hero-description">
              Descubre productos exclusivos, obtén beneficios increíbles y gestiona tus finanzas 
              de manera conversacional con la ayuda de inteligencia artificial.
            </p>
            <div className="hero-actions">
              <Link to="/marketplace" className="btn btn-primary">
                Explorar Marketplace
              </Link>
              <button className="btn btn-secondary">
                Hablar con CENTLI
              </button>
            </div>
          </div>
          <div className="hero-image">
            <CinteotlLogo size={240} className="cinteotl-logo hero-owl" />
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="benefits">
        <h2 className="section-title">¿Por qué elegir CENTLI?</h2>
        <div className="benefits-grid">
          <div className="benefit-card">
            <div className="benefit-icon">💰</div>
            <h3>Cashback Exclusivo</h3>
            <p>Hasta 15% de cashback en productos seleccionados</p>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">📅</div>
            <h3>Meses Sin Intereses</h3>
            <p>Hasta 24 meses sin intereses en tus compras</p>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">🤖</div>
            <h3>Asistente IA</h3>
            <p>Coach financiero disponible 24/7 para ayudarte</p>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">🎯</div>
            <h3>Ofertas Personalizadas</h3>
            <p>Recomendaciones basadas en tus preferencias</p>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="featured">
        <h2 className="section-title">Productos Destacados</h2>
        <div className="featured-grid">
          <div className="featured-card">
            <img src="https://dummyimage.com/800x600/6B46C1/ffffff&text=MacBook+Pro+M3" alt="MacBook Pro" />
            <div className="featured-content">
              <h3>MacBook Pro 14" M3</h3>
              <p className="featured-price">$45,999</p>
              <span className="featured-badge">5% Cashback</span>
            </div>
          </div>
          <div className="featured-card">
            <img src="https://dummyimage.com/800x600/AD37E0/ffffff&text=iPhone+15+Pro" alt="iPhone 15 Pro" />
            <div className="featured-content">
              <h3>iPhone 15 Pro 256GB</h3>
              <p className="featured-price">$28,999</p>
              <span className="featured-badge">8% Cashback</span>
            </div>
          </div>
          <div className="featured-card">
            <img src="https://dummyimage.com/800x600/E91E63/ffffff&text=Sony+WH-1000XM5" alt="Sony WH-1000XM5" />
            <div className="featured-content">
              <h3>Sony WH-1000XM5</h3>
              <p className="featured-price">$7,999</p>
              <span className="featured-badge">15% Cashback</span>
            </div>
          </div>
        </div>
        <div className="featured-action">
          <Link to="/marketplace" className="btn btn-outline">
            Ver Todos los Productos
          </Link>
        </div>
      </section>

      {/* Categories */}
      <section className="categories">
        <h2 className="section-title">Explora por Categoría</h2>
        <div className="categories-grid">
          <Link to="/marketplace?category=tech" className="category-card">
            <div className="category-icon">💻</div>
            <h3>Tecnología</h3>
          </Link>
          <Link to="/marketplace?category=gaming" className="category-card">
            <div className="category-icon">🎮</div>
            <h3>Gaming</h3>
          </Link>
          <Link to="/marketplace?category=home" className="category-card">
            <div className="category-icon">🏠</div>
            <h3>Hogar</h3>
          </Link>
          <Link to="/marketplace?category=fashion" className="category-card">
            <div className="category-icon">👔</div>
            <h3>Moda</h3>
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home
