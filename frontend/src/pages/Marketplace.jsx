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

  useEffect(() => {
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
  }, [selectedCategory, searchTerm, sortBy])

  const handleCategoryChange = (category) => {
    setSelectedCategory(category)
    if (category === 'all') {
      searchParams.delete('category')
    } else {
      searchParams.set('category', category)
    }
    setSearchParams(searchParams)
  }

  return (
    <div className="marketplace">
      <div className="marketplace-header">
        <h1>Marketplace CENTLI</h1>
        <p>Descubre productos exclusivos con beneficios increíbles</p>
      </div>

      <div className="marketplace-container">
        {/* Sidebar Filters */}
        <aside className="marketplace-sidebar">
          <div className="filter-section">
            <h3>Categorías</h3>
            <div className="category-filters">
              <button
                className={`category-filter ${selectedCategory === 'all' ? 'active' : ''}`}
                onClick={() => handleCategoryChange('all')}
              >
                <span>🛍️</span>
                <span>Todas</span>
              </button>
              {categories.map(cat => (
                <button
                  key={cat.id}
                  className={`category-filter ${selectedCategory === cat.id ? 'active' : ''}`}
                  onClick={() => handleCategoryChange(cat.id)}
                >
                  <span>{cat.icon}</span>
                  <span>{cat.name}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="filter-section">
            <h3>Beneficios</h3>
            <div className="benefit-filters">
              <label className="filter-checkbox">
                <input type="checkbox" />
                <span>💰 Cashback</span>
              </label>
              <label className="filter-checkbox">
                <input type="checkbox" />
                <span>📅 Meses sin intereses</span>
              </label>
              <label className="filter-checkbox">
                <input type="checkbox" />
                <span>🏷️ Descuentos</span>
              </label>
            </div>
          </div>

          <div className="filter-section">
            <h3>Rango de Precio</h3>
            <div className="price-range">
              <input type="number" placeholder="Min" className="price-input" />
              <span>-</span>
              <input type="number" placeholder="Max" className="price-input" />
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
                placeholder="Buscar productos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
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

          {/* Results Count */}
          <div className="results-info">
            <p>
              Mostrando <strong>{filteredProducts.length}</strong> productos
              {selectedCategory !== 'all' && (
                <span> en <strong>{categories.find(c => c.id === selectedCategory)?.name}</strong></span>
              )}
            </p>
          </div>

          {/* Products Grid */}
          {filteredProducts.length > 0 ? (
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
              <button className="btn btn-primary" onClick={() => {
                setSearchTerm('')
                setSelectedCategory('all')
              }}>
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
