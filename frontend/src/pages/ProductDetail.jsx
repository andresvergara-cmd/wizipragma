import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { mockProducts } from '../data/mockProducts'
import './ProductDetail.css'

const ProductDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const product = mockProducts.find(p => p.id === id)
  const [quantity, setQuantity] = useState(1)
  const [activeTab, setActiveTab] = useState('description')
  const [imageError, setImageError] = useState(false)

  if (!product) {
    return (
      <div className="product-detail">
        <div className="product-detail-container">
          <div className="no-results">
            <div className="no-results-icon">❌</div>
            <h3>Producto no encontrado</h3>
            <button className="btn btn-primary" onClick={() => navigate('/marketplace')}>
              Volver al Marketplace
            </button>
          </div>
        </div>
      </div>
    )
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
      minimumFractionDigits: 0
    }).format(price)
  }

  const discountPercentage = product.originalPrice 
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0

  const savings = product.originalPrice ? product.originalPrice - product.price : 0

  const handleBuy = () => {
    alert(`¡Comprando ${quantity} unidad(es) de ${product.name}!`)
  }

  const handleChatAboutProduct = () => {
    alert('Abriendo chat con CENTLI para hablar sobre este producto...')
  }

  const handleImageError = () => {
    setImageError(true)
  }

  return (
    <div className="product-detail">
      <div className="product-detail-container">
        <div className="back-button" onClick={() => navigate(-1)}>
          <span>←</span>
          <span>Volver</span>
        </div>

        <div className="product-detail-content">
          <div className="product-detail-grid">
            {/* Image Section */}
            <div className="product-image-section">
              <div className="main-image-container">
                {imageError ? (
                  <div className="product-image-placeholder-large">
                    <div className="placeholder-icon-large">📦</div>
                    <div className="placeholder-text-large">{product.brand}</div>
                    <div className="placeholder-subtext">{product.name}</div>
                  </div>
                ) : (
                  <img 
                    src={product.image} 
                    alt={product.name} 
                    className="main-image"
                    onError={handleImageError}
                    loading="lazy"
                  />
                )}
              </div>
            </div>

            {/* Info Section */}
            <div className="product-info-section">
              <div className="product-brand-tag">{product.brand}</div>
              
              <h1 className="product-title">{product.name}</h1>

              <div className="product-rating-section">
                <div className="rating-display">
                  <span className="rating-stars">⭐ {product.rating}</span>
                  <span className="rating-reviews">({product.reviews} reseñas)</span>
                </div>
                {product.seller?.verified && (
                  <div className="seller-info">
                    <span className="seller-verified">✓</span>
                    <span>{product.seller.name}</span>
                  </div>
                )}
              </div>

              <p className="product-description">{product.description}</p>

              {/* Price Section */}
              <div className="product-price-section">
                <div className="price-display">
                  <span className="current-price-large">{formatPrice(product.price)}</span>
                  {product.originalPrice && (
                    <span className="original-price-large">{formatPrice(product.originalPrice)}</span>
                  )}
                </div>
                {savings > 0 && (
                  <div className="savings-badge">
                    Ahorras {formatPrice(savings)} ({discountPercentage}% OFF)
                  </div>
                )}
              </div>

              {/* Benefits */}
              {product.benefits && product.benefits.length > 0 && (
                <div className="benefits-section">
                  <h3>Beneficios Exclusivos</h3>
                  <div className="benefits-list">
                    {product.benefits.map((benefit, index) => (
                      <div key={index} className="benefit-item">
                        <span className="benefit-icon-large">
                          {benefit.type === 'CASHBACK' && '💰'}
                          {benefit.type === 'MSI' && '📅'}
                          {benefit.type === 'DISCOUNT' && '🏷️'}
                        </span>
                        <div className="benefit-details">
                          <h4>{benefit.description}</h4>
                          {benefit.type === 'CASHBACK' && (
                            <p>Recibes {formatPrice(benefit.amount)} de vuelta</p>
                          )}
                          {benefit.type === 'MSI' && (
                            <p>{formatPrice(benefit.monthlyPayment)}/mes</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Purchase Section */}
              <div className="purchase-section">
                <div className="quantity-selector">
                  <label>Cantidad:</label>
                  <div className="quantity-controls">
                    <button 
                      className="quantity-btn"
                      onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    >
                      −
                    </button>
                    <div className="quantity-display">{quantity}</div>
                    <button 
                      className="quantity-btn"
                      onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                    >
                      +
                    </button>
                  </div>
                  <span className="stock-info">
                    {product.stock > 0 ? `${product.stock} disponibles` : 'Agotado'}
                  </span>
                </div>

                <div className="purchase-actions">
                  <button 
                    className="btn btn-primary btn-buy"
                    onClick={handleBuy}
                    disabled={product.stock === 0}
                  >
                    🛒 Comprar Ahora
                  </button>
                  <button 
                    className="btn btn-secondary btn-chat"
                    onClick={handleChatAboutProduct}
                  >
                    💬 Preguntar a CENTLI
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Tabs Section */}
          <div className="product-tabs">
            <div className="tabs-header">
              <button 
                className={`tab-button ${activeTab === 'description' ? 'active' : ''}`}
                onClick={() => setActiveTab('description')}
              >
                Descripción
              </button>
              <button 
                className={`tab-button ${activeTab === 'features' ? 'active' : ''}`}
                onClick={() => setActiveTab('features')}
              >
                Características
              </button>
              <button 
                className={`tab-button ${activeTab === 'benefits' ? 'active' : ''}`}
                onClick={() => setActiveTab('benefits')}
              >
                Beneficios
              </button>
            </div>

            <div className="tab-content">
              {activeTab === 'description' && (
                <div>
                  <h3>Descripción del Producto</h3>
                  <p>{product.description}</p>
                </div>
              )}

              {activeTab === 'features' && (
                <div>
                  <h3>Características Principales</h3>
                  <div className="features-list">
                    {product.features?.map((feature, index) => (
                      <div key={index} className="feature-item">
                        <span className="feature-icon">✓</span>
                        <span className="feature-text">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'benefits' && (
                <div>
                  <h3>Todos los Beneficios</h3>
                  <div className="benefits-list">
                    {product.benefits?.map((benefit, index) => (
                      <div key={index} className="benefit-item">
                        <span className="benefit-icon-large">
                          {benefit.type === 'CASHBACK' && '💰'}
                          {benefit.type === 'MSI' && '📅'}
                          {benefit.type === 'DISCOUNT' && '🏷️'}
                        </span>
                        <div className="benefit-details">
                          <h4>{benefit.description}</h4>
                          <p>
                            {benefit.type === 'CASHBACK' && `Recibes ${formatPrice(benefit.amount)} de vuelta`}
                            {benefit.type === 'MSI' && `Paga en ${benefit.months.join(', ')} meses sin intereses`}
                            {benefit.type === 'DISCOUNT' && `Descuento de ${formatPrice(benefit.amount)}`}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductDetail
