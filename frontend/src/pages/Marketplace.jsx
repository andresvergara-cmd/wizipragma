import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import ProductCard from '../components/Product/ProductCard'
import { mockProducts, categories } from '../data/mockProducts'
import './Marketplace.css'

const Marketplace = () => {
  const [searchParams, setSearchParams] = useSearchParams()
  const [filteredProducts, setFilteredProducts] = useState(mockProducts)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || 'all')
  const [sortBy, setSortBy] = useState('featured')
  const [selectedBenefits, setSelectedBenefits] = useState([])
  const [priceRange, setPriceRange] = useState({ min: '', max: '' })
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    setIsLoading(true)
    
    // Simulate loading delay for better UX
    setTimeout(() => {
      let filtered = [...mockProducts]

      // Filter by category
      if (selectedCategory !== 'all') {
        filtered = filtered.filter(p => 
          p.category.toLowerCase() === selectedCategory.toLowerCase()
        )
      }

      // Filter by search term
      if (searchTerm) {
        filtered = filtered.filter(p =>
          p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          p.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
          p.brand.toLowerCase().includes(searchTerm.toLowerCase())
        )
      }

      // Filter by benefits
      if (selectedBenefits.length > 0) {
        filtered = filtered.filter(p =>
          p.benefits?.some(b => selectedBenefits.includes(b.type))
        )
      }

      // Filter by price range
      if (priceRange.min) {
        filtered = filtered.filter(p => p.price >= Number(priceRange.min))
      }
      if (priceRange.max) {
        filtered = filtered.filter(p => p.price <= Number(priceRange.max))
      }

      // Sort products
      switch (sortBy) {
        case 'price-asc':
          filtered.sort((a, b) => a.price - b.price)
          break
        case 'price-desc':
          filtered.sort((a, b) => b.price - a.price)
          break
        case 'rating':
          filtered.sort((a, b) => b.rating - a.rating)
          break
        case 'discount':
          filtered.sort((a, b) => {
            const discountA = a.originalPrice ? ((a.originalPrice - a.price) / a.originalPrice) : 0
            const discountB = b.originalPrice ? ((b.originalPrice - b.price) / b.originalPrice) : 0
            return discountB - discountA
          })
          break
        default:
          // featured - keep original order
          break
      }

      setFilteredProducts(filtered)
      setIsLoading(false)
    }, 300)
  }, [selectedCategory, searchTerm, sortBy, selectedBenefits, priceRange])

  const handleCategoryChange = (category) => {
    setSelectedCategory(category)
    if (category === 'all') {
      searchParams.delete('category')
    } else {
      searchParams.set('category', category)
    }
    setSearchParams(searchParams)
  }

  const handleBenefitToggle = (benefitType) => {
    setSelectedBenefits(prev =>
      prev.includes(benefitType)
        ? prev.filter(b => b !== benefitType)
        : [...prev, benefitType]
    )
  }

  const clearAllFilters = () => {
    setSearchTerm('')
    setSelectedCategory('all')
    setSelectedBenefits([])
    setPriceRange({ min: '', max: '' })
    setSortBy('featured')
  }

  return (
    <div className="marketplace">
      {/* Promotional Banner */}
      <div className="promo-banner">
        <div className="promo-content">
          <span className="promo-icon">🎉</span>
          <span className="promo-text">
            <strong>¡Ofertas Especiales!</strong> Hasta 15% de cashback en productos seleccionados
          </span>
          <span className="promo-badge">Válido hasta fin de mes</span>
        </div>
      </div>

      <div className="marketplace-header">
        <h1>Marketplace CENTLI</h1>
        <p>Descubre productos exclusivos con beneficios increíbles</p>
        
        {/* Breadcrumbs */}
        <div className="breadcrumbs">
          <span>Inicio</span>
          <span className="separator">›</span>
          <span>Marketplace</span>
          {selectedCategory !== 'all' && (
            <>
              <span className="separator">›</span>
              <span className="active">{categories.find(c => c.id === selectedCategory)?.name}</span>
            </>
          )}
        </div>
      </div>

      <div className="marketplace-container">
        {/* Sidebar Filters */}
        <aside className="marketplace-sidebar">
          <div className="filter-header">
            <h3>Filtros</h3>
            {(selectedCategory !== 'all' || selectedBenefits.length > 0 || priceRange.min || priceRange.max) && (
              <button className="clear-filters" onClick={clearAllFilters}>
                Limpiar todo
              </button>
            )}
          </div>

          <div className="filter-section">
            <h3>Categorías</h3>
            <div className="category-filters">
              <button
                className={`category-filter ${selectedCategory === 'all' ? 'active' : ''}`}
                onClick={() => handleCategoryChange('all')}
              >
                <span>🛍️</span>
                <span>Todas</span>
                <span className="count">{mockProducts.length}</span>
              </button>
              {categories.map(cat => {
                const count = mockProducts.filter(p => p.category.toLowerCase() === cat.id).length
                return (
                  <button
                    key={cat.id}
                    className={`category-filter ${selectedCategory === cat.id ? 'active' : ''}`}
                    onClick={() => handleCategoryChange(cat.id)}
                  >
                    <span>{cat.icon}</span>
                    <span>{cat.name}</span>
                    <span className="count">{count}</span>
                  </button>
                )
              })}
            </div>
          </div>

          <div className="filter-section">
            <h3>Beneficios</h3>
            <div className="benefit-filters">
              <label className="filter-checkbox">
                <input 
                  type="checkbox" 
                  checked={selectedBenefits.includes('CASHBACK')}
                  onChange={() => handleBenefitToggle('CASHBACK')}
                />
                <span className="checkbox-custom"></span>
                <span>💰 Cashback</span>
              </label>
              <label className="filter-checkbox">
                <input 
                  type="checkbox"
                  checked={selectedBenefits.includes('MSI')}
                  onChange={() => handleBenefitToggle('MSI')}
                />
                <span className="checkbox-custom"></span>
                <span>📅 Meses sin intereses</span>
              </label>
              <label className="filter-checkbox">
                <input 
                  type="checkbox"
                  checked={selectedBenefits.includes('DISCOUNT')}
                  onChange={() => handleBenefitToggle('DISCOUNT')}
                />
                <span className="checkbox-custom"></span>
                <span>🏷️ Descuentos</span>
              </label>
            </div>
          </div>

          <div className="filter-section">
            <h3>Rango de Precio</h3>
            <div className="price-range">
              <input 
                type="number" 
                placeholder="Mín" 
                className="price-input"
                value={priceRange.min}
                onChange={(e) => setPriceRange(prev => ({ ...prev, min: e.target.value }))}
              />
              <span>-</span>
              <input 
                type="number" 
                placeholder="Máx" 
                className="price-input"
                value={priceRange.max}
                onChange={(e) => setPriceRange(prev => ({ ...prev, max: e.target.value }))}
              />
            </div>
            <div className="price-suggestions">
              <button onClick={() => setPriceRange({ min: '', max: '10000' })}>Hasta $10,000</button>
              <button onClick={() => setPriceRange({ min: '10000', max: '30000' })}>$10,000 - $30,000</button>
              <button onClick={() => setPriceRange({ min: '30000', max: '' })}>Más de $30,000</button>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="marketplace-main">
          {/* Search and Sort Bar */}
          <div className="marketplace-controls">
            <div className="search-bar">
              <span className="search-icon">🔍</span>
              <input
                type="text"
                placeholder="Buscar productos, marcas..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              {searchTerm && (
                <button className="clear-search" onClick={() => setSearchTerm('')}>
                  ✕
                </button>
              )}
            </div>

            <div className="sort-controls">
              <label htmlFor="sort">Ordenar por:</label>
              <select
                id="sort"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="sort-select"
              >
                <option value="featured">Destacados</option>
                <option value="price-asc">Precio: Menor a Mayor</option>
                <option value="price-desc">Precio: Mayor a Menor</option>
                <option value="rating">Mejor Calificados</option>
                <option value="discount">Mayor Descuento</option>
              </select>
            </div>
          </div>

          {/* Active Filters */}
          {(selectedBenefits.length > 0 || priceRange.min || priceRange.max) && (
            <div className="active-filters">
              <span className="active-filters-label">Filtros activos:</span>
              {selectedBenefits.map(benefit => (
                <span key={benefit} className="active-filter-tag">
                  {benefit === 'CASHBACK' && '💰 Cashback'}
                  {benefit === 'MSI' && '📅 MSI'}
                  {benefit === 'DISCOUNT' && '🏷️ Descuentos'}
                  <button onClick={() => handleBenefitToggle(benefit)}>✕</button>
                </span>
              ))}
              {(priceRange.min || priceRange.max) && (
                <span className="active-filter-tag">
                  💵 {priceRange.min || '0'} - {priceRange.max || '∞'}
                  <button onClick={() => setPriceRange({ min: '', max: '' })}>✕</button>
                </span>
              )}
            </div>
          )}

          {/* Results Count */}
          <div className="results-info">
            <p>
              {isLoading ? (
                'Buscando productos...'
              ) : (
                <>
                  Mostrando <strong>{filteredProducts.length}</strong> {filteredProducts.length === 1 ? 'producto' : 'productos'}
                  {selectedCategory !== 'all' && (
                    <span> en <strong>{categories.find(c => c.id === selectedCategory)?.name}</strong></span>
                  )}
                </>
              )}
            </p>
          </div>

          {/* Products Grid or Skeleton */}
          {isLoading ? (
            <div className="products-grid">
              {[1, 2, 3, 4, 5, 6].map(i => (
                <div key={i} className="skeleton-card">
                  <div className="skeleton-image"></div>
                  <div className="skeleton-content">
                    <div className="skeleton-line short"></div>
                    <div className="skeleton-line"></div>
                    <div className="skeleton-line medium"></div>
                    <div className="skeleton-badges">
                      <div className="skeleton-badge"></div>
                      <div className="skeleton-badge"></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : filteredProducts.length > 0 ? (
            <div className="products-grid">
              {filteredProducts.map(product => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          ) : (
            <div className="no-results">
              <div className="no-results-icon">🔍</div>
              <h3>No se encontraron productos</h3>
              <p>Intenta ajustar tus filtros o búsqueda</p>
              <button className="btn btn-primary" onClick={clearAllFilters}>
                Limpiar Filtros
              </button>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default Marketplace
