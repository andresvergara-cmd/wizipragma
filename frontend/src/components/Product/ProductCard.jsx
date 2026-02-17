import { Link } from 'react-router-dom'
import './ProductCard.css'

const ProductCard = ({ product }) => {
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

  return (
    <Link to={`/product/${product.id}`} className="product-card">
      <div className="product-image-container">
        <img src={product.image} alt={product.name} className="product-image" />
        {discountPercentage > 0 && (
          <div className="discount-badge">-{discountPercentage}%</div>
        )}
        {product.seller?.verified && (
          <div className="verified-badge">✓ Verificado</div>
        )}
      </div>

      <div className="product-content">
        <div className="product-brand">{product.brand}</div>
        <h3 className="product-name">{product.name}</h3>
        
        <div className="product-rating">
          <span className="rating-stars">⭐ {product.rating}</span>
          <span className="rating-count">({product.reviews})</span>
        </div>

        <div className="product-pricing">
          {product.originalPrice && (
            <span className="original-price">{formatPrice(product.originalPrice)}</span>
          )}
          <span className="current-price">{formatPrice(product.price)}</span>
        </div>

        {product.benefits && product.benefits.length > 0 && (
          <div className="product-benefits">
            {product.benefits.slice(0, 2).map((benefit, index) => (
              <div key={index} className={`benefit-badge benefit-${benefit.type.toLowerCase()}`}>
                <span className="benefit-icon">
                  {benefit.type === 'CASHBACK' && '💰'}
                  {benefit.type === 'MSI' && '📅'}
                  {benefit.type === 'DISCOUNT' && '🏷️'}
                  {benefit.type === 'POINTS' && '⭐'}
                </span>
                <span className="benefit-text">
                  {benefit.type === 'CASHBACK' && `${benefit.value}% Cashback`}
                  {benefit.type === 'MSI' && `${Math.max(...benefit.months)} MSI`}
                  {benefit.type === 'DISCOUNT' && `${benefit.value}% OFF`}
                  {benefit.type === 'POINTS' && `${benefit.value}x Puntos`}
                </span>
              </div>
            ))}
          </div>
        )}

        {product.stock < 10 && product.stock > 0 && (
          <div className="stock-warning">
            ⚠️ Solo quedan {product.stock} unidades
          </div>
        )}
      </div>
    </Link>
  )
}

export default ProductCard
