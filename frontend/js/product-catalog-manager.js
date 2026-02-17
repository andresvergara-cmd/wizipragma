// Product Catalog Manager - Displays products and benefits
class ProductCatalogManager {
  constructor(appState) {
    this.appState = appState;
    this.catalogContainer = null;
  }

  init() {
    this.catalogContainer = document.getElementById('product-catalog');
    this.appState.subscribe((state) => {
      if (state.products.length > 0) {
        this.renderProducts(state.products);
      }
    });
    
    Logger.log('ProductCatalog', 'Product catalog manager initialized');
  }

  renderProducts(products) {
    if (!this.catalogContainer) return;
    
    this.catalogContainer.innerHTML = '<h5>Productos Disponibles</h5>';
    
    const row = document.createElement('div');
    row.className = 'row';
    
    products.forEach(product => {
      const col = document.createElement('div');
      col.className = 'col-md-4 mb-3';
      col.innerHTML = `
        <div class="card" data-testid="product-catalog-item-${product.id}">
          <div class="card-body">
            <h6 class="card-title">${product.name}</h6>
            <p class="card-text">${product.description || ''}</p>
            <p class="text-primary">$${product.price || '0.00'}</p>
            ${product.benefits ? `<small class="text-muted">${product.benefits}</small>` : ''}
            <button class="btn btn-sm btn-primary mt-2" onclick="window.productCatalogManager.selectProduct('${product.id}')">
              Ver Detalles
            </button>
          </div>
        </div>
      `;
      row.appendChild(col);
    });
    
    this.catalogContainer.appendChild(row);
  }

  selectProduct(productId) {
    const state = this.appState.getState();
    const product = state.products.find(p => p.id === productId);
    
    if (product) {
      this.appState.setState({ selectedProduct: product });
      this.showToast(`Producto seleccionado: ${product.name}`, 'info');
      
      // Send to agent
      window.wsManager.send({
        action: 'product_selected',
        product_id: productId,
        user_id: state.user.id,
        session_id: state.user.sessionId
      });
    }
  }

  showToast(message, type) {
    window.dispatchEvent(new CustomEvent('show-toast', { detail: { message, type } }));
  }
}

window.ProductCatalogManager = ProductCatalogManager;
