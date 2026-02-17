import { useState } from 'react'
import './Transactions.css'

// Mock transactions data
const mockTransactions = [
  {
    id: 'tx-001',
    type: 'purchase',
    title: 'Compra - MacBook Pro 14" M3',
    description: 'Apple Store Oficial',
    amount: -45999,
    date: '2026-02-17T10:30:00',
    status: 'completed',
    icon: '🛒'
  },
  {
    id: 'tx-002',
    type: 'transfer',
    title: 'Transferencia a Juan Pérez',
    description: 'Pago de cena',
    amount: -500,
    date: '2026-02-16T18:45:00',
    status: 'completed',
    icon: '💸'
  },
  {
    id: 'tx-003',
    type: 'payment',
    title: 'Cashback recibido',
    description: 'iPhone 15 Pro - 8%',
    amount: 2320,
    date: '2026-02-15T14:20:00',
    status: 'completed',
    icon: '💰'
  },
  {
    id: 'tx-004',
    type: 'purchase',
    title: 'Compra - Sony WH-1000XM5',
    description: 'Sony Store',
    amount: -7999,
    date: '2026-02-14T11:15:00',
    status: 'completed',
    icon: '🛒'
  },
  {
    id: 'tx-005',
    type: 'transfer',
    title: 'Transferencia a María García',
    description: 'Renta departamento',
    amount: -8000,
    date: '2026-02-13T09:00:00',
    status: 'pending',
    icon: '💸'
  }
]

const Transactions = () => {
  const [filter, setFilter] = useState('all')

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
      minimumFractionDigits: 0
    }).format(Math.abs(price))
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('es-MX', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  }

  const filteredTransactions = filter === 'all' 
    ? mockTransactions 
    : mockTransactions.filter(tx => tx.type === filter)

  return (
    <div className="transactions">
      <div className="transactions-container">
        <div className="transactions-header">
          <h1>Mis Transacciones</h1>
          <p>Historial completo de tus movimientos financieros</p>
        </div>

        <div className="transactions-filters">
          <button 
            className={`filter-button ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            Todas
          </button>
          <button 
            className={`filter-button ${filter === 'purchase' ? 'active' : ''}`}
            onClick={() => setFilter('purchase')}
          >
            🛒 Compras
          </button>
          <button 
            className={`filter-button ${filter === 'transfer' ? 'active' : ''}`}
            onClick={() => setFilter('transfer')}
          >
            💸 Transferencias
          </button>
          <button 
            className={`filter-button ${filter === 'payment' ? 'active' : ''}`}
            onClick={() => setFilter('payment')}
          >
            💰 Pagos Recibidos
          </button>
        </div>

        {filteredTransactions.length > 0 ? (
          <div className="transactions-list">
            {filteredTransactions.map(transaction => (
              <div key={transaction.id} className="transaction-card">
                <div className={`transaction-icon ${transaction.type}`}>
                  {transaction.icon}
                </div>

                <div className="transaction-info">
                  <h3 className="transaction-title">{transaction.title}</h3>
                  <div className="transaction-details">
                    <span className="transaction-detail">
                      📅 {formatDate(transaction.date)}
                    </span>
                    <span className="transaction-detail">
                      📝 {transaction.description}
                    </span>
                  </div>
                </div>

                <div className="transaction-amount-section">
                  <div className={`transaction-amount ${transaction.amount > 0 ? 'positive' : 'negative'}`}>
                    {transaction.amount > 0 ? '+' : '-'}{formatPrice(transaction.amount)}
                  </div>
                  <span className={`transaction-status ${transaction.status}`}>
                    {transaction.status === 'completed' && '✓ Completada'}
                    {transaction.status === 'pending' && '⏳ Pendiente'}
                    {transaction.status === 'failed' && '✗ Fallida'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-transactions">
            <div className="empty-icon">📭</div>
            <h3>No hay transacciones</h3>
            <p>No se encontraron transacciones con los filtros seleccionados</p>
            <button className="btn btn-primary" onClick={() => setFilter('all')}>
              Ver Todas
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Transactions
